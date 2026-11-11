"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Pandoc protection.

Mandatory Pandoc structural protection with exact original spans (order 013-a).

The proxy's structural protection path parses each completed answer with the
pinned installed Pandoc binary using an explicit reader profile.  Pandoc's
``sourcepos`` reader extension records source positions on the parsed nodes:
generated wrapper ``Div``/``Span`` nodes carry a ``data-pos`` attribute, as do
position-carrying elements (``CodeBlock``, ``Code``, ``Link``, ``Image``,
``Header``).  Positions are 1-based line/column pairs over the
NFC-normalized document; columns are Unicode code-point columns (a tab
advances to the next tab stop).

Deny by default: only ``Str`` leaf spans whose position is proven against
the unmodified original (valid coordinates, exact original-slice equality,
grapheme-safe, NFC-stable line) are granted as editable prose, plus
whitespace glue only inside a proven shared prose context (between two
granted, contiguous prose spans).  Everything else - code, math, HTML,
links and images (including labels), configuration, metadata, markers,
soft breaks, escapes, entities and every unprovable region - is protected.
Residual machine-content recognizers (``protection_residuals``) then refine
the granted prose; any residual match overlapping granted prose is retained.

Protected extents are proven in physical source order (order 033-a): the
walk collects exact-source candidate grants and structural context events
(literal and entity quotation markers, complete raw opening/closing tags)
with their proven positions, and one document-level finalization coalesces
equivalent physical events (a footnote definition referenced several times
duplicates one physical payload), sorts the events by proven original
position, replays the quote and HTML context stacks, and filters the
candidate grants by the resulting denied intervals before any outcome
reaches detection.  A complete BlockQuote (lazy continuation and nesting
included) is denied in full.  A quotation or tag extent whose closure is
unproved protects to the end of the document.

No substring matching is used for position recovery and no AST-to-Markdown
rendering is used for answers; edits apply to validated original coordinates
with unchanged unapproved slices.
"""

from __future__ import annotations

import bisect
import contextlib
import json
import os
import re
import selectors
import shutil
import signal
import subprocess
import time
import unicodedata
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

import request_lifecycle
from config import (
    PANDOC_ENV_VAR,
    PANDOC_MAX_BLOCKS,
    PANDOC_MAX_INLINES,
    PANDOC_MAX_INPUT_BYTES,
    PANDOC_MAX_OUTPUT_BYTES,
    PANDOC_READER,
    PANDOC_TIMEOUT_SECONDS,
    PANDOC_VERSION,
    PANDOC_WRITER,
)

if TYPE_CHECKING:
    from io import BufferedIOBase

    from protected import Interval

# Finite reason vocabulary (bounded, content-free diagnostics).
REASON_NOT_FOUND = "PANDOC_NOT_FOUND"
REASON_NOT_EXECUTABLE = "PANDOC_NOT_EXECUTABLE"
REASON_WRONG_VERSION = "PANDOC_WRONG_VERSION"
REASON_TIMEOUT = "PANDOC_TIMEOUT"
REASON_BAD_EXIT = "PANDOC_BAD_EXIT"
REASON_OUTPUT_TOO_LARGE = "PANDOC_OUTPUT_TOO_LARGE"
REASON_MALFORMED_OUTPUT = "PANDOC_MALFORMED_OUTPUT"
REASON_CAPABILITY = "PANDOC_CAPABILITY"
REASON_INPUT_TOO_LARGE = "PANDOC_INPUT_TOO_LARGE"
REASON_SCHEMA = "PANDOC_SCHEMA"
REASON_NODE_LIMIT = "PANDOC_NODE_LIMIT"
REASON_MAP_INTEGRITY = "PANDOC_MAP_INTEGRITY"

_CHUNK = 65536

_VERSION_RE = re.compile(r"^pandoc (\d+(?:\.\d+)+)\s*$")
# stdin profile: bare "L:C-L:C" (no input-path prefix).
_POS_RE = re.compile(r"^(\d+):(\d+)-(\d+):(\d+)$")

# Elements that carry a generated data-pos directly in their own attributes.
_DIRECT_POSITIONED = {"CodeBlock", "Code", "Link", "Image", "Header"}

_ZWJ = "\u200d"
_ZWNJ = "\u200c"
_WHITESPACE_SLICE = frozenset(" \t")
_EMPH_KINDS = frozenset({"emph", "strong", "strikeout", "superscript", "subscript"})


def _find_positioned_str(node: object, position: str, content: str) -> bool:
    """True when a wrapper Span at exactly ``position`` holds one Str leaf.

    Searches the whole subtree so the startup capability probe does not
    depend on a brittle block-index chain (e.g. the Para between the
    document wrapper Div and the inline wrapper Spans).
    """
    if isinstance(node, dict):
        if node.get("t") == "Span":
            payload = node.get("c")
            if isinstance(payload, list) and len(payload) == 2:
                attrs = _node_attrs(node)
                if [value for key, value in attrs if key == "data-pos"] == [position]:
                    inlines = payload[1]
                    if (
                        isinstance(inlines, list)
                        and len(inlines) == 1
                        and isinstance(inlines[0], dict)
                        and inlines[0].get("t") == "Str"
                        and inlines[0].get("c") == content
                    ):
                        return True
        for child in (node.get("c"),):
            if isinstance(child, (list, dict)) and _find_positioned_str(
                child, position, content
            ):
                    return True
    elif isinstance(node, list):
        for child in node:
            if _find_positioned_str(child, position, content):
                return True
    return False


# Quotation families (order 033-a, requirement 3): the literal opener code
# point determines the family and the exact compatible closer.  The forms
# cover the Slovenian low/high pair („...“), both guillemet directions
# (»...« and «...»), the established straight and curly double forms, and
# the relevant single forms (straight, curly, both single-guillemet
# directions).  Only a proved compatible closer releases its own opener;
# a mismatched, escaped or entity-normalized marker can never release a
# different outer context, and prose inside a quotation whose extent is
# unproved stays protected (order 013-a, requirement 16, repaired).
_QUOTE_FAMILIES: dict[str, tuple[str, str]] = {
    "\u201e": ("lowhigh-double", "\u201c"),
    "\u201c": ("curly-double", "\u201d"),
    "\u00ab": ("guillemet-double-inward", "\u00bb"),
    "\u00bb": ("guillemet-double-outward", "\u00ab"),
    '"': ("straight-double", '"'),
    "\u2018": ("curly-single", "\u2019"),
    "'": ("straight-single", "'"),
    "\u2039": ("guillemet-single-inward", "\u203a"),
    "\u203a": ("guillemet-single-outward", "\u2039"),
}
_QUOTE_CHARS = frozenset(_QUOTE_FAMILIES) | frozenset(
    closer for _family, closer in _QUOTE_FAMILIES.values()
)
# Established in-word apostrophe: a straight delimiter flanked by word
# characters on both sides is ordinary punctuation, not a quotation
# marker (order 013-a), and follows the normal grant path.
_FLANK_CHECK_CHARS = frozenset('"\u0027')
# Unicode mark categories: any combining mark attaches to a neighboring base
# code point, so a boundary at a mark position is unproved.  This includes
# class-0 marks such as U+034F (COMBINING GRAPHEME JOIN MARK), which
# ``unicodedata.combining`` alone would miss.
_MARK_CATEGORIES = frozenset({"Mn", "Mc", "Me"})


def grapheme_sensitive(char: str) -> bool:
    code = ord(char)
    if code < 32 or code == 127:
        return True
    # Unproved line-separator code points (NEL, LS, PS): a span containing
    # one cannot be proved grapheme-stable, so it is never granted.
    if code in (0x85, 0x2028, 0x2029):
        return True
    if unicodedata.category(char) in _MARK_CATEGORIES:
        return True
    if char in (_ZWJ, _ZWNJ):
        return True
    if 0xFE00 <= code <= 0xFE0F or 0xE0100 <= code <= 0xE01EF:
        return True
    if 0x1F1E6 <= code <= 0x1F1FF:
        return True
    return 0x1F3FB <= code <= 0x1F3FF


def grapheme_boundary_sensitive(char: str) -> bool:
    """True when an edit boundary adjacent to ``char`` could split a grapheme.

    Unlike ``grapheme_sensitive`` this excludes ordinary line and column
    terminators (LF, CR, tab): they form their own graphemes, so a boundary
    next to them is proved.  Only grapheme-joiners (marks, ZWJ/ZWNJ,
    variation selectors, regional indicators, emoji modifiers) and the
    exotic unproved line breaks keep the boundary unproved.
    """
    code = ord(char)
    if unicodedata.category(char) in _MARK_CATEGORIES:
        return True
    if char in (_ZWJ, _ZWNJ):
        return True
    if 0xFE00 <= code <= 0xFE0F or 0xE0100 <= code <= 0xE1EF:
        return True
    if 0x1F1E6 <= code <= 0x1F1FF or 0x1F3FB <= code <= 0x1F3FF:
        return True
    return code in (0, 0x2028, 0x2029, 0x85, 0xC)


@dataclass(frozen=True)
class PandocSpec:
    binary: str
    version: str = PANDOC_VERSION
    reader: str = PANDOC_READER
    writer: str = PANDOC_WRITER
    timeout: float = PANDOC_TIMEOUT_SECONDS
    # The one-time startup check (version + capability) gets a separate,
    # more generous budget than per-answer parses: it runs once before the
    # proxy accepts traffic and may include a cold binary start.
    startup_timeout: float = 30.0


@dataclass(frozen=True)
class ProtectionOutcome:
    ok: bool
    reason: str | None
    granted: tuple[tuple[int, int], ...] = ()
    detail: str = ""


class PandocStartupError(RuntimeError):
    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(reason if not detail else f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail


def resolve_pandoc_spec() -> PandocSpec:
    """Resolve the configured Pandoc binary (explicit variable, then PATH)."""
    configured = os.environ.get(PANDOC_ENV_VAR, "").strip()
    binary = configured or shutil.which("pandoc") or ""
    if not binary:
        raise PandocStartupError(REASON_NOT_FOUND, PANDOC_ENV_VAR)
    return PandocSpec(binary=binary)


def _pandoc_argv(spec: PandocSpec, extra: tuple[str, ...] = ()) -> list[str]:
    return [spec.binary, *extra, "-f", spec.reader, "-t", spec.writer]


def _kill_group(process: subprocess.Popen[bytes]) -> None:
    if getattr(process, "pid", None) is None:
        # Pre-allocated instance whose constructor never created a
        # child: no exact child exists to signal, and a group wait
        # would be a global wait that could touch other owned
        # children, so the never-created state returns without
        # signalling anything (order 023-a, requirement 2).
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        with contextlib.suppress(OSError):
            process.kill()
    # Honest OS-reaping wait on the exact child: if the kernel has
    # not reaped it yet, block here until it does.  The older
    # timed-wait-and-abandon could return while the owned child was
    # still alive; cleanup may honestly wait for OS reaping, with
    # no hard-real-time claim (order 023-a, requirement 2).
    with contextlib.suppress(OSError):
        process.wait()


def _run_bounded(spec: PandocSpec, args: list[str], stdin: bytes) -> tuple[int, bytes]:
    """Run one bounded Pandoc invocation (argv, no shell, capped streams).

    A single select loop multiplexes stdin writes and stdout/stderr reads,
    so a child that writes before consuming stdin cannot deadlock the
    capture.  stdout is streamed within PANDOC_MAX_OUTPUT_BYTES and the cap
    is enforced immediately; stderr is drained and never retained
    (content-free diagnostics).  Every pipe and the owned process group are
    bounded-cleaned on every exit path, including setup failures after
    launch and caller interruptions during or after the real child
    creation.  Raises PandocStartupError with a
    distinct finite reason on timeout or output-limit breach.

    Order 030-a (owned runner ONLY): the runner executes on the
    owner thread, so it consults the context-local active-scope
    cancellation check (``request_lifecycle.active_cancellation_check``,
    the same mechanism as the frozen qwen_client -> review exchange;
    a no-op outside an active request) at a loop top beside the
    deadline check; the same check also runs at the phase entry
    BEFORE the owned launch, so an observed client cancellation
    never starts the child at all (no new optional phase after an
    observed cancellation).  A cancellation observed after the
    actual child start raises
    ``request_lifecycle.RequestCancelled`` with the exact owned
    child signalled and actually reaped by the existing finally,
    and the anchored deadline, caps, the public parser API and
    every other startup semantic are untouched.
    """
    process: subprocess.Popen[bytes] | None = None
    selector = None
    try:
        # Phase-entry cancellation (order 030-a, R4): the
        # context-local active-scope check runs BEFORE the owned
        # launch, so an observed client cancellation starts no
        # child at all (no new optional phase after an observed
        # cancellation); the exact owned cleanup below is
        # unchanged for every path that did launch.
        check = request_lifecycle.active_cancellation_check()
        if check is not None and check():
            raise request_lifecycle.RequestCancelled()
        # The exact process object is owned BEFORE the fallible start
        # can create any child: with the real Popen class the
        # pre-allocated instance carries the real (unmodified) Popen
        # construction, so a caller interruption after actual child
        # creation still leaves the owning instance (and its pid)
        # reachable by the finally below for group kill and an actual
        # wait/reap instead of an orphaned child; the allocation
        # itself sits inside the owned cleanup scope, so its failure
        # leaves no child (order 023-a, requirement 2).  A transparent
        # non-class Popen replacement (a forwarding test double) has
        # no instance to pre-allocate: the direct call is the observed
        # start and ownership lands on return, preserving the
        # historical spy-observable behavior.
        popen = subprocess.Popen
        if isinstance(popen, type):
            process = popen.__new__(popen)
            try:
                popen.__init__(
                    process,
                    args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True,
                )
            except FileNotFoundError:
                raise PandocStartupError(REASON_NOT_FOUND, spec.binary) from None
            except PermissionError:
                raise PandocStartupError(REASON_NOT_EXECUTABLE, spec.binary) from None
        else:
            try:
                process = popen(
                    args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True,
                )
            except FileNotFoundError:
                raise PandocStartupError(REASON_NOT_FOUND, spec.binary) from None
            except PermissionError:
                raise PandocStartupError(REASON_NOT_EXECUTABLE, spec.binary) from None
        assert process.stdin is not None and process.stdout is not None
        assert process.stderr is not None
        # Everything after the successful Popen runs under the same
        # cleanup ownership: a setup failure (selector allocation,
        # registration, nonblocking mode) must not leak the live
        # child or its pipes.
        deadline = time.monotonic() + spec.timeout
        selector = selectors.DefaultSelector()
        in_fd = process.stdin.fileno()
        out_fd = process.stdout.fileno()
        err_fd = process.stderr.fileno()
        for stream in (process.stdin, process.stdout, process.stderr):
            os.set_blocking(stream.fileno(), False)
        selector.register(process.stdout, selectors.EVENT_READ)
        selector.register(process.stderr, selectors.EVENT_READ)
        view = memoryview(stdin)
        offset = 0
        if view:
            selector.register(process.stdin, selectors.EVENT_WRITE)
        else:
            # Empty stdin: close the write end immediately so the child sees
            # EOF; leaving the pipe open would deadlock the parse.
            with contextlib.suppress(OSError):
                process.stdin.close()
        stdin_done = not view
        eof_out = False
        eof_err = False
        stdout_buffer = bytearray()
        while not (stdin_done and eof_out and eof_err):
            if time.monotonic() >= deadline:
                raise PandocStartupError(REASON_TIMEOUT, str(spec.timeout))
            check = request_lifecycle.active_cancellation_check()
            if check is not None and check():
                raise request_lifecycle.RequestCancelled()
            ready = selector.select(timeout=min(0.05, max(0.0, deadline - time.monotonic())))
            for key, _mask in ready:
                fd = key.fd
                if fd == in_fd and not stdin_done:
                    try:
                        written = os.write(in_fd, view[offset:])
                    except (BlockingIOError, InterruptedError):
                        continue
                    except OSError:
                        # Child closed stdin early: stop writing, keep reading.
                        written = len(view) - offset
                    offset += written
                    if offset >= len(view):
                        stdin_done = True
                        with contextlib.suppress(OSError):
                            process.stdin.close()
                        selector.unregister(process.stdin)
                elif fd == out_fd and not eof_out:
                    try:
                        chunk = os.read(out_fd, _CHUNK)
                    except (BlockingIOError, InterruptedError):
                        continue
                    except OSError:
                        chunk = b""
                    if not chunk:
                        eof_out = True
                        selector.unregister(process.stdout)
                        continue
                    stdout_buffer.extend(chunk)
                    if len(stdout_buffer) > PANDOC_MAX_OUTPUT_BYTES:
                        # Enforce the cap immediately; stop reading, kill.
                        raise PandocStartupError(
                            REASON_OUTPUT_TOO_LARGE, str(len(stdout_buffer))
                        )
                elif fd == err_fd and not eof_err:
                    try:
                        chunk = os.read(err_fd, _CHUNK)
                    except (BlockingIOError, InterruptedError):
                        continue
                    except OSError:
                        chunk = b""
                    if not chunk:
                        eof_err = True
                        selector.unregister(process.stderr)
                    # drained and discarded: content-free by construction
        with contextlib.suppress(subprocess.TimeoutExpired, OSError):
            process.wait(timeout=5.0)
        returncode = process.returncode if process.returncode is not None else -9
        return returncode, bytes(stdout_buffer)
    finally:
        # The owned session is always signalled on every exit path,
        # parent alive or already exited: a descendant that outlived
        # the direct child and retained a pipe would otherwise
        # survive this call.  A never-created pre-allocated instance
        # is a no-op; streams are closed by attribute lookup so a
        # partially constructed instance cannot raise.
        if process is not None:
            with contextlib.suppress(OSError):
                _kill_group(process)
        if selector is not None:
            selector.close()
        if process is not None:
            # Attribute lookups tolerate a partially constructed
            # instance; the mirror of the stdlib Popen stream type.
            stdin_stream: BufferedIOBase | None = getattr(process, "stdin", None)
            stdout_stream: BufferedIOBase | None = getattr(process, "stdout", None)
            stderr_stream: BufferedIOBase | None = getattr(process, "stderr", None)
            for candidate in (stdin_stream, stdout_stream, stderr_stream):
                if candidate is not None:
                    with contextlib.suppress(OSError, ValueError):
                        candidate.close()


def check_pandoc(spec: PandocSpec) -> None:
    """Verify executable presence, exact version and required reader capability.

    Must run before the proxy accepts traffic (order 013-a, requirements 2
    and 12).  Raises PandocStartupError with a finite reason on any mismatch.
    """
    if not os.path.isfile(spec.binary) or not os.access(spec.binary, os.X_OK):
        raise PandocStartupError(REASON_NOT_EXECUTABLE, spec.binary)
    startup = PandocSpec(
        spec.binary, spec.version, spec.reader, spec.writer,
        spec.startup_timeout, spec.startup_timeout,
    )
    returncode, stdout = _run_bounded(startup, [spec.binary, "--version"], b"")
    if returncode != 0:
        raise PandocStartupError(REASON_BAD_EXIT, str(returncode))
    first_line = stdout.decode("utf-8", "replace").splitlines()[0] if stdout else ""
    match = _VERSION_RE.match(first_line.strip())
    if match is None or match.group(1) != spec.version:
        raise PandocStartupError(REASON_WRONG_VERSION, spec.version)
    # Reader capability probe: the pinned profile must produce wrapper
    # positions on a minimal document.
    returncode, stdout = _run_bounded(startup, _pandoc_argv(spec), b"Kapabilnost.\n")
    if returncode != 0:
        raise PandocStartupError(REASON_BAD_EXIT, str(returncode))
    if len(stdout) > PANDOC_MAX_OUTPUT_BYTES:
        raise PandocStartupError(REASON_OUTPUT_TOO_LARGE)
    try:
        document = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise PandocStartupError(REASON_MALFORMED_OUTPUT) from None
    try:
        blocks = document["blocks"]
        wrapper = blocks[0]
    except (KeyError, IndexError, TypeError):
        raise PandocStartupError(REASON_CAPABILITY, "unexpected AST shape") from None
    if not isinstance(wrapper, dict) or wrapper.get("t") != "Div":
        raise PandocStartupError(REASON_CAPABILITY, "wrapper Div absent")
    wrapper_positions = [value for key, value in _node_attrs(wrapper) if key == "data-pos"]
    if wrapper_positions != ["1:1-2:1"]:
        raise PandocStartupError(REASON_CAPABILITY, "wrapper sourcepos absent")
    payload = wrapper.get("c")
    if (
        not isinstance(payload, list)
        or len(payload) != 2
        or not _find_positioned_str(payload[1], "1:1-1:12", "Kapabilnost")
    ):
        raise PandocStartupError(REASON_CAPABILITY, "leaf sourcepos absent")


def parse_document(spec: PandocSpec, text: str) -> dict[str, object]:
    """Parse with the pinned profile; fail closed on any structural surprise."""
    encoded = text.encode("utf-8")
    if len(encoded) > PANDOC_MAX_INPUT_BYTES:
        raise PandocStartupError(REASON_INPUT_TOO_LARGE, str(len(encoded)))
    returncode, stdout = _run_bounded(spec, _pandoc_argv(spec), encoded)
    if returncode != 0:
        raise PandocStartupError(REASON_BAD_EXIT, str(returncode))
    if len(stdout) > PANDOC_MAX_OUTPUT_BYTES:
        raise PandocStartupError(REASON_OUTPUT_TOO_LARGE, str(len(stdout)))
    try:
        document = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise PandocStartupError(REASON_MALFORMED_OUTPUT) from None
    if not isinstance(document, dict) or not isinstance(document.get("blocks"), list):
        raise PandocStartupError(REASON_SCHEMA, "missing blocks")
    return document


def _nfc_lines(text: str) -> tuple[list[str], list[bool]]:
    lines = text.split("\n")
    nfc_lines = [unicodedata.normalize("NFC", line) for line in lines]
    stable = [nfc == raw for raw, nfc in zip(lines, nfc_lines, strict=True)]
    if "\n".join(nfc_lines) != unicodedata.normalize("NFC", text):
        raise PandocStartupError(REASON_MAP_INTEGRITY, "NFC line decomposition")
    return nfc_lines, stable


def _line_columns(line: str) -> dict[int, int]:
    """Column -> offset for every code-point start and the virtual line end.

    Columns are 1-based code-point columns.  A tab advances to the next tab
    stop; observed with the pinned binary: a tab starting at column c moves
    the next code point to column ((c - 1) // 4 + 1) * 4 + 1.
    """
    columns: dict[int, int] = {}
    column = 1
    for offset, char in enumerate(line):
        if column in columns:
            raise PandocStartupError(REASON_MAP_INTEGRITY, "column collision")
        columns[column] = offset
        if char == "\t":
            column = ((column - 1) // 4 + 1) * 4 + 1
        else:
            column += 1
    if column in columns:
        raise PandocStartupError(REASON_MAP_INTEGRITY, "column collision")
    columns[column] = len(line)
    return columns


def _position_range(value: str) -> tuple[int, int, int, int] | None:
    match = _POS_RE.match(value)
    if match is None:
        return None
    start_line, start_col, end_line, end_col = (int(part) for part in match.groups())
    if start_line < 1 or start_col < 1 or end_line < 1 or end_col < 1:
        return None
    if end_line < start_line or (end_line == start_line and end_col < start_col):
        return None
    return start_line, start_col, end_line, end_col


@dataclass(frozen=True)
class _QuoteLevel:
    """One open quotation level on the source-ordered replay stack.

    ``origin`` is the event kind that opened the level: a level releases
    only on a proven compatible closer of the SAME provenance, so an
    escaped or entity-normalized marker can never release a different
    (e.g. literal) outer context, and a literal marker can never release
    a normalized level (order 033-a, requirement 3).
    """

    close: str
    origin: str
    start: int


@dataclass(frozen=True)
class _ContextEvent:
    """One structural context event with its provenance.

    ``position`` is the leaf's proven (possibly compound) data-pos value,
    ``span`` the exact mapped original offsets when the whole leaf is
    single-line and proven, ``key`` the physical start (line, column) used
    for source ordering, and ``seq`` the traversal sequence (stable
    tie-break; unplaced events keep traversal order).
    """

    position: str | None
    seq: int
    kind: str
    value: str
    span: tuple[int, int] | None = None

    @property
    def key(self) -> tuple[int, int] | None:
        if self.position is None:
            return None
        parsed = _position_range(self.position.split(";", 1)[0])
        if parsed is None:
            return None
        return (parsed[0], parsed[1])


@dataclass(frozen=True)
class _PendingNote:
    """A footnote definition collected for physical-source-order replay.

    The pinned reader relocates a definition into each of its references
    in AST visitation while retaining the later source coordinates, and a
    reference repeated twice duplicates the whole physical payload (one
    physical delimiter twice).  ``payload_key`` therefore coalesces
    equivalent physical events: each unique definition is replayed exactly
    once (order 033-a, requirement 4 and the root source-order control).
    """

    blocks: list[dict[str, object]]
    start_key: tuple[int, int] | None
    payload_key: str


class _Document:
    def __init__(self, text: str) -> None:
        self.text = text
        self.lines = text.split("\n")
        self.line_count = len(self.lines)
        self.nfc_lines, self.stable = _nfc_lines(text)
        self.line_starts: list[int] = []
        start = 0
        for line in self.lines:
            self.line_starts.append(start)
            start += len(line) + 1
        self.columns = [_line_columns(nfc) for nfc in self.nfc_lines]
        self.granted: list[tuple[int, int]] = []
        self.candidates: list[tuple[int, int]] = []
        self.glue_candidates: list[
            tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
        ] = []
        self.events: list[_ContextEvent] = []
        self.event_seq = 0
        self.pending_notes: list[_PendingNote] = []
        self.processed_notes: set[str] = set()
        self.finalized = False
        self.denied_regions: list[tuple[int, int]] = []
        self.nodes = 0
        self.global_fail: str | None = None

    def fail(self, reason: str, detail: str = "") -> None:
        if self.global_fail is None:
            self.global_fail = reason if not detail else f"{reason} {detail}"

    def count_node(self) -> None:
        self.nodes += 1
        if self.nodes > PANDOC_MAX_BLOCKS + PANDOC_MAX_INLINES:
            self.fail(REASON_NODE_LIMIT, str(self.nodes))

    def map_span(self, value: str) -> tuple[int, int] | None:
        """Map a position to exact original offsets; None when unprovable."""
        if self.global_fail is not None:
            return None
        parsed = _position_range(value)
        if parsed is None:
            return None
        start_line, start_col, end_line, end_col = parsed
        # Virtual EOF: one past the last line, column 1 only (observed
        # container endpoints on documents without a final newline).
        if start_line > self.line_count + 1 or end_line > self.line_count + 1:
            return None
        if end_line == self.line_count + 1 and end_col != 1:
            return None
        if start_line > self.line_count or end_line > self.line_count:
            return None
        if start_line != end_line:
            # Grant candidates never span lines; multi-line positions belong
            # to containers and are never granted.
            return None
        if not self.stable[start_line - 1]:
            # Non-NFC line: conservative abstention for this line.
            return None
        offsets = self.columns[start_line - 1]
        if start_col not in offsets or end_col not in offsets:
            return None
        start_offset = offsets[start_col]
        end_offset = offsets[end_col]
        if start_offset >= end_offset:
            return None
        base = self.line_starts[start_line - 1]
        return base + start_offset, base + end_offset

    def map_block_span(self, value: str) -> tuple[int, int] | None:
        """Map a proven (possibly multi-line) position to original offsets.

        Used only for conservative structural denial extents (complete
        BlockQuote regions): the endpoint lines must be NFC-stable and
        their columns mappable, but the extent may span lines, which
        grant candidates never may.  A virtual EOF endpoint maps past
        the last line.  Any unprovable piece returns None so the caller
        keeps its fail-closed rule.
        """
        if self.global_fail is not None:
            return None
        parsed = _position_range(value)
        if parsed is None:
            return None
        start_line, start_col, end_line, end_col = parsed
        if start_line > self.line_count or end_line > self.line_count + 1:
            return None
        if end_line == self.line_count + 1 and end_col != 1:
            return None
        checked_end = end_line if end_line <= self.line_count else self.line_count
        if not all(self.stable[i] for i in range(start_line - 1, checked_end)):
            return None
        offsets = self.columns[start_line - 1]
        if start_col not in offsets:
            return None
        start_offset = offsets[start_col]
        start_abs = self.line_starts[start_line - 1] + start_offset
        if end_line == self.line_count + 1:
            if start_abs >= len(self.text):
                return None
            return start_abs, len(self.text)
        end_offsets = self.columns[end_line - 1]
        if end_col not in end_offsets:
            return None
        end_offset = end_offsets[end_col]
        end_abs = self.line_starts[end_line - 1] + end_offset
        if end_abs <= start_abs:
            return None
        return (
            start_abs,
            end_abs,
        )

    def _segment_offset(self, segment: str) -> int | None:
        """Offset of one ``L:C`` position segment (geometry, not proof).

        Used only to place context-event bounds when the whole leaf span
        is compound (multi-line) and therefore never grantable; a segment
        that cannot be mapped keeps the extent unproved.
        """
        if self.global_fail is not None:
            return None
        parsed = _position_range(segment)
        if parsed is None:
            return None
        line, col, _end_line, _end_col = parsed
        if line > self.line_count:
            return None
        offsets = self.columns[line - 1]
        if col not in offsets:
            return None
        return self.line_starts[line - 1] + offsets[col]

    def _event_bounds(self, event: _ContextEvent) -> tuple[int, int]:
        """Conservative original bounds of one context event.

        A proven exact span wins; otherwise the first/last segments of a
        (possibly compound) proven position are used.  An unplaceable or
        degenerate event keeps its unproved extent by failing closed
        toward the document ends (order 033-a, requirement 2).
        """
        start_off: int | None = None
        end_off: int | None = None
        if event.span is not None:
            start_off, end_off = event.span
        elif event.position is not None:
            segments = [seg for seg in event.position.split(";") if seg]
            if segments:
                start_off = self._segment_offset(segments[0])
                end_off = self._segment_offset(segments[-1])
        if start_off is None or end_off is None or end_off <= start_off:
            return (0 if start_off is None else start_off, len(self.text))
        return (start_off, end_off)

    def finalize(self) -> None:
        """One document-level source-order finalization (order 033-a).

        After the whole AST has been collected (and before any outcome is
        built): coalesce equivalent physical footnote payloads (each
        unique definition replayed exactly once, so a single physical
        delimiter is never processed twice), sort the structural events
        by proven original position, replay the quotation and HTML
        context stacks, and filter the exact-source candidate grants (and
        their glue) by the resulting denied intervals.  All provenance,
        schema, node, resource and grapheme validations already ran during
        the walk; conflicting or unproved mappings keep the existing
        region/document fail-closed rules.
        """
        if self.finalized or self.global_fail is not None:
            return
        self.finalized = True
        # 1) Unique physical footnote definitions, exactly once each, in
        #    ascending physical position order.  A definition referenced
        #    several times duplicates one physical payload in the AST
        #    (the same payload_key can appear twice within one batch), so
        #    each unique payload is coalesced and replayed exactly once:
        #    one physical delimiter is never processed twice.  Nested
        #    definitions collected during a replay enter the next drain
        #    round.
        while self.pending_notes:
            batch, self.pending_notes = self.pending_notes, []
            fresh = [
                note
                for note in batch
                if note.payload_key not in self.processed_notes
            ]
            if not fresh:
                continue
            unique: dict[str, _PendingNote] = {}
            for note in fresh:
                if note.payload_key not in unique:
                    unique[note.payload_key] = note
            for note in sorted(
                unique.values(),
                key=lambda item: (
                    item.start_key is None,
                    item.start_key or (0, 0),
                ),
            ):
                self.processed_notes.add(note.payload_key)
                _walk_blocks(self, note.blocks)
                if self.global_fail is not None:
                    return
        # 2) Source-ordered replay of the collected structural events.
        events = sorted(
            self.events,
            key=lambda event: (
                event.key is None,
                event.key or (0, 0),
                event.seq,
            ),
        )
        quote_stack: list[_QuoteLevel] = []
        html_stack: list[tuple[str, int]] = []
        denied: list[tuple[int, int]] = []
        for event in events:
            start_off, end_off = self._event_bounds(event)
            if event.kind == "html-open":
                html_stack.append((event.value, start_off))
            elif event.kind == "html-close":
                if html_stack and html_stack[-1][0] == event.value:
                    _name, opener_start = html_stack.pop()
                    denied.append((opener_start, end_off))
                # A closer with another identity, or an orphan closer,
                # cannot discharge an unmatched opener: no raw-string
                # release of a different context.
            elif event.kind in ("quote-literal", "quote-entity", "quote-escaped"):
                top = quote_stack[-1] if quote_stack else None
                if (
                    top is not None
                    and top.origin == event.kind
                    and event.value == top.close
                ):
                    closed = quote_stack.pop()
                    denied.append((closed.start, end_off))
                else:
                    family = _QUOTE_FAMILIES.get(event.value)
                    if family is not None:
                        quote_stack.append(
                            _QuoteLevel(family[1], event.kind, start_off)
                        )
                    # A directional closer with no compatible opener on
                    # top (or an entity releasing a different, e.g.
                    # literal, outer context) is a no-op and never
                    # granted.
        for _name, opener_start in html_stack:
            denied.append((opener_start, len(self.text)))
        for level in quote_stack:
            denied.append((level.start, len(self.text)))
        # Conservative trusted structural extents: complete BlockQuote
        # regions recorded with their proven wrapper positions, so a
        # source-relocated footnote payload can never be granted inside
        # the quoted original region (order 033-a, requirements 4-5).
        denied.extend(self.denied_regions)
        merged: list[tuple[int, int]] = []
        for start, end in sorted(denied):
            if end <= start:
                continue
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        # The merged intervals are disjoint with strictly increasing
        # start AND end (each appended start exceeds the previous end),
        # so the query overlaps one of them iff the last interval whose
        # start is below the query end - the maximum end in that prefix
        # - ends after the query start.  Standard-library binary search
        # over the sorted start endpoints keeps this O(log n) per grant
        # candidate with the exact half-open overlap rule
        # (``denied_start < end and denied_end > start``).
        merged_starts = [item[0] for item in merged]
        merged_ends = [item[1] for item in merged]

        def denied_overlaps(start: int, end: int) -> bool:
            index = bisect.bisect_left(merged_starts, end) - 1
            return index >= 0 and merged_ends[index] > start

        # 3) Filter the exact-source candidate grants by the final denied
        #    context; glue survives only between two surviving spans.
        kept: set[tuple[int, int]] = set()
        for start, end in self.candidates:
            if not denied_overlaps(start, end):
                kept.add((start, end))
        for glue_span, prev_span, next_span in self.glue_candidates:
            if (
                prev_span in kept
                and next_span in kept
                and not denied_overlaps(glue_span[0], glue_span[1])
            ):
                kept.add(glue_span)
        self.granted = sorted(kept)


def _node_attrs(node: dict[str, object]) -> list[tuple[str, str]]:
    try:
        raw = cast("list[list[object]]", node["c"])[0][2]
    except (IndexError, TypeError, KeyError):
        return []
    if not isinstance(raw, list):
        return []
    return [(str(key), str(value)) for key, value in raw]


def _trusted_position(document: _Document, attrs: list[tuple[str, str]]) -> str | None:
    """Return the proven position value for a positioned node, or None.

    Provenance rules established on the pinned binary: exactly one ``data-pos``
    value is generated; an identical user duplicate is a no-op; two distinct
    values (a user attribute colliding with the generated position) defeat
    provenance for that node.  A wrapper marker without a position is
    untrusted (a user can set ``wrapper`` but not positions).
    """
    values = [value for key, value in attrs if key == "data-pos"]
    if not values:
        return None
    if len(set(values)) > 1:
        return None
    return values[0]


@dataclass
class _Leaf:
    kind: str
    position: str | None
    content: str | None
    span: tuple[int, int] | None = None
    granted: bool = False
    raw_content: str | None = None


_RAW_OPEN_NAME = re.compile(r"^<([A-Za-z][A-Za-z0-9-]*)")
_RAW_CLOSE_SHAPE = re.compile(r"^</([A-Za-z][A-Za-z0-9-]*)\s*>$")
_RAW_VOID_TAGS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }
)


def _raw_tag_info(raw_content: str | None) -> tuple[str, str | None]:
    """(action, name) of a reader-recognized raw tag fragment.

    ``action`` is "open", "close" or "neutral".  No HTML parsing: only
    complete tag shapes act.  An opening tag is a complete ``<name ...>``
    ending in ``>`` - the interior may span lines, as the pinned reader
    keeps a multi-line (LF or CRLF attribute) opening tag in ONE RawInline
    with a compound source position, and that opening context must not be
    discarded just because the range is compound - while self-closing and
    void forms are neutral.  A closing tag is exactly the complete
    ``</name>`` shape: a split or incomplete closer (bare ``</``, a name
    across leaves) is never recognized by the reader as a tag and so can
    never release an unmatched opener by raw-string matching (order 033-a,
    requirement 6).  Declarations, comments and unknown shapes are
    neutral.
    """
    if not raw_content:
        return ("neutral", None)
    value = raw_content.strip()
    if not value.startswith("<"):
        return ("neutral", None)
    if value.startswith(("<!", "<?", "<!--")):
        return ("neutral", None)
    if value.startswith("</"):
        match = _RAW_CLOSE_SHAPE.match(value)
        if match is None:
            return ("neutral", None)
        return ("close", match.group(1).lower())
    match = _RAW_OPEN_NAME.match(value)
    if match is None:
        return ("neutral", None)
    name = match.group(1).lower()
    if name in _RAW_VOID_TAGS:
        return ("neutral", None)
    if not value.endswith(">") or value.endswith("/>"):
        return ("neutral", None)
    return ("open", name)


def _classify_inline(document: _Document, node: dict[str, object]) -> _Leaf:
    tag = node["t"]
    content = node.get("c")
    document.count_node()
    if tag in ("Str", "Space", "SoftBreak", "LineBreak", "HorizontalRule"):
        # Leaf wrappers are positioned by their enclosing Span in the pinned
        # JSON shape; a bare leaf carries no position and is never granted.
        return _Leaf(tag.lower(), None, cast("str", content) if tag == "Str" else None)
    if tag in ("Span", "Div"):
        position = _trusted_position(document, _node_attrs(node))
        inner = content[1] if isinstance(content, list) and len(content) > 1 else []
        if (
            tag == "Span"
            and isinstance(inner, list)
            and len(inner) == 1
            and isinstance(inner[0], dict)
        ):
            child = inner[0]
            child_tag = child.get("t")
            if child_tag == "Str":
                return _Leaf("str", position, child.get("c"))
            if child_tag == "RawInline":
                # The wrapper Span of a RawInline still marks the machine
                # fragment for adjacency denial.
                _trusted_position(document, _node_attrs(child))
                raw_text = None
                child_content = child.get("c")
                if (
                    isinstance(child_content, list)
                    and len(child_content) > 1
                    and isinstance(child_content[1], str)
                ):
                    raw_text = child_content[1]
                return _Leaf("raw", position, None, raw_content=raw_text)
            if child_tag == "Note":
                # The pinned reader relocates a footnote definition into
                # the wrapper Span of each reference while the payload
                # retains its physical source coordinates.  It is
                # collected and replayed exactly once, at its proven
                # physical position, by the document-level finalization
                # (order 033-a, requirement 4).
                note_blocks = child.get("c")
                if (
                    isinstance(note_blocks, list)
                    and note_blocks
                    and isinstance(note_blocks[0], dict)
                ):
                    _trusted_position(document, _node_attrs(child))
                    _collect_pending_note(document, note_blocks)
                return _Leaf("note", position, None)
            if child_tag in ("Emph", "Strong", "Strikeout", "Superscript", "Subscript"):
                # Emphasis is wrapper-Span positioned; its inlines are the
                # node payload itself.
                # The recursive walk collects the inner candidate grants
                # and structural events with their own proven positions;
                # the document-level finalization orders and filters them
                # with the enclosing context (order 033-a).
                child_inlines = child.get("c")
                leaf = _Leaf(child_tag.lower(), position, None)
                if isinstance(child_inlines, list):
                    _walk_inlines(document, child_inlines)
                return leaf
            if child_tag in ("Space", "LineBreak", "SoftBreak"):
                kind = {
                    "Space": "space",
                    "LineBreak": "linebreak",
                    "SoftBreak": "softbreak",
                }[child_tag]
                return _Leaf(kind, position, None)
        return _Leaf(tag.lower(), position, None)
    if tag == "RawInline":
        _trusted_position(document, _node_attrs(node))
        raw_text = None
        if isinstance(content, list) and len(content) > 1 and isinstance(content[1], str):
            raw_text = content[1]
        return _Leaf("raw", None, None, raw_content=raw_text)
    if tag == "Code":
        _trusted_position(document, _node_attrs(node))
        return _Leaf("code", None, None)
    if tag == "Math":
        return _Leaf("math", None, None)
    if tag in ("Link", "Image"):
        _trusted_position(document, _node_attrs(node))
        # Whole fragment (label, destination, attributes) stays protected.
        return _Leaf("link", None, None)
    if tag == "Note":
        _trusted_position(document, _node_attrs(node))
        if isinstance(content, list) and content and isinstance(content[0], dict):
            # A footnote definition is relocated into its reference in AST
            # visitation while retaining the later source coordinates, so
            # walking it here would process its quote-like or tag-like
            # glyphs at the wrong (reference) position, and a repeated
            # reference would duplicate one physical delimiter.  The
            # payload is collected and replayed exactly once, at its
            # proven physical position, by the finalization
            # (order 033-a, requirement 4).
            _collect_pending_note(document, content)
        return _Leaf("note", None, None)
    if tag in ("Emph", "Strong", "Strikeout", "Superscript", "Subscript"):
        # JSON shape: the node payload is the inline list itself.
        if isinstance(content, list):
            _walk_inlines(document, content)
        return _Leaf(tag.lower(), None, None)
    if tag in ("SmallCaps", "Underline", "Cite", "Quote", "Poem", "Span2"):
        return _Leaf(tag.lower(), None, None)
    return _Leaf("unknown", None, None)


def _walk_inlines(document: _Document, inlines: list[dict[str, object]]) -> None:
    if document.global_fail is not None:
        return
    leaves: list[_Leaf] = []
    for node in inlines:
        if not isinstance(node, dict) or "t" not in node:
            document.fail(REASON_SCHEMA, "inline node")
            continue
        leaf = _classify_inline(document, node)
        leaves.append(leaf)
    if document.global_fail is not None:
        return
    # Structural event collection without an HTML parser (order 033-a):
    # reader-recognized complete raw opening/closing tags and quotation
    # markers are recorded with their proven positions.  The document
    # level finalization sorts every event by physical source order and
    # replays the context stacks once for the whole document, so
    # unproved extents - unclosed openers, mismatched closers, escaped
    # and entity markers, tags inside nested emphasis, blocks and
    # source-relocated footnote payloads - are computed before any
    # candidate grant is filtered.
    for leaf in leaves:
        if leaf.kind == "raw":
            action, name = _raw_tag_info(leaf.raw_content)
            if action in ("open", "close") and name is not None:
                span = document.map_span(leaf.position) if leaf.position else None
                _record_event(
                    document, leaf.position, "html-" + action, name, span
                )
            continue
        if leaf.kind != "str" or leaf.content is None:
            continue
        content = leaf.content
        if len(content) == 1 and content in _QUOTE_CHARS:
            # A lone quote character is a quotation marker, never granted
            # prose.  A marker only transitions the quote context when its
            # proven original slice is the exact code point (literal), a
            # backslash escape (``\\"``) or a character reference
            # (entity).  Each provenance opens a level that only a
            # compatible closer of the SAME provenance releases, so an
            # escaped or entity inner marker can never release a
            # different (e.g. literal) outer context; none of the forms
            # is ever granted (order 033-a, requirement 3).  A straight
            # delimiter flanked by word characters on both sides is an
            # in-word apostrophe: ordinary punctuation, inert and
            # following the normal grant path for the literal form.
            span = document.map_span(leaf.position) if leaf.position else None
            if span is not None:
                original = document.text[span[0]:span[1]]
                in_word = (
                    content in _FLANK_CHECK_CHARS
                    and (
                        document.text[span[0] - 1] if span[0] > 0 else ""
                    ).isalnum()
                    and (
                        document.text[span[1]]
                        if span[1] < len(document.text)
                        else ""
                    ).isalnum()
                )
                if original != content:
                    if in_word:
                        # Escaped or entity in-word straight apostrophe:
                        # inert machine syntax, never granted, never a
                        # delimiter.
                        continue
                    if (
                        len(original) == 2
                        and original[0] == "\\"
                        and original[1] == content
                    ):
                        _record_event(
                            document, leaf.position, "quote-escaped", content, span
                        )
                    elif len(original) > 1 and original.startswith("&"):
                        _record_event(
                            document, leaf.position, "quote-entity", content, span
                        )
                    continue
                if not in_word:
                    _record_event(
                        document, leaf.position, "quote-literal", content, span
                    )
                    continue
                # In-word literal apostrophe (ordinary punctuation): the
                # normal candidate path below.
            else:
                # Unproved marker position: never granted; the extent is
                # unproved, so the event keeps traversal order
                # (fail-closed placement).
                _record_event(document, leaf.position, "quote-literal", content, None)
                continue
        if leaf.position is None:
            continue
        span = document.map_span(leaf.position)
        if span is None:
            continue
        start, end = span
        original = document.text[start:end]
        if original != leaf.content:
            continue
        if any(grapheme_sensitive(char) for char in original):
            continue
        # Unproved boundary: a grapheme-sensitive neighbor would be split
        # by an edit replacing exactly this slice.
        before = document.text[start - 1] if start > 0 else ""
        after = document.text[end] if end < len(document.text) else ""
        if (
            (before and grapheme_boundary_sensitive(before))
            or (after and grapheme_boundary_sensitive(after))
        ):
            continue
        leaf.span = (start, end)
        leaf.granted = True
        document.candidates.append((start, end))
    # Whitespace glue: a candidate only inside a proven shared prose
    # context -
    # between two granted, contiguous prose spans, never across a protected
    # node or structural barrier.
    for index, leaf in enumerate(leaves):
        if leaf.kind not in ("space", "linebreak") or leaf.position is None:
            continue
        span = document.map_span(leaf.position)
        if span is None:
            continue
        start, end = span
        glue_slice = document.text[start:end]
        if not glue_slice or not set(glue_slice) <= _WHITESPACE_SLICE:
            continue
        previous = leaves[index - 1] if index > 0 else None
        following = leaves[index + 1] if index + 1 < len(leaves) else None
        if (
            previous is None
            or following is None
            or not previous.granted
            or not following.granted
            or previous.span is None
            or following.span is None
            or previous.span[1] != start
            or following.span[0] != end
        ):
            continue
        leaf.granted = True
        # The finalization keeps the glue only when both neighbor spans
        # survive the denied-context filter.
        document.glue_candidates.append(((start, end), previous.span, following.span))


def _record_event(
    document: _Document,
    position: str | None,
    kind: str,
    value: str,
    span: tuple[int, int] | None,
) -> None:
    """Append one structural context event in traversal order."""
    document.events.append(
        _ContextEvent(
            position=position, seq=document.event_seq, kind=kind, value=value, span=span
        )
    )
    document.event_seq += 1


def _first_source_position(node: object) -> str | None:
    """First machine ``data-pos`` value in document order, or None."""
    found: list[str] = []

    def visit(item: object) -> None:
        if found:
            return
        if isinstance(item, dict):
            content = item.get("c")
            if isinstance(content, list) and len(content) >= 3:
                attrs = content[2]
                if isinstance(content[0], str) and isinstance(attrs, list):
                    for pair in attrs:
                        if (
                            isinstance(pair, list)
                            and len(pair) == 2
                            and pair[0] == "data-pos"
                            and isinstance(pair[1], str)
                            and pair[1]
                        ):
                            found.append(pair[1])
                            return
            visit(content)
        elif isinstance(item, list):
            for child in item:
                visit(child)

    visit(node)
    return found[0] if found else None


def _collect_pending_note(
    document: _Document, blocks: list[dict[str, object]]
) -> None:
    """Record a footnote definition for physical-source-order replay.

    The pinned reader relocates a definition into each of its references
    in AST visitation while retaining the later source coordinates, and a
    reference repeated twice duplicates the whole physical payload (one
    physical delimiter twice).  The definition is therefore collected
    here and replayed exactly once, at its proven physical position, by
    the document-level finalization (order 033-a, requirement 4).
    """
    start_key: tuple[int, int] | None = None
    position = _first_source_position(blocks)
    if position is not None:
        parsed = _position_range(position.split(";", 1)[0])
        if parsed is not None:
            start_key = (parsed[0], parsed[1])
    document.pending_notes.append(
        _PendingNote(
            blocks=blocks,
            start_key=start_key,
            payload_key=json.dumps(blocks, sort_keys=True, ensure_ascii=False),
        )
    )


def _walk_blocks(
    document: _Document,
    blocks: list[dict[str, object]],
    enclosing: str | None = None,
) -> None:
    if document.global_fail is not None:
        return
    for node in blocks:
        if not isinstance(node, dict) or "t" not in node:
            document.fail(REASON_SCHEMA, "block node")
            continue
        tag = node["t"]
        content = node.get("c")
        document.count_node()
        if tag == "Div" and isinstance(content, list) and len(content) > 1:
            position = _trusted_position(document, _node_attrs(node))
            _walk_blocks(document, content[1], enclosing=position)
            continue
        if tag in ("Para", "Plain") and isinstance(content, list):
            _walk_inlines(document, content)
            continue
        if tag == "BlockQuote" and isinstance(content, list):
            # A complete Pandoc BlockQuote structure - lazy continuation
            # and nesting included (the pinned reader folds a following
            # unmarked line into the same BlockQuote node) - is denied in
            # full: its content is never walked, so no prose inside a
            # quotation is granted and no quote-like or tag-like glyph in
            # it can transition any surrounding prose context.  The quote
            # proven physical extent (the block's own data-pos, else the
            # positioned wrapper Div that retains the full quote extent
            # even when footnote relocation empties the BlockQuote) is
            # additionally recorded as a denial region so a
            # source-relocated footnote payload can never be granted
            # inside the quoted original region; an unprovable extent
            # fails the document closed.  Independent prose after the
            # proved block boundary is a separate block and is unaffected
            # (order 033-a, requirements 4-5).
            position = _trusted_position(document, _node_attrs(node)) or enclosing
            if position is None:
                document.fail(REASON_MAP_INTEGRITY, "blockquote extent")
                continue
            extent = document.map_block_span(position)
            if extent is None:
                document.fail(REASON_MAP_INTEGRITY, "blockquote extent")
                continue
            document.denied_regions.append(extent)
            continue
        if tag in ("OrderedList", "BulletList") and isinstance(content, list):
            # BulletList payload is the item list; OrderedList payload is
            # (attributes, item list).  Each item is itself a list of
            # blocks, normally a single positioned wrapper Div.
            items = content[1] if tag == "OrderedList" and len(content) > 1 else content
            if not isinstance(items, list):
                document.fail(REASON_SCHEMA, "list payload")
                continue
            for item in items:
                if not (
                    isinstance(item, list)
                    and item
                    and all(isinstance(block, dict) and "t" in block for block in item)
                ):
                    document.fail(REASON_SCHEMA, "list item")
                    continue
                _walk_blocks(document, item)
            continue
        if tag == "Header" and isinstance(content, list) and len(content) > 2:
            _trusted_position(document, _node_attrs(node))
            _walk_inlines(document, content[2])
            continue
        if tag == "Note" and isinstance(content, list) and isinstance(content[0], str):
            # Block-level footnote: identifier, attributes, blocks.
            _trusted_position(document, _node_attrs(node))
            if len(content) > 2 and isinstance(content[2], list):
                _walk_blocks(document, content[2])
            continue
        if tag in ("CodeBlock", "Table", "DefinitionList", "HorizontalRule",
                   "RawBlock", "LineBlock", "Figure", "NativeDiv", "NativeSpan"):
            # Structurally machine: never granted; positions sanity-checked
            # where the element carries them directly.
            if tag in _DIRECT_POSITIONED:
                _trusted_position(document, _node_attrs(node))
            continue
        # Unknown block structure: deny by default (complement protects it).
        continue


def protect_with_pandoc(spec: PandocSpec, text: str) -> ProtectionOutcome:
    """Run the mandatory structural protection; fail closed on any surprise."""
    # The declared input bound is enforced before per-codepoint map
    # allocation, normalization, and the Pandoc subprocess (requirement 8
    # bounded resources): an oversized completed answer must fail closed
    # without building the mapper.
    encoded = text.encode("utf-8")
    if len(encoded) > PANDOC_MAX_INPUT_BYTES:
        return ProtectionOutcome(
            False, REASON_INPUT_TOO_LARGE, detail=str(len(encoded))
        )
    document = _Document(text)
    try:
        parsed = parse_document(spec, text)
    except PandocStartupError as exc:
        return ProtectionOutcome(False, exc.reason, detail=exc.detail[:256])
    try:
        _walk_blocks(document, cast("list[dict[str, object]]", parsed["blocks"]))
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        return ProtectionOutcome(False, REASON_SCHEMA, detail=type(exc).__name__[:32])
    if document.global_fail is not None:
        return ProtectionOutcome(False, REASON_SCHEMA, detail=document.global_fail[:256])
    document.finalize()
    if document.global_fail is not None:
        return ProtectionOutcome(False, REASON_SCHEMA, detail=document.global_fail[:256])
    granted = tuple(sorted(document.granted))
    return ProtectionOutcome(True, None, granted=granted)


def compose_protection(
    text: str,
    outcome: ProtectionOutcome,
    tool_arguments: tuple[str, ...] = (),
) -> list[Interval]:
    """Protected intervals = complement of granted prose + residual machine.

    Returns the merged protected interval list in the historical
    ``Interval`` shape consumed by the detector, acceptance and patcher.
    Residual matches overlapping any granted span are retained in full: a
    machine fragment that begins in protected syntax and extends into
    granted prose must not be truncated.
    """
    from protected import Interval
    from protection_residuals import residual_intervals

    length = len(text)
    protected: list[Interval] = []
    cursor = 0
    for start, end in outcome.granted:
        if start > cursor:
            protected.append(Interval(cursor, start, "pandoc-structure"))
        cursor = end
    if cursor < length:
        protected.append(Interval(cursor, length, "pandoc-structure"))
    for interval in residual_intervals(text, tool_arguments):
        if any(interval.start < end and interval.end > start for start, end in outcome.granted):
            protected.append(interval)
    merged: list[Interval] = []
    for interval in sorted(protected):
        if merged and interval.start <= merged[-1].end:
            merged[-1] = Interval(
                merged[-1].start,
                max(merged[-1].end, interval.end),
                merged[-1].reason + "+" + interval.reason,
            )
        else:
            merged.append(interval)
    return merged

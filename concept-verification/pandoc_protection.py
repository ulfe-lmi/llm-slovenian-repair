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

Deny by default: only ``Str`` leaf spans whose position is proven against the
unmodified original (valid coordinates, exact original-slice equality,
grapheme-safe, NFC-stable line) are granted as editable prose, plus
whitespace glue only inside a proven shared prose context (between two
granted, contiguous prose spans).  Everything else - code, math, HTML,
links and images (including labels), configuration, metadata, markers,
soft breaks, escapes, entities and every unprovable region - is protected.
Residual machine-content recognizers (``protection_residuals``) then refine
the granted prose; any residual match overlapping granted prose is retained.

No substring matching is used for position recovery and no AST-to-Markdown
rendering is used for answers; edits apply to validated original coordinates
with unchanged unapproved slices.
"""

from __future__ import annotations

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
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

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


# Lone-character quote markers: straight quotes as literal text plus the
# typographic forms ``smart`` may produce.  Curly forms carry direction;
# straight forms are context toggles.  A marker toggles quote context;
# prose inside a literal quotation is unproved (order 013-a, requirement 16).
_QUOTE_OPENERS = frozenset("\u201c\u2018")
_QUOTE_CLOSERS = frozenset("\u201d\u2019")
_QUOTE_TOGGLES = frozenset('"\'')
_QUOTE_MARKERS = _QUOTE_OPENERS | _QUOTE_CLOSERS | _QUOTE_TOGGLES
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
    """
    process: subprocess.Popen[bytes] | None = None
    selector = None
    try:
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
        self.granted_revoked: set[tuple[int, int]] = set()
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
    raw_neighbor: bool = False
    raw_content: str | None = None
    # Spans granted by a recursive emphasis walk inside this leaf; the
    # enclosing context scan revokes them when its position is denied.
    contained_spans: list[tuple[int, int]] = field(default_factory=list)


_RAW_TAG_NAME = re.compile(r"^</?([A-Za-z][A-Za-z0-9-]*)")
_RAW_VOID_TAGS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }
)


def _raw_tag_kind(raw_content: str | None) -> str | None:
    """Coarse tag shape of a RawInline content string: open/close/neutral.

    No HTML parsing: only the leading marker, the first tag name, the
    self-closing suffix and the HTML void-tag set are examined.
    Declarations, comments and unknown shapes are neutral; a tag with
    several forms (e.g. ``<b></b>``) is classified by its first tag and so
    fails closed toward "open" only when that first tag opens.
    """
    if not raw_content:
        return None
    value = raw_content.strip()
    if not value.startswith("<"):
        return None
    if value.startswith("</"):
        return "close"
    if value.startswith(("<!", "<?", "<!--")):
        return "neutral"
    match = _RAW_TAG_NAME.match(value)
    if match is None:
        return "neutral"
    if match.group(1).lower() in _RAW_VOID_TAGS:
        return "neutral"
    if value.endswith("/>"):
        return "neutral"
    return "open"


def _classify_inline(
    document: _Document, node: dict[str, object], prev_raw: bool
) -> _Leaf:
    tag = node["t"]
    content = node.get("c")
    document.count_node()
    if tag in ("Str", "Space", "SoftBreak", "LineBreak", "HorizontalRule"):
        # Leaf wrappers are positioned by their enclosing Span in the pinned
        # JSON shape; a bare leaf carries no position and is never granted.
        return _Leaf(
            tag.lower(),
            None,
            cast("str", content) if tag == "Str" else None,
            raw_neighbor=prev_raw,
        )
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
                return _Leaf("str", position, child.get("c"), raw_neighbor=prev_raw)
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
                return _Leaf("raw", position, None, raw_neighbor=True, raw_content=raw_text)
            if child_tag in ("Emph", "Strong", "Strikeout", "Superscript", "Subscript"):
                # Emphasis is wrapper-Span positioned; its inlines are the
                # node payload itself.
                # Grants made during this recursive walk are recorded on
                # the leaf so the enclosing inline list's context scan
                # (HTML depth / quote context) can revoke them when the
                # enclosing position is denied.
                child_inlines = child.get("c")
                leaf = _Leaf(child_tag.lower(), position, None)
                if isinstance(child_inlines, list):
                    before = len(document.granted)
                    _walk_inlines(document, child_inlines)
                    leaf.contained_spans = list(document.granted[before:])
                return leaf
            if child_tag in ("Space", "LineBreak", "SoftBreak"):
                kind = {
                    "Space": "space",
                    "LineBreak": "linebreak",
                    "SoftBreak": "softbreak",
                }[child_tag]
                return _Leaf(kind, position, None, raw_neighbor=prev_raw)
        return _Leaf(tag.lower(), position, None, raw_neighbor=prev_raw)
    if tag == "RawInline":
        _trusted_position(document, _node_attrs(node))
        raw_text = None
        if isinstance(content, list) and len(content) > 1 and isinstance(content[1], str):
            raw_text = content[1]
        return _Leaf("raw", None, None, raw_neighbor=True, raw_content=raw_text)
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
            _walk_blocks(document, content)
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
    prev_raw = False
    for node in inlines:
        if not isinstance(node, dict) or "t" not in node:
            document.fail(REASON_SCHEMA, "inline node")
            continue
        leaf = _classify_inline(document, node, prev_raw)
        prev_raw = leaf.raw_neighbor if leaf.kind in ("raw",) else False
        # A leaf directly adjacent to raw HTML is part of the machine
        # fragment: structural leaf presence never authorizes the edit.
        leaves.append(leaf)
    if document.global_fail is not None:
        return
    # Machine-fragment denial without an HTML parser: an opening raw tag
    # raises the open-tag depth and a closing tag lowers it (floored at
    # zero).  Prose at positive depth is fragment interior; prose at zero
    # depth is prose context and may be granted.  Void tags, comments and
    # declarations do not change the depth.  Unclosed openers keep the
    # remainder of the inline list denied (unprovable extent).
    depth = 0
    quote_depth = 0
    for leaf in leaves:
        quote_marker = (
            leaf.kind == "str"
            and leaf.content is not None
            and len(leaf.content) == 1
            and leaf.content in _QUOTE_MARKERS
        )
        if quote_marker:
            # A lone quote character is a quotation marker, never granted
            # prose; it toggles quote context depth.  Markers are processed
            # before the depth guards so a closer can reset the context
            # even while the context is open.
            if leaf.content in _QUOTE_TOGGLES:
                # A straight quote flanked by word characters on both sides
                # is an in-word apostrophe (ordinary punctuation), not a
                # quotation delimiter: it follows the normal grant path.
                marker_span = document.map_span(leaf.position) if leaf.position else None
                flank_before = (
                    document.text[marker_span[0] - 1] if marker_span and marker_span[0] > 0 else ""
                )
                flank_after = (
                    document.text[marker_span[1]]
                    if marker_span and marker_span[1] < len(document.text)
                    else ""
                )
                if not (flank_before.isalnum() and flank_after.isalnum()):
                    # Paired straight delimiters arrive as identical
                    # characters: the first at depth zero opens and the
                    # next closes; an unpaired opener keeps the remainder
                    # of the inline list denied.
                    quote_depth = 0 if quote_depth > 0 else 1
                    continue
            else:
                if leaf.content in _QUOTE_OPENERS:
                    quote_depth += 1
                else:
                    quote_depth = max(0, quote_depth - 1)
                continue
        if leaf.kind == "str" and (depth > 0 or quote_depth > 0):
            continue
        if leaf.kind == "raw":
            kind = _raw_tag_kind(leaf.raw_content)
            if kind == "open":
                depth += 1
            elif kind == "close":
                depth = max(0, depth - 1)
        if leaf.kind in _EMPH_KINDS and leaf.contained_spans and (depth > 0 or quote_depth > 0):
            # Nested emphasis prose was granted during construction,
            # before this enclosing context was known: revoke all spans
            # contained in the denied position (conservative).
            document.granted_revoked.update(leaf.contained_spans)
        if leaf.kind != "str" or leaf.position is None or leaf.content is None:
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
        document.granted.append((start, end))
    # Whitespace glue: granted only inside a proven shared prose context -
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
        document.granted.append((start, end))


def _walk_blocks(document: _Document, blocks: list[dict[str, object]]) -> None:
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
            _trusted_position(document, _node_attrs(node))
            _walk_blocks(document, content[1])
            continue
        if tag in ("Para", "Plain") and isinstance(content, list):
            _walk_inlines(document, content)
            continue
        if tag == "BlockQuote" and isinstance(content, list):
            _walk_blocks(document, content)
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
    granted = tuple(sorted(set(document.granted) - document.granted_revoked))
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

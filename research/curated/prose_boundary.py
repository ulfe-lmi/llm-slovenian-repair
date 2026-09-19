"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Parser-first structural protection layer (008-c, structural policy v2).

Pipeline (frozen 008-c interface decision, research-pipeline only):

  raw immutable UTF-8 document
    -> pinned pulldown-cmark 0.13.4 subprocess helper (JSONL event protocol,
       one invocation per document, byte offsets)
    -> parser-derived candidate Text regions (policy v2 candidate rule,
       incl. the D1 token-family and the D0 autolink-destination rules)
    -> final protected set = every non-candidate byte (structural) plus the
       narrow residual semantic recognizers (policy v2 classes) applied only
       inside candidate-prose spans, in code-point coordinates
    -> public intervals for the frozen 007-m linguistic pipeline

Fail-closed contract (policy v2): helper unavailable / identity mismatch /
non-zero exit / timeout / malformed or truncated protocol / out-of-order or
unbalanced events / any coordinate-contract violation -> the legacy full-
regex protection (the 008-a research/curated/protected.py rule set, retained
in this module and clearly marked) is used instead, with the fallback reason
recorded in the result. The result is never fail-open: an unprotected result
is never returned.

Label transition (recorded in REPORT-008C.md): the 008-a adapter README's
"MEASUREMENT ADAPTER" label described round 008-a; in 008-c the identical
pinned source and protocol are adopted as the research pipeline's structural
helper. The 008-a README is immutable history.

Privacy: no private absolute paths are embedded in this module; the helper
is resolved from an explicit argument, the OAP_008C_PROSE_BOUNDARY_HELPER
environment variable, the OAP_RESEARCH_RUNTIME_PARENT environment variable,
or the machine-local research runtime parent under the user data directory
(convention: research-runtime-*/008-a-prose-boundary-qualification.*/
scratch/target/release/prose-boundary-meas). Every candidate is verified
against the pinned sha256 before use.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# pinned helper identity (frozen 008-a candidate identity; the 008-a baseline
# files are byte-identical and cited here by the frozen record)
# ---------------------------------------------------------------------------
HELPER_BINARY_NAME = "prose-boundary-meas"
HELPER_PINNED_SHA256 = "5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf"
HELPER_CRATE_CHECKSUM = "e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e"
HELPER_CRATE = "pulldown-cmark =0.13.4"
HELPER_PROFILE = "P2"
HELPER_TIMEOUT_SECONDS = 60.0
HELPER_ENV_VAR = "OAP_008C_PROSE_BOUNDARY_HELPER"
RUNTIME_PARENT_ENV_VAR = "OAP_RESEARCH_RUNTIME_PARENT"
HELPER_SUBDIR_GLOB = "008-a-prose-boundary-qualification.*/scratch/target/release/prose-boundary-meas"
REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_V2_PATH = REPO_ROOT / "research" / "prose-boundary" / "config" / "structural-policy-v2.json"
POLICY_V3_PATH = REPO_ROOT / "research" / "prose-boundary" / "config" / "structural-policy-v3.json"


class ProtectionFallback(Exception):
    """Raised internally when the parser-first path cannot be trusted.

    The reason string is a stable token (see policy v2 fail_closed_fallback
    triggers) and is recorded verbatim in the ProtectionResult.
    """


@dataclass(frozen=True)
class ProtectionResult:
    """Outcome of one protection computation (code-point coordinates).

    intervals: merged (start, end, reason) tuples, half-open, sorted.
    mode: "parser-first" (policy v2 path) or "legacy-fallback" (the 008-a
          full-regex rule set, byte-identical behaviour).
    fallback_reason: None in parser-first mode; the stable trigger token
          otherwise.
    event_count / candidate_count: parser diagnostics (0 in fallback mode).
    """

    intervals: tuple[tuple[int, int, str], ...]
    mode: str
    fallback_reason: str | None
    event_count: int = 0
    candidate_count: int = 0


# ---------------------------------------------------------------------------
# coordinate contract (policy v2; identical semantics to 008-a coordinate.py)
# ---------------------------------------------------------------------------
def on_code_point_boundary(data: bytes, pos: int) -> bool:
    """True iff ``pos`` is a UTF-8 code point boundary in ``data``."""
    if pos < 0 or pos > len(data):
        return False
    if pos == 0 or pos == len(data):
        return True
    # a boundary is a position not falling mid-sequence: the byte at pos must
    # not be a UTF-8 continuation byte (10xxxxxx)
    return (data[pos] & 0xC0) != 0x80


def byte_to_cp(data: bytes, pos: int) -> int | None:
    """Deterministic byte -> code point mapping (None = bisected position)."""
    if not on_code_point_boundary(data, pos):
        return None
    return len(data[:pos].decode("utf-8"))


def cp_to_byte(text: str, cp: int) -> int:
    """Deterministic code point -> byte mapping (exact inverse of byte_to_cp)."""
    return len(text[:cp].encode("utf-8"))


# ---------------------------------------------------------------------------
# structural policy v2 (frozen config; loaded once, validated)
# ---------------------------------------------------------------------------
_policy_cache: dict | None = None


def load_policy_v3() -> dict:
    """Load and validate the active structural policy v3 (fail-closed).

    008-g: the bounded mid-document raw-block fix supersedes policy v2 with
    v3 (the v2 file remains byte-identical in-tree). The candidate rule is
    carried over byte-identically, so the cached value shape is unchanged.
    """
    global _policy_cache
    if _policy_cache is None:
        try:
            config = json.loads(POLICY_V3_PATH.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ProtectionFallback("policy-v3-unreadable") from exc
        if config.get("schema") != "008g-structural-policy/3":
            raise ProtectionFallback("policy-v3-schema-mismatch")
        rule = config.get("candidate_rule")
        if not isinstance(rule, dict):
            raise ProtectionFallback("policy-v3-candidate-rule-missing")
        _policy_cache = {
            "prose": list(rule["PROSE_CONTAINERS"]),
            "non_prose": list(rule["NON_PROSE_CONTAINERS"]),
        }
    return _policy_cache


def load_policy_v2() -> dict:
    """Compatibility alias (008-g): loads the active policy (v3).

    The candidate rule is byte-identical between v2 and v3 (v3 changelog
    'unchanged' clause); the frozen 008-f harness and the 008-c focused test
    suite call this entry point unchanged.
    """
    return load_policy_v3()


def policy_match(token: str, entries: list[str]) -> bool:
    """D1 token-family matching (carried unchanged from the 008-a evaluator):
    a family entry matches its own token or any level-suffixed token."""
    return any(token == e or token.startswith(e + ":") for e in entries)


# ---------------------------------------------------------------------------
# helper resolution (fail-closed; every candidate sha256-verified)
# ---------------------------------------------------------------------------
def _candidate_parents() -> list[Path]:
    parents: list[Path] = []
    env_parent = os.environ.get(RUNTIME_PARENT_ENV_VAR)
    if env_parent:
        parents.append(Path(env_parent))
    parents.append(Path.home() / ".local" / "share" / "llm-slovenian-repair")
    return parents


def find_helper() -> Path | None:
    """Locate the pinned helper (sha256-verified). None = unavailable."""
    env_path = os.environ.get(HELPER_ENV_VAR)
    if env_path:
        candidate = Path(env_path)
        return candidate if _verify_helper(candidate) else None
    for parent in _candidate_parents():
        if not parent.is_dir():
            continue
        patterns = (
            f"research-runtime-*{os.sep}{HELPER_SUBDIR_GLOB}",
            HELPER_SUBDIR_GLOB,  # the parent may be the runtime root itself
        )
        for pattern in patterns:
            for candidate in sorted(parent.glob(pattern)):
                if _verify_helper(candidate):
                    return candidate
    return None


def _verify_helper(candidate: Path) -> bool:
    """Regular file with the pinned sha256 (fail-closed on any mismatch)."""
    try:
        if not candidate.is_file() or candidate.is_symlink():
            return False
        if candidate.stat().st_size == 0:
            return False
        return hashlib.sha256(candidate.read_bytes()).hexdigest() == HELPER_PINNED_SHA256
    except OSError:
        return False


def resolve_helper_path(helper_path: str | Path | None = None) -> tuple[Path | None, str | None]:
    """Resolve the helper for one call. Returns (path, fallback_reason).

    An explicit path that fails verification is a hard identity mismatch
    (never silently re-discovered). Without an explicit path, auto-discovery
    is attempted; absence is "helper-unavailable".
    """
    if helper_path is not None:
        candidate = Path(helper_path)
        if not candidate.is_file():
            return None, "helper-unavailable"
        if not _verify_helper(candidate):
            return None, "helper-identity-mismatch"
        return candidate, None
    found = find_helper()
    if found is None:
        return None, "helper-unavailable"
    return found, None


# ---------------------------------------------------------------------------
# helper invocation and protocol validation (fail-closed)
# ---------------------------------------------------------------------------
def _run_helper(helper: Path, data: bytes) -> bytes:
    """Invoke the pinned helper; raise ProtectionFallback on any failure."""
    try:
        proc = subprocess.run(
            [str(helper), HELPER_PROFILE],
            input=data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=HELPER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise ProtectionFallback("helper-timeout") from exc
    except (OSError, subprocess.SubprocessError) as exc:
        raise ProtectionFallback("helper-unavailable") from exc
    if proc.returncode != 0:
        raise ProtectionFallback(f"helper-exit-{proc.returncode}")
    return proc.stdout


def parse_protocol(raw: bytes, data: bytes) -> list[tuple[str, int, int]]:
    """Parse and validate the JSONL event protocol (fail-closed).

    Returns the event list as (kind, start_byte, end_byte) tuples.
    Enforced, per policy v2: valid UTF-8; one JSON object per line; event
    lines carry exactly the fields i/k/s/e; i strictly increases from 0;
    integer s/e within [0, len(data)] with s <= e and both on UTF-8 code
    point boundaries; Start/End tags balanced with matching family tokens;
    a single final {"eof":true} line.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProtectionFallback("protocol-not-utf8") from exc
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()  # trailing newline
    events: list[tuple[str, int, int]] = []
    stack: list[str] = []
    expected_i = 0
    for idx, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ProtectionFallback("protocol-malformed") from exc
        if not isinstance(obj, dict):
            raise ProtectionFallback("protocol-malformed")
        if "eof" in obj:
            if idx != len(lines) - 1:
                raise ProtectionFallback("protocol-early-eof")
            if stack:
                raise ProtectionFallback("protocol-unbalanced")
            return events
        for key in ("i", "k", "s", "e"):
            if key not in obj:
                raise ProtectionFallback("protocol-malformed")
        i, kind, s, e = obj["i"], obj["k"], obj["s"], obj["e"]
        if type(i) is not int or i != expected_i:
            raise ProtectionFallback("protocol-out-of-order")
        expected_i += 1
        if type(kind) is not str:
            raise ProtectionFallback("protocol-malformed")
        if type(s) is not int or type(e) is not int:
            raise ProtectionFallback("protocol-malformed")
        if s < 0 or e > len(data) or s > e:
            raise ProtectionFallback("coordinate-out-of-bounds")
        if not on_code_point_boundary(data, s) or not on_code_point_boundary(data, e):
            raise ProtectionFallback("coordinate-bisection")
        events.append((kind, s, e))
        if kind.startswith("S."):
            stack.append(kind)
        elif kind.startswith("E."):
            if not stack:
                raise ProtectionFallback("protocol-unbalanced")
            top = stack.pop()[2:]
            end_tok = kind[2:]
            # family match: identical tokens, or the start token is a
            # level-suffixed member of the end family (S.CodeBlock:Fenced ->
            # E.CodeBlock; S.List:ol:2 -> E.List:ol; S.Head:2 -> E.Head:2)
            if top != end_tok and not top.startswith(end_tok + ":"):
                raise ProtectionFallback("protocol-unbalanced")
    raise ProtectionFallback("protocol-truncated")


def candidate_prose(
    events: list[tuple[str, int, int]], data: bytes, policy: dict
) -> list[tuple[int, int]]:
    """Text-leaf byte ranges that are candidate prose under policy v2.

    Ported unchanged from the 008-a evaluator (run_increment1.py): a Text
    event is candidate prose iff its open-tag ancestor set intersects
    PROSE_CONTAINERS and does not intersect NON_PROSE_CONTAINERS (D1
    token-family matching), with the D0 autolink-destination rule: the only
    S.Link whose original source slice starts with byte '<' is an autolink
    and its inner Text leaf is the destination (PROTECTED).
    """
    prose_entries = list(policy["prose"])
    non_prose_entries = list(policy["non_prose"])
    stack: list[tuple[str, int]] = []
    out: list[tuple[int, int]] = []
    for kind, s, e in events:
        if kind.startswith("S."):
            stack.append((kind, s))
        elif kind.startswith("E."):
            stack.pop()
        elif kind == "Text":
            tokens = [t for t, _ in stack]
            if not any(policy_match(t, prose_entries) for t in tokens):
                continue
            if any(policy_match(t, non_prose_entries) for t in tokens):
                continue
            if any(
                t == "S.Link" and data[ss:ss + 1] == b"<"
                for t, ss in stack
            ):
                continue
            out.append((s, e))
    return out


GLUE_INLINE_KINDS = frozenset((
    # inline Markdown/HTML/mathy syntax whose delimiter bytes are not Text
    # leaves but which never delimit a block: emphasis/strong/strike runs,
    # link/image syntax, inline HTML tags, inline/display math delimiters
    "S.Emph",
    "S.Strong",
    "S.Strike",
    "S.Link",
    "S.Image",
    "InlineHtml",
    "InlineMath",
    "DisplayMath",
))


def prose_contexts(
    events: list[tuple[str, int, int]],
    candidate_ranges: list[tuple[int, int]],
    data: bytes,
) -> list[tuple[int, int]]:
    """Maximal byte intervals over which the residual layer operates.

    A prose context is a maximal run of bytes that are candidate prose or
    glue, containing at least one candidate-prose byte. Glue is: SoftBreak /
    HardBreak bytes, an escape backslash byte immediately preceding a
    candidate Text leaf (pulldown-cmark emits the escaped character as the
    Text leaf but consumes the backslash, so the backslash byte is outside
    every Text range), and the byte ranges of inline structural events
    (GLUE_INLINE_KINDS: emphasis/strong/strikethrough delimiter runs,
    link/image syntax, inline HTML tags, inline/display math delimiters).

    Merging over glue is what lets the frozen residual classes see complete
    structures whose delimiter bytes are not Text bytes (e.g. a TeX
    environment pair whose subscript underscores the parser reads as an
    emphasis run, or a bare-JSON value containing emphasis). Block-level
    structure (code, HTML blocks, tables, metadata, list/heading markers,
    blank lines, inline code spans) still breaks contexts, so the residual
    layer never operates across a block boundary. Protection still only
    ever results from residual matches; glue bytes inside a residual span
    are already structurally protected (non-candidate).

    A residual span may span glue bytes. The one start restriction the
    caller enforces (the residual loop in protection_with_status): a span
    whose first byte lies inside a Markdown link/image syntax event
    (S.Link / S.Image source-slice bytes) is not applied, because such a
    match re-parses Markdown structure (e.g. the bracket alternative of
    the bare-json class matching a link's ``[label]`` brackets) in
    violation of the frozen residual scope, and would protect exposed
    prose such as link labels. Spans starting on other glue bytes (TeX /
    math delimiters, emphasis delimiters, escape backslashes) are kept:
    the frozen class spec explicitly protects e.g. the math-like
    remainder after an unpaired opening math delimiter, and the dev
    corpus shows those spans carry protected content.
    """
    n = len(data)
    cand = bytearray(n)
    for s, e in candidate_ranges:
        for i in range(s, e):
            cand[i] = 1
    glue = bytearray(n)
    for kind, s, e in events:
        if kind in ("SoftBreak", "HardBreak") or kind in GLUE_INLINE_KINDS:
            for i in range(s, e):
                glue[i] = 1
    for s, e in candidate_ranges:
        if s > 0 and data[s - 1:s] == b"\\":
            glue[s - 1] = 1
    contexts: list[tuple[int, int]] = []
    i = 0
    while i < n:
        if cand[i] or glue[i]:
            start = i
            has_cand = cand[i] == 1
            i += 1
            while i < n and (cand[i] or glue[i]):
                has_cand = has_cand or cand[i] == 1
                i += 1
            if has_cand:
                contexts.append((start, i))
        else:
            i += 1
    return contexts


# ---------------------------------------------------------------------------
# structural protected set (parser-derived; non-candidate bytes)
# ---------------------------------------------------------------------------
def _merge_byte_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []
    ordered = sorted(ranges)
    out = [[ordered[0][0], ordered[0][1]]]
    for s, e in ordered[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def _subtract_byte_ranges(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """a minus union(b), in byte space (both pre-merged, non-overlapping)."""
    out: list[list[int]] = [[s, e] for s, e in a]
    for bs, be in b:
        nxt: list[list[int]] = []
        for s, e in out:
            if be <= s or bs >= e:
                nxt.append([s, e])
                continue
            if bs > s:
                nxt.append([s, bs])
            if be < e:
                nxt.append([be, e])
        out = nxt
    return [(s, e) for s, e in out]


def structural_protected(
    candidate_ranges: list[tuple[int, int]], data_len: int
) -> list[tuple[int, int]]:
    """Protected byte ranges derived from the parse (policy v2).

    The structural protected set is the complement of the candidate-prose
    bytes: every byte that is not candidate prose is protected (machine
    content, structural delimiters and markers, whitespace outside prose).
    This is exactly the 008-a side-B semantics ("B-protected = complement of
    the candidate set") carried into the runtime, so the 008-a fixture
    baseline re-derives with zero protected-region exposures and zero
    missing prose bytes.
    """
    return _candidate_complement(_merge_byte_ranges(candidate_ranges), data_len)


def _candidate_complement(candidates: list[tuple[int, int]], data_len: int) -> list[tuple[int, int]]:
    """Complement of pre-merged candidate ranges within [0, data_len)."""
    out: list[tuple[int, int]] = []
    pos = 0
    for s, e in candidates:
        if s > pos:
            out.append((pos, s))
        pos = max(pos, e)
    if pos < data_len:
        out.append((pos, data_len))
    return out


# ---------------------------------------------------------------------------
# residual semantic recognizers (policy v2 residual layer)
#
# Narrow, content-level, candidate-prose-only, code-point coordinates.
# Mirror of the active residual class spec (structural-policy-v3.json,
# schema 008g-structural-policy/3; its v2 content is carried byte-identical
# per the v3 "unchanged" clause, plus the 008-g yaml-toml-config strict
# single-line extension and the new xml-fragment class) and of the builder's
# oracle block (research/prose-boundary/tools/prose_boundary_builder.py);
# the dev-corpus safety metric empirically verifies label/runtime agreement.
# No Markdown-delimiter regexes; no reparsing of code, parser-recognized
# math, HTML, or metadata.
# ---------------------------------------------------------------------------
TEX_ENVS = (
    "equation", "equation*", "align", "align*", "aligned", "gather", "gather*",
    "gathered", "eqnarray", "matrix", "pmatrix", "bmatrix", "vmatrix", "cases",
    "split",
)
SHELL_COMMANDS = (
    "sudo", "python", "python3", "uv", "git", "curl", "npm", "npx", "pip",
    "pipx", "pytest", "ruff", "mypy", "cargo", "make", "gcc", "g++", "cc",
    "rustc", "ls", "cat", "grep", "awk", "sed", "echo", "export", "cd", "mv",
    "cp", "rm", "mkdir", "touch", "tar", "zip",
)

RE_URL = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
RE_PATH = re.compile(r"(?<!\w)(?:\.?/|~/|[A-Za-z]:[\\/])[^\s`<>]+")
RE_REL_PATH = re.compile(r"(?<!\w)[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+(?!\w)")
RE_SHELL_LINE = re.compile(
    r"(?m)^\s*(?:[$#>]\s+|(?:sudo\s+)?("
    + "|".join(re.escape(c) for c in SHELL_COMMANDS)
    + r")\s+)\S[^\n]*$"
)
RE_FLAG = re.compile(r"(?<![\w-])(?:--[A-Za-z][\w-]*|-[A-Za-z][\w-]*)(?![\w-])")
RE_ENV_BRACED = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}")
RE_ENV_BARE = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*(?!\w)")
RE_IDENT = re.compile(
    r"(?<!\w)(?=[A-Za-z_]*\d|[A-Za-z_]*_[A-Za-z_])[A-Za-z_][A-Za-z0-9_]*(?!\w)"
)
RE_UPPER = re.compile(r"(?<!\w)[A-Z][A-Z0-9_]{1,}(?!\w)")
RE_NUMBER = re.compile(r"(?<!\w)[+-]?(?:\d+(?:[.,]\d+)?)(?:\s?(?:%|[A-Za-z]{1,8}))?(?!\w)")
RE_TEX_ENV_BEGIN = re.compile(r"\\begin\{(" + "|".join(re.escape(e) for e in TEX_ENVS) + r")\}")
RE_TEX_ENV_END = re.compile(r"\\end\{(" + "|".join(re.escape(e) for e in TEX_ENVS) + r")\}")
RE_KEY_LINE = re.compile(r"^\s*[A-Za-z0-9_.-]+\s*[:=]")
RE_SECTION_LINE = re.compile(r"^\s*\[[^\]\n]+\]")
RE_MATHLIKE = re.compile(r"\\[A-Za-z]+|[\u0391-\u03C9\u03B1-\u03C9\u03A3\u03A4]|\d|[+*/=^_{}<>=\\]")

TEX_SPAN_LIMITS = {"paren": 200, "bracket": 500, "env": 1000}


def _env_name_ok(name: str) -> bool:
    return ("_" in name) or (name.isupper() and len(name) >= 2)


def _tex_spans(text: str) -> list[tuple[str, int, int]]:
    """tex-paren / tex-bracket / tex-env spans (class, start, end), cp coords."""
    spans: list[tuple[str, int, int]] = []
    BS = chr(92)  # backslash; explicit to keep this source escape-free
    paren_open_seq = BS + "("
    paren_close_seq = BS + ")"
    bracket_open_seq = BS + "["
    bracket_close_seq = BS + "]"
    paren_open = re.compile(re.escape(paren_open_seq))
    bracket_open = re.compile(re.escape(bracket_open_seq))
    for m in paren_open.finditer(text):
        close = text.find(paren_close_seq, m.end())
        if close != -1:
            inner = text[m.start():close + 2]
            if "\n" not in inner and len(inner) <= TEX_SPAN_LIMITS["paren"]:
                spans.append(("tex-paren", m.start(), close + 2))
                continue
        tail = text[m.start():]
        if len(tail) <= TEX_SPAN_LIMITS["paren"] and RE_MATHLIKE.search(tail[2:]):
            spans.append(("tex-paren", m.start(), m.start() + len(tail)))
    for m in bracket_open.finditer(text):
        close = text.find(bracket_close_seq, m.end())
        if close != -1:
            inner = text[m.start():close + 2]
            if len(inner) <= TEX_SPAN_LIMITS["bracket"]:
                spans.append(("tex-bracket", m.start(), close + 2))
                continue
        tail = text[m.start():]
        if len(tail) <= TEX_SPAN_LIMITS["bracket"] and RE_MATHLIKE.search(tail[2:]):
            spans.append(("tex-bracket", m.start(), m.start() + len(tail)))
    for m in RE_TEX_ENV_BEGIN.finditer(text):
        name = m.group(1)
        end_seq = BS + "end"
        end_re = re.compile(re.escape(end_seq) + r"\{" + re.escape(name) + r"\}")
        close = end_re.search(text, m.end())
        if close is not None and close.end() - m.start() <= TEX_SPAN_LIMITS["env"]:
            spans.append(("tex-env", m.start(), close.end()))
        else:
            limit = min(len(text), m.start() + TEX_SPAN_LIMITS["env"])
            spans.append(("tex-env", m.start(), limit))
    return spans


def _json_spans(text: str) -> list[tuple[int, int]]:
    """bare-json spans: balanced runs or truncated runs to end of line."""
    spans: list[tuple[int, int]] = []
    pos = 0
    while pos < len(text):
        ch = text[pos]
        if ch not in "{[":
            pos += 1
            continue
        depth = 0
        in_str = False
        esc = False
        end = -1
        for i in range(pos, min(len(text), pos + 2000)):
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c in "{[":
                depth += 1
            elif c in "}]":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end != -1:
            spans.append((pos, end + 1))
            pos = end + 1
        else:
            line_end = text.find("\n", pos)
            if line_end == -1:
                line_end = len(text)
            spans.append((pos, line_end))
            pos = line_end
    return spans


# v3 (008-g) config-class extensions. RE_KEY_LINE is carried over unchanged
# from v2 (digit keys allowed) so that every v2 >= 2-line run and section run
# keeps its v2 protection exactly (no new exposure by construction); the v3
# additions are strict and additive.
RE_WORD_KEY_LINE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_.-]*)\s*[:=]\s*(.*)$")
RE_NESTED_LIST_LINE = re.compile(r"^\s*-+\s+\S")
RE_QUOTED_LITERAL = re.compile(r"^([\"']).*\1$")


def _machine_like_value(value: str) -> bool:
    """v3 strictness contract: the whole trimmed value is machine-like -
    a number (optional short unit), a path, a relative path, an identifier,
    an environment-variable form, or a single-line quoted literal."""
    v = value.strip()
    if not v:
        return False
    if RE_NUMBER.fullmatch(v):
        return True
    if RE_PATH.fullmatch(v) or RE_REL_PATH.fullmatch(v):
        return True
    m = RE_IDENT.fullmatch(v)
    if m:
        return True
    if RE_ENV_BRACED.fullmatch(v):
        return True
    m = RE_ENV_BARE.fullmatch(v)
    if m and _env_name_ok(m.group(0)[1:]):
        return True
    return bool(RE_QUOTED_LITERAL.match(v))


def _config_spans(text: str) -> list[tuple[int, int]]:
    """yaml-toml-config spans (v3).

    Carried over from v2 (unchanged behaviour): >= 2 consecutive key/value
    lines (RE_KEY_LINE, digit keys included) and a '[section]' header run.
    v3 additions (008-g scope item 4(a)(1), strictness contract): a single
    word-key line is protected when its whole value is machine-like or it is
    immediately followed by >= 1 nested list-style line (empty value);
    nested list-style lines (dash-plus-space continuation) extend a protected
    key-value run. Pure list runs (no key line) never fire, so Markdown
    prose lists stay candidate prose.
    """
    spans: list[tuple[int, int]] = []
    lines = text.split("\n")
    offsets: list[int] = []
    off = 0
    for ln in lines:
        offsets.append(off)
        off += len(ln) + 1
    n = len(lines)

    def emit(start_line: int, end_line: int) -> None:
        start = offsets[start_line]
        end = offsets[end_line] + len(lines[end_line])
        spans.append((start, end))

    protected_key = [False] * n  # a key line protected in its own right
    i = 0
    while i < n:
        line = lines[i]
        if RE_SECTION_LINE.match(line):
            j = i + 1
            keys = []
            while j < n and RE_KEY_LINE.match(lines[j]):
                keys.append(j)
                j += 1
            if keys:
                for k in keys:
                    protected_key[k] = True
                # v2: the run covers section header through last key line;
                # v3: nested list-style lines following the run extend it.
                end_line = keys[-1]
                k = end_line + 1
                while k < n and RE_NESTED_LIST_LINE.match(lines[k]):
                    end_line = k
                    k += 1
                emit(i, end_line)
            i = j if keys else i + 1
            continue
        if RE_KEY_LINE.match(line):
            j = i
            while j < n and RE_KEY_LINE.match(lines[j]):
                j += 1
            if j - i >= 2:
                # v2 run (carried over): all its key lines are protected.
                for k in range(i, j):
                    protected_key[k] = True
                end_line = j - 1
                k = end_line + 1
                while k < n and RE_NESTED_LIST_LINE.match(lines[k]):
                    end_line = k
                    k += 1
                emit(i, end_line)
                i = end_line + 1
                continue
            # v3: a single key line in its own right.
            wm = RE_WORD_KEY_LINE.match(line)
            if wm is not None:
                value = wm.group(2)
                has_nested = (i + 1 < n
                              and RE_NESTED_LIST_LINE.match(lines[i + 1]) is not None)
                if _machine_like_value(value) or (value.strip() == "" and has_nested):
                    protected_key[i] = True
                    end_line = i
                    k = i + 1
                    while k < n and RE_NESTED_LIST_LINE.match(lines[k]):
                        end_line = k
                        k += 1
                    emit(i, end_line)
                    i = end_line + 1
                    continue
            i = j
            continue
        i += 1
    return spans


# v3 (008-g) xml-fragment class (scope 4(a)(2)). The residual layer sees
# only parser-approved candidate prose; recognized inline-HTML tags are
# structural (InlineHtml events) and never need this class. This
# recognizer covers HTML/XML tag fragments the parser dialect parses as
# paragraph text: namespaced prefix-colon names (with attributes, so the
# autolink path does not claim them) and names outside the dialect's
# recognized tag-name shape. The trigger requires a letter/underscore
# immediately after "<" and a closing ">" on the same line, so comparison
# operators ("< 5", "<5"), a lone angle bracket, and digits after "<"
# never fire; recognized tag names (the dialect vocabulary) abstain so
# recognised-HTML behaviour stays byte-identical to v2.
RE_XML_NAME = r"[A-Za-z_][A-Za-z0-9_.:-]*"
RE_XML_OPEN = re.compile(r"<(" + RE_XML_NAME + r")([^<>\n]*)>")
RE_XML_CLOSE = re.compile(r"</(" + RE_XML_NAME + r")[^<>\n]*>")
# The parser dialect recognizes an inline-HTML tag exactly when the tag
# name has this shape (verified against the pinned pulldown-cmark 0.13.4
# helper: pure letter/digit/hyphen names, any case, with or without
# attributes -> InlineHtml events, never candidate prose; namespaced
# names and names with a period/underscore are not recognized).
RE_XML_DIALECT_NAME = re.compile(r"[A-Za-z][A-Za-z0-9-]*")
XML_FRAGMENT_LIMIT = 2000  # code points; policy v3 xml-fragment span bound


def _xml_name_triggers(name: str) -> bool:
    """True when the class must fire for this tag name: namespaced
    prefix-colon names, or names outside the dialect's recognized
    tag-name shape. Names the dialect recognizes never need the class
    (their tag bytes are structural, never candidate prose), and firing
    on them would over-protect recognised-HTML content (v2 parity)."""
    if ":" in name:
        return True
    return RE_XML_DIALECT_NAME.fullmatch(name) is None


def _xml_fragment_spans(text: str) -> list[tuple[int, int]]:
    """xml-fragment spans (cp coords), deterministic left-to-right scan.

    A paired fragment (opening tag to its matching case-sensitive closing
    tag, or a self-closing marker) is protected in full (<= 2000 cp); an
    unbalanced opening fragment is protected to the end of its line (recorded
    008-g D0 choice: protected, not policy-exposed); a standalone closing tag
    token is protected as a machine fragment.
    """
    spans: list[tuple[int, int]] = []
    pos = 0
    while True:
        lt = text.find("<", pos)
        if lt < 0:
            break
        m = RE_XML_OPEN.match(text, lt)
        if m is not None:
            name = m.group(1)
            if not _xml_name_triggers(name):
                # recognized tag name: the parser owns these bytes
                # (InlineHtml, never candidate prose) - skip the token
                pos = m.end()
                continue
            start = lt
            if m.group(2).endswith("/"):
                # self-closing: the tag token itself
                end = min(m.end(), start + XML_FRAGMENT_LIMIT)
                spans.append((start, end))
                pos = m.end()
                continue
            close = re.compile(
                r"</" + re.escape(name) + r"[^<>\n]*>"
            ).search(text, m.end())
            if close is not None and close.end() - start <= XML_FRAGMENT_LIMIT:
                spans.append((start, close.end()))
                pos = close.end()
                continue
            # unbalanced opening (or over-bound pair): protect to the end
            # of the line containing the opening tag
            eol = text.find("\n", start)
            end = len(text) if eol < 0 else eol
            end = min(end, start + XML_FRAGMENT_LIMIT)
            spans.append((start, end))
            pos = max(pos, end)
            continue
        mc = RE_XML_CLOSE.match(text, lt)
        if mc is not None:
            if _xml_name_triggers(mc.group(1)):
                # standalone closing tag token of a non-recognized name
                end = min(mc.end(), lt + XML_FRAGMENT_LIMIT)
                spans.append((lt, end))
                pos = mc.end()
                continue
            pos = mc.end()
            continue
        pos = lt + 1
    return spans


def residual_spans(text: str) -> list[tuple[str, int, int]]:
    """All residual-class spans in one candidate-prose span (cp coords).

    Returns (class, start, end) tuples for: url, path, relative-path,
    shell (lines and flags), env-var, identifier, upper-identifier, number,
    tex-paren, tex-bracket, tex-env, bare-json, config, xml-fragment.
    """
    spans: list[tuple[str, int, int]] = []
    for m in RE_URL.finditer(text):
        spans.append(("url", m.start(), m.end()))
    for m in RE_PATH.finditer(text):
        spans.append(("path", m.start(), m.end()))
    for m in RE_REL_PATH.finditer(text):
        spans.append(("relative-path", m.start(), m.end()))
    for m in RE_SHELL_LINE.finditer(text):
        spans.append(("shell", m.start(), m.end()))
    for m in RE_FLAG.finditer(text):
        s, e = m.start(), m.end()
        if text.startswith("--", s) and e < len(text) and text[e] == " ":
            m2 = re.match(r"\s+(\S+)", text[e:])
            if m2 and not m2.group(1).startswith("-"):
                e = e + m2.end()
        spans.append(("shell", s, e))
    for m in RE_ENV_BRACED.finditer(text):
        spans.append(("env-var", m.start(), m.end()))
    for m in RE_ENV_BARE.finditer(text):
        name = m.group(0)[1:]
        if _env_name_ok(name):
            spans.append(("env-var", m.start(), m.end()))
    for m in RE_IDENT.finditer(text):
        spans.append(("identifier", m.start(), m.end()))
    for m in RE_UPPER.finditer(text):
        spans.append(("upper-identifier", m.start(), m.end()))
    for m in RE_NUMBER.finditer(text):
        spans.append(("number", m.start(), m.end()))
    spans.extend(_tex_spans(text))
    for s, e in _json_spans(text):
        spans.append(("bare-json", s, e))
    for s, e in _config_spans(text):
        spans.append(("config", s, e))
    for s, e in _xml_fragment_spans(text):
        spans.append(("xml-fragment", s, e))
    return spans


# ---------------------------------------------------------------------------
# LEGACY FULL-REGEX PROTECTION — 008-a rule set, retained verbatim.
#
# This is the fail-closed fallback ONLY (policy v2 fail_closed_fallback).
# It is NOT the happy path: on the parser-first path the Markdown-syntax
# rules (fenced-code, inline-code, markdown-link) are replaced by the
# parser, and the semantic rules run as residual recognizers on
# candidate-prose spans. The output of this function must stay
# byte-identical to the 008-a research/curated/protected.py behaviour
# (code-point coordinates, same rule order, same merge).
# ---------------------------------------------------------------------------
LEGACY_URL = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
LEGACY_PATH = re.compile(r"(?<!\w)(?:\.?/|~/|[A-Za-z]:[\\/])[^\s`<>]+")
LEGACY_RELATIVE_PATH = re.compile(r"(?<!\w)[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+(?!\w)")
LEGACY_NUMBER = re.compile(r"(?<!\w)[+-]?(?:\d+(?:[.,]\d+)?)(?:\s?(?:%|[A-Za-z]{1,8}))?(?!\w)")
LEGACY_IDENTIFIER = re.compile(
    r"(?<!\w)(?=[A-Za-z_]*\d|[A-Za-z_]*_[A-Za-z_])[A-Za-z_][A-Za-z0-9_]*(?!\w)"
)
LEGACY_UPPER_IDENTIFIER = re.compile(r"(?<!\w)[A-Z][A-Z0-9_]{1,}(?!\w)")
LEGACY_JSON_XML = re.compile(r"(?:\{[^\n{}]{0,2000}\}|\[[^\n\[\]]{0,2000}\]|<[/!?]?[A-Za-z][^>]*>)")
LEGACY_SHELL = re.compile(
    r"(?m)^\s*(?:[$#>]\s+|(?:sudo\s+)?(?:python|python3|uv|git|curl|npm|pip|pytest|ruff|mypy)\s+)\S[^\n]*$"
)
LEGACY_FENCE = re.compile(r"(?s)(?:^|\n)(```+|~~~+)[^\n]*\n.*?\n\1(?=\s|$)")
LEGACY_INLINE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
LEGACY_LINK = re.compile(r"!?(?:\[[^\]\n]*\]\([^\)\n]*\)|<https?://[^>]+>)")


def _legacy_merge(intervals: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    if not intervals:
        return []
    ordered = sorted(intervals)
    merged: list[list] = [[ordered[0][0], ordered[0][1], ordered[0][2]]]
    for start, end, reason in ordered[1:]:
        previous = merged[-1]
        if start <= previous[1]:
            previous[1] = max(previous[1], end)
            previous[2] = previous[2] + "+" + reason
        else:
            merged.append([start, end, reason])
    return [(s, e, r) for s, e, r in merged]


def legacy_protected_intervals(
    text: str, tool_arguments: tuple[str, ...] = ()
) -> list[tuple[int, int, str]]:
    """The 008-a full-regex rule set (code-point coordinates, merged).

    Fail-closed fallback only. Byte-identical to the 008-a
    research/curated/protected.py output for the same input.
    """
    intervals: list[tuple[int, int, str]] = []
    for expression, reason in (
        (LEGACY_FENCE, "fenced-code"),
        (LEGACY_INLINE, "inline-code"),
        (LEGACY_LINK, "markdown-link"),
        (LEGACY_URL, "url"),
        (LEGACY_PATH, "path"),
        (LEGACY_RELATIVE_PATH, "relative-path"),
        (LEGACY_SHELL, "shell"),
        (LEGACY_NUMBER, "number"),
        (LEGACY_IDENTIFIER, "identifier"),
        (LEGACY_UPPER_IDENTIFIER, "upper-identifier"),
        (LEGACY_JSON_XML, "structured"),
    ):
        intervals.extend(
            (match.start(), match.end(), reason) for match in expression.finditer(text)
        )
    for argument in tool_arguments:
        if not argument:
            continue
        start = 0
        while True:
            start = text.find(argument, start)
            if start < 0:
                break
            intervals.append((start, start + len(argument), "tool-argument"))
            start += len(argument)
    return _legacy_merge(intervals)


# ---------------------------------------------------------------------------
# public entry point
# ---------------------------------------------------------------------------
def _merge_triples(items: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    """Merge half-open cp intervals, joining reasons of merged neighbours."""
    if not items:
        return []
    ordered = sorted(items)
    merged: list[list] = [[ordered[0][0], ordered[0][1], ordered[0][2]]]
    for start, end, reason in ordered[1:]:
        previous = merged[-1]
        if start <= previous[1]:
            previous[1] = max(previous[1], end)
            if reason not in previous[2].split("+"):
                previous[2] = previous[2] + "+" + reason
        else:
            merged.append([start, end, reason])
    return [(s, e, r) for s, e, r in merged]


def protection_with_status(
    text: str,
    tool_arguments: tuple[str, ...] = (),
    helper_path: str | Path | None = None,
) -> ProtectionResult:
    """Compute the protected intervals for one document (code points).

    parser-first per frozen policy v2 when the pinned helper is available
    and trustworthy; otherwise the legacy full-regex fallback with the
    reason recorded. Never fail-open.
    """
    args = tuple(tool_arguments)
    data = text.encode("utf-8")

    helper, fallback_reason = resolve_helper_path(helper_path)
    if helper is None:
        return ProtectionResult(
            intervals=tuple(legacy_protected_intervals(text, args)),
            mode="legacy-fallback",
            fallback_reason=fallback_reason,
        )

    try:
        raw = _run_helper(helper, data)
        events = parse_protocol(raw, data)
        policy = load_policy_v2()
        candidates = candidate_prose(events, data, policy)
        triples: list[tuple[int, int, str]] = []
        for s, e in structural_protected(candidates, len(data)):
            cs = byte_to_cp(data, s)
            ce = byte_to_cp(data, e)
            if cs is None or ce is None:
                raise ProtectionFallback("coordinate-bisection")
            triples.append((cs, ce, "non-prose"))
        # residual layer: candidate-prose contexts only, code-point
        # coordinates (contexts merge candidate leaves over glue so the
        # frozen recognizers see complete structures).
        #
        # Start-byte guard (policy v2 residual_layer.scope: the layer
        # "must NOT reparse Markdown structure"; excluded_from_residual:
        # "brackets/parens as link syntax ... are NOT residual classes"):
        # a span whose first byte lies inside a Markdown link/image
        # syntax event is not applied. A class match beginning inside
        # link/image syntax reinterprets that syntax (e.g. the
        # bare-json bracket alternative on a link's "[label]" brackets,
        # protecting the label, which the frozen policy keeps EXPOSED).
        # Every protected byte such a span covers is non-candidate
        # (destination text, brackets) and already structurally
        # protected, so dropping it loses no protection; dev-corpus
        # measurement over all 19,018 residual spans confirms zero
        # ground-truth-protected candidate bytes under this guard.
        # Spans starting on other glue bytes (TeX/math delimiters,
        # emphasis delimiters, escape backslashes) are kept: the frozen
        # class spec explicitly protects e.g. the math-like remainder
        # after an unpaired "\(", and those spans carry protected
        # content in the dev corpus.
        link_syntax_byte = bytearray(len(data))
        for kind, s, e in events:
            if kind in ("S.Link", "S.Image"):
                for i in range(s, e):
                    link_syntax_byte[i] = 1
        for s, e in prose_contexts(events, candidates, data):
            cs = byte_to_cp(data, s)
            ce = byte_to_cp(data, e)
            if cs is None or ce is None:
                raise ProtectionFallback("coordinate-bisection")
            span_text = text[cs:ce]
            for cls, rs, re_ in residual_spans(span_text):
                # span offsets are context-relative: the start byte is the
                # context start plus the context-prefix re-encode (keeps
                # the per-span cost at context scale, not document scale)
                start_byte = s + len(span_text[:rs].encode("utf-8"))
                if link_syntax_byte[start_byte]:
                    continue
                triples.append((cs + rs, cs + re_, f"residual-{cls}"))
    except ProtectionFallback as exc:
        return ProtectionResult(
            intervals=tuple(legacy_protected_intervals(text, args)),
            mode="legacy-fallback",
            fallback_reason=str(exc),
        )

    for argument in args:
        if not argument:
            continue
        start = 0
        while True:
            start = text.find(argument, start)
            if start < 0:
                break
            triples.append((start, start + len(argument), "tool-argument"))
            start += len(argument)

    return ProtectionResult(
        intervals=tuple(_merge_triples(triples)),
        mode="parser-first",
        fallback_reason=None,
        event_count=len(events),
        candidate_count=len(candidates),
    )

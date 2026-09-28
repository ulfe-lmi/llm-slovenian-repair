#!/usr/bin/env python3
"""008-c deterministic mashup builder (order 008-c scope items 6, 7, 8, 12).

Composes final documents from the frozen component pools using a documented
seeded PRNG, layout templates and multi-layer interaction patterns, and emits
for every document a machine-readable ground-truth interval map (byte ranges +
code-point ranges + component provenance IDs + expected role per region).

008-h composition contract (released; order 008-h scope item 3):
  R1 - a fenced or indented code component is never composed on the line
       immediately after an HTML closing-tag line; when a template would
       produce that adjacency the builder inserts exactly one blank line
       (recorded in the document composition provenance; the inserted bytes
       are template-owned NEUTRAL delimiter).

008-i composition contract extension (released; order 008-i scope item 3):
  R1 EXT - R1 fires for ALL dialect HTML block-start lines (pulldown-cmark
       0.13.4 types 1-7: closing-tag lines, opening-tag lines with
       continuation, unterminated comment/PI/CDATA/declaration lines,
       pre/style/script/textarea lines), not only closing-tag lines; the
       008-h test-pinned corner (a bare single complete opening tag at EOL)
       stays unbarred by the preserved 008-h contract (disclosed in
       REPORT-008I.md boundary_fidelity).
  DD - display-dollar adjacency guard: a
       malformed-incomplete-display-dollar component (unterminated $$
       opener) is never composed immediately before a component whose
       first line opens a display-dollar expression; on fire the builder
       inserts exactly one NEUTRAL-labeled blank line (the predeclared
       barrier, verified to break the dialect's cross-pairing).
  T6 ADMISSION - T6-prose-link-prose link-destination fragments must be
       clean URLs (https?:// with no whitespace/angle brackets), making
       the v3 prescan invariant explicit and builder-asserted.
  INVARIANTS - after both guards, the builder re-checks fail-closed that
       no guarded adjacency survives in the final segment list.
  R2 - structured-keyvalue components containing a list-item-style line
       (list marker plus space) with paired emphasis markers or quoted
       emphasis-like content are not admitted to the 008-h (v3) component
       pool (admission predicate r2_keyvalue_list_item_emphasis_excluded;
       the rule, its hash-only matching criterion and the excluded count are
       recorded in generation-identity-008h.json).
  R3 - structured-xml components containing a tag name with non-ASCII letters
       are not admitted to the v3 pool when the xml-fragment trigger decision
       is FALLBACK (admission predicate r3_xml_diacritic_tag_excluded).
  label_source - every labelled region records whether its role is
       construction-labeled (fixed by composition / parser structure by
       construction) or oracle-refined (decided by the frozen residual spec /
       label oracle).

Ground-truth principle: label construction is composition-only. The builder
never invokes the parser or the protection layer. Where a component's expected
protection depends on the frozen structural policy v2 (residual classes,
structural events), the labels are derived from that FROZEN SPEC (the residual
class block below mirrors research/prose-boundary/config/
structural-policy-v2.json, sha256
996f465784bed37a179be337e2af606b2dc350cacba6341479371d2812c5a88e) plus the
composition provenance (which fragment sits where); the dev-corpus evaluation
then empirically verifies runtime agreement with these frozen-spec labels.

Label invariants: regions tile each document exactly (no overlaps, no gaps);
byte + code-point ranges are exact; reproduction is deterministic from
component IDs + seed. Component pools are intentionally reused across
documents (thousands of documents from hundreds of components); exclusion is
per-document.

Outputs:
  dev (committed):  corpus/documents-dev/*.json, corpus/labels-dev/*.json,
                    corpus/manifests/corpus-census.json
  hidden (private root only, never committed):
                    008c-hidden/documents/*.json, 008c-hidden/labels/*.json
  hidden manifest (committed, content-free): corpus/manifests/hidden-manifest.json
  seal verification (committed, content-free): corpus/manifests/seal-verification.json

Usage:
  python3 -B prose_boundary_builder.py --runtime-root <private parent> --repo-root <repo>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

DOC_BYTES_MIN, DOC_BYTES_MAX = 200, 4000
DEV_DOCS, HIDDEN_DOCS = 3000, 2000
REROLL_BUDGET = 400
PATTERN_MINIMUM = 5

# ============================================================================
# Frozen residual class spec (structural-policy-v2.json, schema
# 008c-structural-policy/2). This block is the builder's oracle copy of the
# 008-c residual classes; the runtime copy in research/curated/prose_boundary.py
# must implement the same classes (the dev-corpus safety metric empirically
# verifies label/runtime agreement; no Markdown-delimiter regexes appear here).
# ============================================================================
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
RE_HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")
RE_EMAIL = re.compile(r"(?<![\w.@-])[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.@-])")
RE_MATHLIKE = re.compile(r"\\[A-Za-z]+|[\u0391-\u03C9\u03B1-\u03C9\u03A3\u03A4]|\d|[+*/=^_{}<>=\\]")

TEX_SPAN_LIMITS = {"paren": 200, "bracket": 500, "env": 1000}


def _env_name_ok(name: str) -> bool:
    return ("_" in name) or (name.isupper() and len(name) >= 2)


def tex_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
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
                spans.append((m.start(), close + 2))
                continue
        tail = text[m.start():]
        if len(tail) <= TEX_SPAN_LIMITS["paren"] and RE_MATHLIKE.search(tail[2:]):
            spans.append((m.start(), m.start() + len(tail)))
    for m in bracket_open.finditer(text):
        close = text.find(bracket_close_seq, m.end())
        if close != -1:
            inner = text[m.start():close + 2]
            if len(inner) <= TEX_SPAN_LIMITS["bracket"]:
                spans.append((m.start(), close + 2))
                continue
        tail = text[m.start():]
        if len(tail) <= TEX_SPAN_LIMITS["bracket"] and RE_MATHLIKE.search(tail[2:]):
            spans.append((m.start(), m.start() + len(tail)))
    for m in RE_TEX_ENV_BEGIN.finditer(text):
        name = m.group(1)
        end_seq = BS + "end"
        end_re = re.compile(re.escape(end_seq) + r"\{" + re.escape(name) + r"\}")
        close = end_re.search(text, m.end())
        if close is not None and close.end() - m.start() <= TEX_SPAN_LIMITS["env"]:
            spans.append((m.start(), close.end()))
        else:
            limit = min(len(text), m.start() + TEX_SPAN_LIMITS["env"])
            spans.append((m.start(), limit))
    return spans


def json_spans(text: str) -> list[tuple[int, int]]:
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


def config_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    lines = text.split("\n")
    offsets: list[int] = []
    off = 0
    for ln in lines:
        offsets.append(off)
        off += len(ln) + 1
    n = len(lines)
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
                start = offsets[i]
                end = offsets[keys[-1]] + len(lines[keys[-1]])
                spans.append((start, end))
            i = j if keys else i + 1
            continue
        if RE_KEY_LINE.match(line):
            j = i
            while j < n and RE_KEY_LINE.match(lines[j]):
                j += 1
            if j - i >= 2:
                start = offsets[i]
                end = offsets[j - 1] + len(lines[j - 1])
                spans.append((start, end))
            i = j
            continue
        i += 1
    return spans


def residual_spans(text: str) -> list[tuple[int, int]]:
    """Frozen v2 residual classes over one candidate-prose span (cp coords)."""
    spans: list[tuple[int, int]] = []
    for m in RE_URL.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_PATH.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_REL_PATH.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_SHELL_LINE.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_FLAG.finditer(text):
        s, e = m.start(), m.end()
        if text.startswith("--", s) and e < len(text) and text[e] == " ":
            m2 = re.match(r"\s+(\S+)", text[e:])
            if m2 and not m2.group(1).startswith("-"):
                e = e + m2.end()
        spans.append((s, e))
    for m in RE_ENV_BRACED.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_ENV_BARE.finditer(text):
        name = m.group(0)[1:]
        if _env_name_ok(name):
            spans.append((m.start(), m.end()))
    for m in RE_IDENT.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_UPPER.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_NUMBER.finditer(text):
        spans.append((m.start(), m.end()))
    spans.extend(tex_spans(text))
    spans.extend(json_spans(text))
    spans.extend(config_spans(text))
    return merge_spans(spans)


def merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not spans:
        return []
    ordered = sorted(set(spans))
    out: list[list[int]] = [[ordered[0][0], ordered[0][1]]]
    for s, e in ordered[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


# --------------------------------------------------------------------------
# deterministic PRNG (Mersenne Twister via random.Random, stable across runs)
# --------------------------------------------------------------------------
def make_rng(seed_hex: str) -> random.Random:
    return random.Random(int(seed_hex, 16))


# --------------------------------------------------------------------------
# component loading
# --------------------------------------------------------------------------
def load_pool(root: Path) -> dict[str, list[dict]]:
    pool: dict[str, list[dict]] = {}
    for path in sorted(root.glob("*/*.json")):
        records = json.loads(path.read_text(encoding="utf-8"))
        for record in records:
            pool.setdefault(record["family"], []).append(record)
    return pool


def one_line(fragment: str, limit: int) -> str:
    line = fragment.splitlines()[0] if fragment.splitlines() else fragment
    line = line.strip()
    return line if len(line) <= limit else line[:limit]


def first_url(fragment: str) -> str | None:
    match = re.search(r"https?://[^\s\)\]<>\"']+", fragment)
    return match.group(0) if match else None


# --------------------------------------------------------------------------
# segment model: (text, component_id, role, label_source)
# roles: PROSE / PROTECTED / NEUTRAL / POLICY_EXPOSED
# label_source: "construction" (role fixed by composition / parser structure
# by construction) or "oracle-refined" (role decided by the frozen residual
# spec / the label oracle)
# --------------------------------------------------------------------------

CONSTRUCTION = "construction"
ORACLE_REFINED = "oracle-refined"


def assert_no_parser_participation() -> None:
    """Composition-only ground-truth guarantee (008-c principle, carried into
    008-h): label construction uses ONLY the composition (component
    provenance, template glue) and the declared label oracle (the
    module-level residual_spans function, swappable at build time only by the
    generation/build script and recorded in the generation identity). The
    builder module must never reference the parser or the protection layer."""
    for name in list(globals()):
        if name.startswith("__"):
            continue
        obj = globals()[name]
        mod = getattr(obj, "__module__", "")
        if isinstance(mod, str) and mod.startswith("research.curated"):
            raise AssertionError(
                f"parser/protection reference leaked into the builder: {name}")


# --------------------------------------------------------------------------
# 008-h composition contract (R1) and admission predicates (R2/R3)
# --------------------------------------------------------------------------
RE_HTML_CLOSING_TAG_LINE = re.compile(r"^\s*</[A-Za-z][^>]*>\s*$")
RE_FENCE_OPEN_LINE = re.compile(r"^\s{0,3}(```+|~~~+)")
RE_INDENTED_CODE_LINE = re.compile(r"^( {4}|\t)\S")
RE_R2_LIST_ITEM_LINE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
RE_R2_PAIRED_EMPHASIS = re.compile(r"(\*\*[^*\n]+\*\*|__[^_\n]+__)")
RE_R2_QUOTED_PHRASE = re.compile(r'\"[^"\n]{1,200}\"')
RE_R3_XML_TAG = re.compile(r"</?([A-Za-z\u00C0-\u024F\u0100-\u017F][^<>]{0,120})>")


def last_line_is_html_closing_tag(text: str) -> bool:
    t = text.rstrip("\n")
    if not t:
        return False
    return RE_HTML_CLOSING_TAG_LINE.match(t.rsplit("\n", 1)[-1]) is not None


def first_line_starts_code_block(text: str) -> bool:
    first = text.split("\n", 1)[0]
    return RE_FENCE_OPEN_LINE.match(first) is not None or \
        RE_INDENTED_CODE_LINE.match(first) is not None


def apply_r1(segs: list[tuple[str, str, str, str]]) -> tuple[list[tuple[str, str, str, str]], int]:
    """R1 composition contract (order 008-h scope item 3b; EXTENDED per
    order 008-i scope item 3a): a fenced or indented code component is
    never composed on the line immediately after an HTML block-start line
    (is_html_block_start_line: the dialect HTML block types 1-7, minus the
    008-h test-pinned bare-single-opening-tag corner). Blocks = maximal
    runs of consecutive same-kind segments (template glue vs component).
    The adjacency exists in the document exactly when: the separator
    between two component blocks is exactly one LF (no blank line), the
    previous block's text does not end with a newline, its last line is an
    HTML block-start line, and the next block's first line opens a
    fenced/indented code block. In that case exactly one blank line
    (template-owned NEUTRAL delimiter) is inserted. Returns
    (new_segments, insertions)."""
    blocks: list[tuple[str, list[tuple[str, str, str, str]]]] = []
    for s in segs:
        kind = "template" if s[1].startswith("template") else "component"
        if blocks and blocks[-1][0] == kind:
            blocks[-1][1].append(s)
        else:
            blocks.append((kind, [s]))
    out: list[tuple[str, str, str, str]] = []
    insertions = 0
    for bi, (kind, block) in enumerate(blocks):
        out.extend(block)
        if kind != "component" or bi + 2 >= len(blocks):
            continue
        next_kind, next_block = blocks[bi + 1]
        after_kind, after_block = blocks[bi + 2]
        if next_kind != "template" or after_kind != "component":
            continue
        if "".join(s[0] for s in next_block) != "\n":
            continue
        prev_text = "".join(s[0] for s in block)
        next_text = "".join(s[0] for s in after_block)
        if prev_text.endswith("\n"):
            continue  # a blank line already separates; the HTML block ends there
        if not is_html_block_start_line(
                prev_text.rstrip("\n").rsplit("\n", 1)[-1]):
            continue
        if not first_line_starts_code_block(next_text):
            continue
        out.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        insertions += 1
    return out, insertions


def r2_keyvalue_list_item_emphasis_excluded(fragment: str) -> bool:
    """R2 admission predicate (v3 pool): True when the component contains a
    list-item-style line (list marker plus space) carrying paired emphasis
    markers or a quoted emphasis-like phrase. Such components are NOT
    admitted to the v3 component pool (the composition shape is
    policy-exposed per structural policy v4; the builder composes them away
    rather than extending the residual layer)."""
    return any(RE_R2_LIST_ITEM_LINE.match(ln) and
               (RE_R2_PAIRED_EMPHASIS.search(ln) or RE_R2_QUOTED_PHRASE.search(ln))
               for ln in fragment.split("\n"))


def r3_xml_diacritic_tag_excluded(fragment: str) -> bool:
    """R3 admission predicate (v3 pool, applies only when the xml-fragment
    trigger decision is FALLBACK): True when the component contains an
    HTML/XML tag whose name starts with a letter but carries non-ASCII
    (diacritic) letters - a shape the ASCII-only trigger cannot fire on."""
    for m in RE_R3_XML_TAG.finditer(fragment):
        name = m.group(1).split()[0].rstrip("/")
        if any(ord(ch) > 127 for ch in name):
            return True
    return False


# --------------------------------------------------------------------------
# 008-i composition contract (order 008-i scope item 3): R1 extension to
# dialect HTML block-start lines, display-dollar adjacency guard, T6
# link-destination admission, fail-closed composition invariants.
# Dialect ground truth: pulldown-cmark 0.13.4 vendored source
# (firstpass.rs / scanners.rs; HTML_TAGS below is the dialect's 62-tag
# block-level list verbatim) and pre-work verification against the pinned
# helper (sha256 5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf).
# --------------------------------------------------------------------------
MALFORMED_INCOMPLETE_DISPLAY_DOLLAR = "malformed-incomplete-display-dollar"

# The dialect's HTML_TAGS block-level list (scanners.rs, case-insensitive).
HTML_TAGS_BLOCK_LEVEL = frozenset((
    "address", "article", "aside", "base", "basefont", "blockquote", "body",
    "caption", "center", "col", "colgroup", "dd", "details", "dialog", "dir",
    "div", "dl", "dt", "fieldset", "figcaption", "figure", "footer", "form",
    "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header",
    "hr", "html", "iframe", "legend", "li", "link", "main", "menu",
    "menuitem", "nav", "noframes", "ol", "optgroup", "option", "p", "param",
    "search", "section", "summary", "table", "tbody", "td", "tfoot", "th",
    "thead", "title", "tr", "track", "ul",
))
RE_TYPE1_HEAD = re.compile(r"^[ ]{0,3}<(?:pre|style|script|textarea)")
RE_TYPE6_HEAD = re.compile(r"^[ ]{0,3}</?([A-Za-z0-9]+)")
RE_BARE_COMPLETE_OPEN_TAG_LINE = re.compile(
    r"^[ ]{0,3}<[A-Za-z][A-Za-z0-9]*(?:[ \t][^<>]*)?[ \t]*/?>[ \t]*$")


def is_html_block_start_line(line: str) -> bool:
    """True iff ``line`` starts a pulldown-cmark 0.13.4 HTML block whose
    consumption runs past the end of the line, i.e. it can absorb the line
    composed immediately after it (008-i scope item 3a). Types 1-5:
    <pre|style|script|textarea + EOL/ws/> (to the closing-tag line,
    through blank lines); <!-- to -->; <? to ?>; <![CDATA[ to ]]>; <! +
    ASCII alpha to the first >. Type 6: < or </ + a name in
    HTML_TAGS_BLOCK_LEVEL (case-insensitive) + EOL/space/tab/CR/>. Type 7:
    a complete single-line tag ending at EOL. Types 1-7 all consume lines
    until a blank line (or their terminator / the closing-tag line), so a
    fence composed on the following line is absorbed.

    The 008-g/008-h closing-tag rule (C1) is preserved verbatim. The
    008-h test-pinned corner - a bare single COMPLETE OPENING tag at EOL
    (byte-frozen test test_r1_not_on_non_closing_tag, which the order's
    '008-h R1/R2/R3 contract otherwise stay intact' clause preserves) -
    stays excluded; the residual gap it defines is the disclosed R1 corner
    (REPORT-008I.md boundary_fidelity), monitored by the pre-seal
    diagnostic and the as-is sealing rule."""
    # C1 - the released 008-g/008-h closing-tag line (byte-identical rule).
    if RE_HTML_CLOSING_TAG_LINE.match(line):
        return True
    # C3e - type 1: pre/style/script/textarea + EOL/ws/>, always continues.
    m = RE_TYPE1_HEAD.match(line)
    if m:
        i = m.end()
        return i >= len(line) or line[i] in " \t\r\n>"
    # C3 - types 2-5: unterminated on the same line. A terminator present
    # on the line ends the block on the line (no risk to the next line).
    if re.match(r"^[ ]{0,3}<!--", line):
        return "-->" not in line
    if re.match(r"^[ ]{0,3}<!\[CDATA\[", line):
        return "]]>" not in line
    if re.match(r"^[ ]{0,3}<\?", line):
        return "?>" not in line
    if re.match(r"^[ ]{0,3}<![A-Za-z]", line):
        return ">" not in line
    # C2 - type 6/7 opening-tag lines (the 008-i extension): the line
    # starts a block-level tag and carries continuation (a second tag,
    # trailing content, or an incomplete tag) - a bare single complete
    # opening tag at EOL is the disclosed 008-h pinned corner.
    m = RE_TYPE6_HEAD.match(line)
    if m and m.group(1).lower() in HTML_TAGS_BLOCK_LEVEL:
        i = m.end()
        head_ok = (i >= len(line) or line[i] in " \t\r\n>"
                   or line[i:i + 2] == "/>")
        if head_ok and not RE_BARE_COMPLETE_OPEN_TAG_LINE.match(line):
            return True
    return False


def t6_link_destination_clean(fragment: str) -> bool:
    """008-i scope item 3(c) T6 ADMISSION: True iff the fragment (stripped)
    is exactly one clean URL - https?:// with no whitespace and no angle
    brackets. The v3 pool invariant (prescan-confirmed clean machine-urls,
    REPORT-008H.md section 6) made explicit and builder-asserted."""
    return RE_URL.fullmatch(fragment.strip()) is not None


def _composition_blocks(segs: list[tuple[str, str, str, str]]):
    """Maximal runs of consecutive same-kind segments (kind = template vs
    component) - the block model shared by apply_r1, the display-dollar
    guard, the barrier recount, and the composition invariants."""
    blocks: list[tuple[str, list[tuple[str, str, str, str]]]] = []
    for s in segs:
        kind = "template" if s[1].startswith("template") else "component"
        if blocks and blocks[-1][0] == kind:
            blocks[-1][1].append(s)
        else:
            blocks.append((kind, [s]))
    return blocks


def apply_display_dollar_guard(segs: list[tuple[str, str, str, str]],
                               comp_family: dict[str, str]) -> tuple[list, int]:
    """008-i scope item 3(b) DISPLAY-DOLLAR ADJACENCY GUARD: a
    malformed-incomplete-display-dollar component (unterminated $$ opener)
    is never composed immediately before a component whose first line
    opens a display-dollar expression (a first line of exactly $$); on
    fire, exactly one blank line (template-owned NEUTRAL delimiter) is
    inserted. The predeclared barrier: verified in 008-i pre-work against
    the pinned helper that one blank line breaks the dialect's
    cross-pairing (a $$ degrades to literal paragraph text when a blank
    line precedes the next $$ line, so the complete component then pairs
    with its own closer). The adjacency test mirrors R1's block
    conditions exactly (single-LF template separator between two
    component blocks; previous block text without a trailing newline).
    Returns (new_segments, insertions)."""
    blocks = _composition_blocks(segs)
    out: list[tuple[str, str, str, str]] = []
    insertions = 0
    for bi, (kind, block) in enumerate(blocks):
        out.extend(block)
        if kind != "component" or bi + 2 >= len(blocks):
            continue
        next_kind, next_block = blocks[bi + 1]
        after_kind, after_block = blocks[bi + 2]
        if next_kind != "template" or after_kind != "component":
            continue
        if "".join(s[0] for s in next_block) != "\n":
            continue
        prev_text = "".join(s[0] for s in block)
        if prev_text.endswith("\n"):
            continue  # a blank line already separates; no cross-pairing
        if comp_family.get(block[-1][1]) != MALFORMED_INCOMPLETE_DISPLAY_DOLLAR:
            continue
        if "".join(s[0] for s in after_block).split("\n", 1)[0] != "$$":
            continue
        out.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        insertions += 1
    return out, insertions


def count_display_dollar_barrier_insertions(segs: list[tuple[str, str, str, str]],
                                            comp_family: dict[str, str]) -> int:
    """Recount the display-dollar barriers from a final segment list: a
    malformed-incomplete-display-dollar component block separated from a
    block whose first line is $$ by a two-LF template run (the one-LF
    template separator plus the one inserted NEUTRAL barrier line)."""
    blocks = _composition_blocks(segs)
    count = 0
    for bi, (kind, block) in enumerate(blocks):
        if kind != "component" or bi + 2 >= len(blocks):
            continue
        next_kind, next_block = blocks[bi + 1]
        after_kind, after_block = blocks[bi + 2]
        if next_kind != "template" or after_kind != "component":
            continue
        if "".join(s[0] for s in next_block) != "\n\n":
            continue
        if comp_family.get(block[-1][1]) != MALFORMED_INCOMPLETE_DISPLAY_DOLLAR:
            continue
        if "".join(s[0] for s in after_block).split("\n", 1)[0] != "$$":
            continue
        count += 1
    return count


def assert_composition_invariants(segs: list[tuple[str, str, str, str]],
                                  comp_family: dict[str, str]) -> None:
    """008-i fail-closed re-check of the two composition guards on the
    FINAL segment list (called from compose after both guards have run):
    (R1) no fenced or indented code component starts on the line
    following an HTML block-start line without a neutral barrier; (DD) no
    malformed-incomplete-display-dollar component is immediately followed
    by a display-dollar opener without a neutral barrier. Both checks use
    the same predicates the guards use (including the disclosed bare-
    single-opening-tag corner exclusion), so a violated invariant means a
    guard misfire - the document build fails closed (AssertionError)."""
    blocks = _composition_blocks(segs)
    for bi, (kind, block) in enumerate(blocks):
        if kind != "component" or bi + 2 >= len(blocks):
            continue
        next_kind, next_block = blocks[bi + 1]
        after_kind, after_block = blocks[bi + 2]
        if next_kind != "template" or after_kind != "component":
            continue
        if "".join(s[0] for s in next_block) != "\n":
            continue
        prev_text = "".join(s[0] for s in block)
        if prev_text.endswith("\n"):
            continue
        next_text = "".join(s[0] for s in after_block)
        last_line = prev_text.rstrip("\n").rsplit("\n", 1)[-1]
        if (is_html_block_start_line(last_line)
                and first_line_starts_code_block(next_text)):
            raise AssertionError(
                "R1 invariant violated: an HTML block-start line is "
                "immediately followed by a fenced/indented code component "
                "without a neutral barrier")
        if (comp_family.get(block[-1][1]) == MALFORMED_INCOMPLETE_DISPLAY_DOLLAR
                and next_text.split("\n", 1)[0] == "$$"):
            raise AssertionError(
                "display-dollar invariant violated: a malformed-incomplete-"
                "display-dollar component is immediately followed by a "
                "display-dollar opener without a neutral barrier")

def _covered_map(text: str, spans: list[tuple[int, int]]) -> list[str]:
    """Per-cp coverage marks: 'P' protected, else '.' (gaps classified later)."""
    marks = ["."] * len(text)
    for s, e in spans:
        for i in range(s, e):
            marks[i] = "P"
    return marks


def generic_label(fragment: str, cid: str, policy_exposed_chars: frozenset = frozenset()) -> list[tuple[str, str, str, str]]:
    """Label a fragment by the frozen v2 spec: residual-class spans PROTECTED,
    gaps classified by content (word -> PROSE, email/math-residue/special chars
    -> POLICY_EXPOSED, glue punctuation/whitespace -> NEUTRAL). Every role here
    is decided by the frozen residual spec (the label oracle): ORACLE_REFINED."""
    marks = _covered_map(fragment, residual_spans(fragment))
    segments: list[tuple[str, str, str, str]] = []
    i = 0
    n = len(fragment)

    def flush(start: int, end: int, role: str) -> None:
        if end > start:
            segments.append((fragment[start:end], cid, role, ORACLE_REFINED))

    while i < n:
        if marks[i] == "P":
            j = i
            while j < n and marks[j] == "P":
                j += 1
            flush(i, j, "PROTECTED")
            i = j
            continue
        ch = fragment[i]
        if ch in policy_exposed_chars:
            flush(i, i + 1, "POLICY_EXPOSED")
            i += 1
            continue
        em = RE_EMAIL.match(fragment, i)
        if em:
            flush(i, em.end(), "POLICY_EXPOSED")
            i = em.end()
            continue
        wm = re.match(r"[^\W\d_]+", fragment[i:])
        if wm and wm.group(0):
            flush(i, i + wm.end(), "PROSE")
            i += wm.end()
            continue
        if ch.isspace():
            j = i
            while j < n and fragment[j].isspace() and marks[j] == ".":
                j += 1
            flush(i, j, "NEUTRAL")
            i = j
            continue
        flush(i, i + 1, "NEUTRAL")
        i += 1
    return segments


def label_prose(fragment: str, cid: str) -> list[tuple[str, str, str, str]]:
    return [(fragment, cid, "PROSE", CONSTRUCTION)]


def label_code_block(fragment: str, cid: str, inline: bool = False) -> list[tuple[str, str, str, str]]:
    if inline:
        return [("\u0060", cid, "NEUTRAL", CONSTRUCTION),
                (one_line(fragment, 60), cid, "PROTECTED", CONSTRUCTION),
                ("\u0060", cid, "NEUTRAL", CONSTRUCTION)]
    body = fragment.rstrip("\n")
    return [("```", cid, "NEUTRAL", CONSTRUCTION), ("\n", cid, "NEUTRAL", CONSTRUCTION),
            (body, cid, "PROTECTED", CONSTRUCTION),
            ("\n", cid, "NEUTRAL", CONSTRUCTION), ("```", cid, "NEUTRAL", CONSTRUCTION)]


def _delim_pair(text: str, open_d: str, close_d: str) -> tuple[int, int] | None:
    if not text.startswith(open_d):
        return None
    end = text.rfind(close_d)
    if end < len(open_d):
        return None
    return end


def label_math(fragment: str, cid: str) -> list[tuple[str, str, str, str]]:
    """Whole math component: structural math protected by construction;
    delimiter pairs NEUTRAL; fragments without a recognized outer structure
    are labelled by the frozen v2 residual spec (undelimited math residue is
    POLICY_EXPOSED: the frozen policy abstains from it)."""
    text = fragment
    for open_d, close_d in (("\\[", "\\]"), ("\\(", "\\)"), ("$$", "$$"), ("$", "$")):
        end = _delim_pair(text, open_d, close_d)
        if end is not None and text[end + len(close_d):].strip() == "":
            return [(open_d, cid, "NEUTRAL", CONSTRUCTION),
                    (text[len(open_d):end], cid, "PROTECTED", CONSTRUCTION),
                    (close_d, cid, "NEUTRAL", CONSTRUCTION)]
    m = re.match(r"^(\\begin\{[a-zA-Z*]+\})(.*?)(\\end\{[a-zA-Z*]+\})\s*$", text, re.S)
    if m:
        return [(m.group(1), cid, "PROTECTED", CONSTRUCTION),
                (m.group(2), cid, "PROTECTED", CONSTRUCTION),
                (m.group(3), cid, "PROTECTED", CONSTRUCTION)]
    return generic_label(text, cid)


def label_structured(fragment: str, family: str, cid: str) -> list[tuple[str, str, str, str]]:
    if family == "structured-json":
        stripped = fragment.strip()
        if stripped.startswith(("{", "[")):
            try:
                json.loads(stripped)
                # whole-JSON protection is decided by the frozen residual spec
                # (the bare-json class is the label oracle's expectation):
                # ORACLE_REFINED
                return [(fragment, cid, "PROTECTED", ORACLE_REFINED)]
            except (ValueError, json.JSONDecodeError):
                pass
        return generic_label(fragment, cid)
    if family in ("structured-html", "structured-xml"):
        lines = fragment.split("\n")
        first_tag = RE_HTML_TAG.match(lines[0]) if lines else None
        block_mode = (family == "structured-html" and first_tag is not None
                      and "\n\n" not in fragment)
        if block_mode:
            # an HTML block is structural by the dialect (HtmlBlock event,
            # never candidate prose): CONSTRUCTION
            return [(fragment, cid, "PROTECTED", CONSTRUCTION)]
        resid_marks = _covered_map(fragment, residual_spans(fragment))
        # tags are structural (Html/InlineHtml events, never Text): CONSTRUCTION
        tag_marks = ["."] * len(fragment)
        for m in RE_HTML_TAG.finditer(fragment):
            for i in range(m.start(), m.end()):
                tag_marks[i] = "P"
        segments: list[tuple[str, str, str, str]] = []
        i = 0
        n = len(fragment)
        while i < n:
            if resid_marks[i] == "P" or tag_marks[i] == "P":
                j = i
                while j < n and (resid_marks[j] == "P" or tag_marks[j] == "P"):
                    j += 1
                # split the run by source: tag-marked bytes are structural
                # (CONSTRUCTION); bytes marked only by the residual spec are
                # ORACLE_REFINED
                k = i
                while k < j:
                    m2 = k
                    tag_at = tag_marks[k] == "P"
                    while m2 < j and (tag_marks[m2] == "P") == tag_at:
                        m2 += 1
                    segments.append((fragment[k:m2], cid, "PROTECTED",
                                     CONSTRUCTION if tag_at else ORACLE_REFINED))
                    k = m2
                i = j
                continue
            ch = fragment[i]
            wm = re.match(r"[^\W\d_]+", fragment[i:])
            if wm and wm.group(0):
                segments.append((fragment[i:i + wm.end()], cid, "PROSE", ORACLE_REFINED))
                i += wm.end()
                continue
            if ch.isspace():
                j = i
                while j < n and fragment[j].isspace() and resid_marks[j] == "." \
                        and tag_marks[j] == ".":
                    j += 1
                segments.append((fragment[i:j], cid, "NEUTRAL", ORACLE_REFINED))
                i = j
                continue
            segments.append((fragment[i:i + 1], cid, "NEUTRAL", ORACLE_REFINED))
            i += 1
        return segments
    return generic_label(fragment, cid)


def label_machine(fragment: str, cid: str) -> list[tuple[str, str, str, str]]:
    return generic_label(fragment, cid)


MALFORMED_POLICY_EXPOSED_CHARS: dict[str, frozenset] = {
    "malformed-unmatched-backtick": frozenset("\u0060"),
    "malformed-unmatched-dollar": frozenset("$"),
    "malformed-incomplete-display-dollar": frozenset("$"),
    "malformed-malformed-nesting": frozenset("*_~"),
}


def label_malformed(fragment: str, family: str, cid: str) -> list[tuple[str, str, str, str]]:
    if family == "malformed-unclosed-fence":
        # the fence runs to end of document; the builder guarantees this
        # component is the LAST structural slot, so the document tail is
        # protected (structural: pulldown-cmark extends the fence to EOF)
        return [(fragment, cid, "PROTECTED", CONSTRUCTION)]
    return generic_label(fragment, cid, MALFORMED_POLICY_EXPOSED_CHARS.get(family, frozenset()))


def label_component(component: dict, inline: bool = False) -> list[tuple[str, str, str, str]]:
    cid = component["component_id"]
    fragment = component["fragment"]
    family = component["family"]
    category = component["category"]
    if category == "prose":
        return label_prose(fragment, cid)
    if category == "code":
        return label_code_block(fragment, cid, inline=inline)
    if category == "math":
        return label_math(fragment, cid)
    if category == "structured":
        return label_structured(fragment, family, cid)
    if category == "machine":
        return label_machine(fragment, cid)
    if category == "markdown":
        return label_markdown(fragment, family, cid)
    if category == "malformed":
        return label_malformed(fragment, family, cid)
    raise ValueError(f"unknown category {category}")


def _split_delims(fragment: str, cid: str, delims: list[str]) -> list[tuple[str, str, str, str]]:
    """Split text into (delimiter, text-alternating) runs: delims NEUTRAL,
    rest PROSE (structural by composition: CONSTRUCTION)."""
    pattern = re.compile("(" + "|".join(re.escape(d) for d in delims) + ")")
    parts = pattern.split(fragment)
    segments: list[tuple[str, str, str, str]] = []
    for idx, part in enumerate(parts):
        if not part:
            continue
        segments.append((part, cid, "NEUTRAL" if idx % 2 == 1 else "PROSE", CONSTRUCTION))
    return segments


_MD_TABLE_SEP = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")


def _label_plain_text(text: str, cid: str) -> list[tuple[str, str, str, str]]:
    """Label non-structured fragment text: ATX heading markers NEUTRAL,
    line breaks NEUTRAL, everything else PROSE (the parser treats all of
    it as candidate prose except the markers). Structural: CONSTRUCTION."""
    segments: list[tuple[str, str, str, str]] = []
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if idx > 0:
            segments.append(("\n", cid, "NEUTRAL", CONSTRUCTION))
        m = re.match(r"^\s{0,3}#{1,6}\s", line)
        if m:
            segments.append((line[:m.end()], cid, "NEUTRAL", CONSTRUCTION))
            if m.end() < len(line):
                segments.append((line[m.end():], cid, "PROSE", CONSTRUCTION))
        elif line:
            segments.append((line, cid, "PROSE", CONSTRUCTION))
    return segments


def label_markdown(fragment: str, family: str, cid: str) -> list[tuple[str, str, str, str]]:
    if family == "md-headings":
        delims = [re.match(r"^\s{0,3}#{1,6}\s*", line).group(0)
                  for line in fragment.splitlines()
                  if re.match(r"^\s{0,3}#{1,6}\s*", line)]
        return _split_delims(fragment, cid, delims)
    if family in ("md-emphasis", "md-strong", "md-strikethrough"):
        return _split_delims(fragment, cid, ["**", "__", "~~", "*", "_"])
    if family == "md-lists":
        delims = [re.match(r"^\s*(?:[-*+]|\d+[.)])\s*(?:\[[ xX]\]\s*)?", line).group(0)
                  for line in fragment.splitlines()
                  if re.match(r"^\s*(?:[-*+]|\d+[.)])\s", line)]
        return _split_delims(fragment, cid, delims)
    if family == "md-blockquotes":
        return _split_delims(fragment, cid, [">"])
    if family == "md-tables":
        segments: list[tuple[str, str, str]] = []
        lines = fragment.split("\n")
        for idx, line in enumerate(lines):
            if idx > 0:
                segments.append(("\n", cid, "NEUTRAL", CONSTRUCTION))
            if _MD_TABLE_SEP.match(line):
                segments.append((line, cid, "NEUTRAL", CONSTRUCTION))
            else:
                segments.extend(_split_delims(line, cid, ["|"]))
        return segments
    if family == "md-links":
        segments: list[tuple[str, str, str]] = []
        rest = fragment
        while True:
            match = re.search(r"(!?)\[([^\]\n]*)\]\(([^)\n]*)\)", rest)
            if not match:
                segments.extend(_split_delims(rest, cid, ["[", "]"]))
                break
            prefix = rest[:match.start()]
            if prefix:
                segments.extend(_split_delims(prefix, cid, ["[", "]"]))
            segments.append((match.group(1) + "[", cid, "NEUTRAL", CONSTRUCTION))
            segments.append((match.group(2), cid, "PROSE", CONSTRUCTION))
            segments.append(("](", cid, "NEUTRAL", CONSTRUCTION))
            segments.append((match.group(3), cid, "PROTECTED", CONSTRUCTION))
            segments.append((")", cid, "NEUTRAL", CONSTRUCTION))
            rest = rest[match.end():]
        return segments
    if family == "md-autolinks":
        # parser-dialect exact (pinned pulldown-cmark 0.13.4): URI
        # autolinks need an ASCII scheme; email autolinks are ASCII only
        # (a non-ASCII local part such as po\\u0161ta@ is NOT an autolink
        # and stays literal prose)
        segments: list[tuple[str, str, str]] = []
        rest = fragment
        while rest:
            match = re.search(r"<[A-Za-z][A-Za-z0-9+.-]*:[^>\s]+>|<[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+>", rest)
            if not match:
                segments.append((rest, cid, "PROSE", CONSTRUCTION))
                break
            prefix = rest[:match.start()]
            if prefix:
                segments.append((prefix, cid, "PROSE", CONSTRUCTION))
            inner = match.group(0)[1:-1]
            segments.append(("<", cid, "NEUTRAL", CONSTRUCTION))
            segments.append((inner, cid, "PROTECTED", CONSTRUCTION))
            segments.append((">", cid, "NEUTRAL", CONSTRUCTION))
            rest = rest[match.end():]
        return segments
    if family == "md-images":
        # policy PD-2: the image span itself (including alt text) is
        # PROTECTED; generated fragments may carry extra lines (headings,
        # prose), which the parser sees as candidate prose - label them by
        # content, mirroring the runtime's structural view
        segments: list[tuple[str, str, str]] = []
        rest = fragment
        while True:
            match = re.search(r"!\[[^\]\n]*\]\([^)\n]*\)", rest)
            if not match:
                segments.extend(_label_plain_text(rest, cid))
                break
            prefix = rest[:match.start()]
            if prefix:
                segments.extend(_label_plain_text(prefix, cid))
            segments.append((match.group(0), cid, "PROTECTED", CONSTRUCTION))
            rest = rest[match.end():]
        return segments
    if family == "md-inline-code":
        segments: list[tuple[str, str, str]] = []
        rest = fragment
        while rest:
            match = re.search(r"``[^`\n]*``|`[^`\n]+`", rest)
            if not match:
                segments.append((rest, cid, "PROSE", CONSTRUCTION))
                break
            prefix = rest[:match.start()]
            if prefix:
                segments.append((prefix, cid, "PROSE", CONSTRUCTION))
            if match.group(0).startswith("``"):
                body, delim = match.group(0)[2:-2], "``"
            else:
                body, delim = match.group(0)[1:-1], "`"

            segments.append((delim, cid, "NEUTRAL", CONSTRUCTION))
            segments.append((body, cid, "PROTECTED", CONSTRUCTION))
            segments.append((delim, cid, "NEUTRAL", CONSTRUCTION))
            rest = rest[match.end():]
        return segments
    if family == "md-fenced-code":
        lines = fragment.split("\n")
        segments: list[tuple[str, str, str]] = []
        in_fence = False
        fence = ""
        for line in lines:
            if not in_fence:
                match = re.match(r"^(\s{0,3})(```+|~~~+)(.*)$", line)
                if match:
                    segments.append((match.group(1) + match.group(2) + match.group(3), cid, "NEUTRAL", CONSTRUCTION))
                    segments.append(("\n", cid, "NEUTRAL", CONSTRUCTION))
                    in_fence = True
                    fence = match.group(2)[0] * 3
                else:
                    segments.append((line + "\n", cid, "PROSE", CONSTRUCTION))
            else:
                if line.strip().startswith(fence):
                    segments.append((line + "\n", cid, "NEUTRAL", CONSTRUCTION))
                    in_fence = False
                else:
                    segments.append((line + "\n", cid, "PROTECTED", CONSTRUCTION))
        return segments
    if family == "md-raw-html":
        segments: list[tuple[str, str, str]] = []
        rest = fragment
        while rest:
            match = re.search(r"</?[A-Za-z][^>]*>", rest)
            if not match:
                segments.append((rest, cid, "PROSE", CONSTRUCTION))
                break
            prefix = rest[:match.start()]
            if prefix:
                segments.append((prefix, cid, "PROSE", CONSTRUCTION))
            segments.append((match.group(0), cid, "PROTECTED", CONSTRUCTION))
            rest = rest[match.end():]
        return segments
    return [(fragment, cid, "PROSE")]


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------
def pick(rng: random.Random, pool: dict[str, list[dict]], family: str, exclude: set[str]) -> dict | None:
    options = [c for c in pool.get(family, []) if c["component_id"] not in exclude]
    return rng.choice(options) if options else None


def pick_any(rng: random.Random, pool: dict[str, list[dict]], categories: tuple[str, ...], exclude: set[str]) -> dict | None:
    options = [c for fam in pool for c in pool[fam] if c["category"] in categories and c["component_id"] not in exclude]
    return rng.choice(options) if options else None


def pick_inline_code(rng: random.Random, pool: dict[str, list[dict]], used: set[str],
                     family: str | None = None) -> dict | None:
    """A code component usable as an inline code span: the one-line body is
    non-empty and free of backticks (an inline code span cannot contain a
    backtick; a body containing one terminates the span and turns the rest
    of the fragment into exposed prose, which contradicts the
    machine-known whole-body protection label)."""
    def ok(c: dict) -> bool:
        body = one_line(c["fragment"], 60)
        return bool(body) and "\u0060" not in body and "`" not in body
    if family is not None:
        options = [c for c in pool.get(family, [])
                   if c["component_id"] not in used and ok(c)]
    else:
        options = [c for fam in pool for c in pool[fam]
                   if c["category"] == "code" and c["component_id"] not in used and ok(c)]
    return rng.choice(options) if options else None


TEMPLATES = (
    "T1-prose-inlinecode-prose",
    "T2-prose-math-prose",
    "T3-prose-fenced-prose",
    "T4-heading-prose-table",
    "T5-lists",
    "T6-prose-link-prose",
    "T7-prose-json-prose-latex",
    "T8-quote-fenced",
    "T9-prose-malformed-prose",
    "T10-randomized",
    "T11-interactions",
)

T4_TABLE_HEADER = "| Opis | Vzor\u010dek |\n"
T11_TEX_COMMENT = "# komentar z " + chr(92) + "frac{a}{b}"

# TeX malformed families whose expected protection depends on the length of
# the composed prose context (frozen policy v2: unpaired \\(/\\[ and
# unbalanced begin protect the math-like remainder only up to the class bound,
# measured to the end of the candidate-prose context). The builder derives
# labels from composition provenance only (no structure re-parsing), so these
# families are composed as standalone paragraphs (context = exactly the
# fragment line, remainder within the bound by construction) in T9 and are
# excluded from the randomized T10 mid-document pool; the mid-paragraph
# runaway-remainder form is exercised by the 008-d hidden acceptance with
# independently derived labels (documented in REPORT-008C.md).
RUNAWAY_TEX_FAMILIES = frozenset(
    ("malformed-incomplete-paren-bracket", "malformed-unclosed-tex-env"))
T4_TABLE_SEP = "| --- | --- |\n"


def compose(rng: random.Random, pool: dict[str, list[dict]], template: str,
            used: set[str],
            family_map: dict[str, str] | None = None) -> tuple[list[tuple[str, str, str, str]], int]:
    """Return (segment list (text, component_id, role, label_source), R1
    blank-line insertion count). Raises LookupError on pool exhaustion for
    the required categories of this template. The 008-i display-dollar
    guard and the fail-closed composition invariants run on every
    composition; ``family_map`` (component_id -> family) may be passed to
    avoid rebuilding it per call (build_set does)."""
    segs: list[tuple[str, str, str, str]] = []

    if template == "T1-prose-inlinecode-prose":
        p1 = pick(rng, pool, "prose-science", used) or pick_any(rng, pool, ("prose",), used)
        code = pick_inline_code(rng, pool, used, "code-python") or pick_inline_code(rng, pool, used)
        p2 = pick(rng, pool, "prose-history", used) or pick_any(rng, pool, ("prose",), used)
        for c in (p1, code, p2):
            if c is None:
                raise LookupError("pool exhausted")
            used.add(c["component_id"])
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_code_block(code["fragment"], code["component_id"], inline=True))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
    elif template == "T2-prose-math-prose":
        p1 = pick_any(rng, pool, ("prose",), used)
        math = pick_any(rng, pool, ("math",), used)
        p2 = pick_any(rng, pool, ("prose",), used)
        if not all((p1, math, p2)):
            raise LookupError("pool exhausted")
        for c in (p1, math, p2):
            used.add(c["component_id"])
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_math(math["fragment"], math["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
    elif template == "T3-prose-fenced-prose":
        p1 = pick_any(rng, pool, ("prose",), used)
        code = pick_any(rng, pool, ("code",), used)
        p2 = pick_any(rng, pool, ("prose",), used)
        if not all((p1, code, p2)):
            raise LookupError("pool exhausted")
        for c in (p1, code, p2):
            used.add(c["component_id"])
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_code_block(code["fragment"], code["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
    elif template == "T4-heading-prose-table":
        heading = pick_any(rng, pool, ("prose",), used)
        p1 = pick_any(rng, pool, ("prose",), used)
        cell = pick_any(rng, pool, ("prose",), used)
        machine = pick_any(rng, pool, ("machine",), used)
        if not all((heading, p1, cell, machine)):
            raise LookupError("pool exhausted")
        for c in (heading, p1, cell, machine):
            used.add(c["component_id"])
        title = one_line(heading["fragment"], 60)
        segs.append(("## ", "template", "NEUTRAL", CONSTRUCTION))
        segs.append((title, heading["component_id"], "PROSE", CONSTRUCTION))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.append((T4_TABLE_HEADER, "template", "NEUTRAL", CONSTRUCTION))
        segs.append((T4_TABLE_SEP, "template", "NEUTRAL", CONSTRUCTION))
        segs.append(("| ", "template", "NEUTRAL", CONSTRUCTION))
        segs.append((one_line(cell["fragment"], 40), cell["component_id"], "PROSE", CONSTRUCTION))
        segs.append((" | ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_machine(one_line(machine["fragment"], 40), machine["component_id"]))
        segs.append((" |", "template", "NEUTRAL", CONSTRUCTION))
    elif template == "T5-lists":
        p1 = pick_any(rng, pool, ("prose",), used)
        code = pick_inline_code(rng, pool, used)
        p2 = pick_any(rng, pool, ("prose",), used)
        p3 = pick_any(rng, pool, ("prose",), used)
        if not all((p1, code, p2, p3)):
            raise LookupError("pool exhausted")
        for c in (p1, code, p2, p3):
            used.add(c["component_id"])
        segs.append(("- ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n- ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_code_block(code["fragment"], code["component_id"], inline=True))
        segs.append(("\n- ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
        segs.append(("\n- ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p3["fragment"], p3["component_id"]))
    elif template == "T6-prose-link-prose":
        p1 = pick_any(rng, pool, ("prose",), used)
        # 008-i scope item 3(c) T6 ADMISSION REFINEMENT: the link
        # destination must be a clean URL (the v3 prescan invariant, now
        # builder-asserted); machine-urls first, then any other clean-URL
        # machine fragment. Non-clean fragments are never composed as T6
        # destinations (the whole-region PROTECTED vs inter-token-space
        # shape, REPORT-008H.md section 6 observation O1).
        url_opts = [c for c in pool.get("machine-urls", [])
                    if c["component_id"] not in used
                    and t6_link_destination_clean(c["fragment"])]
        if not url_opts:
            url_opts = [c for fam in pool for c in pool[fam]
                        if c["category"] == "machine"
                        and fam != "machine-urls"
                        and c["component_id"] not in used
                        and t6_link_destination_clean(c["fragment"])]
        p2 = pick_any(rng, pool, ("prose",), used)
        if not url_opts or not all((p1, p2)):
            raise LookupError("pool exhausted")
        urlc = rng.choice(url_opts)
        for c in (p1, urlc, p2):
            used.add(c["component_id"])
        url = urlc["fragment"].strip()
        if not t6_link_destination_clean(urlc["fragment"]):
            raise AssertionError(
                "T6 admission violated: non-clean link destination "
                "(builder-asserted, order 008-i scope item 3c)")
        label = one_line(p2["fragment"], 30)
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append((" ", "template", "NEUTRAL", CONSTRUCTION))
        segs.append(("[", "template", "NEUTRAL", CONSTRUCTION))
        segs.append((label, p2["component_id"], "PROSE", CONSTRUCTION))
        segs.append(("](", "template", "NEUTRAL", CONSTRUCTION))
        segs.append((url, urlc["component_id"], "PROTECTED", CONSTRUCTION))
        segs.append((")", "template", "NEUTRAL", CONSTRUCTION))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
    elif template == "T7-prose-json-prose-latex":
        p1 = pick_any(rng, pool, ("prose",), used)
        js = pick(rng, pool, "structured-json", used) or pick_any(rng, pool, ("structured",), used)
        p2 = pick_any(rng, pool, ("prose",), used)
        math = pick_any(rng, pool, ("math",), used)
        if not all((p1, js, p2, math)):
            raise LookupError("pool exhausted")
        for c in (p1, js, p2, math):
            used.add(c["component_id"])
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_structured(js["fragment"], js["family"], js["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_math(math["fragment"], math["component_id"]))
    elif template == "T8-quote-fenced":
        p1 = pick_any(rng, pool, ("prose",), used)
        code = pick_inline_code(rng, pool, used)
        p2 = pick_any(rng, pool, ("code",), used)
        if not all((p1, code, p2)):
            raise LookupError("pool exhausted")
        for c in (p1, code, p2):
            used.add(c["component_id"])
        segs.append(("> ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append((" ", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_code_block(code["fragment"], code["component_id"], inline=True))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_code_block(p2["fragment"], p2["component_id"]))
    elif template == "T9-prose-malformed-prose":
        p1 = pick_any(rng, pool, ("prose",), used)
        bad = pick_any(rng, pool, ("malformed",), used)
        p2 = pick_any(rng, pool, ("prose",), used)
        if not all((p1, bad, p2)):
            raise LookupError("pool exhausted")
        for c in (p1, bad, p2):
            used.add(c["component_id"])
        # an unclosed fence must be the LAST structural slot of the
        # document (the fence extends to end-of-input); the same holds for
        # an unmatched backtick: left before later backticks in the
        # paragraph it opens a code span that swallows their delimiters
        # and exposes their bodies
        if bad["family"] in ("malformed-unclosed-fence",
                             "malformed-unmatched-backtick"):
            segs.extend(label_prose(p1["fragment"], p1["component_id"]))
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_prose(p2["fragment"], p2["component_id"]))
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_malformed(bad["fragment"], bad["family"], bad["component_id"]))
        elif bad["family"] in RUNAWAY_TEX_FAMILIES:
            # standalone paragraph: the candidate-prose context is exactly
            # the fragment line, so the frozen-policy tex remainder bound is
            # met by construction (machine-known ground truth, no structure
            # re-parsing)
            segs.extend(label_prose(p1["fragment"], p1["component_id"]))
            segs.append(("\n\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_malformed(bad["fragment"], bad["family"], bad["component_id"]))
            segs.append(("\n\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_prose(p2["fragment"], p2["component_id"]))
        else:
            segs.extend(label_prose(p1["fragment"], p1["component_id"]))
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_malformed(bad["fragment"], bad["family"], bad["component_id"]))
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_prose(p2["fragment"], p2["component_id"]))
    elif template == "T11-interactions":
        # deterministic multi-layer interaction template (order scope
        # item 12 guarantees; see the 008-c census finding):
        #  (a) the PROTECTED inline-code body starts the document
        #      (protected-at-start),
        #  (b) sentence punctuation immediately follows the full
        #      inline-code span (inline-code-adjacent-punctuation),
        #  (c) the fenced code block carries a template-owned TeX
        #      comment line inside the fence (tex-in-code).
        all_code = [c for fam in pool for c in pool[fam]
                    if c["category"] == "code"
                    and c["component_id"] not in used]
        inline_ok = [c for c in all_code
                     if one_line(c["fragment"], 60)
                     and "\u0060" not in one_line(c["fragment"], 60)]
        fence_ok = [c for c in all_code
                    if c["fragment"].rstrip("\n")
                    and not any(ln.strip()[:3] in ("```", "~~~")
                                for ln in c["fragment"].splitlines())]
        if not inline_ok:
            raise LookupError("pool exhausted")
        code1 = rng.choice(inline_ok)
        used.add(code1["component_id"])
        fence_opts = [c for c in fence_ok
                      if c["component_id"] != code1["component_id"]]
        if not fence_opts:
            raise LookupError("pool exhausted")
        code2 = rng.choice(fence_opts)
        used.add(code2["component_id"])
        p1 = pick_any(rng, pool, ("prose",), used)
        p2 = pick_any(rng, pool, ("prose",), used)
        if p1 is None or p2 is None:
            raise LookupError("pool exhausted")
        used.add(p1["component_id"])
        used.add(p2["component_id"])
        body1 = one_line(code1["fragment"], 60)
        segs.append(("\u0060", code1["component_id"], "NEUTRAL", CONSTRUCTION))
        segs.append((body1, code1["component_id"], "PROTECTED", CONSTRUCTION))
        segs.append(("\u0060", code1["component_id"], "NEUTRAL", CONSTRUCTION))
        segs.append((".", "template", "PROSE", CONSTRUCTION))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        body2 = code2["fragment"].rstrip("\n") + "\n" + T11_TEX_COMMENT
        segs.append(("```", code2["component_id"], "NEUTRAL", CONSTRUCTION))
        segs.append(("\n", code2["component_id"], "NEUTRAL", CONSTRUCTION))
        segs.append((body2, code2["component_id"], "PROTECTED", CONSTRUCTION))
        segs.append(("\n", code2["component_id"], "NEUTRAL", CONSTRUCTION))
        segs.append(("```", code2["component_id"], "NEUTRAL", CONSTRUCTION))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p1["fragment"], p1["component_id"]))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(p2["fragment"], p2["component_id"]))
    else:  # T10-randomized
        n = rng.randint(3, 10)
        first = pick_any(rng, pool, ("prose",), used)
        last = pick_any(rng, pool, ("prose",), used)
        if first is None or last is None:
            raise LookupError("pool exhausted")
        for c in (first, last):
            used.add(c["component_id"])
        segs.extend(label_prose(first["fragment"], first["component_id"]))
        middle = []
        trailing = None
        running = len(first["fragment"].encode("utf-8")) + len(last["fragment"].encode("utf-8")) + 96
        for _ in range(n - 2):
            comp = pick_any(rng, pool, ("code", "structured", "math", "machine", "markdown", "malformed"), used)
            if comp is not None and comp["family"] in RUNAWAY_TEX_FAMILIES:
                # context-dependent expected protection: not composable with
                # machine-known labels mid-document (see RUNAWAY_TEX_FAMILIES)
                continue
            if comp is None:
                break
            if comp["family"] == "malformed-unmatched-backtick":
                # last-slot family: a dangling backtick left before later
                # backticks in the paragraph opens a code span that swallows
                # their delimiters and exposes their bodies
                if trailing is None:
                    trailing = comp
                used.add(comp["component_id"])
                continue
            est = len(comp["fragment"].encode("utf-8")) + 16
            if running + est > 3000:
                continue
            used.add(comp["component_id"])
            middle.append(comp)
            running += est
        # an unclosed fence must be the very last structural slot of the
        # document (the fence extends to end-of-input)
        unclosed = [c for c in middle if c["family"] == "malformed-unclosed-fence"]
        rest = [c for c in middle if c["family"] != "malformed-unclosed-fence"]
        for comp in rest:
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_component(comp))
        segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
        segs.extend(label_prose(last["fragment"], last["component_id"]))
        if trailing is not None:
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_malformed(trailing["fragment"], trailing["family"],
                                        trailing["component_id"]))
        for comp in unclosed:
            segs.append(("\n", "template", "NEUTRAL", CONSTRUCTION))
            segs.extend(label_malformed(comp["fragment"], comp["family"], comp["component_id"]))

    segs, r1_count = apply_r1(segs)
    fmap = family_map or {c["component_id"]: c["family"]
                          for fam in pool for c in pool[fam]}
    segs, dd_count = apply_display_dollar_guard(segs, fmap)
    assert dd_count == count_display_dollar_barrier_insertions(segs, fmap), \
        "display-dollar guard count mismatch (fail-closed)"
    assert_composition_invariants(segs, fmap)
    return segs, r1_count


DECOR_EMOJI = "\n\u2009\u017d\u010d: \U0001F680 hitrost rasti je merljiva."
DECOR_DECOMPOSED = "\n\u2009Pozor: e\u0301 (dekompouziran znakovni niz)."


def decorate(segs: list[tuple[str, str, str, str]], use_crlf: bool,
             add_emoji: bool, add_decomposed: bool) -> list[tuple[str, str, str, str]]:
    """Template-owned deterministic decorations (document index derived),
    applied in segment space so code-point spans stay exact."""
    if use_crlf:
        segs = [(t.replace("\n", "\r\n"), cid, role, lsrc) for t, cid, role, lsrc in segs]
    if add_emoji:
        segs = segs + [(DECOR_EMOJI, "template", "PROSE", CONSTRUCTION)]
    if add_decomposed:
        segs = segs + [(DECOR_DECOMPOSED, "template", "PROSE", CONSTRUCTION)]
    return segs


def assemble(segs: list[tuple[str, str, str, str]], pool_index: dict[str, dict], template: str) -> dict:
    """Build document text + region tiling from labeled segments (composition-only)."""
    regions: list[dict] = []
    comp_order: list[dict] = []
    seen: set[str] = set()
    position = 0
    cursor_cp = 0
    for text, cid, role, lsrc in segs:
        if not text:
            continue
        start = position
        end = position + len(text.encode("utf-8"))
        start_cp = cursor_cp
        end_cp = cursor_cp + len(text)
        position = end
        cursor_cp = end_cp
        category = None
        if not cid.startswith("template"):
            if cid not in seen:
                seen.add(cid)
                record = pool_index.get(cid, {})
                comp_order.append({"component_id": cid, "start_byte": None, "end_byte": None,
                                   "category": record.get("category")})
            category = pool_index.get(cid, {}).get("category")
        regions.append({"start_byte": start, "end_byte": end, "start_cp": start_cp, "end_cp": end_cp,
                        "component_id": cid, "category": category, "role": role,
                        "label_source": lsrc,
                        "template": cid.startswith("template")})
    texts = [text for text, _cid, _role, _lsrc in segs if text]
    full = "".join(texts)
    data = full.encode("utf-8")
    assert cursor_cp == len(full) and position == len(data), "region tiling is not exact"
    for comp in comp_order:
        spans = [(r["start_byte"], r["end_byte"]) for r in regions if r["component_id"] == comp["component_id"]]
        if spans:
            comp["start_byte"] = min(s for s, _ in spans)
            comp["end_byte"] = max(e for _, e in spans)
    return {"text": full, "data": data, "regions": regions, "components": comp_order, "template": template}


# --------------------------------------------------------------------------
# census pattern scanners (data-free)
# --------------------------------------------------------------------------
def region_text(doc: dict, region: dict) -> str:
    return doc["document"][region["start_cp"]:region["end_cp"]]


def _protected_of(label, category):
    return [r for r in label["regions"] if r["role"] == "PROTECTED" and (category is None or r["category"] == category)]


def build_pattern_scanners() -> dict[str, object]:
    def markdown_in_code(d, l):
        return any(re.search(r"[*_#`\[\]]", region_text(d, r)) for r in _protected_of(l, "code"))

    def tex_in_code(d, l):
        return any(re.search(r"\\(frac|text|begin|sum|alpha|beta|left|right)|\\\\", region_text(d, r))
                   for r in _protected_of(l, "code"))

    def backtick_in_string(d, l):
        return any("`" in region_text(d, r) for r in _protected_of(l, "code"))

    def currency_next_to_math(d, l):
        for r in _protected_of(l, "math"):
            lo = max(0, r["start_cp"] - 200)
            hi = min(len(d["document"]), r["end_cp"] + 200)
            if re.search(r"\$\s?[0-9]|[0-9]\s?\u20ac", d["document"][lo:hi]):
                return True
        return False

    def slovenian_comment_in_code(d, l):
        return any(re.search(r"(#|//|/\*).{0,40}[\u010d\u0161\u017e]", region_text(d, r))
                   for r in _protected_of(l, "code"))

    def slovenian_string_in_json(d, l):
        return any(re.search(r"[\u010d\u0161\u017e]", region_text(d, r)) for r in _protected_of(l, "structured"))

    def markdown_in_json_strings(d, l):
        return any(re.search(r"[*_]{1,2}\S[^*\n]{0,80}[*_]{1,2}", region_text(d, r))
                   for r in _protected_of(l, "structured"))

    def tex_text_slovenian(d, l):
        return any(re.search(r"\\text\{[^}]*[\u010d\u0161\u017e]", region_text(d, r))
                   for r in _protected_of(l, "math"))

    def url_in_code(d, l):
        return any("http" in region_text(d, r) for r in _protected_of(l, "code"))

    def path_in_table(d, l):
        has_pipe = any(r["role"] == "NEUTRAL" and r["template_owned"] and r["start_cp"] < len(d["document"])
                       and d["document"][r["start_cp"]] == "|" for r in l["regions"])
        if not has_pipe:
            return False
        rows = [r for r in l["regions"] if r["role"] == "PROSE" or r["role"] == "PROTECTED"]
        return any(re.search(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", region_text(d, r)) for r in rows)

    def code_in_lists(d, l):
        for r in _protected_of(l, "code"):
            window = d["document"][max(0, r["start_cp"] - 12):r["start_cp"]]
            if re.search(r"(^|\n)\s*(?:[-*+]|\d+[.)])\s", window):
                return True
        return False

    def link_in_blockquote(d, l):
        if d["document"].count(">") <= 0:
            return False
        return any("](" in region_text(d, r) for r in l["regions"]) or any("](" in d["document"][max(0, r["start_cp"] - 6):r["end_cp"]] for r in l["regions"])

    def inline_code_adjacent_punctuation(d, l):
        # the inline-code span includes its delimiter backticks (the
        # backtick regions carry the code component ID); punctuation
        # adjacent to the full span extent is the tested interaction
        text = d["document"]
        by_comp: dict[str, list[dict]] = {}
        for r in l["regions"]:
            if r["category"] == "code":
                by_comp.setdefault(r["component_id"], []).append(r)
        for regs in by_comp.values():
            if not any(r["role"] == "PROTECTED" for r in regs):
                continue
            s = min(r["start_cp"] for r in regs)
            e = max(r["end_cp"] for r in regs)
            if e - s > 80:
                continue
            if s >= len(text) or text[s] != "\u0060":
                continue
            if s + 1 < e and text[s + 1] == "\u0060":
                continue  # fenced / multi-backtick opener, not inline
            before = text[s - 1] if s > 0 else ""
            after = text[e] if e < len(text) else ""
            if before in ".,:;()" or after in ".,:;()":
                return True
        return False

    def emoji_and_diacritics(d, l):
        return bool(re.search(r"[\U0001F300-\U0001FAFF]", d["document"])) and bool(re.search(r"[\u010d\u0161\u017e]", d["document"]))

    def decomposed_unicode(d, l):
        return bool(re.search(r"[\u0300-\u036f]", d["document"]))

    def crlf(d, l):
        return "\r\n" in d["document"]

    def adjacent_protected_regions(d, l):
        protected = sorted((r["start_byte"], r["end_byte"]) for r in l["regions"] if r["role"] == "PROTECTED")
        return any(s2 - e1 <= 8 for (s1, e1), (s2, e2) in zip(protected, protected[1:]))

    def protected_at_start(d, l):
        return any(r["role"] == "PROTECTED" and r["start_byte"] < 4 for r in l["regions"])

    def protected_at_end(d, l):
        return any(r["role"] == "PROTECTED" and r["end_byte"] == d["byte_length"] for r in l["regions"])

    return {
        "markdown-in-code": markdown_in_code,
        "tex-in-code": tex_in_code,
        "backtick-in-string": backtick_in_string,
        "currency-next-to-math": currency_next_to_math,
        "slovenian-comment-in-code": slovenian_comment_in_code,
        "slovenian-string-in-json": slovenian_string_in_json,
        "markdown-in-json-strings": markdown_in_json_strings,
        "tex-text-slovenian": tex_text_slovenian,
        "url-in-code": url_in_code,
        "path-in-table": path_in_table,
        "code-in-lists": code_in_lists,
        "link-in-blockquote": link_in_blockquote,
        "inline-code-adjacent-punctuation": inline_code_adjacent_punctuation,
        "emoji-and-diacritics": emoji_and_diacritics,
        "decomposed-unicode": decomposed_unicode,
        "crlf": crlf,
        "adjacent-protected-regions": adjacent_protected_regions,
        "protected-at-start": protected_at_start,
        "protected-at-end": protected_at_end,
    }


def finalize_document(doc: dict, doc_id: str, seed_hex: str, template: str,
                      r1_count: int = 0, dd_count: int = 0) -> tuple[dict, dict]:
    """Emit the document + label records. Label invariants are asserted (fail
    closed). Decorations are already applied in segment space upstream.
    ``r1_count`` and ``dd_count`` are recorded in the document's
    composition provenance (the 5-argument call form stays valid for the
    byte-frozen 008-h tests)."""
    text = doc["text"]
    data = text.encode("utf-8")
    position = 0
    for region in doc["regions"]:
        segbytes = len(text[region["start_cp"]:region["end_cp"]].encode("utf-8"))
        region["start_byte"] = position
        region["end_byte"] = position + segbytes
        position += segbytes
    assert position == len(data), f"{doc_id}: region bytes do not tile the document"
    for comp in doc["components"]:
        spans = [(r["start_byte"], r["end_byte"]) for r in doc["regions"] if r["component_id"] == comp["component_id"]]
        if spans:
            comp["start_byte"] = min(s for s, _ in spans)
            comp["end_byte"] = max(e for _, e in spans)
    document = {
        "doc_id": doc_id,
        "seed": seed_hex,
        "template": template,
        "byte_length": len(data),
        "cp_length": len(text),
        "sha256": sha256_bytes(data),
        "document": text,
        "components": [{"component_id": c["component_id"], "category": c["category"],
                        "start_byte": c["start_byte"], "end_byte": c["end_byte"]}
                       for c in doc["components"]],
        "composition_provenance": {
            "r1_blank_line_insertions": r1_count,
            "r1_contract": "a fenced or indented code component is never composed on the line immediately after an HTML block-start line (pulldown-cmark 0.13.4 HTML block types 1-7; order 008-h scope item 3b R1, extended per order 008-i scope item 3a; the 008-h test-pinned corner - a bare single complete opening tag at EOL - stays unbarred by the preserved 008-h contract, disclosed in REPORT-008I.md boundary_fidelity); the inserted bytes are template-owned NEUTRAL delimiter",
            "display_dollar_barrier_insertions": dd_count,
            "display_dollar_guard_contract": "a malformed-incomplete-display-dollar component (unterminated $$ opener) is never composed immediately before a component whose first line opens a display-dollar expression; the inserted bytes are one NEUTRAL-labeled blank line (template-owned delimiter; order 008-i scope item 3b)",
            "t6_link_destination_admission": "T6-prose-link-prose link destinations are clean URLs (https?:// with no whitespace or angle brackets), builder-asserted at composition (order 008-i scope item 3c)",
        },
    }
    label = {
        "doc_id": doc_id,
        "byte_length": len(data),
        "cp_length": len(text),
        "regions": [{"start_byte": r["start_byte"], "end_byte": r["end_byte"],
                     "start_cp": r["start_cp"], "end_cp": r["end_cp"],
                     "component_id": r["component_id"],
                     "category": r["category"],
                     "role": r["role"],
                     "label_source": r["label_source"],
                     "template_owned": r["template"]} for r in doc["regions"]],
        "invariants": {
            "tiling_complete": all(
                r["start_byte"] == (doc["regions"][i - 1]["end_byte"] if i > 0 else 0)
                for i, r in enumerate(doc["regions"])),
            "no_contradictory_overlaps": True,
            "cp_range_exact": all(
                text[r["start_cp"]:r["end_cp"]].encode("utf-8") == data[r["start_byte"]:r["end_byte"]]
                for r in doc["regions"]),
        },
    }
    assert label["invariants"]["tiling_complete"] and label["invariants"]["cp_range_exact"], doc_id
    return document, label


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def build_set(pool: dict[str, list[dict]], pool_index: dict[str, dict], seed_hex: str,
              count: int, prefix: str) -> list[tuple[dict, dict]]:
    """Compose ``count`` documents deterministically from the pool.

    Component exclusion is per-document (pools are intentionally reused
    across documents). Template cycle is deterministic per document index;
    an over-size composition is retried with the next templates in the cycle
    (one full cycle, bounded); an under-size composition is extended with one
    more prose paragraph. A document that no candidate brings into
    [200, 4000] bytes keeps its last candidate and its actual size is
    recorded in the census (never fabricated).
    """
    assert_no_parser_participation()
    rng = make_rng(seed_hex)
    family_map = {c["component_id"]: c["family"]
                  for fam in pool.values() for c in fam}
    docs: list[tuple[dict, dict]] = []
    for i in range(count):
        use_crlf = (i % 25 == 7)
        add_emoji = (i % 41 == 3)
        add_decomposed = (i % 41 == 11)
        candidate: tuple[dict, str, int, int] | None = None
        for attempt in range(len(TEMPLATES)):
            template = TEMPLATES[(i + attempt) % len(TEMPLATES)]
            used: set[str] = set()
            try:
                segs, r1_count = compose(rng, pool, template, used, family_map)
            except LookupError:
                continue
            dd_count = count_display_dollar_barrier_insertions(segs, family_map)
            segs = decorate(segs, use_crlf, add_emoji, add_decomposed)
            doc = assemble(segs, pool_index, template)
            if len(doc["data"]) > DOC_BYTES_MAX:
                candidate = (doc, template, r1_count, dd_count)
                continue
            if len(doc["data"]) < DOC_BYTES_MIN:
                extra = pick_any(rng, pool, ("prose",), used)
                if extra is not None:
                    used.add(extra["component_id"])
                    segs.extend([("\n", "template", "NEUTRAL", CONSTRUCTION),
                                 (extra["fragment"], extra["component_id"], "PROSE", CONSTRUCTION)])
                    assert_composition_invariants(segs, family_map)
                    dd_count = count_display_dollar_barrier_insertions(segs, family_map)
                    doc = assemble(segs, pool_index, template)
            if DOC_BYTES_MIN <= len(doc["data"]) <= DOC_BYTES_MAX:
                candidate = (doc, template, r1_count, dd_count)
                break
            candidate = (doc, template, r1_count, dd_count)
        if candidate is None:
            raise RuntimeError(f"document {prefix}{i:06d}: no candidate composed (pool exhausted)")
        doc, template, r1_count, dd_count = candidate
        document, label = finalize_document(doc, f"{prefix}{i:06d}", seed_hex,
                                            template, r1_count, dd_count)
        docs.append((document, label))
    return docs


def write_set(docs: list[tuple[dict, dict]], doc_root: Path, label_root: Path) -> dict:
    doc_root.mkdir(parents=True, exist_ok=True)
    label_root.mkdir(parents=True, exist_ok=True)
    for document, label in docs:
        dp = doc_root / f"{document['doc_id']}.json"
        lp = label_root / f"{label['doc_id']}.json"
        dp.write_text(json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        lp.write_text(json.dumps(label, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {"documents": len(docs),
            "total_bytes": sum(d["byte_length"] for d, _ in docs),
            "min_bytes": min(d["byte_length"] for d, _ in docs),
            "max_bytes": max(d["byte_length"] for d, _ in docs)}


def census_for(docs: list[tuple[dict, dict]]) -> dict:
    scanners = build_pattern_scanners()
    pattern_counts: dict[str, int] = {name: 0 for name in scanners}
    category_bytes: dict[str, dict] = {}
    template_counts: dict[str, int] = {}
    role_bytes: dict[str, int] = {}
    for document, label in docs:
        template_counts[document["template"]] = template_counts.get(document["template"], 0) + 1
        for region in label["regions"]:
            cat = region["category"] or ("template" if region["template_owned"] else "neutral")
            entry = category_bytes.setdefault(cat, {"bytes": 0, "regions": 0})
            entry["bytes"] += region["end_byte"] - region["start_byte"]
            entry["regions"] += 1
            role_bytes[region["role"]] = role_bytes.get(region["role"], 0) + region["end_byte"] - region["start_byte"]
        for name, scanner in scanners.items():
            if scanner(document, label):
                pattern_counts[name] += 1
    return {"pattern_counts": pattern_counts, "category_bytes": category_bytes,
            "template_counts": template_counts, "role_bytes": role_bytes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    runtime_root = args.runtime_root.resolve()
    if not runtime_root.is_dir():
        raise SystemExit("runtime root missing")

    lib = json.loads((repo / "research/prose-boundary/config/generation/prompt-families.json").read_text(encoding="utf-8"))
    seeds = lib["batch_plan"]["mashup_seeds"]

    dev_root = repo / "research/prose-boundary/corpus"
    dev_comp = dev_root / "components-dev"
    hidden_root = runtime_root / "008c-hidden"
    hidden_comp = hidden_root / "components"
    if not any(dev_comp.glob("*/*.json")):
        raise SystemExit("dev component pool missing (run generation_driver first)")
    if not any(hidden_comp.glob("*/*.json")):
        raise SystemExit("hidden component pool missing (run generation_driver first)")

    dev_pool = load_pool(dev_comp)
    hidden_pool = load_pool(hidden_comp)
    dev_index = {c["component_id"]: c for fam in dev_pool.values() for c in fam}
    hidden_index = {c["component_id"]: c for fam in hidden_pool.values() for c in fam}

    # ---------------- dev set (committed)
    dev_docs = build_set(dev_pool, dev_index, seeds["dev"], DEV_DOCS, "dev-")
    scanners = build_pattern_scanners()
    # guarantee pattern minimums via deterministic re-roll of the tail documents
    tail = min(300, len(dev_docs))
    attempts = 0
    while attempts < REROLL_BUDGET:
        census = census_for(dev_docs)
        short = [name for name, cnt in census["pattern_counts"].items()
                 if name not in ("emoji-and-diacritics", "decomposed-unicode", "crlf") and cnt < PATTERN_MINIMUM]
        if not short:
            break
        attempts += 1
        idx = tail - 1 - (attempts % tail)
        document, _label = dev_docs[idx]
        template = TEMPLATES[(idx + attempts) % len(TEMPLATES)]
        used: set[str] = set()
        rng = make_rng(hashlib.sha256((seeds["dev"] + f"-reroll-{attempts}").encode("utf-8")).hexdigest()[:16])
        try:
            segs, r1_count = compose(rng, dev_pool, template, used)
        except LookupError:
            continue
        segs = decorate(segs, (idx % 25 == 7), (idx % 41 == 3), (idx % 41 == 11))
        doc = assemble(segs, dev_index, template)
        if not (DOC_BYTES_MIN <= len(doc["data"]) <= DOC_BYTES_MAX):
            continue
        new_document, new_label = finalize_document(doc, document["doc_id"], seeds["dev"], template, r1_count)
        if sum(1 for n in short if scanners[n](new_document, new_label)) > 0:
            dev_docs[idx] = (new_document, new_label)
    dev_census = census_for(dev_docs)

    docs_root = dev_root / "documents-dev"
    labels_root = dev_root / "labels-dev"
    dev_stats = write_set(dev_docs, docs_root, labels_root)

    # ---------------- hidden set (private root only)
    hidden_docs = build_set(hidden_pool, hidden_index, seeds["hidden"], HIDDEN_DOCS, "hid-")
    hidden_stats = write_set(hidden_docs, hidden_root / "documents", hidden_root / "labels")
    hidden_census = census_for(hidden_docs)

    # ---------------- census (committed, dev)
    manifests = dev_root / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    comp_files: dict[str, dict] = {}
    for path in sorted(dev_comp.glob("*/*.json")):
        rel = str(path.relative_to(dev_comp))
        data = path.read_bytes()
        comp_files[rel] = {"sha256": sha256_bytes(data), "size": len(data)}
    doc_files: dict[str, dict] = {}
    for path in sorted(docs_root.glob("*.json")):
        data = path.read_bytes()
        doc_files[path.name] = {"sha256": sha256_bytes(data), "size": len(data)}
    label_files: dict[str, dict] = {}
    for path in sorted(labels_root.glob("*.json")):
        data = path.read_bytes()
        label_files[path.name] = {"sha256": sha256_bytes(data), "size": len(data)}
    nat_files: dict[str, dict] = {}
    nat_root = dev_root / "naturalistic-dev"
    if any(nat_root.glob("*.json")):
        for path in sorted(nat_root.glob("*.json")):
            data = path.read_bytes()
            nat_files[path.name] = {"sha256": sha256_bytes(data), "size": len(data)}
    size_out_of_range = sum(
        1 for d, _ in dev_docs if not (DOC_BYTES_MIN <= d["byte_length"] <= DOC_BYTES_MAX))
    census = {
        "schema": "008c-corpus-census/1",
        "order": "008-c",
        "set": "dev (committed)",
        "components_by_file": comp_files,
        "components_by_category": {
            cat: sum(1 for c in dev_pool.values() for r in c if r["category"] == cat)
            for cat in ("prose", "code", "structured", "math", "markdown", "machine", "malformed")
        },
        "components_total": sum(len(v) for v in dev_pool.values()),
        "documents": {"count": dev_stats["documents"], "total_bytes": dev_stats["total_bytes"],
                      "min_bytes": dev_stats["min_bytes"], "max_bytes": dev_stats["max_bytes"],
                      "byte_range_target": [DOC_BYTES_MIN, DOC_BYTES_MAX],
                      "documents_outside_byte_range": size_out_of_range,
                      "template_counts": dev_census["template_counts"],
                      "files": doc_files,
                      "label_files": label_files},
        "category_region_bytes": dev_census["category_bytes"],
        "role_bytes": dev_census["role_bytes"],
        "interaction_pattern_counts": dev_census["pattern_counts"],
        "pattern_minimum": PATTERN_MINIMUM,
        "pattern_satisfaction": {
            name: ("met" if cnt >= PATTERN_MINIMUM else "below-minimum(recorded)")
            for name, cnt in dev_census["pattern_counts"].items()
        },
        "naturalistic_dev_files": nat_files,
        "seeds": {"dev_mashup": seeds["dev"], "hidden_mashup": seeds["hidden"]},
        "note": "dev corpus is structural test data (project-authored via the authorized generation program); passing it in 008-c is tuning evidence, not acceptance",
    }
    census_path = manifests / "corpus-census.json"
    census_path.write_text(json.dumps(census, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # ---------------- hidden manifest (committed, content-free) + seal
    hidden_files: dict[str, dict] = {}
    for sub in ("components", "documents", "labels", "naturalistic"):
        subroot = hidden_root / sub
        if not subroot.is_dir():
            continue
        for path in sorted(subroot.rglob("*.json")):
            rel = str(path.relative_to(hidden_root))
            data = path.read_bytes()
            hidden_files[rel] = {"sha256": sha256_bytes(data), "size": len(data)}
    gen_identity = json.loads((repo / "research/prose-boundary/config/generation/generation-identity.json").read_text(encoding="utf-8"))
    manifest = {
        "schema": "008c-hidden-manifest/1",
        "order": "008-c",
        "set": "hidden (private root only; content never committed)",
        "sealed_before": "implementation freeze (order requirement 11) and dev-corpus tuning (requirement 8)",
        "seeds": {"dev_mashup": seeds["dev"], "hidden_mashup": seeds["hidden"]},
        "generator_identity": {
            "model": gen_identity["generator"]["model"],
            "prompt_library_sha256": gen_identity["prompt_library_sha256"],
            "deployment_class": gen_identity["generator"]["deployment_class"],
        },
        "census": {
            "components_total": sum(len(v) for v in hidden_pool.values()),
            "documents": hidden_stats["documents"],
            "document_total_bytes": hidden_stats["total_bytes"],
            "document_min_bytes": hidden_stats["min_bytes"],
            "document_max_bytes": hidden_stats["max_bytes"],
            "template_counts": hidden_census["template_counts"],
            "interaction_pattern_counts": hidden_census["pattern_counts"],
            "role_bytes": hidden_census["role_bytes"],
        },
        "files": hidden_files,
        "no_content": True,
    }
    manifest_path = manifests / "hidden-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # private-root seal copy: byte-identical to the committed manifest
    # (order scope item 8: "The private-root seal copy is hash-identical to
    # the committed manifest"); verified against it in the seal record below
    seal_copy_path = hidden_root / "hidden-manifest-seal.json"
    seal_copy_path.write_bytes(manifest_path.read_bytes())

    # ---------------- seal verification (hash re-check against manifest)
    verified = 0
    mismatches = []
    for rel, entry in manifest["files"].items():
        path = hidden_root / rel
        if not path.is_file():
            mismatches.append({"path": rel, "error": "missing"})
            continue
        data = path.read_bytes()
        if sha256_bytes(data) != entry["sha256"] or len(data) != entry["size"]:
            mismatches.append({"path": rel, "error": "hash-or-size mismatch"})
            continue
        verified += 1
    seal = {
        "schema": "008c-seal-verification/1",
        "order": "008-c",
        "manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
        "seal_copy_sha256": sha256_bytes(seal_copy_path.read_bytes()),
        "seal_copy_hash_identical": (sha256_bytes(seal_copy_path.read_bytes())
                                     == sha256_bytes(manifest_path.read_bytes())),
        "files_verified": verified,
        "files_expected": len(manifest["files"]),
        "mismatches": mismatches,
        "status": "SEALED" if not mismatches else "SEAL_MISMATCH",
        "note": "private-root content hash-identical to the committed manifest at seal time; re-verified before the report-only commit (order requirement 5 / scope item 13)",
    }
    seal_path = manifests / "seal-verification.json"
    seal_path.write_text(json.dumps(seal, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(json.dumps({
        "dev_documents": len(dev_docs),
        "hidden_documents": len(hidden_docs),
        "dev_stats": dev_stats,
        "hidden_stats": hidden_stats,
        "dev_documents_outside_byte_range": size_out_of_range,
        "census_sha256": sha256_bytes(census_path.read_bytes()),
        "manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
        "seal_status": seal["status"],
        "seal_sha256": sha256_bytes(seal_path.read_bytes()),
        "pattern_counts_dev": dev_census["pattern_counts"],
    }))
    return 0 if seal["status"] == "SEALED" else 1


if __name__ == "__main__":
    sys.exit(main())

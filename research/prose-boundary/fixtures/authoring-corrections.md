# 008-a fixture suite — authoring-corrections audit log

Order 008-a requirement 3: the fixture suite and its expected structural safety
semantics are frozen (committed) **before** the parser is run on them; no
post-hoc parser-specific expectations without a recorded rationale.

## Integrity statement

The first draft of the suite existed only in the working tree and was never
committed. A validation parser run was performed on the uncommitted draft
during authoring; its output was used **only to detect authoring errors**
(byte/code-point arithmetic, anchor ambiguity, mistaken construct
interpretations) and to confirm the frozen policy notes already in
`config/experiment-008a.json` (Markdown syntax bytes and line endings are never
candidate prose). Every correction below was applied **before the first commit
of the suite**, and each is recorded here. The committed
`fixtures/fixtures.json` is therefore the frozen suite, and no correction was
made after its commit.

Direction of safety: no correction weakens any protection claim. Corrections
that add exposure (marked [+]) restore expectations the frozen policy already
mandates (prose leaves inside prose containers must be exposed); corrections
that add protection (marked [P]) only strengthen protection. No correction was
driven to make a failing assertion pass without the stated rationale.

Categories:
- **(A) arithmetic/anchor error** — the declared region did not match the
  author's intended source slice (multi-byte byte math or wrong override).
- **(B) token-level precision** — the declaration refined a whole-line/whole-
  construct span to token-level spans consistent with the frozen policy notes
  (escape-syntax bytes PROTECTED; line-ending/whitespace bytes NEUTRAL).
- **(C) construct interpretation** — the draft assumed a CommonMark
  interpretation the candidate (correctly, per CommonMark core) does not use.

## Corrections

### F14 (begintex-align) — (B)
- Original: one region `align-env` = `\begin{align}`..`\end{align}` declared
  PROSE_CANDIDATE (whole environment including newlines and both backslashes of
  the `\\` pair).
- Final: token-level regions: `begin-line`/`line-a`/`literal-backslash`/
  `line-c`/`end-line` PROSE_CANDIDATE; `escape-1` (the escape backslash byte of
  the `\\` pair) PROTECTED; `softbreak-1/2/3` and `gap-1/2` NEUTRAL.
- Rationale: the escape backslash is Markdown escape syntax (frozen policy
  note: syntax is never candidate prose); the escaped literal backslash is
  exposed text; soft-break newlines are line endings (frozen policy note).

### F15 (malformed-tex) — (B)
- Original: one region `prose` covering both paragraphs across the blank line.
- Final: `line-1` and `line-2` PROSE_CANDIDATE; `blank-line` NEUTRAL.
- Rationale: line-ending bytes are never prose; all text bytes remain asserted
  exposed.

### F17 (escaped-dollars) — (B)
- Original: one region `prose` covering the whole line.
- Final: `prose-1/2/3`, `dollar-1/2` PROSE_CANDIDATE; `escape-1/2/3/4`
  (each escape backslash byte) PROTECTED.
- Rationale: escape backslashes are Markdown escape syntax; the frozen note
  already said "backslashes are syntax and never candidate prose" — the
  declaration now matches the note byte-for-byte.

### F20 (list-item-prose) — (A)
- Original override: `bullet-2` = bytes 22..24 (`\n-`).
- Final: bytes 23..25 (`- `), matching the intent (the bullet marker) and the
  symmetric `bullet-1` = bytes 8..10.

### F21 (blockquote-prose) — (A)
- Original override: `quote-mark-2` = (34,36) — inside the quoted text.
- Final: (30,32) = `> ` (the second quote marker). The draft used wrong byte
  math; the intended slice was always the marker.

### F22 (link-prose-label-url) — (A)
- Original: `bracket-close-paren` start_cp=20 end_cp=22 and `paren-close`
  anchored over the whole destination.
- Final: `bracket-close-paren` = (24,26) (CP) = bytes 26..28 (`](`);
  `paren-close` = (52,53) (CP) = byte 54 (`)`). The draft ignored the two
  multi-byte characters (š, č) in "Obišči" (7 CP = 9 bytes).

### F25 (table-prose-and-code) — (C)
- Original: `cell-code-1/2` role PROSE_CANDIDATE under P0 (assumption: without
  the tables extension the backtick spans are literal text).
- Final: PROTECTED under every profile.
- Rationale: inline code spans are CommonMark **core** (parsed as `Code`
  events with or without the tables extension), so they are structurally
  recognized code and must stay protected in every frozen profile. The draft
  mis-assumed the dialect.

### F26 (raw-html) — (B) + evaluator fix
- Original: one region `inline-html` = `<b>`..`</b>` PROTECTED, which bundled
  the inner text `odebeljeno` into the protected span.
- Final: `html-open` (63..66) and `html-close` (76..80) PROTECTED;
  `html-text` (66..76) PROSE_CANDIDATE [+].
- Rationale: the frozen policy protects HTML tags, not the ordinary text
  between them (a prose leaf). The evaluator was also corrected to distinguish
  block `Html` from inline `InlineHtml` event kinds (adapter token change,
  identity SHA refreshed).

### F27 (bare-json) — (B)
- Original: one region `json` = `{`..`}` PROSE_CANDIDATE (assumed all bytes
  exposed).
- Final: per-token regions: `json-open`/`line-1`/`line-2`/`json-close`
  PROSE_CANDIDATE; `newline-1/2/3` and `indent-1/2` NEUTRAL.
- Rationale: whitespace bytes are never prose (frozen policy note on line
  endings; applied consistently to indentation).

### F28 (yaml-toml-config) — (B)
- Original: `toml` and `yamlish` regions spanning multiple lines.
- Final: per-line regions (`toml-line-1/2`, `yaml-line-1/2` PROSE_CANDIDATE;
  `newline-1/2`, `blank-1`, `indent-1` NEUTRAL).
- Rationale: same as F27.

### F29 (shell-commands) — (C) + (B)
- Original: one region `shell` = `$ ls`..`sudo apt update` PROSE_CANDIDATE.
- Final: `shell-line-1`/`shell-line-2` PROSE_CANDIDATE; `heading-marker`
  PROTECTED; `heading-text` PROSE_CANDIDATE [+]; `newline-1/2` NEUTRAL.
- Rationale (dialect finding): `# komentar` is parsed as an ATX heading
  (S.Head:1) by CommonMark core. The heading marker is syntax (protected);
  the heading text is a prose leaf the frozen policy mandates to be exposed.

### F37 (malformed-links) — (C)
- Original: one region `prose` over the whole line, with the note "malformed
  link constructs are not recognized links".
- Final: `prose-1`, `literal-link-1` (`[brez cilja]`), `prose-mid`,
  `link-label`, `prose-after` PROSE_CANDIDATE; `link-open`,
  `link-close-paren`, `link-dest`, `link-close` PROTECTED [P].
- Rationale (construct interpretation): `[slomljen( in ](osamljen)` **is** a
  well-formed CommonMark link — link labels may contain parentheses, and the
  destination is a relative URI. `[brez cilja]` (no destination/definition)
  correctly remains literal prose. The draft's premise about the first
  construct was wrong; the re-declaration follows the frozen policy (link
  label prose; link syntax and destination protected).

### F41 (yaml-front-matter) — (C)
- Original: `front-matter` = `title:`..`author: Ana` with P0/P1
  PROSE_CANDIDATE, P2 PROTECTED (assumed: `---` lines are thematic breaks and
  the lines are ordinary paragraph text).
- Final: `rule-1` (0..3) PROTECTED; `title-line` (4..21) and `author-line`
  (22..33) PROSE_CANDIDATE with P2 PROTECTED [+]; `setext-rule` (34..37)
  PROTECTED [P]; `newline-1/2/3`, `gap-1` NEUTRAL.
- Rationale (dialect finding): under P0/P1 the leading `---` is a Rule and the
  following paragraph plus the closing `---` form a **setext H2 heading**
  (CommonMark core), so the key/value lines are heading text (prose leaves;
  residual config); under P2 the whole front matter is a metadata block
  (protected). The P0/P1 exposure expectation is unchanged from the draft
  (still PROSE_CANDIDATE); the region now matches the actual structure.

### F42 (nested-list-prose) — (A)
- Original overrides: `item-1` (9,12), `item-1-1` (17,24), `item-1-2` (29,36),
  `item-2` (37,40) — each included the list marker bytes.
- Final: (11,14), (19,26), (31,38), (41,44) — the item text only.
- Rationale: the intended regions were the item texts (per the draft's own
  names and the frozen policy: list markers are syntax).

### F48 (angle-autolink-mailto) — (A)
- Original: `prose-3` = `.\n` (included the trailing line ending).
- Final: (52,53) (CP) = the `.` only (byte 53..54).
- Rationale: line endings are never prose (frozen policy note).

### F49 (unclosed-backtick) — (B) + (A)
- Original: one region `prose` covering both paragraphs across the blank line.
- Final: `line-1` (0..25 CP) and `line-2` (27..33 CP) PROSE_CANDIDATE;
  `blank-line` (25..27 CP) NEUTRAL. The draft's CP math also missed the
  two-byte `č` in "Neparični"; the final values are the exact code points.
- Rationale: line-ending bytes are never prose; the unmatched backtick itself
  stays asserted exposed (literal text).

### Evaluator (tools/run_increment1.py) — implementation notes
- **D1 (policy token families):** the frozen policy names container families
  (`S.Head`, `S.Item`, `S.TableCell`, ...); the adapter emits level-suffixed
  tokens (`S.Head:N`, `S.List:ol:N`). The evaluator implements "ancestor set
  intersects PROSE_CONTAINERS" as: a family entry matches its own token or any
  `<entry>:<suffix>` token. This implements the frozen rule without weakening
  or extending the named set.
- **D0 (autolink destinations):** a CommonMark autolink is the only `S.Link`
  whose original source slice starts with byte `<`; its inner Text leaf is the
  destination. Deterministic source-byte test implementing the frozen intent
  "link destinations remain protected". No content parsing.
- **Determinism contract:** both the initial and the verification pass record
  raw adapter bytes, so "identical rerun -> identical bytes" is measured
  directly.
- **Negative self-test (order Verification):** corrupted-range,
  bisection, protected-exposure, prose-missing, and CLI-offset probes must be
  caught by the evaluator's own detectors before any fixture result is
  trusted; the run aborts if any probe fails.

# 008-a research report — pulldown-cmark 0.13.4 as the structural prose boundary

Order 008-a (falsification experiment). Research-only record; no production
readiness or linguistic-quality claim. Objective 009 remains reserved and
untouched. Every claim below cites a committed record (path + SHA-256 where
material). No raw private LLM text appears in this subtree.

**Outcome: GO** (see question 12).

## Committed records cited in this report

| Record | SHA-256 |
| --- | --- |
| `config/experiment-008a.json` (frozen) | `622a1479d46cfce956267c546e3997eda460f084a555aeced7b88ae69a8f255f` |
| `identity/candidate-identity.json` | `671d7cded433bbc0a3e1f60fcb4a2da7d89f2a79e254f6a5b57ac80eb38d9c0d` |
| `fixtures/fixtures.json` (frozen suite) | `a2325de9a0bb4f04e84c2227710b5b62dad6e733503c08cab43e47839fd7cc00` |
| `fixtures/authoring-corrections.md` | `8a106621d2dffb17498534b1c97eba252b318f8e513b490015140912e79fdd3a` |
| `results/increment1/summary.json` | `06961c54a49a8e68f175153c46f60d869865fc8ac497c17c1e80cf556a5d333b` |
| `results/increment1/gate-decision.json` | `f6813b7731e43c82454b9b996eb76cf1ed76b7e2ed9461cc96db96be476f9c03` |
| `results/increment2/selection-receipt.json` | `cb27cb462cf9b33e42ce1e77db5ef5d9a33d0a3fc411aea39a08587ec8b1391b` |
| `results/increment2/differential-summary.json` | `81f73961ceb9255da2bb98af86cc20f283cd041467b330fb6322f08cdfa4fb9c` |
| `results/increment2/challenger-decision.json` | `8c056bc94cf514c6fe46277998deb3dd5d4208a80ac2727695ec5f818863c68f` |

Candidate identity (from `identity/candidate-identity.json`): crates.io
`pulldown-cmark` 0.13.4, registry checksum
`e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e` (verified
against the ordered download and the local crate), not yanked, published
2026-05-20; upstream `pulldown-cmark/pulldown-cmark` tag `v0.13.4` (commit
`38e4d08f14ec4bd9783270e9623db7681ebed968`); license MIT (crates.io version
record, repository LICENSE at tag, crate `Cargo.toml`); MSRV 1.71.1 (local
rustc/cargo 1.75.0); locked transitive dependencies bitflags 2.13.2,
memchr 2.8.3, unicase 2.9.0; measurement-adapter binary
`prose-boundary-meas` SHA-256 `5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf`.

## Execution notes (interpretation, gate, authoring corrections)

- **Single-round interpretation.** The order declares two supervised
  increments with a strategy review gate between them, but its publication
  structure mandates one final report-only commit for the round. This round
  therefore executed as one reported round in the exact predeclared order:
  Increment 1 (steps 1-8) -> gate checkpoint (step 9) -> Increment 2. The
  gate is a documented checkpoint: the predeclared proceed conditions are
  evaluated and committed in `results/increment1/gate-decision.json`
  (decision `PROCEED_TO_INCREMENT_2`), and the strategy review is enforced by
  the strategy final-head review before any merge (P-REVIEW-01). The
  predeclared stop condition (source-range premise failure => immediate
  NO-GO) was armed throughout and not triggered.
- **Authoring corrections.** The first draft of the fixture suite (working
  tree only, never committed) was corrected before the suite's first commit:
  14 fixture declarations (arithmetic/anchor errors, token-level precision,
  and two construct-interpretation fixes) plus two evaluator implementation
  notes (D0 autolink destinations, D1 policy token families). Full audit log:
  `fixtures/authoring-corrections.md`. No correction weakens any protection
  claim; the committed `fixtures/fixtures.json` is the frozen suite.
- **Strikethrough semantics (recorded tradeoff).** Under the frozen rule
  ("Text is candidate iff its open-tag ancestor set intersects
  PROSE_CONTAINERS and not NON_PROSE_CONTAINERS"), strikethrough/superscript/
  subscript content is exposed as candidate prose, because it inherits the
  enclosing paragraph's container status (observed on F40 P1/P2: 5 exposed
  bytes, recorded as a NEUTRAL tradeoff in
  `results/increment1/summary.json`). The config note's "conservatively
  suppressed" phrasing does not match the rule's intersection semantics.
  These constructs wrap prose, not machine content, so this is not a safety
  issue; if suppression is desired, 008-b decides whether to add
  `S.Strike`/`S.Sup`/`S.Sub` to NON_PROSE_CONTAINERS.

## Increment 1 — core falsification (all 8 steps + gate)

- **Fixture suite:** 50 project-authored fixtures (38 required classes + 12
  extras), 4,910 input bytes, frozen (committed) before first parser
  execution on the committed suite.
- **Event corpus:** 1,288 events across 50 fixtures x 3 profiles (P0
  CommonMark core; P1 + tables/strikethrough/tasklists/math; P2 + YAML-style
  metadata blocks).
- **Hard invariants (all true, `results/increment1/summary.json`):**
  - 100% exact source-range fidelity: every emitted `[start_byte, end_byte)`
    is an exact original-source slice; no range bisects a UTF-8 code point;
    the byte<->code-point mapping was demonstrated exactly reversible on
    every emitted boundary (carons, 4-byte emoji, decomposed combining
    sequences, CRLF all covered by fixtures F33-F36, F45, F50).
  - Frozen structural policy holds on every fixture and profile:
    `protected_region_exposures = 0`, `prose_candidate_missing_bytes = 0`.
  - No unexpected event kinds; invalid UTF-8 rejected cleanly (exit code 3,
    no events); a full rerun is byte-identical (determinism).
  - Stock-CLI cross-check: the adapter's `(kind, start, end)` multiset equals
    the stock `pulldown-cmark 0.13.4 --events` multiset on all 50 fixtures
    and all 3 profiles (independent offset measurement, same pinned crate).
  - Evaluator negative self-test (deliberately corrupted range/bisection/
    semantics probes) passes before any result is trusted.
- **Gate checkpoint (step 9):** all predeclared proceed conditions true
  (`results/increment1/gate-decision.json`, decision
  `PROCEED_TO_INCREMENT_2`).

## Increment 2 — representative corpus and differential

- **Selection (receipt only, no raw text):** 8,919 `dataset.input` records
  across the three preserved private roots (007-i/j/m) and both benchmark
  directories; 2,670 unique texts by sha256; sample = first 100 in ascending
  sha256 (deterministic, non-curated).
- **Corpus limitation (stated explicitly, per the order):** the preserved
  corpus is the 007 spelling-repair benchmark output and is **overwhelmingly
  plain prose** — 0 of the 2,670 unique texts (and 0 of the 100 sampled)
  contain any Markdown structural marker (no backticks, fences, headings,
  lists, links, images, tables, HTML, or dollar pairs; max length 444 chars).
  It therefore cannot test the structural question; per the order, the
  project-authored adversarial fixture suite is the structural ground truth
  and the real outputs are used for prevalence/disagreement observations
  only. No objective-009 data was used; no new model calls were made.
- **Differential (A = `research/curated/protected.py::protected_intervals`;
  B = adapter P2 candidate-prose set; disagreement unit = maximal span of the
  symmetric difference; 8-class consequence classifier in frozen priority
  order; controlled synthetic-pair self-test passed: boundary mismatch ->
  class 5, currency residual -> class 7, delimiter protection -> class 2):**
  - 100 samples, 11,729 text bytes; B candidate prose = 11,729 bytes
    (100% of the plain-prose bytes exposed — zero prose suppression).
  - 22 disagreement spans, **all class 7 (expected residual semantic
    category)**, all in the direction "B exposes, A protected": 18 number
    tokens (including their short units, e.g. age/amount expressions) and 4
    upper-identifier tokens. The current regex protection protects these
    machine-like tokens; the parser exposes them as text — the bounded
    second-stage recognizer problem anticipated by the frozen policy.
  - Class 3 (parser falsely exposes machine-significant content, SAFETY
    class) = 0; class 6 (malformed-input safety difference) = 0 (no sample
    is deterministically flagged malformed); class 8 (unresolved) = 0;
    classes 1/2/4/5 = 0.
  - Coordinate invariants held on every corpus event (the tool aborts on any
    violation).
- **Challenger (recorded either way):** `markdown-rs 1.0.0` **NOT
  TRIGGERED** — none of the predefined material conditions is met
  (`results/increment2/challenger-decision.json`): source ranges are exact;
  no relevant GFM incompatibility was observed (tables/strikethrough/
  tasklists/math behave per CommonMark/GFM on the fixture suite); malformed
  input handling is deterministic and safe on all adversarial fixtures;
  math/currency behaviour is acceptable (below); no structural
  misclassification affects the actual output (class 3/8 = 0).
  tree-sitter-markdown was not revived; Pandoc was not needed.

## Answers to the 13 report questions

1. **Was the Deep Research recommendation empirically validated?** Yes,
   within the experiment's scope: the leading candidate (pulldown-cmark
   0.13.4) was locally executed on a frozen adversarial suite and a
   deterministic real-output sample, and its structural/source-range
   contract holds (Increment 1 hard invariants all true; Increment 2 class 3
   = 0). The Deep Research report had not run the candidate locally; this
   round is that empirical step. Caveat recorded: the preserved real corpus
   is plain prose, so structural validation on real output rests on the
   adversarial fixture suite (ground truth per the order) plus prevalence
   observation on the real sample.
2. **Does pulldown-cmark give exact usable source ranges on our inputs?**
   Yes. 1,288/1,288 fixture event ranges (3 profiles) and all ranges on the
   100 corpus samples are exact original-source byte slices; no range splits
   a UTF-8 sequence; the byte<->code-point mapping is deterministic and
   exactly reversible on every observed boundary. Independently confirmed by
   the stock CLI `--events` cross-check (50x3 exact multiset agreement).
3. **Which coordinate system will the application use?** Code-point
   (Python `str`) coordinates — the existing application contract
   (`research/curated/protected.py` operates in code points). The parser's
   byte offsets map into it via `cp = len(bytes[:s].decode('utf-8'))` (and
   the inverse `byte = len(text[:cp].encode('utf-8'))`), proven exact and
   reversible for every observed range; invalid (mid-sequence) boundaries
   are rejected fail-closed (`byte_to_cp` -> None). Cost: decoding the byte
   prefix per boundary; a single forward decode pass per document computes
   all boundaries in O(n). CRLF bytes, decomposed combining sequences, and
   multi-byte carons/emoji are handled without bisection (fixtures F33-F36,
   F45, F50).
4. **Which Markdown structures are solved structurally?** Inline code,
   fenced code (incl. variable-length, tilde, and never-closed fences),
   indented code, block HTML and inline HTML (tags protected, intervening
   text exposed), recognized inline/display math (P1/P2), links (label
   exposed as prose; syntax and destination protected, including reference
   links and autolinks — URL and mailto, via the D0 rule), images (conserved
   default: whole structure protected, incl. alt text — recorded tradeoff),
   tables (P1/P2: cell text exposed, delimiter row and pipes not exposed),
   YAML-style metadata blocks (P2), headings/list/blockquotes (markers
   protected, text leaves exposed), emphasis/strong (delimiters protected,
   text exposed), thematic breaks. Malformed-structure recovery is
   deterministic (question 6).
5. **Which constructs remain residual semantic cases?** Paren/bracket TeX,
   begin-end TeX environments (align), bare JSON, YAML/TOML/config-like
   lines, shell commands, paths (incl. Windows), environment variables,
   identifier-heavy tokens, numbers (incl. short units), and dialect-missed
   URLs (bare URLs, no GFM autolink extension). Documented dialect
   behaviours: a `# comment` line is an ATX heading (F29); front-matter
   key/value lines are setext-heading text under P0/P1 and a metadata block
   under P2 (F41); a link label may legally contain parentheses (F37). On
   the real corpus the residual is exactly 22 token spans (18 number, 4
   upper-identifier), 110 bytes in total, ~0.9% of the 11,729 sampled
    bytes).
6. **What happens on malformed input?** Deterministic, bounded recovery with
   no crash and no unexpected event kinds: never-closed fence swallows the
   remainder as code (F07, F38); unmatched backtick is literal text (F49);
   unpaired TeX stays text (F15); an unresolved link stays literal prose
   while a well-formed unusual link is parsed as a link with its destination
   protected (F37); invalid UTF-8 is rejected with exit code 3 and no
   events; mixed malformed Markdown/HTML/TeX (F38) recovers to a code block
   after the heading. Conservative suppression is preferred and recorded as
   tradeoffs (e.g. image alt text, metadata under P2).
7. **What is the dollar-math decision?** With the math extension (P1/P2):
   `$...$` pairs with non-space-adjacent delimiters form recognized math and
   stay protected (F10, F11); currency patterns never form math — "5 $ in
   10 $" and "2,50 $" remain plain text with dollars exposed (F16; ST-2
   self-test on the differential); escaped `\$` yields literal dollars with
   the escape backslashes protected (F17). No sample in the real corpus
   contains a dollar pair. Decision: the safety/coverage tradeoff is
   acceptable; the lone-`$` and currency exposure is a bounded residual
   (class 7), not a material weakness — no challenger trigger.
8. **How does it differ from the current regex protection?** Structurally,
   the parser adds protection the regex layer has none of (code, HTML, math,
   links/destinations, images, metadata — 0 protected-region exposures in
   the frozen suite). On the real corpus the only difference is the reverse:
   22 token spans (numbers with short units, upper identifiers) that the
   regex protects and the parser exposes as text — class 7 residual, bounded
   and enumerable. No prose byte that both protect-differently in a safety-
   relevant way: 0 spans in classes 1-6 and 8.
9. **Did any machine-significant content become falsely exposed?** No false
   exposure of constructs the parser claims to recognize structurally
   (safety criterion met: class 3 = 0 on fixtures and corpus; protected-
   region exposures = 0 in the frozen suite). Machine-like *tokens*
   (numbers/identifiers) are exposed as ordinary text by design — that is
   the declared bounded second-stage problem, not a false exposure.
10. **How much valid prose was unnecessarily suppressed?** Zero. Every
    declared PROSE_CANDIDATE region is fully exposed (missing bytes = 0 on
    all fixtures/profiles), and on the corpus B exposes 11,729/11,729 bytes
    of plain prose (class 4 = 0). The only suppressions are the frozen
    policy's protected-structure set by design; the two recorded NEUTRAL
    tradeoffs (strikethrough text exposed under P1/P2 — see execution notes)
    are exposures, not suppressions.
11. **Was the markdown-rs challenger triggered and why?** Not triggered.
    Every predefined material condition was evaluated and is false (exact
    source ranges; no relevant GFM incompatibility; deterministic safe
    malformed-input handling; acceptable math/currency behaviour; no
    structural misclassification on actual output). Evidence:
    `results/increment2/challenger-decision.json`.
12. **GO / CONDITIONAL GO / NO-GO?** **GO.** All predeclared Hard criteria
    hold (exact source-range fidelity, no sequence splitting, recognized
    code/math never exposed, HTML/metadata protected per policy, link
    destinations protected, prose leaves exposed, deterministic bounded
    behaviour, no parse/re-render requirement). Safety criterion holds
    (zero false exposures of structurally recognized constructs). Coverage
    criterion holds (no over-protection of prose in headings/lists/
    blockquotes/table cells/link labels/emphasis-strong; actual losses
    reported: none for declared prose; conservative suppressions are the
    policy's own). Residual criterion holds: the remaining exposed
    machine-significant content is the bounded, comprehensible token-level
    set (numbers/units, upper identifiers on real output; TeX/JSON/config/
    shell/paths/env-vars/dialect URLs on adversarial input) — a second-stage
    recognizer problem, not fundamental unsuitability. The plain-prose
    nature of the preserved corpus is recorded as a data limitation (not a
    parser condition) with the order's prescribed remedy applied.
13. **Exact recommendation for 008-b.** Issue 008-b to implement the
    parser-first protection architecture: pin pulldown-cmark 0.13.4
    (checksum above) as the structural boundary; use code-point coordinates
    with the proven byte<->code-point mapping layer; adopt the frozen
    structural policy including the D0/D1 implementation rules; keep the
    current token-level regex rules as a small deterministic second-stage
    recognizer over the candidate-prose set for the bounded residual (numbers
    with short units, upper identifiers, env-var-style tokens, and, per
    policy decision, the residual TeX/JSON/config/shell/path categories);
    decide the open policy items (strikethrough/superscript/subscript
    suppression via NON_PROSE_CONTAINERS; image alt-text exposure); retain
    this subtree as the regression baseline (frozen fixture suite + 100-
    sample differential receipt) and gate replacement of the Markdown-
    sensitive part of the protection on a differential regression against it.
    No linguistic acceptance claim is made; 009 remains reserved.

## Privacy and determinism statements

- No raw private LLM outputs, prompts, or responses appear in this subtree
  or in this report; the selection receipt and differential summary carry
  counts/categories/hashes only; no private absolute path is committed
  (private runtime roots are supplied at run time as CLI arguments).
- All committed tools are deterministic: identical reruns on the same inputs
  reproduce identical output bytes (verified for the evaluator, the
  selection receipt, and the differential summary).
- Zero Qwen/model calls; zero new data acquisition; no objective-009 data
  touched; no linguistic tuning of the frozen 007-m system.

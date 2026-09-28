# 008-g research report — bounded mid-document raw-block protection fix, completed naturalistic adjudication, and final objective-008 verdict on a new sealed hidden set

Order 008-g (corrective and final-verdict round of objective 008).
Research-only record; no production readiness, no release, no deployment, and
no linguistic-quality claim. The final objective-008 verdict recorded here is
STRUCTURAL-SAFETY EVIDENCE ONLY. Objective 009 remains reserved and untouched;
its future sample must not contain any case generated or inspected for
objective 008 (every v1 and v2 component, mashup, and naturalistic case).
Every claim below cites a committed record (path + SHA-256 where material).
No raw private LLM text, no private-root content, and no private paths appear
in this subtree; the v2 hidden set, the spent v1 set, and all adjudication
labels are referenced by committed content-free manifest hashes only.

**Outcome: final objective-008 verdict CONDITIONAL** (predeclared decision
state). The named defect-class shapes are fixed on the fresh pool (zero
exposure in the structured-yaml and structured-xml families; 0 B
policy-exposed in the defect-class families). The remaining bounded scope is
named: one 51 B pre-existing architecture gap on the v2 acceptance set (3 of
2,000 documents; identical exposure under the unfixed implementation) and
five named material naturalistic-consistency cases (parser-dialect dominated).
The completed adjudication (70/70 labels, 0 failures) clears D1-2; D1-1 (fix
mechanism) carries forward until a final PASS.

## Committed records cited in this report

| Record | SHA-256 |
| --- | --- |
| oap/orders/008-g-raw-block-protection-fix-and-final-acceptance.md (order, 55,111 B) | 20ea7c543c9110c89956dd22a838b5f0497b6949d5f58dae28d06a478c5b0319 |
| research/prose-boundary/config/structural-policy-v2.json (frozen v2; byte-identical in-tree) | 996f465784bed37a179be337e2af606b2dc350cacba6341479371d2812c5a88e |
| research/prose-boundary/config/structural-policy-v3.json (active policy) | 7ff6646e3c11d1241cb1c85bd96f08e3f0db08e73d4eb4a4e97fac0c17e1828f |
| research/prose-boundary/config/experiment-008g.json (round config; v2 to v3 sha256 pair; frozen census; D0 choices) | 6346d7cec938defda58d2607e8aca41638359f66ca4856d2dea8f6d85960a5c8 |
| research/curated/prose_boundary.py (frozen census at the dev-regression gate) | 3a5a4ba7b5258dc7937a9b4ef98a90982a6a159d5d8763160f3105048545f2d7 |
| research/curated/protected.py (byte-identical to the 008-f final head) | 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f |
| research/tests/test_raw_document_fragment_protection.py (new focused file) | 2a8fb5c7cc5f39dac545ca6cea414dedad45664a7e786a109657eb3af3d356bb |
| research/prose-boundary/config/generation/generation-identity-008g.json | ddc73cefe9886247c4c7244246d86df353d0a0ee330114d19c09c75b5d8c4922 |
| research/prose-boundary/config/generation/prompt-families.json (frozen prompt library, verbatim) | 904dd36b9891c567f250bf8b42b374d0b6557aa79ca3fcaa3c8824682fcc8fef |
| research/prose-boundary/corpus/manifests/hidden-manifest-v2.json (content-free v2 manifest) | cf37654a45b10c024525fc334f368d4b20956619e2568542544c855d93a85ec1 |
| research/prose-boundary/corpus/manifests/seal-verification-v2.json | c532738dc4ca4e5441b9f35a3cb0930eae02a966562b62f6557c660dfa731a75 |
| research/prose-boundary/corpus/manifests/hidden-annotations-manifest.json (content-free) | fe088cfbbbc6013d8567c3afb8b27192e88b0e5ada07c39b21c280addbf96647 |
| research/prose-boundary/corpus/manifests/corpus-census.json (additive dev-batch update) | 744d69451ab67be925d6f6dc5f2fa54e7f30032557a3dce5f0482a46c7650215 |
| research/prose-boundary/results/hidden-acceptance-v2/dev-regression-008g.json | 7c369cd65dc134ba3f152cc914e9e69e001985b3f2d5071f64301ffda16ff08a |
| research/prose-boundary/results/hidden-acceptance-v2/mashup-metrics-v2.json | 4687bc31e2177edf60548fd1bb30221a6110a9bcf7af6c6dbcb3efef11566938 |
| research/prose-boundary/results/hidden-acceptance-v2/e2e-invariants-hidden-v2.json | 65307f332ff6cd9547dca6bdb67e4f65c2b5fee6cb6ea465f9885a7d522dc390 |
| research/prose-boundary/results/hidden-acceptance-v2/v1-diagnostic.json (DEVELOPMENT DIAGNOSTIC ONLY) | a94deb7e3369755d362a4978066d12c0fcc8be12fd29c0174c1563fe43e8860f |
| research/prose-boundary/results/hidden-acceptance-v2/adjudication-v2-summary.json | e8bf6a3b4bd1bd96e21872c4a5041e43a05acfeb535a25731c799dcd86bdbd05 |
| research/prose-boundary/results/hidden-acceptance-v2/naturalistic-consistency-v2.json | 171293b4a18411b5e01b9e9e76e6a0d1b8cbc4f9dd0e32dce094ea09c5893c9d |
| research/prose-boundary/tools/hidden_acceptance.py (frozen 008-f harness; imported unmodified) | 22ae618bd1be66bfd93c79a10e97066eef5dcd05213f851e7b19f5a12e8771fd |
| research/prose-boundary/tools/hidden_acceptance_v2.py (new thin wrapper) | d9b1a41ca9554be0b36df93ec3a4b7760dbb28249efeaf26332180c13a7f7b96 |
| research/prose-boundary/tools/naturalistic_adjudication.py (committed 008-f driver; byte-identical) | 1a547169f885ebb92bdd46bc11bc6491f6e0899c67ed8c45e23beb1d78743f54 |
| research/prose-boundary/tools/naturalistic_adjudication_v2.py (new v2 driver) | 1703996b92e3e5e0ebef92e124e6f4974e3ca59e6ab2f9c8e760f79076cc08f1 |
| research/prose-boundary/config/annotation-guide.json (frozen guide; adjudication basis) | e65816ddda65343e45b9c0b9fa112b8e18eea19b17310a997cff87b9a200eb5e |
| research/prose-boundary/corpus/manifests/hidden-manifest.json (v1, single-use spent) | 8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18 |
| Pinned helper prose-boundary-meas (008-a recorded identity) | 5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf |
| Strategy v2 seal verification receipt (supervision tree; not committed) | b24ed3f6693d19d180972d440f09d1c3c562d6e8e260d804ecac9f4a8d1488a5 (2,305 B, cites the v2 manifest sha256) |

## 1. The bounded fix (D1-1 choice (a): residual-layer extension)

The 008-f hidden acceptance found 458 B (20 of 2,000 documents, 19-24 B each,
all template T10-randomized, category structured; families structured-yaml
348 B and structured-xml 110 B) of mid-document raw-block content exposed as
candidate prose. Mechanism: the CommonMark dialect does not recognize
mid-document YAML blocks or HTML/XML fragments whose tags are not HTML
block-start tags, so the content parses as paragraph text; the frozen
yaml-toml-config residual class required two or more consecutive key-value
lines or a section header and did not cover the exposed single-line and
nested shapes; no residual class covered non-recognized tag fragments.

Per the D1-1 record (order Governance) the fix extends the residual semantic
layer (the designated home for machine-significant content the parser cannot
structurally distinguish) rather than a structural pre-pass:

- **Policy v3** (structural-policy-v3.json; v2 byte-identical in-tree; the
  v2 to v3 sha256 pair is recorded in experiment-008g.json): (1)
  yaml-toml-config coverage extended under the scope-4 strictness contract -
  a single word-key line is protected only when the whole trimmed value is
  machine-like (number, path, relative path, identifier, environment-variable
  form, or single-line quoted literal) or the value is empty and immediately
  followed by nested list-style lines; nested list-style lines extend a
  protected run; every v2 two-or-more-line run and section run keeps its v2
  protection exactly; (2) new residual class xml-fragment - a paired
  non-recognized tag fragment (namespaced prefix-colon name, or a name
  outside the dialect tag-name shape of letter then letters/digits/hyphens)
  is protected in full, a self-closing token and a standalone closing token
  are protected, and an unbalanced opening fragment is protected to the end
  of its line (recorded D0 choice, justified in the v3 changelog); span bound
  at most 2000 code points; the class never fires on comparison operators,
  on an opening bracket followed by digits, or on a lone bracket (the trigger
  requires a letter or underscore after the opening bracket and a closing
  bracket on the same line); recognized tag names abstain for v2 parity;
  (3) malformed_class_map additions: mid-document-yaml (protected),
  mid-document-xml-fragment (protected), and yaml-nested-parser-split
  (policy-exposed - the parser dialect splits a nested YAML key line from its
  list continuation into different blocks, a pure-function-of-one-span limit
  of the residual architecture; the bounded, named limit); all v2 entries
  unchanged; (4) determinism and scope clauses carried unchanged.
- **Implementation**: the two recognizer changes live in
  research/curated/prose_boundary.py, the 008-c residual-layer home, as pure
  deterministic functions of parser-approved candidate-prose text with
  code-point coordinates (recorded D0 placement choice; protected.py stays
  byte-identical to the 008-f final head). No Markdown-delimiter regexes; the
  residual layer still operates only on parser-approved candidate-prose
  spans. Policy consumption switched to v3 via load_policy_v3 with
  load_policy_v2 retained as a compatibility alias (the candidate rule is
  byte-identical between v2 and v3), so the frozen 008-f harness and the
  008-c test suite call unchanged entry points.
- **Tests**: research/tests/test_raw_document_fragment_protection.py carries
  the positive cases (each defect shape from the dev batch) and the negative
  cases (every prose control stays candidate prose; inequality brackets stay
  exposed; a lone bracket stays exposed; recognized-HTML behaviour
  unchanged). Re-run at this report's head: 34/34 in the new file; the
  existing parser-first protection suite 48/48; no existing assertion
  weakened anywhere.

**Residual gaps disclosed (outside the scope-4 strictness contract):** the
xml-fragment trigger's name pattern is ASCII-only, so XML tag names
containing a non-ASCII (diacritic) letter do not fire (visible in the v1
diagnostic, section 6); YAML comment lines of the hash-plus-text shape parse
as Markdown headings before any recognizer sees them (also v1 diagnostic).
Both are named in the v3 changelog context and in the final verdict.

## 2. The new sealed v2 hidden acceptance set

Generated under the committed 008-c generation driver (imported unmodified)
and the frozen prompt library, with a new recorded generation identity
(generation-identity-008g.json): model qwen3.8-27b (A100-FP8 007-lineage
deployment record; profile sha256
510c3394d2ccad8a098660b8b5512d338de0a5b77352ec693d2286ee2223723c; endpoint
value omitted per 007 convention). 340 new components across all 76 families
(base batch of 4 per family; densified 8 per affected call for
structured-yaml, structured-xml, and malformed-partial-html), composed into
2,000 deterministic mashup documents (mashup seed 9fdfa032940ba48d) by the
committed builder. Ground truth is by construction from composition
provenance; the builder asserts that no parser output participates in label
construction; the label oracle is the active v3 residual implementation at
composition (recorded D0, noted in the manifest).

Zero exact-component overlap with the committed dev pool (641 components) and
the v1 hidden pool (588 components) is asserted by the builder (hash-only
comparison, no content echo) and disclosed: the initial run produced 13
dev-pool and 10 v1-pool exact overlaps, all confined to four saturated
machine families; a bounded K=8 regeneration of those families recovered the
pool and the final assertion re-verified 0/0 over all 340 v2 components.
Model calls for this set: 95 HTTP (82 original-run attempts including the
preflight and two failed-then-retried batches, plus 7 bounded diagnostic
probes that established value-space saturation, plus 1 recovery preflight and
5 recovery component calls with zero recovery retries). This is authorized
test-data generation; it is not objective-009 material.

The v2 set was sealed into the private root (documents, labels, components):
4,076 files verified hash-identical to the committed content-free manifest at
seal time (seal copy byte-identical; 86 out-of-manifest files, all pre-seal
generation receipts, disclosed). Strategy independently re-verified the seal
data-free BEFORE the evaluation phase (receipt identity above) - the
evaluation driver's hard gate - and re-verified it again after the evaluation
phase (4,076/4,076, manifest sha256 unchanged). The v1 seal (4,091/4,091,
manifest sha256 unchanged) was re-verified data-free before and after the
evaluation phase as well, and per file through the harness loader during the
disclosed v1 diagnostic and label census.

## 3. The visible dev defect batch

research/prose-boundary/corpus/defect-dev-008g/ (50 documents + machine-known
labels; the only dev surface on which the fix may be tuned; corpus-census.json
updated additively): the defect shapes (single-line YAML key-value, nested
YAML list lines, sectionless YAML, tag fragments of the namespaced,
non-block-start, self-closing, paired, and unbalanced forms) plus the
explicit prose controls (a Slovenian label-style sentence with a colon and
prose continuation, a digits-colon-digits time expression, an inequality
comparison with angle brackets and a number, a less-than-N phrase with a
bracket, a prose sentence containing a single bracket, a colon-free
interrogative, and a genuine two-line YAML block as positive control).

## 4. Dev regression gate (committed before any hidden evaluation)

dev-regression-008g.json, evaluated through the frozen harness entry points
on (i) the frozen 3,000-document dev corpus and (ii) the 50-document dev
defect batch, with the implementation census recorded at the dev-regression
gate (the new frozen protection identity):

- Dev corpus: protected bytes exposed 0 of 526,315 (008-c baseline 0);
  coordinates 0/0/0; prose over-suppression 1.5485 percent against the 008-c
  baseline 1.5372 percent, delta plus 0.0113 percentage points against the
  predeclared 1.0 point bound.
- Dev defect batch: protected bytes exposed 0 of 702 for all defect-class
  shapes not classified policy-exposed in v3 (the yaml-nested-parser-split
  shape materialized 28 B policy-exposed there, exempt by the harness role
  handling and reported here).
- Actual losses reported by container regardless: dev corpus S.Emph 110,
  S.Head 436, S.Item 3,727, S.Para 20,291, S.TableCell 575, unknown 4,439;
  batch S.Para 28, unknown 93.
- Stop conditions (i)-(iii): none fired; status PASS.

## 5. v2 hidden acceptance metrics (first and only use of the v2 set as acceptance)

mashup-metrics-v2.json carries the full 008-c item-15 metric set over the
2,000-document v2 set through the actual frozen pipeline entry points, with
the embedded raw frozen-harness output explicitly labelled as raw
frozen-harness output over the v2 set (not a development-run result). The
008-f harness was imported unmodified via the disclosed thin wrapper
(hidden_acceptance_v2.py) with only its manifest and policy globals
re-pointed. A re-derivation check re-ran the committed wrapper to a scratch
output (e2e and performance axes skipped) and reproduced the committed
aggregate byte-identically except the wall-clock field and the omitted
section; the wrapper's nonzero exit on safety not met is by design.

- **Safety (the one material defect):** 51 of 384,363 labeled protected bytes
  exposed as candidate prose (0.0133 percent; target 0; not met).
  Attribution (3 of 2,000 documents, all template T10-randomized): v2h-001054
  (code-python, 35 B) - an adjacent structured-html closing tag opens an HTML
  block that absorbs the code fence plus 132 B of code; the blank line ends
  the block and the remaining code lines parse as paragraph, exposing the
  print-line syntax while identifier-like words and the number 99 stay
  covered; v2h-000262 and v2h-000218 (structured-keyvalue, 8 B each, same
  component) - the component embeds Markdown list items with quoted emphasis
  and the dialect parses list plus strong/emphasis, exposing quote characters
  plus one word. A re-run of the frozen 008-c implementation (policy v2) over
  the v2 set reproduces the identical 51 B in the same 3 documents: this is a
  pre-existing architecture gap newly surfaced by the fresh pool, not a fix
  regression. The named defect-class shapes themselves are fixed: zero
  exposure in the structured-yaml and structured-xml families on v2.
- **Coordinates:** 0 UTF-8 boundary violations, 0 byte/code-point conversion
  mismatches, 0 source slice mismatches, 0 patch-preservation violations.
- **Coverage:** 97.843 percent of expected prose bytes exposed
  (1,153,924 of 1,179,365); 494 of 8,382 expected prose regions completely
  available; unnecessary suppression reported as actual loss by container:
  S.Emph 56, S.Head 240, S.Item 1,788, S.Para 12,802, S.TableCell 268,
  unknown 10,287 (no arbitrary threshold).
- **Malformed-input behaviour:** 0 violations over the 10 deterministic
  family rows. Disclosed frozen-harness aggregation defect: the committed
  aggregate's policy-exposed row totals for the four policy-exposed
  malformed families (58/84/34/16) exceed the true label values (56/81/33/15)
  by a 7 B first-document double-count in the frozen 008-f harness
  merged_malformed aggregation (the first contributing row seeds the family
  accumulator and the merge loop adds that same document's values again; the
  first contributing documents v2h-000140, v2h-000339, v2h-000064, and
  v2h-000053 contribute 2/3/1/1 B respectively). Violation counts are
  unaffected (those documents have zero protected-exposed bytes); the frozen
  harness byte was not changed. The same quirk inflates the immutable 008-f
  v1 rows (committed 62/109/20/13; true v1 label census 60/107/19/13).
- **Policy-exposed census (explicit number):** 1,174 B total over the v2 set
  remain policy-exposed by label role - machine-emails 989 B (47 regions, 0
  implementation-covered; inherited from the v2 policy; non-machine-like
  values abstain under the v3 strictness contract) plus the four
  policy-exposed malformed families 185 B (incomplete-display-dollar 56,
  malformed-nesting 81 with 44 covered, unmatched-backtick 33 with 3 covered,
  unmatched-dollar 15 with 1 covered). The defect-class families
  (structured-yaml, structured-xml, structured-keyvalue) contribute 0 B, and
  the new v3 yaml-nested-parser-split class materialized 0 B on v2 (28 B in
  the visible dev batch). Computed from the sealed v2 labels through the
  frozen loader (which re-verified the seal per file) and cross-verified by
  per-document row summing (delta 0).
- **Determinism:** sorted doc_id iteration order; 50-case re-run identical.
- **Performance (qualitative statement only):** median 46.1 / 66.9 / 269.7
  ms per document at 1/10/50 KB (25 runs each), peak RSS 69,088 KB.
- **End-to-end invariants 1-7** (e2e-invariants-hidden-v2.json): all PASS on
  2,000/2,000 hidden-document replays through the actual frozen pipeline
  entry points (frozen deterministic stub boundary; zero network; zero new
  model calls).

## 6. Labeled v1 development diagnostic (disclosed; never acceptance)

v1-diagnostic.json re-runs the single-use spent v1 set under the fixed v3
implementation (frozen harness with only the policy global re-pointed; v1
manifest identity unchanged): 458 of 311,358 labeled protected bytes still
exposed (0.147 percent) - unchanged from the 008-f number. The named defect
shapes are fixed (the dev batch is 0), but the v1 defect population contains
two sub-shapes outside the scope-4 strictness contract: YAML comment lines of
the hash-plus-text shape parsed as Markdown headings (348 B plus 5 B; heading
text becomes candidate prose and no residual class fires) and XML tag names
containing a non-ASCII (diacritic) letter (110 B; the ASCII-only trigger
decides on the wrong name). Disclosed as remaining bounded scope, not as
acceptance evidence.

## 7. Completed naturalistic hidden adjudication (D1-2 refined instrument)

adjudication-v2-summary.json, under the strategy-devised line-indexed range
instrument (the committed 008-f driver stays byte-identical; the new v2
driver's partition-validator self-tests pass 18/18, data-free, zero model
calls):

- 70/70 label files in the private root; 0 ADJUDICATION_FAILED (no case IDs
  to name); 113 HTTP calls (1 preflight + 70 pass-1 + 42 pass-2; 0 retries; 0
  failed calls); model qwen3.8-27b (A100-FP8 007-lineage deployment record;
  profile sha256 above; endpoint omitted per 007 convention); fresh context
  per case; frozen guide bytes unchanged; no access to implementation source,
  implementation output, development labels, or objective-009 material.
- Final line-category totals: AMBIGUOUS 200, GENUINE_PROSE 326,
  STRUCTURAL_PROTECT 399, MACHINE_SIGNIFICANT_RESIDUAL 0,
  DELIMITER_WHITESPACE_NEUTRAL 0 (320 ambiguous lines total).
- Reconciliation (second pass over all pass-1 AMBIGUOUS plus a deterministic
  7-case sample at seed f3d72dd46013a779): 42 second-pass cases (35
  ambiguous + 7 sampled); 39 disagreement_reconciled (102 disagreement line
  spans), 3 identical, 28 single_pass.
- Cross-instrument agreement (sanity statistic only, never acceptance
  evidence): 17 comparable cases - 17 of the 18 preserved v1 raw files carry
  valid frozen tilings (nat-comparison-table-hidden-04 is the known invalid
  tiling, handled); strict line agreement 334 of 447 lines, ambiguous-
  tolerant 418 of 447. **Flag:** the order's predeclared "3 valid v1 tiling
  cases" wording is wrong; the actual comparable count is 17. Disclosed here,
  in the summary, the registry entry, and RESEARCH-STATE section 19.
- **Driver defect and recovery (disclosed):** the first run (same sample
  seed) completed passes 1-2 and then crashed in the mechanical
  cross-instrument phase - unassigned quote-tiling glue code points (empty
  category entries in the frozen v1 tilings) left the line-vote plurality
  empty and the pre-fix driver indexed the first pick (IndexError). Its at
  least 118 HTTP calls (1 preflight + 70 pass-1 + 47 pass-2; retry count
  unrecoverable because raws are overwritten on retry) are disclosed as
  driver-defect recovery overhead. The run's on-disk residue (187 files: 70
  label JSONs + 70 pass-1 raws + 47 pass-2 raws) was censored data-free
  (sha256 plus size of every file, recorded in the round's uncommitted
  scratch) and removed before the official re-run for clean provenance. The
  fix - glue excluded from the line vote; a line with no assigned code point,
  including an empty line, is DELIMITER_WHITESPACE_NEUTRAL - lives in the new
  v2 driver with added self-tests.
- The committed content-free annotations manifest covers the 18 v1 raw files
  and all 70 v2 label files (case IDs + sha256 + size only; no content, no
  private paths).

## 8. Naturalistic consistency check (requirement 8)

naturalistic-consistency-v2.json compares the fixed implementation's
protection output on the 70 naturalistic responses against the completed v2
labels (private-root reads through the harness only; data-free aggregate).
Predeclared materiality: any non-AMBIGUOUS structural-protect or
machine-significant-residual label range with an exposed span of 50 B or
more, or 5 or more exposed ranges of any size in one case. Result: **5
material contradictions** - nat-glossary-entry-hidden-03 (max 69 B exposed),
nat-json-config-hidden-01 (255 B), nat-math-answer-hidden-04 (53 B),
nat-qa-answer-hidden-04 (66 B), nat-table-equations-hidden-03 (125 B).
Attribution of the 15 exposed ranges across all 70 cases: parser-dialect 12,
label-ambiguity 2, residual-class-gap 1. By the predeclared rule this caps
the final verdict at CONDITIONAL (named bounded scope).

## 9. Final objective-008 verdict

Predeclared decision states applied field by field to the committed new
evidence (v2 hidden set + completed adjudication + dev regression):

- **Safety:** v2 target not met - 51 B of 384,363 (0.0133 percent; target 0).
- **Coordinates:** 0/0/0/0 (met).
- **Malformed behaviour:** 0 violations over the deterministic table (met).
- **End-to-end invariants 1-7:** all PASS on 2,000/2,000 (met).
- **Adjudication:** 70/70 labels, 0 failures (met).
- **Naturalistic consistency:** 5 material contradictions (not met).

**Verdict: CONDITIONAL** (predeclared decision state). Not PASS: the v2
safety target is not met and 5 material naturalistic contradictions exist.
Not FAIL: every exposure is bounded and its mechanism fully understood; the
named defect class itself is fixed on the fresh pool (zero exposure in
structured-yaml / structured-xml; 0 B policy-exposed in the defect-class
families); the parser-first design is not materially discredited.

Smallest corrective scope named: (a) a builder-side T10 composition
adjacency guard for the code-python / structured-html boundary (35 B) and
the Markdown-emphasis-in-keyvalue composition (16 B), or a label-oracle
refinement; (b) the five named material naturalistic-consistency cases
(parser-dialect-dominated residual); (c) the two disclosed out-of-contract
v1 sub-shapes (YAML hash-comment heading lines; XML diacritic tag names) if
a future scope elects to cover them.

Judgment debt: **D1-1 CARRIED FORWARD** (clears only on a final
objective-008 PASS verdict); **D1-2 CLEARED** (adjudication completed 70/70
with reconciliation statistics recorded in this record and the report).

Classification: STRUCTURAL-SAFETY EVIDENCE ONLY. No linguistic quality, no
experimental-MVP acceptance, no release or deployment authority. Objective
009 (fresh human-labelled linguistic confirmation of the complete frozen
pipeline) remains the separate reserved next objective; its future sample
must not contain any case generated or inspected for objective 008. No
merge, no auto-merge, no release, no deployment claim; PR #9 remains open
and unmerged. This verdict supersedes the 008-f CONDITIONAL as the current
state of objective 008 additively, in RESEARCH-STATE section 19 and
STATUS.md only; the 008-f section 18 and the 008-f report remain immutable.

## 10. Model-call accounting (recorded and classified distinctly)

- v2 component generation: 95 HTTP (test-data generation class; see
  section 2).
- Adjudication first (crashed) run: at least 118 HTTP (evaluation-process
  class; driver-defect recovery overhead).
- Adjudication official run: 113 HTTP (evaluation-process class).
- Total for the round: at least 326 HTTP. Zero linguistic-pipeline model
  calls; no other model calls of any kind.

## 11. Limitations

- Line-indexed adjudication granularity is coarser than the guide's
  span-level reading; the naturalistic responses are line-structured
  Markdown where protection-relevant spans align with lines, and mixed lines
  are what the AMBIGUOUS label plus reconciliation exists for; bounded
  granularity loss is accepted and disclosed.
- The cross-instrument agreement is a sanity statistic only (preserved v1
  observations vs the v2 instrument), not acceptance evidence, and the
  order's "3 valid v1 tiling cases" predeclaration was wrong (actual 17).
- The frozen 008-f harness aggregation double-counts the first contributing
  document per policy-exposed family in its row totals (7 B on v2; the v1
  rows carry the same quirk); violations are unaffected and no frozen byte
  was changed.
- The xml-fragment trigger is ASCII-name-only and the hash-comment YAML
  sub-shape is out of contract; both are disclosed, not fixed.
- The 51 B v2 residual is a parser-dialect block-boundary interaction and a
  Markdown-in-keyvalue composition; it is addressable at the builder/
  label-oracle level, not by a further residual recognizer.
- Single model deployment (qwen3.8-27b, A100-FP8 007-lineage record); the
  v1 set is single-use spent and was never cited as acceptance; the v2 set
  was used for the first and only time as an acceptance instrument.
- Performance figures are a qualitative statement only (no inference latency
  is measured in this round).

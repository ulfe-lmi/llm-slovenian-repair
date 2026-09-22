
008-i: Opening-tag composition extension, xml-fragment class-boundary decision,
display-dollar adjacency guard, T6 link-destination admission refinement, and
final objective-008 blind acceptance on a new sealed v4 hidden set
(corrective round 3 of objective 008; research-only; no deployment, no release,
no milestone claim, no objective-009 touch, no 007-m linguistic surface change).

```oap-metadata
{
  "id": "008-i",
  "title": "Opening-tag composition extension, xml-fragment class-boundary decision, display-dollar adjacency guard, T6 link-destination admission refinement, and final objective-008 blind acceptance on a new sealed v4 hidden set",
  "objective": "008",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "954d758b0d6308ce1811bccb25ab7d347ad99b7c",
  "branch": "oap/008-prose-boundary-qualification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 9,
  "dependencies": ["008"],
  "local_work": "Preserve byte-for-byte: every merged 000-007 seam on main; the entire research/ tree at the 008-h final head including ALL 008-a through 008-h round artifacts (orders, reports, registry entries, REPORT-008H.md, tools including hidden_acceptance.py, hidden_acceptance_v2.py, hidden_acceptance_v3.py, naturalistic_adjudication.py, naturalistic_adjudication_v2.py, naturalistic_consistency_v3.py, all results directories including hidden-acceptance-v3/* and naturalistic re-run records), the 008-c committed corpus and ALL 008-h additions to it (components-dev, documents-dev, labels-dev, naturalistic-dev, defect-dev-008g, defect-dev-008h, fixture suite, manifests v1/v2/v3 with their seal verifications, the hidden-annotations-manifest, corpus-census.json as rebuilt by 008-h), the frozen 007-m linguistic surfaces (config, prompt, final-root manifest), the annotation guide, every test file, scripts/verify_development_baseline.py (byte-identical, including the 300.0 default timeout), all workflows EXCEPT .github/workflows/application-baseline.yml (released below, single line only), every order and report byte, the 008-d quarantine record, the v1/v2/v3 private roots (seal re-hash only; no re-evaluation of any spent set), and any unrelated local work (untracked residue never committed). Released from freeze for this round ONLY: research/prose-boundary/tools/prose_boundary_builder.py (R1 extension to HTML block-start lines, display-dollar adjacency guard, T6 destination admission refinement, guard/label-source recording), research/curated/prose_boundary.py (the single predeclared xml-fragment trigger decision D1-5 ONLY, and nothing else; on the FALLBACK branch this file is NOT modified), research/prose-boundary/config/structural-policy-v5.json (new; v4 and v3 stay byte-identical in-tree), research/prose-boundary/config/experiment-008i.json (new; the 008-i four-file frozen protection census), research/prose-boundary/config/generation/generation-identity-008i.json (new), research/prose-boundary/corpus/defect-dev-008i/ (new), research/prose-boundary/corpus/manifests/hidden-manifest-v4.json (new), research/prose-boundary/corpus/manifests/seal-verification-v4.json (new), research/prose-boundary/corpus/manifests/corpus-census.json (additive), research/prose-boundary/tools/hidden_acceptance_v4.py (new), research/prose-boundary/tools/naturalistic_consistency_v4.py (new), research/prose-boundary/results/hidden-acceptance-v4/ (new), research/prose-boundary/REPORT-008I.md (new), research/tests/test_008i_composition_and_class_boundary.py (new), research/registry/experiments.json (append exactly one 008-i entry), research/RESEARCH-STATE.md (additive section 21 + machine block), STATUS.md, oap/GENERATED-FILES.json (scoped pin), research/tables/experiment-summary.csv (rebuild), oap/orders/008-i-corrective-scope-and-v4-final-blind-acceptance.md (new, activation), oap/active (pointer), oap/reports/008-i-corrective-scope-and-v4-final-blind-acceptance.md (new, report-only commit), .github/workflows/application-baseline.yml (EXACTLY line 35 at the 008-h final head: append ' --command-timeout 600' to the driver invocation, making the CI per-command cap 600 s for every driver command in CI; every other byte of the file and of all other workflows unchanged; amended file pinned sha256 4490d0fc9e9fcd3eb697b1721b385f986f1a232372593618501dc0ed0918bc4c).",
  "prior_review": "Strategy independent final-head review of 008-h (2026-09-21, private workorders/008-h-final-head-review-20260920.md, status COMPLETE): report-only commit 954d758b0d6308ce1811bccb25ab7d347ad99b7c (sole parent 6e2352948e8e748f1f942709ae8daa55cfdd382c, the implementation head; sole changed path oap/reports/008-h-composition-contract-fix-and-final-blind-acceptance.md, 76,944 B, git blob 1a16fa3398f330dec6a81ad8e039b1286ccd84ae; the initially-built a9e29d9 with a PLAN.md governance-hash typo was caught by the coding local gate, stop-and-correct applied, amended out, and never pushed - dangling locally, zero remote refs); strategy remote verify_report at the final head = verified (scope remote, report_history valid, report_count 52, frozen 006-a/006-c incidents unchanged); check_state remote scope = REVIEW_READY; PR #9 OPEN / UNMERGED / auto-merge DISABLED, head 954d758b0d6308ce1811bccb25ab7d347ad99b7c, base main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 (equals OAP_ACCEPTED_REF, unchanged); required checks at the final head: OAP bootstrap acceptance PASS (run 35544295071), OAP report history PASS (run 35544295071), Research reproducibility PASS (run 35544295075), Application baseline at the 008-h final head 954d758: seven runs, all zero-failure full-pytest TIMEOUT (walls 349.58-352.14 s) at the committed byte-frozen 300 s per-command cap with every other driver command PASSED (jobs 106167363230/106225102320/106226701923/106228145547/106229612442/106305614684/106710758142; both predeclared daytime rechecks 2026-09-21 and 2026-09-22 TIMEOUT - the predeclared escalation trigger of 2+ daytime TIMEOUTs met 2026-09-22 12:44 CEST); the bounded finding was presented to the owner, who selected Option A1 (owner decision recorded 2026-09-22 18:24 CEST: narrowly scoped CI timeout override to 600 s at the workflow invocation only, driver 300 s default preserved, the workflow's existing outer job timeout unchanged, all four required checks genuinely green required at the reviewed final head, no Option B, no broadening into unrelated test optimization); per that selection this round incorporates the single-line CI per-command budget change (Scope item 15 / requirement 13 extension / local_work release below), so the four required checks are evaluated as green at THIS round's final head, which carries the 600 s CI cap; the 008-h round itself remains ACCEPTED as published at 954d758; full recheck evidence in the private review workorders/008-h-final-head-review-20260920.md (addenda 2026-09-21 13:05 CEST and 2026-09-22 12:46 CEST) and workorders/daytime-recheck-2026092{1,2}-result.json; order bytes sha256 782c6811e1963fc07779d4209461ff6ad1057eec62ffa652b5916e6c6fa73342 re-verified from the committed blob at the final head; all sixteen report governance hashes re-verified against the final-head blobs (zero mismatch, including the corrected PLAN.md d2aa1d98...); full round diff fca215c..954d758 audited by strategy diffscope = PASS (out_of_scope=0, frozen_ok=True; 88 paths all inside the released-from-freeze list); eight committed aggregate hashes re-verified (721a76b7.../7d04ea99.../05a82c2c.../ba24c5e4.../79f98d8b.../c7169cae.../62b45226.../4ec3a088...); zero secret-pattern hits in the report commit added lines; untracked residue absent from every commit; 007-m surfaces, 008-g round, and all three seals byte-identical (strategy data-free re-hash v1 4091/4091, v2 4076/4076, v3 4076/4076); round result COMPLETE with the final objective-008 verdict CONDITIONAL (predeclared state; structural-safety evidence only) and the named smallest corrective scope (this round: R1 extension to HTML block-start lines; the xml-fragment class-boundary decision D1-5; the display-dollar adjacency guard; the T6 clean-URL admission refinement; the new sealed v4 hidden set); D1-3 CARRIED, D1-4 CARRIED, 008-g D1-1 CARRIED, no CRIT (CRITICAL.md seed-identical a9ea5fa5... at the final head), DHA Decision NONE; response OK frame received (exact 2-byte frame, watch log 2026-09-21 01:20:25 CEST, single consumption). Merge disposition: DO NOT MERGE at 954d758 (a PASS verdict is required for merge; the CONDITIONAL verdict does not satisfy the report predeclared merge precondition); the named corrective scope is executed by this round 008-i; round ACCEPTED as published.",
  "provenance": [
    {"kind": "H", "reference": "Human research decision 2026-09-17 (objective-008 strengthening): a material defect revealed by the hidden set uses normal Concentrated-OAP corrective sequencing with the hidden set's evidential status explicitly downgraded and a new independent hidden set generated and sealed after fixes; the naturalistic population stays the 70 labeled cases with consistency re-run against existing labels and re-adjudication only if a label must change; predeclared PASS/CONDITIONAL/FAIL decision states govern the final objective-008 conclusion; D0/D1 resolved by strategy; owner is not a terminal relay. Human instruction 2026-09-18/19/20 (current): keep the loop moving through implementation and independent structural acceptance; all four required checks genuinely green at the reviewed final head; no weakening/skipping/redefining any check; no manufactured acceptance. 2026-09-17 human architecture decision: parser first, then parser-approved Text spans, then a narrow residual semantic recognizer on the named machine-significant categories only; no ever-growing regex grammar over the complete raw document; prefer real syntax validators for structured data where practical. 2026-09-20 human note: the 007-lineage qwen3.8-27b generation endpoint configuration (Maelstrom1/Neumann, responses wire API) is provided out-of-band and requires no environment variables; no endpoint value or credential material may appear in any committed artifact."},
    {"kind": "A", "reference": "The 008-h final objective-008 verdict (CONDITIONAL, predeclared) and its named smallest corrective suffix (REPORT-008H.md section 9, RESEARCH-STATE section 20, registry entry 008-h): (1) extend the R1 composition predicate from HTML closing-tag lines to all HTML block-start lines (opening-tag lines included); (2) a bounded class-boundary analysis of the 60 B xml-fragment shape (fire the recognizer when the tag name is dialect-recognised but the tag as a whole is not recognised due to non-ASCII attributes, or document the class boundary with the measured evidence if the trigger refinement is deemed out of scope) and of the 26 B display-dollar shape (pairing across malformed components; a bounded malformed-family composition guard or a documented class); (3) the T6 link-destination admission/label refinement (the disclosed pre-existing observation). Structural-safety-only in every item; no residual-grammar growth; objective 009 untouched. S-REVIEW-01, S-MERGE-01 (merge remains a separate post-review strategic act and requires a PASS verdict), S-ORDER-02/03 (corrective suffix preserves branch and PR), S-EVIDENCE-01 (data-free public artifacts; a report is a claim until independently checked), S-ICA-01/02 (structural-safety evidence is NOT linguistic acceptance), S-DECIDE-02 (D1-5 registered in this order's Governance section; the carried D1-1/D1-3/D1-4 clear only on a final objective-008 PASS on the v4 set)."},
    {"kind": "E", "reference": "008-h final-head committed evidence (REPORT-008H.md; RESEARCH-STATE section 20; registry entry 008-h): v3 hidden safety 364 of 232,816 construction-labeled protected bytes exposed (0.156 percent; target 0) across 5 of 2,000 documents - two 139 B HTML-opening-tag-adjacent fence-absorption shapes (v3h-000713, v3h-001274; family code-cpp), two 30 B xml-fragment non-ASCII-attribute class-boundary shapes (v3h-000625, v3h-001241; family structured-xml), one 26 B display-dollar pairing-across-malformed shape (v3h-001307; family math-display-dollar); exposure byte-identical under the 008-g implementation (the single 008-h curated change reverted) = pre-existing, not a fix regression; all other predeclared fields PASS (coordinates 0/0/0/0; malformed 0; e2e 7/7; determinism identical; dev regression PASS +0.021674 pp within the 1.0 point bound; naturalistic 15/15 ranges resolved with a resolution kind, zero unresolved ranges, 0 label corrections; 89 generation HTTP attempts = budget, 0 linguistic-pipeline calls, 0 objective-009 touches); v3 set: 345 components / 2000 documents / 2000 labels, sealed 4076/4076, zero hash overlap vs dev(641)/v1(588)/v2(340), strategy seal verification pre/post; the bounded pre-existing T6 link-destination observation (whole-region PROTECTED construction label vs non-clean-URL destination; prescan confirmed it did not materialize in the v3 pool)."},
    {"kind": "I", "reference": "Strategy independent final-head review of 008-h (private workorders/008-h-final-head-review-20260920.md, completed this round); the 008-h order (named scope authority) and its report (field-by-field attribution of the 364 B with mechanism, pre-existence proof, bounded T6 observation); the released 008-h builder (sha256 647ecf1f... full hash in the report cited-records table) with R1/R2/R3 composition contract and label_source recording; the frozen v4 policy (sha256 f564d9f8...) and v3 policy (sha256 7ff6646e...); the curated 008-h implementation (sha256 a89f17f8...; single delta vs 008-g = EXTEND trigger name pattern RE_XML_NAME); the v3 manifest (sha256 ee503bd7...) and seal verifications; the committed 008-h experiment identity (four-file frozen protection census in experiment-008h.json); the 007-lineage qwen3.8-27b generation deployment record (endpoint/credential out-of-band); the strategy in-round verifiers (strat-verify-tmp/ data-free: seal verification, diffscope with the 008-h released-from-freeze list - the 008-i list in this order's local_work field supersedes it for this round)."}
  ],
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514",
    "oap/governance/DISTILLATION-MAP.md": "a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7",
    "oap/governance/WORKSPACE-LAYOUT.json": "cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254",
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "lr": ["LR-001", "LR-003", "LR-007", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Corrective round 3 of objective 008 (pulldown-cmark 0.13.4 prose-boundary
qualification). Round 008-h executed the 008-g named scope to closure and
returned the predeclared CONDITIONAL verdict on the v3 hidden set: 364 B of
232,816 construction-labeled protected bytes (0.156 percent) across 5 of 2,000
documents, three named bounded mechanism shapes, byte-identical under the
008-g implementation (pre-existing). This order executes exactly the 008-h
named smallest corrective suffix (REPORT-008H.md section 9) and returns a new
final objective-008 verdict on a NEW independent sealed v4 hidden set, per the
2026-09-17 human decision. Structural-safety-only in every item; no
residual-grammar growth; objective 009 untouched.

## Provenance

- H: as metadata provenance H (2026-09-17 human hidden-set and architecture
  decisions; current loop instructions; 2026-09-20 out-of-band generation
  endpoint note).
- A: as metadata provenance A (the 008-h named corrective suffix is the scope
  authority; S-MERGE-01 merge precondition = PASS verdict).
- E: as metadata provenance E (008-h committed evidence at the final head).
- I: as metadata provenance I (strategy final-head review of 008-h; the 008-h
  order and report; frozen policies v3/v4; released builder; v3 manifest and
  seals; experiment-008h.json frozen protection census; strategy in-round
  verifiers).

## Current verified state

Refreshed at publication (2026-09-21): PR #9 OPEN / UNMERGED / auto-merge
DISABLED, head 954d758b0d6308ce1811bccb25ab7d347ad99b7c (the 008-h final
head); main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 (OAP_ACCEPTED_REF)
unchanged; check_state (remote scope) = REVIEW_READY for 008-h; CRITICAL.md
seed-identical (a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e),
zero entries; registry 32 entries; oap/active = 008-h (this order activates
008-i); v1/v2/v3 private roots sealed, strategy data-free re-hash VERIFIED
(v1 4091/4091, v2 4076/4076, v3 4076/4076, receipts
strat-verify-tmp/v3seal-result-pre-20260920-211915.json and
v3seal-result-post-20260920-214519.json); 008-h report committed and
remotely verified (verify_report scope remote = verified; report_count 52).
The 008-h final-head review is COMPLETE
(workorders/008-h-final-head-review-20260920.md).

## Governance

The sixteen source identities in the metadata governance mapping are the exact
identities of `oap/governance/MANIFEST.json` at the 008-h final head
954d758b0d6308ce1811bccb25ab7d347ad99b7c; strategy re-verified all sixteen
field-by-field against the final-head blobs on 2026-09-21 by independent
re-computation from git blobs. One order-file transcription error (a digit
transposition in the ARCHITECTURE-for-agents.md hash) was detected against the
final-head manifest/blob and corrected; all sixteen now match the final-head
mapping exactly. Any future mismatch blocks publication.

### Carried judgment debt (no new debt created by this section)

- 008-g D1-1 (fix mechanism for the mid-document raw-block defect): CARRIED.
  Clears only on a final objective-008 PASS on the v4 set.
- 008-h D1-3 (composition-contract fix mechanism): CARRIED. The 008-h fix
  validated its ordered closing-tag shape (zero v3 occurrences of the 35 B
  shape); the new opening-tag shape is the subject of Scope item 3. Clears only
  on a final objective-008 PASS on the v4 set.
- 008-h D1-4 (final-round acceptance-criteria design): CARRIED. The v4 round
  reuses the design (8-field verdict table, predeclared states, label-source
  split, per-case naturalistic resolution). Clears only on a final objective-008
  PASS on the v4 set with the resolution aggregate committed.

### D1-5: xml-fragment class-boundary decision (bounded trigger refinement vs documented boundary)

Dilemma: the 60 B v3 shape (two 30 B documents, family structured-xml) arises
because the frozen xml-fragment residual class triggers on tag NAME
membership in the dialect vocabulary, while the dialect's inline-HTML rule
recognises a tag as a whole only with ASCII attribute names; a tag with a
dialect-vocabulary name and a non-ASCII attribute name is therefore neither
recognised inline (its bytes become candidate prose) nor covered by the class
(which abstains). The 008-h report names two materially different
alternatives: (a) a bounded trigger refinement - fire the xml-fragment class
when the tag name is in the dialect vocabulary but the tag as a whole fails
inline recognition solely because of non-ASCII attribute names; or (b) no
trigger change, with the class boundary documented in policy v5 as a measured
dialect limitation (the 30 B shapes remain a bounded residual, forcing at
least a further CONDITIONAL round on any pool that composes them).

Governing authority: the 2026-09-17 human architecture decision (parser first;
narrow residual recognizers on the named machine-significant categories only;
no ever-growing regex grammar; prefer real syntax validators) and the 2026-09-17
human hidden-set decision (new independent sealed set after fixes; predeclared
decision states govern). The xml-fragment class is one of the named
machine-significant categories (structured-XML fragments); refining WHEN the
existing class fires - gated on the exact measured condition - is within the
named class, not grammar growth.

Evidence: REPORT-008H.md field-by-field attribution (shape 2, both documents,
exact byte split 18+10+2, mechanism); the frozen v3/v4 policy residual_layer
and the 008-h curated trigger decision precedent (RE_XML_NAME EXTEND, whose
byte-identical effect on the five documents proved trigger-scope sensitivity
is measurable and bounded); the v2-parity guard history (the class abstains
deliberately for non-vocabulary names - that abstention must be preserved).

Alternatives compared: (a) refinement - converges the objective (the shape
cannot recur as exposure on a pool that composes it), blast radius bounded to
one class trigger predicate, fully reversible (policy v5 is a new file; the
curated delta is a single trigger condition, same pattern as the 008-h single
curated change); (b) documented boundary - zero implementation risk but
guarantees the shape remains a residual wherever composed, prolonging the
objective by at least one more corrective round with a new hidden set.

Stage suitability / reversibility / blast radius: DEMONSTRATOR phase,
research-only, no product behavior change; both alternatives revert by
re-adopting the prior policy file; (a)'s behavioral surface is exactly the
one measured shape family, policed by the focused tests of Scope item 3 and
the dev regression gate of Scope item 6 before any v4 generation.

DECISION (predeclared, executed as a documented choice per the 008-h item-4
pattern): PRIMARY = (a) bounded trigger refinement, implemented as
EXTEND-IF-EVIDENCED: after the dev regression gate (Scope item 6), coding
commits the refinement iff BOTH hold - zero new safety exposures on the dev
corpus (3,000 documents), the 008-g dev batch, the 008-h dev-edge batch, and
the new 008-i dev-edge batch; and the focused positive/negative tests of
Scope item 3 pass (class fires on the measured shape; class still abstains on
a non-vocabulary tag name with non-ASCII attributes - the v2-parity guard is
preserved; no change on any dev document). Otherwise FALLBACK = (b): no
curated change, the class boundary documented in structural-policy-v5.json as
a measured dialect limitation with the v3 evidence cited, disclosed in
REPORT-008I.md; the v4 round proceeds and the predeclared verdict states
handle the residual (CONDITIONAL if only documented bounded residuals remain).
The chosen branch and its committed evidence are recorded in REPORT-008I.md
and the generation identity.

Strongest counterargument: refining the trigger on attribute-name shape is
exactly the kind of dialect-condition accretion the human architecture
decision warned against, and a future non-ASCII-NAME / ASCII-ATTRIBUTE mirror
shape could reopen the same discussion; the contained answer is that the
refinement is gated to the exact measured condition (vocabulary name +
non-ASCII attribute name), preserves the vocabulary abstention, is one
revertible predicate, and the FALLBACK branch exists precisely if the evidence
does not cleanly support it.

Judgment debt registered: D1-5 (this dilemma; provisional choice = PRIMARY
branch predeclared with the committed-evidence gate and FALLBACK). Clears on a
final objective-008 PASS on the v4 set (which includes proof the refinement -
if taken - did not over-suppress: dev regression field vi and the focused
negative tests).

### DHA

Deferred human adjudication: Decision: NONE (expected; no new CRIT is
anticipated - the four scope items are either predeclared decisions or bounded
documented classes; if a CRIT becomes genuinely necessary during
implementation, the coding agent reports the candidate and the first
correction commits safe prerequisites only, then the same-PR correction
appends the canonical entry before the provisional choice is introduced;
S-DHA-01/02).

## Goal and dependencies

Execute the 008-h named smallest corrective suffix to closure -
(1) R1 composition predicate extended to all HTML block-start lines (opening-
tag lines included) so the 278 B absorption shape cannot be composed into the
next pool; (2) the bounded xml-fragment class-boundary decision (D1-5) and the
26 B display-dollar shape's bounded malformed-family composition guard;
(3) the T6 link-destination admission refinement (the disclosed pre-existing
observation) - then generate, seal (strategy pre-gated), and evaluate a NEW
independent v4 hidden acceptance set, and return the final objective-008
verdict under the predeclared decision states. Dependencies: 008-h final head
(verified); nothing else outstanding.

## Scope

1. Pre-work integrity gates (requirement 1): frozen-surface byte-identity at
   the 008-h final head (007-m linguistic surfaces; annotation guide; all
   tests; workflows; orders/reports; the 008-d quarantine record; v1/v2/v3
   manifests and seal verifications re-hashed data-free, no re-evaluation of
   any spent set; the committed corpus including all 008-h additions); registry
   at 32 entries; the strategy in-round seal re-verification of all three
   committed seals (data-free) before the round starts. Any mismatch =
   BLOCKED, report, stop.

2. Data-restricted shape analysis (requirement 2): using the private v3
   evaluation records (never committed content), produce the committed
   data-free analysis of the three v3 exposure shapes and the T6 observation
   (mechanism, byte split, template/family, pre-existence proof reference) as
   the fix specification input; committed BEFORE any implementation change.

3. Policy v5 and bounded implementation (requirement 3), on the released
   surfaces ONLY:
   (a) R1 EXTENSION: the R1 composition predicate fires for ALL HTML
       block-start lines (opening-tag lines included), not only closing-tag
       lines; on fire, insert the NEUTRAL-labeled barrier exactly as the
       released closing-tag rule does; builder asserts the invariant (a fenced
       or indented code component is never composed on the line following an
       HTML block-start line without a neutral barrier); the 008-g closing-tag
       behavior and the 008-h R1/R2/R3 contract otherwise stay intact.
   (b) DISPLAY-DOLLAR ADJACENCY GUARD: a malformed-incomplete-display-dollar
       component (unterminated `$$` opener) must not be composed immediately
       before a component whose first line opens a display-dollar expression;
       predeclared barrier mechanism = one NEUTRAL-labeled blank line (the
       builder may substitute a different NEUTRAL-labeled barrier iff the
       focused test proves the blank line does not break the pairing, and the
       substitution is disclosed in the generation identity and REPORT-008I.md);
       NO new TeX-command residual class (the 008-g spec stays: paren/bracket/
       env only) - a residual-grammar addition is out of scope.
   (c) T6 ADMISSION REFINEMENT: in the v4 pool, T6 link-destination fragments
       must be clean URLs (the pre-seal smoke set confirmed the v3 pool's
       machine-urls are clean URLs; the admission rule makes that invariant
       explicit and builder-asserted); already-committed dev documents with
       non-clean T6 destinations are NOT re-labeled (dev data stays frozen;
       the whole-region PROTECTED construction label vs inter-token space
       behaviour is documented in structural-policy-v5.json as a measured
       observation with the v3 prescan cited, not as a class).
   (d) structural-policy-v5.json (NEW file): carries (a)-(c) where policy-
       expressible, the D1-5 outcome (refinement or documented boundary, with
       the v3 evidence cited), and the frozen protection identity for this
       round = the four-file census recorded in experiment-008i.json; v4 and
       v3 policies stay byte-identical in-tree.
   (e) experiment-008i.json (NEW): the 008-i round identity (census, seed,
       budget, decision record). generation-identity-008i.json (NEW) is
       written during generation (Scope item 7).

4. Predeclared xml-fragment trigger decision D1-5 (requirement 4): execute the
   Governance D1-5 EXTEND-IF-EVIDENCED / FALLBACK decision exactly as
   registered, after the dev regression gate (Scope item 6); on EXTEND the
   curated delta is the single trigger condition and nothing else; on
   FALLBACK research/curated/prose_boundary.py is NOT modified; the chosen
   branch and evidence are committed in REPORT-008I.md and recorded in
   experiment-008i.json.

5. Dev dialect-edge batch (requirement 5): commit
   research/prose-boundary/corpus/defect-dev-008i/ - machine-known-label dev
   documents covering exactly the four fixed/refined shapes: (i) HTML
   opening-tag line followed by a fenced code component (the 278 B family);
   (ii) single-line multi-tag XML line with a vocabulary-name tag carrying a
   non-ASCII attribute name (the 60 B family); (iii) malformed
   incomplete-display-dollar immediately before a complete display-dollar
   component (the 26 B family); (iv) T6 link with a non-clean-URL destination
   (the disclosed observation; retained as a NEUTRAL-split label document).
   Labels are machine-known (construction), content-free manifest committed,
   raw content stays private.

6. Dev regression gate (requirement 6), committed BEFORE any v4 generation:
   scripts/verify_development_baseline.py over the 3,000-document dev corpus +
   008-g dev batch + 008-h dev-edge batch + the new 008-i dev-edge batch;
   predeclared bounds: zero new safety exposures (construction-labeled
   protected bytes exposed = 0 on all dev material); prose over-suppression
   delta within the 1.0 percentage-point bound (008-h precedent
   +0.021674 pp); all dev invariants pass. The gate output commits as the
   D1-5 evidence input (item 4) and the round's regression record.

7. New hidden acceptance set v4 (requirement 7): generate a NEW independent
   v4 set with a fresh generation stream: 007-lineage qwen3.8-27b identity
   (endpoint/credential out-of-band; NO endpoint value or credential material
   in any committed artifact), fresh PRNG seed (recorded in
   generation-identity-008i.json; different from dd1a19a598160b36), the same
   76 families and density plan (base 4/family; densified 16 for the
   densified families) as v3, 345 nominal component slots, 2,000 deterministic
   mashup documents under the 008-i builder (all three guards active), 2,000
   construction labels with the label_source split; budget: at most 96 HTTP
   attempts total including preflights, retries, and bounded recovery
   (008-h precedent 87+1+4=89); zero linguistic-pipeline model calls; zero
   objective-009 touches. Independence: zero exact hash overlap asserted and
   disclosed against the dev (641), v1 (588), v2 (340), and v3 (345) pools
   (hash-only, data-free); bounded zero-overlap recovery allowed per the 008-g
   / 008-h precedent with every discarded duplicate disclosed. Pre-seal dev
   diagnostic: run the frozen 008-i protection over the built v4 set BEFORE
   sealing and record the result in the generation identity - predeclared
   primary case = zero occurrences of the three v3 exposure shapes (guards
   prevent them); if any shape occurs anyway, the set is STILL sealed and
   evaluated as-is (the exposure is a verdict input, not a BLOCKED trigger;
   a mid-round implementation change would break the frozen protection
   identity with no ordered re-freeze path - the 008-h precedent), with the
   occurrence disclosed. Seal the v4 private root (76 component files + 2,000
   document files + 2,000 label files = 4,076 files expected) with the sealed
   manifest; strategy's independent data-free seal verification (pre phase)
   MUST pass before the evaluation phase begins - the evaluation harness
   takes the strategy verification receipt as an input (gate enforced in
   tool, 008-h precedent).

8. Naturalistic consistency re-run (requirement 8): with the frozen 70
   labeled naturalistic cases (labels frozen; re-adjudication ONLY if a label
   must change - the narrow 2026-09-17 human path), re-run consistency under
   the 008-i implementation (naturalistic_consistency_v4.py); predeclared
   expectation: 0 UNRESOLVED, 0 label corrections; every material case (the
   008-g five and the 008-h 15-range resolution aggregate) carries its
   resolution kind.

9. Implementation freeze and v4 hidden evaluation (requirement 9): freeze
   the 008-i implementation (experiment-008i.json census) before evaluation;
   run the full v4 acceptance battery (hidden_acceptance_v4.py): hard safety
   axis (construction-labeled protected bytes exposed, target 0, with
   byte-level attribution for any nonzero result), the four coordinate axes
   (target 0/0/0/0), malformed behaviour (0 violations), e2e invariants 1-7
   on the full 2,000-document replay, determinism (50-case re-run, identical
   output), seal re-hashes pre/post evaluation (v4 + all committed seals),
   model-call accounting (distinct categories). Post-evaluation strategy
   data-free seal re-verification is strategy's recorded in-round duty.

10. Final objective-008 verdict (requirement 10): apply the predeclared
    decision states to the NEW evidence (v4 hidden set + naturalistic
    per-case resolution + dev regression) with the 8-field table:
    (i) v4 construction-labeled protected bytes exposed = 0;
    (ii) coordinates 0/0/0/0; (iii) malformed behaviour 0 violations;
    (iv) e2e invariants 1-7 all PASS on the v4 set; (v) determinism identical
    (50-case re-run); (vi) dev regression PASS (zero new safety exposures;
    over-suppression within the 1.0 point bound); (vii) every material
    naturalistic range resolved (no UNRESOLVED; the 008-g five material cases
    each carry a resolution kind); (viii) zero model calls beyond the recorded
    v4 generation budget; zero linguistic-pipeline calls; zero objective-009
    touches.
    PASS = all eight fields pass. CONDITIONAL = all fields pass except that
    only bounded, clearly understood defects remain (each named and bounded,
    smallest corrective suffix named). FAIL = materially enough
    machine-significant exposure, or an invariant/determinism/regression
    failure, that the parser-first design cannot be trusted at this stage.
    The verdict is structural-safety evidence only (S-ICA-01/02). MERGE
    PRECONDITION (predeclared, 008-h precedent): a PASS verdict is required
    for any merge of PR #9; CONDITIONAL or FAIL = DO NOT MERGE, round
    ACCEPTED as published (if COMPLETE), named corrective suffix for the
    next round. On the (non-occurring) PASS branch: the objective-008
    protection layer is declared FROZEN at the 008-i census (frozen
    protection identity = the four-file census in experiment-008i.json;
    policy of record = v5); that declaration is made ONLY in the final PASS
    report, never by this order, and grants no release/deployment authority.

11. Ledger and state bookkeeping (requirement 11): (a) one 008-i entry
    appended to research/registry/experiments.json (registry 32 -> 33);
    (b) RESEARCH-STATE.md additive section 21 (final verdict, D1 status,
    carried debt) + machine block (registry count, reports-reviewed counter
    51 -> 52, quarantines byte-unchanged); (c) STATUS.md verdict sentences;
    (d) oap/GENERATED-FILES.json scoped pin; (e) research/tables/
    experiment-summary.csv rebuild.

12. Report-only final commit (requirement 12): sole parent = literal
    bookkeeping head; sole changed path
    oap/reports/008-i-corrective-scope-and-v4-final-blind-acceptance.md (the 008-e pre-push validity procedure:
    the report is a claim; it must not assert push/CI success before those
    occur; REPORT-008I.md research record is committed in the implementation
    commits, the OAP report in this commit only).

13. Final-head CI (requirement 13): all four required checks green at the
    final head (Application baseline; Research reproducibility; OAP bootstrap
    acceptance; OAP report history); the current check state at report time
    is disclosed verbatim (predeclared re-run state if a check is still
    running).

14. Send exact response OK after remote verification and stop. PR #9 stays
    OPEN; no merge; no auto-merge; no further rounds without a new order.

15. CI-1 per-command budget line (owner-selected Option A1, recorded
    2026-09-22 18:24 CEST; extends requirement 13): modify
    .github/workflows/application-baseline.yml EXACTLY at line 35 (at the
    008-h final head) by appending ' --command-timeout 600' to the driver
    invocation, in the FIRST implementation commit of the round, so that
    every CI run of this round (including the final head) uses the 600 s
    per-command cap. No other workflow, driver, test, or configuration
    change; scripts/verify_development_baseline.py stays byte-identical
    (300.0 default preserved); the workflow's existing outer job timeout is
    unchanged; the amended workflow file is pinned: sha256
    4490d0fc9e9fcd3eb697b1721b385f986f1a232372593618501dc0ed0918bc4c (git
    blob b2bf32dfb9f25f74761d5a6f1a33c44c48869789, 1687 B). Recorded
    observation (OUT OF SCOPE for this round - no action taken here): the
    driver's timeout path kills the immediate subprocess rather than
    demonstrably the complete descendant process tree; the CI logs show
    pytest completing successfully shortly after the nominal 300 s timeout,
    indicating separate harness-hardening debt for a future bounded order.

## Non-goals

- No 007-m linguistic surface change (config, prompt, final-root manifest).
- No objective-009 touch of any kind (the future 009 sample must not contain
  any case generated or inspected for objective 008, including every v1/v2/
  v3/v4 component, mashup, naturalistic case, dev document, dev batch, and
  dev-edge document).
- No linguistic-pipeline model calls; no linguistic quality claims.
- No residual-grammar growth beyond the predeclared D1-5 primary branch
  (single trigger condition); no new TeX-command class; no class additions.
- No re-labeling of any committed dev document; no re-evaluation of any spent
  hidden set (v1/v2/v3 seals: re-hash only).
- No deployment, no release, no milestone claim, no service activation.
- No endpoint values, credentials, private paths, or raw document/label
  content in any committed artifact (data-free posture).
- No changes to workflows, test infrastructure outside the one new focused
  test file, or any path outside the released-from-freeze list.

## Files and boundaries

Inspect: the 008-h final head tree (read), the private v3 evaluation records
(read, data-free only), the v4 private root (created under the same private
research-runtime root pattern as 008h-hidden: the new directory
008i-hidden under the round's private research runtime root), the 008-g/008-h
dev batches (read). Write: exactly the released-from-freeze list in the
metadata local_work field. Inspect boundary for coding: the coding read set
is the compact sources, this order, and the named data-free records; full
PLAN/architecture/strategic sources are NOT required by this order. The
strategy in-round verifiers (strat-verify-tmp/) are strategy-private; the
008-i diffscope released list = this order's local_work released field.

## Requirements

1. Pre-work integrity gates per Scope item 1 (frozen-surface byte-identity at
   the 008-h final head; all three committed seals re-hashed data-free;
   registry 32; any mismatch = BLOCKED).
2. Data-restricted shape analysis per Scope item 2 (committed data-free fix
   specification input, before any implementation change).
3. Policy v5 and bounded implementation per Scope item 3 (v4/v3 byte-
   identical in-tree; builder guards asserted; no residual-grammar growth
   beyond D1-5 primary).
4. D1-5 trigger decision per Scope item 4 (EXTEND-IF-EVIDENCED or FALLBACK
   with the committed evidence, after the dev regression gate; curated delta
   exactly one trigger condition or zero).
5. Dev-edge batch per Scope item 5 (committed; machine-known labels; four
   shapes; content-free manifest).
6. Dev regression gate per Scope item 6 (committed before any v4 generation;
   zero new safety exposures; over-suppression within bound).
7. New hidden set v4 per Scope item 7 (independent stream; fresh seed;
   zero hash overlap vs dev/v1/v2/v3 disclosed; pre-seal diagnostic recorded
   with the predeclared as-is sealing rule; sealed; strategy pre-gate
   receipt accepted by the evaluation harness before any evaluation).
8. Naturalistic consistency re-run per Scope item 8 (committed; 70 frozen
   cases; 0 UNRESOLVED expected; re-adjudication only on the narrow human
   path).
9. Implementation freeze and v4 evaluation per Scope item 9 (new
   hidden_acceptance_v4.py; all axes; 50-case determinism; seal re-hashes
   pre/post; distinct model-call accounting).
10. Final verdict per Scope item 10 (predeclared states only; field-by-field
    table; structural-safety-only classification; merge precondition PASS).
11. Bookkeeping per Scope item 11 (registry 32 -> 33; machine block
    reports-reviewed 51 -> 52; quarantines unchanged).
12. Report-only commit per Scope item 12 (the 008-e pre-push validity
    procedure; sole path; sole parent).
13. Final-head CI per Scope item 13 (four green or predeclared re-run state
    disclosed verbatim); plus owner Option A1 (recorded 2026-09-22 18:24
    CEST): CI-1 (Scope item 15) is applied in the FIRST implementation
    commit of the round; the final-head Application baseline must run under
    the 600 s cap and be GENUINELY green; if it is NOT green (any failure
    or timeout), STOP and report with the per-command JSON - no further
    reruns, no further cap changes, no executor-side scope change.
14. Send exact response OK after remote verification and stop. PR #9 stays
    open; no merge.

## Acceptance criteria

1. Pre-work gates PASS with committed evidence; any mismatch would have
   BLOCKED (none reported).
2. The data-free shape analysis commits before the first implementation
   commit (git ordering proves it).
3. structural-policy-v4.json and v3 remain byte-identical in the final diff;
   policy v5 and experiment-008i.json are new files; the builder diff is
   limited to the three guards + assertions + recording; no path outside the
   released list changed.
4. D1-5 branch committed with evidence: on EXTEND, the single curated trigger
   condition diff + focused positive/negative tests + zero new dev
   exposures; on FALLBACK, zero curated diff + the documented boundary in
   policy v5 with the v3 evidence cited.
5. The dev regression gate commits before any v4 generation commit (git
   ordering); zero new safety exposures; over-suppression delta within the
   1.0 point bound; all dev invariants pass.
6. The v4 generation identity commits with: fresh seed distinct from the v3
   seed; budget accounting at or under 96 attempts; zero linguistic-pipeline
   calls; zero objective-009 touches; zero-overlap assertion vs dev/v1/v2/
   v3 with any recovery disclosed; the pre-seal diagnostic result recorded.
7. The v4 seal manifest and verification commit; the strategy pre-gate
   receipt is accepted by the evaluation harness (the harness refuses to
   run without it); post-evaluation seal re-hashes match.
8. The naturalistic re-run commits with 0 UNRESOLVED (expected) and every
   material case carrying a resolution kind; any label correction would have
   taken the narrow re-adjudication path and would be disclosed.
9. The v4 acceptance battery commits with all axes reported distinctly
   (PASSED/FAILED counts, not prose-only); any nonzero construction exposure
   carries byte-level field-by-field attribution with mechanism and
   pre-existence check.
10. The final verdict table commits with exactly the 8 predeclared fields,
    a single predeclared state, the structural-safety-only classification,
    and (on PASS) the FROZEN declaration at the 008-i census - or (on
    CONDITIONAL) the named smallest corrective suffix; no state outside the
    predeclared set is used.
11. The report-only commit is the sole changed path with sole parent =
    bookkeeping head; the full round diff (base..final) is limited to the
    released list; zero secret-pattern hits in added lines; untracked
    residue absent from every commit.
12. All four required checks green at the final head (or the predeclared
    re-run state disclosed verbatim at report time, resolved before
    strategy's final-head review); response OK frame received after remote
    verification.
13. CI-1 pinned bytes at the final head: .github/workflows/
    application-baseline.yml sha256 =
    4490d0fc9e9fcd3eb697b1721b385f986f1a232372593618501dc0ed0918bc4c (git
    blob b2bf32dfb9f25f74761d5a6f1a33c44c48869789, 1687 B); scripts/
    verify_development_baseline.py byte-identical to the 008-h final head
    (sha256 3604eb6dd92d2fb47f2993bd9e931a11b1701970867367170738ee6e6fe6c818);
    every other workflow file byte-identical to the base.

## Verification

- Focused: the new focused test file research/tests/
  test_008i_composition_and_class_boundary.py - positive (the opening-
  tag-line + fenced-code composition fires R1 with a NEUTRAL barrier and
  zero exposed protected bytes on the shape fixture; the xml-fragment
  class fires on the measured non-ASCII-attribute shape under the EXTEND
  branch / is classified per the documented boundary under the FALLBACK
  branch; the display-dollar adjacency fires the guard with the NEUTRAL
  barrier and zero exposed TeX-command bytes; the T6 clean-URL admission
  assert passes on clean fragments) and negative (the 008-g/008-h closing-
  tag R1 fixtures unchanged; R2/R3 predicates unchanged; the xml-fragment
  class still ABSTAINS on a non-vocabulary tag name with non-ASCII
  attributes - the v2-parity guard preserved; the guard does not fire for
  a complete display-dollar component not adjacent to a malformed opener,
  nor for a malformed opener not followed by a complete component; no new
  over-suppression on any committed dev fixture - the dev regression gate
  is the corpus-level negative proof), the 008-i dev-edge batch metrics,
  the dev regression gate (committed before any v4 generation), the v4
  seal re-hashes (pre- and post-evaluation) plus the strategy data-free
  seal verification (v4 primary pre-gate feeding the evaluation harness;
  post --all-seals v1/v2/v3), the instance-level zero-overlap check (v4
  vs v3/v2/v1/dev, recomputed hashes), the label-source split
  recomputation on a bounded v4 sample, the harness determinism re-run
  stability check (50-case), the e2e invariant re-derivation on a bounded
  v4 sample, verify_report and check_transcript (pre-push and remote),
  report history, scoped inventory/drift, the 007-o consistency test, the
  publication-guard data-free scan.
- Broader: full research suite with the pinned helper (the v4 results are
  data-free aggregates - the suite does not read the private root), the
  OAP suite, one full local Application-baseline driver run (per-stage
  durations, local evidence only), the full CI battery at the
  implementation head and the final head.
- Evidence boundary: software/test layer (focused tests, dev regression,
  CI); data layer (the v4 sealed set - content-free manifests and
  committed data-free aggregates only); model layer (v4 generation
  attempts counted and categorized; no live-product claims). The report
  is a claim until strategy's independent final-head review re-verifies
  it field-by-field against the committed data-free records (S-EVIDENCE-
  01, S-REVIEW-01). A report written before its push cannot claim push/
  CI success.

## Local setup and constraints

- CPU-only plus the pinned Rust helper (sha256
  5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf) and
  the frozen uv environment; the v1/v2/v3 private roots (seal re-hashes
  only) and the new v4 private root (generation, seal, harness-only
  evaluation reads); no GPU, no new dependencies, no service touches; no
  protected Qwen weight/config/network change (S-PRODUCT-04).
- Authorized model use in this round, each recorded, counted, and
  classified distinctly: component generation for the v4 set ONLY
  (authorized test-data generation; the 007-lineage qwen3.8-27b
  deployment identity with endpoint/credential configured out-of-band per
  the 2026-09-20 human note - no environment variables required; no
  endpoint value or credential material in any committed artifact);
  budget at most 96 HTTP attempts total including preflights, retries,
  and bounded recovery; zero linguistic-pipeline model calls; zero
  objective-009 touches of any kind. No other model calls of any kind.
- Privacy: no raw customer text anywhere; no endpoint values,
  credentials, or private paths in any committed artifact, log, or
  report; the v4 set and all labels remain in the private root (counts/
  categories/hashes only in public artifacts); the shape analysis output
  is data-free; evaluation data is synthetic generated test data under
  the 007-lineage record (the 2026-09-17 human decision authorizes the
  hidden-set methodology; storage stays in the private root).
- Local: reversible setup inside the authorized workspace only; doctor
  runs with env -u CODEX_HOME -u OAP_ROLE; any setup failure that cannot
  be resolved reversibly inside the workspace is BLOCKED and reported,
  not worked around.

## Documentation

REPORT-008I.md (committed in the implementation commits): cited-records
table (sha256), pre-work gate results, data-free shape analysis, the three
guards' implementation record, the D1-5 branch + evidence, dev-edge batch,
dev regression gate, v4 generation identity summary, seal verifications,
v4 acceptance metrics with field-by-field attribution for any nonzero axis,
naturalistic re-run, model-call accounting, final verdict table,
structural-safety-only classification, D1 debt status, limitations.
RESEARCH-STATE.md section 21 + STATUS.md per Scope item 11.

## Git and report publication

- Activation commit (order + oap/active) per the round mechanics;
  implementation/evaluation commits per Scope items 2-10 (exact split at
  the executor's discretion, all within the released-from-freeze list);
  report-only commit per Scope item 12 (sole parent = literal
  implementation head; sole changed path oap/reports/008-i-corrective-
  scope-and-v4-final-blind-acceptance.md).
- Push semantics per the OAP communication profile; no force-push; no
  push after the report-only commit (C-REPORT-01); exact response OK
  after remote verification; the coding wrapper consumes the 008-i
  control signal exactly once before model launch.
- No merge: PR #9 stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act and requires a PASS verdict on the
  v4 set (S-MERGE-01; repository-approved method: standard merge commit
  at the exact reviewed SHA, --verify-merge, default-branch check).

## Decision classification

D0 for the round execution (bounded corrective implementation and
evaluation inside the risk budget, executing the 008-h named scope and
the 2026-09-17 human decision). One new D1 registration in the
Governance section (D1-5: the xml-fragment class-boundary decision -
bounded trigger refinement vs documented boundary - predeclared with the
committed-evidence choice gate and fallback, full S-DECIDE-02 record).
The carried-forward 008-g D1-1, 008-h D1-3, and 008-h D1-4 are recorded
in the Governance section and clear only on a final objective-008 PASS on
the v4 set. No CRIT admission anticipated (all five S-DECIDE-03
conditions fail at condition 1 for the expected round); if a CRIT
becomes genuinely necessary, coding reports the candidate only, the
first correction commits safe prerequisites, and the same-PR correction
appends the canonical entry before the provisional choice is introduced
(S-DHA-01/02).

## Deferred human adjudication

- Decision: NONE

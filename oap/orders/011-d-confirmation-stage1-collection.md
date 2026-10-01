# 011-d: Stage-1 collection for the development-distribution re-measurement on the designated A100-FP8 target (objective 011, round 4; owner-directed DASSLE mechanical-assembly intake per PROTOCOL-009-REVISION-011; identity re-verified at 011-c; PR #12 held open)

Status: FINAL. Strategy's independent 011-c final-head review is PASS
on record (private workorders/011-c-final-head-review-20261001.md);
the owner's 2026-10-01 DASSLE directive (private decision receipt
workorders/dassle-reuse-decision-20261001.md) closes the intake
boundary, so no human input is pending for this round. The study is
reclassified to a development-distribution re-measurement per
PROTOCOL-009-REVISION-011 (registered byte-exact in Scope item 3f;
PROTOCOL-009.md stays byte-frozen).

## Continuity and adaptation note (011-b -> 011-d; bounded, recorded)

This order re-executes the published 011-b stage-1 collection
specification (oap/orders/011-b-confirmation-stage1-collection.md,
sha256 0456004c0136ec0de9e3732b3d76ddd343d9124730a865fa7e946182a3105627,
byte-preserved at the base) VERBATIM for Scope items 4-8 (manifest,
selection, split/pilot, generation, annotation guide and packets),
with Scope item 3 REPLACED (intake gate -> DASSLE source
verification + mechanical assembly per the owner directive) and the
bounded adaptations below. 011-b was truthfully
BLOCKED at its Scope 2c probe stop BEFORE intake, manifest, selection,
generation, or packet work (its review is PASS), so no collection
artifact of this objective exists yet and the stage-1 collection
executes in this round:

1. Scope 2 (the 011-b E2 prelude: designation record + bounded
   freshness re-probe) is REPLACED by a record-verification prelude:
   the designation record and the canonical-route re-probe already
   exist and are byte-verified in this round (011-b committed
   DEPLOYMENT-IDENTITY-011.md sections 1-5; 011-c appended section 6
   with the REGIME-UNCHANGED verdict). NO metadata probe occurs in
   011-d: the owner's bounded-probe usage constraint (exactly 2
   metadata GETs total, no retries) was designed for and exhausted by
   the pinning work of 011-b/011-c; the PROTOCOL-009 element (a)
   freshness precondition (pinned identity verified before the first
   sample is collected) is satisfied by the 011-c record, which this
   round byte-verifies. The only network calls of this round are the
   scaffold generation calls and the ordered per-document main-capture
   generation calls of Scope 7 (scaffold per the registered class;
   main capture under the frozen 007-m profile).
2. Bookkeeping numbers advance from the 011-c final state: registry
   39 -> 40; machine-block counters registry_entries 39 -> 40,
   oap_reports_reviewed 58 -> 59, frozen_report_history_incidents
   unchanged at 2; RESEARCH-STATE additive section 28 (not 26).
3. The zero-leakage assertion and the sidecar eligibility
   attestation of the 011-b item 3 are SUPERSEDED by the
   authorized-reuse disclosure of PROTOCOL-009-REVISION-011 (owner
   directive; per-document DASSLE record attestation with
   consumption tiers); 011-b and 011-c performed no corpus intake or
   inspection, so the consumption history is exactly as recorded in
   the revision (objective-007 campaign8 + 007-h chain).
4. The BLOCKED-on-input rule no longer carries the escalation duty:
   the single pre-authorized escalation of the item-3b specification
   was consumed by the 011-b round (private record in that round's
   publication receipt) and is NOT repeated.
5. Artifact names and the collection-ID scheme are RETAINED exactly as
   pre-registered in the 011-b order (`011b-<seq:04d>` collection
   IDs, `011b-collection-manifest.json`, private `011b-collection/`,
   `011b-packets/`; `011b-intake/` is NOT used - superseded): the
   deterministic selection
   and the sha256-hex partitions are defined over exactly those IDs,
   and renumbering would alter the pre-registered partition without
   any scientific benefit. The executing round is 011-d; the names
   refer to the pre-registered stage-1 collection specification.
6. The evaluation/score/comparator work belongs to 011-e (not 011-c,
   which became the intervening pinning round); stage-2 expansion, if
   triggered by the pre-registered criteria, belongs to 011-f.
7. OWNER DIRECTIVE (2026-10-01; the three verbatim messages are in
   the metadata H field and the private decision receipt
   workorders/dassle-reuse-decision-20261001.md): the owner-
   supplied-intake model of the 011-b item 3b is SUPERSEDED. The
   stage-1 population is MECHANICALLY ASSEMBLED from the byte-
   verified private DASSLE copy: DASSLE texts VERBATIM plus LLM-
   generated Slovenian technical scaffold sections interleaved
   (seeded PRNG; the LLM outputs scaffold sections ONLY, never a
   "pure Slovenian" source document); the scaffold sections are
   DISCARDED before scoring (the discard map is data-free); the
   DASSLE human reference is the source ground truth; the DASSLE
   corrected texts are the FULLY_CORRECT controls. The study is
   RECLASSIFIED from "fresh target-distribution confirmation" to
   "development-distribution re-measurement" (all DASSLE was
   inspected by objective 007; PLAN section 16 milestone/MVP claims
   remain gated on a genuinely fresh set later). The mechanism is
   registered byte-exact in PROTOCOL-009-REVISION-011 (Scope item
   3f; PROTOCOL-009.md stays byte-frozen; it supersedes (b)/(c)/(e)/
   (g) and the zero-leak assertion of (h) only). The 011-b intake
   escalation is consumed and MOOT (no delivery will come; no re-
   escalation; the intake monitor is terminated at publication).

## Metadata

```oap-metadata
{
  "id": "011-d",
  "title": "Stage-1 collection for the development-distribution re-measurement on the designated A100-FP8 target (objective 011, round 4; owner-directed DASSLE mechanical-assembly intake per PROTOCOL-009-REVISION-011; identity re-verified at 011-c; PR #12 held open)",
  "objective": "011",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "47c4da8bf7016614cd62d2448e72f3f7249d0803",
  "branch": "oap/011-target-distribution-confirmation-study",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 12,
  "dependencies": ["007", "008", "009", "010", "011"],
  "local_work": "Preserve byte-for-byte: the entire objective-000..011-c tree at base 47c4da8bf7016614cd62d2448e72f3f7249d0803, including research/target-distribution/PROTOCOL-009.md (sha256 cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a, FROZEN - the single source of truth for this round; every scientific element below transcribes it, none reopens it), research/target-distribution/DEPLOYMENT-IDENTITY-009.md (sha256 b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4, FROZEN), research/target-distribution/DEPLOYMENT-IDENTITY-011.md (sha256 53cefe8fe451402eff3ffd429083eb87d1fe80733c66b641a05bba20b482e94a; sections 1-6 byte-preserved by this round - this round writes ONLY the two additive registered files research/target-distribution/PROTOCOL-009-REVISION-011.md (sha256 609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43, registered byte-exact in Scope item 3f) and research/target-distribution/SCAFFOLD-GENERATOR-PROMPT-011.md (sha256 005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc, registered byte-exact in Scope item 3f) and NO other research/target-distribution/ bytes; the round reads section 6 as its hard-gate precondition), research/tests/test_009a_protocol_elements.py, all 007-m frozen surfaces (config projection 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, deployment profiles c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), the objective-011-a/011-b/011-c artifacts (oap/orders/011-a-*, oap/reports/011-a-*, oap/orders/011-b-confirmation-stage1-collection.md sha256 0456004c0136ec0de9e3732b3d76ddd343d9124730a865fa7e946182a3105627, oap/reports/011-b-confirmation-stage1-collection.md, oap/orders/011-c-identity-reverification-canonical-routes.md sha256 676279b6d3584dc42a3d4a28a8b06eaf317ae929e20127c00e7768899a99a2c7, oap/reports/011-c-identity-reverification-canonical-routes.md, RESEARCH-STATE sections 25-27, the 011-a/011-b/011-c ledger entries, machine block at main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8 with counters registry_entries 39 / oap_reports_reviewed 58 / frozen_report_history_incidents 2), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, the private research-runtime roots (009a-identity/, 011b-identity/ including the STRATEGY-CORRECTED credentials receipt, 011c-identity/ - all read-only for this round; 011b-collection/, 011b-packets/ as released below; 011b-intake/ is NOT used in this round (superseded by the DASSLE mechanical-assembly model; the directory stays absent); none ever committed), and the private DASSLE source copy (private research-runtime campaign8 datasets location; READ-ONLY for this round; byte-verified per Scope 3a), and any unrelated local work (the three untracked residues corpus/, .research-test-scratch/, .rclone-speed-test/ are pre-existing and never committed).",
  "prior_review": "Strategy independent final-head review of 011-c (2026-10-01, private workorders/011-c-final-head-review-20261001.md): verdict PASS on a COMPLETE round. Verified: verify-report remote scope at the 011-c final head 47c4da8bf7016614cd62d2448e72f3f7249d0803 (report history valid, 59 report files, only the two known frozen 006-a/006-c incidents); report-only commit 47c4da8 with implementation head aa37164ec224e706754106019face57ef238a9f8 as sole parent and the report as sole changed path; round diff (011-b final head f505492..47c4da8) exactly the nine released paths; additive fidelity independently recomputed - DEPLOYMENT-IDENTITY-011.md zero deletions/modifications, byte-prefix identical to the 011-b final head blob (sections 1-5 preserved; final blob sha256 53cefe8fe451402eff3ffd429083eb87d1fe80733c66b641a05bba20b482e94a, 11,209 B); strategy re-ran the consistency suite at the final head: 10/10 PASSED (umask 022, real checkout, live-ref and 007-o-lock green); registry 39 with exactly one new 011-c data-free entry (kind state-correction, status COMPLETE); machine-block counters 39/58/2 with all identity fields byte-unchanged; CRITICAL.md independently hashed at final head/base/seed - all identical at the true 64-character hash a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e (the order-text 72-character pin string in 011-b/011-c is a named transcription artifact, no state drift); all four required checks genuinely green at the final head at job level (Application baseline run 36804172459; Research reproducibility run 36804172468; OAP bootstrap run 36804172401 with both jobs OAP bootstrap acceptance and OAP report history; every run head_sha 47c4da8); implementation-head reds exactly the designed count red (58 vs 57) with no unexplained reds; data-free re-scan of the published report clean (disclosure-class scratch sentences only); PR #12 OPEN, MERGEABLE, head 47c4da8, base main at 4507cc78e333c0e48226b64266121171b7b8cea8, autoMergeRequest null; exact OK frame consumed by the strategic watcher at 2026-10-01 04:07:05 CEST. Private reprobe receipt read (data-free): exactly 2 metadata GETs on the canonical 009-a routes, both 200, all identity fields matching the 009-a pin, zero generation calls, zero prohibited contact, verdict REGIME-UNCHANGED ESTABLISHED, observation window 2026-10-01T00:58:35.948Z-00:58:36.253Z.",
  "provenance": [
    {"kind": "H", "reference": "Owner objective-009 start instruction 2026-09-30 (freeze the protocol first; continue the loop into data collection/annotation/evaluation under subsequent proof-sized suffixes without the owner as terminal relay; escalate only genuine human/D2 decisions; the ~99 percent and <=1 per 10,000 numbers are evaluation/calibration targets, not release authorization); the owner's verbatim E2(b) decision 2026-09-30 '(b) Designate A100-FP8 as the confirmation target' (private receipt workorders/e2b-decision-receipt-20261001.md); the standing A1 instruction (all four required checks genuinely green; reds never reinterpreted; no weakening); the owner's out-of-band endpoint/bearer provisioning (controlled storage only; unchanged by this round); the owner's 2026-10-01 DASSLE directive, THREE VERBATIM MESSAGES: 'sorry, I don't have this. When did we mutate to be so picky? use DASSLE NOW!' / 'the idea is to use DASSLE and interleave it with made up technical stuff (that needs then to be discarded).' / 'you need to MECHANICALLY BUILD the dataset out of DASSLE and the made-up technical sections. Made up technical sections can be LLM generated. MECHANICALLY means that the LLM does not output any pure slovenian text, just uses dassle and random generated technical sections.' - recorded with interpretation and consequence in the private decision receipt workorders/dassle-reuse-decision-20261001.md; it supersedes the 011-b item-3b owner-intake model, closes the intake boundary (the single escalation consumed by the 011-b round is moot; no re-escalation), and authorizes the DASSLE reuse and the SCAFFOLD_GENERATION call class under controlled private storage."},
    {"kind": "A", "reference": "research/target-distribution/PROTOCOL-009.md (FROZEN, cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a) elements (a)-(n) and section 4 (element (a): pinned identity verified BEFORE the first sample is collected - satisfied here by the 011-c record, byte-verified in this round's pre-work; element (b): manifest-first collection with the pre-registered seed string 009a-target-distribution-20260930; (c) domain mix with the 10 percent floor; (d) stage-1 size 50-100, target 100, floor 50, shortfall recorded; (e) controls >= 25 percent with >= 10 human-authored technical/rare-name; (f)-(g) annotation taxonomy and two-labeler procedure with the 5-document calibration pilot; (h) zero leakage against all 007/008 material; (i)-(k) comparators, metric families, stopping rules, EXACT/CENSORED/UNAVAILABLE semantics; (l) stopping/falsification rules; (m) failure decomposition; (n) no tuning after unblinding - the calibration subset is covered); research/target-distribution/DEPLOYMENT-IDENTITY-011.md section 6 (committed at the base by the 011-c round: the canonical-route re-probe record, the REGIME-UNCHANGED verdict, and the consequence statement that the collection round may proceed on this verified identity subject to its own intake gate); oap/orders/011-b-confirmation-stage1-collection.md (sha256 0456004c...; the pre-registered stage-1 collection specification, re-executed per the continuity note with the bounded adaptation 7); PROTOCOL-009-REVISION-011 (registered byte-exact in Scope item 3f, sha256 609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43, 19,049 B; committed by this round BEFORE any sample is generated; additive: PROTOCOL-009.md stays byte-frozen; supersedes (b) population and collection procedure, (c) domain mix, (e) controls, (g) ground-truth source and labeler tasking, and the zero-leak assertion of (h) only; carries the reclassification statement, the mechanical-assembly mechanics, the registered SCAFFOLD_GENERATION call class and budget, the discard rule and score scoping, and the authorized-reuse disclosure); the frozen 007-m profile contract (config 0026a1a9..., prompt 572cf2fb..., deployment profiles c79fd658.../0c4aa490...) as the exact main-request contract for the genuine-output generation calls; S-ORDER-03 (continuation suffixes preserve branch and PR while that PR is open); S-RECOVER-01 (a completed BLOCKED round is not replayed; its unfinished purpose continues under the next suffix after the intervening round it required); S-PRODUCT-02 (EXACT/CENSORED/UNAVAILABLE and denominator semantics); S-PRODUCT-04 (protected Qwen/services; explicit rights for evaluation data; no credentials in artifacts); LR-001 (complete main capture precedes review), LR-013 (data-free public artifacts), LR-014 (bounded one-pass review)."},
    {"kind": "E", "reference": "Observed 2026-10-01 ~06:2x-06:4x CEST (this session, from remote and primary records): remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 = OAP_ACCEPTED_REF (gh api re-verification at publication); worktree on branch oap/011-target-distribution-confirmation-study at the 011-c final head 47c4da8bf7016614cd62d2448e72f3f7249d0803 (activation d771197c5d58bde2e47c52ae55ffb71621f82f10, identity record 402d5963a7335122c7acdaf107a0238bf8d15ea9, bookkeeping aa37164ec224e706754106019face57ef238a9f8, report-only 47c4da8bf7016614cd62d2448e72f3f7249d0803); PR #12 OPEN and MERGEABLE at that head, base main, autoMergeRequest null, the only open PR, all four required checks green at that head; oap/active = 011-c and strategy's 011-c final-head review PASS recorded privately (workorders/011-c-final-head-review-20261001.md); OAP state after review: INACTIVE; CRITICAL.md seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e, zero entries; machine block on the branch: main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8, parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 39/58/2, identity fields unchanged; registry = 39 entries (last 011-c, kind state-correction, status COMPLETE); local consistency 10/10 at the 011-c final head (the 011-c review); DEPLOYMENT-IDENTITY-011.md at the base byte-verified with section 6 verdict REGIME-UNCHANGED (observation window 2026-10-01T00:58:35.948Z-00:58:36.253Z; both canonical-route GETs 200; all identity fields matching the 009-a pin); DASSLE source census (byte-verified this session, data-free): private research-runtime campaign8 datasets location, dassle.jsonl 7,385 records sha256 609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6 (fields benchmark/category/example_source/id/index/input/problem_type/reference/reference_status; reference_status SUPPLIED 7,381 and MISSING_BLANK_FIELD 4; category census 977/1,487/1,748/1,971/1,202 over the five DASSLE categories; eligible genuine inventory = SUPPLIED and input != reference = 7,354 records) and dassle-preservation.jsonl 7,381 records sha256 d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec (input == reference in all 7,381 records; preservation true; parent link verified: all 7,381 carry the parent spelling record id with matching category and parent.reference as input); 007 consumption record (RESEARCH-STATE section 4/5): campaign8 full-dataset phase over all records (M0-M3); the 2,973-pair 007-h/i/j/m chain over the Chrkovanje-category subset (1,487 spelling + 1,486 preservation; count-matched against the 007-h config source_identity); the private credentials receipt 011b-identity/target-credentials-20261001.json (0600, strategy-corrected dual bases, bearer unchanged) is the sole profile source for the generation calls; the intake boundary is CLOSED by the owner's 2026-10-01 directive (no human input pending; the intake monitor is terminated at publication)."},
    {"kind": "I", "reference": "Strategy 011-b final-head review PASS (private workorders/011-b-final-head-review-20261001.md) - the 011-b BLOCKED round was protocol-conformant and its scope-2c stop mandated the 011-c intervening round; strategy 011-c final-head review PASS (private workorders/011-c-final-head-review-20261001.md) with the private reprobe receipt read; the 011-b publication receipt (private, with the single-exact-signal record and the FUSE stale-stat workaround note); the wrapper-crash incident receipt (private workorders/incident-011b-wrapper-crash-20261001.md; S-RECOVER-01, no replay); the zero-leak source census recorded in the 011-b order E field (DASSLE/MultiGEC/SloBench/Solar consumed by objective 007 - RESEARCH-STATE section 4 - and ineligible for a FRESH population; all 447 private-root entries 007/008 machine scratch; no fresh uninspected human-authored corpus reachable - hence the owner-supplied intake was the only zero-leak-compliant source until superseded); the owner's 2026-10-01 DASSLE directive and the private decision receipt workorders/dassle-reuse-decision-20261001.md (authorized reuse with per-document disclosure; reclassification to development-distribution re-measurement; PLAN section 16 claims remain gated on a genuinely fresh set later); the technical-debt register (TD-1/2/3 non-gating)."}
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
  "lr": ["LR-001", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Objective 011, round 4, on the EXISTING branch
`oap/011-target-distribution-confirmation-study` (AMEND_EXISTING_PR -
PR #12, verified OPEN at head 47c4da8bf7016614cd62d2448e72f3f7249d0803,
the 011-c final head, base main at
`4507cc78e333c0e48226b64266121171b7b8cea8`). The objective's PR stays
open across its suffix rounds and merges only at the objective's end
(the PR #9 / PR #10 pattern; the 011-a review HOLD decision). This is
the **stage-1 COLLECTION round of the development-distribution
re-measurement** (reclassified from "target-distribution
confirmation" per PROTOCOL-009-REVISION-011) on the E2(b)-designated
A100-FP8 regime, executing the pre-registered 011-b collection
specification with the bounded adaptation 7: it commits the
registered revision and scaffold prompt FIRST (Scope item 3f, byte-
exact), verifies the hard-gate identity record (no probe), byte-
verifies the private DASSLE copy, mechanically assembles the stage-1
population (DASSLE texts verbatim + interleaved LLM-generated
technical scaffold sections; scaffold discarded before scoring;
DASSLE human reference as ground truth; DASSLE corrected texts as
controls), creates the collection manifest FIRST, performs the
deterministic seeded selection and 15/85 split with the 5-document
calibration pilot, generates the stage-1 genuine outputs (target 100,
floor 50) plus the control outputs under the frozen main-capture
contract (with the bounded scaffold generation calls preceding them),
and prepares the annotation guide and labeler packets - and NOTHING
else. It performs no evaluation, no scoring, no annotation,
and no comparator run (those are 011-e); it performs no behavior
change of any frozen element (PROTOCOL-009 (n)); it makes no merge,
release, deployment, or milestone claim. The human-intake
boundary is CLOSED by the owner's 2026-10-01 directive (the 011-b
escalation was consumed and is moot; no human input is pending for
this round), not a relay loop. Results are labeled re-measurement,
not confirmation; no fresh-confirmation, release, or milestone claim
is made.

## Provenance

- H: owner 2026-09-30 objective-009 instruction (continue the loop
  into collection/annotation/evaluation under proof-sized suffixes;
  the owner is not a terminal relay; escalate only genuine human/D2
  decisions; the ~99 percent and <=1 per 10,000 numbers are
  calibration targets, not release authorization), the verbatim E2(b)
  decision 2026-09-30 (private receipt), the standing A1 instruction,
  the out-of-band endpoint/bearer provisioning (controlled storage
  only; unchanged this round), the record that the intake escalation
  was sent EXACTLY ONCE by the 011-b round, and the owner's
  2026-10-01 DASSLE directive (three verbatim messages; private
  decision receipt workorders/dassle-reuse-decision-20261001.md)
  which supersedes the item-3b intake model, closes the intake
  boundary, and authorizes the DASSLE reuse and the SCAFFOLD_
  GENERATION call class.
- A: FROZEN PROTOCOL-009 (cc5e9089...) elements (a)-(n) and section
  4 AS AMENDED by PROTOCOL-009-REVISION-011 (Scope item 3f;
  additive; supersedes (b)/(c)/(e)/(g) and the (h) zero-leak
  assertion only); DEPLOYMENT-IDENTITY-011.md section 6 (the 011-c
  REGIME-UNCHANGED verdict, committed at the base); the published
  011-b order (sha 0456004c...) as the re-executed pre-registered
  collection specification (bounded adaptation 7); the frozen 007-m
  profile contract for the main-capture calls; the registered
  SCAFFOLD-GENERATOR-PROMPT-011 (Scope item 3f); S-ORDER-03; S-
  RECOVER-01; S-PRODUCT-02/04; LR-001/013/014.
- E: the verified state recorded in the metadata E field (main,
  PR #12, worktree, machine block 39/58/2, 10/10 local consistency,
  CRITICAL seed, registry 39, the 011-c identity record, the DASSLE
  source census with both sha256 re-verified this session).
- I: the 011-b review PASS (BLOCKED round, protocol-conformant; its
  scope-2c stop mandated 011-c), the 011-c review PASS (COMPLETE round;
  REGIME-UNCHANGED; hard gate satisfied), the 011-b publication
  receipt (single exact signal; the intake escalation consumed and
  now moot per the owner directive), the incident receipt (wrapper
  crash; S-RECOVER-01), the zero-leak source census and the DASSLE
  authorized-reuse decision receipt, and the technical-debt register
  (TD-1/2/3 non-gating).

## Current verified state

Verified 2026-10-01 (this session, from remote and primary records):
remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 =
OAP_ACCEPTED_REF (gh api re-verification at publication); worktree on
branch oap/011-target-distribution-confirmation-study at the 011-c
final head 47c4da8bf7016614cd62d2448e72f3f7249d0803; PR #12 OPEN and
MERGEABLE at that head, base main, autoMergeRequest null, the only
open PR, all four required checks green at that head; oap/active =
011-c with the strategy 011-c final-head review PASS on record
privately (workorders/011-c-final-head-review-20261001.md); OAP state
INACTIVE; CRITICAL.md seed-identical
a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e with
zero entries; machine block on the branch: main_sha/reviewed
4507cc78e333c0e48226b64266121171b7b8cea8, parent
01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 39/58/2, identity
fields unchanged; registry = 39 entries (last 011-c, kind state-
correction, status COMPLETE); local consistency 10/10 at the 011-c
final head (the 011-c review); DEPLOYMENT-IDENTITY-011.md at the base
byte-verified, section 6 verdict REGIME-UNCHANGED (observation window
2026-10-01T00:58:35.948Z-00:58:36.253Z); DASSLE source census (byte-
verified this session): dassle.jsonl 7,385 records sha256
609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6
(eligible genuine inventory 7,354 = SUPPLIED and input != reference)
and dassle-preservation.jsonl 7,381 records sha256
d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec
(input == reference in all records; parent link verified); the
private credentials receipt 011b-identity/target-credentials-
20261001.json (0600, strategy-corrected dual bases, bearer
unchanged) is the sole profile source. Environment notes: degraded
rclone/Dropbox FUSE mount; heavy test temp on native /home/ubuntu/
.oap-scratch (0700); OAP helper git-history traversals can transiently
time out at the 30 s subprocess limit (TD-3, non-gating, retry
deterministic and safe); CI parity authoritative for the heavy
fixture cycles; REPAIR_ALLOW_LIVE_TESTS = NO unchanged.

## Governance

The sixteen source identities in the metadata governance mapping are
the exact identities of `oap/governance/MANIFEST.json` at the accepted
base `4507cc78e333c0e48226b64266121171b7b8cea8`, unchanged (16/16,
coding_bytes 35076). No governance change occurs in this objective.
The private research-runtime root layout (011b-collection/, 011b-
packets/ directories under the native private root; 0700 directories,
0600 files; 011b-intake/ stays absent - superseded) follows the
established 009a-identity convention; none of it is ever committed.

## Goal and dependencies

Goal: complete the PROTOCOL-009 (as amended by PROTOCOL-009-
REVISION-011) stage-1 collection on the E2(b)-designated A100-FP8
regime exactly as registered: commit the revision and scaffold prompt
byte-exact, verify the hard-gate identity record committed at 011-c
(no probe), byte-verify the private DASSLE copy, mechanically assemble
the stage-1 population (DASSLE texts verbatim + interleaved LLM-
generated technical scaffold sections; scaffold discarded before
scoring; DASSLE human reference as ground truth; DASSLE corrected
texts as controls), create the collection manifest FIRST, perform the
deterministic seeded selection and 15/85 split with the 5-document
calibration pilot, generate the stage-1 genuine outputs (target 100,
floor 50) plus the control outputs under the frozen main-capture
contract (with the bounded scaffold calls preceding them), prepare the
annotation guide and labeler packets, and commit only data-free
artifacts - so that 011-e (annotation consolidation + comparative
evaluation) starts from a fully frozen, fully manifest-documented,
authorized-reuse-disclosed stage-1 population, labeled development-
distribution re-measurement.

Dependencies: 011-c (reviewed PASS; its section-6 REGIME-UNCHANGED
record is the hard-gate precondition; PR #12 held open), the owner
E2(b) decision (standing), the owner's 2026-10-01 DASSLE
directive (standing; closes the intake boundary; private decision
receipt), the byte-verified private DASSLE copy (scope item 3
source; read-only), and
007/008/009/010/011-a/011-b/011-c only as the frozen surfaces
preserved by the local_work field. The two Slovenian-native
independent labelers are a 011-e input, not a 011-d input (this round
only prepares the packets).

## Scope

1. Pre-work integrity gates (data-free): at the base
   47c4da8bf7016614cd62d2448e72f3f7249d0803, byte-verify every frozen
   surface and the objective-009/011-a/011-b/011-c artifacts
   (PROTOCOL-009.md, DEPLOYMENT-IDENTITY-009.md, DEPLOYMENT-
   IDENTITY-011.md including section 6, test_009a_protocol_elements.py,
   the 007-m pins, the 008 protection-layer pins, the 011-a/011-b/
   011-c orders and reports, RESEARCH-STATE sections 24-27, CRITICAL.md
   seed-identical
   a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e);
   machine block on the branch: main_sha/reviewed
   4507cc78e333c0e48226b64266121171b7b8cea8, parent
   01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 39/58/2,
   identity fields unchanged; registry = 39 entries (last 011-c, kind
   state-correction, status COMPLETE); local consistency 10/10 in a
   real checkout of the branch with origin/main =
   4507cc78e333c0e48226b64266121171b7b8cea8. Any mismatch is BLOCKED
   with the mismatch named; no work proceeds.
2. Hard-gate (a) precondition - identity record verification (NO
   probe in this round): verify that
   `research/target-distribution/DEPLOYMENT-IDENTITY-011.md` section
   6 (committed at the base; byte-verified in item 1) records: the
   011-c canonical-route re-probe (attempt 1: server-root /version
   unauthenticated, 200; attempt 2: /v1/models with the authorized
   bearer, 200; exactly 2 metadata GETs; zero generation calls; zero
   prohibited contact); all observed identity fields matching the
   009-a pin (serving framework version 0.28.0; model identifier
   qwen3.8-27b; root suffix Qwen3.8-27B-FP8; max model length 262144;
   OpenAI-compatible Responses wire API non-streaming); the verdict
   REGIME-UNCHANGED ESTABLISHED; the consequence statement that the
   collection round may proceed on this verified identity subject to
   its own intake gate; the observation window
   2026-10-01T00:58:35.948Z-00:58:36.253Z. Any missing or mismatched
   element is BLOCKED with the element named; nothing else is
   executed. NO metadata probe, NO version endpoint call, NO models
   endpoint call occurs in this round: the owner's bounded-probe
   usage constraint (exactly 2 metadata GETs total, no retries) was
   designed for and exhausted by the 011-b/011-c pinning work, and the
   element (a) freshness precondition (pinned identity verified before
   the first sample is collected) is satisfied by the 011-c record
   within this objective. The ONLY network calls of this round are the ordered scaffold
   generation calls (item 3c and 7a; registered class and budget) and
   the ordered per-document main-capture generation calls (item 7b;
   frozen 007-m profile), all on the designated target only.
3. Source gate - DASSLE byte-verification and mechanical assembly
   (owner 2026-10-01 directive; NO human input pending; the 011-b
   escalation is consumed and moot; NOT re-escalated):
   a. Source location and byte verification: the private DASSLE copy
      under the private research-runtime campaign8 datasets location
      (READ-ONLY for this round). Before any assembly or call:
      re-verify dassle.jsonl sha256
      609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6
      (7,385 records) and dassle-preservation.jsonl sha256
      d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec
      (7,381 records) byte-for-byte; verify the record-field census
      (reference_status SUPPLIED 7,381 / MISSING_BLANK_FIELD 4;
      category census per PROTOCOL-009-REVISION-011 section 2;
      preservation input == reference in all 7,381 records; the
      parent-link rule: every preservation record carries the parent
      spelling record id). Any mismatch is BLOCKED with the element
      named; nothing else is executed; NO replacement file.
   b. Eligible inventories (per PROTOCOL-009-REVISION-011 section 3):
      GENUINE arm = records with reference_status == SUPPLIED and
      input != reference (7,354 records); CONTROL arm = all 7,381
      preservation records (exclusion recomputed after Draw 1, item 5).
      The 011-b item-3b owner-delivery specification (fresh human-
      authored documents, sidecars, attestations) is SUPERSEDED in its
      entirety by the directive; its BLOCKED-once escalation remains
      consumed and is not repeated.
   c. Mechanical assembly (per PROTOCOL-009-REVISION-011 sections 3
      and 8, registered byte-exact): for each selected record,
      assemble exactly one document = the verbatim DASSLE block (the
      erroring input for the genuine arm; the corrected text for the
      control arm) plus k = 1 + rng_asm.randrange(3) interleaved
      LLM-generated Slovenian technical scaffold sections (rng_asm =
      random.Random("011d-dassle-mechanical-assembly-20261001"),
      Python 3.12, single instance, created once, documents processed
      in sorted collection-ID order; topics drawn from the registered
      12-topic list; layout per the revision: k=1 -> [s1, D]; k=2 ->
      [s1, D, s2]; k=3 -> [s1, s2, D, s3]; blocks joined by exactly
      two LF characters; no other separators). Each scaffold section
      is ONE SCAFFOLD_GENERATION call on the designated target only
      (registered prompt SCAFFOLD-GENERATOR-PROMPT-011.md, the single
      {tema} sentinel replaced by the drawn topic, no other byte
      changed; Responses wire non-streaming; fresh isolated context,
      no session linkage, no tools, no images, no constitutional-
      adapter recursion; output-token cap 600; 300 s; 2,000,000
      bytes; one terminal attempt; no resampling; profile ONLY from
      the private 011b-identity credentials receipt). Budget cap: at
      most 402 scaffold calls for stage 1 (134 documents x 3
      sections). The DASSLE block enters the document BYTE-FOR-BYTE:
      no synthetic error injection, no model-assisted authoring or
      editing of any DASSLE text; the LLM outputs scaffold sections
      ONLY, never a "pure Slovenian" source document.
   d. Scaffold failure rule: a failed or empty scaffold section
      EXCLUDES its document (named; no replacement, no re-sampling);
      the exclusion is counted operationally. If exclusions drop the
      genuine-arm count below the floor of 50: Result: BLOCKED on the
      named shortfall; NO manifest finalization, NO selection, NO
      split, NO main-capture call, NO sample opened; a truthful
      report is published and the exact response OK sent. The loop
      resumes the same round by recovery re-signal (S-RECOVER-01).
      NO re-escalation of any intake question (the intake boundary is
      closed by the owner directive); a NEW distinct genuine human
      question may be presented once, attributable, never per-
      sample, never as a terminal relay.
   e. Discard map: per document, the code-point (start, end-
      exclusive) offsets of every scaffold block and of the DASSLE
      block are computed and recorded in the manifest (item 4); the
      scaffold sections are DISCARDED before scoring (no denominator,
      word count, coverage, harm rate, or preservation metric ever
      touches them; labelers never label them; packets mark them
      OUT_OF_SCOPE).
   f. REGISTERED FILE BYTES (committed by this round byte-exact,
      BEFORE any sample is opened or any scaffold call made; the
      order is immutable; the round commits exactly these bytes
      data-free under research/target-distribution/ and records the
      sha256 in the manifest/report):
      (1) PROTOCOL-009-REVISION-011.md (19,049 B, sha256
      609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43;
      additive - PROTOCOL-009.md stays byte-frozen):
````markdown
# PROTOCOL-009-REVISION-011 - additive owner-attributed revision: DASSLE
# mechanical-assembly intake for the stage-1 collection

Status: REGISTERED (additive; round 011-d, objective 011). This revision is
committed BEFORE any sample is generated. `PROTOCOL-009.md` remains
byte-frozen and authoritative for every element NOT superseded below. This
document is data-free: it contains no corpus text, no confirmation sample,
no raw Slovenian document, no endpoint values, no credentials, and no
private paths (the registered generator prompt is a registered instruction
template, the same artifact class as the 011-e registered comparator
prompt; the registered topic list carries topic names only).

## 0. Authority, status, supersession map

- Authority: explicit attributable owner directive of 2026-10-01 (three
  verbatim messages recorded in the private decision receipt
  workorders/dassle-reuse-decision-20261001.md; H-provenance of the 011-d
  order). Under S-AUTH-01/02 the owner's explicit decision on data source
  and risk appetite supersedes the owner-supplied-intake model of the
  published 011-b collection specification.
- Effect: SUPERSEDES, for the stage-1 collection and the 011-e evaluation
  that consumes it, exactly the following elements of PROTOCOL-009:
  (b) sampling population and collection procedure; (c) domain mix;
  (e) correct-text negative controls; (g) source-of-ground-truth and
  labeler tasking within the adjudication procedure; (h) the
  zero-leakage assertion only (the split rule of (h) is UNCHANGED).
- Every other element is UNCHANGED and remains authoritative, including:
  (a) target-deployment hard gate (the E2(b)-designated A100-FP8 regime,
  verified by the 011-c REGIME-UNCHANGED record); (d) stage sizes and
  expansion criteria; (f) annotation taxonomy (label names unchanged;
  the assignment tasking is adjusted per section 5 below); (i) comparators
  (including the 011-e registered DIRECT_QWEN_PROOFREADING prompt);
  (j) metrics and denominators (scoped per section 6 below); (k)
  uncertainty intervals; (l) stopping/falsification rules; (m) failure
  decomposition; (n) no-tuning-after-unblinding; section 0, section 2
  (frozen-system identity pin, unchanged byte-for-byte), and section 4
  (data rights and privacy, as extended by section 7 below).
- This revision changes NO frozen element of the frozen system
  (section 2 of PROTOCOL-009): no candidate rule, ranking tuple, detector
  threshold/eligibility, candidate semantics, validator prompt/parser/
  protocol, reasoning level, acceptance policy, protocol limit, retry
  policy, or protection rule is altered. Element (n) is NOT triggered
  (no confirmation-subset decision content is opened; no mechanism
  change). RESEARCH-STATE section 14 (no further tuning on DASSLE or any
  already-inspected benchmark) remains in force for mechanism changes.

## 1. Reclassification statement (recorded once)

This study is RECLASSIFIED from "fresh target-distribution confirmation"
to "development-distribution re-measurement". All DASSLE texts are
previously inspected: objective 007 ran the campaign8 full-dataset phase
over all 7,385 spelling records and all 7,381 preservation records
(M0-M3), and the 2,973-pair 007-h/i/j/m method-development chain consumed
the category-Chrkovanje subset (1,487 spelling + 1,486 preservation;
count-matched against the 007-h config source_identity). Consequences:
1. The results of this study do NOT support a fresh target-distribution
   confirmation claim. PLAN section 16 milestone/MVP claims remain gated
   on a genuinely fresh, uninspected set at a later objective.
2. The reclassification concerns input provenance only: the E2(b) target
   designation (A100-FP8) and the frozen system under measurement are
   unchanged.
3. Honest labeling: the 011-e report title, RESEARCH-STATE section, and
   registry entry must use the re-measurement label.

## 2. Source data (byte-verified, private, data-free references)

- DASSLE spelling source: private file `dassle.jsonl`, 7,385 records,
  sha256 609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6.
  Fields (per record): benchmark, category, example_source, id (unique),
  index, input (erroring source text, sentence-level), problem_type,
  reference (human correction), reference_status (SUPPLIED: 7,381;
  MISSING_BLANK_FIELD: 4).
- DASSLE preservation: private file `dassle-preservation.jsonl`, 7,381
  records, sha256 d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec.
  Fields as above plus preservation: true and parent_source_sha256;
  input == reference in ALL 7,381 records (fully-correct texts by
  construction, per the dataset's own adaptation record).
- Both files reside under the private research-runtime root (the
  campaign8 private location). The 011-d round re-verifies BOTH sha256
  values byte-for-byte before any assembly; any mismatch BLOCKS the
  round (named), no replacement.
- Category distribution (data-free census, verified 2026-10-01):
  Besedišče 977 / Črkovanje 1,487 / Oblikoslovje 1,748 / Skladnja 1,971 /
  Zapis 1,202 (spelling file); preservation file: Besedišče 976 /
  Črkovanje 1,486 / Oblikoslovje 1,748 / Skladnja 1,971 / Zapis 1,200.

## 3. Superseded element (b): population and collection procedure

POPULATION (mechanical assembly). The stage-1 population consists of
MECHANICALLY ASSEMBLED documents. Each document is exactly one DASSLE-
derived block (the VERBATIM `input` text of one DASSLE record: the
erroring source for the genuine arm, the corrected text for the control
arm) plus one to three LLM-generated Slovenian technical scaffold
sections interleaved around it. The LLM outputs ONLY scaffold sections;
it never outputs a "pure Slovenian" source document (owner directive,
verbatim in the decision receipt). No synthetic error injection; no
model-assisted authoring or editing of any DASSLE text; the DASSLE block
enters the document byte-for-byte.

Eligible inventories:
- GENUINE arm: records with reference_status == SUPPLIED and
  input != reference (non-identity pairs; 7,354 records).
- CONTROL arm: all 7,381 preservation records, EXCLUDING (registered)
  every preservation record whose `id` equals the `id` of a record
  selected in Draw 1 (verified parent link: all 7,381 preservation
  records carry the parent spelling record id, inherit its category,
  and carry parent.reference as their input). This prevents one
  underlying text from appearing in both arms.

Assembly mechanics (registered, deterministic; a single PRNG instance
`rng_asm = random.Random("011d-dassle-mechanical-assembly-20261001")`,
Python 3.12, frozen environment, created once, drawn in this exact order
per document, documents processed in sorted collection-ID order):
1. k = 1 + rng_asm.randrange(3) -> the number of scaffold sections
   (k in {1, 2, 3}).
2. For j = 1..k: topic_j = TOPICS[rng_asm.randrange(len(TOPICS))];
   section_j = one SCAFFOLD_GENERATION call (section 4 below) with the
   {tema} sentinel replaced by topic_j (single occurrence, no other
   byte changed).
3. Layout: the DASSLE block is inserted after the first ceil(k/2)
   sections: k=1 -> [s1, D]; k=2 -> [s1, D, s2]; k=3 -> [s1, s2, D, s3].
4. Blocks are joined by exactly two LF characters ("\n\n"); the document
   is exactly that concatenation (no other separators, headers, or
   whitespace).
5. DISCARD MAP: the manifest records, per document, the code-point
   (start, end-exclusive) offsets of every scaffold block and of the
   DASSLE block within the document. The discard map is the data-free
   definition of what is scored and what is discarded.

Selection (re-executes the PROTOCOL-009 (b) PRNG mechanics over the new
population; the pre-registered seed string is retained): a single PRNG
instance `rng_sel = random.Random("009a-target-distribution-20260930")`
is created once and drawn in this exact order, every draw over its list
sorted lexicographically by record id, without replacement, via
`i = rng_sel.randrange(len(remaining)); take remaining.pop(i)`:
- Draw 1 (genuine): from the eligible genuine inventory, up to 100
  (target; floor 50 per (d); any shortfall between 50 and 100 is
  RECORDED with its reason).
- Draw 2 (control): from the eligible control inventory (post-exclusion,
  recomputed AFTER Draw 1), up to ceil(len(Draw 1)/3) (target 34 for
  G = 100; the (e) quota).
The previously registered technical/rare-name control draw is WAIVED by
the owner directive (recorded limitation, section 4b below). The
selected set (G genuine documents + C control documents) is the stage-1
population; each selected DASSLE record yields exactly one document.
Unselected eligible records remain available for 011-f stage-2
expansion only (unopened; no re-sampling of the selected set).

Manifest-first: the collection manifest is created BEFORE any sample is
opened or any scaffold call made, and is extended per document with the
record id, dataset sha references, consumption tier (section 7),
section-count/topic draws (data-free), discard map, and per-call
metadata (numbers only). Collection IDs retain the pre-registered
`011b-<seq:04d>` scheme, assigned deterministically in sorted
(doc_slug) order, with doc_slug = `dassle-spelling-<id>` or
`dassle-preservation-<id>` (the DASSLE record id, zero-padded to 4
digits). Artifact names (`011b-collection-manifest.json`, `011b-
collection/`, `011b-packets/`) are retained unchanged.

## 4. Superseded element (c): domain mix (mechanical mapping)

- The DASSLE source (example_source: Šolar 3.0) is general educational
  prose; its per-record `category` field is an ERROR-TYPE category
  (vocabulary / spelling / morphology / syntax / orthography), not a
  topic domain. Registered mechanical rule: EVERY document carries
  domain_tag = "general-prose"; the DASSLE category is recorded in the
  manifest as source metadata only and is NEVER used as a domain tag.
- The pre-registered 10 percent domain floor (c) is vacuously satisfied
  (single domain; recorded as N/A with the reason - not a violation and
  not an expansion trigger).
- Limitation (WAIVER, owner directive): the pre-registered >= 10
  human-authored technical/rare-name control documents of element (e)
  is WAIVED: the DASSLE source contains no scored technical/rare-name
  population. Technical-domain realism is present ONLY in the discarded
  scaffold sections (which are, by definition, not scored). This
  limitation is recorded in the manifest, the annotation guide, and the
  011-e report, and it bounds the external validity of any technical-
  domain claim (there is none scored in this study).

## 5. Superseded element (g): source of ground truth and labeler tasking

- Source ground truth for DASSLE-derived spans is the DASSLE human
  `reference` (the dataset's own per-record human correction), NOT
  fresh human authoring. For controls (preservation records) the text is
  fully correct by construction (input == reference; dataset-attested).
- Span correspondence (registered deterministic matcher, run in 011-e
  before any scoring): the pipeline operates on the collected main
  answer; the scored DASSLE span of a main answer is located as follows.
  Let M = the main answer truncated to its first 50,000 code points
  (registered cap; a longer main answer is UNALIGNABLE by cap). For
  candidate c in the order (1) the verbatim DASSLE `input`, (2) the DASSLE
  `reference`: compute m = difflib.SequenceMatcher(None, c, M,
  autojunk=False); take (i1, i2, j) = m.find_longest_match(0, len(c), 0,
  len(M)); if (i2 - i1) >= 0.8 * len(c), the scored span is M[j : j +
  (i2 - i1)] (code points, end-exclusive). If no candidate reaches the
  0.8 ratio, the document is UNALIGNABLE (a named conservative state,
  recorded; the document is excluded from span scoring and counted
  operationally; never reported as zero, S-PRODUCT-02).
- Labeler tasking (reduced accordingly): (1) per scored DASSLE span in
  the main answer: verify ACTUAL_ERROR (the span deviates from the
  reference in a way that is a genuine error) or ACCEPTABLE_UNCHANGED
  (already correct or an acceptable variant), or NEEDS_WIDER_EDIT (the
  correct fix is non-local) - the labeler VERIFIES/ADJUDICATES the
  dataset reference; (2) per accepted edit within a scored span:
  intervention outcome (CORRECTS_ERROR / ACCEPTABLE_ALTERNATIVE /
  HARMLESS_STYLISTIC / HARMFUL_CHANGE) relative to the reference;
  (3) MANDATORY DETECTOR_MISS attribution for every genuine error not
  flagged; (4) layer-failure classes per (f) for every genuine error not
  finally repaired, first-failing-stage order per (m). Labelers NEVER
  label scaffold blocks: packets include the discard map, scaffold
  regions are marked OUT_OF_SCOPE, and any accepted edit wholly outside
  the scored span is recorded as OUT_OF_SCORED_SPANS (counted, never
  scored). The two-labeler procedure, disagreement recording, owner/
  named-human adjudication of ambiguous cases, the 5-document
  calibration pilot (alignment only, never scored), and "Qwen is NEVER
  the final judge" are UNCHANGED.

## 6. Superseded element (e): controls; score scoping

- FULLY_CORRECT controls are assembled documents built from
  preservation records (corrected DASSLE texts, fully correct by
  construction). Quota: C >= ceil(G/3) (target 34 for G = 100), drawn
  per section 3 Draw 2 post-exclusion. Controls carry the harm-rate
  denominator (originally-correct words) and the preservation metrics,
  scoped to their scored DASSLE spans (for controls: the entire DASSLE
  block, which is fully correct text).
- Score scoping (extends (j) without changing any formula): every
  denominator and word count is computed over DASSLE-SCORED spans only,
  per the discard map and the section-5 matcher:
  "originally-correct words" = frozen word counter over the reference
  text of the DASSLE blocks (controls: all of it; genuine: the
  reference spans); coverage denominators count genuine errors WITHIN
  scored spans (per the reference, as verified by labelers); accepted-
  edit denominators count assessed accepted edits WITHIN scored spans.
  Edits outside scored spans are OUT_OF_SCORED_SPANS: recorded in the
  report (count + scope), never counted in harm, coverage, or
  preservation. All metric formulas, comparators, and stopping rules of
  (i)-(l) are otherwise unchanged.

## 7. Superseded element (h): authorized-reuse disclosure (split
   rule unchanged)

- The zero-leakage assertion ("no case generated or inspected for any
  earlier objective") is SUPERSEDED by AUTHORIZED-REUSE DISCLOSURE:
  the population is an authorized reuse of DASSLE by the owner's
  2026-10-01 directive (private decision receipt). Per-document
  attestation in the manifest and report: DASSLE record id, dataset sha
  references (section 2), and CONSUMPTION TIER: TIER-2 (method
  development) for records with category == Črkovanje (the 2,973-pair
  007-h/i/j/m chain; verified count-match: 1,487 spelling + 1,486
  preservation); TIER-1 (campaign8 full-dataset only) for all others.
  No document in this population is fresh or uninspected; this is
  disclosed, not hidden.
- The split rule of (h) is UNCHANGED: at collection time, before any
  opening, the 15/85 split by collection ID (k = ceil(0.15 * N);
  lexicographic hex of sha256(collection ID)), the 5-document
  calibration pilot excluded from both subsets, and the confirmation
  subset untouched until final scoring.
- The no-tuning rule (n) is UNCHANGED and NOT triggered by this
  revision (no frozen element changed; no decision informed by
  confirmation-subset content).

## 8. Registered SCAFFOLD_GENERATION call class

- Purpose: produce ONLY the discarded technical scaffold sections.
  This is a new, registered, bounded call class on the designated
  target (the E2(b)-designated A100-FP8 regime as verified at 011-c),
  authorized by the owner directive; it is separate from, and does not
  alter, the main-capture contract of the genuine-output generation
  (which remains the frozen 007-m profile contract) or from
  REPAIR_ALLOW_LIVE_TESTS = NO (product live tests remain disallowed).
- Prompt (registered byte-exact; committed as
  `research/target-distribution/SCAFFOLD-GENERATOR-PROMPT-011.md`,
  exactly the template bytes, 402 B, sha256
  005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc):
  a Slovenian instruction to write a short professional technical
  paragraph (150-250 words) on the topic given by the single {tema}
  sentinel; no title, no bullet list, no code, no persons, no direct
  questions to the reader, no external sources cited; output the
  paragraph text only.
- Registered topic list (12 data-free topic names, exact UTF-8 strings;
  drawn per section 3 step 2): vzdrževanje klimatskih naprav;
  montaža sončnih panelov; konfiguracija omrežnih stikal;
  termična izolacija cevovodov; kalibracija merilnih senzorjev;
  preskušanje nosilnih konstrukcij; vzdrževanje parnih kotlov;
  temeljenje gradbenih objektov; osvetlitev industrijskih prostorov;
  obratovanje hidravličnih dvigal; prezračevanje podstresnih
  prostorov; varnostna preskušanja električnih naprav.
- Call contract: one fresh isolated request per section on the
  designated target only; Responses wire API, non-streaming; NO main
  history, NO session linkage, NO tools, NO images, NO constitutional-
  adapter recursion (S-PRODUCT-02); profile (both bases + bearer) read
  ONLY from the private 011b-identity credentials receipt (the sole
  profile source; never committed, logged, or echoed); output-token
  cap 600; 300 s timeout; 2,000,000-byte response bound; ONE terminal
  attempt; NO resampling, NO retry.
- Response handling (deterministic, pre-registered): store verbatim
  privately (011b-collection scaffold store, 0700/0600, never
  committed); strip exactly one trailing LF; strip exactly one outer
  code-fence pair iff the first and last lines are exactly three
  backticks with nothing outside; otherwise use the text as received.
  If the call fails or the processed section is empty: the document is
  EXCLUDED with the failure named (no replacement, no re-sampling); the
  exclusion is counted operationally.
- Budget (registered cap): at most (G + C) documents, at most 3
  sections each -> at most 402 scaffold calls for stage 1 (G target 100
  + C target 34 = 134 documents). Every call is recorded in the
  manifest (numbers only: HTTP status, wall time, tokens, capture size,
  state).

## 9. Data rights extension (supersedes section 4 only where stated)

- DASSLE was previously acquired and used under owner direction for
  objective 007; the owner's 2026-10-01 directive authorizes controlled
  private reuse for this study. No redistribution; no raw DASSLE text,
  no scaffold text, no main answers, no endpoint values, no
  credentials, and no private paths in any committed artifact, log, or
  report (LR-013; PROTOCOL-009 section 4 otherwise unchanged).
- The LLM-generated scaffold sections are owner-authorized synthetic
  material, private, discarded, and never committed.
````
      (2) SCAFFOLD-GENERATOR-PROMPT-011.md (402 B, sha256
      005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc;
      the scaffold prompt template with the single {tema} sentinel):
````text
Zapiši kratek strokovni tehnični odstavek (150-250 besed) v slovenščini o temi: {tema}. Besedilo naj opiše postopek, sistem ali tehnična navodila iz izbranega področja; naj bo naravno, strokovno in tehnično. Brez naslova, brez seznama z zvezdicami, brez kodnih primerov, brez oseb, brez neposrednih vprašanj bralcu in brez navajanja zunanjih virov. Odgovor naj vsebuje samo besedilo odstavka.
````
      Convention (identical to the 011-e registered-prompt pattern):
      the fence stands at column 0 and the content lines are
      unindented; the exact committed bytes are exactly the bytes
      between the opening fence line and the closing fence line (the
      content already ends with the file's final newline). The round
      must assert the sha256 of each committed file matches the
      recorded value (any mismatch = BLOCKED, named).
4. Collection manifest FIRST (before any sample is opened): commit
   `research/target-distribution/011b-collection-manifest.json`
   (name retained per the continuity note; data-free: counts, IDs,
   tags, timestamps, hashes, selection mechanics; NO raw text, NO
   endpoint values, NO credentials, NO private paths). Contents:
   (i) the full assembly census (collection ID, domain tag, source
   kind, DASSLE record id, arm, dataset sha references, consumption
   tier, assembly draws (k and topics, data-free), private file
   sha256, verification status per document); collection IDs are
   assigned by this round
   deterministically as `011b-<seq:04d>` in sorted (domain_tag,
   doc_slug) order at source verification, where doc_slug =
   dassle-spelling-<id> or dassle-preservation-<id> (the DASSLE
   record id, zero-padded to 4 digits), and are immutable once
   recorded; (ii) the selection draws per item 5 with the exact PRNG
   mechanics recorded (seed string, single instance, draw order, per-
   draw list lengths and final list identities by collection ID - all
   data-free); (iii) the partition per item 6 (pilot / calibration /
   confirmation, by collection ID lists); (iv) the pinned identity
   reference by hash only (the 009-a committed record
   b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4;
   the 011-c re-verification record: DEPLOYMENT-IDENTITY-011.md sha256
   at the base, the REGIME-UNCHANGED verdict, the observation window);
   (v) the per-sample call metadata filled during generation (per
   collection ID: HTTP status, wall time, token counts, capture size,
   state EXACT/CENSORED/UNAVAILABLE - numbers only);    (vi) the authorized-reuse disclosure (per PROTOCOL-009-
      REVISION-011 section 7; replaces the 011-b zero-leakage
      assertion): per-document attestation (DASSLE record id,
      dataset sha references, consumption tier: TIER-2 for the
      Chrkovanje-category records (the 2,973-pair 007-h/i/j/m chain),
      TIER-1 for all others (campaign8 full-dataset only)) plus the
      aggregate statement: this population is an authorized reuse of
      DASSLE by the owner's 2026-10-01 directive; no case in this
      population is fresh or uninspected; the study is a
      development-distribution re-measurement, not a fresh
      confirmation.
   (vii) the discard map (per document: code-point offsets of every
      scaffold block and of the DASSLE block; the data-free
      definition of scored vs discarded content) and the scaffold-
      call census (per collection ID: HTTP status, wall time, tokens,
      capture size, state - numbers only).
5. Stage-1 selection (pre-registered, deterministic; per PROTOCOL-
   009-REVISION-011 section 3, which re-executes the PROTOCOL-009
   (b) PRNG mechanics over the DASSLE population): a single PRNG
   instance `rng = random.Random("009a-target-distribution-20260930")`
   (Python 3.12, frozen environment; the pre-registered seed string)
   is created once and drawn in this exact order, every draw over its
   list sorted lexicographically by DASSLE record id, without
   replacement, via `i = rng.randrange(len(remaining)); take
   remaining.pop(i)`:
   - Draw 1 (genuine): from the eligible genuine inventory (item 3b;
     7,354 records), up to 100 (target; if the eligible list is
     smaller, take all - the floor-50 rule of item 3d bounds
     BLOCKED; any shortfall between 50 and 100 is RECORDED with its
     reason in the manifest and report, per PROTOCOL-009 (d)).
   - Draw 2 (control): from the eligible control inventory AFTER
     excluding every preservation record whose id equals the id of a
     record selected in Draw 1 (the registered no-both-arms rule),
     up to ceil(len(Draw 1)/3) (the (e) quota C >= ceil(G/3); target
     34 for G = 100).
   - The previously registered technical/rare-name control draw is
     WAIVED by the owner directive (recorded limitation, PROTOCOL-
     009-REVISION-011 section 4: the DASSLE source contains no
     scored technical/rare-name population; technical realism is
     present only in the discarded scaffold).
   - Domain-floor check (PROTOCOL-009 (c) as amended): every
     document carries domain_tag general-prose (registered
     mechanical rule; the DASSLE category is source metadata only);
     the 10 percent floor is vacuously satisfied and RECORDED as N/A
     with the reason (single domain; not a violation; no expansion
     trigger; never re-labeling).
   - The selected set (G genuine records + C control records) is the
     stage-1 population (one document per selected record); the
     unselected eligible records remain available for 011-f stage-2
     expansion only (uncollected, unopened; no re-sampling of the
     selected set).
6. Split and calibration pilot (deterministic, at collection time,
   before the confirmation subset is opened; transcribes PROTOCOL-
   009 (g)/(h)):
   - Pilot: the first 5 draw-1 documents in lexicographic order of
     the hex encoding of sha256(collection ID) -> the 5-document
     calibration pilot (genuine outputs; excluded from BOTH the
     calibration subset and the confirmation subset; used only for
     labeler alignment in 011-e; never scored or used for method
     decisions).
   - Let N = (len(draw 1) - 5) + C (the stage-1 documents excluding
     the pilot). k = ceil(0.15 * N). Calibration subset = the first k
     of the N documents in lexicographic order of the hex encoding of
     sha256(collection ID); confirmation subset = the remaining
     N - k documents, UNTOUCHED until final scoring in 011-e.
   - The three partitions (pilot / calibration / confirmation) are
     disjoint and cover the selected stage-1 documents exactly; the
     partition is recorded in the manifest (item 4) by collection ID
     lists. Zero leakage between partitions and with any 007/008
     material is asserted in the manifest (item 4 vi).
   - The calibration subset's use (operational verification of the
     frozen pipeline mechanics in 011-e) is OUT of this round's
     scope; this round computes and records the partition and nothing
     else about those documents.
7. Bounded generation on the designated target (the live work of
   this round; authorized by the E2(b) decision + PROTOCOL-009
   element (a) as re-verified at 011-c + the owner's 2026-10-01
   directive for the scaffold class; separately from
   REPAIR_ALLOW_LIVE_TESTS = NO which stays unchanged for product
   live tests):
   a. SCAFFOLD_GENERATION (preceding the main capture of each
      document; per item 3c and PROTOCOL-009-REVISION-011 section 8):
      one bounded terminal call per scaffold section; registered
      prompt; isolated context; budget cap 402 calls; per-call
      metadata (numbers only) recorded in the manifest; failures
      handled per item 3d (document exclusion, no replacement).
   b. MAIN CAPTURE: for EACH selected document (G genuine + C
      controls), exactly ONE main-capture call on the pinned target
      configuration, under the product's intended use and the FROZEN
      007-m profile contract (configuration 0026a1a9..., prompt
      572cf2fb..., deployment profiles c79fd658.../0c4aa490...;
      Responses wire API non-streaming; complete stored main answer
      per LR-001; protocol limits 300 s / 2,000,000 bytes; one
      terminal attempt; no resampling; no retry). The assembled
      document (DASSLE block + scaffold sections, exactly as
      registered in item 3c) is the input; the stored main answer is
      the collected sample (a genuine target output).
   The authorized profile (both bases and the bearer) is read ONLY
   from the private 011b-identity credentials receipt (0600; the
   value is never committed, never logged, never echoed into any
   report or public artifact). Per sample: assembled input document
   + scaffold sections + main answer + call metadata stored privately
   under the private 011b-collection directory (0700; 0600 files;
   NEVER committed); the data-free per-sample metadata is recorded in
   the manifest (item 4). A call failure is recorded with its state
   (EXACT/CENSORED/UNAVAILABLE semantics preserved - missing or
   censored evidence is never reported as zero, LR-008/S-PRODUCT-02);
   a failed document is excluded from the stage set with the failure
   named; if exclusions drop the genuine-output count below the floor
   of 50, the round reports Result: BLOCKED on the named shortfall
   (no partial-quiet claim; the split and bookkeeping of the
   completed samples are still recorded truthfully). NO
   review/repair calls in this round (the review stage belongs to
   the 011-e comparators); NO second or larger GPU model; NO contact
   with any endpoint other than the designated target; NO server
   mutation.
8. Annotation guide and labeler packets (preparation only; the
   labelers are a 011-e input):
   a. Commit `research/target-distribution/ANNOTATION-GUIDE-011.md`
      (data-free; operationalizes PROTOCOL-009 (f)/(g)/(j)/(k) AS
      AMENDED BY PROTOCOL-009-REVISION-011): the reclassification
      label (development-distribution re-measurement) and the
      authorized-reuse disclosure; the exact taxonomy UNCHANGED in
      label names (source ground truth per scored DASSLE span:
      ACTUAL_ERROR, ACCEPTABLE_UNCHANGED, FULLY_CORRECT_DOCUMENT,
      NEEDS_WIDER_EDIT; intervention outcome per accepted edit:
      CORRECTS_ERROR, ACCEPTABLE_ALTERNATIVE, HARMLESS_STYLISTIC,
      HARMFUL_CHANGE, NO_CHANGE; layer-failure classes:
      PROTECTION_FAILURE, DETECTOR_MISS, CANDIDATE_GENERATION_MISS,
      RANKING_MISS, VALIDATOR_REJECTION_OR_FAILURE,
      ACCEPTANCE_POLICY_REJECTION, PATCH_FAILURE; mandatory
      DETECTOR_MISS on every genuine error not flagged); the GROUND-
      TRUTH RULE (the DASSLE human reference = source ground truth
      for DASSLE-derived spans; controls fully correct by
      construction; the labeler VERIFIES/ADJUDICATES the reference
      and does not create new ground truth); the SPAN-CORRESPONDENCE
      matcher (registered in the revision section 5: M = main answer
      truncated to 50,000 code points; candidates (1) verbatim input,
      (2) reference; difflib.SequenceMatcher autojunk=False
      find_longest_match; accept iff matched length >= 0.8 x
      candidate length; else UNALIGNABLE, named, excluded from span
      scoring, never reported as zero); the DISCARD RULE (scaffold
      blocks per the discard map are OUT_OF_SCOPE: never labeled,
      never scored; accepted edits outside scored spans recorded as
      OUT_OF_SCORED_SPANS, counted, never scored); the two-labeler
      procedure (two independent Slovenian-native labelers per
      scored span and per document; disagreement recorded; ambiguous
      cases adjudicated by the owner or a named human with a
      recorded rationale class; Qwen is NEVER the final judge of its
      own changes - PLAN 14.2); the calibration-pilot procedure
      (alignment only; never scored; labelers do not see internal
      stage decisions before final scoring); the metric-family
      denominators per PROTOCOL-009 (j) SCOPED TO DASSLE-SCORED
      SPANS (accepted-repair correctness over assessed accepted
      edits within scored spans; harmful interventions per 10,000
      originally-correct words with the frozen word counter over the
      reference text of the DASSLE blocks; detector coverage and
      final-repair coverage separately over genuine errors within
      scored spans; stylistic-only rate; preservation over FULLY_
      CORRECT controls' DASSLE blocks; operational cost components);
      the EXACT/CENSORED/UNAVAILABLE semantics (k); the recorded
      limitation (the waived technical/rare-name control floor; no
      scored technical-domain population).
      b. Prepare the labeler work queues under the private
      `011b-packets` directory (0700/0600; NEVER committed): the 5
      pilot packets, each containing the assembled input document,
      the collected main answer, the DISCARD MAP (block offsets;
      scaffold regions marked OUT_OF_SCOPE), the DASSLE reference
      for the scored span, and the frozen CPU detector's span output
      on that main answer (frozen detector, no intervention, no
      review call, no accepted edit, no scoring in this round); the
      per-span/per-document queue structure for the calibration and
      confirmation subsets (IDs and hashes only until 011-e opens
      them, applying the span-correspondence matcher first). Data-
      free aggregates (packet counts, file hashes) are committed
      with the manifest; no raw text is committed.
   9. Bookkeeping (data-free): (a) exactly one 011-d entry appended to
   `research/registry/experiments.json` (registry 39 -> 40; data-
   free; kind collection; status per the round outcome COMPLETE or
   BLOCKED; counts and partition sizes only; private locations
   referenced by relative directory names only); (b) machine-block
   counters registry_entries 39 -> 40 and oap_reports_reviewed 58 ->
   59 (the 011-d report file), frozen_report_history_incidents
   unchanged at 2; all identity fields UNCHANGED (no advance - that
   is a post-merge round's job); (c) STATUS.md round sentences; (d)
   `oap/GENERATED-FILES.json` scoped pin (same scope pattern as
   009-a/009-b/010-a/011-a/011-b/011-c, extended with this round's
   artifacts); (e) `research/tables/experiment-summary.csv` rebuild;
   (f) `research/RESEARCH-STATE.md` additive section 28 (the 011-d
   collection record: the reclassification label (development-
   distribution re-measurement), source verification (both DASSLE
   sha256), assembly census, selection draws, stage-1 sizes, domain
   mix (single domain, floor N/A with reason), split sizes, per-call
   statistics data-free (scaffold + main capture), identity
   reference (009-a pin hash + 011-c verdict), authorized-reuse
   disclosure (owner directive + consumption tiers), the recorded
   limitation (waived technical/rare-name control floor), private
   locations by relative name; NO rewrite of sections 1-27 or the
   machine block except item 9b).
10. Report-only final commit: sole parent = the literal
    implementation head; sole changed path
    `oap/reports/011-d-confirmation-stage1-collection.md`; the
    report discloses the final-head check state verbatim and, in the
    BLOCKED branches, the exact gate and named input with zero
    samples opened.
11. Final-head CI: all four required checks green at the final head
    (or the predeclared re-run state disclosed verbatim at report
    time, resolved before strategy's final-head review).
12. Push and verify; send the exact response OK and stop. PR #12
    stays OPEN; no merge; no auto-merge.

## Non-goals

- No evaluation, no scoring, no metric computation on the confirmation
  or calibration subset, no comparator run (ORIGINAL / DETECTOR_ONLY
  / DIRECT_QWEN_PROOFREADING / FROZEN_RESTRICTED_METHOD / CORPUS_ONLY
  all belong to 011-e).
- No annotation by any model or any human in this round (Qwen is
  NEVER the final judge; the two labelers are a 011-e input; the
  pilot is prepared but not scored).
- No metadata probe of any kind in this round (item 2; the bounded-
  probe budget was exhausted by 011-b/011-c by design).
- No behavior change of any frozen element (PROTOCOL-009 (n) no-
  tuning-after-unblinding, which covers the calibration subset too):
  candidate rule, ranking tuple, detector thresholds/eligibility,
  candidate semantics, validator prompt/parser/protocol, reasoning
  level, acceptance policy, protocol limits, retry policy,
  protection rules - all untouched; an operational finding that would
  suggest a behavior change STOPS the round and escalates.
- No PROTOCOL-009.md, DEPLOYMENT-IDENTITY-009.md, DEPLOYMENT-
  IDENTITY-011.md, or frozen-surface change (this round writes NO
  research/target-distribution/ identity bytes); no test change; no
  governance or CRITICAL.md change; no OAP protocol change.
- No merge, no auto-merge, no force-push, no release, no deployment,
  no milestone claim, no E2 re-opening (the designation stands).
- No contact with the RTX-3090 host (MUST-NOT-BE-STARTED; zero
  probes, zero calls), no contact with Deployment B
  (EXCLUDED_BY_HUMAN_OVERRIDE; zero probes, zero calls, ever), no
  second large GPU model, no server mutation.
- No LLM-generated "pure Slovenian" source documents (the LLM
  outputs ONLY the registered scaffold sections; the owner's
  mechanical-assembly constraint); no synthetic error injection; no
  model-assisted authoring or editing of any DASSLE text; no
  synthetic stand-in for genuine target outputs (the main answers
  ARE the genuine target outputs; the scaffold is registered,
  discarded scaffolding).
- No scoring, labeling, word counting, or denominator contribution
  from scaffold sections (the discard rule; OUT_OF_SCOPE
  everywhere); no fresh-confirmation, milestone, MVP, release, or
  deployment claim (re-measurement label; PLAN section 16 claims
  remain gated on a genuinely fresh, uninspected set later).
- No raw DASSLE text, no scaffold text, or main answer in any
  committed artifact, log, or report (PROTOCOL-009 section 4 as
  extended by the revision section 9).
- No raw confirmation text, no endpoint values, no credentials, no
  private absolute paths in any committed artifact or log
  (PROTOCOL-009 section 4; LR-013); the private tree is NEVER
  committed; the publication guard runs on the full tree pre-push.
- No re-labeling of collected documents, no re-sampling of the
  selected set, no renumbering of the pre-registered collection IDs
  or artifact names (continuity note item 5).

## Files and boundaries

Write (repository): exactly
`research/target-distribution/PROTOCOL-009-REVISION-011.md` (new;
the Scope item 3f bytes verbatim; additive - PROTOCOL-009.md stays
byte-frozen), `research/target-distribution/SCAFFOLD-GENERATOR-
PROMPT-011.md` (new; the Scope item 3f prompt bytes verbatim),
`research/target-distribution/ANNOTATION-GUIDE-011.md` (new, data-
free), `research/target-distribution/011b-collection-manifest.json`
(new, data-free), `research/RESEARCH-STATE.md` (additive section 28 +
machine-block counters only), `research/registry/experiments.json`
(+1 data-free entry), `STATUS.md`, `oap/GENERATED-FILES.json` (scoped
pin), `research/tables/experiment-summary.csv` (rebuild),
`oap/orders/011-d-confirmation-stage1-collection.md` (new,
activation), `oap/active` (pointer),
`oap/reports/011-d-confirmation-stage1-collection.md` (new, report-
only commit).
Write (private, never committed): `011b-collection/` (assembled
document inputs, scaffold sections, main-answer samples, per-call
metadata), `011b-packets/` (labeler work queues) - all under the
private research runtime root (0700/0600). `011b-intake/` is NOT
created (superseded by the mechanical-assembly model; stays
absent).
Read-only: the rest of the accepted tree and all frozen surfaces
(byte-verified in the pre-work gate); the private 009a-identity/,
011b-identity/ (the credentials receipt - the sole profile source for
the generation calls), and 011c-identity/ directories; the private
DASSLE source copy (campaign8 datasets location; byte-verified in
item 3a; never modified).
Coding read set: the compact sources, this order, RESEARCH-STATE
sections 13/24-28, PROTOCOL-009.md (full, frozen), DEPLOYMENT-
IDENTITY-009.md, DEPLOYMENT-IDENTITY-011.md (full, sections 1-6
byte-preserved), the frozen 007-m profile contract files, the private
011b-identity credentials receipt (identity values only as needed for
the generation calls), and the 011-b and 011-c reports.

## Requirements

1. Pre-work gates per Scope 1 (any mismatch BLOCKED and named).
2. The hard-gate identity record verified per Scope 2 (section 6
   byte-present with the REGIME-UNCHANGED verdict and observation
   window; zero probes executed in this round).
3. Source gate per Scope 3 (DASSLE byte verification; eligible
   inventories; mechanical assembly per the registered revision;
   BLOCKED-on-shortfall rule with the exact named shortfall; no
   re-escalation; recovery re-signal path recorded; discard map
   computed per document).
4. Manifest committed data-free BEFORE any sample is opened or any
   scaffold call made, per Scope 4 (assembly census, IDs, draws,
   partition, identity hash reference, call-metadata schema,
   authorized-reuse disclosure, discard map, scaffold-call census).
5. Selection per Scope 5 (single seeded PRNG instance; two draws in
   order (genuine, then control post-exclusion); domain-floor check
   recorded as N/A with the single-domain reason; the technical/
   rare-name draw waived and recorded).
6. Split and pilot per Scope 6 (pilot 5; k = ceil(0.15*N);
   confirmation untouched; partition recorded).
7. Generation per Scope 7 (scaffold calls per the registered class
   and budget; one terminal main-capture call per selected document
   under the frozen profile from the private credentials receipt;
   private storage; per-sample states preserved; floor-50 shortfall
   rule).
8. Annotation guide committed per Scope 8a (ground-truth rule, span-
   correspondence matcher, discard rule, scoped denominators,
   recorded limitation); pilot packets and queue structure prepared
   per Scope 8b (discard map + DASSLE reference in packets; CPU-
   detector spans only; no review calls; no scoring).
9. Bookkeeping per Scope 9 (registry 40; counters 40/59/2; STATUS.md;
   GENERATED-FILES pin; csv; RESEARCH-STATE section 28 additive).
10. Report-only commit per Scope 10; final-head CI per Scope 11 (all
    four required checks genuinely green); exact response OK per
    Scope 12 after remote verification; PR #12 stays OPEN.

## Acceptance criteria

1. The pre-work gate evidence is committed or recorded; any mismatch
   would have BLOCKED the round with the mismatch named.
2. The hard-gate precondition is verified by record, not by probe:
   section 6 of DEPLOYMENT-IDENTITY-011.md carries the REGIME-
   UNCHANGED verdict with the 011-c observation window, byte-
   identical to the base; this round executed ZERO metadata GETs.
3. PROTOCOL-009-REVISION-011.md and SCAFFOLD-GENERATOR-PROMPT-011.md
   are committed byte-exact (sha256 609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43 and
   005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc
   recorded in the manifest/report); PROTOCOL-009.md is byte-
   unchanged; the manifest is committed data-free and was created
   before the first sample was opened or any scaffold call made; it
   carries the assembly census, the exact PRNG mechanics (both
   instances), the partition, the identity hash reference, the
   authorized-reuse disclosure, and the discard map; the private
   samples are absent from the repository.
4. Stage-1 collection completed (or BLOCKED truthfully at the source
   gate or the floor-50 shortfall, with zero samples opened in the
   BLOCKED branches): both DASSLE sha256 re-verified at the byte
   level; G in [50, 100] genuine documents with the shortfall reason
   recorded when G < 100; C >= ceil(G/3) control documents (the
   technical/rare-name floor waived and recorded as a limitation);
   every selected document has exactly one terminal main-capture
   call with its state recorded (EXACT/CENSORED/UNAVAILABLE
   preserved) and its scaffold calls bounded by the registered
   budget; no underlying text appears in both arms (the registered
   exclusion).
5. The partition is exactly as specified (pilot 5, k = ceil(0.15*N)
   calibration, remainder confirmation); the confirmation subset is
   untouched beyond partitioning; the 5 pilot packets are prepared
   (assembled input + main answer + discard map + DASSLE reference +
   CPU-detector spans only).
6. ANNOTATION-GUIDE-011.md is committed, data-free, and complete
   against the PROTOCOL-009 (f)/(g)/(j)/(k) taxonomy, procedure, and
   denominators AS AMENDED BY PROTOCOL-009-REVISION-011 (ground-
   truth rule, span-correspondence matcher, discard rule, scoped
   denominators, recorded limitation).
7. Bookkeeping is complete and consistent (registry 40 with exactly
   one new 011-d data-free entry; counters 40/59/2; STATUS.md;
   GENERATED-FILES pin; csv; RESEARCH-STATE section 28 additive with
   sections 1-27 unaltered except the ordered counters).
8. The report-only commit has the literal implementation head as
   sole parent and the report path as sole changed path; the round
   diff (base..final) is limited to the released-from-freeze list;
   zero secret-pattern hits in added lines; the untracked residues
   absent from every commit; the private tree absent from every
   commit.
9. All four required checks genuinely green at the final head (no
   pending, cancelled, or reinterpreted check); the response OK frame
   received after remote verification.
10. PR #12 on oap/011-target-distribution-confirmation-study (base
    main at 4507cc78e333c0e48226b64266121171b7b8cea8) is still OPEN;
    no merge; no auto-merge.

## Verification

- Focused: research/tests/test_research_state_consistency.py (10/10
  green at the final head in a real checkout with origin/main =
  4507cc78e333c0e48226b64266121171b7b8cea8; at the implementation
  head exactly one designed red - the report-count assertion 59 vs
  58 - the 008-i/009-b/010-a/011-a/011-b/011-c pattern, recorded with
  the tested SHA); the 009-a focused lint (research/tests/
  test_009a_protocol_elements.py, unchanged, still green); the full
  research suite under the frozen uv environment; the OAP suite to
  the extent feasible on the degraded rclone/Dropbox FUSE mount (if
  a heavy fixture cycle cannot complete in the round window, record
  NOT RUN with the reason - the two OAP CI jobs are authoritative for
  those cycles, the 009-a/009-b/010-a/011-a/011-b/011-c precedent);
  one full local Application-baseline driver run (local evidence
  only; the recurring FUSE git-walk 30-s subprocess timeout in
  WhitespaceVerifier is a known environmental artifact - manual
  repro distinguishes it, the 011-a/011-b precedent).
- Data-free artifact checks: the manifest JSON parses and contains no
  raw-text fields (structural schema check + content-free field
  audit); the two new committed artifacts and the report pass the
  repository publication guard (full-tree scan) pre-push; strategy
  re-scans the published report privately post-publication (endpoint/
  credential/private-path/raw-text patterns) and records it in the
  review.
- Broader: the full CI battery at the implementation head and the
  final head.
- Evidence boundary: the live work is EXACTLY the bounded scaffold
  generation calls (registered class, budget cap 402) + the bounded
  per-document main-capture calls on the E2(b)-designated target
  (authorized by the owner E2(b) decision + PROTOCOL-009 element (a)
  as re-verified at 011-c + the owner's 2026-10-01 directive for the
  scaffold class; separately from REPAIR_ALLOW_LIVE_TESTS = NO which
  stays unchanged for product live tests); ZERO metadata probes; no
  other network calls, no other endpoints, no writes anywhere on the
  target. Software/test evidence and live-
  collection evidence are distinct layers (S-EVIDENCE-01). The
  report is a claim until strategy's independent final-head review
  re-verifies it field-by-field (S-REVIEW-01).

## Local setup and constraints

- The frozen uv environment; no new dependencies; no GPU on this
  host (the target is the remote designated A100-FP8 deployment; NO
  second large GPU model); no service touches; no protected Qwen
  weight/config/network change (S-PRODUCT-04); REPAIR_ALLOW_LIVE_
  TESTS stays NO; no endpoint value, credential, or private absolute
  path in any committed artifact or log.
- Private roots: 011b-collection/ (assembled inputs, scaffold
  sections, main answers, metadata), 011b-packets/ - 0700
  directories, 0600 files, native private root, never committed;
  009a-identity/, 011b-identity/, 011c-identity/ read-only; the
  DASSLE source copy read-only (item 3a); 011b-intake/ stays absent
  (superseded).
- Local: reversible setup inside the authorized workspace only;
  doctor runs with env -u CODEX_HOME -u OAP_ROLE; heavy test temp on
  native /home/ubuntu/.oap-scratch (0700) given the degraded FUSE
  mount; any unresolvable setup failure is BLOCKED and reported, not
  worked around.

## Documentation

- PROTOCOL-009-REVISION-011.md (Scope 3f) - the additive registered
  revision (mechanical assembly, reclassification, authorized-reuse
  disclosure, scaffold call class, discard rule, score scoping).
- SCAFFOLD-GENERATOR-PROMPT-011.md (Scope 3c/3f) - the registered
  scaffold prompt, byte-exact.
- ANNOTATION-GUIDE-011.md (Scope 8a) - the data-free labeler
  operationalization.
- 011b-collection-manifest.json (Scope 4) - the data-free collection
  manifest.
- RESEARCH-STATE.md additive section 28 (Scope 9f) - the canonical
  ledger entry for the stage-1 collection, plus the machine-block
  counters (Scope 9b).
- STATUS.md per Scope 9c; the OAP report per the round mechanics
  (data-free by construction: counts, IDs, domain tags, hashes,
  verdict references; no raw text, no endpoint values, no
  credentials; the round's classification recorded: D0 execution of
  the pre-registered collection; no CRIT admission).

## Git and report publication

- Branch `oap/011-target-distribution-confirmation-study` (EXISTING;
  verified at 47c4da8bf7016614cd62d2448e72f3f7249d0803, PR #12 OPEN,
  base main at 4507cc78e333c0e48226b64266121171b7b8cea8). This round
  AMENDS PR #12; no new branch, no new PR, no force-push.
- Activation commit (order + oap/active) per the round mechanics
  (including the established FUSE stale-stat pre-staging workaround
  if the environment requires it, recorded in the round report);
  implementation commits per Scope 3-9 (exact split at the executor's
  discretion, all within the released-from-freeze list); the report-
  only commit per Scope 10 (sole parent = literal implementation
  head; sole changed path = the report).
- Push semantics per the OAP communication profile; no push after
  the report-only commit; the exact response OK after remote
  verification; the coding wrapper consumes the 011-d control signal
  exactly once before model launch.
- No merge: PR #12 stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act at the objective's end (S-
  MERGE-01; repository-approved method: standard merge commit at the
  exact reviewed SHA, verify-merge, default-branch check) - not in
  this round.

## Decision classification

D0 (S-DECIDE-01): the round executes the pre-registered stage-1
collection specification (published in the 011-b order, byte-
preserved) AS AMENDED by the owner's standing 2026-10-01 DASSLE
directive (private decision receipt) and the registered additive
revision (Scope 3f), on the identity re-verified at 011-c, under the
owner's standing E2(b) authorization; the intake escalation was
consumed and is moot (no re-escalation); every mechanical choice is
the unique transcription of the ordered procedure - no judgment
debt, no CRIT admission (S-DECIDE-03 condition 1 fails: the frozen
protocol as amended, the published 011-b specification, the 011-c
verdict record, and the owner directive leave no unresolved choice).
A BLOCKED-on-shortfall outcome is a truthful stop that hands the
named finding to the human boundary - it is a stop, not a decision.

## Deferred human adjudication

- Decision: NONE

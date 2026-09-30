# 009-a: Pre-registered frozen protocol for the fresh human-labelled target-distribution confirmation study (objective 009, round 1; data-free scoping, deployment-identity record, no confirmation data, no tuning)

Status: FINAL

Finalized by strategic reconciliation of 2026-09-30: quiescent post-merge
checkpoint of objective 008 (independent verification of remote main =
185dc3d9c654991619ae5c57b64e0c54f4550a16 / PR #9 MERGED, OAP_ACCEPTED_REF
refreshed from the objective-007 base 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9
to the accepted merge, OAP state reconciled), and the owner 2026-09-30
instruction to start objective 009 with a preregistration/scoping round. The
new PR identity is not invented (CREATE_NEW_PR); it is created by the coding
round. All content is finalized from the owner 2026-09-30 instruction, PLAN
sections 14.2/14.3/15.2/16, RESEARCH-STATE sections 3/9/13/14, and the
independent checkpoint verifications of this session.

```oap-metadata
{
  "id": "009-a",
  "title": "Pre-registered frozen protocol for the fresh human-labelled target-distribution confirmation study (objective 009, round 1; data-free scoping, deployment-identity record, no confirmation data, no tuning)",
  "objective": "009",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "185dc3d9c654991619ae5c57b64e0c54f4550a16",
  "branch": "oap/009-target-distribution-confirmation",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": ["007", "008"],
  "local_work": "Preserve byte-for-byte: every merged 000-008 seam on main; the entire research/ tree at accepted main 185dc3d9c654991619ae5c57b64e0c54f4550a16, including all 007 and 008 round artifacts (orders, reports, registry entries, manifests, seals, corpus, results, tables, configs), the frozen 007-m linguistic surfaces (research/configs/007-m-rank-ambiguous-levenshtein-candidates.json sha256 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration sha256 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt sha256 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, frozen deployment profiles sha256 c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py sha256 c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py sha256 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json sha256 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json sha256 f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json sha256 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, and any unrelated local work (untracked residue never committed). Released from freeze for this round ONLY: research/target-distribution/PROTOCOL-009.md (new; the pre-registered frozen protocol, data-free), research/target-distribution/DEPLOYMENT-IDENTITY-009.md (new; the data-free deployment-identity record and E2 decision package), research/tests/test_009a_protocol_elements.py (new; data-free structural lint of the two documents), research/registry/experiments.json (append exactly one 009-a entry), research/RESEARCH-STATE.md (additive section 22 plus machine-block counters only: registry_entries 33 to 34 and oap_reports_reviewed 52 to 53; identity fields unchanged), STATUS.md (round sentences), oap/GENERATED-FILES.json (scoped pin), research/tables/experiment-summary.csv (rebuild), oap/orders/009-a-target-distribution-confirmation-preregistration.md (new, activation), oap/active (pointer), oap/reports/009-a-target-distribution-confirmation-preregistration.md (new, report-only commit).",
  "prior_review": "Strategy independent final-head review of 008-i (2026-09-28, private workorders/008-i-final-head-review-20260928.md): verdict PASS, all 12 criteria MET; report-only commit 59d8f030a91309f4386bde48b360f17d7ea11e86 (sole parent b9d44911638068ae213a265f5f42d0b4818e5175, sole changed path oap/reports/008-i-corrective-scope-and-v4-final-blind-acceptance.md); verify_report remote scope = verified; all four required checks green at the final head (Application baseline run 35817046687, Research reproducibility run 35817046682, OAP bootstrap acceptance plus OAP report history run 35817046828; Application baseline job 107040689790: 13/13 commands PASSED under the owner-approved 600 s CI per-command cap, zero timeouts); whole-round diff 954d758..59d8f03 audited by strategy diffscope = PASS (out_of_scope=0, frozen_ok=True); v4 seal re-hashes 4076/4076 pre and post; pool overlap zero; CI-1 pinned bytes exact; zero secret-pattern hits; deployment side-effect check negative (all three workflows pull_request-to-main only); D1-1/D1-3/D1-4/D1-5 CLEARED; D1-6 registered (the published report criterion-13 citation carries a one-hex-digit error, 5f08 versus the order-pinned 5f98; the actual bytes satisfy the order pin exactly; non-gating); CRITICAL NONE (register seed-identical); strategic_gate at the reviewed SHA = structural development gate valid. Development-only merge of PR #9 at the exact reviewed SHA (standard merge commit; merge commit 185dc3d9c654991619ae5c57b64e0c54f4550a16, parents 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 plus 59d8f030a91309f4386bde48b360f17d7ea11e86; verify-merge: merged true, default head 185dc3d9c654991619ae5c57b64e0c54f4550a16, deployment_authorized false; PR #9 MERGED 2026-09-28T03:30:43Z). Quiescent post-merge checkpoint (2026-09-30, this session): remote default branch re-verified at 185dc3d9c654991619ae5c57b64e0c54f4550a16; OAP_ACCEPTED_REF refreshed from 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 to 185dc3d9c654991619ae5c57b64e0c54f4550a16 (backup runtime.env.bak-20260930-pre009 preserved); all sixteen governance identities independently re-computed against the merge blobs (zero mismatch); worktree reconciled to the accepted head. Owner instruction 2026-09-30: the D1-6 report-citation typo is closed by the review-of-record (the immutable report is not rewritten; no 008-j); the diffscope_008i.py --commit-only defect (worktree-versus-commit instead of commit-versus-parent) and the driver subprocess-tree timeout-kill observation (the CI log shows pytest completing after the nominal timeout) are recorded as non-gating technical debt for a future bounded maintenance round if and when they become relevant; objective 009 starts with a new branch/PR from accepted main; 009-a is a preregistration/scoping round for the fresh human-labelled target-distribution confirmation (not a tuning round, not immediate consumption of the final confirmation sample); PLAN sections 14.2/14.3 remain authoritative; the target-deployment question must be resolved before confirmation data are spent (if the intended RTX-3090 configuration is available, pin and verify its exact model/quantization/API/runtime identity before collection; otherwise stop at the D2 boundary and present concrete alternatives; never silently run the confirmatory study on A100-FP8 and call it target-distribution evidence); after 009-a passes independent review and CI the loop continues into collection/annotation/evaluation under subsequent proof-sized suffixes without the owner as terminal relay, escalating only genuine human/D2 decisions.",
  "provenance": [
    {"kind": "H", "reference": "Owner instruction 2026-09-30 (objective 009 start), nine elements: (1) quiescent post-merge checkpoint first - independent verification of main = 185dc3d9c654991619ae5c57b64e0c54f4550a16 / PR #9 merged, OAP_ACCEPTED_REF refresh from the objective-007 base, OAP state check before any new order; (2) no 008-j (the 008-i report-citation typo is already corrected by the independent review-of-record; the immutable report is not rewritten); (3) record the diffscope_008i.py --commit-only defect and the driver subprocess-tree timeout-kill observation as non-gating technical debt for a future bounded maintenance round if/when relevant; (4) new objective 009 branch/PR from accepted main; 009-a is a preregistration/scoping round for the fresh human-labelled target-distribution confirmation, not a tuning round and not immediate consumption of the final confirmation sample; (5) before collecting confirmatory examples, freeze the protocol with these exact elements: exact target deployment/model identity; sampling population and deterministic/randomized collection procedure; domain mix; first-stage sample size and expansion criteria; correct-text negative controls; annotation taxonomy including actual error, acceptable alternative, harmless stylistic preference, harmful change, needs-wider-edit/non-local case and protection-related failure; independent human adjudication procedure; calibration versus untouched confirmation split; comparator methods required by PLAN 14.2; metrics and denominators; uncertainty intervals; stopping/falsification rules; failure decomposition protection -> detector -> candidate generation/ranking -> validator -> acceptance -> patch; explicit no-tuning-after-unblinding rule; (6) PLAN 14.2/14.3 authoritative: initial study approximately 50-100 genuine outputs of the target configuration, later expansion toward approximately 100-500 across domains; fully correct Slovenian text including technical language, rare expressions and names; threshold/calibration cases separate from the final test set; compare at least original, detector-only, direct Qwen proofreading and the frozen restricted method; report accepted-repair correctness, harmful interventions per 10,000 originally-correct words, coverage and operational cost; the approximately 99 percent accepted-repair correctness and at most 1 harmful intervention per 10,000 correct words are evaluation/calibration targets, not automatic release authorization; (7) resolve the target-deployment question before confirmation data are spent: PLAN identifies the target as the strongly quantized Qwen3.8-27B on RTX 3090; the 007 evidence came from A100-FP8 and is not deployment-equivalent; if the intended RTX-3090 configuration is available, pin and verify its exact model/quantization/API/runtime identity before collection; if unavailable or changed, stop at the D2 boundary and present concrete alternatives; do not silently run the confirmatory study on A100-FP8; (8) the frozen system entering 009 is the accepted objective-008 structural protection layer plus the frozen 007-m linguistic method; no retuning of ranking, detector thresholds, candidate semantics, validator prompt/parser, reasoning level, acceptance policy or protection rules against the future confirmation set; (9) after 009-a passes independent review/CI, continue the OAP loop into data collection/annotation/evaluation under subsequent proof-sized suffixes without the owner as terminal relay; escalate only genuine human/D2 decisions. Prior durable human inputs: the 2026-09-17 research decision (009 design parameters: fresh human-labelled confirmation, two-labeler adjudication with owner or named-human adjudication of disagreements, Qwen never final judge of its own changes, target deployment per the E2 resolution, no tuning against the confirmation set, data-free public posture, explicit rights and controlled storage); the 2026-09-20 out-of-band generation-endpoint note (the 007-lineage deployment identity is provided out-of-band; no endpoint value or credential material in any committed artifact); the 2026-09-22 Option A1 CI decision (008 history only)."},
    {"kind": "A", "reference": "PLAN.md v1.0 (protected bytes): header line 6 target-deployment identification (Ciljna namestitev: obstoječi, močno kvantizirani Qwen3.8-27B na RTX 3090); section 14.2 (approximately 50-100 real target outputs first, expansion to approximately 100-500 across domains; per-case labels of actual errors, acceptable alternatives, stylistic-only preferences and non-locally-repairable places; fully correct Slovenian material including technical language, rare expressions and names; calibration cases separate from the final test set; human review of ambiguous repairs and Qwen never final judge of its own changes; compare at least original, corpus detector without intervention, direct Qwen proofreading as comparator and the agreed restricted procedure; optional corpus-only research arm; comparator proofreading is not production architecture); section 14.3 (accepted-repair correctness with the assessed count; harmful interventions per 10,000 originally-correct words with stylistic-only changes separate; coverage detector-versus-finally-repaired; operational cost; approximately 99 percent and at most 1 per 10,000 are calibration targets, not automatic release authorization; zero events in a small sample is not proof of a zero rate, the 3/N 95 percent upper bound at zero events, approximately 30,000 correct words needed for a bound near 1 per 10,000, intra-document correlation caution); section 15.2 (M01 initial labelled set with correct controls and a separate threshold part; M04 calibration of acceptance; M07 comparative report); section 16 (MVP criteria; measured quality on cases that did not serve development). ARCHITECTURE.md v1.1: section 15 protected environment (shared GPU, services, ports, no second large model); sections 16.2/16.3 evidence layers and the deployment boundary. RESEARCH-STATE.md: section 3 (exact frozen 007-m identity), section 9 (deployment-validity matrix: PLAN target remains authoritative; A100-FP8 is a different regime; E2 open with resolutions (a)/(b)), section 13 (objective 009 reserved design), section 14 (no-tuning boundary, verbatim list), section 15 (merge/release/deployment limitations). Concentrated OAP / this constitution: S-ORDER-01/02/03 (one objective one coherent proof-sized PR; exact order contract; ID grammar; objective sequencing after the accepted merge), S-EVIDENCE-01 (evidence layers; distinct PASSED/FAILED/SKIPPED/NOT RUN/BLOCKED/PENDING/MISSING), S-DECIDE-04 (D2 boundary: protected Qwen/network/deployment changes; bounded isolated preparation allowed while the real boundary stays blocked), S-ICA-01/02 (evaluation evidence distinct from deployment authority; fresh-context audit before closure), S-PRODUCT-02/03/04 (statistical independence; preservation semantics; protected environment). OAP-COMMUNICATION-strategic sections 4/5/6/7/11 (one-PR continuity; finalized work-order contract; atomic publication and exact FIFO; coding publication and SELF; operator commands)."},
    {"kind": "E", "reference": "Observed facts: (1) the intended RTX-3090 endpoint is TCP-closed at the 2026-09-09 reconnaissance (private reconnaissance record; the endpoint is marked must-not-be-started/reconfigured; no probing is possible or permitted in this round); (2) the A100-FP8 deployment (the out-of-band 007-lineage identity) is reachable and its identity was re-confirmed live on 2026-09-29T23:12Z (serving framework vLLM 0.28.0; model identifier qwen3.8-27b; model root ending Qwen3.8-27B-FP8; max model length 262144; Responses wire API non-streaming), matching the frozen 007 profiles (profile sha256 c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e); (3) Deployment B remains EXCLUDED_BY_HUMAN_OVERRIDE (no probes, no calls, ever); (4) the accepted objective-008 structural protection layer (final objective-008 verdict PASS at the 008-i census; v4 hidden set 4076/4076 sealed; zero out-of-scope diff; dev regression within the pre-declared bound) is the structural precondition entering 009; (5) no attributable human decision redefining the intended production target exists in the durable records (RESEARCH-STATE section 9); (6) the entire 007 live evidence base is A100-FP8 regime and does not transfer to the intended deployment without replication."},
    {"kind": "I", "reference": "Strategy checkpoint verifications of this session (2026-09-30): remote default branch main = 185dc3d9c654991619ae5c57b64e0c54f4550a16 (merge commit, parents 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 plus 59d8f030a91309f4386bde48b360f17d7ea11e86); PR #9 state MERGED (2026-09-28T03:30:43Z); OAP_ACCEPTED_REF = 185dc3d9c654991619ae5c57b64e0c54f4550a16 in runtime.env (prior value 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 preserved in runtime.env.bak-20260930-pre009); all sixteen governance identities independently re-computed from the 185dc3d9 blobs and matching oap/governance/MANIFEST.json at that ref (zero mismatch); CRITICAL.md seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e with zero entries; registry 33 entries (last 008-i PASS); machine block registry_entries 33 / oap_reports_reviewed 52 / frozen_report_history_incidents 2 with identity fields frozen at the 007 review point; frozen-surface hashes re-computed at the accepted ref (prose_boundary.py c57e2901e52af962..., protected.py 27f22eaee129190b..., policy v5 915f70d34ecc69ab..., policy v4 f564d9f87ef01a89..., experiment-008i.json 24e25edafbbf0b1d..., 007-m config projection 41e1482a9ee100f5...); the coding wrapper idle on control.fifo (last consumed round 008-i); the 008-i final-head review of record (private workorders/008-i-final-head-review-20260928.md) and the publication/merge execution record (private workorders/008i-publication-runbook-20260920.md)."}
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

Round 1 of objective 009 - the fresh, untouched, human-labelled
target-distribution linguistic confirmation of the complete effective
pipeline (reserved since RESEARCH-STATE section 13). This is the
preregistration/scoping round: it freezes the complete study protocol as a
committed data-free document, records the current deployment-identity state
as a data-free decision package for the open E2 human decision, and creates
the objective-009 branch/PR from accepted main. It is not a tuning round, it
consumes no confirmation sample, and it performs no confirmation data
collection, annotation, or evaluation. The new PR identity is not invented
(CREATE_NEW_PR); it is created by the coding round.

## Provenance

- H: as metadata provenance H (owner 2026-09-30 instruction, all nine
  elements; prior durable human inputs 2026-09-17/20/22).
- A: as metadata provenance A (PLAN sections 14.2/14.3/15.2/16 and header
  line 6; ARCHITECTURE sections 15/16.2/16.3; RESEARCH-STATE sections
  3/9/13/14/15; constitution clauses S-ORDER-01/02/03, S-EVIDENCE-01,
  S-DECIDE-04, S-ICA-01/02, S-PRODUCT-02/03/04; OAP-COMMUNICATION-strategic
  sections 4/5/6/7/11).
- E: as metadata provenance E (RTX-3090 TCP-closed reconnaissance of
  2026-09-09; live A100-FP8 identity re-confirmation of 2026-09-29T23:12Z
  matching the frozen 007 profiles; Deployment B exclusion; accepted
  objective-008 structural precondition; no attributable target redefinition;
  007 evidence base entirely A100-FP8 regime).
- I: as metadata provenance I (this session's checkpoint verifications; the
  008-i final-head review of record; the publication/merge execution
  record).

## Current verified state

Refreshed at publication (2026-09-30 CEST, this session): remote default
branch main = 185dc3d9c654991619ae5c57b64e0c54f4550a16 (merge commit;
parents 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 and
59d8f030a91309f4386bde48b360f17d7ea11e86), re-verified in this session via
the read-only remote API and ls-remote; PR #9 merged (merged_at
2026-09-28T03:30:43Z, merge_commit_sha
185dc3d9c654991619ae5c57b64e0c54f4550a16); zero open PRs; no PR or branch
oap/009-target-distribution-confirmation exists yet; OAP_ACCEPTED_REF =
185dc3d9c654991619ae5c57b64e0c54f4550a16 in runtime.env (prior value
7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 preserved in
runtime.env.bak-20260930-pre009); worktree reconciled to the accepted head
(git checkout main plus merge --ff-only origin/main, both RC=0, 6382 file
updates, workorders/checkout-009-prep.log and workorders/ffmerge-009.log)
and re-verified in this session: HEAD =
185dc3d9c654991619ae5c57b64e0c54f4550a16 on main, a fresh full
git status --porcelain pass at 2026-09-30T02:32:38+02:00 (RC=0,
workorders/status-recheck-009a-20260930-023238.log) clean except the three
known untracked residues (corpus/ 4907 files, .research-test-scratch/ 33
files, .rclone-speed-test/ 200 files, per the incident audit); note: on
2026-09-30 a Dropbox sync deleted a subset of the objective-008 worktree
files; all restored from the intact Git object DB; no committed data loss;
private research roots are on native disk outside the sync mount; incident
recorded in workorders/incident-009a-prep-20260930.md; oap/active = 008-i
(this order activates 009-a); the coding wrapper is idle on control.fifo
(consumed.json = 008-i, recovery false; publication.json = the 008-i
remote-verified record); CRITICAL.md seed-identical
a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e, zero
entries; registry 33 entries (last 008-i PASS); machine block
registry_entries 33 / oap_reports_reviewed 52 /
frozen_report_history_incidents 2 with identity fields frozen at the 007
review point; all sixteen governance identities independently re-computed
from the accepted base blobs in this session (zero mismatch against
oap/governance/MANIFEST.json at
185dc3d9c654991619ae5c57b64e0c54f4550a16 and against this order's
governance mapping); frozen surface hashes independently re-verified in
this session at the accepted base (prose_boundary.py
c57e2901e52af962..., protected.py 27f22eaee129190b..., policy v5
915f70d34ecc69ab..., policy v4 f564d9f87ef01a89...,
experiment-008i.json 24e25edafbbf0b1d..., 007-m config projection
41e1482a9ee100f5...); local pre-publication gates (env -u CODEX_HOME -u
OAP_ROLE, this session): check_state local scope =
PUBLICATION_RECONCILIATION_REQUIRED (id 008-i; the expected conservative
pre-remote label), check_state remote scope = REVIEW_READY (id 008-i, pr
9), check_governance accepted-runtime at
185dc3d9c654991619ae5c57b64e0c54f4550a16 with strategic-home = valid
(coding_bytes 35076), check_transcript --revision HEAD = valid (revision
185dc3d9c654991619ae5c57b64e0c54f4550a16; active 008-i; 53 orders / 53
reports; three known quarantined historical reports 007-d/007-n/008-d with
corrective rounds 007-e/007-o/008-e; report history valid with the two
frozen known historical incidents); deployment facts: A100-FP8 identity
live re-confirmed 2026-09-29T23:12Z (vLLM 0.28.0; model identifier
qwen3.8-27b; model root ending Qwen3.8-27B-FP8; max model length 262144;
Responses wire API non-streaming) matching the frozen 007 profiles (sha256
c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and
0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e,
out-of-band private files); the intended RTX-3090 endpoint is TCP-closed
per the 2026-09-09 reconnaissance record (zero probes and zero calls in
this round); Deployment B EXCLUDED_BY_HUMAN_OVERRIDE (no probes, no calls,
ever); REPAIR_ALLOW_LIVE_TESTS = NO unchanged.

## Governance

The sixteen source identities in the metadata governance mapping are the
exact identities of `oap/governance/MANIFEST.json` at the accepted base
185dc3d9c654991619ae5c57b64e0c54f4550a16; strategy independently re-computed
all sixteen from the base blobs on 2026-09-30 (zero mismatch). Any future
mismatch blocks publication.

### Non-gating technical debt (recorded per owner 2026-09-30; out of scope
### for this objective; future bounded maintenance round if/when relevant)

- `strat-verify-tmp/diffscope_008i.py` `--commit-only` mode is defective: it
  compares the worktree against the named commit, not the commit against its
  parent. The 008-i report-commit invariants were therefore verified
  directly with git (sole parent b9d44911638068ae213a265f5f42d0b4818e5175;
  sole path A oap/reports/008-i-...). Recorded, no action in this objective.
- The development-baseline driver timeout path kills the immediate subprocess
  rather than demonstrably the complete descendant process tree; the CI logs
  of the pre-Option-A1 reruns showed pytest completing successfully shortly
  after the nominal 300 s timeout. Separate harness-hardening debt, recorded
  per the owner 2026-09-22 decision and the 2026-09-30 instruction; no
  action in this objective.
- D1-6 (the 008-i report criterion-13 citation carries a one-hex-digit
  error, 5f08 versus the order-pinned 5f98; actual bytes satisfy the order
  pin exactly) is closed by the review-of-record per the owner 2026-09-30
  instruction. The immutable 008-i report is not rewritten. No 008-j exists
  or is created.

## Goal and dependencies

Goal: freeze the scientifically defensible, preregistered protocol for the
fresh human-labelled target-distribution confirmation study (the reserved
objective 009 per RESEARCH-STATE section 13), together with the data-free
deployment-identity record that frames the open E2 human decision, so that
subsequent proof-sized suffixes (009-b onward: collection, annotation,
evaluation, comparative report) can execute the frozen protocol without any
protocol change. The 009 line maps to the PLAN section 15.2 work groups M01
(initial labelled set with correct controls and a separate
threshold/calibration part), M04 (calibration of acceptance - here
pre-registered, never executed against the confirmation set) and M07
(comparative report). The project phase token remains DEMONSTRATOR,
continuous from 000-008.

Dependencies: 007 (the frozen 007-m linguistic method) and 008 (the accepted
structural protection layer at the 008-i census). Neither is re-opened by
this objective: the frozen system enters 009 exactly as accepted.

## Scope

1. Pre-work integrity gates (data-free): at the base commit, byte-verify
   every frozen surface listed in the metadata local_work field (all pinned
   sha256 values); registry = 33 entries with the last 008-i PASS; machine
   block registry_entries 33 / oap_reports_reviewed 52 /
   frozen_report_history_incidents 2 with the identity fields unchanged;
   CRITICAL.md seed-identical
   a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e; the
   four required checks green at the accepted base head (the 008-i final
   head set). Any mismatch is BLOCKED with the mismatch named; no work
   proceeds.
2. Commit the preregistered frozen protocol
   `research/target-distribution/PROTOCOL-009.md` (data-free; the single
   source of truth for 009-b onward) with exactly these pre-registered
   elements:
   - (a) Target deployment/model identity (HARD GATE): the target
     configuration is the PLAN-identified intended deployment (strongly
     quantized Qwen3.8-27B on RTX 3090, PLAN header line 6). Confirmation
     collection is authorized only from a deployment whose pinned identity
     (model identifier, quantization, serving framework and version, wire
     protocol, max model length, endpoint class) matches the
     owner-designated target. The 007 evidence regime (A100-FP8, model
     qwen3.8-27b, Responses non-streaming, vLLM 0.28.0 observed) is NOT
     deployment-equivalent, and no 007 live result transfers to the intended
     deployment without replication (RESEARCH-STATE section 9). Until the
     owner resolves E2 with an attributable decision, no confirmation data
     is collected from any deployment and the loop idles at that boundary.
   - (b) Sampling population and collection procedure: genuine
     Slovenian-language outputs of the pinned target configuration,
     generated under the product's intended use (complete stored main
     answers per LR-001), plus human-authored fully-correct control
     documents under explicit rights and controlled storage; no synthetic
     stand-in may replace genuine target outputs in the confirmation
     population; a collection manifest is created BEFORE the first sample is
     opened (collection IDs, domain tags, source kind, collection
     timestamps, pinned deployment identity reference, private-root file
     hashes - content-free); within the genuine-output population, selection
     uses a seeded PRNG (seed fixed in this protocol) applied to the
     eligible inventory to avoid selection bias; the manifest is committed
     data-free.
   - (c) Domain mix: pre-declared domain tags (general Slovenian prose;
     technical language; a mix including rare expressions and proper names;
     any further domains the owner adds at E2 resolution); per-stage minimum
     counts per domain pre-registered (no domain below 10 percent of stage
     size at stage 1; a violation triggers expansion, never re-labeling).
   - (d) First-stage size and expansion criteria: stage 1 = 50-100 genuine
     outputs (target 100, floor 50 with the reason for any shortfall
     recorded at collection); stage 2 expansion toward 100-500 (target 300,
     cap 500) across domains, triggered only by the pre-registered
     criteria: (i) the stage-1 accepted-repair correctness 95 percent CI is
     too wide to decide against the approximately 99 percent calibration
     goal; (ii) a pre-registered domain is under-represented against its
     minimum count; (iii) the stage-1 operational failure rate exceeds the
     pre-registered stop threshold of Scope item 2(l)(d). Expansion adds
     only fresh, uncollected, unopened samples from the same pinned target
     configuration; no re-sampling, no re-collection, no method change.
   - (e) Correct-text negative controls: pre-registered quota - at least 25
     percent of stage-1 documents are FULLY_CORRECT controls (fully correct
     Slovenian text including technical language, rare expressions and
     proper names, PLAN 14.2), of which at least 10 are human-authored
     technical/rare/name documents; controls carry the harm-rate denominator
     (originally-correct words) and the preservation metrics.
   - (f) Annotation taxonomy (exact labels, pre-registered): source ground
     truth per span/document - ACTUAL_ERROR (genuine error in the target
     span), ACCEPTABLE_UNCHANGED (acceptable as-is), FULLY_CORRECT_DOCUMENT
     (control document), NEEDS_WIDER_EDIT (genuine error whose correct fix
     is non-local); intervention outcome per accepted edit - CORRECTS_ERROR,
     ACCEPTABLE_ALTERNATIVE (acceptable alternative rendering; no error
     fixed; optional change), HARMLESS_STYLISTIC (unnecessary but harmless
     stylistic preference), HARMFUL_CHANGE (correct text made incorrect or
     semantically different), NO_CHANGE; layer-failure classes -
     PROTECTION_FAILURE (the frozen v5 protection layer exposed or
     over-protected against policy, with byte-level attribution),
     DETECTOR_MISS, CANDIDATE_GENERATION_MISS, RANKING_MISS,
     VALIDATOR_REJECTION_OR_FAILURE, ACCEPTANCE_POLICY_REJECTION,
     PATCH_FAILURE; a mandatory DETECTOR_MISS label on every genuine error
     not flagged by the detector.
   - (g) Independent human adjudication procedure: two independent human
     labelers (Slovenian-native; trained on the committed data-free
     annotation guide before first label) per detected span and per document;
     the two-labeler disagreement is recorded; ambiguous cases are
     adjudicated by the owner or a named human with a recorded rationale
     class; Qwen is never the final judge of its own changes (PLAN 14.2); a
     5-document calibration pilot (genuine outputs, excluded from the
     confirmation set and the calibration subset) aligns the labelers before
     labeling starts and is never scored or used for method decisions;
     labelers do not see internal stage decisions before final scoring.
   - (h) Calibration versus untouched confirmation split: at collection
     time, before any opening, a document-level split fixed by a
     deterministic rule on collection IDs (15 percent calibration / 85
     percent confirmation, rounded by the pre-registered rule); the
     calibration subset is used only for operational verification of the
     frozen pipeline on the target configuration (call/parse/patch
     mechanics) and never for behavior change - a verification failure that
     suggests a behavior change stops the round and escalates; the
     confirmation subset is untouched until final scoring; zero leakage
     between subsets or with any 007/008 material (the 009 confirmation
     population contains no case generated or inspected for any earlier
     objective).
   - (i) Comparator methods (PLAN 14.2, required): ORIGINAL (unmodified);
     DETECTOR_ONLY (CPU detector, no intervention); DIRECT_QWEN_PROOFREADING
     (one fresh bounded request per document under a pre-registered
     comparator protocol, isolated context, settings recorded; explicitly
     not the production architecture); FROZEN_RESTRICTED_METHOD (the
     complete frozen system: 007-m linguistic method plus the 008
     protection layer); optional research arm CORPUS_ONLY (corpus repair
     without Qwen adjudication) may be enabled by a recorded budget
     decision and never blocks the required four.
   - (j) Metrics and denominators: (1) accepted-repair correctness =
     CORRECTS_ERROR edits / all assessed accepted edits, with the assessed
     count reported and a 95 percent Clopper-Pearson interval; (2) harmful
     interventions per 10,000 originally-correct words = 10000 x
     HARMFUL_CHANGE count on originally-correct spans /
     originally-correct word count (frozen word counter), with the 3/N
     95 percent upper bound at zero events and the intra-document
     correlation caution; (3) coverage, reported separately: detector
     coverage = genuine errors flagged / all genuine errors; final-repair
     coverage = genuine errors finally repaired as CORRECTS_ERROR / all
     genuine errors; (4) stylistic-only rate = (ACCEPTABLE_ALTERNATIVE +
     HARMLESS_STYLISTIC) assessed edits / all assessed accepted edits, a
     separate metric; (5) preservation: unchanged-correct-document rate
     over FULLY_CORRECT controls, and edit units introduced on
     originally-correct text per 10,000 correct words; (6) operational
     cost: review-call rate (answers with at least one repair call / all
     answers), token totals per answer (main and repair separately),
     p50/p95 latency with and without repair, failure/timeout rate per
     attempt.
   - (k) Uncertainty intervals: 95 percent Clopper-Pearson for all
     proportions on their assessed denominators; the 3/N upper bound for
     zero-event rates; no pooling of different-scope counts;
     EXACT/CENSORED/UNAVAILABLE evidence states preserved - missing or
     censored evidence is never reported as zero (LR-008/S-PRODUCT-02
     semantics).
   - (l) Stopping/falsification rules (pre-registered): (a) stop and report
     if accepted-repair correctness falls materially below the
     approximately 99 percent goal with an assessed count large enough that
     the 95 percent CI decides it - no rescue tuning (any mechanism change
     requires a new objective, fresh data, and a new PR); (b) every
     established HARMFUL_CHANGE is reported individually with full
     attribution; the study falsifies the strict-mode harm goal when the
     one-sided 95 percent lower bound of the harmful rate exceeds 1 per
     10,000 originally-correct words; zero events at small N are always
     reported as upper bounds, not achievement (the 1 per 10,000 bound
     needs approximately 30,000 correct words at zero events); (c) if
     final-repair coverage is negligible relative to genuine-error
     incidence, the round reports the coverage limitation with the measured
     benefit/harm statement (PLAN 14.3: lower coverage is acceptable if the
     measured benefit is clear and harm is small); (d) stop and report if
     the operational failure rate makes the service path unreliable
     (pre-registered threshold: more than 5 percent of attempts as distinct
     conservative failures, or a deterministic repeated transport failure).
     A pass does not auto-accept the MVP; it enables the human milestone
     decision (S-ICA).
   - (m) Failure decomposition: every genuine error not finally repaired is
     assigned exactly the first failing stage in the order
     PROTECTION_LAYER -> DETECTOR -> CANDIDATE_GENERATION -> RANKING ->
     VALIDATOR -> ACCEPTANCE_POLICY -> PATCH, using the layer-failure
     classes of (f); a low end-to-end recall must stay attributable to a
     stage.
   - (n) No-tuning-after-unblinding rule: once the confirmation subset is
     opened, or once any decision is informed by its content, no change of
     any frozen element is permitted against the confirmation set, ever:
     the candidate rule (deterministic unique single-letter unigram
     substitution plus complete standard Levenshtein distance-one
     expansion), the predeclared lexicographic ranking tuple, the detector
     thresholds/eligibility, the candidate semantics (frozen unigram
     vocabulary, expansion), the validator prompt/parser/protocol
     (USE_CANDIDATE/KEEP_ORIGINAL/UNCERTAIN), the reasoning level, the
     acceptance policy (conservative acceptance; EXACT/CENSORED/UNAVAILABLE
     handling), the protocol limits (300 s / 2,000,000 bytes / one terminal
     attempt / no resampling), the retry policy (none), and the protection
     rules (policy v5, curated prose_boundary.py, protected.py). The rule
     also covers the calibration subset: operational verification must not
     lead to behavior change. Any mechanism change requires a new
     objective, fresh data, and a new PR (RESEARCH-STATE section 14).
   - The protocol states additionally: the approximately 99 percent
     accepted-repair correctness and at most 1 harmful intervention per
     10,000 originally-correct words are evaluation/calibration targets,
     NOT automatic release authorization (PLAN 14.3 [S1]); confirmation
     data require explicit rights and controlled storage; outputs are
     private; no raw text in public artifacts.
3. Commit the data-free deployment-identity record
   `research/target-distribution/DEPLOYMENT-IDENTITY-009.md`:
   - (a) a bounded read-only metadata re-probe of the out-of-band A100-FP8
     identity: metadata GET of the version endpoint and the models endpoint
     with the authorized out-of-band profile only; at most 6 HTTP attempts
     total including preflights and retries, each recorded with timestamp,
     status, and observed fields; no chat/generation/responses calls, no
     other endpoints, no writes, no server mutation; record the observed
     identity (framework version, model identifier, quantization marker as
     present in the identity, max model length, wire protocol class,
     observation timestamp) data-free - no endpoint values, no
     credentials, no private paths in any committed artifact;
   - (b) the documented current unavailability of the intended RTX-3090
     target (TCP-closed at the 2026-09-09 reconnaissance; the endpoint must
     not be started or reconfigured; zero calls to that host in this
     round);
   - (c) the Deployment B exclusion (EXCLUDED_BY_HUMAN_OVERRIDE; no probes,
     no calls, ever);
   - (d) the E2 decision package with the concrete alternatives: (a)
     restore/authorize access to the intended quantized RTX-3090
     deployment, then pin and verify its exact model/quantization/API/
     runtime identity before collection (and, if the configuration drifted
     from the frozen 007-era expectation, a bounded replication of the
     frozen method on it precedes confirmation); (b) explicitly designate
     the A100-FP8 regime as the confirmation target (a product-intent
     change, recorded as such; the 007 regime becomes the target by
     designation, no additional replication required); (c) designate
     another deployment, with identity pinned by the same procedure. Each
     alternative carries an impact statement (evidence transferability,
     rights, cost, timeline, risk).
4. Frozen-system identity pin (inside PROTOCOL-009.md): the exact frozen
   identity entering 009 - the 007-m linguistic method (configuration
   sha256 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26;
   public projection file sha256
   41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0; prompt
   sha256 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d;
   the predeclared lexicographic ranking tuple verbatim (trigram exactness
   flag, trigram exact count, exact bigram side count, sum of exact bigram
   counts, unigram exact count; exact top-score tie selects nothing;
   gold structurally absent from ranking inputs); validator protocol
   USE_CANDIDATE/KEEP_ORIGINAL/UNCERTAIN with one terminal attempt per
   candidate and no resampling; limits 300 s / 2,000,000 bytes /
   new_call_budget 0; frozen implementation head
   537aa6a3ff03c60dd1b2c7f697c577940d52e88d; deployment profiles sha256
   c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and
   0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e) and
   the objective-008 protection layer (research/curated/prose_boundary.py
   sha256 c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50;
   research/curated/protected.py sha256
   27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f;
   structural-policy-v5.json sha256
   915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542 as the
   policy of record; structural-policy-v4.json sha256
   f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f
   byte-identical in-tree; experiment-008i.json sha256
   24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685 census)
   plus the RESEARCH-STATE section 14 no-tuning list verbatim.
5. Ledger and state bookkeeping: (a) exactly one 009-a entry appended to
   research/registry/experiments.json (registry 33 -> 34; data-free fields;
   status per the round outcome); (b) RESEARCH-STATE.md additive section 22
   (accepted main 185dc3d9..., objective 008 merged and closed, objective
   009 activated, E2 open item, protocol frozen at this round) plus machine
   block counters only (registry_entries 33 -> 34; oap_reports_reviewed
   52 -> 53; identity fields main_sha/branch/pr unchanged at the frozen 007
   review point; frozen_report_history_incidents unchanged at 2); (c)
   STATUS.md round sentences; (d) oap/GENERATED-FILES.json scoped pin; (e)
   research/tables/experiment-summary.csv rebuild.
6. Focused structural lint (data-free):
   research/tests/test_009a_protocol_elements.py asserts the committed
   protocol document carries the pre-registered element markers (target
   hard gate; collection procedure; domain mix; stage sizes and expansion
   criteria; controls quota; the full taxonomy label set; adjudication
   procedure; split rule; all five comparators; all six metric families
   with denominators; uncertainty rules; all four stopping rules; the full
   failure-decomposition stage order; the no-tuning-after-unblinding rule;
   the calibration-targets-not-release-authorization statement) and the
   deployment-identity document carries the E2 alternatives, the 3090
   unavailability record, and the B exclusion; positive: all markers
   present at the tested head; negative: the test fails when any marker is
   removed (a tamper-negative run is recorded as local evidence).
7. Report-only final commit: sole parent = the literal implementation head;
   sole changed path oap/reports/009-a-target-distribution-
   confirmation-preregistration.md (the 008-e pre-push validity procedure:
   the report is a claim; it must not assert push/CI success before those
   occur).
8. Final-head CI: all four required checks green at the final head
   (Application baseline; Research reproducibility; OAP bootstrap
   acceptance; OAP report history); the current check state at report time
   is disclosed verbatim (a predeclared re-run state if a check is still
   running).
9. Send the exact response OK after remote verification and stop. The new
   PR stays OPEN; no merge; no auto-merge; no further rounds without a new
   order.

## Non-goals

- No confirmation data collection, annotation, or evaluation; no
  consumption of any confirmation sample in any form; the confirmation
  population does not exist yet and must not be touched by this round.
- No tuning of the frozen system (the RESEARCH-STATE section 14 list
  verbatim applies); no mechanism change of any kind; no changes to any
  frozen surface (config, prompt, ranking, detector thresholds, candidate
  semantics, validator prompt/parser, reasoning level, acceptance policy,
  protection rules, implementation).
- No confirmation model calls of any kind; the only network activity
  authorized is the bounded metadata re-probe of Scope item 3(a)
  (metadata GETs only; no chat/generation/responses calls).
- No RTX-3090 probing, starting, or reconfiguration; no Deployment B probes
  or calls; no endpoint values, credentials, or private paths in any
  committed artifact (the out-of-band identity is never committed).
- No deployment, no release, no milestone claim, no service activation, no
  ICA launch; no D2 crossing (the E2 target-deployment decision remains a
  blocked human boundary; this round performs only the safe isolated
  preparation of Scope item 3); REPAIR_ALLOW_LIVE_TESTS stays NO.
- No 008-j: the D1-6 report-citation typo is closed by the review-of-record
  per the owner 2026-09-30 instruction; the immutable 008-i report is not
  rewritten.
- No action on the recorded non-gating technical debt (the
  diffscope_008i.py --commit-only defect; the driver subprocess-tree
  timeout-kill observation) - tracked for a future bounded maintenance
  round if/when relevant.
- No workflow, test-infrastructure, or path changes outside the
  released-from-freeze list.
- No changes to CRITICAL.md, oap/governance, or any OAP protocol file.

## Files and boundaries

Inspect (read-only): the accepted-main tree
185dc3d9c654991619ae5c57b64e0c54f4550a16 (all frozen surfaces per the
pre-work gates); the committed data-free 007/008 records (RESEARCH-STATE
sections 3/9/13/14, configs, manifests, census). Write: exactly the
released-from-freeze list in the metadata local_work field, plus the private
round directory 009a-identity under the round's private research runtime
root (same pattern as 008i-hidden; the C2 re-probe receipt and any private
identity notes, content-free). Coding read set: the compact sources, this
order, and the named data-free records; full PLAN/architecture/strategic
sources are NOT required by this order.

## Requirements

1. Pre-work integrity gates per Scope item 1 (any mismatch BLOCKED with the
   mismatch named).
2. PROTOCOL-009.md per Scope item 2 - every element (a) through (n)
   pre-registered exactly, data-free, internally consistent with PLAN
   14.2/14.3 and RESEARCH-STATE 13/14; the cited-records table carries
   sha256 of every pinned artifact.
3. DEPLOYMENT-IDENTITY-009.md per Scope item 3 - the bounded metadata
   re-probe within the declared boundary (two metadata GETs against the A
   identity only; at most 6 HTTP attempts; zero generation calls; zero
   3090/B contact; the private receipt records observed values with
   timestamps); the committed record is data-free (no endpoint values, no
   credentials, no private paths).
4. The frozen-system identity pin per Scope item 4 (every pinned hash
   re-verified against the base blobs at the implementation head; the
   no-tuning list verbatim).
5. The focused lint per Scope item 6 (committed; positive and tamper-
   negative evidence).
6. Bookkeeping per Scope item 5 (registry 33 -> 34 with exactly one new
   entry; machine block counters only; STATUS.md; GENERATED-FILES pin; csv
   rebuild).
7. The report-only commit per Scope item 7 (sole path; sole parent = the
   implementation head; the 008-e pre-push validity procedure).
8. Final-head CI per Scope item 8 (four green, or the predeclared re-run
   state disclosed verbatim at report time).
9. Send the exact response OK after remote verification and stop; the PR
   stays OPEN; no merge; no auto-merge.

## Acceptance criteria

1. The pre-work gate evidence commits; any mismatch would have BLOCKED
   (none reported).
2. PROTOCOL-009.md at the final head carries all pre-registered elements
   (a) through (n), consistent with PLAN 14.2/14.3 and RESEARCH-STATE
   13/14; zero raw sample content, zero endpoint values, zero
   credentials, zero private paths; the target hard gate and the
   no-tuning-after-unblinding rule are explicit; the calibration targets
   are labeled as not release authorization.
3. DEPLOYMENT-IDENTITY-009.md at the final head: the A identity observation
   data-free (framework version, model identifier, quantization marker, max
   model length, wire protocol class, observation timestamp); the 3090
   unavailability documented with the 2026-09-09 reconnaissance reference;
   the B exclusion documented; the E2 alternatives (a)/(b)/(c) each with an
   impact statement; the private receipt exists under the round private
   root (counts/categories/observed fields only).
4. The frozen identity pin matches the base blobs exactly (all Scope item
   4 hashes re-verified at the implementation head; zero drift).
5. Bookkeeping: registry 34 with exactly one 009-a entry (data-free);
   machine block registry_entries 34 / oap_reports_reviewed 53 / identity
   fields unchanged / frozen_report_history_incidents 2; the
   research-state consistency test green at the final head (red at the
   implementation head by design, the 008-i pattern).
6. The report-only commit is the sole changed path with sole parent = the
   implementation head; the full round diff (base..final) is limited to the
   released-from-freeze list; zero secret-pattern hits in added lines; the
   untracked residue absent from every commit.
7. All four required checks green at the final head (or the predeclared
   re-run state disclosed verbatim at report time, resolved before
   strategy's final-head review); the response OK frame received after
   remote verification.
8. The new PR on oap/009-target-distribution-confirmation (base main at
   185dc3d9c654991619ae5c57b64e0c54f4550a16) exists, is OPEN, and stays
   OPEN; no merge, no auto-merge.

## Verification

- Focused: research/tests/test_009a_protocol_elements.py (positive: all
  element markers present at the tested head; negative/tamper: the test
  fails when a marker is removed - the tamper run is recorded as local
  evidence); the research-state consistency test at the implementation head
  (the designed red) and at the final head (green).
- Broader: the full research suite under the frozen uv environment
  (data-free), the OAP suite, one full local Application-baseline driver
  run (per-stage durations, local evidence only), the full CI battery at
  the implementation head and the final head.
- Evidence boundary: software/test layer (focused lint, consistency test,
  CI); data layer: none (no confirmation data exists; zero sample content
  anywhere in committed artifacts); model layer: the C2 metadata re-probe
  only (categorized as deployment-identity reconnaissance, bounded, no
  generation). The report is a claim until strategy's independent
  final-head review re-verifies it field-by-field against the committed
  data-free records (S-EVIDENCE-01, S-REVIEW-01). A report written before
  its push cannot claim push/CI success.

## Local setup and constraints

- CPU-only; the frozen uv environment; no new dependencies; no GPU; no
  service touches; no protected Qwen weight/config/network change
  (S-PRODUCT-04).
- The C2 re-probe uses the out-of-band A100-FP8 identity per the 2026-09-20
  human note (endpoint/credential out-of-band; no environment variables
  required; no endpoint value or credential material in any committed
  artifact); strictly the two metadata GETs of Scope item 3(a), at most 6
  HTTP attempts total, each recorded and classified; no
  chat/generation/responses calls; zero contact with the RTX-3090 host and
  zero contact with Deployment B.
- Privacy: no raw customer text (none exists in this round); no raw
  confirmation sample (none exists yet); no endpoint values, credentials,
  or private paths in any committed artifact, log, or report; the private
  receipt stays under the round private root (content-free).
- Local: reversible setup inside the authorized workspace only; doctor runs
  with env -u CODEX_HOME -u OAP_ROLE; any setup failure that cannot be
  resolved reversibly inside the workspace is BLOCKED and reported, not
  worked around.

## Documentation

PROTOCOL-009.md (committed in the implementation commits): the cited-records
table (sha256), the pre-registered elements (a) through (n), the
frozen-system identity pin, the no-tuning list verbatim, the
calibration-target statement. DEPLOYMENT-IDENTITY-009.md (committed): the
observed A identity (data-free), the 3090 unavailability record, the B
exclusion, the E2 decision package with impact statements. RESEARCH-STATE.md
section 22 plus STATUS.md per Scope item 5. The OAP report per the round
mechanics (data-free).

## Git and report publication

- Branch oap/009-target-distribution-confirmation created from the base
  185dc3d9c654991619ae5c57b64e0c54f4550a16; the new PR (CREATE_NEW_PR) is
  created before composing the final report; base = main.
- Activation commit (order + oap/active) per the round mechanics;
  implementation commits per Scope items 1-6 (exact split at the
  executor's discretion, all within the released-from-freeze list); the
  report-only commit per Scope item 7.
- Push semantics per the OAP communication profile; no force-push; no push
  after the report-only commit; the exact response OK after remote
  verification; the coding wrapper consumes the 009-a control signal
  exactly once before model launch.
- No merge: the PR stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act (S-MERGE-01; repository-approved
  method: standard merge commit at the exact reviewed SHA, verify-merge,
  default-branch check).
- After this round's merge, the loop's next step is the owner E2 decision
  (presented with the round report's decision package); collection
  suffixes (009-b onward) start only after an attributable E2 resolution.
  No confirmation work before that.

## Decision classification

D0 for the round execution (data-free scoping and bounded identity
reconnaissance inside the risk budget, executing the owner 2026-09-30
instruction). The E2 target-deployment question is a D2/human boundary that
stays explicitly blocked (S-DECIDE-04): this order authorizes only the safe
isolated preparation (the bounded metadata reconnaissance and the
alternatives package) while the real boundary (choosing/authorizing the
confirmation target deployment) remains blocked pending an attributable
owner decision; no confirmation data is spent before that decision. No CRIT
admission is anticipated (S-DECIDE-03 condition 1 fails: the governing
human instruction resolves the process; the open E2 is a human decision,
not an unresolved dilemma requiring a provisional choice). If a CRIT became
genuinely necessary, coding reports the candidate only, the first
correction commits safe prerequisites, and the same-PR correction appends
the canonical entry before the provisional choice is introduced
(S-DHA-01/02).

## Deferred human adjudication

- Decision: NONE

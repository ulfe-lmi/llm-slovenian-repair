# 011-a: Post-merge machine-block identity advance to the accepted objective-010 merge (objective 011, round 1; opens the confirmation-study continuation on a green quiescent base - no product, data, protocol, or test change)

Status: DRAFT UNTIL STRATEGIC RECONCILIATION

```oap-metadata
{
  "id": "011-a",
  "title": "Post-merge machine-block identity advance to the accepted objective-010 merge (objective 011, round 1; opens the confirmation-study continuation on a green quiescent base - no product, data, protocol, or test change)",
  "objective": "011",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "4507cc78e333c0e48226b64266121171b7b8cea8",
  "branch": "oap/011-target-distribution-confirmation-study",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": ["007", "008", "009", "010"],
  "local_work": "Preserve byte-for-byte: every merged 000-010 seam on main and every 009-a/009-b/010-a artifact on the merged tree; the entire research/ tree at accepted main 4507cc78e333c0e48226b64266121171b7b8cea8, including research/target-distribution/PROTOCOL-009.md (sha256 cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a, FROZEN - the single source of truth for objective-010 collection/annotation/evaluation rounds) and research/target-distribution/DEPLOYMENT-IDENTITY-009.md (sha256 b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4, FROZEN - carries the open E2 decision package), research/tests/test_009a_protocol_elements.py, all 007-m frozen surfaces (config projection 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, deployment profiles c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), the objective-010 round-1 artifacts (oap/orders/010-a-post-merge-machine-block-identity-advance.md, oap/reports/010-a-post-merge-machine-block-identity-advance.md, RESEARCH-STATE section 24, the 010-a ledger entry), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, the private research-runtime roots (including 009a-identity/ under both the sync mount and the native private root), and any unrelated local work (untracked residue never committed).",
  "prior_review": "Strategy independent final-head review of 010-a (2026-09-30, private workorders/010-a-final-head-review-20260930.md): verdict PASS - all five acceptance criteria MET; machine block advanced to the accepted objective-009 merge (main_sha/reviewed head a501b20af7f6d9774df989c41c5ec27e21b36f3e, parent b0e33702463a9c44988e1d1ba4cb9b194c247e93) with exactly the five ordered field changes and sections 1-23 byte-identical; consistency test 10/10 green at the final head in the real checkout; registry 36 with exactly one new 010-a data-free state-correction entry; round diff exactly the eight released paths; precise secret scan zero hits; all four required checks genuinely green at final head 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d (every check run at that head_sha; Application baseline 12m03s, OAP bootstrap 4m49s, OAP report history 6s, Research reproducibility 22s); S-MERGE-01 strongest-reason-not-to-merge recorded and outweighed. strategic-gate at the reviewed SHA: report_verified true, merge_performed false, deployment_authorized false. Development-only merge of PR #11 at the exact reviewed SHA: standard merge commit 4507cc78e333c0e48226b64266121171b7b8cea8 (parents a501b20af7f6d9774df989c41c5ec27e21b36f3e + 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d), verify-merge: merged true, default head 4507cc78e333c0e48226b64266121171b7b8cea8, deployment_authorized false. Quiescent post-merge checkpoint (2026-09-30, private workorders/post-merge-checkpoint-20260930-010.md): worktree ff to 4507cc7; OAP_ACCEPTED_REF refreshed to 4507cc78e333c0e48226b64266121171b7b8cea8 (backup runtime.env.bak-20260930-pre010merge); governance accepted-runtime valid (16/16 identities, coding_bytes 35076); transcript valid at the new main (55 orders 000-a..010-a; 56 reports; three quarantined 007-d/007-n/008-d; two known frozen 006-a/006-c incidents); CRITICAL seed-identical, zero entries; state REVIEW_READY (010-a, remote verifiable post-merge), loop quiescent. The E2 target-deployment decision (D2/human boundary) remains open with the committed decision package (DEPLOYMENT-IDENTITY-009.md section 4, alternatives (a)/(b)/(c)); per PROTOCOL-009 element (a) NO confirmation data is collected from any deployment until an attributable owner decision, and this round performs no confirmation work.",
  "provenance": [
    {"kind": "H", "reference": "Owner objective-009 start instruction 2026-09-30 (continue the OAP loop into data collection/annotation/evaluation under subsequent proof-sized suffixes without the owner as terminal relay; escalate only genuine human/D2 decisions; the target-deployment question is a D2 boundary presented with concrete alternatives) and the standing owner A1 instruction (all four required checks genuinely green; never reinterpret a red required check as acceptable; no weakening)."},
    {"kind": "A", "reference": "research/tests/test_research_state_consistency.py (read-only contract: test_main_is_ancestor_of_reviewed_head asserts machine-block main_sha equals live refs/remotes/origin/main and that main_sha is an ancestor of reviewed_branch_head_sha; test_branch_and_pr_match_committed_007o_order locks branch and pr_number to the committed 007-o order; test_registry_and_report_counts derives registry_entries and oap_reports_reviewed from primary records); research/RESEARCH-STATE.md sections 16(c), 22(g), 23 and 24 (the structural post-merge condition, the 008-b/009-b precedent, and the 010-a advance); the research-state-machine-v1 block contract; S-ORDER-01/02/03 (a new objective follows a verified accepted merge/default head; one coherent proof-sized PR; corrective suffixes preserve branch/PR only while that PR is open - PR #11 being merged, the post-merge continuation publishes as a new round on a new PR), S-EVIDENCE-01 (distinct check states; no weakened tests), S-DECIDE-01 (D0 routine reversible bookkeeping); PROTOCOL-009.md element (a) (FROZEN: no confirmation work before the E2 owner decision - this round performs none: no collection, no annotation, no model/generation calls, no deployment probes, no identity pinning)."},
    {"kind": "E", "reference": "Observed 2026-09-30 (this session, remote and primary records): remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 (the PR #11 merge commit; parents a501b20af7f6d9774df989c41c5ec27e21b36f3e + 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d); PR #11 MERGED; zero open PRs; the local consistency test at the new main fails exactly 1 of 10 (test_main_is_ancestor_of_reviewed_head: live origin/main 4507cc7 != frozen machine-block main_sha a501b20af7f6d9774df989c41c5ec27e21b36f3e - the same structural post-merge condition, now relative to the objective-010 merge; the other nine pass, including the count assertions at registry 36 / reports 55 counted); the machine block at the new main carries counters 36/55/2 with identity fields at the 009-merge review point (main_sha a501b20af7f6d9774df989c41c5ec27e21b36f3e, branch oap/007-concept-verification, pr_number 8, reviewed head a501b20af7f6d9774df989c41c5ec27e21b36f3e, parent b0e33702463a9c44988e1d1ba4cb9b194c247e93, quarantined 007n/008d, frozen 007-m shas); the merged objective-010 branch oap/010-target-distribution-confirmation-study remains at 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d (fully merged into main; not reused - PR #11 closed, and the transition machine requires a new objective/branch/PR)."},
    {"kind": "I", "reference": "Strategy 010-a final-head review, merge verification, and post-merge checkpoint (private, this session), including re-derivation of the exact additive green path for this merge point, the mechanical finding that a same-objective 010-b is impossible after the PR #11 merge (oap_core.transition SAME_PR_REQUIRED: same-objective rounds need the prior PR open; therefore the study continues as new objective 011), and the decision to keep this state correction as its own proof-sized round (011-a) rather than folding the identity advance into the E2-gated collection round, so the data-bearing collection round (011-b) starts from a green quiescent main - the 008-b/009-b/010-a separation precedent and the 009-a PARTIAL lesson (a scientific round carrying a structural base red produced a PARTIAL review and a corrective round)."}
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

New objective 011 - the confirmation-study continuation (collection,
annotation, evaluation under the frozen PROTOCOL-009, opening from the
objective-010 tree) - round 1 on a NEW branch
`oap/011-target-distribution-confirmation-study` and a NEW PR
(CREATE_NEW_PR), based on the accepted objective-010 merge
`4507cc78e333c0e48226b64266121171b7b8cea8`. A new objective is required
because the study's objective-010 PR (#11) is merged: the protocol
transition machine (oap_core.transition, SAME_PR_REQUIRED) admits
same-objective rounds only while that objective's PR is open, and
S-ORDER-03 binds one objective to one branch/PR - so the study continues
as objective 011, exactly as it opened as objective 010 after the
objective-009 PR merged (010-a was then the post-merge state correction;
this round is the same kind for the objective-010 merge). This opening
round is a bounded state correction with **no new scientific content, no
product change, no data, no model calls, and no test change**: it
advances the research-state-machine-v1 review-point identity from the
009-merge review point (a501b20af7f6d9774df989c41c5ec27e21b36f3e) to
the accepted objective-010 merge (4507cc78e333c0e48226b64266121171b7b8cea8),
restoring all four required checks to green by the only viable
non-weakening means, and registers this round in the canonical
experiment ledger. It performs **no confirmation work of any kind**: no
collection, no annotation, no evaluation, no model/generation calls, no
deployment probes of any kind, no identity pinning - the PROTOCOL-009
element (a) hard gate and the open E2 owner decision are untouched. The
collection round is **011-b** (renumbered from the 010-b pre-draft; see
Decision classification); it proceeds only after an attributable owner
E2 resolution, from the green quiescent main this round restores.

## Provenance

- H: owner 2026-09-30 objective-009 instruction (the loop continues into
  collection/annotation/evaluation under subsequent proof-sized suffixes
  without the owner as terminal relay; escalate only genuine
  human/D2 decisions; the E2 target-deployment question is presented as
  concrete alternatives at the D2 boundary) and the standing A1
  instruction (red required checks are never reinterpreted as acceptable;
  tests are never weakened).
- A: the committed consistency-test contract (test source read directly),
  RESEARCH-STATE sections 16(c)/22(g)/23/24, the research-state-machine-
  v1 block, S-ORDER-01/02/03, S-EVIDENCE-01, S-DECIDE-01, and the FROZEN
  PROTOCOL-009 element (a) (no confirmation work before the E2 decision -
  this round is state bookkeeping only and is not confirmation work).
- E: the 010-a final-head review PASS, the development-only merge of
  PR #11 (merge commit 4507cc7, parents a501b20a + 01ea3fa), the
  quiescent post-merge checkpoint, and the observed 1-of-10 local
  consistency-test red at the new main (the single live-ref assertion;
  pre-existing by construction at the merge, identical in kind to the
  008-a, 009-a and 010-a conditions resolved by the additive 008-b,
  009-b and 010-a updates).
- I: strategy's 010-a final-head review, merge verification, and
  post-merge checkpoint (private, this session), including re-derivation
  of the exact additive green path for this merge point and the
  separation decision recorded in Decision classification.

## Current verified state

Verified 2026-09-30 (this session, from remote and primary records):
remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 (the PR #11
merge commit; parents a501b20af7f6d9774df989c41c5ec27e21b36f3e +
01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d); OAP_ACCEPTED_REF =
4507cc78e333c0e48226b64266121171b7b8cea8 (refreshed at the 2026-09-30
quiescent post-merge checkpoint; backup
runtime.env.bak-20260930-pre010merge preserved); governance accepted-
runtime valid at the new main (16/16 identities, coding_bytes 35076,
strategic copy check clean); worktree on main at
4507cc78e333c0e48226b64266121171b7b8cea8 with the three untracked
residues (corpus/, .research-test-scratch/, .rclone-speed-test/)
preserved and never committed. PR #11 MERGED; zero open PRs. Local
consistency test at the new main: 1 of 10 failing -
test_main_is_ancestor_of_reviewed_head only (live origin/main
4507cc78e333c0e48226b64266121171b7b8cea8 != machine-block main_sha
a501b20af7f6d9774df989c41c5ec27e21b36f3e; the other nine pass,
including the count assertions at registry 36 / 55 counted). Machine
block at the new main: registry_entries 36, oap_reports_reviewed 55,
frozen_report_history_incidents 2; identity fields at the 009-merge
review point (main_sha a501b20af7f6d9774df989c41c5ec27e21b36f3e, branch
oap/007-concept-verification, pr_number 8, reviewed head
a501b20af7f6d9774df989c41c5ec27e21b36f3e, parent
b0e33702463a9c44988e1d1ba4cb9b194c247e93, quarantined 007n/008d, frozen
007-m shas); registry = 36 entries (last 010-a, kind state-correction,
status COMPLETE). Transcript valid at the new main (55 orders; 56
reports; two known frozen 006-a/006-c incidents). CRITICAL.md
seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e,
zero entries. State: REVIEW_READY (010-a, remote verifiable post-merge);
the loop is quiescent with no active round; the coding wrapper is idle
on the control fifo with no model child. The E2 target-deployment
decision remains open with the committed decision package
(DEPLOYMENT-IDENTITY-009.md section 4); per PROTOCOL-009 element (a) no
confirmation data is collected from any deployment until an attributable
owner decision, and this round performs no confirmation work.
Environment note: the rclone/Dropbox FUSE mount remains degraded
(minutes-scale stalls, D-state I/O); heavy test temp stays on native
/home/ubuntu/.oap-scratch; CI parity is authoritative for the heavy
fixture cycles; OAP helper git-history traversals can transiently time
out at the 30 s subprocess limit on a cold cache (TD-3, recorded
non-gating; the retry is deterministic and safe - four occurrences so
far this session, all retries clean).

## Governance

The sixteen source identities in the metadata governance mapping are the
exact identities of `oap/governance/MANIFEST.json` at the base
4507cc78e333c0e48226b64266121171b7b8cea8, re-verified by strategy at the
post-merge quiescent checkpoint (governance accepted-runtime valid,
16/16, coding_bytes 35076; zero mismatch). No governance change occurs in
this objective.

## Goal and dependencies

Goal: make the research-state machine block truthful at the current
post-010-merge review point so that the frozen 007-o consistency test is
satisfied again and all four required checks are green at this round's
final head, without weakening any test, altering any frozen surface, or
changing any protocol, data, or product element. This opens objective 011
(the confirmation-study continuation) on a green quiescent base for the
E2-gated collection round (011-b); the E2 human decision remains the only
gate before that round may begin, and this round neither resolves nor
pre-decides it.

Dependencies: 010 (its merged tree, including the 010-a state round and
the open E2 decision package), 009 (frozen protocol and identity record),
007/008 only as the frozen surfaces preserved by the local-work field.
Nothing else.

## Scope

1. Pre-work integrity gates (data-free): at the base 4507cc7,
   byte-verify every frozen surface and the objective-009/010-a
   artifacts (research/target-distribution/PROTOCOL-009.md,
   research/target-distribution/DEPLOYMENT-IDENTITY-009.md,
   research/tests/test_009a_protocol_elements.py, the 010-a order and
   report, RESEARCH-STATE section 24, all 007-m and 008 frozen pins per
   the local_work field); registry = 36 entries (last 010-a); machine
   block counters registry_entries 36 / oap_reports_reviewed 55 /
   frozen_report_history_incidents 2 with the 009-merge review-point
   identity fields still present (main_sha
   a501b20af7f6d9774df989c41c5ec27e21b36f3e); CRITICAL.md
   seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e.
   Any mismatch is BLOCKED with the mismatch named.
2. Additive machine-block identity advance in research/RESEARCH-STATE.md
   (the research-state-machine-v1 block plus an additive prose note,
   section 25, the 008-b/009-b/010-a pattern; no rewrite of section 24
   or earlier text):
   - main_sha: a501b20af7f6d9774df989c41c5ec27e21b36f3e ->
     4507cc78e333c0e48226b64266121171b7b8cea8
   - reviewed_branch_head_sha: a501b20af7f6d9774df989c41c5ec27e21b36f3e ->
     4507cc78e333c0e48226b64266121171b7b8cea8
   - reviewed_branch_head_parent_sha: b0e33702463a9c44988e1d1ba4cb9b194c247e93 ->
     01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d (the accepted objective-010
     branch head, second parent of merge commit 4507cc7)
   - UNCHANGED and byte-preserved: branch (oap/007-concept-verification),
     pr_number (8), quarantined_007n, quarantined_008d, all frozen_007m sha
     fields, and every other block field except the three above and the
     counters of item 3.
   - The additive prose note records: the old review point and its
     identity, the advance to the accepted 010 merge, the reason (the
     010-a identity advance targeted the then-accepted main; the 010-a
     merge advanced main again, re-creating the structural live-ref
     condition by construction; resolved by this additive update per the
     documented 008-a/008-b, 009-a/009-b, and 010-a precedent chain; D0
     per that precedent), and the invariants (no test logic changed;
     every numeric re-derivation assertion remains binding; no
     confirmation work performed or authorized by this round; the
     collection round 011-b proceeds only after an attributable owner
     E2 resolution).
3. Ledger and state bookkeeping: (a) exactly one 011-a entry appended to
   research/registry/experiments.json (registry 36 -> 37; data-free;
   status per the round outcome; kind state-correction referencing the
   010-a/009-b/008-b precedent chain); (b) machine-block counters
   registry_entries 36 -> 37 and oap_reports_reviewed 55 -> 56 (the
   011-a report file); frozen_report_history_incidents unchanged at 2;
   (c) STATUS.md round sentences; (d) oap/GENERATED-FILES.json scoped
   pin (same scope pattern as 009-a/009-b/010-a); (e)
   research/tables/experiment-summary.csv rebuild.
4. Local verification (data-free): research/tests/test_research_state_
   consistency.py green at the final head in a real checkout with
   origin/main = 4507cc78e333c0e48226b64266121171b7b8cea8 (all
   assertions including test_main_is_ancestor_of_reviewed_head and
   test_branch_and_pr_match_committed_007o_order); at the implementation
   head exactly one test fails (the designed report-count red, 56 vs 55,
   the 008-i/009-b/010-a pattern - the live-ref assertion is green at
   both heads because main_sha already equals live main); the focused
   009-a lint still green; the full research suite under the frozen uv
   environment; the OAP suite to the extent feasible on the degraded
   rclone/Dropbox FUSE mount (if the heavy fixture cycles cannot
   complete in the round window, record NOT RUN with the reason; both
   OAP CI jobs are authoritative for the heavy fixture cycles - the
   009-a/009-b/010-a precedent); one full local Application-baseline
   driver run (local evidence only; the recurring FUSE git-walk 30-s
   subprocess timeout in WhitespaceVerifier is a known environmental
   artifact with manual-repro rc=0 - the 009-a/009-b/010-a precedent;
   record it distinctly).
5. Report-only final commit: sole parent = the literal implementation
   head; sole changed path oap/reports/011-a-post-merge-machine-block-
   identity-advance.md; the report discloses the final-head check state
   verbatim.
6. Final-head CI: all four required checks green at the final head (or
   the predeclared re-run state disclosed verbatim at report time,
   resolved before strategy's final-head review).
7. Push and verify; send the exact response OK and stop. The new PR
   stays OPEN; no merge; no auto-merge.

## Non-goals

- No confirmation work of any kind: no collection, no annotation, no
  evaluation, no consumption of any confirmation sample, no
  model/generation calls of any kind, no deployment probes of any kind
  (the RTX-3090, Deployment B, and the A100-FP8 endpoint all remain
  untouched; REPAIR_ALLOW_LIVE_TESTS stays NO; PROTOCOL-009 element (a)
  hard gate fully intact).
- No E2 resolution: the target-deployment decision remains a blocked
  D2/human boundary; this round changes nothing about it, does not
  consume or pre-decide it, and the collection round (011-b) starts
  only after an attributable owner decision.
- No change to any test file or test logic (the consistency test is read
  only; it is the binding contract).
- No change to PROTOCOL-009.md, DEPLOYMENT-IDENTITY-009.md, or any
  frozen surface (007-m method, 008 protection layer, policies, configs,
  prompts, implementation).
- No branch/pr_number change in the machine block (locked to the
  committed 007-o order by test_branch_and_pr_match_committed_007o_order);
  no quarantined-identity or frozen-sha change; no CRITICAL.md,
  oap/governance, or OAP protocol change.
- No force-push, no reset of the merged 010-a branch, no merge, no
  auto-merge, no deployment, no release, no milestone claim.

## Files and boundaries

Write: exactly research/RESEARCH-STATE.md, research/registry/
experiments.json, STATUS.md, oap/GENERATED-FILES.json, research/tables/
experiment-summary.csv, oap/orders/011-a-post-merge-machine-block-
identity-advance.md (new, activation), oap/active (pointer),
oap/reports/011-a-post-merge-machine-block-identity-advance.md
(new, report-only commit). No non-repository writes of any kind this round
(the private research-runtime roots are untouched).
Read-only: the rest of the accepted tree and the objective-009/010-a
artifacts (verified byte-identical in the pre-work gate). Coding read
set: the compact sources, this order, RESEARCH-STATE sections
16(c)/22(g)/23/24, the consistency test source, and the 010-a report.

## Requirements

1. Pre-work gates per Scope 1 (any mismatch BLOCKED and named).
2. The additive identity advance per Scope 2 with exactly the three
   field changes and exactly the counter changes; the additive
   section-25 prose note complete; all other block fields byte-identical.
3. Bookkeeping per Scope 3 (registry 37 with exactly one new 011-a
   data-free entry; counters 37/56; incidents 2; STATUS.md; GENERATED-
   FILES pin; csv rebuild).
4. Local verification per Scope 4, with the designed implementation-head
   count red and the final-head green recorded distinctly (PASSED/FAILED
   with tested SHAs).
5. The report-only commit per Scope 5.
6. Final-head CI per Scope 6: all four required checks genuinely green.
7. Exact response OK after remote verification; the new PR stays OPEN.

## Acceptance criteria

1. The pre-work gate evidence commits; any mismatch would have BLOCKED.
2. At the final head the machine block carries main_sha =
   4507cc78e333c0e48226b64266121171b7b8cea8, reviewed_branch_head_sha =
   4507cc78e333c0e48226b64266121171b7b8cea8, reviewed_branch_head_parent_
   sha = 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters registry_
   entries 37 / oap_reports_reviewed 56 / frozen_report_history_incidents
   2, and byte-identical branch, pr_number, quarantined identities, and
   frozen 007-m sha fields; the additive section-25 note is present and
   the 010-a text (section 24) is unaltered.
3. The research-state consistency test is green at the final head in a
   real checkout (every assertion, including the live-ref and 007-o-lock
   assertions); the round diff (base..final) is limited to the released-
   from-freeze list; zero secret-pattern hits in added lines; the
   untracked residue absent from every commit.
4. All four required checks genuinely green at the final head (no
   pending, cancelled, or reinterpreted check); the response OK frame
   received after remote verification.
5. The new PR on oap/011-target-distribution-confirmation-study (base
   main at 4507cc78e333c0e48226b64266121171b7b8cea8) is OPEN; no merge;
   no auto-merge.

## Verification

- Focused: test_research_state_consistency.py (green at the final head;
  the designed implementation-head count red recorded); the 009-a
  focused lint (unchanged, still green); the full research suite; the
  OAP suite (degraded-mount caveat per Scope 4); one full local
  Application-baseline driver run (local evidence only).
- Broader: the full CI battery at the implementation head and the final
  head.
- Evidence boundary: software/test layer only; zero data, zero model
  calls, zero network calls beyond the bounded CI and the read-only
  remote reads of this order's own publication mechanics. The report is
  a claim until strategy's independent final-head review re-verifies it
  field-by-field (S-EVIDENCE-01, S-REVIEW-01).

## Local setup and constraints

- CPU-only; the frozen uv environment; no new dependencies; no GPU; no
  service touches; no protected Qwen weight/config/network change
  (S-PRODUCT-04); REPAIR_ALLOW_LIVE_TESTS stays NO; no endpoint,
  credential, or private path in any committed artifact.
- Local: reversible setup inside the authorized workspace only; doctor
  runs with env -u CODEX_HOME -u OAP_ROLE; heavy test temp on native
  /home/ubuntu/.oap-scratch (0700) given the degraded FUSE mount; any
  unresolvable setup failure is BLOCKED and reported, not worked around.

## Documentation

RESEARCH-STATE.md additive section-25 identity-advance note plus the
machine block (Scope 2/3); STATUS.md per Scope 3; the OAP report per the
round mechanics (data-free; the round's classification recorded: D0 per
the documented 008-a/008-b, 009-a/009-b, and 010-a precedent chain -
single viable non-weakening remedy; no CRIT admission; the E2 boundary
untouched and still the only gate before the 011-b collection round).

## Git and report publication

- Branch oap/011-target-distribution-confirmation-study created from
  the base 4507cc78e333c0e48226b64266121171b7b8cea8 (the accepted
  main); the new PR (CREATE_NEW_PR) is created before composing the
  final report; base = main. No force-push; the merged objective-010
  branch is not touched.
- Activation commit (order + oap/active) per the round mechanics;
  implementation commits per Scope 2-3 (exact split at the executor's
  discretion, all within the released-from-freeze list); the report-only
  commit per Scope 5.
- Push semantics per the OAP communication profile; no force-push; no
  push after the report-only commit; the exact response OK after remote
  verification; the coding wrapper consumes the 011-a control signal
  exactly once before model launch.
- No merge: the PR stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act (S-MERGE-01; repository-approved
  method: standard merge commit at the exact reviewed SHA, verify-merge,
  default-branch check).

## Decision classification

D0 (S-DECIDE-01): routine, reversible bookkeeping within the risk
budget, following the documented 008-a/008-b, 009-a/009-b, and 010-a
precedent chain for the identical structural condition (now relative to
the objective-010 merge); the exact green path was re-derived from the
committed test source in this session; no human judgment debt; no CRIT
admission (S-DECIDE-03 condition 1 fails: the governing test contract,
the documented precedent, and the owner's A1 instruction leave exactly
one viable non-weakening path). Renumbering decision (recorded, D0):
the strategy-side plan had this state correction as 010-b (folding the
identity advance ahead of the E2-gated collection round, which it
pre-drafted as the objective-010 round 2); the objective-010 PR (#11)
merged after 010-a, and the protocol transition machine admits
same-objective rounds only while that PR is open (oap_core.transition,
SAME_PR_REQUIRED), so 010-b is mechanically impossible and the study
continues as new objective 011 with this round as 011-a - the same
objective-rollover that opened 010 after the objective-009 PR merged.
The collection round is renumbered 011-b (the pre-draft is updated
accordingly at E2 finalization). The separation rationale is unchanged:
the 008-b/009-b/010-a separation precedent plus the 009-a PARTIAL lesson
(a data-bearing scientific round should start from a green quiescent
base and not carry a structural base red), and this round runs while
the owner's E2 deliberation is still open, shortening the post-E2
critical path. This round is the standard post-merge state correction;
it is NOT confirmation work (PROTOCOL-009 element (a) untouched) and NOT
the E2 decision (which remains a blocked D2/human boundary).

## Deferred human adjudication

- Decision: NONE

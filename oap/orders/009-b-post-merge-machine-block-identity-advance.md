# 009-b: Post-merge machine-block identity advance to the accepted objective-008 merge (objective 009, round 2; bounded state correction, no product, data, protocol, or test change)

Status: FINAL

Finalized by strategic reconciliation of 2026-09-30 (this session):
strategy's independent 009-a final-head review (private
workorders/009-a-final-head-review-20260930.md; verdict PARTIAL; the single
red required check is the pre-existing structural live-ref assertion,
reclassified D0 per the documented 008-a/008-b precedent; NO MERGE at the
009-a final head d8e306812b5c265ecb5dca2ecc2b39a296cea8a4), plus
re-verification in this session of the final-head CI, the report identity
(remote-scope verified), the machine block, the committed test contract,
and the round diff. This round is the bounded corrective remedy.

```oap-metadata
{
  "id": "009-b",
  "title": "Post-merge machine-block identity advance to the accepted objective-008 merge (objective 009, round 2; bounded state correction, no product, data, protocol, or test change)",
  "objective": "009",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "d8e306812b5c265ecb5dca2ecc2b39a296cea8a4",
  "branch": "oap/009-target-distribution-confirmation",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 10,
  "dependencies": ["007", "008", "009"],
  "local_work": "Preserve byte-for-byte: every merged 000-008 seam on main and every 009-a artifact on the branch; the entire research/ tree at the 009-a final head d8e306812b5c265ecb5dca2ecc2b39a296cea8a4, including research/target-distribution/PROTOCOL-009.md (sha256 cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a), research/target-distribution/DEPLOYMENT-IDENTITY-009.md (sha256 b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4), research/tests/test_009a_protocol_elements.py, all 007-m frozen surfaces (config projection 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, deployment profiles c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, the private research-runtime roots (including 009a-identity/), and any unrelated local work (untracked residue never committed).",
  "prior_review": "Strategy independent final-head review of 009-a (2026-09-30, private workorders/009-a-final-head-review-20260930.md): verdict PARTIAL - criteria 1, 2, 3, 4, 6, 8 MET; criterion 5 PARTIAL (bookkeeping MET: registry 34 with exactly one 009-a data-free entry, counters 34/53/2, identity fields byte-unchanged at the 007 review point; the consistency-test-green clause NOT MET by a structural order-internal contradiction: scope item 5 freezes the machine-block identity fields at the 007 review point while criterion 5 demands the frozen consistency test be green at the final head, unsatisfiable after the 008 merge advanced main; the red is proven pre-existing at the activation head, 1 of 10 tests, before any 009-a mutation); criterion 7 NOT MET at the final head (Research reproducibility red on the single pre-existing live-ref assertion). Report-only commit d8e306812b5c265ecb5dca2ecc2b39a296cea8a4 (sole parent 789650e176c68c54375d585cfd9d6848fbd586f8, sole changed path oap/reports/009-a-target-distribution-confirmation-preregistration.md); verify-report (remote scope) = verified; round diff 185dc3d9c654991619ae5c57b64e0c54f4550a16..d8e3068 = exactly the eleven released paths; zero secret-pattern hits in added lines (benign hits only: the PR #10 URL, the value-never-recorded sentences, the native temp-scratch path); untracked residues absent from every commit; final-head CI re-observed: Application baseline SUCCESS (13/13 commands, zero timeouts), OAP bootstrap acceptance SUCCESS, OAP report history SUCCESS, Research reproducibility FAILURE (failures=1, skipped=53; the single assertion live origin/main 185dc3d9c654991619ae5c57b64e0c54f4550a16 != machine-block main_sha 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9); independent local run at the final head in the real checkout: 10 tests, 1 failure, the same assertion. Non-blocking findings: F1 the 009a-identity private receipt exists only on the degraded sync mount (mitigation ordered: 009-b copies it to the native private root, originals untouched); F2 the local OAP suite NOT RUN in-round (both OAP CI jobs PASSED); F3 three local-only driver failures (CI parity authoritative, 13/13); F4 three in-round uncommitted-test fixes (D0); F5 the report privacy-field wording overbroad (native temp-scratch path disclosed in the setup fields). The 009-a report D1 dilemma candidate (criterion 5 vs the frozen identity clause) is reclassified D0 by strategy: the committed test contract (test_main_is_ancestor_of_reviewed_head; test_branch_and_pr_match_committed_007o_order; test_registry_and_report_counts) and the documented 008-a/008-b precedent leave exactly one viable non-weakening path - the additive same-PR machine-block identity advance ordered by this round. No CRIT admission. NO MERGE at the 009-a final head (red required check; owner A1 standing instruction).",
  "provenance": [
    {"kind": "H", "reference": "Owner objective-009 start instruction 2026-09-30 (the OAP loop continues under subsequent proof-sized suffixes without the owner as terminal relay; escalate only genuine human/D2 decisions) and the standing owner A1 instruction 2026-09-22 (all four required checks must become genuinely green; never reinterpret a red required check as acceptable; do not weaken tests or gates)."},
    {"kind": "A", "reference": "research/tests/test_research_state_consistency.py (read-only contract: test_main_is_ancestor_of_reviewed_head asserts machine-block main_sha equals live refs/remotes/origin/main and that main_sha is an ancestor of reviewed_branch_head_sha; test_branch_and_pr_match_committed_007o_order locks branch and pr_number to the committed 007-o order; test_registry_and_report_counts derives registry_entries and oap_reports_reviewed from primary records); research/RESEARCH-STATE.md sections 16(c) and 22(g) (the structural post-merge condition and the 008-b precedent); the research-state-machine-v1 block contract; S-ORDER-01/02/03 (corrective suffix preserves branch and PR), S-EVIDENCE-01 (distinct check states; no weakened tests), S-DECIDE-01 (D0 routine reversible bookkeeping)."},
    {"kind": "E", "reference": "Observed: at the 009-a implementation head 789650e176c68c54375d585cfd9d6848fbd586f8, CI run Research reproducibility failed solely on test_main_is_ancestor_of_reviewed_head (live origin/main 185dc3d9c654991619ae5c57b64e0c54f4550a16 != frozen machine-block main_sha 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9) plus the designed report-count red (53 vs 52, self-resolving with the report commit); the same main-sha assertion is structurally red at every head after the 008 merge, pre-existing at the 009-a base 185dc3d9; the 009-a coding round disclosed this in RESEARCH-STATE section 22(g) and reported it as a dilemma candidate with the full evidence chain; the 008-a round disclosed the identical condition (main had moved at the 007 merge) and strategy classified it D0 with the additive 008-b identity update as the only viable non-weakening remedy, restoring all four required checks to green at the 008-b final head."},
    {"kind": "I", "reference": "Strategy final-head review of 009-a (private, this session): round verified against its order; the red required check is a structural consequence of the 008 merge combined with the 009-a order's counters-only bookkeeping clause; the test source (read directly) confirms the exact green path: set main_sha and reviewed_branch_head_sha to 185dc3d9c654991619ae5c57b64e0c54f4550a16 (self-ancestor holds; live-ref equality holds while main is 185dc3d9) and record reviewed_branch_head_parent_sha as the accepted 008 branch head 59d8f030a91309f4386bde48b360f17d7ea11e86 (second parent of the merge commit; the field is not asserted by the test but must be truthful per the 008-b pattern); branch, pr_number, quarantined identities and frozen 007-m sha fields remain unchanged (branch/pr_number are locked to the committed 007-o order; all other numeric re-derivation assertions remain binding)."}
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

Corrective suffix `009-b` of objective 009 on the existing branch
`oap/009-target-distribution-confirmation` and existing PR #10
(AMEND_EXISTING_PR), based on the 009-a final head
`d8e306812b5c265ecb5dca2ecc2b39a296cea8a4`. The round is a bounded
state correction with **no new scientific content, no product change, no
data, no model calls, and no test change**: it advances the
research-state-machine-v1 review-point identity from the 007 review point
(7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9) to the accepted objective-008
merge (185dc3d9c654991619ae5c57b64e0c54f4550a16), restoring all four
required checks to green at its final head by the only viable non-weakening
means, and registers this round in the canonical experiment ledger. The E2
target-deployment decision remains a blocked D2/human boundary; this round
does not touch the frozen protocol, the deployment-identity record, or any
frozen surface.

## Provenance

- H: owner 2026-09-30 objective-009 instruction (loop continues under
  subsequent proof-sized suffixes without the owner as terminal relay) and
  the standing A1 instruction (red required checks are never reinterpreted
  as acceptable; tests are never weakened).
- A: the committed consistency-test contract (test source read directly),
  RESEARCH-STATE sections 16(c) and 22(g), the research-state-machine-v1
  block, S-ORDER-01/02/03, S-EVIDENCE-01, S-DECIDE-01.
- E: the 009-a final-head CI red on the single structural main-sha
  assertion (plus the designed self-resolving report-count red), disclosed
  in RESEARCH-STATE section 22(g) and in the 009-a report as a dilemma
  candidate; the condition is pre-existing at the 009-a base and identical
  in kind to the 008-a condition resolved by the additive 008-b update.
- I: strategy's 009-a final-head review and direct test-source analysis
  (private, this session), including verification of the exact additive
  green path and of the fields that must remain unchanged.

## Current verified state

Verified 2026-09-30 (this session, from remote and primary records):
remote main = 185dc3d9c654991619ae5c57b64e0c54f4550a16 (the accepted PR #9
merge; parents 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 +
59d8f030a91309f4386bde48b360f17d7ea11e86); OAP_ACCEPTED_REF =
185dc3d9c654991619ae5c57b64e0c54f4550a16 (refreshed at the 2026-09-30
quiescent checkpoint; backup runtime.env.bak-20260930-pre009 preserved);
all sixteen governance identities re-verified at that checkpoint with zero
mismatch; worktree on oap/009-target-distribution-confirmation at
d8e306812b5c265ecb5dca2ecc2b39a296cea8a4 (the 009-a final head; untracked
residues corpus/, .research-test-scratch/, .rclone-speed-test/ preserved,
never committed). PR #10 OPEN and MERGEABLE, head
d8e306812b5c265ecb5dca2ecc2b39a296cea8a4, base main, auto-merge disabled.
Final-head CI at d8e3068: Application baseline SUCCESS (13/13 commands
PASSED under the owner-approved 600 s per-command cap, zero timeouts), OAP
bootstrap acceptance SUCCESS, OAP report history SUCCESS, Research
reproducibility FAILURE (failures=1, skipped=53; the single assertion live
origin/main 185dc3d9c654991619ae5c57b64e0c54f4550a16 != machine-block
main_sha 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 - the pre-existing
structural condition this round resolves). Local consistency test at the
final head in the real checkout: 10 tests, 1 failure (the same assertion),
the other nine passing. Machine block at d8e3068: registry_entries 34,
oap_reports_reviewed 53, frozen_report_history_incidents 2; identity fields
at the 007 review point (main_sha 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9,
branch oap/007-concept-verification, pr_number 8, reviewed head
7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, parent
4a029287f27e038d5c34c39b26ca836be7c6914b, quarantined 007n/008d, frozen
007-m shas); registry = 34 entries (last 009-a). verify-report 009-a
(remote scope) = verified; report history valid (two known frozen 006-a/
006-c incidents). The 009-a exact OK frame was received 2026-09-30 05:45:43
CEST; consumed.json = 009-a (phase consumed, recovery false); the coding
wrapper is idle on the control fifo. CRITICAL.md seed-identical
a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e, zero
entries. Environment note: the rclone/Dropbox FUSE mount remains degraded
(minutes-scale stalls, D-state I/O); heavy test temp stays on native
/home/ubuntu/.oap-scratch; CI parity is authoritative for the heavy fixture
cycles.

## Governance

The sixteen source identities in the metadata governance mapping are the
exact identities of `oap/governance/MANIFEST.json` at the base
185dc3d9c654991619ae5c57b64e0c54f4550a16, re-verified by strategy at the
009-a publication checkpoint (zero mismatch). No governance change occurs in
this objective.

## Goal and dependencies

Goal: make the research-state machine block truthful at the current
post-008-merge review point so that the frozen 007-o consistency test is
satisfied again and all four required checks are green at this round's final
head, without weakening any test, altering any frozen surface, or changing
any protocol, data, or product element. This clears the last
non-product blocker on objective 009's development merge so that the E2
human decision (presented from the 009-a decision package) is the only
remaining gate before collection suffixes (009-c onward) may begin.

Dependencies: 007, 008, and 009-a (its report and its disclosed dilemma
candidate). Nothing else.

## Scope

1. Pre-work integrity gates (data-free): at the 009-a final head,
   byte-verify every frozen surface and the 009-a artifacts
   (research/target-distribution/PROTOCOL-009.md,
   research/target-distribution/DEPLOYMENT-IDENTITY-009.md,
   research/tests/test_009a_protocol_elements.py, all 007-m and 008 frozen
   pins per the 009-a order local_work field); registry = 34 entries (last
   009-a); machine block counters registry_entries 34 /
   oap_reports_reviewed 53 / frozen_report_history_incidents 2 with the
   007-review-point identity fields still present; CRITICAL.md
   seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e.
   Any mismatch is BLOCKED with the mismatch named.
2. Additive machine-block identity advance in research/RESEARCH-STATE.md
   (the research-state-machine-v1 block plus an additive prose note, the
   008-b pattern; no rewrite of section 22 or earlier text):
   - main_sha: 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 ->
     185dc3d9c654991619ae5c57b64e0c54f4550a16
   - reviewed_branch_head_sha: 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 ->
     185dc3d9c654991619ae5c57b64e0c54f4550a16
   - reviewed_branch_head_parent_sha: 4a029287f27e038d5c34c39b26ca836be7c6914b ->
     59d8f030a91309f4386bde48b360f17d7ea11e86 (the accepted objective-008
     branch head, second parent of merge commit 185dc3d9)
   - UNCHANGED and byte-preserved: branch (oap/007-concept-verification),
     pr_number (8), quarantined_007n, quarantined_008d, all frozen_007m sha
     fields, and every other block field except the three above and the
     counters of item 3.
   - The additive prose note records: the old review point and its
     identity, the advance to the accepted 008 merge, the reason (the 009-a
     order's counters-only clause left the live-ref assertion structurally
     red post-merge; pre-existing at the 009-a base; resolved by this
     additive update per the documented 008-a/008-b precedent; D0 per that
     precedent), and the invariants (no test logic changed; every numeric
     re-derivation assertion remains binding).
3. Ledger and state bookkeeping: (a) exactly one 009-b entry appended to
   research/registry/experiments.json (registry 34 -> 35; data-free; status
   per the round outcome; kind state-correction referencing the 009-a
   dilemma candidate and the 008-b precedent); (b) machine-block counters
   registry_entries 34 -> 35 and oap_reports_reviewed 53 -> 54 (the 009-b
   report file); frozen_report_history_incidents unchanged at 2; (c)
   STATUS.md round sentences; (d) oap/GENERATED-FILES.json scoped pin (same
   scope pattern as 009-a); (e) research/tables/experiment-summary.csv
   rebuild; (f) private receipt consolidation: copy (not move) the three
   009a-identity files from the round private research runtime root under
   the sync mount (STRATEGIC_HOME/research-runtime-20260911.YJemoq/
   009a-identity/, the degraded Dropbox FUSE tree) to the native private
   root /home/ubuntu/.local/share/llm-slovenian-repair/research-runtime-
   20260911.YJemoq/009a-identity/ (the 008i-hidden pattern); the
   sync-mount originals remain untouched; the copy's byte-identity is
   recorded; no receipt byte enters the repository; the receipt carries
   observed identity fields and counts only (the out-of-band endpoint value
   appears only in the private receipt, never in a committed artifact).
4. Local verification (data-free): research/tests/test_research_state_
   consistency.py green in a real checkout with origin/main =
   185dc3d9c654991619ae5c57b64e0c54f4550a16 (all assertions including
   test_main_is_ancestor_of_reviewed_head and
   test_branch_and_pr_match_committed_007o_order); the focused 009-a lint
   still green; the research-state consistency test red at the implementation
   head on the designed report-count assertion only (54 vs 53), green at
   the final head (the 008-i pattern); the full research suite under the
   frozen uv environment; the OAP suite to the extent feasible on the
   degraded rclone/Dropbox FUSE mount (if the ~190 MB fixture copytree
   cannot complete in the round window, record NOT RUN with the reason;
   both OAP CI jobs are authoritative for the heavy fixture cycles - the
   009-a check-12 precedent); one full local Application-baseline
   driver run (local evidence only).
5. Report-only final commit: sole parent = the literal implementation head;
   sole changed path oap/reports/009-b-post-merge-machine-block-identity-
   advance.md; the report discloses the final-head check state verbatim.
6. Final-head CI: all four required checks green at the final head (or the
   predeclared re-run state disclosed verbatim at report time, resolved
   before strategy's final-head review).
7. Push and verify; send the exact response OK and stop. PR #10 stays OPEN;
   no merge; no auto-merge.

## Non-goals

- No change to any test file or test logic (the consistency test is read
  only; it is the binding contract).
- No change to PROTOCOL-009.md, DEPLOYMENT-IDENTITY-009.md, or any frozen
  surface (007-m method, 008 protection layer, policies, configs, prompts,
  implementation).
- No confirmation data collection, annotation, or evaluation; no
  consumption of any confirmation sample; no model/generation calls; no
  deployment probes of any kind (the 3090 and Deployment B remain
  untouched; REPAIR_ALLOW_LIVE_TESTS stays NO).
- No E2 resolution: the target-deployment decision remains a blocked
  D2/human boundary; this round changes nothing about it and does not
  consume or pre-decide it.
- No branch/pr_number change (locked to the committed 007-o order by
  test_branch_and_pr_match_committed_007o_order); no quarantined-identity or
  frozen-sha change; no CRITICAL.md, oap/governance, or OAP protocol change.
- No merge, no auto-merge, no deployment, no release, no milestone claim.

## Files and boundaries

Write: exactly research/RESEARCH-STATE.md, research/registry/
experiments.json, STATUS.md, oap/GENERATED-FILES.json, research/tables/
experiment-summary.csv, oap/orders/009-b-post-merge-machine-block-identity-
advance.md (new, activation), oap/active (pointer), oap/reports/009-b-
post-merge-machine-block-identity-advance.md (new, report-only commit). The only non-repository write of
the round is the receipt copy under the native private root named in Scope
item 3(f) (copy only; sync-mount originals untouched).
Read-only: the rest of the accepted tree and the 009-a artifacts (verified
byte-identical in the pre-work gate). Coding read set: the compact sources,
this order, RESEARCH-STATE sections 16(c)/22(g), the consistency test
source, and the 009-a report.

## Requirements

1. Pre-work gates per Scope 1 (any mismatch BLOCKED and named).
2. The additive identity advance per Scope 2 with exactly the three field
   changes and exactly the counter changes; the additive prose note
   complete; all other block fields byte-identical.
3. Bookkeeping per Scope 3 (registry 35 with exactly one new 009-b
   data-free entry; counters 35/54; incidents 2; STATUS.md; GENERATED-FILES
   pin; csv rebuild; receipt consolidation per Scope 3(f) with recorded
   byte-identity and the originals untouched).
4. Local verification per Scope 4, with the designed implementation-head
   count red and the final-head green recorded distinctly (PASSED/FAILED
   with tested SHAs).
5. The report-only commit per Scope 5.
6. Final-head CI per Scope 6: all four required checks genuinely green.
7. Exact response OK after remote verification; PR #10 stays OPEN.

## Acceptance criteria

1. The pre-work gate evidence commits; any mismatch would have BLOCKED.
2. At the final head the machine block carries main_sha =
   185dc3d9c654991619ae5c57b64e0c54f4550a16, reviewed_branch_head_sha =
   185dc3d9c654991619ae5c57b64e0c54f4550a16, reviewed_branch_head_parent_
   sha = 59d8f030a91309f4386bde48b360f17d7ea11e86, counters registry_
   entries 35 / oap_reports_reviewed 54 / frozen_report_history_incidents 2,
   and byte-identical branch, pr_number, quarantined identities, and frozen
   007-m sha fields; the additive prose note is present and the 009-a text
   is unaltered.
3. The research-state consistency test is green at the final head in a real
   checkout (every assertion, including the live-ref and 007-o-lock
   assertions); the round diff (009-a final head..final) is limited to the
   released-from-freeze list; zero secret-pattern hits in added lines; the
   untracked residue absent from every commit; the 009a-identity receipt
   copy exists under the native private root byte-identical to the
   sync-mount originals, which remain untouched.
4. All four required checks genuinely green at the final head (no pending,
   cancelled, or reinterpreted check); the response OK frame received after
   remote verification.
5. PR #10 on oap/009-target-distribution-confirmation (base main at
   185dc3d9c654991619ae5c57b64e0c54f4550a16) is OPEN; no merge; no
   auto-merge.

## Verification

- Focused: test_research_state_consistency.py (green at the final head; the
  designed implementation-head count red recorded); the 009-a focused lint
  (unchanged, still green); the full research suite; the OAP suite; one
  full local Application-baseline driver run (local evidence only).
- Broader: the full CI battery at the implementation head and the final
  head.
- Evidence boundary: software/test layer only; zero data, zero model
  calls, zero network calls beyond the bounded CI and the read-only remote
  reads of this order's own publication mechanics. The report is a claim
  until strategy's independent final-head review re-verifies it
  field-by-field (S-EVIDENCE-01, S-REVIEW-01).

## Local setup and constraints

- CPU-only; the frozen uv environment; no new dependencies; no GPU; no
  service touches; no protected Qwen weight/config/network change
  (S-PRODUCT-04); REPAIR_ALLOW_LIVE_TESTS stays NO; no endpoint,
  credential, or private path in any committed artifact.
- Local: reversible setup inside the authorized workspace only; doctor runs
  with env -u CODEX_HOME -u OAP_ROLE; any unresolvable setup failure is
  BLOCKED and reported, not worked around.

## Documentation

RESEARCH-STATE.md additive identity-advance note (Scope 2) plus the machine
block (Scope 2/3); STATUS.md per Scope 3; the OAP report per the round
mechanics (data-free; the dilemma-candidate disposition recorded: classified
D0 by strategy per the documented 008-a/008-b precedent - single viable
non-weakening remedy; no CRIT admission; the 009-a report's candidate
report stands as the coding-side record).

## Git and report publication

- AMEND_EXISTING_PR on oap/009-target-distribution-confirmation (PR #10)
  from the 009-a final head d8e306812b5c265ecb5dca2ecc2b39a296cea8a4; the
  PR base remains main at 185dc3d9c654991619ae5c57b64e0c54f4550a16.
- Activation commit (order + oap/active) per the round mechanics;
  implementation commits per Scope 2-3 (exact split at the executor's
  discretion, all within the released-from-freeze list); the report-only
  commit per Scope 5.
- Push semantics per the OAP communication profile; no force-push; no push
  after the report-only commit; the exact response OK after remote
  verification; the coding wrapper consumes the 009-b control signal exactly
  once before model launch.
- No merge: PR #10 stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act (S-MERGE-01).

## Decision classification

D0 (S-DECIDE-01): routine, reversible bookkeeping within the risk budget,
following the documented 008-a/008-b precedent for the identical structural
condition; the 009-a coding round's D1 dilemma-candidate report is
reclassified D0 by strategy with the exact green path verified from the
test source; no human judgment debt; no CRIT admission (S-DECIDE-03
condition 1 fails: the governing test contract, the documented precedent,
and the owner's A1 instruction leave exactly one viable non-weakening
path). The E2 target-deployment question remains a blocked D2/human
boundary, untouched by this round.

## Deferred human adjudication

- Decision: NONE

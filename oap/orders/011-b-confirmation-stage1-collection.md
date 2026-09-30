# 011-b: Confirmation study stage-1 collection on the designated A100-FP8 target (objective 011, round 2; E2(b) designation recorded, manifest-first deterministic collection, data-free commits; PR #12 held open)

Status: FINAL

```oap-metadata
{
  "id": "011-b",
  "title": "Confirmation study stage-1 collection on the designated A100-FP8 target (objective 011, round 2; E2(b) designation recorded, manifest-first deterministic collection, data-free commits; PR #12 held open)",
  "objective": "011",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "2e5d76d16875b3f0cede4b9c49ddf32ab70faee4",
  "branch": "oap/011-target-distribution-confirmation-study",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 12,
  "dependencies": ["007", "008", "009", "010", "011"],
  "local_work": "Preserve byte-for-byte: the entire objective-000..011-a tree at base 2e5d76d16875b3f0cede4b9c49ddf32ab70faee4, including research/target-distribution/PROTOCOL-009.md (sha256 cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a, FROZEN - the single source of truth for this round; every scientific element below transcribes it, none reopens it), research/target-distribution/DEPLOYMENT-IDENTITY-009.md (sha256 b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4, FROZEN - carries the resolved E2 decision package and the 009-a pinned identity), research/tests/test_009a_protocol_elements.py, all 007-m frozen surfaces (config projection 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, deployment profiles c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), the objective-011-a artifacts (oap/orders/011-a-post-merge-machine-block-identity-advance.md, oap/reports/011-a-post-merge-machine-block-identity-advance.md, RESEARCH-STATE section 25, the 011-a ledger entry, machine block at main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8 with counters registry_entries 37 / oap_reports_reviewed 56 / frozen_report_history_incidents 2), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, the private research-runtime roots (including 009a-identity/ under the native private root and the new round-private 011b-identity/ directory, which is private and never committed), and any unrelated local work (the three untracked residues corpus/, .research-test-scratch/, .rclone-speed-test/ are pre-existing and never committed).",
  "prior_review": "Strategy independent final-head review of 011-a (2026-09-30, private workorders/011-a-final-head-review-20260930.md): verdict PASS - exactly the five ordered machine-block field changes (main_sha/reviewed head 4507cc78e333c0e48226b64266121171b7b8cea8, parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 37/56/2), sections 1-24 byte-identical, additive section 25, registry 37, round diff exactly the eight released paths, local consistency 10/10 at the final head in a real checkout, precise secret scan zero hits, all four required checks genuinely green at final head 2e5d76d16875b3f0cede4b9c49ddf32ab70faee4 (every check run at that head_sha; Application baseline 7m55s, OAP bootstrap 4m39s, OAP report history 6s, Research reproducibility 27s); the designed implementation-head count red (56 vs 55) plus one transient FUSE WhitespaceVerifier stall (manual repro green, non-gating precedent class) were the only reds at the implementation head. HOLD decision recorded in that review: PR #12 stays OPEN (no merge, no auto-merge) so objective-011 rounds b and beyond can amend it - the objective's PR accumulates its rounds and merges only at the objective's end (the PR #9 / PR #10 pattern); merging per round is what forced the 010->011 rollover and is not repeated. E2 RESOLVED (private workorders/e2b-decision-receipt-20261001.md): the owner's verbatim decision '(b) Designate A100-FP8 as the confirmation target' (2026-09-30, owner strategic thread; recorded by the successor strategic session 2026-09-30T22:11Z) selects alternative E2(b) of the committed decision package (DEPLOYMENT-IDENTITY-009.md section 4): the A100-FP8 regime is designated the confirmation target as a recorded product-intent change; no replication is required (the frozen method was developed and frozen on this regime); the PROTOCOL-009 element (a) hard gate is lifted for this regime only, subject to this round's bounded freshness re-probe before the first sample is opened. The 009-a pinned identity (DEPLOYMENT-IDENTITY-009.md section 1: vLLM 0.28.0, model qwen3.8-27b, root suffix Qwen3.8-27B-FP8, max model length 262144, Responses wire API non-streaming; private attempt-level receipt in the 009a-identity directory of the round private research runtime root) is the reference identity for that re-probe; the authorized out-of-band profile (endpoint and bearer) was re-provisioned by the owner out-of-band at successor-session start (2026-09-30 evening CEST) and is recorded in the private controlled-storage receipt 011b-identity/target-credentials-20261001.json (0600; value never committed, never logged, never echoed).",
  "provenance": [
    {"kind": "H", "reference": "Owner objective-009 start instruction 2026-09-30 (freeze the protocol first; continue the loop into data collection/annotation/evaluation under subsequent proof-sized suffixes without the owner as terminal relay; escalate only genuine human/D2 decisions; ~99% accepted-repair correctness and <=1 harmful intervention per 10,000 originally-correct words are evaluation/calibration targets, not release authorization); the owner's verbatim E2(b) decision 2026-09-30 '(b) Designate A100-FP8 as the confirmation target' (private receipt workorders/e2b-decision-receipt-20261001.md); the standing A1 instruction (all four required checks genuinely green; red required checks never reinterpreted; no weakening); the owner's out-of-band endpoint/bearer provisioning (controlled storage only)."},
    {"kind": "A", "reference": "research/target-distribution/PROTOCOL-009.md (FROZEN, cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a) elements (b)-(n) and section 4 (population and manifest-first collection procedure with the pre-registered seed string 009a-target-distribution-20260930; domain mix with the 10 percent floor; stage-1 size 50-100 target 100 floor 50 with shortfall reason; correct-text negative controls >=25 percent with >=10 human-authored technical/rare/name; the exact annotation taxonomy; the two-labeler adjudication procedure and 5-document calibration pilot; the 15/85 deterministic split with zero leakage against all 007/008 material; the four required comparators and optional fifth; the six metric families with denominators; Clopper-Pearson and 3/N semantics with EXACT/CENSORED/UNAVAILABLE preserved; the four stopping rules; the first-failing-stage decomposition; the no-tuning-after-unblinding rule covering the calibration subset; data rights and controlled storage with data-free committed artifacts); research/RESEARCH-STATE.md section 13 (objective-009 design requirements: 100 real outputs, human annotation required, explicit rights and controlled storage, Qwen never final judge, frozen method identity, primary and operational metrics, failure decomposition, stopping rules, the two 2026-09-17 prohibitions); PLAN 14.2/14.3 (comparators, ~50-100 initial genuine outputs expanding toward 100-500, fully correct Slovenian text including technical language/rare expressions/names, thresholds/calibration separated from the final test set, evaluation/calibration targets not release authorization); DEPLOYMENT-IDENTITY-009.md section 4(b) (the E2(b) impact statement); S-ORDER-03 (corrective/continuation suffixes preserve branch and PR while that PR is open); S-PRODUCT-02 (EXACT/CENSORED/UNAVAILABLE and denominator semantics); S-PRODUCT-04 (protected Qwen/services; explicit rights for evaluation data; no credentials in artifacts); LR-001 (complete main capture precedes review), LR-013 (data-free public artifacts), LR-014 (bounded one-pass review); the frozen 007-m profile contract (config 0026a1a9..., prompt 572cf2fb..., deployment profiles c79fd658.../0c4aa490...) as the exact main-request contract for the genuine-output generation calls."},
    {"kind": "E", "reference": "Observed 2026-09-30T22:0x-22:1xZ (this successor session, from remote and primary records): remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 = OAP_ACCEPTED_REF (the accepted objective-010 merge); the worktree is on branch oap/011-target-distribution-confirmation-study at 2e5d76d16875b3f0cede4b9c49ddf32ab70faee4 (the 011-a final head; activation 02e6ab4, implementation 333b02d, report-only 2e5d76d); PR #12 OPEN and MERGEABLE at head 2e5d76d, base main, autoMergeRequest null, and the ONLY open PR; oap/active = 011-a; OAP state REVIEW_READY (011-a); CRITICAL.md seed-identical a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e with zero entries; machine block on the 011 branch at 2e5d76d carries main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8, parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters registry_entries 37 / oap_reports_reviewed 56 / frozen_report_history_incidents 2 with branch oap/007-concept-verification and pr_number 8 unchanged; local consistency 10/10 at the final head (verified in the 011-a review; re-verified by this session's pre-work gate); the 009-a C2 re-probe receipt (private 009a-identity/c2-reprobe-receipt.json): 4/6 attempts, 0 generation calls, 0 RTX-3090 contact, 0 Deployment B contact, observed identity vLLM 0.28.0 / qwen3.8-27b / Qwen3.8-27B-FP8 / 262144 / Responses non-streaming, observation window 2026-09-30T01:09:44Z-01:10:22Z; PROTOCOL-009 and DEPLOYMENT-IDENTITY-009 byte-verified at the base this session (cc5e9089... and b6734b35...). Zero-leakage source census (data-free, this session): the four public Slovenian datasets present in the private evaluation-data location (DASSLE, MultiGEC, SloBench, Solar) were consumed by the objective-007 campaign (RESEARCH-STATE section 4: full-campaign8 16,375 cases across them; the 007-h chain consumed the 2,973-pair DASSLE-derived population) and are therefore INSPECTED for an earlier objective and ineligible for the confirmation population under PROTOCOL-009 (h); every entry in the private research runtime root (447 top-level entries: addendum-fidelity-*, distinct-dispatch-*, integrity-recipe-*, historical-executable-*, llm-slovenian-index-recovery-*, 007-* scratch, 008*-hidden, 008i-*) is machine-generated research scratch from objectives 007/008 - no fresh, uninspected, human-authored Slovenian corpus exists in any reachable private location; the only zero-leak-compliant source is fresh human-authored material supplied by the owner/designee under explicit rights (the human dependency of scope item 3)."},
    {"kind": "I", "reference": "Strategy 011-a final-head review PASS with the PR-hold decision (private workorders/011-a-final-head-review-20260930.md); the 2026-09-30 quiescent post-merge checkpoint and rollover record (private workorders/post-merge-checkpoint-20260930-010.md); the 011-b pre-draft (private workorders/draft-011b-confirmation-stage1-collection-20260930.md), finalized here by bounded edit after the E2(b) resolution (E2-branch prelude collapsed to the (b) path; artifact names renumbered -010 -> -011; the eligible-inventory definition resolved per the E reference so the PROTOCOL-009 (b) selection rule is executable and the zero-leakage assertion is makeable); the technical-debt register (TD-1 diffscope --commit-only, TD-2 driver subprocess-tree timeout kill, TD-3 FUSE 30-s git-walk - all non-gating, carried forward)."}
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

Objective 011, round 2, on the EXISTING branch
`oap/011-target-distribution-confirmation-study` (AMEND_EXISTING_PR - PR #12,
verified OPEN and MERGEABLE at head
`2e5d76d16875b3f0cede4b9c49ddf32ab70faee4`, the 011-a final head, base
main at `4507cc78e333c0e48226b64266121171b7b8cea8`). The objective's PR
stays open across its suffix rounds and merges only at the objective's end
(the PR #9 / PR #10 pattern; the 011-a review HOLD decision). This is the
**stage-1 COLLECTION round of the target-distribution confirmation study**
on the E2(b)-designated A100-FP8 regime: it records the designation,
re-verifies the pinned identity by bounded metadata re-probe, ingests the
owner/designee-supplied fresh human-authored corpus, performs the
manifest-first deterministic selection and split, generates the stage-1
genuine outputs, and prepares the annotation infrastructure - and NOTHING
else. It performs no evaluation, no scoring, no annotation, and no
comparator run (those are 011-c); it performs no behavior change of any
frozen element (PROTOCOL-009 (n)); it makes no merge, release, deployment,
or milestone claim. The single named human input (the intake corpus) is a
pre-specified external dependency with a BLOCKED-once escalation path, not
a relay loop.

## Provenance

- H: owner 2026-09-30 objective-009 instruction (continue the loop into
  collection/annotation/evaluation under proof-sized suffixes; the owner
  is not a terminal relay; escalate only genuine human/D2 decisions; the
  ~99% and <=1/10,000 numbers are calibration targets, not release
  authorization), the verbatim E2(b) decision 2026-09-30 (private receipt
  `workorders/e2b-decision-receipt-20261001.md`), the standing A1
  instruction, and the out-of-band endpoint/bearer provisioning
  (controlled storage only).
- A: FROZEN PROTOCOL-009 (cc5e9089...) elements (b)-(n) and section 4;
  RESEARCH-STATE section 13; PLAN 14.2/14.3; DEPLOYMENT-IDENTITY-009
  section 4(b); S-ORDER-03; S-PRODUCT-02/04; LR-001/013/014; the frozen
  007-m profile contract for the main-capture calls.
- E: the verified state recorded in the metadata E field (main, PR #12,
  worktree, machine block 37/56/2, 10/10 local consistency, CRITICAL seed,
  009-a re-probe identity facts) plus the data-free zero-leak source
  census: the DASSLE/MultiGEC/SloBench/Solar evaluation datasets are
  ineligible (consumed by the objective-007 campaign, RESEARCH-STATE
  section 4), all private research scratch is 007/008 machine-generated,
  and no fresh uninspected human-authored corpus exists in any reachable
  private location - hence the intake is a human input.
- I: strategy's 011-a final-head review PASS with PR-hold decision, the
  2026-09-30 post-merge checkpoint/rollover record, the 011-b pre-draft
  finalized by bounded edit (E2(b) branch; -011 renumbering;
  eligible-inventory definition), and the technical-debt register (TD-1/2/3
  non-gating).

## Current verified state

Verified 2026-09-30T22:0x-22:1xZ (successor strategic session, from remote
and primary records): remote main =
`4507cc78e333c0e48226b64266121171b7b8cea8` (= OAP_ACCEPTED_REF; the
accepted objective-010 merge; parents a501b20af7f6d9774df989c41c5ec27e21b36f3e
+ 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d); worktree on
`oap/011-target-distribution-confirmation-study` at
`2e5d76d16875b3f0cede4b9c49ddf32ab70faee4` (011-a final head; activation
02e6ab4, implementation 333b02d, report-only 2e5d76d) with the three
pre-existing untracked residues (corpus/, .research-test-scratch/,
.rclone-speed-test/) preserved and never committed; PR #12 OPEN,
MERGEABLE, head 2e5d76d, base main, autoMergeRequest null, the only open
PR; oap/active = 011-a; OAP state REVIEW_READY (011-a); CRITICAL.md
seed-identical
a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e,
zero entries; machine block on the 011 branch at 2e5d76d: main_sha /
reviewed_branch_head_sha 4507cc78e333c0e48226b64266121171b7b8cea8, parent
01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, branch
oap/007-concept-verification, pr_number 8, quarantined 007n/008d, frozen
007-m sha fields, counters registry_entries 37 / oap_reports_reviewed 56 /
frozen_report_history_incidents 2; local consistency 10/10 at the final
head (011-a review; re-verified by this session's pre-work gate);
registry = 37 entries (last 011-a, kind state-correction, status COMPLETE);
transcript valid at the branch final head (56 orders
000-a..011-a; 56 reports; two known frozen 006-a/006-c incidents); PROTOCOL-009 (cc5e9089...) and
DEPLOYMENT-IDENTITY-009 (b6734b35...) byte-verified at the base this
session; the coding wrapper (pid 2467156, supervisor 412040) is alive and
idle on the control fifo with no model child; REPAIR_ALLOW_LIVE_TESTS = NO
(unchanged). Environment: the rclone/Dropbox FUSE mount remains degraded
(minutes-scale stalls); heavy test temp stays on native
/home/ubuntu/.oap-scratch (0700); OAP helper git-history traversals can
transiently time out at the 30 s subprocess limit on a cold cache (TD-3,
non-gating; retry is deterministic and safe); CI parity is authoritative
for the heavy fixture cycles.

## Governance

The sixteen source identities in the metadata governance mapping are the
exact identities of `oap/governance/MANIFEST.json` at the accepted base
`4507cc78e333c0e48226b64266121171b7b8cea8`, unchanged since the 011-a
round (governance accepted-runtime 16/16, coding_bytes 35076, verified at
the 2026-09-30 quiescent checkpoint). No governance change occurs in this
objective. The private research-runtime root layout (round-private
011b-identity/, 011b-intake/, 011b-collection/, 011b-packets/ directories
under the native private root; 0700 directories, 0600 files) follows the
established 009a-identity convention; none of it is ever committed.

## Goal and dependencies

Goal: complete PROTOCOL-009 stage-1 collection on the E2(b)-designated
A100-FP8 regime exactly as preregistered: record the designation in a
committed data-free identity record, re-verify the pinned identity by
bounded metadata re-probe (regime unchanged or stop at the drift finding),
ingest the owner/designee-supplied fresh human-authored corpus under
explicit rights, create the collection manifest FIRST, perform the
deterministic seeded selection and 15/85 split with the 5-document
calibration pilot, generate the stage-1 genuine outputs (target 100, floor
50) plus the control outputs under the frozen main-capture contract,
prepare the annotation guide and labeler packets, and commit only
data-free artifacts - so that 011-c (annotation consolidation +
comparative evaluation) starts from a fully frozen, fully manifest-
documented, zero-leak stage-1 population.

Dependencies: 011-a (reviewed PASS; PR #12 held open; green quiescent
branch base), the owner E2(b) decision (attributable, private receipt),
the owner/designee intake corpus (scope item 3 - the single named human
input), and 007/008/009/010 only as the frozen surfaces preserved by the
local_work field. The two Slovenian-native independent labelers are a
011-c input, not a 011-b input (this round only prepares the packets).

## Scope

1. Pre-work integrity gates (data-free): at the base
   `2e5d76d16875b3f0cede4b9c49ddf32ab70faee4`, byte-verify every frozen
   surface and the objective-009/011-a artifacts (PROTOCOL-009.md,
   DEPLOYMENT-IDENTITY-009.md, test_009a_protocol_elements.py, the 007-m
   pins, the 008 protection-layer pins, the 011-a order and report,
   RESEARCH-STATE sections 24-25, CRITICAL.md seed-identical
   a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e);
   machine block on the branch: main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8,
   parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 37/56/2,
   identity fields unchanged; registry = 37 entries (last 011-a); local
   consistency 10/10 in a real checkout of the branch with origin/main =
   4507cc78e333c0e48226b64266121171b7b8cea8. Any mismatch is BLOCKED with
   the mismatch named; no work proceeds.
2. E2(b) prelude - designation record and bounded freshness re-probe:
   a. Commit `research/target-distribution/DEPLOYMENT-IDENTITY-011.md`
      (data-free: no endpoint values, no credentials, no private paths, no
      raw text): (i) the E2(b) designation recorded VERBATIM (the owner's
      exact decision message; attribution: 2026-09-30 owner strategic
      thread; private receipt referenced by name only, never reproduced);
      (ii) the product-intent-change impact statement per
      DEPLOYMENT-IDENTITY-009 section 4(b) (evidence transferability NONE
      to the RTX-3090 target; the study confirms the designated regime;
      the target-distribution label refers to it; future RTX-3090
      deployments remain unconfirmed by this study; no replication
      required); (iii) the 009-a pinned identity referenced by hash only
      (committed record b6734b35...; private 009a-identity receipt in the
      round private research runtime root); (iv) the freshness re-probe
      attempt record (timestamps, statuses, observed identity fields,
      response sizes - data-free values only) and the verdict; (v)
      reaffirmed boundaries (RTX-3090 MUST-NOT-BE-STARTED, zero contact;
      Deployment B EXCLUDED_BY_HUMAN_OVERRIDE, zero contact, ever;
      REPAIR_ALLOW_LIVE_TESTS stays NO).
   b. Bounded freshness re-probe BEFORE the first sample is opened:
      EXACTLY 2 metadata GETs (serving-version endpoint; models endpoint
      with the authorized bearer), no retries, zero
      chat/generation/responses calls, zero other endpoints, zero writes,
      zero server mutation, zero RTX-3090 contact, zero Deployment B
      contact. The authorized profile (endpoint + bearer) is read ONLY
      from the private 011b-identity credentials receipt (0600; the value
      is never committed, never logged, never echoed into any report or
      public artifact). Every attempt is recorded in the round private
      receipt `011b-identity/reprobe-receipt.json` (private, never
      committed).
   c. Verdict rule: all observed identity fields MATCH the 009-a pin
      (serving framework version 0.28.0; model identifier qwen3.8-27b;
      root suffix Qwen3.8-27B-FP8; max model length 262144; wire protocol
      class OpenAI-compatible Responses non-streaming) -> regime
      unchanged, proceed to item 3. ANY field mismatch, or a transport
      failure within the 2-attempt budget -> the round STOPS at that
      finding: the data-free finding is recorded in
      DEPLOYMENT-IDENTITY-011.md, Result: BLOCKED (drift or probe
      failure) with the exact mismatch named; no intake, no manifest, no
      collection, no split, no sample opened; an intervening round is
      required before any collection.
3. Human input gate - the intake corpus (the single named human
   dependency; escalated ONCE if missing, never relayed per-sample):
   a. Declared intake location: the `011b-intake` directory under the
      round private research runtime root (0700; document files 0600),
      created by this round if absent. The owner/designee places the
      corpus there BEFORE the round's intake check (the check occurs
      after item 2, before the manifest of item 4).
   b. Intake specification (exact; the escalation, if needed, quotes
      this verbatim):
      - GENUINE_OUTPUT_SOURCE documents: target >= 100 (floor 50; a
        floor-or-above intake proceeds, the shortfall is recorded at
        selection); fresh, human-authored Slovenian documents, one UTF-8
        text file each; content spanning the three pre-declared domains
        (general prose; technical language; rare expressions and proper
        names) with naturally occurring language quality (errors as they
        genuinely occur in human writing - NO synthetic error injection,
        NO model-assisted authoring or editing of any source document).
      - FULLY_CORRECT_CONTROL documents: target >= 34 (the quota is
        recomputed at selection per item 5: C >= ceil(G/3) where G is the
        number of selected genuine outputs; the intake should cover the
        target-100 case); fresh, human-authored, FULLY CORRECT Slovenian
        documents, one UTF-8 text file each; AT LEAST 10 of the delivered
        controls must be tagged technical or rare-expression-name.
      - Per-document data-free sidecar JSON (delivered alongside each
        document; the sidecar contains NO raw text, only): doc_slug;
        domain_tag in {general-prose, technical, rare-expression-name};
        source_kind in {GENUINE_OUTPUT_SOURCE, FULLY_CORRECT_CONTROL};
        authorship attestation (human-authored by <name/designee>,
        <date>); rights statement (one line; e.g. owner-provided for
        internal evaluation use, no redistribution); eligibility
        attestation (never generated or inspected for any OAP objective
        000-011; not derived from DASSLE, MultiGEC, SloBench, Solar, or
        any 007/008 research set); for controls additionally
        fully_correct_attested: true.
      - Exclusions (zero-leak (h), hard): any document generated by any
        model; any document from or derived from the DASSLE, MultiGEC,
        SloBench, or Solar datasets (consumed by objective 007 -
        RESEARCH-STATE section 4); any document from or derived from any
        007/008 research set (hidden sets, naturalistic sets, scratch);
        any document previously inspected by the research team for any
        objective; any document lacking the rights statement.
   c. Intake verification (this round): file census; domain-tag
      distribution; sidecar well-formedness; per-file sha256 (content-
      free); eligibility attestation present on every file; excluded-
      corpus provenance check against the attestations. Any document
      failing verification is REJECTED from the eligible inventory (named
      in the report; the file stays private and unopened).
   d. BLOCKED-on-input rule: if the intake is absent, or the delivered
      GENUINE_OUTPUT_SOURCE count is below the floor of 50, or fewer than
      10 delivered controls are tagged technical or rare-expression-name,
      or fewer than ceil(50/3) = 17 controls are delivered: Result:
      BLOCKED on the named input; NO manifest finalization, NO selection,
      NO split, NO generation call, NO sample opened; a truthful report
      is published and the exact response OK sent; strategy escalates to
      the owner EXACTLY ONCE with the item-3b specification (including
      the declared private intake location and the delivery mechanics:
      plain UTF-8 files + sidecars, 0600); the loop then waits for the
      human input - the same round is resumed by a recovery re-signal
      (S-RECOVER-01) once the input is in place, from the first
      unfinished requirement. This is the pre-authorized escalation path;
      the owner is never a terminal relay for per-sample work.
4. Collection manifest FIRST (before any sample is opened): commit
   `research/target-distribution/011b-collection-manifest.json`
   (data-free: counts, IDs, tags, timestamps, hashes, selection
   mechanics; NO raw text, NO endpoint values, NO credentials, NO private
   paths). Contents: (i) the full intake census (collection ID, domain
   tag, source kind, delivery timestamp, private file sha256,
   verification status per document); collection IDs are assigned by
   this round deterministically as `011b-<seq:04d>` in sorted (domain_tag,
   doc_slug) order at intake verification, and are immutable once
   recorded; (ii) the selection draws per item 5 with the exact PRNG
   mechanics recorded (seed string, single instance, draw order, per-draw
   list lengths and final list identities by collection ID - all
   data-free); (iii) the partition per item 6 (pilot / calibration /
   confirmation, by collection ID lists); (iv) the pinned identity
   reference by hash only (b6734b35... committed record; re-probe verdict
   from item 2); (v) the per-sample call metadata filled during
   generation (per collection ID: HTTP status, wall time, token counts,
   capture size, state EXACT/CENSORED/UNAVAILABLE - numbers only);
   (vi) the zero-leakage assertion (per-document eligibility attestations
   plus the aggregate statement: no case in this population was generated
   or inspected for any earlier objective 000-011a, and no case is from
   or derived from the excluded corpora).
5. Stage-1 selection (pre-registered, deterministic; transcribes
   PROTOCOL-009 (b)/(c)/(d)/(e)): a single PRNG instance
   `rng = random.Random("009a-target-distribution-20260930")` (Python
   3.12, frozen environment; the pre-registered seed string) is created
   once and drawn in this exact order, every draw over its list sorted
   lexicographically by collection ID, without replacement, via
   `i = rng.randrange(len(remaining)); take remaining.pop(i)`:
   - Draw 1 (genuine outputs): from the eligible GENUINE_OUTPUT_SOURCE
     list, up to 100 (target; if the eligible list is smaller, take all -
     the floor-50 rule of item 3d bounds BLOCKED; any shortfall between 50
     and 100 is RECORDED with its reason in the manifest and report, per
     PROTOCOL-009 (d)).
   - Draw 2 (technical/rare-name controls): from the eligible
     FULLY_CORRECT_CONTROL documents tagged technical or
     rare-expression-name, up to 10.
   - Draw 3 (remaining controls): from the remaining eligible
     FULLY_CORRECT_CONTROL documents (general-prose), up to
     `ceil(len(draw 1)/3) - len(draw 2)` (the >= 25 percent stage-1
     control quota, C >= ceil(G/3)); if draw 2 took fewer than 10 (the
     intake delivered fewer), draw 3 tops the total up to
     `ceil(len(draw 1)/3)` from the general-prose controls, and the
     resulting shortfall against the >=10 technical/rare-name condition
     is recorded as a BLOCKED condition per item 3d (the intake gate
     would have blocked before selection; this clause is the
     fail-closed remainder).
   - Domain-floor check (PROTOCOL-009 (c)): over the selected draw-1
     documents, no domain below 10 percent of the selected stage size; a
     violation is RECORDED (it triggers expansion in 011-d per the
     pre-registered criteria - never re-labeling of collected documents).
   - The selected set (G genuine-output sources + C controls) is the
     stage-1 population; the unselected eligible documents remain
     available for 011-d stage-2 expansion only (fresh, uncollected,
     unopened; no re-sampling of the selected set).
6. Split and calibration pilot (deterministic, at collection time,
   before the confirmation subset is opened; transcribes PROTOCOL-009
   (g)/(h)):
   - Pilot: the first 5 draw-1 documents in lexicographic order of the
     hex encoding of sha256(collection ID) -> the 5-document calibration
     pilot (genuine outputs; excluded from BOTH the calibration subset
     and the confirmation subset; used only for labeler alignment in
     011-c; never scored or used for method decisions).
   - Let N = (len(draw 1) - 5) + C (the stage-1 documents excluding the
     pilot). k = ceil(0.15 * N). Calibration subset = the first k of the
     N documents in lexicographic order of the hex encoding of
     sha256(collection ID); confirmation subset = the remaining
     N - k documents, UNTOUCHED until final scoring in 011-c.
   - The three partitions (pilot / calibration / confirmation) are
     disjoint and cover the selected stage-1 documents exactly; the
     partition is recorded in the manifest (item 4) by collection ID
     lists. Zero leakage between partitions and with any 007/008 material
     is asserted in the manifest (item 4 vi).
   - The calibration subset's use (operational verification of the frozen
     pipeline mechanics in 011-c) is OUT of this round's scope; this
     round computes and records the partition and nothing else about
     those documents.
7. Genuine-output generation (the bounded live work of this round;
   authorized by the E2(b) decision + PROTOCOL-009, separately from
   REPAIR_ALLOW_LIVE_TESTS = NO which stays unchanged): for EACH selected
   document (G sources + C controls), exactly ONE main-capture call on
   the pinned target configuration, under the product's intended use and
   the FROZEN 007-m profile contract (configuration 0026a1a9..., prompt
   572cf2fb..., deployment profiles c79fd658.../0c4aa490...; Responses
   wire API non-streaming; complete stored main answer per LR-001;
   protocol limits 300 s / 2,000,000 bytes; one terminal attempt; no
   resampling; no retry). The stored main answer is the collected sample.
   Per sample: input document + main answer + call metadata stored
   privately under the round-private `011b-collection` directory (0700;
   0600 files; NEVER committed); the data-free per-sample metadata is
   recorded in the manifest (item 4 v). A call failure is recorded with
   its state (EXACT/CENSORED/UNAVAILABLE semantics preserved - missing or
   censored evidence is never reported as zero, LR-008/S-PRODUCT-02);
   the failed document is excluded from the stage set with the failure
   named; if exclusions drop the genuine-output count below the floor of
   50, the round reports Result: BLOCKED on the named shortfall (no
   partial-quiet claim; the split and bookkeeping of the completed
   samples are still recorded truthfully). NO review/repair calls in this
   round (the review stage belongs to the 011-c comparators); NO second
   or larger GPU model; NO contact with any endpoint other than the
   designated target.
8. Annotation guide and labeler packets (preparation only; the labelers
   are a 011-c input):
   a. Commit `research/target-distribution/ANNOTATION-GUIDE-011.md`
      (data-free; operationalizes PROTOCOL-009 (f)/(g)/(j)): the exact
      taxonomy (source ground truth per span/document: ACTUAL_ERROR,
      ACCEPTABLE_UNCHANGED, FULLY_CORRECT_DOCUMENT, NEEDS_WIDER_EDIT;
      intervention outcome per accepted edit: CORRECTS_ERROR,
      ACCEPTABLE_ALTERNATIVE, HARMLESS_STYLISTIC, HARMFUL_CHANGE,
      NO_CHANGE; layer-failure classes: PROTECTION_FAILURE, DETECTOR_MISS,
      CANDIDATE_GENERATION_MISS, RANKING_MISS, VALIDATOR_REJECTION_OR_
      FAILURE, ACCEPTANCE_POLICY_REJECTION, PATCH_FAILURE; mandatory
      DETECTOR_MISS on every genuine error not flagged); the two-labeler
      procedure (two independent Slovenian-native labelers per detected
      span and per document; disagreement recorded; ambiguous cases
      adjudicated by the owner or a named human with a recorded rationale
      class; Qwen is NEVER the final judge of its own changes - PLAN
      14.2); the calibration-pilot procedure (alignment only; never
      scored; labelers do not see internal stage decisions before final
      scoring); the metric-family denominators per PROTOCOL-009 (j)
      (accepted-repair correctness over assessed accepted edits; harmful
      interventions per 10,000 originally-correct words with the frozen
      word counter; detector coverage and final-repair coverage
      separately; stylistic-only rate; preservation over FULLY_CORRECT
      controls; operational cost components); the EXACT/CENSORED/
      UNAVAILABLE semantics (k).
   b. Prepare the labeler work queues under the round-private
      `011b-packets` directory (0700/0600; NEVER committed): the 5 pilot
      packets, each containing the input document, the collected main
      answer, and the frozen CPU detector's span output on that main
      answer (frozen detector, no intervention, no review call, no
      accepted edit, no scoring in this round); the per-span/per-document
      queue structure for the calibration and confirmation subsets (IDs
      and hashes only until 011-c opens them). Data-free aggregates
      (packet counts, file hashes) are committed with the manifest; no
      raw text is committed.
9. Bookkeeping (data-free): (a) exactly one 011-b entry appended to
   `research/registry/experiments.json` (registry 37 -> 38; data-free;
   kind collection; status per the round outcome COMPLETE or BLOCKED;
   counts and partition sizes only; private locations referenced by
   relative directory names only); (b) machine-block counters
   registry_entries 37 -> 38 and oap_reports_reviewed 56 -> 57 (the 011-b
   report file), frozen_report_history_incidents unchanged at 2; all
   identity fields UNCHANGED (no advance - that is a post-merge round's
   job); (c) STATUS.md round sentences; (d)
   `oap/GENERATED-FILES.json` scoped pin (same scope pattern as 009-a/
   009-b/010-a/011-a, extended with this round's artifacts); (e)
   `research/tables/experiment-summary.csv` rebuild; (f)
   `research/RESEARCH-STATE.md` additive section 26 (the 011-b
   collection record: intake census, selection draws, stage-1 sizes,
   domain mix, split sizes, per-call statistics data-free, re-probe
   verdict, zero-leakage assertion, private locations by relative name;
   NO rewrite of sections 1-25 or the machine block except item 9b).
10. Report-only final commit: sole parent = the literal implementation
    head; sole changed path
    `oap/reports/011-b-confirmation-stage1-collection.md`; the report
    discloses the final-head check state verbatim and, in the BLOCKED
    branches, the exact gate and named input with zero samples opened.
11. Final-head CI: all four required checks green at the final head (or
    the predeclared re-run state disclosed verbatim at report time,
    resolved before strategy's final-head review).
12. Push and verify; send the exact response OK and stop. PR #12 stays
    OPEN; no merge; no auto-merge.

## Non-goals

- No evaluation, no scoring, no metric computation on the confirmation
  or calibration subset, no comparator run (ORIGINAL / DETECTOR_ONLY /
  DIRECT_QWEN_PROOFREADING / FROZEN_RESTRICTED_METHOD / CORPUS_ONLY all
  belong to 011-c).
- No annotation by any model or any human in this round (Qwen is NEVER
  the final judge; the two labelers are a 011-c input; the pilot is
  prepared but not scored).
- No behavior change of any frozen element (PROTOCOL-009 (n) no-
  tuning-after-unblinding, which covers the calibration subset too):
  candidate rule, ranking tuple, detector thresholds/eligibility,
  candidate semantics, validator prompt/parser/protocol, reasoning level,
  acceptance policy, protocol limits, retry policy, protection rules -
  all untouched; an operational finding that would suggest a behavior
  change STOPS the round and escalates.
- No PROTOCOL-009.md, DEPLOYMENT-IDENTITY-009.md, or frozen-surface
  change; no test change; no governance or CRITICAL.md change; no
  OAP protocol change.
- No merge, no auto-merge, no force-push, no release, no deployment, no
  milestone claim, no E2 re-opening (the designation stands; only the
  011-b drift stop-condition could reopen a boundary, and it would stop
  the round, not decide anything).
- No contact with the RTX-3090 host (MUST-NOT-BE-STARTED; zero probes,
  zero calls), no contact with Deployment B (EXCLUDED_BY_HUMAN_OVERRIDE;
  zero probes, zero calls, ever), no second large GPU model, no server
  mutation.
- No raw confirmation text, no endpoint values, no credentials, no
  private absolute paths in any committed artifact or log (PROTOCOL-009
  section 4; LR-013); the private tree is NEVER committed; the
  publication guard runs on the full tree pre-push.
- No re-labeling of collected documents, no re-sampling of the selected
  set, no synthetic stand-in for genuine outputs.

## Files and boundaries

Write (repository): exactly
`research/target-distribution/DEPLOYMENT-IDENTITY-011.md` (new, data-
free), `research/target-distribution/ANNOTATION-GUIDE-011.md` (new, data-
free), `research/target-distribution/011b-collection-manifest.json` (new,
data-free), `research/RESEARCH-STATE.md` (additive section 26 + machine-
block counters only), `research/registry/experiments.json` (+1 data-free
entry), `STATUS.md`, `oap/GENERATED-FILES.json` (scoped pin),
`research/tables/experiment-summary.csv` (rebuild),
`oap/orders/011-b-confirmation-stage1-collection.md` (new, activation),
`oap/active` (pointer),
`oap/reports/011-b-confirmation-stage1-collection.md` (new, report-only
commit).
Write (private, never committed): `011b-identity/` (the pre-recorded
credentials receipt; the round re-probe receipt), `011b-intake/` (owner/
designee corpus; round-created if absent), `011b-collection/` (input +
main-answer samples and call metadata), `011b-packets/` (labeler work
queues) - all under the round private research runtime root (0700/0600).
Read-only: the rest of the accepted tree and all frozen surfaces
(byte-verified in the pre-work gate); the private 009a-identity/
directory (the 009-a pinned-identity receipt).
Coding read set: the compact sources, this order, RESEARCH-STATE
sections 13/24/25, PROTOCOL-009.md (full, frozen),
DEPLOYMENT-IDENTITY-009.md, the frozen 007-m profile contract files, the
private 011b-identity credentials receipt (identity values only as
needed for calls), and the 011-a report.

## Requirements

1. Pre-work gates per Scope 1 (any mismatch BLOCKED and named).
2. DEPLOYMENT-IDENTITY-011.md committed per Scope 2a; the re-probe
   executed per Scope 2b (exactly 2 metadata GETs, zero generation
   calls); the verdict recorded per Scope 2c (regime unchanged ->
   proceed; drift/failure -> BLOCKED at the finding, nothing else
   executed).
3. Intake gate per Scope 3 (verification; BLOCKED-on-input rule with the
   exact named input; escalation exactly once).
4. Manifest committed data-free BEFORE any sample is opened, per Scope 4
   (census, IDs, draws, partition, identity hash reference, call-
   metadata schema, zero-leakage assertion).
5. Selection per Scope 5 (single seeded PRNG instance; three draws in
   order; domain-floor check recorded).
6. Split and pilot per Scope 6 (pilot 5; k = ceil(0.15*N); confirmation
   untouched; partition recorded).
7. Generation per Scope 7 (one terminal main-capture call per selected
   document under the frozen profile; private storage; per-sample states
   preserved; floor-50 shortfall rule).
8. Annotation guide committed per Scope 8a; pilot packets and queue
   structure prepared per Scope 8b (CPU-detector spans only; no review
   calls; no scoring).
9. Bookkeeping per Scope 9 (registry 38; counters 38/57/2; STATUS.md;
   GENERATED-FILES pin; csv; RESEARCH-STATE section 26 additive).
10. Report-only commit per Scope 10; final-head CI per Scope 11 (all
    four required checks genuinely green); exact response OK per Scope 12
    after remote verification; PR #12 stays OPEN.

## Acceptance criteria

1. The pre-work gate evidence is committed or recorded; any mismatch
   would have BLOCKED the round with the mismatch named.
2. DEPLOYMENT-IDENTITY-011.md is committed and data-free: the verbatim
   designation, the product-intent impact statement, the 009-a pin by
   hash, the complete re-probe attempt record (exactly 2 metadata GETs;
   zero generation calls; zero prohibited contact), and the verdict
   (regime unchanged) - or the round is BLOCKED at that finding with
   nothing else executed.
3. The manifest is committed data-free and was created before the first
   sample was opened; it carries the intake census, the exact PRNG
   mechanics, the partition, the identity hash reference, and the
   zero-leakage assertion; the private samples are absent from the
   repository.
4. Stage-1 collection completed (or BLOCKED truthfully at the intake
   gate or the floor-50 shortfall, with zero samples opened in the
   BLOCKED branches): G in [50, 100] genuine outputs with the shortfall
   reason recorded when G < 100; C >= ceil(G/3) controls with >= 10
   technical/rare-name; every selected document has exactly one terminal
   main-capture call with its state recorded (EXACT/CENSORED/UNAVAILABLE
   preserved).
5. The partition is exactly as specified (pilot 5, k = ceil(0.15*N)
   calibration, remainder confirmation); the confirmation subset is
   untouched beyond partitioning; the 5 pilot packets are prepared
   (input + main answer + CPU-detector spans only).
6. ANNOTATION-GUIDE-011.md is committed, data-free, and complete against
   the PROTOCOL-009 (f)/(g)/(j)/(k) taxonomy, procedure, and
   denominators.
7. Bookkeeping is complete and consistent (registry 38 with exactly one
   new 011-b data-free entry; counters 38/57/2; STATUS.md; GENERATED-
   FILES pin; csv; RESEARCH-STATE section 26 additive with sections
   1-25 unaltered).
8. The report-only commit has the literal implementation head as sole
   parent and the report path as sole changed path; the round diff
   (base..final) is limited to the released-from-freeze list; zero
   secret-pattern hits in added lines; the untracked residues absent
   from every commit; the private tree absent from every commit.
9. All four required checks genuinely green at the final head (no
   pending, cancelled, or reinterpreted check); the response OK frame
   received after remote verification.
10. PR #12 on oap/011-target-distribution-confirmation-study (base main
    at 4507cc78e333c0e48226b64266121171b7b8cea8) is still OPEN; no
    merge; no auto-merge.

## Verification

- Focused: research/tests/test_research_state_consistency.py (10/10
  green at the final head in a real checkout with origin/main =
  4507cc78e333c0e48226b64266121171b7b8cea8; at the implementation head
  exactly one designed red - the report-count assertion 57 vs 56 - the
  008-i/009-b/010-a/011-a pattern, recorded with the tested SHA); the
  009-a focused lint (research/tests/test_009a_protocol_elements.py,
  unchanged, still green); the full research suite under the frozen uv
  environment; the OAP suite to the extent feasible on the degraded
  rclone/Dropbox FUSE mount (if a heavy fixture cycle cannot complete in
  the round window, record NOT RUN with the reason - the two OAP CI jobs
  are authoritative for those cycles, the 009-a/009-b/010-a/011-a
  precedent); one full local Application-baseline driver run (local
  evidence only; the recurring FUSE git-walk 30-s subprocess timeout in
  WhitespaceVerifier is a known environmental artifact - manual repro
  distinguishes it, the 011-a precedent).
- Data-free artifact checks: the manifest JSON parses and contains no
  raw-text fields (structural schema check + content-free field audit);
  the two new committed artifacts and the report pass the repository
  publication guard (full-tree scan) pre-push; strategy re-scans the
  published report privately post-publication (endpoint/credential/
  private-path/raw-text patterns) and records it in the review.
- Broader: the full CI battery at the implementation head and the final
  head.
- Evidence boundary: the live work is EXACTLY the bounded main-capture
  calls on the E2(b)-designated target (authorized by the owner E2(b)
  decision + PROTOCOL-009, separately from REPAIR_ALLOW_LIVE_TESTS = NO
  which stays unchanged for product live tests) plus the 2-attempt
  metadata re-probe; no other network calls, no other endpoints, no
  writes anywhere on the target. Software/test evidence and live-
  collection evidence are distinct layers (S-EVIDENCE-01). The report is
  a claim until strategy's independent final-head review re-verifies it
  field-by-field (S-REVIEW-01).

## Local setup and constraints

- The frozen uv environment; no new dependencies; no GPU on this host
  (the target is the remote designated A100-FP8 deployment; NO second
  large GPU model); no service touches; no protected Qwen
  weight/config/network change (S-PRODUCT-04); REPAIR_ALLOW_LIVE_TESTS
  stays NO; no endpoint value, credential, or private absolute path in
  any committed artifact or log.
- Private roots: round-private 011b-identity/ (the pre-recorded
  credentials receipt is already in place at publication; the round
  writes only its re-probe receipt), 011b-intake/ (owner/designee-
  supplied; round-created if absent), 011b-collection/, 011b-packets/ -
  0700 directories, 0600 files, native private root, never committed.
- Local: reversible setup inside the authorized workspace only; doctor
  runs with env -u CODEX_HOME -u OAP_ROLE; heavy test temp on native
  /home/ubuntu/.oap-scratch (0700) given the degraded FUSE mount; any
  unresolvable setup failure is BLOCKED and reported, not worked around.
- Generation pacing: sequential main-capture calls (one document at a
  time, no parallel load on the shared deployment); the 300 s per-call
  limit and 2,000,000-byte capture bound are frozen; a stuck call is
  recorded CENSORED/UNAVAILABLE with the wall time, not retried.

## Documentation

- DEPLOYMENT-IDENTITY-011.md (Scope 2a) - the designation record.
- ANNOTATION-GUIDE-011.md (Scope 8a) - the operational annotation
  contract for 011-c.
- 011b-collection-manifest.json (Scope 4) - the collection record
  (data-free).
- RESEARCH-STATE.md additive section 26 (Scope 9f) - the 011-b
  collection entry in the canonical ledger narrative, plus the machine-
  block counters (Scope 9b).
- STATUS.md per Scope 9c; the OAP report per the round mechanics (data-
  free by construction: counts, IDs, states, timestamps, hashes; no raw
  text; the round's classification recorded: D0 execution of the frozen
  protocol under the owner's E2(b) authorization; no CRIT admission).

## Git and report publication

- Branch `oap/011-target-distribution-confirmation-study` (EXISTING;
  verified at `2e5d76d16875b3f0cede4b9c49ddf32ab70faee4`, PR #12 OPEN,
  base main at 4507cc78e333c0e48226b64266121171b7b8cea8). This round
  AMENDS PR #12; no new branch, no new PR, no force-push.
- Activation commit (order + oap/active) per the round mechanics;
  implementation commits per Scope 2-9 (exact split at the executor's
  discretion, all within the released-from-freeze list); the report-only
  commit per Scope 10 (sole parent = literal implementation head; sole
  changed path = the report).
- Push semantics per the OAP communication profile; no push after the
  report-only commit; the exact response OK after remote verification;
  the coding wrapper consumes the 011-b control signal exactly once
  before model launch.
- No merge: PR #12 stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act at the objective's end (S-MERGE-01;
  repository-approved method: standard merge commit at the exact reviewed
  SHA, verify-merge, default-branch check) - not in this round.

## Decision classification

D0 (S-DECIDE-01): the round executes the FROZEN protocol (PROTOCOL-009,
byte-verified) under the owner's attributable E2(b) authorization
(private receipt; the D2 target-deployment boundary was the owner's
decision, not strategy's, and is recorded as a product-intent change
per the committed decision package); every mechanical choice (intake
spec, ID assignment, PRNG draw order, pilot/split arithmetic, fail-closed
BLOCKED rules) is the unique deterministic transcription of the frozen
preregistration - no judgment debt, no CRIT admission (S-DECIDE-03
condition 1 fails: the frozen protocol, the 009-a order, the decision
package, and the verified source census leave no unresolved choice).
The single named human input (the intake corpus) is a pre-specified
external dependency with the pre-authorized BLOCKED-once escalation path
(owner standing instruction: escalate only genuine human/D2 decisions;
the owner is not a terminal relay). Renumbering (recorded): the pre-
draft's artifact names (DEPLOYMENT-IDENTITY-010.md, ANNOTATION-GUIDE-
010.md) are renumbered -011 in this order (objective-011 artifacts), and
the draft's expected PR number is confirmed as #12 (verified, not
invented).

## Deferred human adjudication

- Decision: NONE

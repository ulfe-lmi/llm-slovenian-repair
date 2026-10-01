# 011-e: Stage-1 collection recovery for the development-distribution re-measurement on the designated A100-FP8 target (objective 011, round 5; continuation of the 011-d BLOCKED collection purpose under S-RECOVER-01; SCAFFOLD_GENERATION call class amended per PROTOCOL-009-REVISION-012 (output cap 8,192, reasoning effort pinned low); selection/partition/IDs unchanged; no re-sampling; PR #12 held open)

Status: FINAL.

## Continuity and adaptation note (011-d -> 011-e; bounded, recorded)

1. 011-d (round 4) completed as Result: BLOCKED at its pre-declared
   scope-item-3d floor-50 gate: 134/134 selected documents excluded
   by failed terminal scaffold attempts (8 x HTTP 200 incomplete at
   reasoning_tokens 600 = the full registered 600-token cap, zero
   message output, under server-default xhigh and effort low; 127 x
   HTTP 400 with the verbatim server message 'Unexpected reasoning
   effort minimal. Supported types are xhigh (default), medium, and
   low.'), zero main-capture calls, zero samples opened. Strategy's
   independent final-head review of 011-d is PASS on a COMPLETE,
   protocol-conformant round (private
   workorders/011-d-final-head-review-20261002.md).
2. S-RECOVER-01: a completed BLOCKED round is not replayed; its
   unfinished purpose (the stage-1 collection) continues under the
   next suffix - THIS round - on the same branch and PR.
3. The 011-d single-new-question (amendment of the registered
   SCAFFOLD_GENERATION call class) is resolved by strategy as a D0
   routine reversible choice within the risk budget (S-DECIDE-01;
   no CRIT admission - S-DECIDE-03 condition 3 fails): the
   registered additive revision PROTOCOL-009-REVISION-012
   (Scope item 2, byte-exact) amends ONLY the REVISION-011 section-
   8 call-contract parameters (output-token cap 600 -> 8,192;
   reasoning-effort pin "low"; per-round budget) and adds the
   stage-1 recovery clause. Not a method change: scaffold sections
   are discarded before scoring, no frozen method element is
   touched, and no calibration/confirmation content was opened at
   011-d - PROTOCOL-009 (n) is NOT triggered.
4. The committed selection, draws, per-document assembly draws,
   collection IDs, and partition of the 011-d-committed manifest
   STAND unchanged (REVISION-012 section 3). NO re-selection, NO
   re-draw, NO replacement, NO renumbering. The 134 exclusions of
   011-d are terminal for that round's attempts; the recovery
   regenerates the SAME 134 documents with fresh scaffold calls.
5. Driver constraint recorded from the 011-d review: the 011-d
   driver probed "minimal" (HTTP 400 on the standalone diagnostic)
   and nonetheless used it for the remaining 126 documents' single
   terminal attempts. This round FORBIDS any reasoning-effort value
   other than the pinned "low" and forbids omitting the field
   (REVISION-012 section 2); a call carrying any other value is a
   driver defect named in the report, and the attempt still counts
   as that document's single terminal attempt.
6. Suffix remap (recorded): the evaluation round drafted as 011-e
   becomes 011-f; the stage-2 expansion (if triggered by the pre-
   registered criteria (i)-(iii)) becomes 011-g. The labeler
   specification (private workorders/draft-011f-labeler-
   spec-20261001.md, sha256 efe6d24f8d504cfd9f9f21b06d9e1b17a7a770d3ac9bdf2b265bc5086dff6ca5)
   is updated to the mechanical-assembly model. The second named
   human input (labelers) surfaces exactly once at THIS round's
   completion boundary, with the packets in place (the 011-d
   boundary produced zero packets; the surface condition is
   "packets exist"), recorded in this round's publication receipt.
7. Artifact names and the collection-ID scheme are RETAINED exactly
   as pre-registered in the 011-b order and executed at 011-d
   (`011b-<seq:04d>` collection IDs, `011b-collection-manifest.json`,
   private `011b-collection/`, `011b-packets/`; `011b-intake/` stays
   absent - superseded). The private 011-d round state (progress
   ledger, assembly summary, 8 stored incomplete raw responses) is
   preserved immutable; this round appends round-tagged records and
   writes new raw responses under an attempt-tagged name.

## Metadata

```oap-metadata
{
  "id": "011-e",
  "title": "Stage-1 collection recovery for the development-distribution re-measurement on the designated A100-FP8 target (objective 011, round 5; 011-d BLOCKED continuation per S-RECOVER-01; SCAFFOLD_GENERATION class amended per PROTOCOL-009-REVISION-012; selection/partition/IDs unchanged; PR #12 held open)",
  "objective": "011",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "79eefe84adde9dda150949c61f527e94bc0638e8",
  "branch": "oap/011-target-distribution-confirmation-study",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 12,
  "dependencies": ["007", "008", "009", "010", "011"],
  "local_work": "Preserve byte-for-byte: the entire objective-000..011-d tree at base 79eefe84adde9dda150949c61f527e94bc0638e8, including research/target-distribution/PROTOCOL-009.md (sha256 cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a, FROZEN - the single source of truth; every scientific element below transcribes it, none reopens it), research/target-distribution/PROTOCOL-009-REVISION-011.md (sha256 609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43, 19,049 B, byte-frozen by this round - REVISION-012 amends only its named section-8 parameters), research/target-distribution/SCAFFOLD-GENERATOR-PROMPT-011.md (sha256 005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc, 402 B, byte-frozen), research/target-distribution/DEPLOYMENT-IDENTITY-009.md (sha256 b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4, FROZEN), research/target-distribution/DEPLOYMENT-IDENTITY-011.md (sha256 53cefe8fe451402eff3ffd429083eb87d1fe80733c66b641a05bba20b482e94a; sections 1-6 byte-preserved - this round writes NO identity bytes and reads section 6 as its hard-gate precondition), research/target-distribution/ANNOTATION-GUIDE-011.md (sha256 e2acabdda674c2e588cdc14e4a52e7af19f2c7f969ec31a2ebab69356759f94e, 16,818 B, byte-frozen - the operative labeler reference), research/target-distribution/011b-collection-manifest.json (sha256 456d0529a1d61660a411adc1847d5c36278df4fd5e8dfd9957280c175e05dd90 at the base; the ONE released exception: extended and finalized by this round per Scope 7, all base bytes preserved as the committed prefix of the extension semantics), research/tests/test_009a_protocol_elements.py, all 007-m frozen surfaces (config projection 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, deployment profiles c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), the objective-011-a/011-b/011-c/011-d artifacts (oap/orders/011-b-confirmation-stage1-collection.md sha256 0456004c0136ec0de9e3732b3d76ddd343d9124730a865fa7e946182a3105627, oap/orders/011-c-identity-reverification-canonical-routes.md sha256 676279b6d3584dc42a3d4a28a8b06eaf317ae929e20127c00e7768899a99a2c7, oap/orders/011-d-confirmation-stage1-collection.md sha256 f60392f0739717afc596c7be25590167bea8df75d33e2383ff54ba32e957527d, and all four orders' reports byte-identical to the base blobs; RESEARCH-STATE sections 25-28; the 011-a..011-d ledger entries; machine block at main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8 with counters registry_entries 40 / oap_reports_reviewed 59 / frozen_report_history_incidents 2), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, the private research-runtime roots (009a-identity/, 011b-identity/ including the STRATEGY-CORRECTED credentials receipt, 011c-identity/ - all read-only for this round; 011b-collection/ read-only for its 011-d records and released for appended 011-e records per Scope 4; 011b-packets/ as released in Scope 8; 011b-intake/ stays absent), and the private DASSLE source copy (private research-runtime campaign8 datasets location; READ-ONLY for this round; byte-verified per Scope 1), and any unrelated local work (the three untracked residues corpus/, .research-test-scratch/, .rclone-speed-test/ are pre-existing and never committed). This round writes ONLY: research/target-distribution/PROTOCOL-009-REVISION-012.md (new; registered byte-exact in Scope 2), the manifest extension (Scope 7), and the bookkeeping paths of Scope 9.",
  "prior_review": "Strategy independent final-head review of 011-d (2026-10-02, private workorders/011-d-final-head-review-20261002.md): verdict PASS on a COMPLETE round (Result BLOCKED at the pre-declared scope-item-3d floor-50 gate - a truthful stop, not a defect). Independently verified: verify-report remote at the 011-d final head 79eefe84adde9dda150949c61f527e94bc0638e8 (report history valid, 60 report files, only the two known frozen 006-a/006-c incidents); report-only commit 79eefe8 with implementation head 60f31de48b7ebb803527babf6f91a84406ae7a78 as sole parent and the report as sole changed path; round diff (47c4da8..79eefe8) exactly the twelve released paths; committed artifacts independently re-hashed - PROTOCOL-009-REVISION-011.md 609751c1..., SCAFFOLD-GENERATOR-PROMPT-011.md 005edf0a..., ANNOTATION-GUIDE-011.md e2acabdd..., manifest 456d0529... (data-free, PENDING_GENERATION); commit chain d740bbb/03580ce/c8224d8/b94262d/60f31de/79eefe8 sole-parent verified; all four required checks genuinely green at the final head at job level (Application baseline; OAP report history; Research reproducibility; OAP bootstrap acceptance); registry 40 with exactly one new 011-d data-free entry (kind collection, status BLOCKED); machine-block counters 40/59/2 with identity fields byte-unchanged; CRITICAL.md byte-identical at the true seed hash; the private 011b-collection ledger, assembly summary, and 8 stored incomplete raw responses inspected (usage output_tokens 600 = reasoning_tokens 600, no message content; the verbatim 400 message names the supported efforts xhigh/medium/low); E2(b) boundary honored (135 authorized scaffold-class calls + 2 disclosed transport diagnostics, zero metadata probes). The round's single-new-question (the SCAFFOLD_GENERATION class amendment) is resolved by strategy as D0 per S-DECIDE-01 (no CRIT admission; REVISION-012 registered; the strongest counterargument - the 126 terminal attempts on the known-invalid effort minimal - is recorded as a driver-behavior finding and converted into the Scope-4 driver constraint of this order).",
  "provenance": [
    {"kind": "H", "reference": "Owner objective-009 start instruction 2026-09-30 (continue the loop into data collection/annotation/evaluation under proof-sized suffixes without the owner as terminal relay; escalate only genuine human/D2 decisions; the ~99 percent and <=1 per 10,000 numbers are evaluation/calibration targets, not release authorization); the owner's verbatim E2(b) decision 2026-09-30 '(b) Designate A100-FP8 as the confirmation target' (private receipt workorders/e2b-decision-receipt-20261001.md); the standing A1 instruction (all four required checks genuinely green; reds never reinterpreted); the owner's out-of-band endpoint/bearer provisioning (controlled storage only; unchanged by this round); the owner's 2026-10-01 DASSLE directive (THREE VERBATIM MESSAGES recorded in the 011-d order's H field and the private decision receipt workorders/dassle-reuse-decision-20261001.md) - still in force, superseding nothing in this round; no NEW human input is requested by this round: the 011-d single-new-question is resolved by strategy's D0 decision recorded in the 011-d final-head review and embodied in PROTOCOL-009-REVISION-012."},
    {"kind": "A", "reference": "research/target-distribution/PROTOCOL-009.md (FROZEN, cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a) elements (a)-(n) and section 4 as amended by PROTOCOL-009-REVISION-011 (FROZEN at 609751c1...) and NOW further amended ONLY in its section-8 call-contract parameters by PROTOCOL-009-REVISION-012 (registered byte-exact in Scope 2, sha256 cbbb7b58739d2124a9d1834dbd0e1a1d42d816ab3af215d877c6c23798acc809, 7,684 B; additive; the named supersession map: the 600-token output cap, the absent effort pin, and the budget clause of REVISION-011 section 8; the stage-1 recovery clause); element (a) freshness precondition satisfied BY RECORD via DEPLOYMENT-IDENTITY-011.md section 6 (REGIME-UNCHANGED, observation window 2026-10-01T00:58:35.948Z-00:58:36.253Z) - NO probe in this round (the exactly-2-GET metadata budget remains exhausted by 011-b/011-c); the frozen 007-m profile contract (config 0026a1a9..., prompt 572cf2fb..., deployment profiles c79fd658.../0c4aa490...) as the exact main-capture contract for the survivors; the registered scaffold prompt (005edf0a..., 402 B) and 12-topic list (REVISION-011 section 8, unchanged); oap/orders/011-d-confirmation-stage1-collection.md (sha256 f60392f0739717afc596c7be25590167bea8df75d33e2383ff54ba32e957527d) - the pre-registered stage-1 collection specification whose BLOCKED scope-item-3d gate and floor-50 rule this round re-executes over the regenerated documents; S-RECOVER-01 (a completed BLOCKED round is not replayed; its unfinished purpose continues under the next suffix after the intervening work it required); S-ORDER-03 (continuation suffixes preserve branch and PR while that PR is open); S-DECIDE-01 (the D0 class decision recorded in the 011-d final-head review); S-PRODUCT-02 (fresh isolated requests; EXACT/CENSORED/UNAVAILABLE; denominator semantics); S-PRODUCT-04 (protected Qwen/services; explicit rights for evaluation data; no credentials in artifacts); LR-001 (complete main capture precedes review), LR-013 (data-free public artifacts), LR-014 (bounded one-pass review)."},
    {"kind": "E", "reference": "Observed 2026-10-02 ~09:0x-09:4x CEST (this session, from remote and primary records): remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 = OAP_ACCEPTED_REF (gh api re-verification at publication time, recorded in the publication receipt); worktree on branch oap/011-target-distribution-confirmation-study at the 011-d final head 79eefe84adde9dda150949c61f527e94bc0638e8 (activation d740bbb96182467d6584048e79a233af0c1545d0, registered files 03580ce6445aa2a43146a77b9b18e5f5eb1cebd1, manifest c8224d8cbd02ebb753bfd088c396ed38d7658f13, guide b94262dc80723e38213ee2e198ec7c0616b91d97, implementation head 60f31de48b7ebb803527babf6f91a84406ae7a78, report-only 79eefe84adde9dda150949c61f527e94bc0638e8); PR #12 OPEN and MERGEABLE at that head, base main, autoMergeRequest null, the only open PR, all four required checks success at that head (job level); oap/active = 011-d consumed (the 011-d response OK frame observed by the strategic watcher at 2026-10-01 11:44:39 CEST, log workorders/response-011d-watch.log); OAP state: INACTIVE pending this publication; CRITICAL.md seed-identical a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e, zero entries; machine block on the branch: main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8, parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, identity fields unchanged, counters 40/59/2; registry = 40 entries (last 011-d, kind collection, status BLOCKED); local consistency 10/10 at the 011-d final head (strategy re-run); the 011-d BLOCKED census (committed manifest + report + private ledger, re-verified this session): G = 100 selected genuine, C = 34 selected controls (134 documents; pilot 5 / calibration 20 / confirmation 109; collection IDs 011b-0001..011b-0134; per-document k and topics committed), 135 scaffold-class calls consumed (134 terminal attempts + 1 standalone diagnostic; budget 135/402 under REVISION-011), 134/134 excluded (SCAFFOLD_FAIL_s1 per document, no replacement, no re-sampling), 0 survivors, 0 main-capture calls, 0 samples opened, 011b-packets/ absent, 011b-intake/ absent; the structural finding (data-free): on the designated deployment the reasoning overhead on the scaffold task exceeds the registered 600-token output cap at every supported effort - 8/8 HTTP 200 attempts at reasoning_tokens 600/600 with zero message content (xhigh default 2, low 6; 8 raw responses stored verbatim privately, 0600), 127 x HTTP 400 for the probed effort minimal with the verbatim server message naming the supported set xhigh (default) / medium / low; the frozen 007-m corroboration (1,901 stored completed responses at effort low, reasoning 16-4,417 tokens, no output cap); the private credentials receipt (011b-identity, 0600, strategy-corrected dual bases + bearer) is the sole profile source for all calls; the DASSLE source census unchanged (dassle.jsonl 7,385 records sha256 609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6, eligible genuine 7,354; dassle-preservation.jsonl 7,381 records sha256 d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec; both byte-re-verified at 011-d and re-verified in this round's pre-work); the intake boundary remains CLOSED by the owner's 2026-10-01 directive (no re-escalation)."},
    {"kind": "I", "reference": "Strategy 011-d final-head review PASS (private workorders/011-d-final-head-review-20261002.md) including the private 011b-collection inspection and the D0 decision record for the SCAFFOLD_GENERATION class amendment (the strongest counterargument and its disposition: the 126 terminal attempts on the known-invalid effort minimal are a driver-behavior finding, terminal by registration, converted into the Scope-4 driver constraint); the 011-d publication receipt (private, signal discipline, FUSE stale-stat workaround); the updated labeler specification (private workorders/draft-011f-labeler-spec-20261001.md, mechanical-assembly model, staged deliveries, verify/adjudicate tasking, scaffold OUT_OF_SCOPE); the technical-debt register (TD-1/2/3 non-gating, incl. the subprocess-tree timeout debt recorded at 008-i); the 011-a..011-d publication receipts (signal discipline, FUSE workarounds)."}
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

Objective 011, round 5, on the EXISTING branch
`oap/011-target-distribution-confirmation-study` (AMEND_EXISTING_PR -
PR #12, verified OPEN at head 79eefe84adde9dda150949c61f527e94bc0638e8,
the 011-d final head, base main at
`4507cc78e333c0e48226b64266121171b7b8cea8`). The objective's PR stays
open across its suffix rounds and merges only at the objective's end
(the PR #9 / PR #10 / 011-a..d pattern). This is the **stage-1
COLLECTION RECOVERY round of the development-distribution
re-measurement** on the E2(b)-designated A100-FP8 regime: it re-
executes the 011-d stage-1 collection purpose (S-RECOVER-01) over
the SAME committed selection under the amended SCAFFOLD_GENERATION
call class (PROTOCOL-009-REVISION-012: output cap 8,192, reasoning
effort pinned low, per-round budget 402 + 1 diagnostic), with the
floor-50 gate re-applied verbatim and - on success - the main-capture
completion branch of the 011-d specification that 011-d never
reached.

## Provenance

The H/A/E/I provenance above. No element of this order is bare:
every requirement traces to the frozen protocol as amended, the
published 011-b/011-d specifications, the 011-c identity verdict,
the 011-d review and census, or the owner's standing instructions.

## Current verified state

Verified 2026-10-02 (this session, pre-publication; re-verified at
publication time and recorded in the publication receipt):

- main = 4507cc78e333c0e48226b64266121171b7b8cea8 = OAP_ACCEPTED_REF
  (unchanged; remote re-verified at publication).
- Worktree on the 011 branch at the 011-d final head 79eefe8
  (sole-parent chain d740bbb -> 03580ce -> c8224d8 -> b94262d ->
  60f31de -> 79eefe8 verified); PR #12 OPEN/MERGEABLE at that head,
  base main, autoMergeRequest null, only open PR; all four required
  checks success at that head (job level).
- oap/active = 011-d (consumed; the 011-d response OK frame observed
  2026-10-01 11:44:39 CEST).
- OAP state INACTIVE; CRITICAL.md seed-identical (true hash
  a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e),
  zero entries; machine block counters 40/59/2, identity fields
  unchanged; registry 40 (last 011-d, kind collection, status
  BLOCKED).
- 011-d review PASS (private); the 011-b/011-c identity records
  byte-verified at the base (section 6 REGIME-UNCHANGED).
- The 011-d BLOCKED census re-verified: 134 selected documents
  (100 genuine 011b-0035..011b-0134, 34 controls 011b-0001..
  011b-0034), partition pilot 5 (011b-0079, 011b-0114, 011b-0067,
  011b-0072, 011b-0097) / calibration 20 / confirmation 109, 134/134
  excluded, 0 survivors, 0 main-capture calls, 0 samples opened.
- The private 011b-collection/ 011-d state (progress ledger,
  assembly summary, 8 stored incomplete raw responses) inspected and
  confirmed intact; 011b-packets/ absent; 011b-intake/ absent.

## Governance

The sixteen source identities in the metadata governance mapping are
the exact identities of `oap/governance/MANIFEST.json` at the
accepted base `4507cc78e333c0e48226b64266121171b7b8cea8`, unchanged
(16/16). No governance change occurs in this objective. The private
research-runtime root layout (011b-collection/ - 011-d records
immutable, 011-e records appended per Scope 4; 011b-packets/ per
Scope 8; 011b-intake/ stays absent - superseded) follows the
established convention (0700 directories, 0600 files); none of it
is ever committed.

## Goal and dependencies

Goal: complete the stage-1 collection of the development-
distribution re-measurement on the designated target - regenerate
the SAME 134 committed documents under the amended SCAFFOLD_
GENERATION class, re-apply the floor-50 gate, and - on success -
execute the frozen 007-m main-capture contract over every surviving
document, extend and finalize the committed manifest, and prepare
the annotation guide packets - all committed data-free - so that the
011-f evaluation round can open the confirmation subset for final
scoring. A pass is the collection of record; it is NOT release
authorization and enables no milestone claim (the study remains a
re-measurement on a reused, fully-disclosed population).

Dependencies: 011-d (reviewed PASS; the committed manifest, guide,
revision-011, prompt, census), the amended class per PROTOCOL-009-
REVISION-012 (Scope 2), the designated target identity (re-verified
at 011-c by record; byte-verified in this round's pre-work; NO
probe in this round), and the frozen surfaces preserved by
local_work. The two labelers are a 011-f input, not a 011-e input
(this round prepares the packets; the second named human input
surfaces exactly once at this round's completion boundary, recorded
in the publication receipt). CORPUS_ONLY: disabled (011-f scope).

## Scope

1. Pre-work integrity gates (data-free): at the base 79eefe84adde9dda150949c61f527e94bc0638e8,
   byte-verify every frozen surface and the objective-009..011-d
   artifacts pinned in local_work (PROTOCOL-009.md, PROTOCOL-009-
   REVISION-011.md, SCAFFOLD-GENERATOR-PROMPT-011.md, DEPLOYMENT-
   IDENTITY-009.md, DEPLOYMENT-IDENTITY-011.md sections 1-6,
   ANNOTATION-GUIDE-011.md, 011b-collection-manifest.json at the
   base sha256 456d0529a1d61660a411adc1847d5c36278df4fd5e8dfd9957280c175e05dd90,
   test_009a_protocol_elements.py, the 007-m pins, the 008
   protection-layer pins, the 011-a..011-d orders and reports,
   RESEARCH-STATE sections 24-28, CRITICAL.md seed-identical at the
   true hash); machine block on the branch: main_sha/reviewed
   4507cc78e333c0e48226b64266121171b7b8cea8, parent
   01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 40/59/2,
   identity fields unchanged; registry 40 (last 011-d, kind
   collection, status BLOCKED); local consistency 10/10 in a real
   checkout with origin/main =
   4507cc78e333c0e48226b64266121171b7b8cea8; the DASSLE source gate:
   both files byte-re-verified (sha256
   609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6
   and d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec;
   census unchanged). Any mismatch is BLOCKED with the mismatch
   named; no work proceeds. NO metadata probe of any kind (the
   exactly-2-GET budget remains exhausted; hard-gate (a) is
   satisfied BY RECORD via DEPLOYMENT-IDENTITY-011.md section 6,
   byte-verified here).
2. Commit `research/target-distribution/PROTOCOL-009-
   REVISION-012.md` (new; registered byte-exact below; additive -
   PROTOCOL-009.md and PROTOCOL-009-REVISION-011.md stay byte-
   frozen; sha256 cbbb7b58739d2124a9d1834dbd0e1a1d42d816ab3af215d877c6c23798acc809,
   7,684 B) BEFORE any sample is regenerated or any scaffold call
   is made. The committed bytes are exactly the fence interior
   below, including its final newline.
3. Reproducibility assertion (deterministic, BEFORE the first live
   call): re-derive the per-document assembly draws (k, topics,
   layout, block order, discard-map block offsets) for all 134
   collection IDs from the committed manifest's assembly mechanics
   (the registered PRNG instances and seeds); assert byte-identity
   against the 011-d private per-document ledger (collection ID,
   record ID, arm, k, topics, layout) for all 134 documents. Any
   mismatch is BLOCKED with the mismatch named (this round must
   regenerate the SAME documents; it may not drift).
4. Scaffold generation (the live work; the amended class per
   PROTOCOL-009-REVISION-012 section 2): for each of the 134
   documents in committed ID order, generate its k scaffold sections
   (k from the committed per-document draw; 1 <= k <= 3): one fresh
   isolated request per section on the designated target ONLY;
   Responses wire API, non-streaming; the registered 402-B prompt
   with the committed topic for that section; the reasoning effort
   field pinned to "low" (the ONLY permitted value; omitting the
   field or sending any other value - including xhigh, medium, or
   minimal - is a driver defect named in the report, and the call
   still counts as that section's single terminal attempt); output-
   token cap 8,192; 300 s timeout; 2,000,000-byte response bound;
   ONE terminal attempt per section; NO resampling, NO retry;
   profile read ONLY from the private 011b-identity credentials
   receipt. Response handling per the registered class: store
   verbatim privately in 011b-collection/scaffold/ under an
   attempt-tagged name (011b-<id>-s<n>-r2-raw.json; the 011-d files
   stay immutable); strip exactly one trailing LF; strip exactly one
   outer code-fence pair iff the first and last lines are exactly
   three backticks with nothing outside; otherwise as received.
   Failure or empty processed section: the document is EXCLUDED,
   the failure named per document (SCAFFOLD_FAIL_s<n>), no
   replacement, no re-sampling, counted operationally. Budget: at
   most 402 terminal scaffold attempts + 1 standalone diagnostic;
   every call recorded (numbers only: HTTP status, wall time,
   tokens, capture size, state) in the manifest extension and the
   round-tagged ledger records. At most one standalone diagnostic
   call is permitted (for a transport-level fault only, named in
   the report).
5. Floor-50 gate (the 011-d scope-item-3d rule, verbatim): after
   assembly, genuine-arm survivors < 50 -> Result: BLOCKED on the
   named shortfall (no main-capture call, no packet finalization,
   no manifest finalization, truthful report, exact OK). The
   completion branch below is reached ONLY with >= 50 genuine-arm
   survivors.
6. Main capture (completion branch): for every SURVIVING document
   (genuine + control), exactly one main-capture call under the
   frozen 007-m profile contract (byte-identical wire; the
   assembled document as input; EXACT/CENSORED/UNAVAILABLE
   semantics recorded per document; stored verbatim privately in
   011b-collection/main/ (0600); never committed). NO other live
   call of any kind occurs in this round.
7. Manifest extension and finalization (data-free): extend the
   committed 011b-collection-manifest.json (all base bytes and
   fields preserved; per-document PENDING_GENERATION fields
   completed with the round's data-free call metadata: HTTP
   status, wall time, tokens, capture size, state, per-call
   EXACT/CENSORED/UNAVAILABLE) and finalize it: survivor list,
   exclusion census (per-document names), regenerated discard maps
   (block offsets; scaffold regions OUT_OF_SCOPE), assembly census,
   partition unchanged, identity reference unchanged, round =
   011-e. The manifest remains the single collection of record.
8. Annotation guide and labeler packets (preparation only; the
   labelers are a 011-f input): ANNOTATION-GUIDE-011.md stays byte-
   frozen (already committed at 011-d; NOT re-written). Prepare
   the labeler work queues under the private 011b-packets/
   directory (0700/0600; NEVER committed): the 5 pilot packets,
   each containing the assembled input document, the collected main
   answer, the DISCARD MAP (block offsets; scaffold regions marked
   OUT_OF_SCOPE), the DASSLE reference for the scored span, and the
   frozen CPU detector's span output on that main answer (frozen
   detector, no intervention, no review call, no accepted edit, no
   scoring in this round); the per-span/per-document queue
   structure for the calibration and confirmation subsets (IDs and
   hashes only until 011-f opens them, applying the span-
   correspondence matcher first). Data-free aggregates (packet
   counts, file hashes) are committed with the manifest; no raw
   text is committed. The second named human input (the two
   labelers per the updated private labeler specification) surfaces
   exactly once at this round's completion boundary (packets in
   place), recorded in this round's publication receipt.
9. Bookkeeping (data-free): (a) exactly one 011-e entry appended to
   `research/registry/experiments.json` (registry 40 -> 41; data-
   free; kind collection; status per the round outcome COMPLETE or
   BLOCKED; counts and partition sizes only; private locations
   referenced by relative directory names only); (b) machine-block
   counters registry_entries 40 -> 41 and oap_reports_reviewed
   59 -> 60 (the 011-e report file), frozen_report_history_
   incidents unchanged at 2; all identity fields UNCHANGED (no
   advance - that is a post-merge round's job); (c) STATUS.md round
   sentence; (d) `oap/GENERATED-FILES.json` scoped pin (same scope
   pattern as the prior rounds, extended with this round's
   artifacts); (e) `research/tables/experiment-summary.csv`
   rebuild; (f) `research/RESEARCH-STATE.md` additive section 29
   (the 011-e collection-recovery record: the D0 decision record
   for the SCAFFOLD_GENERATION class amendment (REVISION-012 sha,
   the 011-d finding, the no-CRIT rationale), the reproducibility
   assertion result, the per-call census data-free (scaffold + main
   capture), the survivor/exclusion census, the driver-behavior
   finding disposition (the Scope-4 constraint), the stage-1
   population of record (G/C/partition sizes, per-call states),
   private locations by relative name; NO rewrite of sections
   1-28 or the machine block except item 9b).
10. Report-only final commit: sole parent = the literal
    implementation head; sole changed path
    `oap/reports/011-e-confirmation-stage1-collection-recovery.md`;
    the report discloses the final-head check state verbatim and, in
    the BLOCKED branches, the exact gate and named input with zero
    samples opened.
11. Final-head CI: all four required checks green at the final head
    (or the predeclared re-run state disclosed verbatim at report
    time, resolved before strategy's final-head review).
12. Push and verify; send the exact response OK and stop. PR #12
    stays OPEN; no merge; no auto-merge.

### 2a. Registered bytes: PROTOCOL-009-REVISION-012 (Scope 2)

The committed bytes of `research/target-distribution/PROTOCOL-009-
REVISION-012.md` are exactly the fence interior below (including its
final newline); sha256 cbbb7b58739d2124a9d1834dbd0e1a1d42d816ab3af215d877c6c23798acc809;
7,684 bytes.

````
# PROTOCOL-009 REVISION 012 (additive) - amendment of the registered
# SCAFFOLD_GENERATION call class; stage-1 recovery clause - 2026-10-02

Status: REGISTERED. Committed byte-exact by order 011-e BEFORE any
live call. Additive: PROTOCOL-009.md remains byte-frozen (sha256
cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a);
PROTOCOL-009-REVISION-011 (sha256
609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43,
19,049 B) remains byte-frozen; this revision supersedes ONLY the
named call-contract parameters of its section 8 and nothing else:
(i) the "output-token cap 600" clause of the call contract; (ii) the
absence of a reasoning-effort pin (the REVISION-011 payload left the
effort to the server default, then the 011-d driver probed values);
(iii) the budget clause (re-registered per round, below). Every
other element of PROTOCOL-009 and of REVISION-011 (population,
mechanical assembly, PRNG mechanics, selection, partition, ground-
truth rule, span-correspondence matcher, discard rule, score
scoping, labeler tasking, comparators, metric families, stopping
rules, (m) failure decomposition, (n) no-tuning, data rights) is
UNCHANGED.

## 1. Recorded finding (evidence for the amendment)

011-d (first collection round) BLOCKED truthfully at the pre-
declared floor-50 gate: 134/134 selected documents excluded by
failed terminal scaffold attempts (135 calls: 134 terminal attempts,
one per document, plus 1 standalone diagnostic; budget 135/402).
- 8 x HTTP 200 incomplete (documents 011b-0001..0008): under server-
  default effort xhigh (2) and effort low (6),
  incomplete_details.reason = max_output_tokens with
  usage.output_tokens = 600 = the full registered cap, of which
  output_tokens_details.reasoning_tokens = 600 - the entire cap was
  consumed by reasoning with zero message content. The 8 raw
  responses are stored verbatim privately (0600), never committed.
- 127 x HTTP 400 (documents 011b-0009..0134 + the diagnostic): the
  probed effort "minimal" is rejected; the server's verbatim
  message: 'Unexpected reasoning effort minimal. Supported types
  are xhigh (default), medium, and low.'
Finding: on this deployment (vLLM 0.28.0; qwen3.8-27b;
Qwen3.8-27B-FP8; the E2(b)-designated A100-FP8 regime as verified at
011-c) the model's reasoning overhead on the registered scaffold
task exceeds 600 output tokens at every supported reasoning effort
(supported set: xhigh / medium / low; minimal UNSUPPORTED), so the
registered 600-token output cap structurally prevented scaffold-
section completion. Corroboration: the frozen 007-m evidence base
holds 1,901 stored completed responses at effort low with reasoning
of 16-4,417 tokens under no output cap.

## 2. Superseded element: section-8 call-contract parameters

- Output-token cap: 600 -> 8,192. Rationale (data-free): 8,192
  bounds (a) the registered scaffold message budget (150-250 words
  ~ <= 500 message tokens) plus (b) the observed low-effort
  reasoning maximum of 4,417 tokens in the frozen 007-m corpus
  (1.85x margin), plus the 600 observed on this task class before
  truncation. The cap is a ceiling, not a target.
- Reasoning-effort pin: the scaffold payload carries the reasoning
  effort field pinned to "low" - the same field value as the frozen
  007-m main-capture contract (configuration pin
  0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26).
  "low" is supported (measured HTTP 200 in 011-d) and is the
  frozen-method effort. "xhigh" (server default) and "medium" are
  supported but MUST NOT be used for scaffold calls; "minimal" is
  UNSUPPORTED (HTTP 400; verbatim message in section 1) and MUST
  NEVER be sent. Sending any effort value other than "low" (or
  omitting the field) is a driver defect, not a registered variant.
- UNCHANGED within the call contract: one fresh isolated request
  per section on the designated target only; Responses wire API,
  non-streaming; NO main history, NO session linkage, NO tools, NO
  images, NO constitutional-adapter recursion (S-PRODUCT-02);
  profile (both bases + bearer) read ONLY from the private
  011b-identity credentials receipt (the sole profile source; never
  committed, logged, or echoed); 300 s timeout; 2,000,000-byte
  response bound; ONE terminal attempt; NO resampling, NO retry;
  response handling (store verbatim privately, 0700/0600, never
  committed; strip exactly one trailing LF; strip exactly one outer
  code-fence pair iff the first and last lines are exactly three
  backticks with nothing outside; otherwise as received; failure or
  empty processed section -> document EXCLUDED, failure named, no
  replacement, no re-sampling, counted operationally); the
  registered prompt (byte-exact, 402 B,
  005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc)
  and the registered 12-topic list.
- Budget (re-registered per round): each collection round that
  issues scaffold calls carries an explicit per-round cap. The 011-
  e recovery round's cap: at most 402 terminal scaffold attempts
  (134 documents x up to 3 sections per the committed per-document
  k) plus 1 standalone diagnostic. The 135 calls consumed at 011-d
  are accounted under the REVISION-011 cap and are NOT charged
  against the 011-e cap.

## 3. Stage-1 recovery clause (order 011-e)

- The committed selection, draws, per-document assembly draws (k,
  topics, layout), collection IDs, and partition (pilot 5 /
  calibration 20 / confirmation 109) from the 011-d-committed
  manifest STAND unchanged. NO re-selection, NO re-draw, NO
  replacement records, NO renumbering. The 134 exclusions of 011-d
  are terminal for that round's attempts.
- The recovery round regenerates the SAME 134 documents: the
  deterministic assembly (registered PRNG instances, seeds, and per-
  document draws committed in the 011-d manifest) reproduces byte-
  identical document structure, layout, and topic assignment; only
  the scaffold section texts are new (fresh generation calls under
  the amended class). The round MUST assert reproducibility against
  the 011-d private per-document ledger (k, topics, layout,
  collection ID, record ID, arm) BEFORE the first live call; any
  mismatch is BLOCKED with the mismatch named.
- The 011-d private round state (progress ledger, assembly
  summary, the 8 stored incomplete raw responses) is preserved
  immutable. The recovery round appends round-tagged (011-e)
  records to the ledger and writes new raw responses under an
  attempt-tagged name; the collection of record remains the single
  committed manifest, extended and finalized in this round.
- The 011-d order's floor-50 gate (its scope item 3d) applies
  verbatim to the recovery round's survivors: genuine-arm survivors
  < 50 -> Result BLOCKED on the named shortfall with zero samples
  opened beyond the failed attempts.

## 4. Scope statement: not a method change

The scaffold sections are discarded before scoring (REVISION-011
sections 5-6: OUT_OF_SCOPE, never labeled, never scored). This
revision changes only an operational generation parameter of the
discarded-scaffold mechanism. It changes no frozen method element
(ranking, detector thresholds, candidate semantics, validator
prompt/parser, main-capture contract reasoning level, acceptance
policy, protection rules) and is informed by no calibration or
confirmation content (zero samples were opened at 011-d; the
confirmation subset is untouched). The no-tuning rule of PROTOCOL-
009 (n) is NOT triggered. The study label (development-
distribution re-measurement), the authorized-reuse disclosure, the
reclassification statement, and all PLAN section 14.2/14.3
comparator and metric requirements are UNCHANGED.
````

## Non-goals

- No evaluation, no scoring, no metric computation on the
  confirmation or calibration subset, no comparator run (ORIGINAL /
  DETECTOR_ONLY / DIRECT_QWEN_PROOFREADING / FROZEN_RESTRICTED_
  METHOD / CORPUS_ONLY all belong to 011-f), no labeler contact in
  this round (the surface is at the completion boundary; the labels
  are 011-f work).
- No re-selection, no re-draw, no replacement records, no
  renumbering, no change to the partition, no consumption of any
  DASSLE record outside the committed 134.
- No metadata probe of any kind (item 1; the bounded-probe budget
  was exhausted by 011-b/011-c by design).
- No behavior change of any frozen element (PROTOCOL-009 (n) no-
  tuning-after-unblinding; the (n) rule is NOT triggered by
  REVISION-012 - its section 4 scope statement records why: the
  scaffold mechanism is discarded, never scored, and no calibration
  or confirmation content was opened at 011-d). No change to the
  frozen 007-m main-capture contract, the detector, the validator,
  the ranking, the acceptance policy, or the protection layer.
- No commit of raw DASSLE text, raw scaffold text, raw main
  answers, endpoint values, credentials, or private absolute paths
  (LR-013; the publication guard scans the full tree).
- No RTX-3090 contact (MUST-NOT-BE-STARTED), no Deployment B
  contact (EXCLUDED_BY_HUMAN_OVERRIDE), no second large GPU model,
  no other endpoint, no streaming, no writes to the target, no
  server mutation (S-PRODUCT-04; E2(b) boundary).
- No merge, no auto-merge (the merge is the objective-end strategic
  act after the 011-f evaluation and the quiescent checkpoint).

## Files and boundaries

Committed (released from freeze):
`research/target-distribution/PROTOCOL-009-REVISION-012.md` (new,
registered byte-exact per Scope 2), `research/target-
distribution/011b-collection-manifest.json` (extension +
finalization per Scope 7; all base bytes preserved),
`research/registry/experiments.json` (Scope 9a),
`research/RESEARCH-STATE.md` (Scope 9f, additive section 29 +
counters), `STATUS.md` (Scope 9c), `oap/GENERATED-
FILES.json` (Scope 9d scoped pin), `research/tables/experiment-
summary.csv` (Scope 9e), `oap/orders/011-e-confirmation-stage1-
collection-recovery.md` (activation), `oap/active` (activation),
`oap/reports/011-e-confirmation-stage1-collection-recovery.md`
(report-only commit).

Private (NEVER committed; relative names only in artifacts):
`011b-collection/` (inputs/ assembled documents, scaffold/ the 011-
d records immutable + the 011-e attempt-tagged raw responses,
main/ the surviving documents' main answers, the round-tagged
progress ledger records, the extended assembly summary - 0700
directories, 0600 files), `011b-packets/` (the prepared packets),
`011b-identity/` (read-only; sole profile source), `009a-
identity/`, `011c-identity/` (read-only references), the DASSLE
source copy (read-only). `011b-intake/` stays absent (superseded).
The three untracked residues (corpus/, .research-test-scratch/,
.rclone-speed-test/) are pre-existing and never committed.

## Requirements

1. Reconcile and byte-verify before any mutation (Scope 1); record
   the verification data-free.
2. Commit PROTOCOL-009-REVISION-012 byte-exact BEFORE any
   regeneration or live call (Scope 2); assert the sha256 against
   the registered value at commit time.
3. Reproduce the 134 assembly draws byte-identically and assert
   against the 011-d ledger BEFORE the first live call (Scope 3).
4. Execute the amended scaffold class exactly (Scope 4): pinned
   effort "low" only, cap 8,192, 300 s, 2,000,000 B, one terminal
   attempt per section, no resampling, no retry, budget 402 + 1
   diagnostic, per-call recording, verbatim private storage.
5. Apply the floor-50 gate verbatim (Scope 5); BLOCK truthfully on
   shortfall with zero samples opened.
6. On >= 50 genuine-arm survivors: execute the frozen 007-m main
   capture once per surviving document (Scope 6); record EXACT/
   CENSORED/UNAVAILABLE per document.
7. Extend and finalize the manifest data-free (Scope 7); no raw
   bytes committed.
8. Prepare the packets per Scope 8 (pilot 5 + queue structure;
   discard map + DASSLE reference in packets; CPU-detector spans;
   no scoring); record the second-named-human-input surface at the
   completion boundary in the publication receipt.
9. Bookkeeping per Scope 9 (registry 41; counters 41/60/2; STATUS;
   pin; CSV; RESEARCH-STATE section 29 additive).
10. Report-only final commit per Scope 10 (sole parent = literal
    implementation head; sole changed path = the report).
11. All four required checks green at the final head (Scope 11).
12. Push, verify, single exact OK, stop (Scope 12); PR #12 OPEN.

## Acceptance criteria

1. The pre-work gate evidence is recorded and every gate passed
   with zero mismatch (or the mismatch named and the round
   BLOCKED before any mutation); the hard-gate (a) precondition
   verified BY RECORD (section 6), zero metadata GETs in this
   round.
2. PROTOCOL-009-REVISION-012.md committed byte-exact (sha256
   cbbb7b58739d2124a9d1834dbd0e1a1d42d816ab3af215d877c6c23798acc809,
   7,684 B) before any regeneration; PROTOCOL-009.md and
   PROTOCOL-009-REVISION-011.md byte-unchanged; the registered
   prompt and topic list byte-unchanged.
3. The reproducibility assertion passed for all 134 documents
   (k, topics, layout, collection ID, record ID, arm byte-identical
   to the 011-d ledger) before the first live call - or the round
   BLOCKED with the mismatch named.
4. Scaffold calls exactly per the amended class: effort pinned
   "low" on every call (any deviation named as a driver defect in
   the report), cap 8,192, one terminal attempt per section, no
   resampling/retry, budget within 402 + 1 diagnostic, every call
   recorded data-free; raw responses stored verbatim privately,
   never committed.
5. The floor-50 gate executed verbatim: either >= 50 genuine-arm
   survivors (completion branch) or Result BLOCKED on the named
   shortfall with zero main-capture calls and zero samples opened
   beyond the failed attempts.
6. On the completion branch: exactly one frozen 007-m main-capture
   call per surviving document; per-document EXACT/CENSORED/
   UNAVAILABLE recorded; the frozen main-capture wire byte-
   identical to the 007-m contract; zero other live calls in the
   round.
7. The manifest extended and finalized data-free (all base bytes
   and fields preserved; survivor list, exclusion census,
   regenerated discard maps, per-call states, partition unchanged);
   the manifest remains the single collection of record.
8. Packets prepared per Scope 8 (pilot 5 complete; queue structure
   for calibration/confirmation; discard map + DASSLE reference +
   CPU-detector spans per packet; data-free aggregates committed);
   011b-packets/ absent from every commit.
9. Bookkeeping complete and consistent (registry 41 with exactly
   one new 011-e data-free entry; counters 41/60/2; identity
   fields byte-unchanged; STATUS.md; scoped pin; CSV rebuild;
   RESEARCH-STATE section 29 additive with sections 1-28
   unaltered except the ordered counters).
10. The report-only commit has the literal implementation head as
    sole parent and the report path as sole changed path; the
    round diff (base..final) is limited to the released-from-
    freeze list (exactly twelve paths including the report); zero
    secret-pattern hits in round-authored added lines; the
    publication guard passes on the full tree.
11. All four required checks green at the final head (or the
    predeclared re-run state disclosed verbatim, resolved before
    strategy review); the designed implementation-head count red
    (60 != 59) clears with the report file present.
12. Push and remote verification recorded; the exact single OK
    frame sent after durable state is valid; PR #12 OPEN at the
    final head; no merge, no auto-merge.

## Verification

- Named entry points: the round's driver entry (the scaffold-class
  generation driver and the frozen 007-m main-capture driver as
  pinned), the consistency suite in a real checkout, the
  publication guard (full tree), verify-report at strategy's
  review.
- Positive proofs: the reproducibility assertion (134/134 byte-
  identical draws); the per-call census with the pinned effort on
  every call; the manifest extension diff (additive, base prefix
  preserved); the packet census (data-free); the four required
  checks green at the final head.
- Negative proofs: the floor-50 gate on a shortfall (BLOCKED
  branch, zero samples opened); a scaffold failure named per
  document with no replacement; any effort deviation named as a
  driver defect; the publication guard over the full tree (no raw
  text, no endpoint values, no credentials, no private paths in
  round-authored bytes); the report-only commit shape (sole
  parent, sole changed path); zero metadata probes (no version or
  models endpoint call in the round's network trace).
- Evidence layers recorded distinctly: software (consistency
  suite, guard), committed artifacts (hashes), live calls (the
  census, data-free), linguistic quality (NOT assessed in this
  round - 011-f).

## Local setup and constraints

- The frozen uv environment; no new dependencies; no GPU on this
  host (the target is the remote designated A100-FP8 deployment; NO
  second large GPU model); no service touches; no protected Qwen
  weight/config/network change (S-PRODUCT-04); REPAIR_ALLOW_LIVE_
  TESTS stays NO; no endpoint value, credential, or private
  absolute path in any committed artifact or log.
- Private roots: 011b-collection/ (011-d records immutable; 011-e
  records appended), 011b-packets/ - 0700 directories, 0600
  files, native private root, never committed; 009a-identity/,
  011b-identity/, 011c-identity/ read-only; the DASSLE source copy
  read-only (Scope 1); 011b-intake/ stays absent (superseded).
- Local: reversible setup inside the authorized workspace only;
  doctor runs with env -u CODEX_HOME -u OAP_ROLE; heavy test temp
  on native /home/ubuntu/.oap-scratch (0700) given the degraded
  FUSE mount (TD-3: cold git walks may hit the 30-s subprocess
  limit; a single retry is deterministic and clean - recorded, not
  worked around); any unresolvable setup failure is BLOCKED and
  reported, not worked around.

## Documentation

- PROTOCOL-009-REVISION-012.md (Scope 2) - the additive registered
  amendment (the amended call-contract parameters, the per-round
  budget, the stage-1 recovery clause, the not-a-method-change
  scope statement).
- 011b-collection-manifest.json (Scope 7) - the extended and
  finalized collection of record (data-free).
- RESEARCH-STATE.md additive section 29 (Scope 9f) - the canonical
  ledger entry for the collection recovery (the D0 decision
  record, the census, the driver-behavior finding disposition),
  plus the machine-block counters (Scope 9b).
- STATUS.md per Scope 9c; the OAP report per the round mechanics
  (data-free by construction: counts, IDs, domain tags, hashes,
  verdict references; no raw text, no endpoint values, no
  credentials; the round's classification recorded: D0 execution
  of the pre-registered collection as amended; no CRIT
  admission).

## Git and report publication

- Branch `oap/011-target-distribution-confirmation-study`
  (EXISTING; verified at 79eefe84adde9dda150949c61f527e94bc0638e8,
  PR #12 OPEN, base main at 4507cc78e333c0e48226b64266121171b7b8cea8).
  This round AMENDS PR #12; no new branch, no new PR, no force-
  push.
- Activation commit (order + oap/active) per the round mechanics
  (including the established FUSE stale-stat pre-staging workaround
  if the environment requires it, recorded in the round report);
  implementation commits per Scope 2-9 (exact split at the
  executor's discretion, all within the released-from-freeze
  list); the report-only commit per Scope 10 (sole parent =
  literal implementation head; sole changed path = the report).
- Push semantics per the OAP communication profile; no push after
  the report-only commit; the exact response OK after remote
  verification; the coding wrapper consumes the 011-e control
  signal exactly once before model launch.
- No merge: PR #12 stays OPEN; no auto-merge; the merge decision is
  a separate post-review strategic act at the objective's end (S-
  MERGE-01; repository-approved method: standard merge commit at
  the exact reviewed SHA, verify-merge, default-branch check) -
  not in this round.

## Decision classification

D0 (S-DECIDE-01): the round executes the pre-registered stage-1
collection specification (011-b, as amended by the owner's
2026-10-01 DASSLE directive and REVISION-011, published at 011-d)
with its SCAFFOLD_GENERATION call class amended per the registered
additive revision PROTOCOL-009-REVISION-012 (Scope 2). The class
amendment is strategy's D0 decision (recorded in the 011-d final-
head review, private): a routine reversible engineering choice
within the risk budget - a registered operational parameter of the
discarded-scaffold mechanism, corrected against observed
deployment behavior, touching no frozen method element, no DHA
axis, and no unblinded content (PROTOCOL-009 (n) NOT triggered;
S-DECIDE-03 condition 3 fails - no CRIT admission). Every other
mechanical choice is the unique transcription of the ordered
procedure (the frozen protocol as amended twice, the published
011-b/011-d specifications, the 011-c verdict record, the owner
directive); no judgment debt beyond the recorded D0 decision; a
BLOCKED-on-shortfall outcome is a truthful stop that hands the
named finding to the human boundary - it is a stop, not a decision.

## Deferred human adjudication

- Decision: NONE

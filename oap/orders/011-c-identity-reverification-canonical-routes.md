# 011-c: Bounded canonical-route identity re-verification of the designated A100-FP8 target (objective 011, round 3; intervening pinning round required by the 011-b scope-2c stop; no collection, no intake, no generation calls; PR #12 held open)

Status: FINAL

```oap-metadata
{
  "id": "011-c",
  "title": "Bounded canonical-route identity re-verification of the designated A100-FP8 target (objective 011, round 3; intervening pinning round required by the 011-b scope-2c stop; no collection, no intake, no generation calls; PR #12 held open)",
  "objective": "011",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "f505492daa2fa396015739999677bc593c07dc0f",
  "branch": "oap/011-target-distribution-confirmation-study",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 12,
  "dependencies": ["007", "008", "009", "010", "011"],
  "local_work": "Preserve byte-for-byte: the entire objective-000..011-b tree at base f505492daa2fa39601573999677bc593c07dc0f, including research/target-distribution/PROTOCOL-009.md (sha256 cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a, FROZEN), research/target-distribution/DEPLOYMENT-IDENTITY-009.md (sha256 b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4, FROZEN), research/target-distribution/DEPLOYMENT-IDENTITY-011.md (sha256 ba3862c9aefdc8b1bdb6c45857d492cc36769e7df99ecec1ecb646e57bd6ea74 - sections 1-5 are byte-preserved by this round; only the ordered additive section 6 may be appended), research/tests/test_009a_protocol_elements.py, all 007-m frozen surfaces (config projection 41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0, configuration 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, frozen implementation head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d, deployment profiles c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60 and 0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e), the objective-008 protection layer (research/curated/prose_boundary.py c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50, research/curated/protected.py 27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f, research/prose-boundary/config/structural-policy-v5.json 915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542, structural-policy-v4.json f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f, research/prose-boundary/config/experiment-008i.json 24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685, policy v3 and all earlier policies, and every other prose-boundary file), the objective-011-a/011-b artifacts (oap/orders/011-a-*, oap/reports/011-a-*, oap/orders/011-b-confirmation-stage1-collection.md sha256 0456004c0136ec0de9e3732b3d76ddd343d9124730a865fa7e946182a3105627, oap/reports/011-b-confirmation-stage1-collection.md, RESEARCH-STATE sections 25-26, the 011-a/011-b ledger entries, machine block at main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8 with counters registry_entries 38 / oap_reports_reviewed 57 / frozen_report_history_incidents 2), CRITICAL.md (seed-identical a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e), every test file, all workflows, scripts/, src/, the OAP tree except the files released below, the private research-runtime roots (009a-identity/ read-only; 011b-identity/ read-only including the STRATEGY-CORRECTED credentials receipt; the new round-private 011c-identity/ directory, private and never committed), and any unrelated local work (the three untracked residues corpus/, .research-test-scratch/, .rclone-speed-test/ are pre-existing and never committed).",
  "prior_review": "Strategy independent final-head review of 011-b (2026-10-01, private workorders/011-b-final-head-review-20261001.md): verdict PASS on a BLOCKED round result (a truthful, protocol-conformant outcome). Verified: verify-report remote scope at f505492daa2fa396015739999677bc593c07dc0f (report history valid, 58 report files, only the two known frozen 006-a/006-c incidents); report-only commit with implementation head d4873cfaa4d1f9ceab4d529402db5743f5a9c902 as sole parent and the report as sole changed path; round diff exactly the nine released paths; local consistency 10/10 at the final head; registry 38 with exactly one new 011-b data-free entry (status BLOCKED); machine block counters 38/57/2 with all identity fields byte-unchanged; DEPLOYMENT-IDENTITY-011.md data-free with the verbatim E2(b) designation, the product-intent impact statement, the 009-a pin by hash, the complete 2-of-2 re-probe attempt record (401 on /v1/version; 404 on /v1/v1/models) and the honest verdict (drift NEITHER ESTABLISHED NOR EXCLUDED; regime-unchanged NOT established); all four required checks genuinely green at the final head (Application baseline run 36794503524; OAP bootstrap workflow run 36794503508 with both jobs green - OAP bootstrap acceptance and OAP report history; Research reproducibility run 36794503495; every run at head f505492); PR #12 OPEN at f505492, no merge, no auto-merge. The review names the STRATEGY-SIDE root cause of the probe failure: the private credentials receipt recorded the /v1 API base as the single base, whereas the 009-a re-probe used the server root for /version and the /v1 base for /v1/models; the round's scope-2c stop was the design working as intended. The strategy-side correction (private, 2026-10-01): the credentials receipt 011b-identity/target-credentials-20261001.json now carries BOTH bases (endpoint_server_root_base for the /version route; endpoint_base_url with the /v1 prefix for the /v1/models route) plus an explicit metadata_probe_routes field and a correction_record; the bearer is unchanged (same owner-provided out-of-band value, controlled storage 0600, never committed). The intervening round required by DEPLOYMENT-IDENTITY-011 section 4 is THIS round (011-c): the canonical-route 2-GET probe under the same exactly-2-attempt budget, recording its own private receipt. The E2(b) designation stands untouched (no re-opening); the single named human input (the 011b-intake corpus per the 011-b order item 3b) remains outstanding and is escalated to the owner exactly once - independently of this round, which performs no intake work.",
  "provenance": [
    {"kind": "H", "reference": "The owner's verbatim E2(b) decision 2026-09-30 '(b) Designate A100-FP8 as the confirmation target' (private receipt workorders/e2b-decision-receipt-20261001.md) - the D2 boundary resolution this round verifies; the owner's out-of-band endpoint/bearer provisioning with the bounded-probe usage constraint (at most 2 metadata GETs total, exactly 2 attempts, no retries, zero generation calls) as recorded in the private credentials receipt; the standing A1 instruction (all four required checks genuinely green; reds never reinterpreted; no weakening); the owner's 2026-09-30 objective-009 instruction (continue the loop without the owner as terminal relay; escalate only genuine human/D2 decisions)."},
    {"kind": "A", "reference": "research/target-distribution/DEPLOYMENT-IDENTITY-011.md section 4 (committed at the 011-b final head, byte-preserved): 'The intervening round must re-execute the ordered 2-GET probe against the canonical server-root metadata routes (/version unauthenticated; /v1/models with the authorized bearer) under the same exactly-2-attempt budget, and record its own private receipt'; research/target-distribution/PROTOCOL-009.md (FROZEN, cc5e9089...) element (a) (the hard gate: the target's pinned identity must be verified by the bounded metadata procedure BEFORE the first confirmation sample is collected) and element (b) (the freshness precondition of the collection round); research/target-distribution/DEPLOYMENT-IDENTITY-009.md (FROZEN, b6734b35...) section 1 (the 009-a pinned identity: vLLM 0.28.0, qwen3.8-27b, root suffix Qwen3.8-27B-FP8, max model length 262144, OpenAI-compatible Responses wire API non-streaming) and the attempt-level route precedent (attempt 1: /version, 200, unauthenticated; attempt 4: /v1/models, 200, authorized bearer); S-ORDER-03 (continuation suffixes preserve branch and PR while that PR is open); S-DECIDE-01 (D0 routine bounded verification); S-PRODUCT-04 (no protected Qwen change; no credentials in artifacts; zero contact with the RTX-3090 host and Deployment B); LR-013 (data-free public artifacts)."},
    {"kind": "E", "reference": "Observed 2026-10-01 (this session, successor strategic, from remote and primary records): remote main = 4507cc78e333c0e48226b64266121171b7b8cea8 = OAP_ACCEPTED_REF (unchanged during the 011-b round); worktree on branch oap/011-target-distribution-confirmation-study at f505492daa2fa39601573999677bc593c07dc0f (the 011-b final head; activation 08d5c8b, identity record bd93112, implementation d4873cf, report-only f505492); PR #12 OPEN and MERGEABLE at head f505492, base main, autoMergeRequest null, the only open PR; oap/active = 011-b; OAP state REVIEW_READY (011-b); CRITICAL.md seed-identical a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e, zero entries; machine block on the branch at f505492: main_sha/reviewed 4507cc78e333c0e48226b64266121171b7b8cea8, parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 38/57/2, identity fields unchanged; local consistency 10/10 at the final head (verified in the 011-b review); registry 38 (last 011-b, kind collection, status BLOCKED); the 011-b re-probe's two non-200 outcomes (401 /v1/version; 404 /v1/v1/models) on non-canonical routes with no identity field observed (committed DEPLOYMENT-IDENTITY-011 section 3; private 011b-identity/reprobe-receipt.json); the private credentials receipt corrected 2026-10-01 (dual bases + explicit canonical metadata routes + correction_record; bearer unchanged; 0600)."},
    {"kind": "I", "reference": "Strategy 011-b final-head review PASS (private workorders/011-b-final-head-review-20261001.md) including the root-cause attribution (strategy-side credentials-receipt route structure) and the correction record; the 011-b publication receipt (private workorders/011-b-publication-receipt-20261001.md) with the FUSE stale-stat observation and the single-exact-signal record; the wrapper-crash incident receipt (private workorders/incident-011b-wrapper-crash-20261001.md) - the 011-b control was consumed exactly once, the supervisor's automatic --resume-id 011-b restart is the S-RECOVER-01 path, and the resumed round completed truthfully; the technical-debt register (TD-1/2/3 non-gating; the TD-3 count stands at 8 occurrences this loop, all retries clean)."}
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
  "lr": ["LR-013"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Objective 011, round 3, on the EXISTING branch
`oap/011-target-distribution-confirmation-study` (AMEND_EXISTING_PR -
PR #12, verified OPEN and MERGEABLE at head
`f505492daa2fa396015739999677bc593c07dc0f`, the 011-b final head, base
main at `4507cc78e333c0e48226b64266121171b7b8cea8`). This is the
**intervening pinning round** required by the 011-b scope-2c stop
(DEPLOYMENT-IDENTITY-011 section 4, committed and byte-preserved): it
re-executes the bounded 2-GET metadata probe against the CANONICAL
routes of the 009-a precedent (server-root `/version` unauthenticated;
`/v1/models` with the authorized bearer) under the same exactly-2-
attempt budget, records the result in an additive section of the
objective's identity record, and - if and only if all identity fields
match the 009-a pin - establishes the regime-unchanged verdict that
satisfies the PROTOCOL-009 element (a) hard gate for the collection
round. It performs NO collection, NO intake, NO manifest, NO selection,
NO split, NO generation call, NO annotation, and NO evaluation; it
makes no merge, release, deployment, or milestone claim; it does not
re-open the E2(b) designation (which stands) and it resolves nothing
about the outstanding human intake (escalated to the owner separately,
once).

## Provenance

- H: the verbatim E2(b) decision (private receipt) whose target identity
  this round verifies; the owner's bounded-probe usage constraint
  (exactly 2 metadata GETs, no retries, zero generation calls) as
  recorded in the private credentials receipt; the standing A1
  instruction; the 2026-09-30 objective-009 instruction.
- A: DEPLOYMENT-IDENTITY-011 section 4 (the exact intervening-round
  requirement, quoted in the metadata); PROTOCOL-009 element (a)/(b)
  (FROZEN); DEPLOYMENT-IDENTITY-009 section 1 (the 009-a pinned
  identity and the canonical route precedent); S-ORDER-03; S-DECIDE-01;
  S-PRODUCT-04; LR-013.
- E: the verified state in the metadata E field (main, PR #12, worktree,
  machine block 38/57/2, 10/10 local consistency, CRITICAL seed, the
  011-b non-canonical-route finding, the corrected private credentials
  receipt).
- I: the 011-b final-head review PASS with the root-cause attribution
  and the receipt correction record; the 011-b publication receipt; the
  wrapper-crash incident receipt (S-RECOVER-01 handled; no replay); the
  technical-debt register (TD-3 at 8 occurrences, all retries clean).

## Current verified state

Verified 2026-10-01 (successor strategic session, from remote and
primary records): remote main =
`4507cc78e333c0e48226b64266121171b7b8cea8` (= OAP_ACCEPTED_REF,
unchanged during the 011-b round); worktree on
`oap/011-target-distribution-confirmation-study` at
`f505492daa2fa396015739999677bc593c07dc0f` (011-b final head;
activation 08d5c8b, identity record bd93112, implementation
d4873cfaa4d1f9ceab4d529402db5743f5a9c902, report-only f505492) with the
three pre-existing untracked residues preserved and never committed;
PR #12 OPEN, MERGEABLE, head f505492, base main, autoMergeRequest null,
the only open PR; oap/active = 011-b; OAP state REVIEW_READY (011-b);
CRITICAL.md seed-identical
a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e,
zero entries; machine block on the branch at f505492: main_sha /
reviewed_branch_head_sha 4507cc78e333c0e48226b64266121171b7b8cea8,
parent 01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, branch
oap/007-concept-verification, pr_number 8, quarantined 007n/008d,
frozen 007-m sha fields, counters registry_entries 38 /
oap_reports_reviewed 57 / frozen_report_history_incidents 2; local
consistency 10/10 at the 011-b final head (011-b review); registry = 38
entries (last 011-b, kind collection, status BLOCKED); all four
required checks genuinely green at the 011-b final head (verified in
the 011-b review at job level); the private credentials receipt
(`011b-identity/target-credentials-20261001.json`, 0600) is the
STRATEGY-CORRECTED version (dual bases; explicit metadata_probe_routes;
correction_record; bearer unchanged); the 011b-intake/ location is
absent (the human input remains outstanding; this round performs no
intake work). Environment: the rclone/Dropbox FUSE mount remains
degraded; heavy test temp stays on native /home/ubuntu/.oap-scratch
(0700); OAP helper git-history traversals can transiently time out at
the 30 s subprocess limit (TD-3, non-gating; retry deterministic and
safe); CI parity is authoritative for the heavy fixture cycles.

## Governance

The sixteen source identities in the metadata governance mapping are the
exact identities of `oap/governance/MANIFEST.json` at the accepted base
`4507cc78e333c0e48226b64266121171b7b8cea8`, unchanged (16/16,
coding_bytes 35076). No governance change occurs in this objective. The
round-private `011c-identity/` directory (0700; receipt 0600) follows
the established convention; it is never committed.

## Goal and dependencies

Goal: establish (or truthfully fail to establish) the regime-unchanged
verdict for the E2(b)-designated A100-FP8 target by the bounded
canonical-route metadata probe, so that the PROTOCOL-009 element (a)
hard gate is either satisfied (enabling the collection round 011-d on
the verified identity) or the exact finding is recorded for a
bounded next step - with zero collection, zero generation calls, and
zero contact with any other endpoint.

Dependencies: 011-b (reviewed PASS; its scope-2c stop defines this
round's exact task), 011-a (green quiescent branch base), the
E2(b) designation (standing; not re-opened), the corrected private
credentials receipt (strategy-side, in place at publication). Nothing
else. The human intake and the two labelers belong to later rounds and
are NOT dependencies of this round.

## Scope

1. Pre-work integrity gates (data-free): at the base
   `f505492daa2fa396015739999677bc593c07dc0f`, byte-verify every frozen
   surface and the objective-009/011-a/011-b artifacts (PROTOCOL-009.md,
   DEPLOYMENT-IDENTITY-009.md, DEPLOYMENT-IDENTITY-011.md sections 1-5,
   test_009a_protocol_elements.py, the 007-m pins, the 008 protection-
   layer pins, the 011-a/011-b orders and reports, RESEARCH-STATE
   sections 24-26, CRITICAL.md seed-identical
   a9ea5fa5db2affabf0f85710f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e);
   machine block on the branch: main_sha/reviewed
   4507cc78e333c0e48226b64266121171b7b8cea8, parent
   01ea3fa4cde5c4759bcf29d6c665ed8b2e29524d, counters 38/57/2, identity
   fields unchanged; registry = 38 entries (last 011-b, status BLOCKED);
   local consistency 10/10 in a real checkout of the branch with
   origin/main = 4507cc78e333c0e48226b64266121171b7b8cea8. Any mismatch
   is BLOCKED with the mismatch named; no work proceeds.
2. Bounded canonical-route re-probe BEFORE any other mutation beyond
   the ordered record (EXACTLY 2 metadata GETs total, no retries, zero
   chat/generation/responses calls, zero other endpoints, zero writes,
   zero server mutation, zero RTX-3090 contact, zero Deployment B
   contact):
   - Attempt 1: GET {endpoint_server_root_base}/version, unauthenticated
     (the canonical 009-a route; 009-a attempt 1 returned 200 there).
   - Attempt 2: GET {endpoint_base_url}/models with the authorized
     bearer (the canonical 009-a route; 009-a attempt 4 returned 200
     there).
   - The authorized profile (both bases and the bearer) is read ONLY
     from the strategy-corrected private credentials receipt
     (`011b-identity/target-credentials-20261001.json`, 0600; the value
     is never committed, never logged, never echoed into any report or
     public artifact). The route construction follows the receipt's
     metadata_probe_routes field verbatim; if the receipt and this
     order ever disagree, the round BLOCKS on the named discrepancy
     rather than improvising a route.
   - Every attempt is recorded in the round private receipt
     `011c-identity/reprobe-receipt.json` (private, never committed;
     timestamps, statuses, observed fields, response sizes, wall times).
3. Verdict rule (exact):
   - REGIME-UNCHANGED: attempt 1 returns 200 with serving framework
     version 0.28.0 AND attempt 2 returns 200 with model identifier
     qwen3.8-27b, root suffix Qwen3.8-27B-FP8, max model length 262144,
     and the wire protocol class remains OpenAI-compatible Responses
     non-streaming (per the observed identity fields) -> the pinned
     identity is re-verified as of this round; the regime-unchanged
     verdict is ESTABLISHED; the PROTOCOL-009 element (a) hard gate is
     satisfied for collection; the round proceeds to item 4 (the
     additive record states that the collection round 011-d may proceed
     on this verified identity, subject to its own intake gate).
   - DRIFT: both attempts return 200 but ANY observed identity field
     differs from the 009-a pin -> the drift is ESTABLISHED and named
     field-by-field; the round records it in the additive section,
     reports Result: BLOCKED (drift) - the frozen protocol authorizes no
     behavior on a drifted regime; a re-designation or endpoint
     restoration is a D2/human decision that this round does not take;
     no collection may proceed.
   - PROBE FAILURE: any attempt within the 2-attempt budget returns
     non-200 (including 401/404/timeout/transport error) -> the round
     STOPS at the finding per the 011-b scope-2c precedent: the exact
     route, status, and request metadata are recorded data-free in the
     additive section, Result: BLOCKED (probe failure), drift NEITHER
     ESTABLISHED NOR EXCLUDED; a second consecutive probe failure
     (across rounds) requires a strategy-side bounded diagnostic before
     any further probe, and an endpoint change is an owner input - this
     round never improvises beyond the 2-attempt budget.
4. Additive identity record: append EXACTLY one additive section 6 to
   `research/target-distribution/DEPLOYMENT-IDENTITY-011.md` (sections
   1-5 byte-preserved; no rewrite of any committed byte of sections
   1-5): the 011-c canonical-route re-probe attempt record (routes,
   statuses, observed identity fields, observation window, response
   sizes - data-free values only) plus the verdict per item 3 plus the
   consequence statement (collection authorized on the verified
   identity / drift named and collection blocked / probe failure named
   and collection blocked) plus the reaffirmed boundaries (RTX-3090
   MUST-NOT-BE-STARTED zero contact; Deployment B excluded ever;
   REPAIR_ALLOW_LIVE_TESTS stays NO; no second large GPU model).
5. Bookkeeping (data-free): (a) exactly one 011-c entry appended to
   `research/registry/experiments.json` (registry 38 -> 39; data-free;
   kind state-correction; status per the round outcome; the verdict
   and the attempt outcomes data-free); (b) machine-block counters
   registry_entries 38 -> 39 and oap_reports_reviewed 57 -> 58 (the
   011-c report file), frozen_report_history_incidents unchanged at 2;
   all identity fields UNCHANGED (no advance); (c) STATUS.md round
   sentences; (d) `oap/GENERATED-FILES.json` scoped pin (same scope
   pattern as 009-a/009-b/010-a/011-a/011-b); (e)
   `research/tables/experiment-summary.csv` rebuild; (f)
   `research/RESEARCH-STATE.md` additive section 27 (the 011-c identity
   re-verification record: the canonical routes, the attempt outcomes,
   the verdict, the consequence for the collection round; NO rewrite of
   sections 1-26 or the machine block except item 5b).
6. Report-only final commit: sole parent = the literal implementation
   head; sole changed path
   `oap/reports/011-c-identity-reverification-canonical-routes.md`; the
   report discloses the final-head check state verbatim and, in the
   BLOCKED branches, the exact finding with zero collection performed.
7. Final-head CI: all four required checks green at the final head (or
   the predeclared re-run state disclosed verbatim at report time,
   resolved before strategy's final-head review).
8. Push and verify; send the exact response OK and stop. PR #12 stays
   OPEN; no merge; no auto-merge.

## Non-goals

- NO collection, NO intake (the 011b-intake/ location stays absent
  unless the owner delivers the corpus in the meantime - this round
  performs no intake verification either way; the intake gate belongs
  to the collection round 011-d), NO manifest, NO selection, NO split,
  NO generation call of any kind, NO sample opened, NO annotation, NO
  evaluation, NO scoring, NO comparator run.
- NO behavior change of any frozen element (PROTOCOL-009 (n) intact).
- NO PROTOCOL-009.md, DEPLOYMENT-IDENTITY-009.md, or frozen-surface
  change; NO rewrite of DEPLOYMENT-IDENTITY-011.md sections 1-5 (the
  ordered additive section 6 only); NO test change; NO governance or
  CRITICAL.md change; NO OAP protocol change.
- NO merge, NO auto-merge, NO force-push, NO release, NO deployment, NO
  milestone claim, NO E2 re-opening (the designation stands; a drift
  finding would BLOCK, not re-decide).
- NO contact with the RTX-3090 host (MUST-NOT-BE-STARTED; zero probes,
  zero calls), NO contact with Deployment B (EXCLUDED_BY_HUMAN_OVERRIDE;
  zero probes, zero calls, ever), NO server mutation, NO second large
  GPU model, NO streaming, NO endpoint other than the two canonical
  metadata routes of the designated target.
- NO raw text, NO endpoint values, NO credentials, NO private absolute
  paths in any committed artifact or log (LR-013); the private tree is
  NEVER committed; the publication guard runs on the full tree
  pre-push.

## Files and boundaries

Write (repository): exactly
`research/target-distribution/DEPLOYMENT-IDENTITY-011.md` (additive
section 6 only; sections 1-5 byte-preserved),
`research/RESEARCH-STATE.md` (additive section 27 + machine-block
counters only), `research/registry/experiments.json` (+1 data-free
entry), `STATUS.md`, `oap/GENERATED-FILES.json` (scoped pin),
`research/tables/experiment-summary.csv` (rebuild),
`oap/orders/011-c-identity-reverification-canonical-routes.md` (new,
activation), `oap/active` (pointer),
`oap/reports/011-c-identity-reverification-canonical-routes.md` (new,
report-only commit).
Write (private, never committed): `011c-identity/reprobe-receipt.json`
(round private research runtime root; 0700/0600).
Read-only: the rest of the accepted tree and all frozen surfaces
(byte-verified in the pre-work gate); the private 009a-identity/ and
011b-identity/ directories (the 009-a receipt and the corrected
credentials receipt).
Coding read set: the compact sources, this order, RESEARCH-STATE
sections 24-26, DEPLOYMENT-IDENTITY-011.md (full, sections 1-5
byte-preserved), DEPLOYMENT-IDENTITY-009.md section 1, the private
011b-identity credentials receipt (identity values only as needed for
the two calls), and the 011-b report.

## Requirements

1. Pre-work gates per Scope 1 (any mismatch BLOCKED and named).
2. The canonical-route re-probe per Scope 2 (exactly 2 metadata GETs on
   the canonical routes; zero generation calls; the corrected receipt
   as the sole profile source; the private receipt written).
3. The verdict per Scope 3 (regime-unchanged / drift / probe failure),
   executed exactly: the consequence of the verdict is the round's
   stopping or proceeding rule.
4. The additive section 6 per Scope 4 (sections 1-5 byte-preserved;
   data-free).
5. Bookkeeping per Scope 5 (registry 39; counters 39/58/2; STATUS.md;
   GENERATED-FILES pin; csv; RESEARCH-STATE section 27 additive).
6. Report-only commit per Scope 6; final-head CI per Scope 7 (all four
   required checks genuinely green); exact response OK per Scope 8
   after remote verification; PR #12 stays OPEN.

## Acceptance criteria

1. The pre-work gate evidence is committed or recorded; any mismatch
   would have BLOCKED the round with the mismatch named.
2. The re-probe executed exactly 2 metadata GETs on the canonical routes
   (attempt 1: server-root /version unauthenticated; attempt 2:
   /v1/models with the authorized bearer); zero generation calls; zero
   prohibited contact; the private receipt records every attempt.
3. The verdict is one of the three exact branches, recorded data-free
   in the additive section 6 with the exact finding; sections 1-5 of
   DEPLOYMENT-IDENTITY-011.md are byte-identical to the 011-b final
   head; in the REGIME-UNCHANGED branch the consequence statement
   authorizes the collection round on the verified identity; in the
   DRIFT and PROBE-FAILURE branches the round reports BLOCKED with the
   exact finding and nothing beyond the ordered record is executed.
4. Bookkeeping is complete and consistent (registry 39 with exactly one
   new 011-c data-free entry; counters 39/58/2; STATUS.md; GENERATED-
   FILES pin; csv; RESEARCH-STATE section 27 additive with sections
   1-26 unaltered except the ordered counters).
5. The report-only commit has the literal implementation head as sole
   parent and the report path as sole changed path; the round diff
   (base..final) is limited to the released-from-freeze list; zero
   secret-pattern hits in added lines; the untracked residues absent
   from every commit; the private tree absent from every commit.
6. All four required checks genuinely green at the final head (no
   pending, cancelled, or reinterpreted check); the response OK frame
   received after remote verification.
7. PR #12 on oap/011-target-distribution-confirmation-study (base main
   at 4507cc78e333c0e48226b64266121171b7b8cea8) is still OPEN; no
   merge; no auto-merge.

## Verification

- Focused: research/tests/test_research_state_consistency.py (10/10
  green at the final head in a real checkout with origin/main =
  4507cc78e333c0e48226b64266121171b7b8cea8; at the implementation head
  exactly one designed red - the report-count assertion 58 vs 57 - the
  008-i/009-b/010-a/011-a/011-b pattern, recorded with the tested SHA);
  the 009-a focused lint (research/tests/test_009a_protocol_elements.py,
  unchanged, still green); the full research suite under the frozen uv
  environment; the OAP suite to the extent feasible on the degraded
  rclone/Dropbox FUSE mount (bounded-stop clause per the 009-a/009-b/
  010-a/011-a/011-b precedent; the two OAP CI jobs are authoritative);
  one full local Application-baseline driver run (local evidence only;
  the recurring FUSE git-walk 30-s subprocess timeout is a known
  environmental artifact - manual repro distinguishes it, the 011-b
  precedent).
- Additive-fidelity check: git diff of DEPLOYMENT-IDENTITY-011.md
  shows ONLY the section-6 insertion (sections 1-5 byte-identical to
  the base blob ba3862c9aefdc8b1bdb6c45857d492cc36769e7df99ecec1ecb646e57bd6ea74
  prefix).
- Data-free artifact checks: the additive section carries no endpoint
  values, no credentials, no private absolute paths, no raw text; the
  publication guard (full-tree) passes pre-push; strategy re-scans the
  published report privately post-publication and records it in the
  review.
- Broader: the full CI battery at the implementation head and the final
  head.
- Evidence boundary: the live work is EXACTLY the 2-attempt canonical-
  route metadata probe on the E2(b)-designated target (authorized by
  the owner E2(b) decision + PROTOCOL-009 element (a), separately from
  REPAIR_ALLOW_LIVE_TESTS = NO which stays unchanged); no other network
  calls, no other endpoints, no writes anywhere on the target. The
  report is a claim until strategy's independent final-head review
  re-verifies it field-by-field (S-REVIEW-01).

## Local setup and constraints

- The frozen uv environment; no new dependencies; no GPU on this host
  (the target is the remote designated A100-FP8 deployment; NO second
  large GPU model); no service touches; no protected Qwen
  weight/config/network change (S-PRODUCT-04); REPAIR_ALLOW_LIVE_TESTS
  stays NO; no endpoint value, credential, or private absolute path in
  any committed artifact or log.
- Private roots: the round-private `011c-identity/` directory (0700)
  holds only the re-probe receipt (0600); the 011b-identity/ corrected
  credentials receipt is the sole profile source (read-only for this
  round); 009a-identity/ is a read-only reference; never committed.
- Local: reversible setup inside the authorized workspace only; doctor
  runs with env -u CODEX_HOME -u OAP_ROLE; heavy test temp on native
  /home/ubuntu/.oap-scratch (0700) given the degraded FUSE mount; any
  unresolvable setup failure is BLOCKED and reported, not worked around.

## Documentation

- DEPLOYMENT-IDENTITY-011.md additive section 6 (Scope 4) - the 011-c
  re-probe record and verdict.
- RESEARCH-STATE.md additive section 27 (Scope 5f) - the identity
  re-verification entry in the canonical ledger narrative, plus the
  machine-block counters (Scope 5b).
- STATUS.md per Scope 5c; the OAP report per the round mechanics (data-
  free by construction: routes, statuses, observed fields, verdict; no
  endpoint values, no credentials; the round's classification recorded:
  D0 execution of the ordered bounded verification; no CRIT admission).

## Git and report publication

- Branch `oap/011-target-distribution-confirmation-study` (EXISTING;
  verified at `f505492daa2fa396015739999677bc593c07dc0f`, PR #12 OPEN,
  base main at 4507cc78e333c0e48226b64266121171b7b8cea8). This round
  AMENDS PR #12; no new branch, no new PR, no force-push.
- Activation commit (order + oap/active) per the round mechanics;
  implementation commits per Scope 2-5 (exact split at the executor's
  discretion, all within the released-from-freeze list); the report-only
  commit per Scope 6 (sole parent = literal implementation head; sole
  changed path = the report).
- Push semantics per the OAP communication profile; no push after the
  report-only commit; the exact response OK after remote verification;
  the coding wrapper consumes the 011-c control signal exactly once
  before model launch.
- No merge: PR #12 stays OPEN; no auto-merge; the merge decision is a
  separate post-review strategic act at the objective's end (S-MERGE-01;
  repository-approved method: standard merge commit at the exact reviewed
  SHA, verify-merge, default-branch check) - not in this round.

## Decision classification

D0 (S-DECIDE-01): the round executes the ordered bounded verification
that the committed identity record (DEPLOYMENT-IDENTITY-011 section 4,
from the 011-b round under the FROZEN protocol's element (a))
pre-specifies, under the owner's standing E2(b) authorization; the
route correction is a strategy-side private-receipt fix (root-caused in
the 011-b review; recorded privately), not a protocol change; every
mechanical choice is the unique transcription of the ordered procedure
- no judgment debt, no CRIT admission (S-DECIDE-03 condition 1 fails:
the committed requirement, the 009-a route precedent, the corrected
receipt, and the owner's exactly-2-attempt constraint leave no
unresolved choice). A DRIFT or second PROBE-FAILURE outcome is a
truthful BLOCKED result that hands a genuine D2/human question to the
owner - it is a stop, not a decision.

## Deferred human adjudication

- Decision: NONE

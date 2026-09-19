# Work order 008-d — Application-baseline timing corrective and ledger registration

Status: FINAL

Finalized by strategic review of 008-c (final head
4b6a90ab13c0c9a02e533a2673a084e26f841a5c, report-only commit over
implementation head 9aec9cb0bc514be5e2db593ca0f1930b34c93891, base
49e4e70f1a8c304b4ad5ce27055a39e9e6e17288) and the explicit human
instruction of 2026-09-18: before any further scientific work, finish the
current corrective work correctly and ensure that Application baseline,
Research reproducibility, OAP bootstrap acceptance, and OAP report history
are all genuinely green at the reviewed final head, without weakening,
skipping, or redefining any check, and without manufacturing green status,
milestone, deployment, or linguistic acceptance. Independently verified
strategic review found exactly one red gate at the 008-c final head: the
Application baseline full-pytest stage recorded TIMEOUT at the frozen 300 s
per-command cap with 653 passed, 14 skipped, 89 subtests and ZERO test
failures in 337.20 s (stable 329.96/334.87/337.06/337.20 s across the
2026-09-18 runner pool, versus 134.92 s for the 008-b implementation head
on the 2026-09-17 pool): a runner-pool timing artifact on an inherited
application test suite, not a 008-c test failure. This round is therefore a
bounded measurement-and-bookkeeping corrective suffix on the same objective-
008 branch and PR #9: it reconciles the current state, observes the frozen
full-pytest stage under the unchanged 300 s cap (bounded rerun observations
of the identical commit, recorded verbatim), produces a committed data-free
timing decomposition so the inherited-debt classification is precise,
registers the round in the research ledger and machine block, corrects the
single stale suffix reference in current status documentation (blind hidden
acceptance is round 008-e, not 008-d, per the recorded D1 renumbering in the
008-c final-head review), and publishes the truthful report that additively
records the 008-c final-head CI facts. The round makes NO gate, cap,
driver, workflow, or test change. A BLOCKED outcome is predeclared and
permitted: if the frozen full-pytest stage still exceeds the 300 s cap at
this round's final head after the bounded observation budget, the round
reports BLOCKED with the per-factor decomposition and stops; strategy then
adjudicates before 008-e (possible separate bounded correction order for
the inherited debt, or pool-recovery wait). No hidden-set evaluation occurs
in this round; that is 008-e. No linguistic-method change of any kind
occurs; the frozen 007-m system and the frozen 008-c implementation remain
byte-identical.

```oap-metadata
{
  "id": "008-d",
  "title": "Application-baseline timing corrective and ledger registration",
  "objective": "008",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "4b6a90ab13c0c9a02e533a2673a084e26f841a5c",
  "branch": "oap/008-prose-boundary-qualification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 9,
  "dependencies": ["008"],
  "local_work": "Preserve byte-for-byte: every merged 000-007 seam on main, the entire research/ tree at the 008-c final head (including the frozen 008-a baseline under research/prose-boundary/: config/experiment-008a.json, fixtures/, results/increment1/, results/increment2/, REPORT.md, adapter/ source, identity/), the 008-c parser-first implementation (research/curated/prose_boundary.py, research/curated/protected.py, all research/prose-boundary/config/ files, the committed corpus under research/prose-boundary/corpus/, results/increment3/), the 008-c focused test file research/tests/test_parser_first_protection.py byte-identical, ALL other test files byte-identical, scripts/verify_development_baseline.py byte-identical, all .github/workflows/ byte-identical, every private experiment root (including the sealed 008c-hidden/ private root - manifest-hash access only, no hidden content reads in this round), and any unrelated local work (untracked .research-test-scratch/ and any untracked root corpus/ residue - never commit either).",
  "prior_review": "Strategy independent final-head review of 008-c (2026-09-18, private workorders/008-c-final-head-review-20260918.md): report-only commit 4b6a90a (sole parent 9aec9cb, sole changed path oap/reports/008-c-parser-first-protection.md); verify_report remote=verified (report history valid, 2 frozen incidents, report_count 47); round diff 49e4e70..4b6a90a = 6114 added / 7 modified, all within order scope; frozen 008-a baseline and src/ byte-identical; registry 27 entries; machine block consistent (oap_reports_reviewed 46 = 47 report files minus the 007-o exclusion); hidden seal independently re-hashed 4091/4091 against committed corpus/manifests/hidden-manifest.json (sha256 8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18); generation identity 386/400 planned slots, 414 disclosed attempts, all failures recorded; dev-corpus tuning evidence (protected-bytes-exposed 0/526,315, coordinate violations 0, end-to-end invariants 7/7); CI at final head 4b6a90a: OAP bootstrap acceptance PASS (run 35350302302), OAP report history PASS (run 35350302302), Research reproducibility PASS (run 35350302411, 280 tests), Application baseline FAIL (run 35350302300: full-pytest stage TIMEOUT at the frozen 300 s command cap, 653 passed / 14 skipped / 89 subtests / 0 failures, 337.20 s); response OK frame lost (no reader on response FIFO) - per P-RECOVERY-01 strategic review proceeded without coding replay, no resend; disposition: 008-c accepted as published, development merge of PR #9 BLOCKED (one required check red at the final head), corrective path = bounded suffix 008-d (observation and bookkeeping only, no gate changes), blind hidden acceptance renumbered to 008-e; PR #9 open/unmerged, main still 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9. Protocol state re-verified by strategy at 008-d publication: check_state with remote = REVIEW_READY for 008-c.",
  "provenance": [
    {"kind": "H", "reference": "Human instruction 2026-09-18 (current turn): (1) finish the currently active corrective work correctly before any further scientific work; inspect current PR #9 head, oap/active, and current required CI; independently verify the order and implementation; resolve the current defect without weakening checks; ensure Application baseline, Research reproducibility, OAP bootstrap acceptance, and OAP report history are all genuinely green at the reviewed final head; correct materially stale current-status documentation when scope/governance permits; do not merge a red head; do not skip the report-only final state; do not manufacture milestone, deployment, or linguistic acceptance; (2) if the Application baseline failure is unrelated inherited/flaky debt, classify it precisely and propose a separate bounded correction order after this report round - do not smuggle an unrelated application fix into this research-state publication; (3) keep the Concentrated-OAP loop moving; the owner is not a terminal relay; D0/D1 are strategy's to resolve, only genuine D2 escalates; (4) continuing context of the human research decision of 2026-09-17: 008-a GO stands as supporting evidence for pulldown-cmark 0.13.4 with its two recorded limitations, LLM calls are authorized strictly for structural test-data generation (not in this round - none are made), objective 009 remains separate and untouched, the frozen 007-m linguistic method is never tuned."},
    {"kind": "A", "reference": "S-REVIEW-01 (independent final-head review; post-publication checks recorded privately), S-MERGE-01 (a missing/pending/failed required check blocks development merge; a red head is never merged), S-ORDER-02/03 (exact order contract; corrective suffix preserves the objective branch and PR), S-EVIDENCE-01 (truthful distinct recording of PASSED/FAILED/TIMEOUT/PENDING per head and SHA), S-DIAGNOSE-01 (locate the earliest failing boundary; smallest discriminating experiment with a stop condition), the driver contract scripts/verify_development_baseline.py (DEFAULT_COMMAND_TIMEOUT = 300.0, a frozen 007-era per-command watchdog, unchanged by this round), the 004-d scoped generated-file pin precedent (oap/GENERATED-FILES.json STATUS.md entry), the 008-b ledger-registration pattern (registry kind audit entry + machine-block update), P-SELF-03 (a pre-push report never claims future push/CI success; publication_verified=false convention)."},
    {"kind": "E", "reference": "CI at 008-c final head 4b6a90a (independently re-verified by strategy 2026-09-18 via GitHub): Application baseline run 35350302300 FAILED - full-pytest stage TIMEOUT at the 300 s cap with the captured session summary '653 passed, 14 skipped, 89 subtests passed in 337.20s (0:05:37)' and driver record failure 'full pytest:TIMEOUT'; OAP bootstrap acceptance run 35350302302 PASS; OAP report history run 35350302302 PASS; Research reproducibility run 35350302411 PASS (280 tests). Prior 008-c implementation heads on the 2026-09-18 pool, recorded in the immutable 008-c report and this round's base: 21c4135 full-pytest TIMEOUT 329.96s ('2 failed, 651 passed' = B10 + count assertion, both fixed in-round), 9aec9cb full-pytest TIMEOUT 337.06s ('1 failed, 652 passed' = solely the designed pre-report count assertion), d0c284a full-pytest TIMEOUT (334.87 s recorded in the 008-c final-head review receipt). 2026-09-17 pool reference point: 008-b implementation head 8300573 full-pytest FAILED (not TIMEOUT) in 134.92s ('613 tests' total, 1 failed = solely the same designed pre-report count assertion, 5 skipped, 87 subtests). The 008-c round changed the full-pytest population by exactly one new focused test file (48 tests; 14 of them skip in CI without the pinned Rust helper) - no modification of any pre-existing test. check_state with remote at 4b6a90a = REVIEW_READY for 008-c; oap/active = 008-c; consumed.json = 008-c with recovery true; coding wrapper alive and blocked on the control FIFO."},
    {"kind": "I", "reference": "Strategy independent final-head reviews: workorders/008-c-final-head-review-20260918.md (this round's direct basis: the one red gate, its per-head timing evidence, merge BLOCKED disposition, corrective 008-d path, 008-e renumbering) and workorders/008-b-final-head-review-20260917.md (the 008-b ledger-registration pattern and all-four-green baseline at 49e4e70)."}
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

Fourth round of objective 008, amending the objective-008 branch
`oap/008-prose-boundary-qualification` and PR #9. 008-a (frozen head
8dbb79a20f129d4c07c6b94827cacad74683ba6b) qualified `pulldown-cmark`
0.13.4 with outcome GO; 008-b (final head
49e4e70f1a8c304b4ad5ce27055a39e9e6e17288) restored the post-merge
research-state identities and registered 008-a in the ledger; 008-c
(final head 4b6a90ab13c0c9a02e533a2673a084e26f841a5c) implemented the
parser-first structural protection layer, the authorized generated
structural evaluation program, and the sealed hidden acceptance set, and
froze the implementation. Independent strategic review accepted 008-c as
published but found the development merge BLOCKED: at the 008-c final
head the Application baseline required check is red - the full-pytest
stage timed out at the frozen 300 s per-command cap (337.20 s) with
ZERO test failures, a runner-pool timing artifact on the inherited
application test suite (the 008-b implementation head ran the near-
identical suite in 134.92 s on the 2026-09-17 pool). This round is the
bounded corrective suffix: it observes the frozen stage under the
unchanged cap, decomposes the timing data-free, registers the round in
the ledger, corrects the one stale suffix reference in status
documentation (blind hidden acceptance is 008-e per the recorded D1
renumbering), and publishes the truthful report. It is bounded D0
engineering plus CI observation. It is not a test change, not a gate
change, not a production change, not a linguistic experiment, and it
makes no model call.

## Provenance

- H: Human instruction 2026-09-18 (full text summarized in the metadata
  provenance): finish the current corrective work correctly before any
  further scientific work; all four required checks genuinely green at
  the reviewed final head; no weakening/skipping/redefining any check; no
  manufactured green status, milestone, deployment, or linguistic
  acceptance; correct materially stale current-status documentation when
  scope/governance permits; classify unrelated inherited/flaky debt
  precisely and propose a separate bounded correction order rather than
  smuggling an unrelated application fix into this round; keep the loop
  moving; the owner is not a terminal relay. Continuing context of the
  2026-09-17 decision: 008-a GO is supporting evidence only; LLM calls
  are authorized strictly for structural test-data generation (this round
  makes none); objective 009 remains separate and untouched; the frozen
  007-m linguistic method is never tuned.
- A: S-REVIEW-01, S-MERGE-01 (a failed required check blocks the
  development merge; a red head is never merged), S-ORDER-02/03 (order
  contract; corrective suffix preserves branch and PR), S-EVIDENCE-01
  (distinct truthful per-head check recording), S-DIAGNOSE-01 (earliest
  failing boundary; smallest discriminating experiment; explicit stop
  condition), the frozen driver contract
  (`scripts/verify_development_baseline.py`, DEFAULT_COMMAND_TIMEOUT =
  300.0 per-command watchdog, 007-era, unchanged), the 004-d scoped
  generated-file pin precedent (oap/GENERATED-FILES.json), the 008-b
  ledger-registration pattern, P-SELF-03 (no pre-push claim of future
  push/CI success).
- E: The verified CI facts at 4b6a90a and the per-head timing record
  (metadata provenance E): run 35350302300 full-pytest TIMEOUT at the 300
  s cap, 653 passed / 14 skipped / 89 subtests / 0 failures / 337.20 s;
  runs 35350302302 (OAP jobs) and 35350302411 (Research) PASS; prior
  008-c heads TIMEOUT at 329.96 s (21c4135) and 337.06 s (9aec9cb) with
  only the in-round-fixed defects and/or the designed pre-report count
  assertion failing; 334.87 s recorded for d0c284a in the 008-c
  final-head review receipt; 134.92 s at the 008-b implementation head
  8300573 on the 2026-09-17 pool with solely the designed pre-report
  count assertion failing; the 008-c round's only full-pytest population
  change is the single new focused test file (48 tests, 14 CI-skips).
- I: Strategy independent final-head reviews of 008-c (private
  workorders/008-c-final-head-review-20260918.md) and 008-b (private
  workorders/008-b-final-head-review-20260917.md).

## Current verified state

Verified by strategy at publication (this session, from remote and primary
records):

- main remains `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9` (development-
  only merge of PR #8); objective 007 closed.
- PR #9 OPEN / UNMERGED, auto-merge disabled, head
  4b6a90ab13c0c9a02e533a2673a084e26f841a5c (the 008-c final head).
- CI at 4b6a90a (re-verified this session via GitHub): Application
  baseline FAIL (run 35350302300, full-pytest stage TIMEOUT at the 300 s
  cap, 653 passed / 14 skipped / 89 subtests / 0 failures, 337.20 s);
  OAP bootstrap acceptance PASS (run 35350302302); OAP report history
  PASS (run 35350302302); Research reproducibility PASS (run
  35350302411, 280 tests). The full-pytest population difference between
  the 09-17 and 09-18 observations is exactly the 008-c focused test
  file; no pre-existing test was modified.
- Protocol state: `oap/active` = 008-c; `check_state` with remote =
  REVIEW_READY for 008-c; consumed.json = 008-c (recovery true). The
  008-c response OK frame was lost (no reader); per P-RECOVERY-01 the
  round is complete and reviewed, no resend, no coding replay. The
  coding wrapper is alive and blocked on the control FIFO.
- The 008-c report is immutable and already records the final-head CI
  truth as PENDING inside the pre-push report (publication_verified=false,
  P-SELF-03), deferring the post-publication state to strategic review;
  this round's report completes that deferral additively.
- Local worktree at 4b6a90a plus untracked residue only
  (`.research-test-scratch/` and possibly an untracked root `corpus/`
  generation residue; neither is ever committed).

## Governance

S-REVIEW-01, S-MERGE-01, S-ORDER-01/02/03, S-EVIDENCE-01, S-DIAGNOSE-01,
S-DECIDE-01 (D0: bounded, reversible, inside the risk budget). D0
overall: CI observation of a frozen gate plus ledger/state bookkeeping
and one sentence of documentation correction. No D1 is created in this
round (the 008-d/008-e suffix renumbering is the D1 judgment already
recorded in the 008-c final-head review receipt; this order merely
executes it in documentation). No CRIT admission: the five conditions
fail at condition 1 - the human instruction of 2026-09-18 resolves the
substantive issue (observe honestly, classify precisely, separate bounded
correction order if debt persists) and the residual choices are reversible
engineering mechanics.

## Goal and dependencies

Restore the required-check state of PR #9 to all four genuinely green at
this round's final head by honest observation of the frozen full-pytest
stage (bounded, recorded reruns of the identical commit under the
unchanged 300 s cap - a green rerun of the identical commit is the
current check state and is disclosed verbatim, never manufactured),
register the round in the research ledger and machine block, correct the
stale 008-d/008-e suffix reference in current status documentation, and
publish a truthful report that additively records the 008-c final-head CI
facts and the precise classification of the inherited application-suite
timing debt. If the frozen stage still exceeds the cap at this round's
final head after the bounded observation budget, the round ends
BLOCKED with the committed per-factor decomposition and strategy
adjudicates before 008-e (a separate bounded correction order for the
inherited debt, or a pool-recovery wait - decided after this round's
evidence, not inside it).

Dependencies (all satisfied and verified): 008-a (GO evidence, pinned
candidate, frozen baseline), 008-b (consistent state, ledger pattern,
green baseline), 008-c (frozen implementation, sealed hidden set, the
one red gate to correct). No other dependencies.

## Scope

1. Reconcile current state exactly (requirement 1).
2. Bounded CI observation at the 008-c final head 4b6a90a: rerun the
   failed Application baseline job (run 35350302300) at the identical
   commit, up to 2 additional observations, each recorded verbatim
   (stage results, full-pytest session summary with pass/skip/subtest
   counts and wall time, pool date). No code change is made for this
   observation (requirement 2).
3. Data-free timing decomposition (requirement 3): locally replicate the
   driver's full-pytest stage (same workspace-copy, same uv-frozen
   environment, same command plus `--durations=40`) at 4b6a90a and
   commit one data-free JSON under
   `research/prose-boundary/results/baseline-timing/008d-decomposition.json`
   containing: total wall time, per-directory test totals
   (tests/contract, oap/tests, concept-verification/tests, research/
   tests), the top-40 slowest tests, the host/date/pool note (local host,
   not a CI runner), and the explicit statement that this is diagnostic
   measurement of an inherited suite, not a gate run. The decomposition
   is committed so strategy and the owner can classify the inherited
   debt precisely.
4. Ledger and state bookkeeping (requirement 4):
   (a) add exactly one 008-d registry entry to
       `research/registry/experiments.json` (kind `audit`, following the
       008-b-entry pattern) with: experiment_id
       `008-d-application-baseline-restoration`; question "Which of the
       four required checks was red at the 008-c final head 4b6a90a, why
       (per-head timing evidence), and how was the round corrected and
       registered without weakening, skipping, or redefining any gate?";
       frozen_choices recording new_model_calls = 0, new_science = 0,
       gate_or_test_changes = 0, cap_or_driver_or_workflow_changes = 0,
       observation_reruns_performed (per-head verbatim list per requirements 2 and 10); metrics from
       the actual committed observations (per-head full-pytest wall
       times, pass/skip/subtest counts, TIMEOUT/PASSED outcomes, the
       09-17 reference point 134.92 s, decomposition per-directory
       totals); evidence_files citing the committed
       `baseline-timing/008d-decomposition.json`, the immutable 008-c
       OAP report (sha256/size from the committed blob at 4b6a90a), the
       008-d order (committed at activation), and the 008-d-final-head
       RESEARCH-STATE.md and experiments.json blobs (byte-identical
       between implementation head and final head - the report-only
       commit changes no other path); public_report
       `research/RESEARCH-STATE.md#16`; public_metrics the committed
       decomposition; public_configuration none; source_manifest none;
       pending_evidence `["008-e: blind hidden-acceptance evaluation of
       the frozen implementation (PASS/CONDITIONAL/FAIL), naturalistic
       label adjudication per the frozen annotation guide, end-to-end
       preservation on the hidden set"]`.
   (b) update the RESEARCH-STATE.md machine block: registry_entries
       27 -> 28, oap_reports_reviewed 46 -> 47; every identity field
       unchanged (main_sha, branch, pr_number, reviewed_branch_head_sha,
       reviewed_branch_head_parent_sha, quarantined_007n, frozen 007-m
       SHAs, frozen_report_history_incidents); add one short additive
       note in the current-rounds narrative recording: the 008-c
       final-head CI truth (Application baseline full-pytest TIMEOUT at
       the frozen 300 s cap with zero test failures; the three other
       checks green), the 008-d corrective purpose, and the recorded
       renumbering (blind hidden acceptance = 008-e).
   (c) correct STATUS.md: the objective-008 paragraph's sentence
       "deferred to round 008-d" must read that the blind hidden
       acceptance and final objective-008 disposition are deferred to
       round 008-e, with round 008-d recorded as the bounded
       application-baseline timing corrective. No other semantic change
       to STATUS.md. In the same commit, update the scoped
       oap/GENERATED-FILES.json STATUS.md pin (class/sha256/bytes) per
       the 004-d mechanism and verify the OAP scoped-inventory/drift
       checks pass locally (the 008-c d0c284a defect class must not
       recur).
   (d) regenerate `research/tables/experiment-summary.csv` with
       `python3 -B -m research.tools.rebuild_tables` and verify with
       `--check`.
5. Freeze verification (requirement 5): `git diff` over the frozen
   surfaces is empty: `research/curated/`, `src/`,
   `research/prose-boundary/config/`, `research/prose-boundary/corpus/`,
   `research/prose-boundary/results/increment1|2|3/`,
   `research/prose-boundary/REPORT.md`, `research/prose-boundary/
   REPORT-008C.md`, `research/prose-boundary/adapter/`,
   `research/prose-boundary/identity/`, `research/prose-boundary/
   fixtures/`, all test files (including the 008-c focused file),
   `scripts/verify_development_baseline.py`, `.github/workflows/`.
6. Hidden-seal re-verification, data-free (requirement 6): re-hash the
   private-root hidden content against the committed
   `research/prose-boundary/corpus/manifests/hidden-manifest.json`
   (expect 4091/4091 verified; manifest sha256 still
   8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18);
   no hidden file content is read or echoed anywhere (counts/hashes
   only). Any mismatch: STOP and report BLOCKED (seal contract).
7. Local verification (requirement 7): full research suite with the
   pinned helper present (the e2e invariant re-derivation passes
   locally before commit), the OAP suite (including the scoped
   inventory/drift and B10 checks), publication guard, whitespace check,
   and one full local Application-baseline driver run (recorded
   per-stage durations; a local full-pytest wall time is recorded as
   local evidence only and is never claimed as a CI observation).
8. Implementation head, push, and CI (requirement 8): commit the
   bookkeeping, push; at the implementation head the designed
   pre-report count assertion is red in BOTH Research reproducibility
   and the Application baseline full-pytest (machine block 47 vs 46
   report files in the tree) - the 008-b/008-c designed precedent,
   exactly one failing test (test_research_state_consistency), no other
   failures; if the full-pytest stage instead records TIMEOUT at the 300
   s cap with zero test failures, apply the bounded rerun observation
   (up to 3 additional observations at this head, recorded verbatim).
   The implementation head is recorded literally in the report.
9. Report-only final commit (requirement 9): one commit with the
   literal implementation head as sole parent and
   `oap/reports/008-d-application-baseline-restoration.md` as the sole
   changed path; push; verify remote PR head, exact report bytes,
   parent, and changed-path invariant; send response OK.
10. Final-head CI (requirement 10): all four required checks green at
    the final head. If the full-pytest stage at the final head records
    TIMEOUT at the 300 s cap with ZERO test failures (the pool-variance
    failure class), apply the bounded rerun observation (up to 3
    additional observations at the identical final head, each recorded
    verbatim with session summary and wall time); a green rerun of the
    identical commit is the current check state (GitHub required-check
    semantics track the latest run) and is disclosed verbatim in the
    report - it is an honest observation of a stochastic runner pool,
    never a manufactured or weakened check. If the stage is still red
    after the observation budget: publish the report with
    `Result: BLOCKED`, the committed decomposition, the verbatim
    observations, and the explicit predeclared stop - do not chase
    further reruns, do not change any gate; strategy adjudicates before
    008-e. Any full-pytest failure showing a genuine test failure (a
    nonzero failure count other than the designed pre-report count
    assertion at the implementation head) is a DIFFERENT failure class:
    STOP, preserve evidence, report BLOCKED with the failing test named
    - it is not pool variance.

## Non-goals

- No change to the 300 s per-command cap, the baseline driver
  (`scripts/verify_development_baseline.py`), any workflow file, or any
  other gate definition.
- No change to any test file (no edits, no additions, no skips, no
  deletions); the full-pytest population is identical to the 008-c
  final head.
- No change to `research/curated/`, `src/`, the 008-c implementation,
  the 008-a baseline, the committed corpus, configs, or the hidden
  manifest; no hidden-set evaluation or regeneration (008-e's scope).
- No 007-m linguistic change (detector, ranking, candidate semantics,
  validator prompt/parser, acceptance, reasoning settings); no
  linguistic benchmark artifact change.
- No model calls of any kind (the 008-c generation program is complete;
  its 414 disclosed attempts are closed); no new data acquisition.
- No objective-009 data of any kind; 009 remains reserved.
- No merge, no auto-merge, no force-push, no rewrite of any immutable
  order, report, or the 008-c report in particular.
- No fix of the inherited application-suite performance debt in this
  round: it is classified precisely (requirement 3) and any correction
  is a separate bounded order proposed after this round's evidence.
- No CRITICAL append or mitigation update.

## Files and boundaries

Inspect (read-only): `oap/orders/008-c-parser-first-protection.md` and
`oap/reports/008-c-parser-first-protection.md` (immutable references);
`scripts/verify_development_baseline.py` (frozen driver contract,
including DEFAULT_COMMAND_TIMEOUT = 300.0); `.github/workflows/*.yml`
(frozen); `research/tests/*` (frozen, byte-identical check);
`research/prose-boundary/results/increment3/e2e-invariants.json`
(committed dev-evidence reference); `research/prose-boundary/
corpus/manifests/hidden-manifest.json` (seal reference);
`research/RESEARCH-STATE.md`, `research/registry/experiments.json`,
`research/tables/experiment-summary.csv`, `STATUS.md`,
`oap/GENERATED-FILES.json` (bookkeeping targets); private
`workorders/008-c-final-head-review-20260918.md` (review basis);
`workorders/consumed.json` and the FIFO state (reconciliation).

Modify (only these): `oap/orders/008-d-application-baseline-
restoration.md` (new, activation commit); `oap/active` (-> 008-d);
`research/prose-boundary/results/baseline-timing/008d-decomposition.json`
(new data-free); `research/registry/experiments.json` (append exactly one
008-d entry); `research/RESEARCH-STATE.md` (machine block 27->28 and
46->47 plus the one additive note); `STATUS.md` (the one sentence
correction); `oap/GENERATED-FILES.json` (the STATUS.md pin entry only);
`research/tables/experiment-summary.csv` (rebuild_tables output);
`oap/reports/008-d-application-baseline-restoration.md` (new, report-only
commit).

## Requirements

1. Reconcile: `oap/active` = 008-d after activation; remote branch head
   == 4b6a90ab13c0c9a02e533a2673a084e26f841a5c before any push; PR #9
   open/unmerged with auto-merge disabled; local worktree at 4b6a90a
   plus untracked residue only; verify the frozen surfaces of scope item
   5 are byte-identical to base (git diff empty) BEFORE any commit; no
   other concurrent mutation.
2. Bounded CI observation at 4b6a90a: rerun the failed Application
   baseline job (`gh run rerun 35350302300 --failed`, then up to 1
   further rerun if the first rerun is red), each observation recorded
   verbatim in the report evidence (run id, stage results, full-pytest
   session summary with pass/skip/subtest counts and wall time). This
   is observation only: no commit, no code change. If the first rerun is
   green, the second is not performed (budget spent: max 2 observations).
3. Data-free timing decomposition at 4b6a90a locally (diagnostic, not a
   gate run): replicate the driver's full-pytest stage (workspace copy
   with the same ignore rules, uv-frozen sync, identical pytest command
   plus `--durations=40`, the driver's environment including
   OAP_FORWARD_RECOVERY_HISTORY_SOURCE), then commit
   `research/prose-boundary/results/baseline-timing/008d-decomposition.json`
   (schema-free but containing at minimum: order 008-d, label
   "diagnostic measurement of the inherited full-pytest population, not
   a gate run", host date and that the host is the local development
   machine not a CI runner, total wall time, per-directory totals for
   tests/contract, oap/tests, concept-verification/tests, research/tests
   with test counts and seconds, top-40 slowest tests by name and
   seconds, and the 09-17/09-18 CI reference points quoted verbatim).
   The file is data-free (no private text, no customer data).
4. Bookkeeping exactly per scope item 4 (a)-(d): one 008-d registry
   entry (byte-stable JSON, inserted in chronological position after the
   008-c entry); machine block registry_entries 27 -> 28 and
   oap_reports_reviewed 46 -> 47 with every other machine-block field
   unchanged; the one additive RESEARCH-STATE note; the one STATUS.md
   sentence correction with the scoped pin updated in the same commit
   (OAP scoped-inventory/drift checks green locally, 164/164 inventory
   entries match); CSV is the byte-identical rebuild_tables output
   (`--check` passes).
5. Freeze verification after the bookkeeping commit and again before the
   report-only commit: git diff base..HEAD empty over every frozen
   surface in scope item 5; the 008-c OAP report blob byte-identical;
   the two frozen report-history incidents intact (report history
   check green locally).
6. Hidden-seal re-verification data-free per scope item 6 (4091/4091;
   manifest sha256 unchanged; zero hidden content reads; any mismatch
   STOP/BLOCKED).
7. Local verification: full research suite with the pinned helper
   present (280+ tests OK, including the e2e invariant re-derivation and
   the 007-o consistency test at the pre-report red state - i.e. the
   consistency test fails locally ONLY on the designed count assertion
   until the report commit; verify that exactly that single assertion
   fails locally at the implementation head); OAP suite green (B10
   included); publication guard PASS; whitespace PASS; one full local
   Application-baseline driver run with per-stage durations recorded in
   the report (local full-pytest wall time recorded as local evidence
   only).
8. Push the implementation head (activation commit + bookkeeping
   commit); record the literal implementation head SHA; observe CI at
   the implementation head and record it verbatim. Expected red state
   (the 008-b/008-c designed precedent): the single designed pre-report
   count assertion failing in Research reproducibility and in the
   Application baseline full-pytest (machine block 47 vs 46 report
   files in the tree); on a slow pool the full-pytest stage may
   additionally record TIMEOUT at the 300 s cap with the session
   showing exactly that one designed failure. NO rerun is performed at
   the implementation head: a green is impossible by design before the
   report-only commit. Any additional genuine test failure beyond the
   single designed count assertion is a STOP/BLOCKED event with the
   failing test named (not pool variance).
9. Report-only commit per scope item 9; remote invariants verified
   (verify_report remote=verified, including exact report bytes and
   parent/changed-path); the report contains every mandatory field
   (Result; order identity/hash; PR mode/number/URL/state; branch/base
   and starting remote SHA; implementation head SHA; report publication
   commit SELF; per-criterion evidence; each command/check with
   PASSED/FAILED/TIMEOUT/PENDING/NOT RUN and tested SHA; negative-path
   evidence; setup/resource/privacy evidence; Critical action NONE;
   limitations; no-merge confirmation) and the documentation-section
   content; `publication_verified: false` before its own push per
   P-SELF-03.
10. Final-head CI per scope item 10 (all four green at the final head,
    with the bounded verbatim rerun observation for the zero-failure
    TIMEOUT class; predeclared BLOCKED stop after the budget; any
    genuine test failure is a STOP/BLOCKED with the failing test named).
    After final-head CI settles, re-verify the remote PR head still
    equals the report-only commit (a changed head voids the review and
    requires reconciliation, not a silent acceptance).
11. Send exact response OK after remote verification and stop. PR #9
    remains open and unmerged.

## Acceptance criteria

1. At the final head, either: all four required checks green (with
   every rerun observation disclosed verbatim) - the success state; or
   Result: BLOCKED with the committed decomposition, verbatim
   observations, and the predeclared stop - the permitted failure
   state. No third state is acceptable.
2. git diff base..final empty over every frozen surface of scope item 5
   (no test, gate, driver, workflow, implementation, corpus, config,
   manifest, or 008-a baseline change); the full-pytest population is
   byte-identical to the 008-c final head.
3. Registry holds exactly 28 entries; the 008-d entry follows the 008-b
   pattern (kind audit; evidence files' sha256/size matching committed
   blobs; pending_evidence naming 008-e); machine block registry_entries
   = 28 and oap_reports_reviewed = 47 with every identity field
   unchanged; CSV byte-identical rebuild output; the 007-o consistency
   test green at the final head.
4. Report-only commit invariants verified remotely (parent = literal
   implementation head; sole changed path = the 008-d report; exact
   bytes).
5. STATUS.md carries exactly the one sentence correction (008-d/008-e
   suffix truth); the scoped GENERATED-FILES.json STATUS.md pin updated
   in the same commit; OAP scoped-inventory/drift checks green.
6. Hidden seal re-verified data-free (4091/4091; manifest sha256
   8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18
   unchanged; zero content reads).
7. Zero model calls; zero 009 data touched; zero linguistic-method
   changes; the 008-c report and all prior immutable reports
   byte-identical; no merge/auto-merge; PR #9 open/unmerged; main
   unchanged at 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9.
8. Every CI observation (original runs, every rerun, at both heads)
   recorded verbatim with run ids, stage results, session summaries,
   and wall times; the report distinguishes the zero-failure TIMEOUT
   class from genuine test failures explicitly.
9. The decomposition JSON is committed, data-free, and matches the
   report's quoted numbers.
10. The report makes no milestone, release, deployment, or linguistic-
    acceptance claim, and states explicitly that 008-e (blind hidden
    acceptance) and objective 009 remain reserved against the frozen
    implementation.

## Verification

Focused: `python3 -B -m research.tools.rebuild_tables --check`;
`research/tests/test_research_state_consistency.py` at the implementation
head (expected: exactly the single designed count-assertion failure) and
at the final head (green); the OAP suite (B10, scoped inventory/drift,
transcript, report history) green locally; git diff freeze checks (scope
item 5) at the implementation head and before the report-only commit;
hidden-manifest data-free re-hash (4091 files). Broader: the full
research suite with the pinned helper present (280+ tests OK, e2e
re-derivation); one full local Application-baseline driver run (all
stages, per-stage durations recorded; local wall times are local
evidence only). Remote: `verify_report` (local before push, remote after
push); `gh pr checks 9` at the implementation head and the final head;
`gh run view <id> --log-failed` for every observed full-pytest session
(verbatim capture of the driver JSON summary line). Negative paths: a
frozen-surface diff -> STOP/violation; a hidden-manifest mismatch ->
STOP/BLOCKED (seal voided, recorded); a full-pytest observation showing
genuine test failures -> STOP/BLOCKED with the failing test named (NOT
pool variance); a rerun budget exhausted with the stage still red ->
predeclared BLOCKED stop, no further chasing, no gate change; an
implementation-head CI showing more than the single designed count-
assertion failure -> STOP/BLOCKED.

## Local setup and constraints

CPU-only. No Rust toolchain work is required in this round (no helper
rebuild; the pinned helper is only exercised by the local research suite
for the e2e re-derivation, presence verified by sha256 against
5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf).
Local long runs use the persistent temp parent convention (never /tmp
for the baseline driver). No network beyond normal GitHub publication
and the bounded `gh run rerun` observations (no new endpoints, no
generation calls, no other model calls). No private customer data
anywhere; the decomposition JSON is data-free; private absolute paths
stay out of committed documents. The private-root hidden set is accessed
manifest-hash-only (data-free re-verification), never content-read.

## Documentation

The OAP report `oap/reports/008-d-application-baseline-restoration.md`
must state: (1) the round purpose and that it completes the 008-c
report's deferred final-head CI truth additively (the 008-c report is
never edited); (2) the verbatim per-head CI record - the original
observations at 4b6a90a (run 35350302300: 653 passed / 14 skipped / 89
subtests / 0 failures / 337.20 s / TIMEOUT at the 300 s cap; the three
green runs 35350302302/35350302411) and every bounded rerun observation
at both heads (run id, session summary, wall time, pool date); (3) the
pool-variance analysis with the verified reference points (134.92 s at
8300573 on the 2026-09-17 pool; 329.96 s at 21c4135, 337.06 s at
9aec9cb, 337.20 s at 4b6a90a on the 2026-09-18 pool; 334.87 s at
d0c284a per the 008-c final-head review receipt) and the explicit
statement that the 008-c round's only population change is the single
new focused test file; (4) the committed data-free decomposition
(per-directory totals, top-40 slowest, host note) and the precise
classification: inherited application-suite timing debt amplified by
runner-pool variance against a frozen 007-era 300 s per-command cap -
not a 008-caused test failure, not a 008-c defect; (5) the explicit
statement that the cap, the driver, the workflows, and every test file
are byte-unchanged (no gate weakened, skipped, or redefined); (6) the
proposed separate bounded correction path for the inherited debt
(classification plus the candidate options for strategy/owner
consideration after this round - e.g. a separate bounded order for the
cap or for the app-suite performance, decided on this round's evidence -
NOT executed in this round); (7) the recorded renumbering (blind hidden
acceptance = 008-e, per the D1 recorded in the 008-c final-head review);
(8) the registry/machine-block/CSV/STATUS/pin updates with their
mechanics (including the designed pre-report count-assertion red at the
implementation head and its green at the final head, the 008-b/008-c
precedent); (9) the hidden-seal re-verification result (4091/4091, data-
free); (10) the explicit statements: no milestone, release, deployment,
or linguistic acceptance is made or implied; PR #9 remains open and
unmerged; 008-e and objective 009 remain reserved against the frozen
implementation; no model calls were made in this round.

RESEARCH-STATE.md carries the one additive note (scope item 4b).
STATUS.md carries the one sentence correction (scope item 4c). No other
documentation file is touched.

## Git and report publication

AMEND_EXISTING_PR on `oap/008-prose-boundary-qualification` (PR #9),
base 4b6a90ab13c0c9a02e533a2673a084e26f841a5c. Commit boundaries
(suggested): (1) order + active activation; (2) decomposition artifact +
bookkeeping (registry, RESEARCH-STATE machine block and note, STATUS.md +
scoped pin, CSV); (3) report-only commit (sole parent = the literal
implementation head from commit 2; sole changed path
`oap/reports/008-d-application-baseline-restoration.md`). Push after
each; verify remote head after the final push; verify report bytes,
parent, and changed-path invariant remotely; send exact response OK;
stop. No merge, no auto-merge, no force-push, no subsequent push for
this round after the report-only commit.

## Decision classification

D0 overall: bounded, reversible CI observation plus ledger/state
bookkeeping and one sentence of documentation correction, all inside the
architecture and risk budget. The bounded-rerun-observation mechanic is
routine CI practice (the 008-c round already performed one rerun at
4b6a90a; GitHub required-check semantics track the latest run of the
identical commit; every observation is disclosed verbatim, so no green
status is manufactured - the report shows exactly which run, at what
wall time, on what pool date, produced the green). The choice to commit
a data-free decomposition artifact and its path is routine reversible
engineering. No new D1 judgment is created (the suffix renumbering is
the already-recorded D1 of the 008-c final-head review). Five-condition
CRIT admission: not triggered - condition 1 fails because the human
instruction of 2026-09-18 resolves the substantive path (observe
honestly; classify precisely; separate bounded correction order if the
debt persists; pool-recovery wait as the alternative), leaving only
reversible mechanics; the residual risk (the inherited app-suite timing
debt may make the frozen cap flaky for subsequent rounds) is recorded in
the report and is owned by the strategy adjudication after this round,
not by a provisional product choice.

## Deferred human adjudication
- Decision: NONE

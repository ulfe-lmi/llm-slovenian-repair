# Work order 007-n — Restore the deterministic Application baseline

Status: FINAL

```oap-metadata
{
  "id": "007-n",
  "title": "Restore the deterministic Application baseline",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": ["007"],
  "local_work": "Canonical active/order/report and local branch ref are at remotely verified 007-m report head e20819ace916ed4e619270cc0c72baad9c7a7274. Preserve every 007-a through 007-m artifact, all private experiment roots, any unrelated local work, and the owner-abandoned environment residue. Git worktree/history traversal on the sync filesystem can block; use the existing native cache/temp conventions and do not clean, reset, stash, or rewrite around it.",
  "prior_review": "Strategic review remotely verified the 007-m SELF report and accepted its bounded scientific result as a conservative same-sample tradeoff, not linguistic or product acceptance. Research reproducibility, OAP bootstrap acceptance, and OAP report history pass at e20819a. Required Application baseline fails in full pytest at the terminal-SSE no-EOF test; independent exact-head repetition reproduced the timeout on iteration 4. Direct mypy then confirms the latent 11 verify_source_artifact.py errors. PR #8 is OPEN/UNMERGED and 007-n is unused.",
  "provenance": [
    {"kind":"E","reference":"GitHub Actions run 34789634104, job 103811343705 at e20819ace916ed4e619270cc0c72baad9c7a7274 fails required Application baseline in ConceptTests.test_proxy_stops_at_terminal_event_without_eof; later job steps are skipped."},
    {"kind":"I","reference":"Private strategic review receipt logs/007-m-strategic-review-20260914.md records remote report verification, three green required checks, exact-head iteration-4 reproduction, the earliest response-capture boundary, and the separate 11-error mypy observation."},
    {"kind":"A","reference":"S-EVIDENCE-01, S-DIAGNOSE-01, S-ORDER-03 and the 007-m required_checks field require boundary-faithful repair on the same objective branch/PR before any development merge."}
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
  "lr": ["LR-001", "LR-007", "LR-008", "LR-011", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Corrective round 007-n amends existing objective 007, branch
`oap/007-concept-verification`, and PR #8. It creates no new PR and does not
advance to objective 008. Ordinary implementation iteration remains 007-n.

## Provenance

This order is driven by observed final-head CI and an independent exact-head
reproduction, not adjacent cleanup. The required Application baseline cannot
become green until both the reached intermittent pytest boundary and the already
confirmed later mypy boundary are repaired.

## Current verified state

At 2026-09-14T18:05:03+02:00, remote `main` is
`ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #8 is open and unmerged at
`e20819ace916ed4e619270cc0c72baad9c7a7274`, mergeable with state `unstable`.
The 007-m report is remotely verified: its only changed path is the exact report,
its sole parent is implementation head `1a67adf80a679489288c39998cc41974f0c21d8e`,
and report history is valid with the two frozen historical incidents. CRITICAL
contains no entries or dispositions. No 007-n order/report exists remotely.

The final-head required checks are Research reproducibility PASSED, OAP bootstrap
acceptance PASSED, OAP report history PASSED, and Application baseline FAILED.
The latter stops during full pytest at a repeatable terminal-SSE timeout. A direct
exact-head mypy run reports 11 errors in `scripts/verify_source_artifact.py` from
one loop variable being inferred as both `stat_result` and `ZipInfo`.

## Governance

S-AUTH-01, S-STATE-01, S-ORDER-01 through S-ORDER-03, S-EVIDENCE-01,
S-DIAGNOSE-01, S-PROTOCOL-01 and S-REVIEW-01 govern. LR-001/LR-011 require a
bounded complete-response capture result rather than waiting for upstream EOF;
LR-007/LR-008/LR-013 preserve data, evidence, and privacy semantics. This is a
D0 correctness/evidence repair. It introduces no judgment debt and grants no
live-test, milestone, merge, release, or deployment authority.

## Goal and dependencies

Make the required Application baseline deterministic and green at the final PR
head by correcting the reached buffered-response capture race and the separate
latent mypy naming/type defect, without changing 007-m research semantics or any
protected boundary.

## Scope

Repair the no-EOF terminal-SSE read behavior in the existing concept proxy and
add deterministic regression coverage at the real response-capture seam. Repair
the `verify_source_artifact.py` static typing defect without changing its ZIP
validation behavior. Run focused, broader, governance, privacy, and final-head
CI verification. Publish one truthful immutable 007-n report.

## Non-goals

No change to 007-m ranking, metrics, datasets, private roots, observations,
prompts, model requests, corpus/index, research configuration/results/reports,
gateway, API contract, dependencies, CI timeouts/workflow semantics, accepted
governance, protected Qwen/vLLM/CUDA/service/network state, live repair testing,
new experiment, resampling, objective 008, PR merge, release, or deployment.
Do not mask the race by increasing sleeps/timeouts, retrying requests, marking
the test flaky, weakening assertions, excluding files from mypy, adding broad
`type: ignore`, or skipping the required baseline.

## Files and boundaries

- `concept-verification/proxy.py` and
  `concept-verification/tests/test_concept.py`: terminal-event capture and
  actual proxy integration.
- `scripts/verify_source_artifact.py` and
  `tests/contract/test_objective_005.py`: distinct filesystem/ZIP member types
  and unchanged artifact/ZIP safety gates.
- `scripts/verify_development_baseline.py`, the four CI workflows/checks, and
  relevant OAP helpers: verification only unless a demonstrated in-scope defect
  makes a minimal edit necessary.
- Exact 007-n order/active/report paths. Do not mutate any earlier order/report.

## Requirements

1. Reconcile exact active 007-n, remote main, branch/PR/head, the verified 007-m
   parent report, and all local work before mutation. Reuse PR #8. If remote head
   changed or 007-n already exists, stop mutation and report the conflict.
2. Preserve the 007-m implementation, data-free public projections, aggregate
   claims, private evidence, and no-resample state byte-for-byte. No model or
   network request may be made by this round except normal GitHub publication.
3. Reproduce or directly model the earliest SSE failure before fixing it. Test
   the material hypothesis that `http.client.HTTPResponse` can already contain
   body bytes in its buffered reader while readiness polling only the underlying
   raw socket waits until timeout. Record evidence that distinguishes this from
   slow server startup, missing terminal bytes, client timeout, or EOF handling.
4. Correct `_bounded_read` so it consumes already buffered response bytes and
   terminates promptly on one fully delimited `response.completed` event even
   when the HTTP/1.1 connection stays open. Preserve the absolute deadline,
   byte bound, explicit SSE-completion requirement, incomplete-stream failure,
   malformed-event failure, and ordinary finite-body behavior. Do not depend on
   a longer test sleep/timeout or an automatic request retry.
5. Add a deterministic regression that would fail under raw-socket-only
   readiness while the terminal event is already buffered. Retain an actual
   loopback proxy test proving response status/body delivery before EOF. Negative
   tests must prove incomplete, malformed, over-bound, and timed-out streams do
   not become successful complete responses, and that threads/sockets terminate.
6. Demonstrate stability with at least 25 consecutive executions of the formerly
   flaky focused integration test at the implementation head. One failure is a
   failed criterion; do not select only passing attempts.
7. Repair all 11 observed mypy errors in `scripts/verify_source_artifact.py` by
   keeping filesystem metadata and `ZipInfo` member metadata under distinct,
   correctly typed names or an equivalently narrow typed structure. Preserve
   descriptor/no-follow checks, regular-file validation, hashing, member-name,
   duplicate, symlink, nonregular, encryption, size, total-size and compression
   ratio rejection behavior. Do not silence or remove the checks.
8. Run the focused ZIP verifier contract tests and mypy. The exact command
   `mypy src tests/contract` must report zero errors without new ignores or
   exclusions, and every existing objective-005 ZIP negative must still pass.
9. Run the real `scripts/verify_development_baseline.py` entry point with its
   native temp/cache boundary. It must complete every stage, including full
   pytest, Ruff, mypy, build/sdist/wheel/install/import/CLI checks and cleanup,
   with result PASSED. Do not substitute component commands for this criterion.
10. Re-run the 222-test research suite, deterministic table check and 151-file
    publication guard to prove the corrective round did not alter research or
    leak private data. Run normal OAP transcript/governance/report-history,
    whitespace/protected-source and Git integrity checks.
11. Push all non-report work and wait for the implementation-head required
    checks. All four named checks must be present and green before composing the
    immutable report. A missing, pending, cancelled, skipped or failed check is
    not green; repair only a demonstrated in-scope failure.
12. Publish one final report-only 007-n commit with its literal implementation
    head as sole parent and only the matching report path changed. Verify remote
    head, report bytes, parent and changed-path invariant, then send response OK
    and stop. PR #8 must remain open and unmerged for strategic review.

## Acceptance criteria

1. The formerly flaky terminal-SSE integration path passes 25 consecutive runs,
   and deterministic boundary coverage proves buffered terminal data is consumed
   without EOF while invalid/incomplete/oversized/timed-out streams still fail.
2. All 11 `verify_source_artifact.py` mypy errors are removed through a narrow
   type-correct repair with all ZIP security and integrity tests unchanged or
   strengthened.
3. The actual Application baseline driver passes every stage, research/OAP/
   privacy regression evidence passes, and all four required GitHub checks are
   green at the pushed implementation head.
4. The final 007-n report is remotely verified under SELF; PR #8 remains open,
   unmerged, and contains no unrelated or protected-boundary change.

## Verification

Focused commands must include the single terminal-SSE test repeated 25 times,
its deterministic buffered-reader negative/positive tests, objective-005 ZIP
contract tests, and `mypy src tests/contract`. Broader commands must include the
real development-baseline driver, research suite/table/privacy guard, OAP suite,
transcript/governance/report-history, protected-source/whitespace checks,
`git diff --check`, and `git fsck --full --no-reflogs`. Record each result and
tested SHA separately. Expected final-head GitHub checks are exactly Application
baseline, Research reproducibility, OAP bootstrap acceptance, and OAP report
history.

## Evidence boundary and negative paths

The deterministic response-reader regression must exercise the buffering/readiness
boundary under claim; a fake that removes `HTTPResponse` buffering cannot prove
the defect closed. The loopback proxy test must exercise the actual `ConceptProxy`
request path. ZIP tests must exercise `_verify_artifact_entry` and its actual file
descriptor/archive parser boundary. Offline tests and green CI do not establish
live Qwen compatibility, linguistic benefit, ICA, milestone acceptance, release,
or deployment authorization.

## Local setup and constraints

Source `scripts/project_env.sh` or apply its documented native cache/temp settings.
Resolve routine package/test setup without human terminal work. Use only synthetic
test payloads and owned disposable fixtures. Do not display or persist credentials,
raw private experiment content, targets, prompts, responses, endpoints, or private
root paths. Do not touch the protected GPU/model/service/network environment.
`REPAIR_ALLOW_LIVE_TESTS` remains NO.

## Documentation

Update only comments or development/testing documentation whose existing claim
would otherwise become false. Do not alter 007-m scientific reports/results or
inflate product/readiness language. The 007-n report must state that this closes
a development CI/capture reliability gate only.

## Git and report publication

Start from verified PR #8 head `e20819ace916ed4e619270cc0c72baad9c7a7274`
on the same branch. Preserve history and unrelated work; no reset, clean, stash,
force-push, new PR, merge, auto-merge, release, or deployment. Commit/push all
implementation, tests, order and active-pointer changes before the report. The
report records literal implementation head and `Report publication commit: SELF`,
then its final commit changes only
`oap/reports/007-n-restore-deterministic-application-baseline.md`. Verify it
remotely and send exact response `OK` only after publication is durable.

## Decision classification

D0. Both defects are ordinary, reversible, bounded correctness/evidence failures
with directly observed negative paths. They do not satisfy the five-condition
D1 threshold and do not authorize any D2 action.

## Deferred human adjudication

- Decision: NONE

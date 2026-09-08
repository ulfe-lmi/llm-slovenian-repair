# Work order 004-e — Stabilize disposable Git teardown

Status: FINAL

```oap-metadata
{
  "id": "004-e",
  "title": "Stabilize disposable Git teardown",
  "objective": "004",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 5,
  "dependencies": ["000", "001", "002", "003"],
  "local_work": "Clean objective branch at remote 004-d report head 84e3e7cbaf4d4f613bac0d238db1100b708696a2; preserve all objective history, ignored environments and private strategic state.",
  "prior_review": "004-d product semantics and root import probes pass, but repeated required CI failures in unrelated OAP TemporaryDirectory teardown make PR #5 unmergeable despite same-SHA retries.",
  "provenance": [
    {"kind": "E", "reference": "Runs 34197187586, 34198301076, 34201554086 and 34202726494 failed nondeterministically after passing test bodies when cleanup removed disposable .git; failures moved among transcript, fake-GitHub and lock tests and some same-SHA reruns passed"},
    {"kind": "I", "reference": "Earliest shared boundary is oap_core.git used by all disposable repos plus unretired TemporaryDirectory cleanup; helper sets GIT_OPTIONAL_LOCKS=0 but does not disable automatic detached Git maintenance"},
    {"kind": "A", "reference": "S-EVIDENCE-01/S-DIAGNOSE-01 and OAP required-final-head green-check gate; test fixtures must clean owned state without masking persistent leaks"}
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
  "lr": ["LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

004-e is a corrective round on existing objective branch/PR #5. It addresses a
recurrent required-check fixture teardown failure discovered during 004-c/d review.
Preserve every prior order/report/failed check and same-SHA rerun; do not amend history.

## Provenance

- E: four hosted runs failed after test bodies, always `OSError: [Errno 39]
  Directory not empty: .git` in `TemporaryDirectory.cleanup()`, but in different
  unrelated tests. Same-SHA reruns sometimes passed. Product checks were green.
- I: all failing fixtures create disposable Git repositories through shared
  `oap_core.git`; teardown immediately recursively removes them. The helper waits for
  foreground Git but does not disable automatic maintenance/detachment.
- A: required CI must be meaningful and stable. A narrow retry may tolerate filesystem
  retirement latency, but must be bounded and re-raise persistent/non-ENOTEMPTY errors.

## Current verified state

Accepted main remains `dac4789f52c9e82aec90d1cf92ce9f1194cc103a`. PR #5 is sole
open PR at remote 004-d SELF head `84e3e7cbaf4d4f613bac0d238db1100b708696a2`,
implementation parent `8207e7e147ca9e7c80d81cbd28858d3dc8d97adb`. Remote report,
transcript, governance and active `004-d\n` verify. Final OAP passed, but final
Application baseline failed only at embedded OAP cleanup after all product stages.

004-d manifest and lazy-root direct probes pass. CRITICAL is empty. Branch protection
is disabled/rulesets empty; no setting change authorized. No merge/live/release action.

## Governance

Preserve product and governance bytes. Fix the test infrastructure at its shared Git/
cleanup boundary; do not weaken assertions, ignore cleanup errors, delete arbitrary
paths or label failed attempts passed. D0/NONE.

## Goal and dependencies

Eliminate detached Git writers from OAP helper invocations and make owned test-fixture
retirement tolerate only short transient ENOTEMPTY races while still failing persistent
leaks. Prove with focused deterministic tests, repeated affected tests and fresh CI.

## Scope

1. Configure shared `oap_core.git()` subprocesses to disable automatic/detached Git
   maintenance without persistent repository/global configuration.
2. Add one shared bounded cleanup helper for owned OAP TemporaryDirectory fixtures and
   use it in Acceptance/Processes and TranscriptGuard teardown.
3. Add focused unit/process tests for command configuration and cleanup retry semantics.
4. Run bounded stress repetitions plus complete suites; update direct runbook/docs only
   if test-fixture behavior needs explanation.
5. Publish exact 004-e order/active/report on PR #5.

## Non-goals

No product/manifest/fixture-data/root-import/dependency/governance/CRITICAL changes.
No blanket ignore_errors, unbounded retry/sleep, broad OSError suppression, repository
cleanup, global Git config, GitHub setting, workflow weakening, check removal, live
model, corpus access, merge, release or deployment.

## Files and boundaries

Expected paths: `oap/bin/oap_core.py`, `oap/tests/support.py`,
`oap/tests/test_acceptance.py`, `oap/tests/test_transcript_guard.py`, focused OAP tests
and exact generated inventories if required, plus 004-e protocol files. Avoid product
source/tests/docs unless exact inventory tooling requires no-op confirmation.

The boundary is real Git subprocess invocation and real owned TemporaryDirectory
cleanup. Fakes may inspect argv/config but at least one real disposable Git stress test
must create/commit/retire repositories.

## Requirements

1. Every `oap_core.git()` command passes nonpersistent command-scoped settings before
   the subcommand to disable automatic background maintenance: at least `gc.auto=0`,
   `maintenance.auto=false`, and `gc.autoDetach=false` (or an equally explicit tested
   combination). Preserve argument arrays, `-C`, timeout, captured output, environment
   isolation and existing return/error semantics. Do not write local/global config.
2. Add a narrowly named cleanup helper accepting an owned `TemporaryDirectory`.
   Attempt ordinary cleanup first. Retry only `OSError` with `errno.ENOTEMPTY`, using a
   small fixed maximum (at most 10) and short fixed delay (at most 100 ms). Re-raise all
   other errors immediately and re-raise ENOTEMPTY after exhaustion. Never accept an
   arbitrary path, shell out, use recursive ignore-errors or leave success unverified.
3. Use the helper in the common Acceptance teardown inherited by Processes and in
   TranscriptGuard teardown. Preserve environment-patch stop order and ensure cleanup
   success means the temporary root no longer exists.
4. Unit tests inspect the actual Git invocation to prove settings precede subcommand
   and caller args remain exact. Verify no repository/global config bytes are changed.
5. Cleanup tests use a controlled fake TemporaryDirectory cleanup method: immediate
   success; two ENOTEMPTY failures then success with exact bounded calls; non-ENOTEMPTY
   immediate propagation; and exhaustion propagation. Do not depend only on timing.
6. Add a real disposable-Git stress proof that repeatedly initializes/commits through
   the shared helper and retires the owned directory. Repeat the three historically
   failing tests or their exact classes at least 20 iterations total in fresh processes.
   No surviving fixture process/path may remain.
7. Run the complete OAP suite at least twice consecutively at the implementation head,
   plus native application baseline and product tests once. Record each run separately;
   one pass does not erase historical failures.
8. Preserve all 004-c root-import and 004-d manifest semantics. Direct probes still
   reject rights/encoding/media aliases and bare source/wheel import stays dependency-
   lazy. Product fixture SHA/size remain unchanged.
9. Required CI must pass on the implementation head without manual rerun before report
   publication. If either initial attempt fails, diagnose and correct in the same round
   or report truthfully; do not use a retry as sole closure evidence.
10. Force-stage exact `004-e\n`, preserve prior history, and make matching report the
    sole final commit. Final-head checks must later pass without manual rerun before
    strategic merge review.

## Acceptance criteria

1. Git helper settings and cleanup retry/propagation tests pass at the real boundaries;
   persistent leaks remain failures.
2. At least 20 targeted disposable-fixture iterations and two full OAP suite runs pass
   with all roots retired, followed by a complete native baseline pass.
3. Root import and strict manifest direct regressions remain green; no product bytes or
   fixture SHA/size changed in 004-e.
4. Both required implementation-head and final-report-head checks pass on their first
   attempts at each SHA. Historical failed/rerun evidence remains disclosed.
5. PR #5 stays open/unmerged during coding; remote SELF verifies. Branch settings,
   live/model/corpus/release/deployment boundaries remain unchanged.

## Verification

Run/report exact focused tests chosen for new helper behavior, targeted stress command,
and:

```text
python3 -B -m unittest discover -s oap/tests -v
python3 -B -m unittest discover -s oap/tests -v
pytest tests/contract/test_objective_001.py -q
pytest tests/contract/test_objective_004.py -q
pytest -q
ruff check src scripts tests
mypy src tests
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-e
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-e
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a
git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD
git diff --exit-code dac4789f52c9e82aec90d1cf92ce9f1194cc103a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After report publication strategy verifies SELF, first-attempt final CI, full diff,
direct root/manifest probes and strongest merge objection. This remains test/process
evidence, not linguistic/live/milestone/release proof.

## Local setup and constraints

Owned `/tmp` fixtures and frozen lock only. Cleanup targets must derive from
TemporaryDirectory objects, never broad paths. No global/local Git config writes or
repository `.venv`. No secrets/private/customer/model/corpus data.

## Documentation

Record the recurrent teardown diagnosis, command-scoped Git controls, bounded retry,
stress counts and remaining uncertainty. Do not claim proven causality beyond evidence.

## Git and report publication

Stay on existing branch/PR #5 and preserve all commits through `84e3e7c`. Commit/push
non-report changes/order/active, require first-attempt implementation CI, record SHA,
then create only `oap/reports/004-e-stabilize-disposable-git-teardown.md` as SELF
report-only commit. Push, remotely verify, send exact `OK`, exit. Do not merge.

## Decision classification

D0. This is bounded deterministic test-process stabilization after repeated evidence;
no human intent, production or external authority is selected.

## Deferred human adjudication
- Decision: NONE

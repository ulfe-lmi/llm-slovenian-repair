# Work order 001-b — Native environment and offline runtime closure

Status: FINAL

```oap-metadata
{
  "id": "001-b",
  "title": "Native environment and offline runtime closure",
  "objective": "001",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
  "branch": "oap/001-reproducible-application-development-baseline",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 2,
  "dependencies": [
    "000"
  ],
  "local_work": "Clean objective branch at remote report head b1f5335f311772533c6a80cabbaf28d37500b32c; preserve immutable 001-a order/report and the ignored disposable .venv created by strategic review until it can be safely discarded without sync-mount contention.",
  "prior_review": "001-a remote report verified COMPLETE and both required final-head checks passed, but independent local review reproduced a blocking repository-.venv sync-mount path and showed the reported fresh offline wheel install used --no-deps, leaving the declared runtime closure unproved.",
  "provenance": [
    {
      "kind": "A",
      "reference": "001-a requirements 6-9 and acceptance criteria 1-5; ARCHITECTURE.md §§4.1,15,16; WORKSPACE-LAYOUT.json sync-storage exception; S-DIAGNOSE-01 and S-EVIDENCE-01"
    },
    {
      "kind": "E",
      "reference": "2026-09-08 strategic review at b1f5335f311772533c6a80cabbaf28d37500b32c: documented default uv run created repository .venv on the owner-selected sync mount and blocked in filesystem lookup; a fresh UV_OFFLINE install without --no-deps failed because the runtime closure was not available from the tested cache, while CI run 34173079156 proved only --no-deps wheel import"
    }
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
  "lr": [
    "LR-012",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "Application baseline"
  ],
  "decision_class": "D0"
}
```

## Identity

001-b is a corrective round on the existing objective-001 branch and PR #2.
Preserve implementation commit 7671177, immutable 001-a report commit b1f5335,
and their remote check history. Do not amend history, create a second PR, or advance
the numeric objective.

## Provenance

- A: 001-a required a clean native owned environment, import-time network denial,
  full wheel installation, reproducible documented commands and final-head CI.
  Workspace layout explicitly records that the selected sync mount lacks ordinary
  POSIX/hardlink semantics. Evidence must exercise that actual local boundary.
- E: independent review invoked the documented root-level uv commands. The created
  `.venv` on the sync mount blocked both pytest and direct Python import in filesystem
  lookup. Coding's own report had already disclosed that it stopped the shared path
  after contention and succeeded only with an owned temporary environment. CI then
  installed the wheel with `--offline --no-index --no-deps`, so it never proved that
  HTTPX and Pydantic plus transitive dependencies could be resolved/installed from
  the cache populated by frozen sync. Removing `--no-deps` reproduced an offline
  resolution failure in the independently available cache.

The earliest boundaries are local environment placement and offline dependency
closure. Do not change package behavior, dependency declarations or import code to
work around them.

## Current verified state

Remote/default accepted `main` remains objective-000 merge
`82ea1e6f4173934fa47bb34ee6a6f78338d3603a`. PR #2 is open and clean at report
head `b1f5335f311772533c6a80cabbaf28d37500b32c`; 001-a implementation head is
`76711778ead2edbf4c039a62fd1beaa74fa2de8c`. Both 001-a reports/SELF invariants are
remotely verified and both required GitHub checks completed successfully at b1f5335.

The repository diff is otherwise clean and accepted governance passes. CRITICAL has
no entries or gates. A disposable ignored `.venv` created solely by strategic review
may remain locally; a recoverable trash attempt itself blocked on the sync filesystem
and was stopped. Do not treat that ignored environment as authoritative evidence or
delete it with an unsafe broad command. No product/live/linguistic/audit/release/
deployment boundary has been crossed.

## Governance

Preserve the accepted governance identity map and every objective-000/001-a order,
report and commit byte. Apply LR-012 to keep all work CPU/package-only with no model,
GPU or import-time acquisition. Apply LR-014: local native-environment, wheel and CI
proof remain package evidence only. No governance source revision, D1 dilemma or DHA
entry is authorized.

## Goal and dependencies

Make the documented and CI development path use an explicit native owned temporary
environment rather than repository `.venv`, and prove a fresh offline installation
of the complete declared runtime dependency closure after a frozen sync populates an
isolated cache. Close the exact evidence gaps in 001-a without changing its package
contract or adding repair functionality.

## Scope

1. Add one small standard-library verification driver under `scripts/` that runs the
   complete development/package proof in a fresh native temporary root.
2. Update `docs/DEVELOPMENT.md` so the supported one-command local path uses that
   driver and no fixed shared `/tmp` directory or repository `.venv`.
3. Update `.github/workflows/application-baseline.yml` to use the same driver/native
   environment and prove the full offline runtime closure.
4. Add focused tests for the driver's path/env/command invariants without recursively
   invoking the full driver from inside the full suite.
5. Update only exact inventory rows if an already-inventoried generated surface is
   changed; publish exact 001-b order/active/report protocol files.

## Non-goals

Do not change Python/package versions, dependency ranges, uv.lock resolution,
package root API, application behavior, canonical governance, objective-001-a
history, bootstrap CI, GitHub settings, service/release workflows or protected
resources. Do not add/remove Pydantic, HTTPX, dev tools, morphology analyzers,
FastAPI, corpora, models or product modules. Do not claim the sync mount supports
venvs or recursively delete arbitrary `.venv`/cache paths.

No live Qwen/data use, GPU/vLLM/CUDA/gateway/network mutation, package publication,
merge, auto-merge, milestone acceptance, release or deployment.

## Files and boundaries

Expected mutable paths are limited to:

- `scripts/verify_development_baseline.py`;
- `tests/contract/test_objective_001.py` or a narrowly named sibling for driver
  contract tests;
- `docs/DEVELOPMENT.md`;
- `.github/workflows/application-baseline.yml`;
- exact affected inventory rows only if applicable;
- published `oap/orders/001-b-native-environment-and-offline-runtime-closure.md`,
  `oap/active`, and matching immutable report.

Inspect pyproject/lock/package, 001-a report, CI logs and ignored `.venv` read-only as
needed. The verification driver must operate only on its own `TemporaryDirectory`
and repository read paths; it must never clean an unresolved caller path.

## Requirements

1. Implement a Python 3.12 standard-library driver with a finite subprocess timeout
   per command and an optional explicit native temp-parent argument. It must create
   its unique owned root with `tempfile.TemporaryDirectory`, reject a resolved temp
   root inside the repository, use argument arrays, and rely on context-managed
   cleanup. Do not use shell evaluation, a fixed shared venv name, broad glob cleanup,
   or recursive deletion of caller-supplied paths.
2. Inside that owned root set `UV_PROJECT_ENVIRONMENT` to an owned `venv`,
   `UV_CACHE_DIR` to an owned `cache`, `UV_LINK_MODE=copy`, and a Python selector that
   requires 3.12 without silently choosing 3.13. Preserve the caller environment only
   as needed; do not print auth/proxy/credential values.
3. Through that single environment run, in order: `uv lock --check`; frozen sync of
   all groups/extras; focused contract tests; full pytest; Ruff; mypy; separate OAP
   unittest discovery; and sdist/wheel build into an owned output directory. Record
   finite command/result labels without capturing or echoing private environment.
4. After online frozen sync has populated the isolated cache, create a second fresh
   owned Python 3.12 venv. With `UV_OFFLINE=1`, install the built wheel **without**
   `--no-deps` and without any network access. Import
   `llm_slovenian_repair`, `pydantic`, and `httpx` from outside the repository and
   assert expected versions/package metadata. A missing cached transitive dependency
   must fail the proof, not be bypassed.
5. Preserve the existing Python socket/URL-blocked import-isolation test. Add focused
   nonrecursive tests of driver environment construction, repository-path refusal,
   command ordering, timeout/error propagation and the absence of repository `.venv`
   creation. Test doubles may replace subprocess execution only outside the driver
   policy/path boundary; the workflow must exercise real uv/build/install commands.
6. The application workflow retains its exact job/check name, read-only permission,
   pinned actions, uv/Python versions, runner and finite job timeout. Run the driver
   with a unique `$RUNNER_TEMP` parent, then assert the checkout contains no `.venv`,
   `dist`, build or cache artifact. Retain accepted-base whitespace/protected-source
   checks. Do not use setup-uv caching, secrets or write permissions.
7. Replace the documented raw sequence as the supported selected-workspace path with
   the exact driver command using `/tmp` (or another verified native explicit parent).
   Explain why repository `.venv` is unsupported on the owner-selected sync mount,
   how the driver populates and then disables network for the full dependency install,
   and that its temporary environment/cache/build artifacts are automatically scoped
   and cleaned. Remove fixed-path `rm -rf` guidance.
8. Keep pyproject, lock, package API/dependencies and public status claims unchanged
   unless a direct test proves a minimal correction is necessary; report any such
   discrepancy before expanding scope. Preserve the 001-a failed/partial observations
   exactly as historical evidence.

## Acceptance criteria

1. Running the driver from the actual selected workspace with native temp parent
   completes lock, sync, 65-or-more pytest tests, Ruff, mypy, 61-or-more OAP tests,
   sdist/wheel build and full offline runtime-closure installation/import without
   creating or accessing repository `.venv`.
2. The offline install omits `--no-deps`, runs under enforced uv offline mode, and
   imports exact locked `pydantic`, `pydantic-core`, `httpx` and package versions in
   the fresh wheel environment. A synthetic missing-cache case fails explicitly.
3. Focused driver tests prove native path/refusal, exact environment isolation,
   command sequence, timeouts/error propagation and no repository environment.
4. `docs/DEVELOPMENT.md` names the working native driver command and no longer
   presents sync-mounted `.venv`, a fixed shared venv, `--no-deps`, or broad manual
   deletion as the supported proof.
5. Both `OAP bootstrap acceptance` and `Application baseline` complete successfully
   at the exact final 001-b report head. CI logs show the real driver, full dependency
   offline installation and no checkout `.venv`/dist/cache artifact.
6. Accepted-runtime governance and protected-source diff pass, CRITICAL is unchanged,
   001-a history is intact, active blob is exactly `001-b\n`, and remote 001-b SELF
   report verification succeeds.
7. PR #2 remains the sole open objective PR and unmerged during coding; no product,
   live model/data, private path/value, repository-setting, release or deployment
   change is present.

## Verification

Run and report at the literal implementation SHA, using unique owned native paths:

```text
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp
python3.12 -m pytest tests/contract/test_objective_001.py -q
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 82ea1e6f4173934fa47bb34ee6a6f78338d3603a
python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair
git diff --check 82ea1e6f4173934fa47bb34ee6a6f78338d3603a...HEAD
git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

The driver itself runs the named uv/pytest/Ruff/mypy/build/offline-install sequence;
the report must list its sub-results and exact timeout/cleanup evidence rather than
only a wrapper exit code. After report publication, independently verify both exact
final-head checks and the remote SELF invariant. Local/package evidence remains
separate from repair/Qwen/linguistic/ICA/release/deployment evidence.

## Local setup and constraints

Use Python 3.12, uv and only unique `TemporaryDirectory` roots on native storage.
Registry access is allowed only during the initial isolated frozen sync/build
dependency population. Enforce offline mode for the second wheel environment.
Do not use or repair the ignored repository `.venv`; it is disposable review residue,
not evidence. Do not ask the human to clean it or relay terminal output.

No credentials, auth files, proxy values, customer/model text, prompts, replacements,
raw responses or private strategic paths in Git, CI, reports or logs. No package
publishing, Qwen/corpus access, service/daemon, GPU/model/server/gateway/network
mutation, GitHub-setting change, release or deployment.

## Documentation

Update `docs/DEVELOPMENT.md` to make the safe native verification driver the primary
local command, explain online-cache-population versus enforced-offline install, and
preserve dependency licenses/ranges and all evidence limitations. No README/status
change is expected. The immutable 001-b order/report must preserve the exact initial
failure and the stronger proof without rewriting 001-a history.

## Git and report publication

Stay on `oap/001-reproducible-application-development-baseline` and amend only open
PR #2. Preserve 7671177 and b1f5335. Commit/push all non-report correction files plus
exact 001-b order and active pointer before composing a new report. Do not merge or
enable auto-merge.

Record the literal implementation head, then create exactly
`oap/reports/001-b-native-environment-and-offline-runtime-closure.md`. The final
report commit has the implementation head as sole parent and changes only that path.
Push, verify remote PR/head/bytes/parent/path, send exact response `OK`, and exit with
no later mutation. A COMPLETE report may truthfully leave future report-head checks
PENDING for strategic observation; do not claim them before publication.

## Decision classification

D0. Native temporary environment placement and full offline dependency installation
are ordinary reversible build/evidence corrections within the selected workspace
and architecture. The observed hangs/failures are prerequisites and test gaps, not
five-condition judgment debt. No D1 append or D2 action is authorized.

## Deferred human adjudication
- Decision: NONE

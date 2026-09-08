# Work order 001-c — Lock-driven offline sync and diagnostics

Status: FINAL

```oap-metadata
{
  "id": "001-c",
  "title": "Lock-driven offline sync and diagnostics",
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
  "local_work": "Clean objective branch at remote report head 11b483fd829a8d9b5fb4118799d2f551caa4add0; preserve all 001-a/001-b commits and immutable reports plus ignored disposable review residue.",
  "prior_review": "001-b report remotely verified COMPLETE and both final-head checks passed, but independent semantic review rejected uv-private cache wheel reconstruction and non-actionable suppressed subprocess diagnostics; PR #2 remains open and unmerged.",
  "provenance": [
    {
      "kind": "A",
      "reference": "001-a/001-b exact lock, clean offline install and truthful evidence requirements; ARCHITECTURE.md §§4.1,15,16; S-EVIDENCE-01 and S-DIAGNOSE-01"
    },
    {
      "kind": "E",
      "reference": "2026-09-08 independent experiment at 001-b report head: isolated frozen sync followed by UV_OFFLINE=1 uv sync --frozen --no-dev --no-install-project into a fresh venv installed 11 exact locked runtime packages, then normal offline wheel install/import passed; this avoids reconstructed wheels and uv internal wheels-v6 layout"
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

001-c is the next corrective round on existing objective branch
`oap/001-reproducible-application-development-baseline` and PR #2. Preserve all
prior commits/reports and CI attempts; do not amend history, duplicate the PR, or
advance the numeric objective.

## Provenance

- A: exact locked artifacts and independent clean-install evidence must be proved by
  supported tooling at the real boundary. Diagnostic failures must preserve enough
  bounded evidence to locate the earliest failure rather than depend on blind retry.
- E: the 001-b verifier reaches into `UV_CACHE_DIR/wheels-v6/pypi`, reads extracted
  directories, and creates new zip archives with synthesized wheel filenames. Those
  are not the original lockfile-hashed distribution artifacts, and `wheels-v6` is a
  uv implementation detail. CI attempt 1 at fac9f68 failed its OAP unittest step;
  the driver suppressed all subprocess output, so retry success at the unchanged SHA
  could not explain or supersede the failure causally.
- E: a minimal independent alternative at report head 11b483f used one isolated uv
  cache and native root: online frozen runtime sync, wheel build, fresh offline
  `uv sync --frozen --no-dev --no-install-project`, normal offline wheel installation
  without `--no-deps`, and exact imports. It passed with 11 locked runtime packages,
  including pydantic 2.13.5, pydantic-core 2.46.5 and httpx 0.28.1.

## Current verified state

Accepted remote/default `main` remains
`82ea1e6f4173934fa47bb34ee6a6f78338d3603a`. PR #2 is open and clean at 001-b
report head `11b483fd829a8d9b5fb4118799d2f551caa4add0`; 001-b implementation is
`fac9f68c96e860df8ef7f0be4da66a4fb734ba8b`. Both 001-a and 001-b remote SELF
reports verify. Both required final-head checks are green at 11b483f.

The initial Application-baseline attempt at fac9f68 failed during OAP unittest
discovery; a same-SHA retry and final report-head run passed. The failure remains
unexplained because output was discarded. Accepted governance and protected-source
diff are clean; CRITICAL has no entries/gates; no merge, product/live/model/data,
milestone, release or deployment action occurred.

## Governance

Preserve the exact accepted governance map, package/lock/API contract, all earlier
orders/reports/commits and CRITICAL bytes. Apply LR-012 and LR-014: this is a
CPU/package evidence correction only and establishes no repair/live/linguistic/
milestone/deployment result. D0 and `Decision: NONE`; no new judgment debt.

## Goal and dependencies

Replace private-cache wheel reconstruction with uv's lock-driven offline sync into a
fresh runtime environment, then install the built project wheel normally. Make any
future command failure actionable through strictly bounded path-redacted diagnostics,
while keeping the native temporary-environment solution and package contract intact.

## Scope

1. Simplify `scripts/verify_development_baseline.py` to use a second offline frozen
   sync with `--no-dev --no-install-project` and the same isolated cache.
2. Remove wheelhouse reconstruction and every dependency on uv internal cache paths,
   extracted package directories, synthesized wheel archives and zipfile repacking.
3. Add bounded redacted failure diagnostics and direct focused tests for them.
4. Update development documentation and the existing Application-baseline workflow
   only as required by the simplified driver/diagnostic contract.
5. Publish exact 001-c order/active/report on existing PR #2.

## Non-goals

Do not change pyproject, uv.lock, direct/transitive versions, package code/API,
Python/uv/pinned-action versions, bootstrap workflow, product/governance sources,
previous transcript/history or public status. Do not add a download command, package
index, wheel vendor directory, generated third-party artifact, persistent cache,
analyzer/model/corpus, repair module, service, release/publish workflow or dependency.

No Qwen/GPU/vLLM/CUDA/gateway/service/network setting mutation, GitHub setting,
merge/auto-merge, milestone label, release or deployment.

## Files and boundaries

Expected mutable paths:

- `scripts/verify_development_baseline.py`;
- driver-focused portions of `tests/contract/test_objective_001.py`;
- `docs/DEVELOPMENT.md` and `.github/workflows/application-baseline.yml` only if
  wording/commands need alignment;
- published 001-c order/active pointer and immutable matching report.

Do not modify package metadata/lock or inventories when their bytes are unchanged.
The native mirror may remain only as a bounded copy of current readable repository
bytes for filesystem-compatible testing; it is not a substitute for Git/remote truth.

## Requirements

1. After the initial online frozen sync populates the owned `UV_CACHE_DIR`, build the
   project wheel into the owned output directory. Create a fresh second project
   environment and run uv with `UV_OFFLINE=1` using the same cache:
   `uv sync --frozen --no-dev --no-install-project --python 3.12`. This must install
   the complete exact runtime closure from `uv.lock` without network or project code.
2. Install the built wheel into that environment using normal uv dependency handling
   under offline mode. Do not use `--no-deps`, `--no-index`, `--find-links`, a
   wheelhouse, or reconstructed third-party wheels. Dependencies must already be
   satisfied by the offline lock sync; import package/Pydantic/pydantic-core/HTTPX
   from outside the repository and verify exact locked versions/normalized metadata.
3. Delete code/imports/tests/docs for `wheels-v6`, `materialize_cached_runtime_wheels`,
   runtime wheel graph traversal used solely for repacking, wheelhouse paths, and
   synthesized third-party archives. Prefer a materially smaller driver and preserve
   only controls that prove path ownership, sequence, timeouts, cleanup and results.
4. `run_command` must capture only a finite stdout/stderr tail on failure, replace the
   resolved repository and owned temporary root with stable placeholders, strip
   control characters, and cap the reported diagnostic to at most 4096 UTF-8 bytes.
   Never emit environment values, credentials, proxy/auth data, full logs or success
   output. The summary must retain label, FAILED/TIMEOUT, return code when present and
   the sanitized bounded diagnostic; successful records remain content-free.
5. Focused tests must prove truncation, path redaction, control-character handling,
   success-output omission, timeout/nonzero distinction, and that a synthetic secret
   environment value not present in subprocess output cannot appear in the summary.
   Keep path/refusal/command-order/no-repository-venv/missing-offline-cache negatives.
6. A real native driver run and Application CI must exercise the supported offline
   sync plus wheel install. CI may not pass through a retry alone: final implementation
   and report heads each need successful fresh runs. Preserve any earlier failed run
   in history and report its unknown cause honestly.
7. Documentation must describe lock-driven offline sync, not wheelhouse/cache-layout
   reconstruction, and state that bounded diagnostics identify future failures while
   the earlier fac9f68 failure remains causally unresolved. Keep the single supported
   native driver command and automatic owned cleanup.
8. Preserve exact report-only SELF chronology, check names, workflow permissions and
   accepted-base/protected-source checks. No repository `.venv`, build, dist or cache
   artifact may be created by the driver or remain after CI.

## Acceptance criteria

1. Driver source and tests contain no `wheels-v6`, wheelhouse/repacking function,
   synthesized third-party `.whl`, private uv cache layout assumption, `--no-deps`,
   `--no-index` or `--find-links` path.
2. A real native run records PASSED for online frozen sync, offline runtime-only
   frozen sync, normal offline built-wheel install, exact imports, all test/lint/type/
   build steps and cleanup. The fresh offline environment contains all 11 exact
   runtime dependencies and no dev group requirement.
3. Focused negative tests prove missing-cache failure at the offline sync boundary and
   bounded/redacted diagnostic behavior, including distinct timeout and nonzero exit.
4. The earlier unexplained attempt-1 failure remains visible and is not relabelled;
   new implementation-head and report-head Application/OAP checks both pass without a
   rerun of the new SHA.
5. Accepted governance/protected-source checks pass, CRITICAL is unchanged, active is
   exactly `001-c\n`, earlier 001 reports are immutable, and 001-c remote SELF report
   verification succeeds.
6. PR #2 remains the sole open objective PR and unmerged during coding; no unrelated,
   product, live/model/data, private-value, setting, release or deployment change.

## Verification

Run and record at the literal implementation SHA:

```text
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3.12 -m pytest tests/contract/test_objective_001.py -q
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 82ea1e6f4173934fa47bb34ee6a6f78338d3603a
python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair
git diff --check 82ea1e6f4173934fa47bb34ee6a6f78338d3603a...HEAD
git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Inspect the driver JSON summary for named sub-results without private/raw output.
After report publication, independently verify remote SELF and both exact final-head
checks. Package evidence remains separate from repair/Qwen/linguistic/ICA/release/
deployment evidence.

## Local setup and constraints

Use only Python 3.12, uv, the existing locked dependencies, and unique owned native
temporary roots. Registry network is allowed only during the initial frozen sync;
the second sync/install/import must be uv-offline. Do not access or delete the ignored
repository `.venv` or unrelated `/tmp` content. The driver owns and cleans only its
TemporaryDirectory.

No credentials, auth/proxy values, customer/model text, prompts, replacements or raw
responses in Git/CI/report diagnostics. No Qwen/corpus/GPU/service/gateway/network
configuration mutation, package publication, merge, release or deployment.

## Documentation

Align `docs/DEVELOPMENT.md` with the supported lock-driven offline path, bounded
diagnostic behavior and automatic native cleanup. Preserve package versions/licenses,
PLANNED product status and all distinct evidence/human gates. Do not edit README or
STATUS unless a direct contradiction is found and returned to strategy first.

## Git and report publication

Stay on existing objective branch/PR #2 and preserve all 001-a/001-b commits/reports.
Commit/push all non-report changes plus exact order/active before the report. Do not
merge or enable auto-merge.

After final non-report push/checks, record the literal implementation head and create
only `oap/reports/001-c-lock-driven-offline-sync-and-diagnostics.md`. Its SELF commit
has the implementation head as sole parent and changes only that report. Push,
independently verify remote bytes/head/parent/path, send exact `OK`, and make no later
mutation. Future report-head checks remain PENDING inside the report.

## Decision classification

D0. Replacing a private cache-layout workaround with the supported lock-driven uv
flow and making diagnostics bounded/actionable is an ordinary reversible evidence
repair. No unresolved consequential alternative meets the D1 threshold; no D2 action
is authorized.

## Deferred human adjudication
- Decision: NONE

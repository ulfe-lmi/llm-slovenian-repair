# Work order 001-a — Reproducible application development baseline

Status: FINAL

```oap-metadata
{
  "id": "001-a",
  "title": "Reproducible application development baseline",
  "objective": "001",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
  "branch": "oap/001-reproducible-application-development-baseline",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "000"
  ],
  "local_work": "Clean local main matching remote accepted merge commit 82ea1e6f4173934fa47bb34ee6a6f78338d3603a at 2026-09-08 after verified objective 000 merge; preserve all published 000-a/000-b history.",
  "prior_review": "Objective 000 accepted and development PR #1 merged with merge commit 82ea1e6f4173934fa47bb34ee6a6f78338d3603a after exact-head review, 61 local tests, and successful required final-head CI.",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §12 and demonstrator D01; owner-selected Apache-2.0 LICENSE and explicit development-loop authorization"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§4.1, 15, 16; oap/strategic-instructions/INITIAL-ROADMAP.md objective 001-a; TESTING.md TEST-02 and TEST-03"
    },
    {
      "kind": "E",
      "reference": "2026-09-08 inspection: merged main has no pyproject, lockfile, src package, application contract tests, or application CI; local Python is 3.12.3 and uv is 0.12.5; official releases inspected for uv 0.12.10, hatchling 1.32.0, pydantic 2.13.5, httpx 0.28.1, pytest 9.1.1, ruff 0.16.6 and mypy 2.3.1"
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

001-a is the first round of DEMONSTRATOR objective 001 and creates exactly one
branch/PR: `oap/001-reproducible-application-development-baseline`. If interrupted
after branch or PR creation, recover that exact object and ID; do not duplicate it.

## Provenance

- H: PLAN §12 proposes Python 3.12, uv, typed validation, HTTPX and pytest as the
  implementation stack; D01 requires initial contracts/policy. The owner supplied
  and selected the repository's Apache-2.0 code license.
- A: ARCHITECTURE §4.1 selects Python 3.12, a locked uv environment, Pydantic,
  HTTPX, pytest, optional bounded CPU analyzers, and FastAPI only for the later
  adapter. §§15–16 require no import-time downloads, protected-resource isolation,
  reproducibility and evidence-layer separation. Roadmap 001 requires the package,
  lock, commands and offline defaults before product modules.
- E: accepted main contains bootstrap/governance only. It has no package metadata,
  lock, `src` tree, application contract suite or application CI. Local tools are
  Python 3.12.3 and uv 0.12.5; ruff and mypy are not globally installed. Primary
  release/registry inspection on 2026-09-08 found compatible current baselines:
  uv 0.12.10, hatchling 1.32.0, Pydantic 2.13.5, HTTPX 0.28.1, pytest 9.1.1,
  Ruff 0.16.6 and mypy 2.3.1. Their recorded licenses are MIT except HTTPX's BSD.

Coding uses the compact read set and this bounded order; these citations do not
require loading full PLAN, full architecture, roadmap, or source doctrine.

## Current verified state

Remote and clean local `main` are the verified objective-000 merge commit
`82ea1e6f4173934fa47bb34ee6a6f78338d3603a`. PR #1 is merged; its exact merge is
verified on remote main and its four objective commits preserve both SELF reports.
There are no open PRs and no remote branch for objective 001. Current OAP state is
REVIEW_READY at 000-b, with no critical entry, disposition or gate.

The accepted governance identity set is unchanged from objective 000 and passes
accepted-runtime validation at the new accepted Git base. The existing PR-triggered
check `OAP bootstrap acceptance` is active and passed 61 tests at the final 000-b
head. No application package or application check exists. Python 3.12.3 and uv
0.12.5 are installed locally. Live repair testing remains disabled; no Qwen/corpus,
linguistic, ICA, milestone, release or deployment evidence exists.

## Governance

The metadata map is the literal accepted governance identity set at base
`82ea1e6f4173934fa47bb34ee6a6f78338d3603a`. Preserve PLAN, ARCHITECTURE,
CRITICAL, role law, compact projections, prompts, source locks, the distillation
map, workspace layout, bootstrap snapshots and all objective-000 transcript bytes.

Apply LR-012: no additional large model, GPU/model/server mutation or import-time
download. Apply LR-014: a package build/import and fake/contract tests prove only
the software development baseline, not serving compatibility, repair behavior,
linguistic quality, ICA or deployment authority. There is no D1 decision or DHA
gate. The private quiescent refresh reported no changed governance copy; its lock
limitation is strategic runtime state and not coding scope.

## Goal and dependencies

Create a reproducible, installable Python 3.12 library skeleton whose runtime,
development and future morphology dependencies are explicitly separated and fully
locked, with stable lint/type/test/build commands and an import path proven not to
perform model/corpus/network work. Objective 000 is verified and merged.

This establishes D01's development substrate only. It does not implement the typed
repair contracts assigned to objective 003 or any functional repair behavior.

## Scope

1. Add standards-based `pyproject.toml`, committed `uv.lock`, and a checked-in
   Python 3.12 selector if uv uses one.
2. Add the minimal `src/llm_slovenian_repair` package needed to build and import,
   without repair functions, model clients, downloads, initialization side effects,
   or false public API claims.
3. Add `tests/contract/test_objective_001.py` and only support files needed to test
   metadata, locked dependency policy, import isolation and the built wheel.
4. Add concise development/build documentation and a discoverable README link.
5. Add one PR-triggered application workflow/job named exactly `Application baseline`
   while preserving the existing `OAP bootstrap acceptance` job.
6. Update generated/installation inventory values only where an already-inventoried
   generated surface is intentionally changed.

## Non-goals

Do not implement spans, evidence, policy, protected text, corpus access, detection,
review prompts/client, acceptance, patching, pipeline, CLI or API behavior. Do not
add FastAPI, a morphology/analyzer package, a corpus/model downloader, runtime
scraper, Git/URL/path dependency, pre-commit framework, release/publish workflow,
container/service config or production entry point. Do not call Qwen, acquire data,
change the GPU/model/server/gateway/network, change GitHub settings/protection, or
claim demonstrator/MVP/release/deployment readiness.

Do not modify canonical product/governance sources or rewrite objective-000 orders,
reports, commits, CI history or private strategic state.

## Files and boundaries

Expected mutable paths are limited to the coherent package substrate:

- `pyproject.toml`, `uv.lock`, and optionally `.python-version`;
- `src/llm_slovenian_repair/__init__.py` and optional `py.typed`;
- `tests/contract/test_objective_001.py` plus package-local test support only if
  direct evidence requires it;
- `docs/DEVELOPMENT.md` and the minimal README link/status adjustment;
- `.github/workflows/application-baseline.yml`;
- exact affected rows in `oap/GENERATED-FILES.json` and `oap/INSTALLATION.json`;
- the published 001-a order/active pointer and matching immutable report.

Package indexes are permitted only for resolving/installing the named ordinary
dependencies into an owned project environment and producing the committed lock.
Application import, tests and operation must not contact them. Test doubles stay
outside the package-import boundary being proved.

## Requirements

1. Use a PEP 517/621 `src`-layout package named `llm-slovenian-repair`, version
   `0.0.0`, `requires-python = ">=3.12,<3.13"`, Apache-2.0 metadata and Hatchling
   build backend constrained to `>=1.32,<2`. The root package may expose only inert
   metadata/documentation; no repair API is invented.
2. Declare runtime requirements with compatible upper bounds:
   `pydantic>=2.13.5,<3` and `httpx>=0.28.1,<1`. Do not import either eagerly from
   the root package. Do not add FastAPI yet.
3. Declare the local development dependency group separately:
   `pytest>=9.1.1,<10`, `ruff>=0.16.6,<0.17`, and `mypy>=2.3.1,<3`. Declare a
   published optional extra named `morphology` as an intentionally empty list with
   documentation that objective 027 must select/qualify any analyzer and its rights.
   An empty extra grants no analyzer capability.
4. Set uv's project requirement to accept the verified compatible tool range
   `>=0.12.5,<0.13`. Generate and commit a cross-platform `uv.lock` containing exact
   resolved artifacts/hashes. Use only the default public registry; no alternative
   index, Git, URL, local path, editable external or unbounded direct dependency.
5. Configure versioned commands for Ruff and mypy in `pyproject.toml` without
   disabling useful checks or globally ignoring errors. Target Python 3.12. Tests
   and package code must pass the configured lint, type and pytest commands.
6. Contract tests must parse the real `pyproject.toml`/lock, verify the exact Python,
   dependency-group/extra/source policy, and import the installed package in a fresh
   subprocess with Python socket/connect and common URL-opening operations blocked
   before import. Run from an owned empty cwd/home with any corpus/model location
   pointing to an absent path; assert import creates no file, loads no Pydantic,
   HTTPX, model or analyzer module, and performs no network call.
7. Build both sdist and wheel from the committed metadata with `uv build --no-sources`.
   In a new owned Python 3.12 virtual environment, install the exact wheel with uv
   offline after the locked dependencies have been populated by the ordinary sync;
   import it from outside the repository. Inspect wheel metadata to prove name,
   version, Python constraint, license, runtime requirements and absence of package
   data/model/corpus payloads. Remove all owned build/venv artifacts after proof.
8. Development documentation must give exact `uv sync --frozen --all-groups`,
   focused/full pytest, Ruff, mypy, lock-check, build and clean-install commands;
   explain runtime/dev/empty-morphology separation; state that dependency resolution
   may use the registry but package import performs no download; and preserve every
   live/product/evidence limitation.
9. Add a least-privilege, finite PR workflow using immutable
   `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` and
   `astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d` with uv 0.12.10.
   Its single job/check name is exactly `Application baseline`; use ubuntu-24.04,
   Python 3.12, frozen sync, contract/full tests, Ruff, mypy, build, offline wheel
   installation/import and accepted-base-to-HEAD whitespace checks. No secret,
   cache, write permission, live service, model, corpus, deploy or publish step.
10. Preserve the bootstrap workflow/check unchanged and require both named checks at
    the final report head. Recalculate only directly affected inventory hashes from
    actual final bytes; do not alter accepted governance identities.

## Acceptance criteria

1. A clean `uv sync --frozen --all-groups --all-extras` under Python 3.12 succeeds
   from committed metadata/lock; `uv lock --check` confirms no drift. The lock has
   exact artifacts/hashes and no forbidden source or analyzer/model dependency.
2. Focused and full pytest, Ruff and mypy pass using only the project environment.
   No globally installed Ruff/mypy is required and no check is weakened/skipped.
3. The real installed package imports successfully from outside the source tree with
   outbound Python networking blocked and no corpus/model present, creates no files,
   imports no heavy runtime/analyzer module and exposes no invented repair behavior.
4. The sdist/wheel build succeeds; a fresh offline wheel installation/import succeeds
   from populated locked cache, and inspected metadata matches the exact contract.
5. Both final-head GitHub checks—`OAP bootstrap acceptance` and `Application baseline`—
   complete successfully at the exact 001-a report commit. Missing, pending,
   skipped, cancelled, failed or stale-head results do not pass.
6. Accepted-runtime governance passes at base 82ea1e6, protected-source diff is empty,
   CRITICAL is unchanged, and objective-000 history remains intact. The new active
   blob is exactly `001-a\n`.
7. The final remote report satisfies SELF identity/parent/only-path verification on
   the sole objective-001 PR. Coding does not merge or enable auto-merge.
8. Documentation names actual commands and evidence boundaries. No repair feature,
   live-Qwen/corpus/linguistic claim, private path/data, product milestone, release,
   deployment or production authorization is introduced.

## Verification

Run and record the literal implementation SHA for each command:

```text
uv lock --check
uv sync --frozen --all-groups --all-extras --python 3.12
uv run --frozen pytest tests/contract/test_objective_001.py -q
uv run --frozen pytest -q
uv run --frozen ruff check src tests
uv run --frozen mypy src tests/contract
uv build --no-sources
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 82ea1e6f4173934fa47bb34ee6a6f78338d3603a
python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair
git diff --check 82ea1e6f4173934fa47bb34ee6a6f78338d3603a...HEAD
git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Also run the documented owned temporary-directory offline wheel install/import
proof and report its exact command. Inspect both required checks after pushing the
implementation head and again at the final report head. Report-head CI remains a
post-publication strategic observation; do not claim future success inside the
report. A COMPLETE implementation report may record those final-head checks PENDING
when all locally observable requirements are complete.

Fake/contract tests prove packaging/import behavior only. They do not establish
repair logic, actual reviewer/API compatibility, linguistic benefit, runtime
resource behavior, ICA, release or deployment readiness.

## Local setup and constraints

Use the repository `.venv` and uv cache or owned temporary directories. Registry
access is permitted only to resolve/download the explicitly named ordinary package,
build and development dependencies and record their provenance in `uv.lock`/docs.
Do not install global lint/type packages, daemons, services, GPU software, models,
corpora, browsers or databases. Clean owned build/temporary artifacts; preserve the
committed lock and all unrelated user work.

No credentials, auth files, customer/model text, prompts, replacements, raw API
responses or private runtime paths in Git, test output, reports or CI. Do not access
or mutate Qwen weights/quantization, vLLM/CUDA, GPU allocation, services/ports,
network/VPN/firewall, gateway or neighboring repositories. Live repair tests remain
disabled. Dependency installation does not authorize package publishing or release.

## Documentation

Create `docs/DEVELOPMENT.md` as the package development contract and link it from
README. Record exact Python/uv ranges, declared direct dependencies and observed
licenses, frozen commands, optional-extra status, clean build/install procedure,
no-import-download guarantee and cleanup. Keep README/STATUS claims honest: this
objective establishes only an installable development skeleton; product remains
PLANNED and no live/quality/milestone/release/deployment gate is cleared.

Update generated/installation inventory rows mechanically if README or another
already-inventoried generated file changes. New application files are ordinary
development artifacts, not retroactive bootstrap outputs.

## Git and report publication

Start from exact merged main `82ea1e6f4173934fa47bb34ee6a6f78338d3603a` and create
only `oap/001-reproducible-application-development-baseline` and its one PR. Commit
and push all non-report work, including exact published order/active bytes, before
composing the report. Open the PR first; repair safe in-scope failures on the same
branch/PR. Never merge or enable auto-merge.

Record the literal implementation head after all non-report changes. Create one
immutable `oap/reports/001-a-reproducible-application-development-baseline.md`
report with publication commit SELF; its final commit must have the implementation
head as sole parent and change only that report path. Push, independently verify
remote head/report bytes/parent/path, then send exact response `OK` and exit without
later mutation. The report must distinguish local/implementation-head proof from
future report-head checks and preserve all limitations.

## Decision classification

D0. The Python minor range, standard `src`/Hatchling layout, bounded compatible
dependency ranges, exact lock, empty future-analyzer extra and CI/test mechanics are
ordinary reversible choices inside the architecture-selected baseline. No rights
ambiguity remains for the named packages, no product acceptance boundary changes,
and no five-condition D1 dilemma exists. D2 live/model/data/release/deployment and
security-posture actions remain blocked.

## Deferred human adjudication
- Decision: NONE

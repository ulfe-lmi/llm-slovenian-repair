# Work order 007-k — Migrate development environment off the shared FUSE tree

Status: FINAL

```oap-metadata
{
  "id": "007-k",
  "title": "Migrate development environment off the shared FUSE tree",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": ["001", "002", "007"],
  "local_work": "Clean local/remote objective branch at immutable 007-j report head f752e8f3ddd9a8bf9bec2f20e789d512da67990b. Preserve all source, lock, Git/OAP/research/private evidence. The ignored repository .venv and transient caches are explicitly owned cleanup targets only after external-environment verification.",
  "prior_review": "007-j is remotely verified and complete; PR #8 remains OPEN/UNMERGED, main ee2d1b4. Final-head Research and both OAP checks pass; Application baseline retains the inherited verifier mypy failure. Dropbox/rclone write throttling and FUSE metadata stalls are independently observed. No 007-k files or external persistent environment exist.",
  "provenance": [
    {"kind":"H","reference":"Owner explicitly requires the shared Dropbox/FUSE project to retain source/Git/lock/config/docs/research while each machine recreates the uv environment at $HOME/envs/llm-slovenian-repair, redirects bytecode/transient caches machine-locally, verifies replacement, then removes the project-local .venv without unrelated changes."},
    {"kind":"E","reference":"Current project-local .venv is ignored/untracked but resolves its Python prefix inside the FUSE repository; ordinary shell has no UV_PROJECT_ENVIRONMENT or pycache/tool-cache redirection, ten repository __pycache__ directories and local caches exist, and rclone logs show too_many_write_operations including .venv files."},
    {"kind":"I","reference":"STRATEGIC_HOME/workorders/007-k-external-development-environment-reconnaissance.md SHA-256 ed0c1a36dd7e0fef5a5899a867ac15b353d70da340d6167d7c002c41b7ecfa48 fixes uv, portability, optional-direnv, cache, deletion, validation and coding-profile boundaries before mutation."},
    {"kind":"A","reference":"Objective-001 development contract and scripts/verify_development_baseline.py already require native external environments/caches for authoritative checks; S-ORDER-03 permits same-PR suffix 007-k after verified 007-j, and the requested correction directly removes the current objective FUSE failure."}
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
  "lr": ["LR-012", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Research reproducibility", "OAP bootstrap acceptance", "OAP report history", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

Human-authorized same-PR infrastructure correction after immutable 007-j. This
round preserves the locked uv dependency model while moving the ordinary persistent
developer environment and generated caches off the shared Dropbox/rclone FUSE tree.
It also performs the expressly authorized exact cleanup only after replacement proof.

Mandatory private source, read in full:

- `STRATEGIC_HOME/workorders/007-k-external-development-environment-reconnaissance.md`,
  SHA-256 `ed0c1a36dd7e0fef5a5899a867ac15b353d70da340d6167d7c002c41b7ecfa48`.

## Provenance

The owner's current direction fixes the storage split, multi-machine behavior,
no-copy recreation, portable `$HOME` paths, cleanup order and validation. Existing
objective-001 native-runner behavior and observed FUSE throttling supply architecture
and evidence provenance. No generated roadmap item authorizes adjacent product work.

## Current verified state

Remote main is `ee2d1b479719009ff1d07829478f241e3f395f7c`; local/remote
branch and open/unmerged PR #8 head are
`f752e8f3ddd9a8bf9bec2f20e789d512da67990b`, the immutable 007-j report
commit. Active/report are 007-j; CRITICAL has no admitted entries. The working tree
is clean. The project is a Python 3.12 uv project with committed `uv.lock`; the
ignored/untracked `.venv` is inside the FUSE repository and no external persistent
environment presently exists.

## Governance

S-AUTH-01, S-STATE-01, S-ORDER-01/03, S-EVIDENCE-01, S-PROTOCOL-01,
S-REVIEW-01 and the exact human deletion authority apply. Product/corpus/model
semantics do not change. The target Qwen service and experimental evidence are not
part of this migration. The coding invocation itself must use the human-selected
`qwen-neumann` Codex profile without copying its bearer into Dropbox.

## Goal and dependencies

Make ordinary multi-machine uv development use a clean machine-local environment at
`$HOME/envs/llm-slovenian-repair`, direct Python/tool caches outside the repository,
preserve the shared lock/source tree, and remove the verified old project-local
environment only after the new path passes sync and smoke tests.

## Scope

Add one canonical sourceable project-environment helper, one executable bootstrap/
sync helper, optional tracked `.envrc`, focused tests and concise development/README
documentation. Adjust `.gitignore` only to track that exact `.envrc` while retaining
all environment/cache ignores. Recreate from `uv.lock`, validate, then delete only
the exact authorized project-local environment/caches. Update PR metadata and publish
the immutable 007-k OAP report. No other repository or private evidence change.

## Non-goals

No dependency/version/lock change, package-manager migration, global shell-profile
mutation, mandatory direnv installation, environment copy/move, system Python change,
global bytecode disable, Docker/CI architecture rewrite, application/product/research
semantic change, Qwen service/model/config mutation, source/corpus acquisition, PR
merge, release or deployment. Do not repair the inherited application mypy defect.

## Files and boundaries

Expected repository scope: `.gitignore`, new `.envrc`, new small scripts under
`scripts/`, focused contract tests, `docs/DEVELOPMENT.md`, and a minimal README link
or note. Touch the existing baseline driver/workflow only if a direct failing test
proves a minimal compatibility change; preserve its disposable-native semantics.
OAP changes are exact 007-k order/active/report only. Machine-local environment and
caches are not Git artifacts.

## Requirements

1. Reconcile exact clean head, main, branch, PR, active/report and prior artifact
   identities. Preserve all source, Git/OAP history, lockfiles, experiments and
   private research evidence. Commit no generated environment/cache file.
2. Preserve `pyproject.toml`, `uv.lock`, Python 3.12 and uv dependency-management
   semantics byte-for-byte unless an actual unavoidable compatibility defect is
   proved. Synchronization uses normal `uv sync --frozen`; never copy/move `.venv`.
3. Add a canonical sourceable POSIX shell helper that derives project name/path from
   checked-in policy and `$HOME`, validates nonempty absolute HOME, and exports:
   `UV_PROJECT_ENVIRONMENT=$HOME/envs/llm-slovenian-repair`, matching `VIRTUAL_ENV`,
   environment `bin` first in PATH exactly once, and project-specific machine-local
   `PYTHONPYCACHEPREFIX`, `RUFF_CACHE_DIR`, `MYPY_CACHE_DIR`, pytest cache and TMPDIR.
   Preserve unrelated existing environment options rather than overwriting them.
4. The helper creates only the exact project-specific local parent/cache directories,
   never the uv environment itself, with safe ownership/type/symlink/outside-repo
   checks where applicable. Repeated sourcing is idempotent. Executing instead of
   sourcing must fail with a concise instruction rather than pretend activation.
5. Add an executable bootstrap helper that imports the same canonical environment,
   validates repository identity, uv version constraint and Python 3.12 availability,
   rejects a missing/unsafe/home-or-repository-overlapping environment, creates the
   machine-local target through uv and runs `uv sync --frozen`. It may expose a
   no-network/check mode for tests but must not duplicate dependency declarations.
6. Add a tracked minimal `.envrc` that only sources the canonical helper. Remove or
   override `.gitignore` for this exact `.envrc` while retaining ignores for `.venv`,
   all `__pycache__`/pyc, `.pytest_cache`, `.mypy_cache`, `.ruff_cache` and other
   environment names. Direnv is optional and is neither installed nor required by
   tests; document `direnv allow` as the one-time automatic-cd option.
7. Provide a no-direnv workflow requiring at most one simple source command per shell,
   followed by ordinary `uv sync`, `uv run`, `python`, pytest, Ruff and mypy use.
   Document that a plain shell cannot receive exported variables from an executed
   child and therefore must source the helper or use optional direnv.
8. Add focused tests using a controlled native temporary HOME that prove exact
   `$HOME`-relative paths, no hard-coded usernames, PATH idempotence, environment/
   cache paths outside the repository, wrong use/execution failure, unsafe HOME/path
   rejection, exact `.envrc` delegation, ignores, bootstrap argument/error behavior,
   unchanged lock/project metadata and no default network during unit tests.
9. Before destructive cleanup, source the helper with the actual HOME, run the real
   bootstrap/normal `uv sync --frozen`, and prove the new target is a real owned
   machine-local environment outside `/home/ubuntu/workspace` and outside the repo.
   Verify its `bin/python` reports Python 3.12, `sys.prefix` equals the resolved target,
   package import resolves through the external environment, and installed pytest/
   Ruff/mypy identities match the lock constraints.
10. Prove `python` in the configured project shell and `uv run python` both resolve to
    the external environment. Prove `sys.pycache_prefix` equals the local cache path;
    run a controlled import/compile and verify no repository `__pycache__`/pyc is
    created while expected bytecode appears only beneath the machine-local prefix.
11. Run focused environment tests, the relevant objective-001 contract tests, normal
    project smoke/full pytest as proportionate, Ruff and mypy at the external path.
    Preserve inherited failures distinctly; do not loosen tests or repair unrelated
    application code.
12. Only after requirements 9–11 pass, resolve exact non-symlink targets and remove
    the ignored/untracked repository `.venv`, `.pytest_cache`, `.mypy_cache`,
    `.ruff_cache`, and rebuildable repository `__pycache__`/pyc outside `.git`.
    Do not follow symlinks or use an unresolved/broad/globbed target. Let the bounded
    FUSE cleanup finish; report targets/counts and recoverability (recreatable only).
13. In a fresh configured shell after cleanup, run `uv sync --frozen` and `uv run`
    again. Verify the external prefix remains active and no `.venv` or named cache/
    bytecode tree is recreated under the shared repository. Verify Git status contains
    only ordered tracked changes and the shared project/lock/research artifacts remain.
14. Document exact first-use steps on another machine: install compatible uv and
    Python 3.12 if absent, clone/mount/open the shared project, source the helper then
    run bootstrap/sync; or optionally install/enable direnv and run `direnv allow`
    once. Dependency updates travel only through committed `pyproject.toml`/`uv.lock`;
    each machine reruns locked sync into its own `$HOME/envs` path.
15. Run publication/privacy, transcript, governance, report-history, acquisition,
    accepted-base whitespace, protected-source diff, Git fsck and final-head GitHub
    checks. No Qwen target calls, source downloads, merge or deployment.
16. Perform strongest-reason-not-to-publish review: unqualified uv still creates
    `.venv`; helper is not sourced by `.envrc`; dynamic paths hard-code this host;
    PATH duplicates; cache still lands in repo; sync mutates the lock; Python/tool
    prefix is old; cleanup precedes proof, follows a symlink, targets too broadly or
    removes durable artifacts; another machine cannot reproduce; CI/native baseline
    semantics regress; or docs imply direnv is mandatory. Correct only actual 007-k
    defects.
17. Publish all non-report changes and update PR #8 metadata through GitHub only.
    Final report commit changes only
    `oap/reports/007-k-migrate-development-environment-off-fuse.md`, has the exact
    implementation head as sole parent, is pushed/remotely verified, sends exact OK,
    and stops. Do not merge or start another round.

## Acceptance criteria

- `$HOME/envs/llm-slovenian-repair` is freshly synchronized from the unchanged lock
  and is the verified Python/uv-run/tool prefix.
- Ordinary configured commands write environment, bytecode and named caches only to
  machine-local paths; repository `.venv` and transient caches are absent and are not
  recreated by a second locked sync/run.
- The shared helper, optional `.envrc`, bootstrap, tests and documentation provide a
  portable `$HOME`-relative first-use workflow on each sequential machine.
- Only exact rebuildable local artifacts were removed after proof; repository history,
  project metadata, experiments and private evidence remain intact.
- PR #8 remains open/unmerged and the immutable report is remotely verified.

## Verification

Run requirements 8–16 at the exact relevant heads. The real sync and destructive
cleanup are ordered acceptance boundaries, not unit fakes. Record commands without
printing complete environments, credentials or unrelated local paths. Final-head CI
is evidence, not merge authority.

## Local setup and constraints

Network package access is permitted only for the ordinary lock-driven uv sync if the
machine-local uv cache is insufficient. Use compatible installed uv/Python or install
ordinary user-local tooling if needed; do not ask the owner to relay commands. The
new persistent environment is machine-local and rebuildable. Cleanup authority is
limited to exact repository-local ignored transient trees after validation.

## Documentation

Update development/README guidance with exact portable source/bootstrap/sync/test
commands, optional direnv workflow, local paths, multi-machine lock behavior, cache
behavior, cleanup/no-copy rationale and first-use steps. Do not claim global shell
configuration or automatic activation where direnv is absent.

## Git and report publication

Same objective branch and PR #8. Commit/push implementation/tests/docs/order/active
and all final non-report work before the immutable report. No earlier report/order or
research record mutation. The coding agent never merges.

## Decision classification

D0. Human direction fixes the storage and deletion choice; implementation is bounded,
reversible by locked recreation and contains no production/deployment boundary.

## Deferred human adjudication

- Decision: NONE

# Work report 007-k — Migrate development environment off the shared FUSE tree

```oap-report
{
  "id": "007-k",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-k-migrate-development-environment-off-fuse.md",
  "order_sha256": "8171f2f07439c8cb117657ebcc9cb59f1b6c5cd75a41aea3371d73abc166b6ea",
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
  "publication_commit": "SELF",
  "implementation_head": "2b955c1b71a894cf99b89da2b6742761ae520f78",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "f752e8f3ddd9a8bf9bec2f20e789d512da67990b",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 oap/bin/check_state.py --repo-root .",
      "result": "PASSED",
      "details": "Startup reconciliation reported RECOVERY_REQUIRED for active 007-k without a report, the expected signature of the interrupted round; order ID, branch oap/007-concept-verification, PR 8, base ee2d1b4, and remote head f752e8f all matched the immutable order, so the same ID/branch/PR was resumed from the first unfinished requirement.",
      "sha": "f752e8f3ddd9a8bf9bec2f20e789d512da67990b",
      "publication_head_claim": false
    },
    {
      "command": "full content audit of every tracked file against the git index (hash-object per file)",
      "result": "PASSED",
      "details": "A Dropbox/rclone FUSE stat-cache artifact had masked the oap/active 007-j to 007-k transition from git status/diff; the content audit found exactly the expected in-flight 007-k working set (.gitignore, README.md, docs/DEVELOPMENT.md, oap/active) and no other hidden tracked changes. oap/active was staged by forced content-based index update.",
      "sha": "f752e8f3ddd9a8bf9bec2f20e789d512da67990b",
      "publication_head_claim": false
    },
    {
      "command": "mandatory private source full read with SHA pin verification (STRATEGIC_HOME workorder 007-k reconnaissance)",
      "result": "PASSED",
      "details": "007-k-external-development-environment-reconnaissance.md read in full; SHA-256 ed0c1a36dd7e0fef5a5899a867ac15b353d70da340d6167d7c002c41b7ecfa48 matches the order pin exactly.",
      "sha": "f752e8f3ddd9a8bf9bec2f20e789d512da67990b",
      "publication_head_claim": false
    },
    {
      "command": "configured-shell environment resolution proof (helper sourced in clean env -i shell with real HOME): exports, PATH idempotence, uv sync --frozen, python and uv run python prefix, package import, tool identities",
      "result": "PASSED",
      "details": "UV_PROJECT_ENVIRONMENT/VIRTUAL_ENV = $HOME/envs/llm-slovenian-repair; environment bin first in PATH exactly once across repeated sourcing; cache/TMPDIR variables exactly $HOME/.cache/{python-pycache,ruff,mypy,pytest,tmp}/llm-slovenian-repair; uv sync --frozen reported 'Checked 23 packages' with no lock mutation; python 3.12.3 and uv run python both report prefix = external environment; llm_slovenian_repair import resolves through the external environment; pytest 9.1.1, ruff 0.16.6, mypy 2.3.1 match the committed uv.lock; the environment lives on the native ext4 root, outside /home/ubuntu/workspace (fuse.rclone) and outside the repository.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "bytecode placement proof: sys.pycache_prefix plus controlled import/compile with repository __pycache__/.pyc before/after snapshots",
      "result": "PASSED",
      "details": "sys.pycache_prefix equals the machine-local prefix; the controlled import created zero new __pycache__ directories and zero .pyc files under the shared repository while expected bytecode appeared only beneath $HOME/.cache/python-pycache/llm-slovenian-repair; uv.lock and pyproject.toml are byte-identical before and after the locked sync.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_007_env.py -v",
      "result": "PASSED",
      "details": "All 18 focused 007-k environment contract tests passed: exact $HOME-relative paths, no hard-coded usernames or hostnames, PATH idempotence, outside-repository targets, execution-refusal instruction, unsafe HOME rejection, unrelated environment option preservation, root resolution without override, exact .envrc delegation, retained environment ignores, bootstrap --check plan, argument/HOME/overlap/symlink/uv-version/lockfile rejection, and unchanged project metadata.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py -q",
      "result": "PASSED",
      "details": "All 13 relevant objective-001 development contract tests passed against the new environment workflow; the disposable-native baseline driver semantics are unchanged.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "Canonical local OAP bootstrap acceptance suite completed: Ran 129 tests in 705.086 s, OK (this run completed without the FUSE metadata stall documented in 007-j).",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest -q (full local project suite)",
      "result": "FAILED",
      "details": "528 passed, 1 failed, 77 subtests passed in 679.31 s. The single failure is concept-verification/tests/test_concept.py::ConceptTests::test_proxy_stops_at_terminal_event_without_eof, a load-dependent intermittent test that passed 3 of 3 standalone runs (16/16 each) at the same head; it is unchanged by 007-k (last modified in 007-b), is not in the ordered 007-k scope, and is not part of any required GitHub check. Before the in-round bootstrap-manifest correction, the same full run also failed 23 OAP acceptance/process-boundary tests with SOURCE_GENERATION_DRIFT: .gitignore; after the correction all 24 previously failing tests passed 24/24 in a clean sequential run.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 ruff check src scripts tests",
      "result": "PASSED",
      "details": "Ruff check passed for the entire baseline target set, including the new 007-k helper, bootstrap, and test files.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 ruff format --check on the 007-k files",
      "result": "PASSED",
      "details": "The new tests/contract/test_objective_007_env.py was ruff-formatted in round and then passed the format check; 14 pre-existing unformatted files from earlier rounds were left untouched (the authoritative baseline driver runs ruff check only).",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 mypy src tests/contract",
      "result": "FAILED",
      "details": "Inherited failure preserved distinctly: Found 11 errors in 1 file, all in scripts/verify_source_artifact.py (stat_result/ZipInfo typing), identical to the inherited final-head Application baseline failure recorded in 007-j. Zero errors in 007-k code or any file touched this round. Repairing the inherited defect is an explicit non-goal of this order.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "details": "Governance structure valid at the implementation head, including the newly published 007-k order and active record; semantic and human authorization proofs remain false by design.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "39-report history and the two frozen historical incidents remained valid at the implementation head before this report.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD",
      "result": "PASSED",
      "details": "Cumulative acquisition history valid at 14 with no new source acquisition in this round.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py for accepted OAP and application bases",
      "result": "PASSED",
      "details": "Both accepted-base whitespace checks (--base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a and --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da, --revision HEAD) passed with exactly the three pre-existing frozen blank-at-EOF incidents.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-k",
      "result": "PASSED",
      "details": "Committed transcript coherence verified against expected id 007-k (39 reports) at the implementation head.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs --no-progress",
      "result": "PASSED",
      "details": "Git object integrity passed; pre-existing dangling scratch objects were preserved.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/publication_guard.py --root research; --staged-tree .",
      "result": "PASSED",
      "details": "The public research tree (145 files) and the staged non-report publication tree passed the privacy guard; no raw rows, targets, replacements, prompts, responses, credentials, or private paths were present.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No changes to any protected source path relative to the accepted application base.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "git diff --name-only f752e8f3..2b955c1b scope audit",
      "result": "PASSED",
      "details": "The implementation commit changes exactly the 11 ordered paths: .envrc, .gitignore, README.md, docs/DEVELOPMENT.md, oap/BOOTSTRAP-MANIFEST.sha256, oap/GENERATED-FILES.json, oap/active, oap/orders/007-k-migrate-development-environment-off-fuse.md, scripts/bootstrap_dev_env.sh, scripts/project_env.sh, tests/contract/test_objective_007_env.py. The two OAP manifest files are the mechanical generated-file hash recording for the ordered .gitignore/README.md change, matching the established same-commit manifest-recording pattern (e.g., 006-j).",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "fresh configured shell after all changes: uv sync --frozen, uv run python prefix check, repository cache/bytecode snapshot diff",
      "result": "PASSED",
      "details": "uv sync --frozen reported 'Checked 23 packages'; uv run python prefix equals the external environment; repository __pycache__/.pyc snapshot unchanged (single pre-existing oap/bin/__pycache__ legacy entry only); uv.lock unchanged; the legacy .venv and the three named repository caches remain present and untouched per the owner override.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "GitHub required checks at PR #8 head f752e8f3 (pre-push observation)",
      "result": "PASSED",
      "details": "Research reproducibility pass; OAP bootstrap acceptance pass; OAP report history pass; Application baseline fail on the inherited verify_source_artifact.py mypy errors (unchanged, no application code changed in this round).",
      "sha": "f752e8f3ddd9a8bf9bec2f20e789d512da67990b",
      "publication_head_claim": false
    },
    {
      "command": "GitHub required checks at PR #8 head 2b955c1b",
      "result": "PENDING",
      "details": "Queued on the remote after the implementation push; final-head CI is not observable inside this pre-push report and is not claimed. Strategy verifies at publication review.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    },
    {
      "command": "gh pr edit 8 --repo ulfe-lmi/llm-slovenian-repair --body (data-free 007-k metadata)",
      "result": "PASSED",
      "details": "PR #8 metadata updated through GitHub only to the data-free 007-k scope, owner-override record, and durable links; PR #8 remains OPEN and UNMERGED.",
      "sha": "2b955c1b71a894cf99b89da2b6742761ae520f78",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-13T14:34:50+02:00",
  "report_written_at": "2026-09-13T14:44:09+02:00",
  "implementation": "Added the canonical sourceable POSIX helper scripts/project_env.sh (derives the project name from pyproject.toml and every persistent path from $HOME; exports UV_PROJECT_ENVIRONMENT, VIRTUAL_ENV, exactly-once-first environment bin in PATH, and project-specific machine-local PYTHONPYCACHEPREFIX/RUFF_CACHE_DIR/MYPY_CACHE_DIR/pytest cache/TMPDIR while preserving unrelated user values; creates only exact project-specific parent/cache directories; refuses execution, unsafe HOME, symlinks, and repository-overlapping targets). Added executable scripts/bootstrap_dev_env.sh (validates repository identity, the checked-in uv constraint, and Python 3.12, then runs the normal uv sync --frozen; supports --check). Added tracked delegating .envrc, 18 focused contract tests, the .gitignore exception for the exact root .envrc, and development/README documentation. Recorded the ordered .gitignore/README.md bytes in oap/GENERATED-FILES.json and oap/BOOTSTRAP-MANIFEST.sha256 (mechanical generated-file hash recording, same-commit pattern established in 006-j). Published the 007-k order and activated 007-k. The implementation head is 2b955c1b71a894cf99b89da2b6742761ae520f78 on oap/007-concept-verification; the external environment at $HOME/envs/llm-slovenian-repair (Python 3.12.3, lock-identical tools) was created and verified in the interrupted first half of this round and was preserved untouched.",
  "documentation": "docs/DEVELOPMENT.md gained the machine-local environment section (path table, first-use steps, sourcing semantics, optional direnv workflow, multi-machine lock behavior, and truthful legacy-tree status); README.md gained a short pointer; both report that the pre-existing repository-local .venv and named caches remain in place as inactive legacy data rather than claiming removal.",
  "criteria": "Under the owner-revised scope: $HOME/envs/llm-slovenian-repair is freshly synchronized from the byte-identical lock and is the verified python/uv-run/tool prefix (3.12.3; pytest 9.1.1, ruff 0.16.6, mypy 2.3.1 per uv.lock); ordinary configured commands write environment, bytecode, and named caches only to machine-local paths with zero new repository bytecode; the shared helper, .envrc, bootstrap, 18 focused tests, and documentation provide a portable $HOME-relative workflow; only exact rebuildable local debugging artifacts created this round were removed; repository history, project metadata (pyproject.toml/uv.lock byte-identical), experiments, and private evidence remain intact; PR #8 remains open/unmerged. Order requirement 12 and the deletion-dependent parts of requirement 13 and acceptance were superseded by the live owner override recorded below.",
  "negative_paths": "Contract tests prove execution-refusal with a concise instruction, missing/relative HOME rejection, unsafe environment target rejection, repository-overlap rejection, symlink environment refusal, unknown/excess bootstrap argument rejection, unsupported uv version rejection, missing lockfile rejection, PATH idempotence across repeated sourcing, preservation of unrelated user environment values, exact .envrc delegation (no network or export content), retained ignores for .venv/__pycache__/pyc/.pytest_cache/.mypy_cache/.ruff_cache and nested .envrc while the exact root .envrc is tracked, and unchanged project metadata hashes. An unqualified uv run (helper not sourced) was observed to attempt rebuilding the repository-local .venv and fail mid-deletion on FUSE ENOTEMPTY; all subsequent uv operations were run in configured shells, and no unqualified uv was run again. The bootstrap manifest drift (SOURCE_GENERATION_DRIFT: .gitignore) that broke 23 local OAP tests after the ordered .gitignore change was located, corrected by hash recording, and proven fixed by a 24/24 re-run.",
  "boundary_fidelity": "Only the exact 007-k implementation, documentation, order, active, and generated-file manifest recordings changed in the implementation commit. No dependency/version/lock change, no package-manager migration, no global shell-profile mutation, no direnv installation, no environment copy/move, no system Python change, no Qwen service/model/config mutation, no source acquisition, no merge or deployment. Per the live owner override: no deletion, rename, purge, or remote mutation of the legacy .venv or repository caches was performed or retried; rclone was not restarted or reconfigured; the interrupted round's deletion attempt was abandoned exactly where it left the legacy tree.",
  "setup": "Resumed the interrupted 007-k round after state reconciliation: check_state RECOVERY_REQUIRED for active 007-k without report (expected), content-based audit of all tracked files exposing a FUSE stat-cache mask on oap/active, remote main ee2d1b4 and branch head f752e8f verified, PR #8 OPEN/MERGEABLE verified. This round's owned debugging artifacts were identified by creation time (12:43-12:58) and content: the accidental repository file 'for' (shell trace artifact) and 35 /tmp probe scripts/fake-home/fake-bootstrap/fake-path/fake-trace fixtures, all removed. Research-suite temp directories under the configured TMPDIR are by-design test artifacts (recreated on every suite run) and were left in place.",
  "privacy": "No credentials, bearer values, endpoint values, profile paths, or private root paths appear in this report, the PR metadata, or any public file. The publication guard passed on the research tree and the staged publication tree. Debugging probes were removed; no probe content is reproduced here beyond public artifact names and counts.",
  "limits": "No Qwen target calls, no source downloads, no network fetches beyond the ordinary lock-driven uv sync (which required none: 'Checked 23 packages'). All validation ran offline against the external machine-local environment. Local full-suite runtime 679.31 s; OAP suite 705.086 s; bounded diagnostics only.",
  "human_gates": "D0 / Decision NONE. CRITICAL has no admitted entries. A live human owner override received during the interrupted round supersedes order requirement 12 and the deletion-dependent parts of requirement 13 and the acceptance criteria: the repository-local .venv and repository caches are not to be deleted, renamed, purged, or remotely mutated; rclone is not to be restarted or reconfigured; the residual .venv is to be treated as inactive legacy data and reported truthfully. This round completed the remaining in-scope housekeeping only and authorizes no other scope expansion. PR #8 remains OPEN and UNMERGED; no merge, release, or deployment occurred.",
  "scope": "Finished only the exact active 007-k order as revised by the owner override: external machine-local development environment, canonical helper, bootstrap, .envrc, tests, truthful documentation, debug-artifact cleanup, proportionate validation, and this immutable report. No next suffix or adjacent objective was assigned or started.",
  "result_summary": "COMPLETE under the owner-revised scope. The development environment migration off the shared FUSE tree is preserved and verified: configured shells resolve python, uv run, and all tools through $HOME/envs/llm-slovenian-repair with bytecode and named caches confined to machine-local paths, the lock is byte-identical, and the portable first-use workflow is documented. The legacy repository .venv and named caches remain present as inactive legacy data (the .venv in a partially reduced state after an accidental unqualified uv rebuild attempt that failed on FUSE and was not retried); requirement 12 and the deletion-dependent acceptance parts are superseded by the live owner direction. The immutable report is this sole report-only change."
}
```

## Result

The 007-k environment migration round is COMPLETE under the scope revised by the live owner override. The interrupted first half of the round had already created and verified the external environment; this resumed half finished the in-scope housekeeping, corrected one in-round defect (bootstrap manifest drift), cleaned this round's debugging artifacts, adjusted the documentation to truth, and published the implementation and this report.

## Owner override (live human direction)

A live human owner override was received during the interrupted round and is recorded here verbatim in effect:

- Abandon the entire repository-local `.venv`/cache deletion requirement.
- Do not delete, rename, purge, remotely mutate, or keep retrying deletion of `.venv` or the remaining repository caches.
- Do not restart or reconfigure rclone.
- Treat the ignored residual `.venv` as inactive legacy data and report its continued presence truthfully.
- Preserve the successful external-environment migration.
- Finish the other in-scope housekeeping only: configured uv/Python resolution to the external environment without changing the legacy `.venv`; removal of only this round's debugging artifacts (the accidental repository file `for` and the exact owned temporary probes); documentation/test adjustment so nothing falsely claims the legacy tree was removed; proportionate validation; commit/push/publish the immutable 007-k report; keep PR #8 open and unmerged; then stop.

This direction supersedes order requirement 12 and the deletion-dependent parts of requirement 13 and the acceptance criteria in the immutable order, and authorizes no other scope expansion. All of it was followed.

## Legacy tree state (reported truthfully)

The ignored repository-local trees remain present and were not deleted, renamed, purged, or remotely mutated by this round:

- `.venv` — present but in a partially reduced state. Reconnaissance recorded approximately 898 files / 72 MiB; at the end of this round the tree holds 375 files / 61 directories / about 51 MiB: `pyvenv.cfg`, `lib64`, and `lib/python3.12/site-packages` (partial) remain, while `bin/` is absent. The reduction came from an accidental unqualified `uv run --frozen --python 3.12` (helper not sourced) in the first half of this round: uv attempted to rebuild the repository-local environment and failed mid-deletion on a FUSE `Directory not empty` error. No further deletion was attempted, per the owner override. The mount's write-back may sync part of this reduction to the Dropbox remote; rclone was not restarted or reconfigured and no remote mutation was attempted. The environment is recreatable from the committed lock and remains inert for configured shells.
- `.pytest_cache`, `.mypy_cache`, `.ruff_cache` — present and intact (6/18/26 files respectively); not used by configured shells.
- `oap/bin/__pycache__` — the single remaining repository `__pycache__` directory (nine others had already been removed by the interrupted round before the override); untouched.

Configured shells never read from or write to these trees: every verification command this round ran with the helper sourced, and repository bytecode snapshots were byte-stable throughout.

## Verification summary

All required local checks at the implementation head `2b955c1b` are recorded in the metadata fence. Highlights: 18/18 focused environment tests, 13/13 objective-001 contract tests, 129/129 OAP bootstrap acceptance tests, ruff clean, mypy showing only the inherited 11-error `verify_source_artifact.py` failure, transcript/governance/report-history/acquisition/whitespace/fsck/privacy guards all passing, and the GitHub required checks at the prior final head observed as Research/OAP pass with the inherited Application baseline failure. The full local pytest run is recorded as FAILED for one load-dependent intermittent concept-verification proxy test (passed 3/3 standalone; unchanged since 007-b; outside every required GitHub check).

## Deferred human adjudication

- Decision: NONE

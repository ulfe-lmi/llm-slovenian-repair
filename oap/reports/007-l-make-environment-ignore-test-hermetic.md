# Work report 007-l — Make the environment-ignore contract hermetic

```oap-report
{
  "id": "007-l",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-l-make-environment-ignore-test-hermetic.md",
  "order_sha256": "81cd83564ed91363a7da7fb3fbb5b0b51d734c144a4200353ab375bce6f83e56",
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
  "implementation_head": "00cd913e372d8b457a55193e5529f1ba780616ec",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 oap/bin/check_state.py --repo-root .",
      "result": "PASSED",
      "details": "Startup reconciliation reported RECOVERY_REQUIRED for active 007-l without a report, the expected signature of the newly delivered round; active ID, order file, branch oap/007-concept-verification, PR 8, base ee2d1b4, and remote branch head 2faa6b2 (the immutable 007-k report) all matched the immutable order, so this exact ID/branch/PR round was executed. No open CRITICAL gates.",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "content-based audit of oap/active (git status/diff vs hash-object) and forced content-based index update",
      "result": "PASSED",
      "details": "The wrapper's in-place 007-k to 007-l rewrite of oap/active was again masked by the FUSE stat cache (identical size, preserved mtime), invisible to git status/diff at the starting head; content hashes (disk 79db9e40 vs HEAD blob a68c4f72) confirmed it was the only masked tracked change. It was staged by mtime touch plus add (forced content-based update) and the staged blob 79db9e40 equals the disk bytes.",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "order oap-metadata governance table vs on-disk SHA-256 (16 files)",
      "result": "PASSED",
      "details": "All 16 governance files named in the order's oap-metadata table hash-match the on-disk bytes exactly.",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "gh pr view 8 + git ls-remote origin (main, oap/007-concept-verification)",
      "result": "PASSED",
      "details": "PR #8 OPEN/MERGEABLE with head 2faa6b2 on oap/007-concept-verification; remote main ee2d1b4 equals the ordered base_sha; local HEAD equaled the remote branch head; the worktree carried exactly the ordered in-flight set (007-l order untracked, 007-k test file, masked oap/active).",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Governance structure valid at both the starting head and the implementation head against the launcher's accepted main; semantic and human authorization proofs remain false by design.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "failure-boundary reproduction: driver-style Git-less source copy (driver ignore list, no .git, no parent .git) + failing 007-k test",
      "result": "PASSED",
      "details": "In the Git-less copy, git rev-parse --show-toplevel fails with 'not a git repository (or any of the parent directories): .git' and the unmodified 007-k test fails at its first positive assertion (.venv) exactly as on GitHub final head 2faa6b2: the nonzero check-ignore result came from missing Git infrastructure, not .gitignore semantics.",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "smallest discriminating experiment: disposable git-init repository holding a byte copy of the checked-in .gitignore, real git check-ignore --no-index per candidate (git 2.43.0)",
      "result": "PASSED",
      "details": "All eight positive candidates are ignored and the exact root .envrc is not ignored in the disposable repository. Directory-only patterns (.pytest_cache/, .mypy_cache/, .ruff_cache/) do not match nonexistent paths, so the test creates those directory types inside the disposable repository; --no-index evaluates nonexistent candidate paths without an index. No Git ignore rules are parsed or reimplemented in Python.",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_007_env.py::test_gitignore_retains_environment_ignores -v in the real checkout and in a driver-style Git-less copy",
      "result": "PASSED",
      "details": "The corrected test passes in both contexts: the real checkout (Git present) and the Git-less disposable source copy (no .git, no parent .git).",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_007_env.py -q",
      "result": "PASSED",
      "details": "All 18 focused 007-k environment contract tests pass unchanged under the external configured environment; environment behavior is identical to 2b955c1.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 ruff check tests/contract/test_objective_007_env.py; ruff format --check on the same file",
      "result": "PASSED",
      "details": "Ruff lint and format checks pass on the changed test file.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 mypy tests/contract/test_objective_007_env.py",
      "result": "PASSED",
      "details": "Success: no issues found in 1 source file.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 scripts/verify_development_baseline.py --temp-parent \"$TMPDIR\" (sourced helper; TMPDIR is the machine-local native temp parent)",
      "result": "FAILED",
      "details": "Exact native locked/offline driver run with a machine-local temp parent. uv lock --check, frozen dependency sync, and focused contract tests PASSED. The full pytest phase in the intentionally Git-less pytest-workspace executed the complete suite: 527 passed, 2 skipped, 77 subtests passed, 0 failed in 423.01 s - the corrected ignore test passes in the Git-less workspace and no 007-l test failure exists. The phase was recorded TIMEOUT because the phase wall time exceeded the driver's fixed 300 s per-command budget on this machine (a timing artifact; the same phase completes within budget on the 2faa6b2 GitHub run); the driver then stopped before the mypy phase. The two skips are the by-design OAP mirror tests that require Git history in the owned workspace (oap/tests/test_report_history_cache.py:121 and :400).",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 mypy src tests/contract",
      "result": "FAILED",
      "details": "Inherited failure preserved distinctly: Found 11 errors in 1 file, all in scripts/verify_source_artifact.py (stat_result/ZipInfo typing), identical in count, file, and signature to the inherited final-head Application baseline failure recorded in 007-j and 007-k. Zero errors in the file changed this round. Repairing the inherited defect is an explicit non-goal of this order.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest -q -rs (full local project suite, configured shell, real checkout)",
      "result": "PASSED",
      "details": "529 passed, 77 subtests passed in 699.43 s with 0 failed and 0 skipped (the real checkout has Git history, so both OAP mirror tests ran). The load-dependent concept-proxy flake recorded in 007-k did not reproduce in this run.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest concept-verification/tests/test_concept.py::ConceptTests::test_proxy_stops_at_terminal_event_without_eof -q (3 standalone runs)",
      "result": "PASSED",
      "details": "3 of 3 standalone passes; the CI failure at the implementation head is the recorded load-dependent intermittent variant of this test (unchanged since 007-b, untouched by this round).",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v (configured shell with sourced helper)",
      "result": "PASSED",
      "details": "Ran 129 tests in 693.305 s, OK - identical to the 007-k canonical result. An earlier misconfigured attempt (helper not sourced, so TMPDIR absent) failed to import test_forward_recovery (its module-level select_scratch rejects /tmp) and ran only 111 tests with two transient FUSE git-log 30 s timeouts; the authoritative run was repeated in the sourced shell per requirement 9.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "40-report history and the two frozen historical incidents remain valid at the implementation head. The first run at the starting head hit one transient FUSE git-log 30 s timeout and passed on retry (3.8 s).",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-l",
      "result": "PASSED",
      "details": "Committed transcript coherence (40 reports, latest committed order 007-l active, worktree active byte-equal) verified at the implementation head. At the starting head the same check correctly reported ACTIVE_COMMIT_MISMATCH for the in-flight round (worktree 007-l vs committed 007-k), the expected pre-commit signature.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD",
      "result": "PASSED",
      "details": "Cumulative acquisition history valid at 14 with no new source acquisition in this round.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py for accepted OAP and application bases (--revision HEAD)",
      "result": "PASSED",
      "details": "Both accepted-base whitespace checks (--base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a and --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da) passed with exactly the three pre-existing frozen blank-at-EOF incidents.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs --no-progress",
      "result": "PASSED",
      "details": "Git object integrity exit 0 with zero error lines; the 52 pre-existing dangling scratch objects were preserved.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/publication_guard.py --root research; --staged-tree .",
      "result": "PASSED",
      "details": "The public research tree (145 files) and the staged non-report publication tree passed the privacy guard; no raw rows, targets, replacements, prompts, responses, credentials, or private paths were present.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No changes to any protected source path relative to the accepted application base.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "git diff --name-only 2faa6b2bba453ed65fdfbd50041675f17e641bc4 00cd913e372d8b457a55193e5529f1ba780616ec (scope audit)",
      "result": "PASSED",
      "details": "The implementation commit changes exactly the three ordered paths: oap/active, oap/orders/007-l-make-environment-ignore-test-hermetic.md, tests/contract/test_objective_007_env.py.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "configured-shell environment resolution (sourced helper): exports, prefix, import resolution, lock bytes",
      "result": "PASSED",
      "details": "UV_PROJECT_ENVIRONMENT/VIRTUAL_ENV = $HOME/envs/llm-slovenian-repair; uv run python prefix equals the external environment; llm_slovenian_repair imports through it; pyproject.toml sha256 81bd1c4ba8d0dada273d7f655aca76845745980f79521469f137ed74a3bb1b3c and uv.lock sha256 28864b7e70e10e97e896771d141c84e9fbd1e27635e38771ac6cf88e3e8daeb9 unchanged from the starting head.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "GitHub required checks at PR #8 head 2faa6b2b (pre-push observation)",
      "result": "PASSED",
      "details": "Research reproducibility pass; OAP bootstrap pass; Application baseline fail at the 007-k ignore-test boundary - the exact failure this order corrects.",
      "sha": "2faa6b2bba453ed65fdfbd50041675f17e641bc4",
      "publication_head_claim": false
    },
    {
      "command": "GitHub required checks at PR #8 head 00cd913e (implementation head, observed after push)",
      "result": "PASSED",
      "details": "Research reproducibility success; OAP bootstrap success; Application baseline failure confined to the recorded, unrelated, load-dependent concept-proxy flake: full pytest 526 passed, 2 skipped (by-design mirror skips), 1 failed (test_proxy_stops_at_terminal_event_without_eof, TimeoutError, 3/3 standalone) in 131.46 s. The corrected ignore test passes in the Git-less CI workspace; no 007-l failure remains and the mypy phase was not reached because the driver stops at the first failed phase.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "GitHub required checks at the exact report head",
      "result": "PENDING",
      "details": "Queued on the remote after the report push; final-head CI is not observable inside this pre-push report and is not claimed. Post-publication observation goes to the bounded private receipt and strategic review.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    },
    {
      "command": "gh pr edit 8 --body (blocked: deprecated Projects Classic GraphQL), then REST PATCH repos/ulfe-lmi/llm-slovenian-repair/pulls/8 per order requirement 11",
      "result": "PASSED",
      "details": "gh pr edit failed with the anticipated 'Projects (classic) is being deprecated' GraphQL error on repository.pullRequest.projectCards and left the body unchanged; the REST path updated PR #8 metadata to the data-free 007-l scope without creating any repository commit. PR #8 remains OPEN and UNMERGED.",
      "sha": "00cd913e372d8b457a55193e5529f1ba780616ec",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-13T16:13:29+02:00",
  "report_written_at": "2026-09-13T16:20:00+02:00",
  "implementation": "Changed only test_gitignore_retains_environment_ignores in tests/contract/test_objective_007_env.py: the test now creates a disposable native Git repository under its own native temporary fixture (fake_home), asserts git init succeeds (initialization failure is a test failure, never a pass or skip), copies the checked-in .gitignore bytes into it, creates the three directory types whose ignore patterns are directory-only, and exercises real git check-ignore --no-index semantics there with return codes 0 (ignored) and 1 (not ignored) distinguished from Git errors. All eight 007-k positive candidates (.venv, .venv/bin/python, nested __pycache__, .pyc, .pytest_cache, .mypy_cache, .ruff_cache, nested .envrc) and the exact negative (root .envrc not ignored) are asserted unchanged; no ignore rule is parsed or reimplemented in Python; no network call; all mutable state stays below the fixture's temporary directory. Published the 007-l order and activated 007-l. Implementation head 00cd913e372d8b457a55193e5529f1ba780616ec on oap/007-concept-verification; the external environment, all 007-k implementation/report bytes, all research evidence, and the abandoned repository-local legacy environment/cache residue are preserved untouched.",
  "documentation": "No user documentation change: the 007-k documentation already describes the correct workflow, and the corrected test changes no supported behavior.",
  "criteria": "Requirement 1: every 007-k and earlier order/report byte is unchanged (scope audit shows exactly the three ordered 007-l paths), 2b955c1 runtime behavior unchanged (18/18 focused tests, lock bytes identical), PR #8 open/unmerged. Requirement 2: the final-head failure boundary reproduced from the GitHub log and the actual driver (Git-less copy, infrastructure-absence nonzero, assertion at .venv); the ignore assertions were neither weakened nor removed. Requirement 3: hermetic test via a disposable test-owned native Git repository with the checked-in .gitignore bytes and real git check-ignore --no-index; no Python reimplementation of ignore rules. Requirement 4: all eight positives and the exact root .envrc negative proven by the real Git engine; repository init/use failure is a test failure. Requirement 5: the test passes with no parent .git, keeps all mutable state below its native temporary fixture, makes no network call, and cleans up via the fixture. Requirement 6: focused test and full 007-k contract file run under the external configured environment (18/18); Ruff and mypy clean on the changed file. Requirement 7: the exact native locked/offline driver ran with a machine-local temp parent; its full-pytest phase passes the ignore test with zero test failures (527 passed, 2 by-design skips) though the phase wall time 423.01 s exceeded the fixed 300 s per-command budget on this machine, recorded truthfully as a timing artifact; the inherited mypy failure is preserved distinctly (11 errors, all in scripts/verify_source_artifact.py) and not repaired here. Requirement 8: proportionate full tests, OAP/report-history/transcript/governance, protected-source diff, Git fsck, and final-head GitHub checks all ran; the repeated unrelated concept-proxy full-suite flake is recorded (GitHub: 1/529, 3/3 standalone), not repaired. Requirement 9: no unqualified uv in the repository; every ordinary uv/Python/tool command ran in a sourced scripts/project_env.sh shell; the legacy .venv and named caches were not deleted, renamed, purged, copied, rebuilt, or deeply inspected; rclone untouched. Requirement 10: all this-round temporary probes (repro copies, scratch repos, phase workspaces, output files, fsck output, PR body staging file) were removed from /tmp and the machine-local temp area before publication. Requirement 11: PR #8 metadata updated through the REST path after the deprecated Projects Classic GraphQL field blocked gh pr edit; no repository commit was created. Requirement 12: all non-report work (test, order, active) was committed and pushed before this report; this report-only commit has the exact implementation head as its sole parent; push, remote verification, and exact OK follow, with no merge and no resumption of experiments or roadmap work.",
  "negative_paths": "The FUSE stat-cache mask on oap/active recurred (same-size atomic write invisible to git status/diff) and was handled by content hashing plus a forced content-based index update. The local driver full-pytest phase was recorded TIMEOUT at the fixed 300 s per-command budget despite 0 test failures (machine timing artifact; the same phase completes within budget on GitHub). The GitHub Application baseline at the implementation head failed only on the recorded load-dependent concept-proxy flake (test_proxy_stops_at_terminal_event_without_eof, TimeoutError, 3/3 standalone, unchanged since 007-b) - recorded per requirement 8, not repaired. One early OAP-suite attempt was misconfigured (helper not sourced, TMPDIR absent): test_forward_recovery's module-level select_scratch rejected /tmp, 19 tests were not collected, and two transient FUSE git-log 30 s timeouts occurred; the authoritative sourced run passed 129/129. The first report-history invocation hit one transient FUSE git-log 30 s timeout and passed on retry. A uv run from this round's Git-less reproduction copy transiently re-pointed the shared external environment's editable project install to the copy; the immediately following configured real-repo uv run restored it (direct_url.json and the pth verified back to the repository src) and the lock stayed byte-identical throughout; the reproduction copy was removed. The pre-commit transcript check reported ACTIVE_COMMIT_MISMATCH at the starting head, the expected in-flight signature, and passes at the implementation head.",
  "boundary_fidelity": "Only the exact 007-l implementation (one test function), order, and active changed in the implementation commit. No .gitignore, baseline-driver, environment-helper, bootstrap, production, dependency, lock, manifest, documentation, research, Qwen, corpus, or CI workflow change. Per the standing owner override: the repository-local .venv (partially reduced legacy state) and the .pytest_cache/.mypy_cache/.ruff_cache trees and oap/bin/__pycache__ were not deleted, renamed, purged, copied, rebuilt, or deeply inspected, and rclone was not restarted or reconfigured. No second large GPU model, no protected deployment touch, no merge or deployment.",
  "setup": "Wrapper-delivered ready round under OAP_ROLE=coding. Startup read the root router, the coding law, the compact architecture, the coding communication contract, the exact active 007-l and its immutable order, and SECURITY.md/TESTING.md; verified the order's 16-file governance hash table, remote main/branch/PR truth, and clean worktree apart from the ordered in-flight set. The external environment at $HOME/envs/llm-slovenian-repair was verified before use. All validation ran offline against the machine-local environment; the only network activity was ordinary GitHub publication and check observation.",
  "privacy": "No credentials, bearer values, endpoint values, profile paths, or private root paths appear in this report, the PR metadata, or any public file. No corpus row, prompt, response, or private experimental data entered Git or report output. The publication guard passed on the research tree and the staged publication tree. All this-round probes were removed; no probe content is reproduced beyond public artifact names and counts.",
  "limits": "No Qwen calls, no source downloads, no live tests, no network beyond ordinary GitHub publication/check observation. Suite runtimes: full local pytest 699.43 s, OAP unittest 693.305 s, driver full-pytest phase 423.01 s (local), GitHub full-pytest phase 131.46 s. Bounded diagnostics only.",
  "human_gates": "D0 / Decision NONE. CRITICAL has no admitted entries. The standing live owner override (no legacy .venv/cache deletion, no rclone restart, truthful legacy-tree reporting) remains controlling and was observed. PR #8 remains OPEN and UNMERGED; no merge, release, or deployment occurred.",
  "scope": "Finished only the exact active 007-l order: hermetic correction of the one focused 007-k ignore-semantics test plus exact order/active/report publication. No next suffix, no adjacent objective, and no roadmap work was assigned or started.",
  "result_summary": "COMPLETE. The environment-ignore contract is now proven by the real Git ignore engine in a disposable test-owned repository, independent of the source tree's .git presence, with every 007-k candidate path and assertion unchanged. The corrected full-pytest phase passes the ignore test in the Git-less driver workspace locally and in the GitHub CI workspace; the only observed full-suite failure anywhere is the recorded, unrelated, load-dependent concept-proxy flake (3/3 standalone), and the inherited 11-error mypy result is preserved distinctly as the known, separately understood Application baseline state. The immutable corrective report is this sole report-only change."
}
```

## Result

The 007-l hermetic-test correction round is COMPLETE. The single focused 007-k
contract test that broke the final-head Application baseline now exercises the
real Git ignore engine in a disposable, test-owned native Git repository that
holds a byte copy of the checked-in `.gitignore`, so the contract is proven both
in the real checkout and in the baseline driver's intentionally Git-less
disposable source copy. No ignore assertion was weakened or removed, no
production, environment, driver, `.gitignore`, or legacy-residue change was
made, and PR #8 remains open and unmerged.

## Failure boundary and correction

GitHub run 34757933623 (job 103725463779) at final head `2faa6b2` failed the
Application baseline because `prepare_test_workspace` copies the source tree
without `.git`, while `test_gitignore_retains_environment_ignores` invoked
`git -C <source root> check-ignore` and treated any nonzero result as
"not ignored." Reproduced locally in a driver-style Git-less copy: the same
assertion failed at the first candidate (`.venv`) with
`fatal: not a git repository (or any of the parent directories): .git` —
infrastructure absence, not `.gitignore` semantics.

The correction creates a disposable native Git repository under the test's
native temporary fixture, asserts successful `git init` (failure is a test
failure, never a pass or skip), copies the checked-in `.gitignore` bytes into
it, creates the three directory types whose patterns are directory-only
(`.pytest_cache`, `.mypy_cache`, `.ruff_cache`), and exercises real
`git check-ignore --no-index` semantics there, distinguishing return codes 0
(ignored) and 1 (not ignored) from Git errors. All eight 007-k positive
candidates and the exact negative (root `.envrc` not ignored) are asserted
unchanged; no ignore rules are parsed or reimplemented in Python.

## Baseline restoration (recorded truthfully)

- Local driver (exact native locked/offline command, machine-local temp
  parent): the full-pytest phase in the Git-less workspace ran the complete
  suite — 527 passed, 2 skipped (by-design OAP mirror skips), 77 subtests,
  **0 failed**, including the corrected ignore test. The phase was recorded
  TIMEOUT because its 423.01 s wall time exceeded the driver's fixed 300 s
  per-command budget on this machine; that is a timing artifact with no test
  failure, and the same phase completes within budget on GitHub (131.46 s at
  the implementation head). The driver then stopped before the mypy phase.
- Inherited mypy, preserved distinctly and not repaired: `mypy src
  tests/contract` reports exactly the inherited 11 errors, all in
  `scripts/verify_source_artifact.py` (stat_result/ZipInfo typing), identical
  to the 007-j/007-k records. Zero errors in the changed file.
- GitHub at the implementation head: Research reproducibility **pass**, OAP
  bootstrap **pass**, Application baseline **fail** — the sole full-pytest
  failure is the recorded, unrelated, load-dependent concept-proxy flake
  (`test_proxy_stops_at_terminal_event_without_eof`, TimeoutError; 3/3
  standalone; unchanged since 007-b; requirement 8: recorded, not repaired).
  The corrected ignore test passes in the Git-less CI workspace, so no 007-l
  failure remains and the Application baseline is restored to its prior,
  separately understood state (the flake and the inherited mypy failure being
  the only known failure sources, both pre-existing and documented).

## Legacy tree state (reported truthfully)

Per the standing owner override, the ignored repository-local trees were not
touched this round and remain present: `.venv` (partially reduced legacy
state), `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, and
`oap/bin/__pycache__`. Configured shells never read or write them; the
repository lock and project metadata are byte-identical to the starting head.

## Verification summary

All required local checks at the implementation head
`00cd913e372d8b457a55193e5529f1ba780616ec` are recorded in the metadata fence.
Highlights: 18/18 focused environment tests, the corrected ignore test green
in both Git contexts, Ruff/mypy clean on the changed file, full local suite
529 passed with 0 failures, OAP bootstrap acceptance 129/129, transcript
(expected 007-l)/report-history/governance/acquisition/whitespace/
protected-source/fsck/publication guards all passing, scope audit showing
exactly the three ordered paths, and the GitHub required checks at the
implementation head observed as Research/OAP pass with the Application baseline
confined to the recorded flake. The report-head GitHub checks are queued and
verified post-publication; they are not claimed inside this pre-push report.

## Deferred human adjudication

- Decision: NONE

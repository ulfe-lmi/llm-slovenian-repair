# Work order 007-l — Make the environment-ignore contract hermetic

Status: FINAL

```oap-metadata
{
  "id": "007-l",
  "title": "Make the environment-ignore contract hermetic",
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
  "local_work": "Clean local/remote objective branch at immutable 007-k report head 2faa6b2bba453ed65fdfbd50041675f17e641bc4. Preserve the external environment, all 007-k implementation/report bytes, all research evidence, and the owner-abandoned repository-local legacy environment/cache residue.",
  "prior_review": "Independent final-head review verified the 007-k report and remote head, but the final Application baseline failed in the new test_gitignore_retains_environment_ignores test: the native baseline driver runs tests in a copied source tree without .git, so git check-ignore returned nonzero for infrastructure absence rather than .gitignore semantics. Research reproducibility and both OAP checks passed. PR #8 remains OPEN/UNMERGED.",
  "provenance": [
    {"kind":"H","reference":"The owner classifies the environment migration as housekeeping, abandons all further repository-local environment/cache deletion, and asks to be told when normal work can continue."},
    {"kind":"E","reference":"GitHub Actions run 34757933623 job 103725463779 at final head 2faa6b2 failed only because test_objective_007_env.py invoked git check-ignore in the baseline driver's intentionally Git-less pytest-workspace; the same ignore patterns work in the real checkout."},
    {"kind":"I","reference":"Strategic final-head review established the earliest failing boundary: test harness repository context, not .gitignore content, environment selection, uv synchronization, package behavior, or inherited mypy."},
    {"kind":"A","reference":"S-EVIDENCE-01 requires tests to exercise the named boundary without substituting infrastructure assumptions; S-ORDER-03 requires this post-report correction to use the next suffix on the same PR."}
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
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Human-authorized same-PR corrective suffix after immutable 007-k. Make the one
new ignore-semantics test self-contained in both the real checkout and the
baseline driver's Git-less disposable source copy. Restore the Application
baseline to its prior, separately understood state without changing environment
behavior or touching the abandoned legacy `.venv`/cache trees.

## Provenance

The owner's housekeeping scope and deletion override supply human provenance.
The exact final-head GitHub failure supplies executable evidence, strategic
review located the Git-less copied-workspace boundary independently, and the
same-PR corrective law supplies architecture/protocol provenance. No generated
roadmap item or neighboring product work is implicated.

## Current verified state

Remote main is `ee2d1b479719009ff1d07829478f241e3f395f7c`; local/remote branch
and open PR #8 head are `2faa6b2bba453ed65fdfbd50041675f17e641bc4`, the immutable
007-k report. The worktree is clean. The external environment at
`$HOME/envs/llm-slovenian-repair` is verified and the locked dependency metadata
is unchanged. Final-head Research reproducibility, OAP bootstrap acceptance, and
OAP report history pass. Application baseline fails the new ignore test before
reaching the inherited mypy boundary.

## Governance

S-STATE-01, S-ORDER-03, S-EVIDENCE-01, S-PROTOCOL-01 and S-REVIEW-01
apply. The live deletion override remains controlling: no legacy environment or
cache mutation is permitted. This is a test-harness correction only.

## Goal and dependencies

Restore the final-head Application baseline's full-pytest phase by exercising
Git ignore semantics in a test-owned repository. This depends on the accepted
objective-001 baseline and the immutable 007-k environment setup; it changes
neither.

## Scope

Change only the focused 007-k contract test as needed, plus exact 007-l
order/active/report publication. If a direct test proves a tiny supporting test
utility change unavoidable, keep it within the same test file. No production,
environment-helper, bootstrap, `.gitignore`, docs, manifest, dependency, lock,
research, Qwen, corpus, CI workflow, or baseline-driver behavior change.

## Non-goals

No deletion cleanup, product code, experiment, source acquisition, prompt/model,
benchmark, production, CI workflow, dependency, lock, documentation, release,
deployment, merge, milestone acceptance, or unrelated flaky-test repair.

## Files and boundaries

Expected implementation scope is only
`tests/contract/test_objective_007_env.py`, plus exact 007-l order/active/report
publication. Test mutable state must remain below its native temporary fixture.
The external environment and repository-local ignored residue are read-only
boundaries for this correction.

## Requirements

1. Preserve every published 007-k and earlier order/report byte and the exact
   implementation behavior at `2b955c1`. Preserve PR #8 as open and unmerged.
2. Reproduce the final-head failure boundary from the GitHub log and actual
   baseline driver: `prepare_test_workspace` copies source without `.git`, while
   the test invokes `git -C ROOT check-ignore` and interprets any nonzero result
   as “not ignored.” Do not weaken or remove the ignore assertions.
3. Make `test_gitignore_retains_environment_ignores` hermetic by creating a
   disposable native Git repository owned by the test, copying the checked-in
   `.gitignore` bytes into it, and exercising real `git check-ignore` semantics
   there. Use `--no-index` where needed so nonexistent candidate paths are
   evaluated. Do not parse or reimplement Git ignore rules in Python.
4. Continue to prove `.venv`, `.venv/bin/python`, nested `__pycache__`, `.pyc`,
   `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, and nested `.envrc` are ignored,
   while the exact root `.envrc` is not ignored. Failure to initialize/use the
   disposable Git repository is a test failure, not a pass or skip.
5. The test must work when its source tree has no parent `.git`, must create all
   mutable state only below its native temporary fixture, must make no network
   call, and must clean up normally. Add no expected linguistic result.
6. Run the corrected focused test and full 007-k contract file under the external
   configured environment. Run Ruff and mypy for the changed test file.
7. Run the exact native locked/offline `scripts/verify_development_baseline.py`
   command with a machine-local temp parent. The full pytest phase must pass the
   ignore test. Preserve any subsequently reached inherited mypy failure
   distinctly; do not repair it here.
8. Run proportionate full tests plus OAP/report-history/transcript/governance,
   protected-source diff, Git fsck, and final-head GitHub checks. A repeated
   unrelated concept-proxy full-suite flake is recorded, not repaired.
9. Do not run unqualified uv in the repository. Source `scripts/project_env.sh`
   for all ordinary uv/Python/tool commands. Do not delete, rename, purge, copy,
   rebuild, or inspect deeply inside the residual repository `.venv` or named
   caches; do not restart/reconfigure rclone.
10. Remove exact corrective-round temporary probes from `/tmp` or other transient
    locations before publication. No credential, token, corpus row, prompt,
    response, or private experimental data enters Git/report output.
11. Update PR #8 metadata through the REST path if the deprecated Projects
    Classic GraphQL field prevents `gh pr edit`; this creates no repository
    commit.
12. Commit/push all non-report work, then publish one immutable report-only
    `oap/reports/007-l-make-environment-ignore-test-hermetic.md` commit whose sole
    parent is the exact implementation head. Push/verify, send exact OK, and
    stop. Do not merge or resume experiments/roadmap work.

## Acceptance criteria

- The real Git ignore engine proves all positive and negative 007-k patterns in
  a disposable repository independent of the source tree's `.git` presence.
- The exact Application baseline passes the corrected full-pytest phase and no
  new 007-l failure remains; the known mypy result is classified accurately.
- External environment selection and all 007-k runtime behavior remain unchanged;
  the inactive repository-local legacy residue is untouched.
- PR #8 remains open/unmerged and the immutable corrective report is remotely
  verified.

## Verification

Run the focused test/file, Ruff and mypy on the changed test, and the exact native
locked/offline baseline driver. Run the transcript/report-history/governance,
protected-source and Git checks proportionately, then verify all required GitHub
checks on the exact report head. Record inherited failures distinctly.

## Local setup and constraints

Use only the already-verified machine-local environment. Source
`scripts/project_env.sh` before uv commands. Temporary test repositories must be
native and self-cleaning. No network is needed except ordinary GitHub
publication/check observation. Do not inspect or mutate the legacy `.venv`.

## Documentation

No user documentation change is expected: the 007-k documentation already
describes the correct workflow. The 007-l report records only the hermetic-test
correction and evidence.

## Git and report publication

Amend the existing objective branch and PR #8. Commit/push the test plus
order/active before creating the report. The final report commit changes only
`oap/reports/007-l-make-environment-ignore-test-hermetic.md`, has the exact
implementation head as sole parent, is pushed/remotely verified, and sends exact
OK. Do not merge.

## Decision classification

D0. This is a reversible, contained correction to test setup; it crosses no
human, deployment, data, service, or product boundary.

## Deferred human adjudication

- Decision: NONE

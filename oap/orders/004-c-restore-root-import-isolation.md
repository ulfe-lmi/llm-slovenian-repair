# Work order 004-c — Restore root import isolation

Status: FINAL

```oap-metadata
{
  "id": "004-c",
  "title": "Restore root import isolation",
  "objective": "004",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 5,
  "dependencies": ["001", "002", "003"],
  "local_work": "Clean objective branch at remote 004-b BLOCKED report head 8f236e0021420ba39ae1b541626e5919cc539ad5; preserve all prior commits/reports, ignored environments and private strategic state.",
  "prior_review": "External sceptical finding was independently confirmed against accepted main; 004-b was disposed BLOCKED without product changes because it was published before the intervention. PR #5 remains open and is the required corrective branch.",
  "provenance": [
    {"kind": "H", "reference": "Objective 001-a requirements 1,2,6 and its accepted no-eager-Pydantic/HTTPX import proof; human 2026-09-08 request for source-tree/built-wheel regression and protocol-valid remediation"},
    {"kind": "A", "reference": "Objective 003-a requirement 9, S-STATE-01/S-ORDER-03/S-EVIDENCE-01, ARCHITECTURE.md §4.1 and compact A-STACK-01"},
    {"kind": "I", "reference": "Independent review of exact accepted main dac4789: source import without Pydantic fails; built wheel bare import loads Pydantic plus 39 submodules; 003 reversed the 001 test expectation without superseding authority"}
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

004-c is the next suffix on existing objective-004 branch and PR #5. It is an
explicit roadmap remap: remediate the already-merged objective-003 regression before
resuming source-manifest work. Preserve 004-a, the BLOCKED 004-b report, and every
earlier immutable order/report/commit. Do not create a new PR.

## Provenance

- H: accepted 001-a says root exposes inert metadata/documentation and does not
  eagerly import Pydantic or HTTPX; its fresh installed-process test proved both
  absent. The human requested direct source/built-wheel remediation evidence.
- A: 003-a requirement 9 explicitly required preserving 001 import isolation. Its
  requirement 8 requested stable contract/policy exports but did not require eager
  loading or explicitly supersede 001. Canonical PLAN/ARCHITECTURE did not change.
- I: exact-main source import fails without Pydantic. Exact-main installed wheel bare
  import loads `pydantic` and 39 submodules, not HTTPX. Diff shows 003 changed the
  negative assertion to positive. Current docs still promise no eager dependency.

## Current verified state

Accepted main is `dac4789f52c9e82aec90d1cf92ce9f1194cc103a` and contains the
regression. PR #5 is the sole open PR at remote 004-b report head
`8f236e0021420ba39ae1b541626e5919cc539ad5`; 004-b implementation/disposition is
`2dddc6ab23fd5e9306afe9f30730c18589d7b5c4`. Remote SELF, exact active `004-b\n`,
complete transcript, accepted governance and both final-head checks verify.

PR #5 already contains unmerged 004-a manifest/fixture work. Do not add or resume
source-manifest behavior in this round. Branch protection remains disabled (GitHub
protection API 404; rulesets empty); do not change settings. CRITICAL remains empty.
Live repair, milestone, release and deployment authorization remain absent.

## Governance

The no-eager-root-import condition remains accepted cross-objective authority. A
green test cannot redefine it by reversing the assertion. Preserve historical bytes
and add forward remediation only. The intended root export names may remain available
through lazy attribute resolution; typing-only imports must not execute at runtime.

This deterministic regression repair is D0/NONE. It introduces no new product intent,
dependency, external right, public exposure or D2 action.

## Goal and dependencies

Restore bare `import llm_slovenian_repair` as an inert, dependency-lazy operation in
source and built-wheel environments while retaining documented 003/004 root names
through a small lazy-export mechanism. Reinstate permanent 001 regression evidence
without weakening expanded wheel payload expectations.

## Scope

1. Refactor only root `src/llm_slovenian_repair/__init__.py` for lazy exports.
2. Restore and extend objective-001 import-isolation tests.
3. Update native installed-wheel verification to test root import before explicit
   runtime dependency imports.
4. Add focused lazy-export identity/unknown-name/type-check tests as necessary.
5. Update direct docs/inventory assertions only if bytes/behavior wording requires.
6. Publish exact 004-c order/active/report on PR #5.

## Non-goals

No change to contract/policy/source-manifest semantics, fixtures, corpus work,
dependencies/lock, acceptance/detection/reviewer/patcher/pipeline/API, OAP governance,
CRITICAL, GitHub settings, live model, release or deployment. Do not delete public
names solely to make import pass, and do not eagerly preload modules through another
indirection. Do not rewrite old tests/commits/reports.

## Files and boundaries

Expected paths: root `__init__.py`, `tests/contract/test_objective_001.py`, focused
003/004 tests only if needed for lazy symbol access, native baseline driver/tests,
direct DEVELOPMENT/README/STATUS and exact inventory rows, plus 004-c protocol files.

The named boundaries are separate fresh processes for source/root import and the exact
built wheel installed outside the repository. Inspecting source text or importing in
an already-contaminated pytest process is insufficient.

## Requirements

1. Bare root import executes no `contracts`, `policy` or `source_manifest` import and
   leaves every `pydantic*` and `httpx*` module absent when they were absent before.
   It retains `__version__`, exact documented `__all__`, and no filesystem/network/
   environment/model/corpus/service side effect.
2. Retain intended 003 and current PR 004 root symbols lazily using module
   `__getattr__` with an explicit immutable name-to-(module, attribute) map and
   `TYPE_CHECKING` imports (or a simpler equally lazy design). Unknown names raise
   `AttributeError`. Resolve only trusted fixed relative modules; no caller path,
   plugin discovery, dynamic eval/exec or arbitrary import target.
3. First access to a valid typed symbol imports only its declared module/dependencies,
   returns the exact same object as explicit submodule import, and caches it in root
   globals. `dir()`/`__all__` remain deterministic. Bare import itself must not invoke
   `__getattr__` for exported names.
4. Restore objective-001's fresh-process assertion to `pydantic` and `httpx` absent;
   retain expanded `__all__` and wheel-file allowlist required by 003/004. Add a guard
   that fails if the negative is reversed again. Keep blocked socket/URL/file-creation
   and model/analyzer absence checks.
5. Add a source-tree fresh-process proof where Pydantic/HTTPX imports are blocked or
   unavailable: bare root import succeeds and exposes inert metadata without loading
   them. Then, in a dependency-installed process, access one lazy typed symbol and
   prove Pydantic loads only at that point while HTTPX remains absent.
6. At the built-wheel boundary, install the exact built artifact outside the repo.
   Snapshot modules, bare-import root, assert no Pydantic/HTTPX modules were added,
   version/exports are correct and no files were created. Only afterwards explicitly
   import/access typed contracts and verify their identity. Where practical, also
   prove the wheel's bare root imports with project dependencies omitted; distinguish
   any setup limitation truthfully.
7. Update `scripts/verify_development_baseline.py` so its offline installed-wheel
   runtime command checks the negative root-import boundary before explicitly loading
   Pydantic/HTTPX for their separate version/metadata proof. Preserve all lock/offline,
   bounded diagnostic and cleanup behavior.
8. Audit every 001 test change introduced by 003/004. Preserve legitimate wheel
   payload/export additions, restore only the contradicted Pydantic negative, and
   document that HTTPX/network/filesystem/dependency/metadata/offline invariants were
   never superseded. Do not claim older tests passed behavior they did not test.
9. Run complete product/OAP/native/transcript/governance checks and both exact final-
   head CI checks. Branch protection remains an observed risk, not a setting change.
10. Force-stage exact `004-c\n`, preserve 004-b BLOCKED history, and publish only the
    matching report as final commit. No 004 manifest correction or merge in this round.

## Acceptance criteria

1. Fresh source and exact built-wheel bare imports both add zero Pydantic/HTTPX modules
   and perform no file/network side effect; source bare import works even when those
   dependencies cannot be imported.
2. All intended root export names remain available; lazy access returns the explicit
   submodule object and Pydantic appears only after first typed access. Unknown names
   fail cleanly and no arbitrary module can be selected.
3. Objective-001 regression expectation is negative again, permanent tests cover
   source and installed wheel, and native offline verification exercises ordering at
   the actual runtime boundary.
4. No other 001 invariant is weakened; lock and package metadata are unchanged, HTTPX
   remains lazy, expanded package files remain tested, and current docs are accurate.
5. Focused/broad pytest, `ruff check src scripts tests`, mypy, full OAP suite, native
   locked/offline baseline, transcript/governance/protected checks and both required
   final-head CI checks pass at exact SHAs.
6. PR #5 remains open/unmerged during coding. Remote SELF verifies; source-manifest
   resumption, live/model/ICA/milestone/release/deployment remain blocked/unproven.

## Verification

Use fresh owned native environments and run/report:

```text
pytest tests/contract/test_objective_001.py -q
pytest tests/contract/test_objective_003.py -q
pytest tests/contract/test_objective_004.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-c
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-c
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a
git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD
git diff --exit-code dac4789f52c9e82aec90d1cf92ce9f1194cc103a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Report explicit fresh-process module deltas for source and wheel. After publication,
strategy repeats them and verifies remote SELF/final-head CI. These are import and
packaging proofs only, not functional, linguistic, live, milestone or release proof.

## Local setup and constraints

Use frozen lock and owned native `/tmp` environments/caches; no repository `.venv`.
Registry use is limited to normal frozen setup. Clean owned artifacts. No credentials,
customer/model text, corpus access, Qwen/GPU/service/network-setting mutation.

## Documentation

Keep the existing promise that root import eagerly imports no runtime dependency and
clarify lazy symbol access. Record the confirmed regression/remediation and other 001
invariants without rewriting historical reports. Record branch protection disabled.

## Git and report publication

Stay on `oap/004-source-manifests-and-miniature-synthetic-corpus`, amend only PR #5,
and preserve `2bc3cfb`/`f38f961`/`2dddc6a`/`8f236e0`. Commit/push all non-report
work, exact order and active, run CI, and record literal implementation SHA.

Then create only `oap/reports/004-c-restore-root-import-isolation.md` as a SELF
report-only commit with implementation sole parent. Push, remotely verify, send exact
`OK`, and exit. Do not merge or resume 004-b manifest work.

## Decision classification

D0. This restores an explicit accepted invariant through a reversible lazy-export
mechanism and tests; it does not choose new human intent or cross an external boundary.

## Deferred human adjudication
- Decision: NONE

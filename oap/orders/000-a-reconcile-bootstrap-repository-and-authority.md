# Work order 000-a — Reconcile bootstrap, repository and authority

Status: FINAL

```oap-metadata
{
  "id": "000-a",
  "title": "Reconcile bootstrap, repository and authority",
  "objective": "000",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "7ca26f1a6d9c110aa3c71a736d185028661d110d",
  "branch": "oap/000-reconcile-bootstrap-repository-and-authority",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [],
  "local_work": "Clean local main at 7ca26f1a6d9c110aa3c71a736d185028661d110d with no tracked or untracked changes observed at 2026-09-08T00:27:31+02:00; preserve the subsequently published order and active pointer plus any later work.",
  "prior_review": "Owner-published bootstrap baseline accepted at remote main 7ca26f1a6d9c110aa3c71a736d185028661d110d; no prior objective order, report, pull request, or objective branch exists.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Explicit operational-start instruction embodied in oap/prompts/strategic-start.md at accepted ref 7ca26f1a6d9c110aa3c71a736d185028661d110d; PLAN.md §§1.2, 12, 16"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§1, 17, 20; oap/strategic-instructions/INITIAL-ROADMAP.md objective 000-a; docs/bootstrap/specifications/WORK-PROGRAM.md §1 and row 000"
    },
    {
      "kind": "E",
      "reference": "2026-09-08 bootstrap-suite observation: the operational strategic environment failed only test_B27_live_shell_returns_after_fake_CLI_exit at CONFIG_AUTHORITY_CONFLICT before shell entry, while the focused test and all 60 tests passed in a neutral environment"
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
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance"
  ],
  "decision_class": "D0"
}
```

## Identity

000-a is the first DEMONSTRATOR objective and creates one branch and one pull
request: `oap/000-reconcile-bootstrap-repository-and-authority`. If execution is
interrupted after creating either object, recover that same branch and PR; do not
create a duplicate.

## Provenance

- H: the owner deliberately published and accepted the bootstrap baseline and
  authorized this development loop through the operational-start instruction
  versioned at `oap/prompts/strategic-start.md`; PLAN §§1.2, 12 and 16 separate
  proposed implementation from measured product evidence.
- A: ARCHITECTURE §§1, 17 and 20, INITIAL-ROADMAP objective 000-a, and WORK-PROGRAM
  §1/row 000 require the reviewed scaffold to enter the operational transcript
  without repeating bootstrap or claiming product functionality.
- E: on 2026-09-08 the ordinary full bootstrap command inherited live operational
  configuration into a nested fixture subprocess. It failed before shell entry
  with `CONFIG_AUTHORITY_CONFLICT` in
  `test_B27_live_shell_returns_after_fake_CLI_exit`. The focused test and then all
  60 tests passed in a deliberately neutral environment. Preserve this observation
  and correct the fixture-boundary interpretation; do not weaken configuration
  conflict detection.

These anchors do not require coding to load full PLAN, architecture, roadmap, or
doctrine. Use the compact read sequence and the shared hash/governance helpers.

## Current verified state

At 2026-09-08T00:27:31+02:00, GitHub repository
`ulfe-lmi/llm-slovenian-repair` is public with default branch `main` at
`7ca26f1a6d9c110aa3c71a736d185028661d110d`, identical to the configured accepted
reference and clean local `main`. There are no pull requests in any state, no
remote objective branch, no workflow runs, no repository rulesets, and `main` is
not branch-protected. Do not change repository settings in this order.

Before publication there was no `oap/active`, published order, or report; shared
state reported `INACTIVE`. CRITICAL matches its protected seed and contains no
live entries, dispositions, gates, or mitigation updates. Accepted-runtime
governance and the doctor pass with the owner-selected split layout. Role profiles,
authentication, accepted baseline, development-only merge effect, and both loop
acknowledgements are configured. Live repair testing remains disabled; product
functionality, Qwen compatibility, linguistic benefit, ICA, milestone acceptance,
release, and deployment have not been established.

The neutral-environment bootstrap acceptance run passed all 60 tests in 88.545s.
The same ordinary command in the already-configured strategic environment passed
59 and failed only the nested setup-shell fixture described under Provenance.

## Governance

The metadata identity map is the accepted `oap/governance/MANIFEST.json` map at
base SHA `7ca26f1a6d9c110aa3c71a736d185028661d110d`. Preserve PLAN, ARCHITECTURE,
CRITICAL, all dense/full role laws, compact projections, prompts, the distillation
map, source lock, historical bootstrap sources, and workspace-layout governance
byte-for-byte. Use C-READ-01, C-WORK-01, C-EVIDENCE-01, C-REPORT-01 and
P-SELF-01–03. LR-014 governs the separation between scaffold correctness, live
model compatibility, linguistic quality, ICA, and human release/deployment gates.
There is no D1 entry or applicable critical gate.

## Goal and dependencies

Adopt the owner-reviewed scaffold baseline into the first operational PR by making
its process-boundary test reliable inside the actual role environment, establishing
one minimal final-head CI check for the bootstrap seam, and correcting public status
documentation to distinguish activated development from product readiness.

There is no earlier numeric objective. This remains a scaffold/governance adoption
PR; objectives 001 and 002 still own application packaging and the broader
CPU-only application/governance CI baseline.

## Scope

1. Correct the environment isolation of the nested setup-shell survival fixture in
   `oap/tests/test_process_boundaries.py`.
2. Add a minimal `.github/workflows/oap-bootstrap.yml` workflow whose single job is
   named exactly `OAP bootstrap acceptance` and proves this scaffold at every PR
   head targeting `main`.
3. Update `README.md`, `STATUS.md`, and only directly affected runbook wording so
   they no longer claim that the accepted remote, role qualification, or operational
   loop is unresolved/inactive. Keep all product/evidence limitations explicit.
4. Preserve and commit the strategically published order and active pointer as
   protocol state. Do not rewrite their bytes.

## Non-goals

Do not regenerate the bootstrap, change canonical or compact governance, implement
repair application code, introduce Python packaging, download corpora, call Qwen,
run linguistic evaluation, modify the protected model/GPU/gateway/network, change
GitHub repository settings or branch protection, merge or enable auto-merge, create
another objective/branch/PR, or claim any milestone, release, or deployment state.
Do not relax `runtime_config` conflict rejection merely to make its fixture pass.

## Files and boundaries

Inspect and change only the smallest coherent set among:

- `oap/tests/test_process_boundaries.py` for the regression;
- `.github/workflows/oap-bootstrap.yml` for the named hosted check;
- `README.md`, `STATUS.md`, and directly contradictory wording in
  `docs/OAP-RUNBOOK.md` for durable status accuracy;
- the already-published `oap/orders/000-a-reconcile-bootstrap-repository-and-authority.md`
  and `oap/active`, which must be committed exactly as supplied.

Use shared helper entry points as the implementation boundary. Test fixtures may
create only owned disposable repositories, strategic directories, and FIFOs.
Do not edit helper authority checks unless new evidence first shows the product
boundary, rather than the fixture environment, is defective.

## Requirements

1. In the live-shell survival test, construct the nested subprocess environment so
   no ambient allowlisted runtime key or ambient `CODEX_HOME` can conflict with the
   disposable fixture's `runtime.env`; then set only the fixture-required role and
   fake-exit controls. Continue to assert the exact surviving role, cwd and role
   home after the fake CLI exits nonzero. Assert the subprocess exit/result clearly
   enough that a pre-shell configuration failure cannot appear as a shell failure.
2. Preserve the real configuration-authority boundary. The existing negative proof
   that conflicting runtime values raise `CONFIG_AUTHORITY_CONFLICT` must continue
   to pass. Do not clear or ignore conflicts in production parsing or role setup.
3. The workflow must use least privilege (`contents: read`), a finite timeout, a
   full-history checkout sufficient to resolve the literal accepted base, and the
   currently verified immutable checkout action
   `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`
   (release v7.0.1 observed 2026-09-08). It must fail if Python 3.12 or `tmux` is
   absent, run the complete bootstrap acceptance suite, run accepted-runtime
   governance against the literal base SHA, and run `git diff --check`. It must not
   use secrets, live services, Qwen, corpus data, caches, deployment, or write
   permissions.
4. Make the single job/check name exactly `OAP bootstrap acceptance`, so the name
   in order metadata is the final-head check strategy will require. Do not add a
   matrix or dynamic suffix that changes that check-run name.
5. Documentation must say only that the bootstrap baseline is owner-published and
   accepted for continued development, role operation is qualified, and the
   development loop has been deliberately started. It must direct readers to
   `oap/active`/`check_state.py` for current protocol state and continue to report
   the repair product as PLANNED, live repair tests disabled, Qwen compatibility and
   linguistic quality not established, ICA not run, and no milestone/release/
   deployment approval.
6. Before report publication, prove no canonical source, role law, compact
   projection, governance manifest/map, historical seed, or immutable input changed.
   Preserve the empty live CRITICAL register. Report any deviation instead of
   updating expected hashes or regenerating accepted sources.

## Acceptance criteria

1. The focused process-boundary suite passes when invoked directly from the
   activated coding role environment, including an actually executed
   `test_B27_live_shell_returns_after_fake_CLI_exit`; no neutral outer shell is
   required to obtain the pass.
2. The complete 60-test-or-greater bootstrap suite passes in the coding role
   environment with zero failures/errors. The tmux integration test is executed,
   not skipped; the test report states any other skip separately rather than
   treating it as proof.
3. `check_governance.py` reports accepted-runtime structure valid against
   `7ca26f1a6d9c110aa3c71a736d185028661d110d`, and an explicit accepted-source diff
   shows no changes to protected/governance identity paths.
4. A PR exists only for the ordered branch; its exact final report commit receives
   a successful GitHub check run named `OAP bootstrap acceptance`. Pending, missing,
   skipped, cancelled, or stale-head runs do not satisfy this criterion.
5. README/status/runbook claims match the operational facts while preserving the
   distinction between bootstrap evidence and every product/live/quality/audit/
   human gate.
6. `check_state.py` recognizes the exact active order without malformed-pointer,
   duplicate-history, or replay behavior. The final remote report then satisfies
   its separate SELF parent/path/bytes verification contract.
7. No repair code, corpus/model artifact, credential, private path, raw text,
   product completion claim, GitHub setting mutation, merge, release, or deployment
   is present in the diff or report.

## Verification

Run and report these focused and broader commands at the literal implementation
SHA (use an equivalent direct module selector only if unittest discovery requires
it, and record the exact command):

```text
python3 -B -m unittest discover -s oap/tests -p 'test_process_boundaries.py' -v
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 7ca26f1a6d9c110aa3c71a736d185028661d110d
python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair
git diff --check
git diff --exit-code 7ca26f1a6d9c110aa3c71a736d185028661d110d -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Inspect the workflow result at the final report head and record its exact check name,
status, conclusion and tested SHA. Negative evidence must include malformed/absent
active distinction, draft-order rejection, configuration-conflict rejection, no
duplicate model launch, and the setup shell surviving the fake CLI's nonzero exit.

The 60-test suite uses synthetic/disposable repositories, faked GitHub/model edges,
and real local filesystem/Git/FIFO/tmux boundaries. Its pass proves bootstrap
mechanics only. Hosted CI independently reproduces those mechanics at the pushed
head. Neither proves live Qwen compatibility, repair behavior, linguistic benefit,
branch-protection policy, ICA, or deployment authority.

## Local setup and constraints

Use the existing standard-library test stack and installed local Git/Python/tmux.
No package, corpus, model, browser, database, system service, or daemon setup is
needed locally. Owned temporary fixture directories and FIFOs must be finite and
cleaned by the tests. Keep real native FIFOs at their configured strict modes; do
not use them as test fixtures or send either operational FIFO from inside tests.

Do not expose role auth files, tokens, private runtime values, user/model text, or
absolute strategic-home paths in commits, Actions logs, reports, or PR prose. Do
not access or mutate Qwen weights, quantization, vLLM/CUDA, GPU allocation, running
services, ports, network/VPN/firewall, gateway, or neighboring repositories. Live
repair testing remains disabled and is outside this order.

## Documentation

Update the named public status surfaces only to remove stale bootstrap-activation
claims and describe how current protocol state is queried. Preserve the Apache-2.0
license fact already selected by the owner. State the exact evidence split:
bootstrap software mechanics tested; repair application absent/planned; live Qwen,
linguistic evaluation, ICA, milestone acceptance, release and deployment not
established. Do not publish private runtime configuration or turn proposed PLAN
measurements into results.

## Git and report publication

Start from the exact accepted base and create only
`oap/000-reconcile-bootstrap-repository-and-authority`. Commit and push all scoped
non-report changes, including the exact published order and `oap/active`, then open
the one PR before composing the report. Repair safe in-scope failures on that same
branch/PR. Do not merge or enable auto-merge.

After all non-report work is pushed, record the literal implementation head. Write
one immutable matching report at
`oap/reports/000-a-reconcile-bootstrap-repository-and-authority.md` with
`Report publication commit: SELF`; its final commit must have the implementation
head as sole parent and change only that report path. Push it, verify the remote PR
head, report bytes, sole parent and changed-path invariant with `verify_report.py`,
and send response `OK` only after that verification. The report must not claim its
future push or CI succeeded; record post-publication/final-head observations only
in the allowed private receipt for strategic review. Make no later mutation or push
for this round.

## Decision classification

D0. Isolating a disposable subprocess test from ambient runtime configuration,
adding a bounded least-privilege bootstrap CI check, and correcting stale status
language are reversible scaffold decisions within the accepted architecture. The
observed configuration conflict is an evidence/test-harness issue, not D1 judgment
debt. No D2 action is authorized; repository settings, live testing, public product
exposure, release, deployment, credentials, and protected infrastructure remain
blocked by their separate human gates.

## Deferred human adjudication
- Decision: NONE

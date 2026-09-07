# Work order 000-b — Exclude live reports from bootstrap fixtures

Status: FINAL

```oap-metadata
{
  "id": "000-b",
  "title": "Exclude live reports from bootstrap fixtures",
  "objective": "000",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "7ca26f1a6d9c110aa3c71a736d185028661d110d",
  "branch": "oap/000-reconcile-bootstrap-repository-and-authority",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 1,
  "dependencies": [],
  "local_work": "Clean objective branch at remote report head 7819dd0970019d966fd2756f5261efe3d9032c9b observed 2026-09-08T01:01:30+02:00; preserve both 000-a commits and its immutable report.",
  "prior_review": "000-a remote report verified, but result is PARTIAL and required final-head check OAP bootstrap acceptance failed at 7819dd0970019d966fd2756f5261efe3d9032c9b; PR #1 remains open and unmerged.",
  "provenance": [
    {
      "kind": "A",
      "reference": "Published work order 000-a acceptance criteria 2, 4 and 6; S-EVIDENCE-01, S-DIAGNOSE-01 and S-ORDER-03; TESTING.md TEST-01 and TEST-02"
    },
    {
      "kind": "E",
      "reference": "GitHub Actions run 34168409221 at report head 7819dd0970019d966fd2756f5261efe3d9032c9b: required check OAP bootstrap acceptance failed because copied synthetic fixtures retained the newly published oap/reports/000-a report, producing COMPLETED_REPLAY, AMBIGUOUS_ID and related inactive-state failures"
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

000-b is the first corrective round for numeric objective 000. Amend only existing
PR #1 and branch `oap/000-reconcile-bootstrap-repository-and-authority`. Preserve
000-a order/report history and both existing commits; do not amend, replace, or
create another PR.

## Provenance

- A: 000-a acceptance requires the complete bootstrap suite and the exact required
  check to pass at the final report head. Strategic evidence and diagnostic law
  require repair on the same objective/PR at the earliest failing boundary.
- E: GitHub Actions run 34168409221 passed the checkout and early tests, then failed
  13 tests after the 000-a report-only commit became part of the checked-out source.
  `Acceptance.setUp` copies the current repository into synthetic fixtures. Its
  new ignore function excludes live `oap/active` and `oap/orders/*.md`, but not
  `oap/reports/*.md`; the copied 000-a report turns intentionally inactive and
  synthetic 000-a scenarios into completed/ambiguous history. The same workflow
  passed at implementation head 5e7e6c6 before that report existed.

This supersedes any interpretation that the helper state machine or published
report is defective. Do not mutate either to treat the symptom.

## Current verified state

At 2026-09-08T01:01:30+02:00, remote `main` and accepted base remain
`7ca26f1a6d9c110aa3c71a736d185028661d110d`. PR #1 is open, non-draft, mergeable
but UNSTABLE, with head `7819dd0970019d966fd2756f5261efe3d9032c9b` on the ordered
branch. Local branch and remote head match with a clean worktree. The 000-a report
is remotely verified: its sole parent is implementation head
`5e7e6c6a87d605d745aed2920e20dcf72ac0effd`, and it changes only its report path.

The required check passed at implementation head 5e7e6c6 and failed at report head
7819dd0 in run 34168409221. State is REVIEW_READY for 000-a; no critical entries,
human dispositions, or relevant DHA gates exist. Accepted-runtime governance remains
valid and all protected source/governance identities still match the accepted base.
No merge, release, deployment, live repair test, or product implementation occurred.

## Governance

Use the accepted governance identity map in metadata and the normal compact coding
read set. Preserve PLAN, ARCHITECTURE, CRITICAL, full/dense role laws, compact
projections, prompts, source lock, distillation map, governance manifest, workspace
layout, historical bootstrap sources, the published 000-a order, and immutable
000-a report bytes. LR-014 requires the bootstrap CI repair to remain distinct from
product/live/linguistic/milestone/deployment evidence. Decision is D0; DHA is NONE.

## Goal and dependencies

Make bootstrap fixtures independent of all live mutable protocol history so the
complete acceptance suite passes after a report-only commit, and make the hosted
whitespace check examine the actual PR range. Close only the known final-head CI
failure on PR #1; objective 000 remains the same.

## Scope

1. Extend the shared synthetic-repository copy filter in
   `oap/tests/test_acceptance.py` to exclude published Markdown reports under
   `oap/reports`, in addition to the already excluded active pointer and orders.
2. Add or strengthen a focused regression that proves current live active, order,
   and report artifacts are absent from the copied synthetic repository while
   scaffold placeholders such as `.gitkeep` remain available as intended.
3. Change the workflow whitespace step to compare the literal accepted base through
   `HEAD`, rather than checking only a clean worktree.
4. Update only directly required generated/installation inventory hashes for changed
   generated files. Preserve historical bootstrap receipt/manifest snapshots.

## Non-goals

Do not edit any 000-a order or report; state-machine helpers; runtime conflict
validation; application code; product architecture/governance; source locks;
historical bootstrap sources; documentation unrelated to this correction; workflow
permissions, runner, action pin or test breadth; GitHub settings; branch protection;
Qwen/corpus/GPU/gateway/network resources; PR identity; or readiness claims. Do not
delete real protocol history from the working repository—exclude it only from
synthetic test-fixture copies.

## Files and boundaries

The expected mutable boundary is:

- `oap/tests/test_acceptance.py`;
- `.github/workflows/oap-bootstrap.yml`;
- `oap/GENERATED-FILES.json` and `oap/INSTALLATION.json` only for exact resulting
  hashes/byte counts of changed generated surfaces;
- the strategically published 000-b order/active pointer and coding's immutable
  `oap/reports/000-b-exclude-live-reports-from-bootstrap-fixtures.md`.

Inspect the 000-a CI log, previous diff and helper behavior as read-only evidence.
If repair requires any additional product/governance file, stop that mutation and
report the discrepancy rather than expanding scope.

## Requirements

1. The copy filter must treat `oap/orders/*.md` and `oap/reports/*.md` symmetrically
   as live protocol history, excluding both only at their exact directories. It
   must also exclude only the root `oap/active` pointer. Do not broadly ignore all
   Markdown, the whole `oap` tree, templates, source laws, or `.gitkeep` placeholders.
2. The regression must begin from a source fixture containing representative live
   active/order/report artifacts and prove the disposable copy is inactive, has no
   published order/report Markdown, and remains structurally usable by the normal
   materializer/state tests. It must fail on 000-a head 7819dd0 for the diagnosed
   reason and pass after this fix.
3. Preserve the environment-isolation and explicit subprocess-return assertion from
   000-a. Preserve independent negative proofs for malformed active, completed replay,
   ambiguous identifiers, configuration-authority conflict and SELF report rules;
   never make those helpers accept leaked state.
4. In `.github/workflows/oap-bootstrap.yml`, keep the job name exactly
   `OAP bootstrap acceptance`, `contents: read`, ubuntu-24.04, ten-minute timeout,
   full history, immutable checkout pin, Python 3.12/tmux presence checks, complete
   suite and accepted-runtime governance check. Change whitespace verification to
   `git diff --check 7ca26f1a6d9c110aa3c71a736d185028661d110d...HEAD` or an
   exactly equivalent accepted-base-to-head range.
5. Recalculate inventory values mechanically from final bytes. Do not edit unrelated
   inventory rows, bootstrap historical manifests, expected governance hashes, or
   accepted source identities to make tests pass.
6. Run the focused and full suites from the ordinary activated coding environment
   with the real 000-a/000-b protocol files present. The final 000-b report-only
   commit must itself trigger and pass the required hosted check.

## Acceptance criteria

1. A focused regression directly proves that synthetic repositories omit root
   `oap/active`, every live `oap/orders/*.md`, and every live `oap/reports/*.md`,
   while retaining the directories/placeholders and all non-history scaffold files.
2. The complete bootstrap suite passes with 60 or more executed tests and zero
   failures/errors in the coding role environment after both the 000-a and 000-b
   report files exist. The real tmux and live-shell tests execute rather than skip.
3. The required check `OAP bootstrap acceptance` completes successfully at the
   exact final 000-b report head. The earlier 7819dd0 failure remains visible and
   is not rerun, erased, or relabelled as success.
4. Accepted-runtime governance passes, protected-source diff is empty, and CRITICAL
   remains byte-identical to the accepted base. Only expected scoped files differ.
5. Workflow whitespace validation checks the committed PR range, not merely the
   clean checkout worktree.
6. PR #1 remains the sole objective PR, open and unmerged during coding. The 000-b
   SELF report has its literal implementation head as sole parent and changes only
   its matching report path; remote verification succeeds before response `OK`.
7. No product functionality, live Qwen/linguistic claim, credential/private data,
   protected-resource mutation, repository-setting change, merge, release, or
   deployment is introduced.

## Verification

Run and record at the literal implementation SHA:

```text
python3 -B -m unittest discover -s oap/tests -p 'test_acceptance.py' -v
python3 -B -m unittest discover -s oap/tests -p 'test_process_boundaries.py' -v
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 7ca26f1a6d9c110aa3c71a736d185028661d110d
python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair
git diff --check 7ca26f1a6d9c110aa3c71a736d185028661d110d...HEAD
git diff --exit-code 7ca26f1a6d9c110aa3c71a736d185028661d110d -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After report publication, verify the remote report bytes/parent/only-path invariant
for 000-b and inspect the exact required check at that remote head. Local and fake
evidence proves only scaffold behavior; the GitHub run proves hosted reproduction.
Neither proves repair application behavior, live Qwen, linguistic quality, ICA,
milestone acceptance, release, or deployment.

## Local setup and constraints

Use only the existing Python 3.12 standard-library suite, Git, tmux and owned
disposable fixtures. Do not install packages or services. Do not send either real
operational FIFO from inside a test. Keep native FIFO layout/modes unchanged. No
customer/model text, corpus, credential, auth file or private runtime value may
enter Git, logs, PR prose or reports.

Do not access or mutate Qwen weights/quantization, vLLM/CUDA, GPU allocation,
running services/ports, network/VPN/firewall, gateway, neighboring repositories,
GitHub settings, branch protection, release or deployment. Live repair testing
remains disabled.

## Documentation

No public product/status documentation change is expected. The immutable 000-b
order and report must document the diagnosed final-head-only fixture leak, exact CI
run/head, negative-path preservation and evidence limitations. Do not revise the
000-a report or hide its PARTIAL result and failed final-head check.

## Git and report publication

Remain on `oap/000-reconcile-bootstrap-repository-and-authority` and amend only
open PR #1. Preserve commits 5e7e6c6 and 7819dd0. Commit/push all non-report changes,
including the exact 000-b order and updated `oap/active`, before composing the new
report. Do not merge or enable auto-merge.

After all non-report changes are pushed, record the literal implementation head.
Write one new immutable report at
`oap/reports/000-b-exclude-live-reports-from-bootstrap-fixtures.md` with publication
commit SELF. Its final commit must have the implementation head as sole parent and
change only that report path. Push once, independently verify the remote PR head,
report bytes, parent and path, then send response `OK` and exit with no later mutation.
Do not claim future report-head CI success inside the report. If implementation and
all observable local requirements are complete, `Result: COMPLETE` may coexist with
the required final-head check recorded as PENDING for strategic post-publication
verification; use PARTIAL only for a genuine implementation/evidence gap other than
that structurally future observation.

## Decision classification

D0. The failure is an ordinary, reversible test-fixture boundary defect with a
minimal deterministic correction and no consequential unresolved design choice.
Preserving the helper's fail-closed replay/ambiguity behavior is mandatory. No D1
entry is admitted and no D2 action is authorized.

## Deferred human adjudication
- Decision: NONE

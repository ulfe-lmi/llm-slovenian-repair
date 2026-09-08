# Work order 002-a — CPU-only CI and governance guards

Status: FINAL

```oap-metadata
{
  "id": "002-a",
  "title": "CPU-only CI and governance guards",
  "objective": "002",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
  "branch": "oap/002-cpu-only-ci-and-governance-guards",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "000",
    "001"
  ],
  "local_work": "Merged main 2832fa1e51bdf3641aabbd81feab8ddb64a876da plus authorized recovery of worktree oap/active from stale committed 001-a to latest completed 001-c; preserve ignored disposable .venv review residue and all unrelated work.",
  "prior_review": "Objective 001 PR #2 merged after final-head review, but post-merge state exposed that 001-b/001-c same-size active-pointer writes were never staged; strategic review missed the stale 001-a blob. Reports/orders remain verified and recovery is recorded privately.",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §§14.1,16 and owner-authorized development loop; no product/live/release expansion"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§1,17,18,20; INITIAL-ROADMAP objective 002-a; TESTING.md TEST-01 through TEST-03; OAP protocol active/order/report/SELF requirements"
    },
    {
      "kind": "E",
      "reference": "Post-merge objective-001 observation: merged main 2832fa1 contains oap/active=001-a although published latest round/report is 001-c; check_state with remote failed REMOTE_HEAD_MISMATCH. All 001 implementation/report commits contain the stale blob because Git stat caching missed same-size atomic writes. Worktree-only recovery to 001-c restored REVIEW_READY."
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
    "LR-013",
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

002-a is the first round of DEMONSTRATOR objective 002. Create exactly branch
`oap/002-cpu-only-ci-and-governance-guards` and one new PR. If interrupted after
creation, recover those same objects and ID; never duplicate them.

## Provenance

- H: the product plan requires meaningful software/negative evidence without
  elevating it to repair, Qwen, linguistic, milestone or deployment proof.
- A: roadmap 002 requires CPU-only CI around shared governance/OAP commands, source
  and compact coverage, deliberate CRITICAL handling, DHA/provenance enforcement and
  append-only negatives. Existing TESTING/OAP contracts already name most fixtures.
- E: objective 001 added both CI checks and verified package isolation, but exposed a
  transcript gap after merge. `publish_order.py` atomically wrote `001-b` and `001-c`
  into the worktree, yet the sync filesystem preserved same-size stat metadata; Git
  did not notice/stage those writes. All 001 commits and merged main retained
  `001-a\n`. Strategic review displayed those bytes and incorrectly accepted them.
  The orders/reports remain intact and verified. A worktree-only correction to
  `001-c\n` restored remote `REVIEW_READY`; do not rewrite old commits or reports.

## Current verified state

Remote/default/local `main` is objective-001 merge
`2832fa1e51bdf3641aabbd81feab8ddb64a876da`; PR #2 is merged and no PR is open.
The objective-001 branch head/report is `de171121d6cccff075f085e9c254f08dcd22258d`,
with both required final-head checks green and all three 001 reports remotely
verified. No objective-002 branch or PR exists.

Merged `oap/active` is stale `001-a\n`; strategy changed only the local worktree
pointer to `001-c\n`, making state `REVIEW_READY` for the actual latest completed
round. This authorized recovery is the only tracked local difference before 002
publication. An ignored `.venv` from strategic diagnosis may remain and must not be
used, inspected or broadly deleted. Accepted governance passes at 2832fa1; CRITICAL
has no live entry/disposition/gate. Product remains an inert installable skeleton;
live repair testing is disabled.

## Governance

Use the accepted identity map in metadata and preserve every canonical product/
governance byte, CRITICAL history, compact/full role source, prompt, source lock,
bootstrap snapshot and prior immutable order/report. The stale committed pointer and
missed review are historical evidence; do not rewrite them.

Apply LR-013 to keep logs/check output free of raw/private text and secrets. Apply
LR-014 to distinguish OAP/package CI from application behavior, Qwen compatibility,
linguistic benefit, ICA and human gates. D0/NONE; the pointer bug and absent guard are
ordinary process defects, not judgment debt.

## Goal and dependencies

Establish final-head CPU-only governance CI that runs the shared checks and their
negative fixtures, and add a transcript guard that fails when the worktree/index/HEAD
active pointer is uncommitted or does not identify the latest published round.
Commit 002's exact active bytes despite sync-mount stat caching. Objectives 000 and
001 are merged prerequisites.

## Scope

1. Add a shared transcript-coherence function/CLI under `oap/bin` with thin entry
   point and focused standard-library tests.
2. Integrate the guard into `OAP bootstrap acceptance` without renaming that check or
   duplicating application dependency/build work.
3. Prove existing source drift, compact read-set/full-source preload, missing DHA,
   CRITICAL append/history and SELF extra-path/parent negatives remain exercised in
   the required final-head checks.
4. Update OAP/runbook/template documentation for explicit forced staging and
   index/committed active-byte verification, without changing governance identities.
5. Commit the recovered current transcript through normal 002 publication: the final
   committed pointer is `002-a\n`; preserve the missing 001-b/001-c snapshots as
   recorded history rather than manufacturing commits.

## Non-goals

Do not alter PLAN, ARCHITECTURE, CRITICAL, role constitutions, compact architecture,
coding communication, distillation map, source locks or historical bootstrap seeds.
Do not rewrite/squash prior objective history, amend old reports, reconstruct missing
active commits, or change the protocol's exact active-ID selection into an mtime/
directory-order rule. Do not add product modules, thresholds, corpora, model clients,
services, deployment/release workflows, secrets, GPU dependencies or live tests.

Do not change GitHub branch protection/settings, merge/auto-merge, package versions,
uv lock, or the verified native development driver unless a directly failing 002
test proves a minimal compatibility correction and it is reported.

## Files and boundaries

Expected mutable boundary:

- `oap/bin/oap_core.py`, `oap/bin/oap_cli.py` and a thin
  `oap/bin/check_transcript.py` entry point;
- a focused new `oap/tests/test_transcript_guard.py` and only direct existing OAP
  test support if necessary;
- `.github/workflows/oap-bootstrap.yml`;
- `docs/OAP-RUNBOOK.md`, `oap/README.md` and/or
  `oap/templates/WORK-ORDER-TEMPLATE.md` for exact operator/coding checks;
- exact generated/installation inventory rows for changed generated files;
- published 002-a order/active pointer and immutable matching report.

Tests use owned disposable Git repositories/fakes outside the guard boundary. The
real helper must inspect actual Git index/commit blobs and order/report metadata.

## Requirements

1. Implement one reusable `check_transcript` core and thin CLI with `--repo-root`,
   optional `--expected-id`, and explicit `--index` versus `--revision HEAD` modes.
   Default/failure behavior must be deterministic, read-only and redacted. Reuse
   existing ID/order/report/critical/governance parsing; do not create a second
   incompatible grammar.
2. Enumerate published order/report files by parsed ID and protocol suffix order
   `a…z, aa…az, ba…zz`, never lexicographic/mtime/directory order. Absence of active
   is valid only when no published order/report exists. Require every report to have
   its exact matching order and pass the existing local SELF/order/report validation.
   An order without report is allowed only for the current active round.
3. Require active ID to equal the highest sequential published order ID. Reject
   gaps, backward/stale active values, reports without orders, non-current unfinished
   orders, duplicate/ambiguous IDs and later objectives that bypass unresolved prior
   transcript. This consistency validation does not select which order coding may
   execute; coding still uses exact `oap/active` only.
4. In `--index` mode compare worktree active bytes with `git show :oap/active`; in
   committed mode compare worktree bytes with the requested commit blob and validate
   transcript paths at that revision. Fail if the same-size write exists only in the
   worktree, is missing from the index/commit, or differs from `--expected-id` plus
   LF. Do not rely on Git status/stat/mtime.
5. Add focused positive/negative tests using real disposable Git histories for:
   inactive empty transcript; active unfinished current order; current SELF report;
   a→b, z→aa and az→ba; worktree-only/index-only/stale committed active; latest-order
   mismatch; suffix/numeric gap; report without order; non-current unfinished order;
   extra-path/wrong-parent report; malformed/draft/missing-DHA order; source/compact
   drift and attempted full-source coding read-set expansion. Assert exact failure
   codes and no writes.
6. Extend the existing OAP workflow to run complete standard-library tests, accepted
   governance at literal base 2832fa1, and transcript guard in committed HEAD mode
   with expected `002-a` for this PR. Keep job name `OAP bootstrap acceptance`,
   least privilege, pinned checkout, Python/tmux checks and accepted-base whitespace.
   The expected ID must be derived safely for future orders or updated by an explicit
   order; do not leave a permanent 002-a hardcode that blocks later objectives.
7. Document the executor pre-implementation/report sequence: explicitly stage
   `oap/active` even if Git status is silent, run the guard in index mode with exact
   active ID, commit non-report work, and rerun committed mode before report. CI
   reruns committed mode at final report head. Never make publication implicitly
   stage/commit/signal.
8. For this round explicitly `git add -f oap/active` (or exact equivalent), prove
   `git show :oap/active` is hex `3030322d610a` before implementation commit, and
   prove both implementation and report HEAD contain those bytes. The coding report
   must include the prior 001 pointer omission and strategic-review miss.
9. Preserve CPU-only boundaries: no Qwen/corpus/customer data, model/GPU/service,
   network beyond ordinary GitHub/package CI already configured, or raw private text
   in logs. The guard reports IDs/codes/hashes only, not order/report bodies.
10. Update generated/installation hashes mechanically only for actual generated files
    changed. Keep required CI names exactly `OAP bootstrap acceptance` and
    `Application baseline`; both must pass at final report head.

## Acceptance criteria

1. Focused transcript tests pass all named positive and negative histories, including
   a same-size worktree/index/HEAD mismatch that would have rejected objective 001.
2. The actual 002 implementation index and both committed heads contain exact
   `002-a\n`; the guard passes in index mode before commit and committed mode after
   implementation/report commits. Git status output is not used as proof.
3. Final `OAP bootstrap acceptance` logs show the complete helper suite, accepted
   governance and committed transcript guard. Existing B05/B07/B14/B20/B22/B23
   negatives prove full-source preload, source drift, missing DHA, report-only extra
   path, exact append/history and invented-human rejection remain enforced.
4. `Application baseline` remains green and continues to prove only package/native
   offline behavior; no redundant dependency resolution is added to OAP CI.
5. Accepted governance/protected-source diff passes, CRITICAL is unchanged, every
   old order/report is byte-identical, and the incident is truthfully described.
6. PR #3 or the actual sole new objective PR is open/unmerged during coding; remote
   002-a SELF report verification succeeds and both final-head checks are green.
7. No product repair behavior, live model/data use, credential/private content,
   GitHub setting, merge, release, deployment or readiness claim is introduced.

## Verification

Run and report at the literal implementation SHA:

```text
python3 -B -m unittest discover -s oap/tests -p 'test_transcript_guard.py' -v
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 002-a
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 002-a
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da
python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
git diff --check 2832fa1e51bdf3641aabbd81feab8ddb64a876da...HEAD
git diff --exit-code 2832fa1e51bdf3641aabbd81feab8ddb64a876da -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

At the implementation and final report remote heads inspect both named required
checks and the committed active blob. After report publication verify remote SELF
bytes/parent/only-path. Fake/helper/package evidence remains distinct from product,
live Qwen, linguistic, ICA and human release/deployment evidence.

## Local setup and constraints

Use standard-library OAP fixtures and the existing native development verifier.
Owned temporary repositories/FIFOs/environments must be unique and cleaned. Do not
use, modify or delete the ignored repository `.venv` created by strategic diagnosis;
the native verifier excludes it. No new dependency or global install is needed.

No credentials, auth files, private strategic contents, customer/model text, prompts,
replacements or raw responses in Git/CI/report. Do not inspect private strategic
workorders; this order contains the bounded incident evidence coding needs. No Qwen,
corpus, GPU/model/server/gateway/service/VPN/firewall, GitHub-setting, release or
deployment mutation.

## Documentation

Update only OAP runbook/helper/template documentation necessary to make the exact
index/committed active guard durable. State that prior 001-b/001-c active snapshots
are absent from Git history and were not fabricated. Do not change public product
readiness or package-development claims except for a direct verified contradiction.

## Git and report publication

Start from exact merged main `2832fa1e51bdf3641aabbd81feab8ddb64a876da`, create
only `oap/002-cpu-only-ci-and-governance-guards`, and open one new PR. The recovered
worktree pointer will be replaced by the strategically published `002-a\n`; explicitly
force-stage it and prove index bytes before committing all non-report work. Never
merge or enable auto-merge.

After all non-report work/checks are pushed, record the literal implementation head.
Create only `oap/reports/002-a-cpu-only-ci-and-governance-guards.md` with SELF. Its
final commit has implementation as sole parent and changes only that report. Push,
verify remote head/report bytes/parent/path and both committed active blobs, send exact
`OK`, and stop without later mutation. Report-head CI remains future/PENDING in the
report and is observed by strategy.

## Decision classification

D0. The stale pointer is a reproducible same-size Git/stat/staging defect; the shared
guard, forced stage and CI integration are reversible bounded process engineering
inside the planned objective. Neither the bug nor strategic review miss creates a
five-condition consequential design dilemma. No D1 entry or D2 action is authorized.

## Deferred human adjudication
- Decision: NONE

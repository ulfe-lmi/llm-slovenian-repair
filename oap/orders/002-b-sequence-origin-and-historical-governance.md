# Work order 002-b — Sequence origin and historical governance

Status: FINAL

```oap-metadata
{
  "id": "002-b",
  "title": "Sequence origin and historical governance",
  "objective": "002",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
  "branch": "oap/002-cpu-only-ci-and-governance-guards",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 3,
  "dependencies": [
    "000",
    "001"
  ],
  "local_work": "Clean objective branch at remote report head 3d096a798664884b3f89ab7425cdcbe2c290f22e; preserve all 002-a and prior transcript commits/reports plus ignored disposable review residue.",
  "prior_review": "002-a remote report and both final-head checks verified, but semantic review proved the transcript guard accepts a sequence beginning at 000-z/000-aa or objective 001 and overrides historical order governance with the current revision manifest.",
  "provenance": [
    {
      "kind": "A",
      "reference": "OAP ID grammar/transition law, immutable historical order governance rule, S-ORDER-03 and published 002-a requirements 2,3,5"
    },
    {
      "kind": "E",
      "reference": "2026-09-08 direct final-head probe: _transcript_order(['000-z','000-aa']) returned valid and _transcript_order(['001-a']) returned valid; oap_core validate_order(source_ref=resolved) rebinds every historical order to current revision governance instead of its metadata base"
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

002-b is the first corrective round on existing objective-002 branch and PR #3.
Preserve implementation/report commits af24ae1/3d096a7 and every earlier immutable
order/report. Do not amend history, create another PR, or advance objective number.

## Provenance

- A: transcript history begins at 000-a; every numeric objective is sequential; each
  objective begins at suffix a and corrections follow the complete explicit suffix
  order. Historical orders retain the governance identity accepted at their original
  base. Current candidate hashes cannot rewrite that history.
- E: 002-a checks only suffix ranks from the first observed suffix and objective
  integers from the first observed objective. Direct probes therefore accept missing
  initial history. Its new `source_ref` override makes historical order validation
  compare against the current revision's manifest, which will reject legitimate old
  orders after a controlled governance evolution or tempt history rewriting.

## Current verified state

Remote/default accepted main remains
`2832fa1e51bdf3641aabbd81feab8ddb64a876da`. PR #3 is open and clean at 002-a
report head `3d096a798664884b3f89ab7425cdcbe2c290f22e`; implementation head is
`af24ae13c9305896d10c4632a138e5da56614bbc`. The remote 002-a SELF report verifies,
both final-head checks passed, committed active is exact `002-a\n`, and state is
REVIEW_READY. CRITICAL is empty; accepted governance is unchanged.

The real current transcript 000-a/b, 001-a/b/c and 002-a is sequential, so the
reported checks are genuine for current data. The defect is missing negative/future
evolution coverage, not current transcript corruption. No product/live/release/
deployment action occurred.

## Governance

Preserve all accepted source/governance/CRITICAL bytes and prior transcript history.
An immutable order validates against its own `governance_ref` when present or its
own `base_sha`, exactly as the original `validate_order` contract states. The selected
revision supplies transcript file bytes, not replacement historical authority.

LR-013/LR-014 remain evidence/privacy boundaries. D0 and Decision NONE; this is an
ordinary validation bug with deterministic correction.

## Goal and dependencies

Require transcript numbering to originate at objective 000 and suffix a, prove full
z→aa and az→ba ordering without accepting omitted prefixes, and preserve historical
per-order governance validation across later accepted governance revisions.

## Scope

1. Correct sequence-origin validation in the shared transcript guard.
2. Remove the current-revision governance override from historical order validation.
3. Replace misleading transition fixtures and add focused missing-origin and
   historical-governance tests.
4. Update direct docs only if behavior wording is inaccurate; preserve workflow/check
   names and integration unless a test requires a minimal command correction.
5. Publish exact 002-b order/active/report on existing PR #3.

## Non-goals

Do not redesign ID grammar, change active selection, modify publication/report/merge
semantics, add product code/dependencies, alter current governance identities, rewrite
old orders/reports, reconstruct missing 001 active commits, change workflows beyond
direct necessity, or touch private strategic state. No live Qwen/data, model/GPU/
service/gateway/network setting, GitHub setting, merge, release or deployment.

## Files and boundaries

Expected mutable paths are `oap/bin/oap_core.py`, focused
`oap/tests/test_transcript_guard.py`, exact inventory rows if those generated files
change, and 002-b order/active/report. `oap/bin/oap_cli.py`, thin entry point, workflow
and docs should remain unchanged unless direct verification demonstrates necessity.

Tests use disposable Git histories. A pure sequence-order unit test may exercise the
full suffix prefix without creating dozens of report commits; report/governance tests
must still use real Git blobs and the actual validator boundary.

## Requirements

1. Require the first objective integer to be 0 and objective list to equal
   `range(0, last + 1)`. A transcript containing only `001-a` or later must fail
   `TRANSCRIPT_OBJECTIVE_GAP` (or a more precise stable code), while empty inactive
   bootstrap remains valid.
2. Require every observed numeric objective's suffix ranks to start at `a` and equal
   the full zero-based prefix through its last suffix. `000-z,000-aa` without a…y
   must fail; `000-a,000-c` must fail. Full a…z→aa and a…az→ba prefixes must pass
   using `SUFFIX_ORDER`, never lexicographic order.
3. Replace the current z/aa and az/ba tests with full-prefix sequence tests or direct
   sequence-helper tests. Add explicit missing-initial-a and missing-objective-000
   negatives. Keep real report/active transition coverage for ordinary a→b.
4. Restore `validate_order` to its historical contract: governance identities come
   from `m.get('governance_ref', m['base_sha'])`. Do not add/retain a caller-selected
   `source_ref` that can rebind an immutable order. The transcript guard reads order
   bytes from index/revision but validates authority at the order's recorded base.
5. Add a real Git regression: commit a valid 000-a order/report at its base; create a
   later revision with a deliberately different current manifest identity map; prove
   transcript validation still validates 000-a against its original base rather than
   current manifest. The governance helper may separately reject an invalid current
   candidate; do not weaken it.
6. Keep index/committed pointer checks, latest-active, report/order/SELF, unfinished,
   malformed/DHA and CI integrations unchanged. Explicitly force-stage `002-b\n` and
   prove index/implementation/report blobs independently of Git status.
7. Run fresh implementation-head and report-head checks once per new SHA. Preserve
   002-a test/report claims as current-scope evidence but do not claim their missing
   negatives passed.

## Acceptance criteria

1. Direct probes reject `['000-z','000-aa']`, `['001-a']`, and `['000-a','000-c']`;
   complete prefixes through aa and ba pass in protocol order.
2. Historical-governance regression passes and `validate_order` has no active
   current-revision override; existing candidate/accepted governance negatives remain
   green.
3. Full transcript-focused and OAP suites pass, actual index/HEAD guard selects exact
   `002-b`, and all prior active/report/SELF negatives remain enforced.
4. Both required checks pass at exact final report head; accepted governance and
   protected-source diff pass; CRITICAL and all older transcript bytes are unchanged.
5. PR #3 remains sole open objective PR/unmerged during coding; remote 002-b SELF
   verification succeeds. No product/live/private/setting/release/deployment change.

## Verification

Run and report at the literal implementation SHA:

```text
python3 -B -m unittest discover -s oap/tests -p 'test_transcript_guard.py' -v
python3 -B -m unittest discover -s oap/tests -v
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 002-b
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 002-b
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
git diff --check 2832fa1e51bdf3641aabbd81feab8ddb64a876da...HEAD
git diff --exit-code 2832fa1e51bdf3641aabbd81feab8ddb64a876da -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After report publication independently verify SELF, exact committed active bytes and
both required checks. The guard remains orchestration evidence only, not application,
Qwen, linguistic, ICA or release/deployment evidence.

## Local setup and constraints

Use existing standard-library fixtures and native development driver only. No new
dependency/install/network beyond existing GitHub/package CI. Owned temporary repos
must be finite and cleaned. Do not touch ignored `.venv` or private strategic files.

No credentials, auth/proxy values, customer/model text, prompts, replacements or raw
responses in code/log/report. No Qwen/corpus/GPU/service/gateway/network setting,
package publication, merge, release or deployment.

## Documentation

No documentation change is expected unless exact current wording claims partial
suffix/objective histories are valid or historical orders use current governance.
Any change must preserve the 001 active-pointer incident and evidence separation.

## Git and report publication

Stay on `oap/002-cpu-only-ci-and-governance-guards` and amend only PR #3. Preserve
af24ae1/3d096a7. Commit/push all non-report changes plus exact order and force-staged
active before report. Do not merge/auto-merge.

Record literal implementation head and create only
`oap/reports/002-b-sequence-origin-and-historical-governance.md`. SELF commit has
implementation as sole parent and changes only that report. Push, verify remote
head/bytes/parent/path and active blobs, send exact `OK`, stop without later mutation.
Report-head checks remain future/PENDING inside report.

## Decision classification

D0. Sequence-origin and historical-base validation are deterministic protocol bugs,
not consequential unresolved alternatives. The correction is bounded/reversible and
adds no D1 or D2 action.

## Deferred human adjudication
- Decision: NONE

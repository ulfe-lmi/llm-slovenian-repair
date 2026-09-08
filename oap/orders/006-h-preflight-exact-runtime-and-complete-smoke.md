# Work order 006-h — Preflight exact runtime and complete smoke

Status: FINAL

```oap-metadata
{
  "id": "006-h",
  "title": "Preflight exact runtime and complete smoke",
  "objective": "006",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/006-unigram-lexicon-importer",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "dependencies": ["003", "004", "005"],
  "local_work": "Clean branch at remote 006-g blocked report head 13706ca116ad1cfe08d237f29b0b48dda50f677b; report/transcript/final CI/fsck verified; active tree mode 100644; no 006-g source temp or owned environment remains.",
  "prior_review": "006-g one verifier-first GET passed then direct system-python CLI stopped before member access because checkout src was absent; post-attempt path fix is committed, but an independent isolated clean-shell probe then proved system python lacks Pydantic. Zero importer attempts; cumulative GETs nine.",
  "provenance": [
    {"kind": "E", "reference": "006-g receipt/report: canonical verifier PASSED, HEADER_CONTRACT_UNAVAILABLE before member access, attempts zero/null results, cleanup true, one GET/cumulative nine; final helper source-path bootstrap exists only after that attempt."},
    {"kind": "E", "reference": "Independent `env -u PYTHONPATH python3.12 -B -I` run-path probe from /tmp resolves current source bootstrap but returns provenance-construction-failed caused by missing Pydantic in that exact system interpreter."},
    {"kind": "A", "reference": "S-DIAGNOSE-01 and S-EVIDENCE-01 require correction at the earliest reproducible setup/invocation boundary and proof through the actual named entry point before product acceptance."}
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
  "lr": ["LR-008"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

006-h is the exact-runtime correction and final bounded compatibility attempt on
existing PR #7. Preserve every 006-a–g order/report/receipt and request count.

## Provenance

- E: 006-g failed at two separable invocation prerequisites, not source or importer.
- I: A positive no-PYTHONPATH preflight under the exact retained interpreter closes both
  missing-source-path and missing-dependency hypotheses before source access.
- A: Only a successful real member/import run can complete objective 006 evidence.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`; PR #7 open at valid
006-g BLOCKED SELF `13706ca116ad1cfe08d237f29b0b48dda50f677b`, implementation
`b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64`; final CI/transcript/fsck pass.
Optional-tab importer and committed smoke helper are offline-green only. One 006-g GET
was consumed, cumulative nine; no external bytes/temp/environment remain. CRITICAL empty.

GitHub branch protection and repository rulesets remain absent when last checked, so
the development gate is procedural. Recheck but do not change settings. No live repair,
milestone, release or deployment gate is authorized.

## Governance

Compact law, LR-008, security/testing/source inventory. D0/NONE. No broad catch, raw
source output or unsupported interpreter assumption.

## Goal and dependencies

Make successful CLI runtime readiness executable and permanent, then use that exact
preflighted dependency interpreter for one verifier-first 32-row real-prefix smoke.

## Scope

1. Add exact positive CLI preflight plus clean-process tests; narrow error handling.
2. Correct current 006-g status prose and add one 006-h receipt.
3. Create/retain one lock-derived owned environment through one real attempt.
4. Complete sequential verification and report on PR #7.

## Non-goals

No parser/aggregate/source-verifier semantics, automatic downloader, full archive import,
index/database/lookup/detector, n-grams/other sources, committed source bytes, root export
or dependency change, history rewrite, GitHub setting, merge, live Qwen, release,
deployment, ICA or milestone claim.

## Files and boundaries

Smoke helper/its focused tests, current direct docs/status, new 006-h receipt, active/
order, generated inventories and report. Do not change importer, diagnostic classifier,
source verifier or lock unless an offline test proves an exact defect; otherwise stop.

## Requirements

1. Add a finite positive CLI preflight mode requiring the canonical inventory and source
   ID but no artifact. It must load/validate the canonical inventory entry, import and
   validate the exact 834-byte header contract, construct real COMPLETE/COMPLETE/PARTIAL
   provenance, import the actual `import_unigrams` entry point and limits, and emit only
   a bounded `READY` summary of identities/counts/completeness—no source content.
2. Make preflight and smoke argument forms mutually exclusive/fail closed. Remove the
   broad `except Exception`; enumerate/map only expected bounded failures at the layer
   that owns them. Unexpected programming errors must not be relabelled as evidence.
3. Add a subprocess regression that invokes the actual script by absolute path from an
   owned non-repository cwd with `PYTHONPATH` absent and Python isolated mode. It must
   positively complete preflight using the test environment's interpreter, proving both
   repository source bootstrap and installed dependency closure. Negative argument and
   unavailable-dependency paths remain finite and content-free.
4. Retain all 006-g helper/member/aggregate/import tests. Add a second direct process
   check under the exact interpreter later retained for acquisition. Do not claim a
   wrong-source early exit proves runtime readiness. Correct `STATUS.md` and direct docs
   to record 006-g's actual blocked attempt and the independent system-Python dependency
   finding without rewriting its report/receipt.
5. Run objective-005/006 focused suites, full contract/full pytest, Ruff, mypy, OAP and
   native baseline sequentially before source access. Run explicit pytest commands in an
   owned dependency-complete environment, not the host interpreter and never repository
   `.venv`; record any exploratory failures separately from final authoritative results.
6. After offline green, create an exact owned `/tmp/...006-h-env...` from the committed
   lock using supported tooling. Install/sync only project development dependencies and
   retain this literal environment through the source action. From an owned `/tmp` cwd,
   with `PYTHONPATH` removed and isolated Python, run the committed preflight by absolute
   path using exactly that environment's interpreter. Any failure stops before GET.
7. Only after that exact preflight passes, create one literal owned
   `/tmp/...006-h-source...` path. Do not search broad paths. Perform exactly one 006-h
   GET with `curl --disable`, direct HTTPS/no redirect/no credentials/options, fail,
   connect <=10s, total <=900s, max-filesize 115865656 and one `.part` target. No retry.
8. From the same owned cwd/environment and still without PYTHONPATH, invoke the committed
   helper by absolute path on that exact part. Require canonical verifier success before
   one selected-member access, 14 preamble/exact header/32 rows within 4 MiB, exact 006-e
   aggregate, and two successful public importer runs with immutable equality, 32 records,
   equal nonnull input/output hashes and COMPLETE/COMPLETE/PARTIAL bindings.
9. On any failure, preserve only finite aggregate/null facts and make no second GET.
   Guaranteed cleanup must delete and verify absence of the exact source path and exact
   owned environment, without broad `find`, glob deletion or overlapping test/OAP/Git/
   acquisition/cleanup commands. Never log header/row values, records or per-row hashes.
10. Add `resources/source-acquisitions/gigafida-2.0-words-006-h.json` recording exact UTC,
    canonical identities, preflight interpreter/environment/PYTHONPATH facts without a
    private path, one 006-h GET/cumulative ten, preserved 006-f/g failures, aggregate,
    attempts/runs/count/equality/hashes/completeness, cleanup/non-retention and
    redistribution false. Null anything not observed; no future commit guess.
11. Receipt/preflight tests validate schema, counters, completeness, hashes, no-content
    fields and history. Preserve lock/dependencies, root source/wheel laziness, all 003–
    006-g contracts/evidence, active 100644, source inventory and protected governance.
12. After receipt/docs, rerun focused/full checks, native baseline, transcript, governance,
    protected diff and fsck sequentially; final-head required CI must be green. Report
    criteria is a string; distinguish each commit and every failed/pass attempt, sole
    SELF report, no future-CI, retry, merge, live, release, deployment or milestone claim.

## Acceptance criteria

1. Positive CLI preflight succeeds from non-repo cwd with no PYTHONPATH under both test
   and exact retained acquisition interpreters; no broad exception catch remains.
2. Exactly one 006-h fetch (cumulative ten) reaches the committed helper and yields the
   exact aggregate plus two equal 32-record importer results with nonnull equal hashes.
3. Receipt/docs truthfully preserve prior failures and prove exact source/environment
   cleanup, no content/retention and PARTIAL import scope; all earlier invariants pass.
4. All final local/report-head checks and fsck pass; PR #7 remains unmerged during coding.

## Verification

```text
pytest tests/contract/test_objective_005.py -q
pytest tests/contract/test_objective_006.py -q
pytest tests/contract/test_objective_006_diagnostics.py -q
pytest tests/contract/test_objective_006_smoke.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-h
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-h
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git ls-files --stage oap/active
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Also run the exact isolated preflight, one acquisition, same-interpreter helper and exact
cleanup sequence required above.

## Local setup and constraints

One 006-h request after exact runtime preflight. Literal owned paths only, no broad
search/delete or concurrency, no repo `.venv`, explicit Git maintenance disabled. No
source content, credentials, protected host/settings, live model or neighboring repo.

## Documentation

Correct current status and document preflight, exact interpreter, bounded real-smoke
outcome and limitations. Historical 006-f/g evidence stays immutable.

## Git and report publication

Same PR #7. New commits only, no amend/force. Push all non-report work/check CI; sole
`oap/reports/006-h-preflight-exact-runtime-and-complete-smoke.md` SELF report with literal
implementation head parent, remote verify, exact OK, exit. No merge.

## Decision classification

D0. Reversible dependency/runtime preflight and one bounded public-source compatibility
probe; no human intent, rights, live-service, release or deployment decision.

## Deferred human adjudication
- Decision: NONE

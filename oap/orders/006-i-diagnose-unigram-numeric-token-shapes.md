# Work order 006-i — Diagnose unigram numeric token shapes

Status: FINAL

```oap-metadata
{
  "id": "006-i",
  "title": "Diagnose unigram numeric token shapes",
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
  "local_work": "Clean branch at remotely verified recovered 006-h report 6d11312b6ab169e0000269dc4abd23c2f0a1385b; final report-head CI/transcript/fsck green; two invalid unpublished report commits preserved under local recovery refs; no source/temp/environment remains.",
  "prior_review": "006-h exact preflight/verifier/member/prefix/structural aggregate passed; first public importer attempt returned import-invalid-count, second did not run and hashes are null. One GET/cumulative ten; exact cleanup. Cause is not yet known.",
  "provenance": [
    {"kind": "E", "reference": "006-h receipt and recovered report: 32-row structure PASSED with known 31/1 terminators, helper_reached_importer true, attempts one/runs zero, failure import-invalid-count, one 006-h GET/cumulative ten and cleanup."},
    {"kind": "I", "reference": "Independent semantic review rejects guessing locale/grouping/whitespace/count semantics from a finite label; a fixed aggregate numeric-token classifier can distinguish the plausible formats without disclosing values."},
    {"kind": "A", "reference": "S-DIAGNOSE-01 and S-EVIDENCE-01 require the smallest experiment separating hypotheses at the earliest reproducible product boundary before mutation."}
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

006-i is a diagnostic-only corrective round on existing PR #7. Preserve 006-a–h
history, receipts, recovery refs/incidents and cumulative request count.

## Provenance

- E: Source routing/structure is now proven; numeric parsing is the first failure.
- I: `invalid-count` alone cannot distinguish grouping, locale, whitespace or other
  syntax and cannot authorize normalization.
- A: Diagnose fixed categories first; product semantics remain unchanged this round.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`; PR #7 open at valid
006-h BLOCKED report `6d11312b6ab169e0000269dc4abd23c2f0a1385b`, implementation
`10ac426441a3f778ffbd7d713640af42f88e54db`; report-head CI/transcript/fsck pass.
006-h reached one real importer attempt after full structural success and stopped at
`import-invalid-count`. Cumulative GETs ten. No source/temp/environment remains.

GitHub branch protection/rulesets are absent when last checked; recheck but do not change
settings. Development enforcement is procedural. CRITICAL empty; no live repair,
milestone, release or deployment gate is authorized.

## Governance

Compact law, LR-008, security/testing/source inventory. Diagnostic D0/NONE. Fixed
categories and aggregate counts only; no raw tokens, digits, field values or row hashes.

## Goal and dependencies

Determine the bounded first-32-row numeric token syntax and exact current-parser failure
location without changing importer acceptance, so strategy can order one evidence-based
parser correction rather than another guess.

## Scope

1. Add a fixed content-free numeric token classifier/mode and synthetic tests.
2. Run one preflighted verifier-first 006-i diagnostic; publish one receipt.
3. Update only current diagnostic docs/status and complete PR/report evidence.

## Non-goals

No importer/normalization/count/decimal semantics, record/result model, source verifier,
full archive import, index/lookup/detector, n-grams, automatic downloader, retained data,
dependency/root export, history/recovery-ref rewrite, GitHub setting, merge, live Qwen,
release, deployment, ICA or milestone action.

## Files and boundaries

Prefer the existing smoke/diagnostic helper plus a focused diagnostic test module; new
006-i receipt, current direct docs/status, active/order, generated inventories and report.
`src/llm_slovenian_repair/**`, source verifier/inventory and lock are inspect-only.

## Requirements

1. Add a mutually exclusive numeric-diagnostic CLI path that reuses successful 006-h
   preflight, canonical verification, one selected-member open, exact bounded envelope
   and structural aggregate. It must stop before product mutation and call the current
   importer exactly once to confirm the finite reason/location; no second run.
2. Parse the already structurally valid 28 semantic fields only in transient memory.
   For the eight known absolute-count columns and sixteen published-decimal columns,
   emit per-1-based-column histograms drawn only from a closed enum such as EMPTY,
   ASCII_DIGITS, ASCII_DECIMAL_DOT, ASCII_DECIMAL_COMMA,
   ASCII_GROUPED_DOT_TRIPLETS, ASCII_GROUPED_COMMA_TRIPLETS,
   ASCII_GROUPED_SPACE_TRIPLETS, UNICODE_SPACE_GROUPED_TRIPLETS,
   ASCII_SCIENTIFIC_DOT, ASCII_SCIENTIFIC_COMMA, SIGN_PREFIX, PERCENT_SUFFIX,
   LEADING_OR_TRAILING_WHITESPACE, OTHER_ASCII and OTHER_UNICODE. Define deterministic
   mutually exclusive priority and context-specific absolute/decimal interpretation.
3. Emit aggregate row count, count/decimal compatibility totals under the **current**
   parser only, and first incompatible sample row ordinal, 1-based column, semantic kind
   and fixed category. If the importer is called, expose only its allowlisted reason and
   numeric column parsed from an exact safe `reason:column` form; otherwise null. Never
   emit token text, digits, prefixes/suffixes, code points, byte substrings, token length,
   per-row hashes, record objects or an open-ended source-derived label.
4. Treat all classifications as syntax evidence only. Do not infer numeric value,
   thousands/decimal meaning, denominator/completeness, locale or permitted conversion.
   Ensure every of 32 rows and every 24 numeric cells contributes exactly once to its
   column histogram and global totals; structural mismatch fails before profiling.
5. Synthetic tests exercise every enum category and overlap priority with project-authored
   values, all 24 numeric columns, exact conservation totals, first-location semantics,
   deterministic output and absence of exact synthetic token strings/sentinel fragments
   in serialized results/errors. Tests prove default preflight/full-smoke behavior is unchanged and the
   diagnostic CLI is mutually exclusive/content-free.
6. Add a positive isolated subprocess test from a non-repository cwd with PYTHONPATH
   absent using an owned dependency-complete interpreter. Use a synthetic-test seam only
   outside canonical verification/member/import boundaries. No broad exception catch.
7. Run focused objective-005/006 suites, full contract/full pytest, Ruff/mypy, OAP and
   native baseline sequentially before source. Every uv command must set a validated
   owned `UV_PROJECT_ENVIRONMENT` and `UV_CACHE_DIR` in the same process before running;
   never invoke uv against repository `.venv`, never repair it, and do not overlap work.
8. Create and retain one exact lock-derived `/tmp/...006-i-env...`; from an owned non-repo
   cwd with PYTHONPATH absent and isolated mode, pass preflight under that exact interpreter.
   Then create one literal `/tmp/...006-i-source...` and perform exactly one 006-i GET
   with the established bounded curl recipe. No broad search, retry or second GET.
9. Use that same interpreter and exact path to invoke the committed numeric diagnostic.
   Require verifier and structural success plus a complete 32-row profile and the safe
   current importer failure observation. On mismatch stop with null unobserved fields.
   Guaranteed exact cleanup removes/verifies the literal source/env/cwd/run paths only.
10. Add `resources/source-acquisitions/gigafida-2.0-words-006-i.json` with exact UTC,
    canonical/preflight facts, one 006-i GET/cumulative eleven, preserved 006-f/g/h
    failures, structural aggregate, numeric histograms/conservation/first location,
    importer attempt/reason/column, no content/retention/temp and redistribution false.
11. Receipt tests validate fixed keys/enums, exact 32x24 conservation, safe location,
    counters/history/nulls and recursive forbidden content keys. Docs label it bounded
    syntax diagnosis, not a chosen conversion or compatibility/full-import result.
12. Preserve active 100644, lock/dependencies, objective-001 source/wheel root laziness,
    all 003–006-h behavior/evidence and protected governance. After receipt/docs rerun
    complete checks/transcript/governance/diff/fsck sequentially; final-head CI green.
    Report criteria is a string, sole SELF, all SHAs/failures explicit, no merge/live/
    release/deployment/milestone claim and no angle-bracket placeholder commands.

## Acceptance criteria

1. Fixed categorical profiling covers exactly 32x24 numeric cells, is deterministic and
   serialized output contains no token/value/length/per-row material.
2. One 006-i fetch (cumulative eleven) reproduces structural success and records complete
   per-column numeric shape plus safe first current-parser incompatibility/reason/column.
3. No importer semantics change; receipt/docs preserve all prior failures and exact
   cleanup/non-retention with no broader interpretation.
4. All local/report-head checks and fsck pass; PR #7 remains unmerged during coding.

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
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-i
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-i
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git ls-files --stage oap/active
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Also run the exact preflight, one acquisition, numeric diagnostic and exact cleanup.

## Local setup and constraints

One 006-i request only after offline/preflight green. Owned literal paths, no broad search,
repo `.venv`, concurrency, raw values or source retention. Explicit Git maintenance off.

## Documentation

Record categorical syntax evidence and its limits; do not select parser semantics or
rewrite historical 006 evidence/recovery facts.

## Git and report publication

Same PR #7. New commits only; no amend/force. Push non-report work/check CI; sole
`oap/reports/006-i-diagnose-unigram-numeric-token-shapes.md` SELF report with literal
implementation parent, remote verify, exact OK, exit. No merge.

## Decision classification

D0. Bounded content-free diagnosis at a reached parser boundary; no provisional product,
rights, live-service, release or deployment judgment.

## Deferred human adjudication
- Decision: NONE

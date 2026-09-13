# Work order 006-j — Refine marker row and numeric units

Status: FINAL

```oap-metadata
{
  "id": "006-j",
  "title": "Refine marker row and numeric units",
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
  "local_work": "Clean branch at verified 006-i report head 94f09a22dc202c29f61a87bfcc8cc68e7a076dcf; report/transcript/final CI/fsck green; no source/temp/environment remains; local unpublished 006-h recovery refs preserved.",
  "prior_review": "006-i diagnostic COMPLETE: 32x24 numeric cells conserved; row 1 is OTHER_ASCII in every numeric column, rows 2–32 have digit counts plus percent-suffixed shares and mostly decimal-comma relative values; importer invalid-count at row 1 column 5. Row role and marker identity remain unresolved.",
  "provenance": [
    {"kind": "E", "reference": "006-i receipt/report: verifier/structure/profile passed, count compatibility 248/256, decimal 4/512, first incompatibility row 1 column 5 OTHER_ASCII, current importer invalid-count:5, one GET/cumulative eleven and cleanup."},
    {"kind": "I", "reference": "Independent review finds all 24 row-1 numeric cells share the coarse OTHER_ASCII class; this cannot yet distinguish metadata/unit row from lexical missing values or authorize skipping/normalization."},
    {"kind": "C", "reference": "006-i immutable report misstates starting_remote_sha as f14686c; verified actual round-start remote was 6d11312, while f14686c was the final implementation head. Record correction without rewriting history."},
    {"kind": "A", "reference": "S-DIAGNOSE-01 and S-EVIDENCE-01 require a smallest content-free discriminating experiment before changing parser semantics."}
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

006-j is the second diagnostic-only numeric-format round on PR #7. Preserve every
006-a–i source request, receipt/report and recovery fact.

## Provenance

- E: All ordinary sampled rows share stable numeric classes; row 1 alone is a complete
  numeric outlier and blocks the importer first.
- I: A fixed marker/equality/identity profile can distinguish row-role hypotheses without
  exposing values; omitting row 1 in a diagnostic-only envelope can expose the next
  current-parser boundary without treating omission as accepted behavior.
- C: Correct the 006-i starting-remote evidence only in new history.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`; PR #7 open at valid
006-i COMPLETE report `94f09a22dc202c29f61a87bfcc8cc68e7a076dcf`, implementation
`f14686c8b30962a948ca4dd5acba7ebbe0a9d86a`; final checks and fsck pass.
Numeric syntax profile complete, importer unchanged and incompatible. Cumulative GETs
eleven; no external bytes/temp/environment remain. CRITICAL empty.

GitHub branch protection returns 404 and rulesets are empty as rechecked by 006-i. Do not
change settings. Development enforcement is procedural. No live, milestone, release or
deployment gate is authorized.

## Governance

Compact law, LR-008, security/testing/source inventory. Diagnostic D0/NONE. Only fixed
derived categories, equality/relationship counts and safe failure locations may leave
transient memory.

## Goal and dependencies

Refine the first sampled row's `OTHER_ASCII` markers and lexical-identity relationships,
and expose the next current-parser boundary when only that row is omitted diagnostically,
without choosing or implementing skip/missing/locale/unit semantics.

## Scope

1. Add fixed row-marker/identity refinement to the existing diagnostic path and tests.
2. Add one counterfactual omit-first-row current-importer call, one 006-j fetch/receipt.
3. Record the 006-i report identity correction and current diagnostic docs/status.

## Non-goals

No importer/source verifier/normalization/count/decimal/skip behavior, result model,
full import, index/lookup/detector, other source, automatic downloader, retained data,
dependency/root export, history/recovery-ref rewrite, GitHub setting, merge, live Qwen,
release, deployment, ICA or milestone action.

## Files and boundaries

Existing diagnostic/smoke helpers and their focused tests, new 006-j receipt, direct
current docs/status, active/order, generated inventories and report. `src/**`, verifier,
source inventory, lock, protected governance and all prior evidence are inspect-only.

## Requirements

1. Extend only the diagnostic mode after exact structural success. For each row-1
   `OTHER_ASCII` numeric cell, refine via a closed enum with deterministic priority:
   HYPHEN_MINUS, REPEATED_HYPHEN_MINUS, DOT, REPEATED_DOT, SLASH, PERCENT_ONLY,
   ASCII_LETTERS_ONLY, ASCII_ALNUM, ASCII_PUNCTUATION_OTHER and ASCII_MIXED_OTHER.
   Do not emit the token or any token hash/length.
2. Also emit fixed booleans/counts: exact distinct numeric marker count across row 1;
   whether all 24 are identical; per absolute/share/relative semantic family distinct
   counts and within-family uniformity; whether any identical marker recurs in the same
   column in rows 2–32. Equality comparisons occur transiently with no representative.
3. Profile row 1 identity columns 1–4 using only EMPTY, ASCII_LETTERS, UNICODE_LETTERS,
   ASCII_PUNCTUATION, ALNUM and MIXED. Emit nonempty mask, form/lemma/lowercase-lemma
   equality pattern from a fixed enum, NFC-casefold relation booleans, POS-shape category,
   and how many rows 2–32 share that exact derived identity profile. No text/length/hash.
4. State only evidence predicates such as NUMERIC_MARKERS_UNIFORM,
   NUMERIC_MARKERS_COLUMN_SPECIFIC, LEXICAL_RELATIONS_MATCH_ORDINARY_SAMPLE or
   IDENTITY_PROFILE_OUTLIER. Do not label the row metadata/units/lexical or authorize a
   skip unless that is already explicit source authority; this round must not decide it.
5. Create a second in-memory diagnostic-only envelope with original 14 preamble/header
   and rows 2–32, changing no retained bytes. Call the unchanged public importer exactly
   once on it with max_rows 31 and real COMPLETE/COMPLETE/PARTIAL provenance. Record only
   attempts/runs/count and exact allowlisted reason/column; null absent values. This is a
   counterfactual failure locator, not evidence that production may omit row 1.
6. Synthetic tests cover every refinement/identity/equality category, family mapping,
   recurrence/outlier relations, conservation, deterministic result, counterfactual
   envelope integrity and exactly one importer call. Serialized result/error must exclude
   every exact synthetic sentinel plus token/value/raw/length/hash/record fields. Preserve
   all 006-i category/default preflight/full-smoke behavior and no broad catch.
7. Run all focused objective-005/006, contract/full pytest, Ruff/mypy, OAP and native
   baseline sequentially before source. Every uv command must set owned validated
   `UV_PROJECT_ENVIRONMENT` and `UV_CACHE_DIR` first; never touch/repair repo `.venv` or
   overlap checks. Source tree stays unchanged and exact diff must prove it.
8. Retain one exact lock-derived 006-j environment through preflight and source action.
   From owned non-repo cwd with no PYTHONPATH and isolated Python, pass preflight, then
   perform exactly one bounded direct 006-j GET to one literal source part. No broad
   search, retry, second GET or unowned interpreter.
9. Using that same interpreter/path, invoke the committed refined diagnostic once.
   Require canonical verifier, one member access, structural aggregate, original numeric
   conservation, complete row-1 refinement and one omit-row-1 counterfactual importer
   result. Stop/null on mismatch; clean and verify only exact source/env/cwd/run paths.
10. Add `resources/source-acquisitions/gigafida-2.0-words-006-j.json` with exact UTC,
    canonical/preflight facts, one 006-j GET/cumulative twelve, preserved 006-h/i facts,
    fixed marker/identity/equality predicates, counterfactual result, no content/retention/
    temp and redistribution false. Record correction: actual 006-i starting remote
    `6d11312b6ab169e0000269dc4abd23c2f0a1385b`; its report field
    `f14686c8b30962a948ca4dd5acba7ebbe0a9d86a` is the implementation head. Do not
    edit that report.
11. Receipt tests validate enum/key allowlists, 32-row/768-cell conservation, row-1
    refinement/equality counts, counterfactual attempt, history/correction and forbidden
    fields. Docs call all row-role/unit meanings unresolved pending strategic selection.
12. Preserve active mode 100644, dependencies, objective-001 source/wheel root laziness,
    003–006-i contracts and governance. After receipt/docs run all final checks/fsck and
    final-head CI. Report `starting_remote_sha` must be exact `94f09a22dc202c29f61a87bfcc8cc68e7a076dcf`;
    criteria is a string, commands contain no angle placeholders, sole SELF, no merge/
    live/release/deployment/milestone claim.

## Acceptance criteria

1. Complete fixed row-1 marker/equality/identity profile is deterministic and contains
   no source value/hash/length material.
2. One 006-j fetch (cumulative twelve) reproduces prior aggregates and records one safe
   omit-row-1 current-importer result/reason/column without treating omission as valid.
3. `src/` remains unchanged; receipt/docs preserve history and correct 006-i report
   identity, exact cleanup/non-retention and unresolved semantic interpretation.
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
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-j
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-j
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git ls-files --stage oap/active
git diff --exit-code 94f09a22dc202c29f61a87bfcc8cc68e7a076dcf...HEAD -- src
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Also run the exact preflight, one acquisition, refined diagnostic and exact cleanup.

## Local setup and constraints

One 006-j request after offline/preflight green. Owned literal paths only; no broad
search/delete, repo `.venv`, concurrency, raw values or retention. Git maintenance off.

## Documentation

Record only derived row-marker/identity/counterfactual evidence and the 006-i identity
correction. Do not select semantics or rewrite historical evidence.

## Git and report publication

Same PR #7. New commits only, no amend/force. Push non-report work/check CI; sole
`oap/reports/006-j-refine-marker-row-and-numeric-units.md` SELF report with literal
implementation parent, remote verify, exact OK, exit. No merge.

## Decision classification

D0. Content-free source-format diagnosis and evidence correction; no product conversion,
human intent, rights, live-service, release or deployment decision.

## Deferred human adjudication
- Decision: NONE

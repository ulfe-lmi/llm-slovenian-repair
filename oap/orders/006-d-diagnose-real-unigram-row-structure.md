# Work order 006-d — Diagnose real unigram row structure

Status: FINAL

```oap-metadata
{
  "id": "006-d",
  "title": "Diagnose real unigram row structure",
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
  "local_work": "Clean objective branch at remote append-only 006-c BLOCKED reconciliation head 898ccbc04ea1c8450f93ce3f1b7cc0869f97e9f9; preserve ignored environments/caches and private incident reviews.",
  "prior_review": "006-c single verifier-first fetch read 32 rows but content-free shape check failed without recording discriminating categories; product parser was not run and must not be changed again from guesswork.",
  "provenance": [
    {"kind": "E", "reference": "006-c receipt: BLOCKED_STRUCTURAL_ROW_SMOKE, rows_read 32, rows_qualified null, failure STRUCTURAL_ROW_SHAPE_MISMATCH before importer, one GET/cumulative five, cleanup/no-content true."},
    {"kind": "I", "reference": "Strategic review finds current receipt insufficient to distinguish terminal-tab counts, CSV field counts, quoting, empty/nonempty extra fields, embedded delimiters or newline variation; exact next mutation is unresolved."},
    {"kind": "A", "reference": "S-DIAGNOSE-01 requires the smallest experiment separating plausible source-format hypotheses and an explicit stop condition before product mutation; evidence must remain bounded/non-content."}
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

006-d is a diagnostic corrective suffix on PR #7. Preserve all 006-a/b/c code,
receipts, reports, publication-reconciliation commits and CI. It diagnoses only; no
importer-format change or product compatibility claim.

## Provenance

- E: Existing hypotheses each failed at the real source: strict 28 fields, then one
  assumed terminal tab. The latest receipt lacks the aggregate shape needed to choose.
- I: Plausible causes include nonuniform terminal delimiters, quoting differences,
  semantic/empty extra fields, embedded quoted tabs or row/newline variation.
- A: One bounded classifier should separate these without exposing field values or
  mutating the parser. Stop after the evidence receipt, even if one answer looks clear.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`. Sole PR #7 at valid 006-c
BLOCKED report reconciliation `898ccbc04ea1c8450f93ce3f1b7cc0869f97e9f9`; exact
report/transcript and both final checks pass. 006-c implementation chain and stale-
active/report-hash failures remain. No archive/temp exists. Cumulative observed GETs five.

CRITICAL empty; branch protection/rulesets disabled. No live/release/deployment gates.

## Governance

Use compact law, LR-008 and security/testing. No source values, per-row hashes or paths
in output. Preserve parser code and all protected/current sources. D0/NONE.

## Goal and dependencies

Produce a durable content-free structural diagnosis of exactly the first 32 real data
rows after accepted artifact verification, sufficient for strategy to order one exact
format correction. Do not implement that correction in this round.

## Scope

1. Add a standard-library, offline row-structure classifier plus synthetic tests.
2. Perform one verified temporary 006-d fetch, classify 32 rows, write aggregate receipt.
3. Update only direct diagnostic documentation/status/inventories and protocol files.
4. Run complete checks and publish. No importer behavior change.

## Non-goals

No modification to `src/llm_slovenian_repair/unigram_importer.py`, root exports, existing
synthetic TSV, 006-a/b/c receipts, actual row semantics, parser acceptance, real importer
run, extra source request, full import/index/detector, committed source bytes, dependency,
live Qwen, GitHub setting, merge, release or deployment.

## Files and boundaries

Expected new diagnostic script such as `scripts/diagnose_unigram_rows.py`, focused tests
using only synthetic structure, new 006-d receipt, status/data-source/development docs,
generated inventories and 006-d order/active/report. Runtime package bytes should not
change. Diagnostic accepts a caller-owned binary stream after external verification;
it performs no path open/network/write and returns immutable aggregate metadata.

## Requirements

1. Define finite strict diagnostic schema/limits. Accept exactly 1–32 CRLF-terminated
   byte rows with a total/line byte cap. Parse UTF-8 and CSV/quoted-tab structure only
   to classify shape; never return/store decoded field values, raw bytes, per-row hashes,
   token lengths or content-derived examples.
2. For the sample as a whole record only: requested/read count; UTF-8 valid/invalid and
   CRLF/LF/missing-newline counts; histogram of terminal-tab counts (`0`,`1`,`2+`);
   CSV field-count histogram; empty-final-field count; nonempty-field-after-28 count;
   fully-all-fields-quoted count; embedded-tab-in-quoted-field row count; quote-parse
   error count; existing parser finite failure-reason histogram; min/max whole-row byte
   length; and first structurally failing source line number. No other content metric.
3. Implement quote/delimiter classification robustly with doubled-quote handling. Tests
   cover exact 28/no terminal, 28/one terminal, double terminal, nonempty 29th, embedded
   quoted tab, escaped quote, malformed/unclosed quote, LF/missing newline, invalid UTF-8,
   mixed sample and row/count/byte limits. Assert output JSON contains no input values.
4. Do not import or call `import_unigrams` to decide validity except optionally catch its
   finite error reason per row without retaining its model/output; the diagnostic is not
   an acceptance test. Do not change importer/tests/fixture to make diagnosis pass.
5. After diagnostic tests and complete offline baseline pass, perform exactly one 006-d
   GET of the same canonical artifact with `curl --disable`, direct HTTPS/no redirect,
   no credentials/options, fail-on-HTTP, connect <=10s, total <=900s, exact max-filesize
   115865656, owned `/tmp/...006-d.../*.part`. No other source contact.
6. Run accepted verifier before ZIP/member access and require exact size/MD5/SHA/member
   facts. Skip 14 preamble/header lines without output, feed exactly next 32 complete
   rows to the classifier, and print/write only the aggregate schema from requirement 2.
   Do not print header names or row content. Do not change code after seeing results
   except receipt/docs/tests that assert the aggregate diagnostic schema, not a parser fix.
7. Close/delete exact owned temp tree and verify no matching directory. New receipt
   records exact UTC/source/inventory/artifact/header identities, verifier PASSED,
   one 006-d GET/cumulative six, 006-a exact-one false, prior b/c BLOCKED, aggregate
   diagnostic result, no importer run, no content/bytes retained, cleanup and
   redistribution false. If classifier fails, preserve partial aggregates as null and
   report BLOCKED; never refetch.
8. Focused tests validate receipt keys/types/bounds and ensure no forbidden content
   fields (`fields`, `values`, `raw`, `row_hash`, decoded strings). A COMPLETE diagnostic
   means hypotheses were separated, not importer compatibility or objective completion.
9. Preserve all existing product tests/dependencies/root/wheel/source inventory/
   protected governance. Generated bootstrap/inventory hashes change only for ordered
   docs/script/tests/receipt and pass source-generation validation.
10. Run diagnostic/focused/all contract/full pytest, Ruff/mypy, full OAP, native baseline,
    transcript/governance/protected checks and required CI. Force-stage `006-d\n`.
    Report uses criteria string and exact implementation/SELF shape, names diagnosis
    versus product status, and makes no future-CI/source-content/release claim.

## Acceptance criteria

1. Synthetic classifier tests distinguish every named shape and return content-free
   bounded aggregate metadata; importer/package behavior is byte-identical to 006-c.
2. Exactly one verifier-first 006-d GET classifies exactly 32 real rows and records a
   nonempty discriminating histogram/first-failure boundary without content.
3. Receipt records cumulative six, prior blocked rounds, no importer execution, no
   retained source/temp and cleanup true. Evidence is sufficient to specify one next
   format contract or explicitly says no single bounded contract is supported.
4. Full checks/final-head CI pass; PR remains unmerged; no product/live/release/deploy.

## Verification

Report exact owned commands:

```text
uv run --frozen --python 3.12 pytest tests/contract/test_objective_006_diagnostics.py -q
uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q
uv run --frozen --python 3.12 pytest tests/contract -q
uv run --frozen --python 3.12 pytest -q
uv run --frozen --python 3.12 ruff check src scripts tests
uv run --frozen --python 3.12 mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-d
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-d
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Also execute the one verifier/classifier/cleanup boundary. No retry or parser mutation.

## Local setup and constraints

One exact 006-d request after offline green. Owned `/tmp`, accepted public artifact,
no redirect/config/credentials/content output; all CI offline. Preserve ignored caches,
protected systems/repos/settings and no customer/model text.

## Documentation

Record only aggregate shape diagnosis and limits, clearly not source values/importer
success. Preserve incident history and current blocked product status.

## Git and report publication

Stay PR #7. Commit/push non-report diagnostic/order/active/receipt, wait implementation
CI, record SHA, then sole report
`oap/reports/006-d-diagnose-real-unigram-row-structure.md` with SELF parent. Push,
remote verify, exact OK, exit. No merge.

## Decision classification

D0. Bounded read-only diagnosis reduces uncertainty without selecting product behavior,
exposing content or crossing rights/live/release/deployment authority.

## Deferred human adjudication
- Decision: NONE

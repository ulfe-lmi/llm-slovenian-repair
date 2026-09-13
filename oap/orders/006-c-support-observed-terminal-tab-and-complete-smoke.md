# Work order 006-c — Support observed terminal tab and complete smoke

Status: FINAL

```oap-metadata
{
  "id": "006-c",
  "title": "Support observed terminal tab and complete smoke",
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
  "local_work": "Clean objective branch at remote 006-b BLOCKED report head 4fc0f42d119ea22c914e0898b34a9a5e37cfa5c8; preserve ignored environments/caches and private incident reviews.",
  "prior_review": "006-b provenance/API/result corrections pass, but its single verifier-first real smoke stopped at line 16 because publisher data rows have one trailing tab after 28 quoted fields; no retry or value logging occurred.",
  "provenance": [
    {"kind": "E", "reference": "006-b receipt records exact verified archive identity and failure INVALID_QUOTING at line 16 boundary trailing-tab-after-28-fields, with one GET/cumulative four and complete cleanup."},
    {"kind": "I", "reference": "Strategic review confirmed header remains exact 28 quoted fields/no terminal tab while first real data row has an empty structural 29th field caused by one terminal tab; current parser rejects that exact source format."},
    {"kind": "A", "reference": "S-DIAGNOSE-01/S-EVIDENCE-01 and 006 importer contract require the smallest demonstrated format correction, strict negatives, verifier-first real boundary and no silent optional-column acceptance."}
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

006-c is the next corrective suffix on PR #7. Preserve 006-a's acquisition/report
incidents and BLOCKED result and 006-b's verifier-first incompatible smoke. No history
rewrite, same-SHA retry or retroactive success label.

## Provenance

- E: The accepted archive passed integrity and ZIP checks; parser failed at the first
  data row solely because one tab follows its 28th quoted field before CRLF.
- I: The header contract has no terminal delimiter. The smallest hypothesis is that
  data records use a single empty terminator, not a general optional 29th column.
- A: Test this exact distinction and fail closed on every wider shape before claiming
  compatibility. A new single fetch may test multiple rows and the corrected parser.

## Current verified state

Accepted main remains `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #7 is sole
open PR at 006-b BLOCKED SELF head `4fc0f42d119ea22c914e0898b34a9a5e37cfa5c8`,
implementation parent `b8202c63b4fa609e35824705df53b4282d752b23`; remote report,
transcript and both final checks verify. Worktree clean; no archive/temp source bytes.

006-b software corrections independently pass. Its receipt has one GET/cumulative four,
accepted size/MD5/SHA, BLOCKED line 16, null smoke hashes and cleanup true. CRITICAL is
empty; branch protection/rulesets disabled. Live/release/deployment remain closed.

## Governance

Apply compact coding law, LR-008 and security/testing. Preserve source identity,
evidence completeness, prior receipts/reports, protected governance and no-content
logging. Only exact observed formatting may change. D0/NONE.

## Goal and dependencies

Support the verified Gigafida data-record terminator without admitting arbitrary extra
columns, then establish a deterministic 32-row real compatibility smoke from one new
verified acquisition. Keep import completeness PARTIAL and all prior failures visible.

## Scope

1. Bind data-row format to 28 quoted fields plus exactly one terminal tab and CRLF;
   header remains its existing exact no-terminal-tab bytes.
2. Update synthetic fixture/parser/tests and documentation for that distinction.
3. Perform one verifier-first 006-c fetch and structural/sample smoke; create receipt.
4. Run complete checks and publish 006-c on PR #7.

## Non-goals

No optional/general 29th field, arbitrary trailing whitespace/delimiters, new schema
column, full import/index/database/lookup/detector, another source, committed real row,
automatic download, dependency, root export, live Qwen, GitHub setting, merge, release
or deployment. No alteration of 006-a/b receipts except direct navigation if necessary.

## Files and boundaries

Expected importer, objective-006 tests/synthetic fixture/readme, docs/status, new
`gigafida-2.0-words-006-c.json`, generated inventories and protocol files. Keep receipts
and fixtures outside wheel/sdist. Parser remains stream-only and offline.

## Requirements

1. Header parsing remains exact existing `EXPECTED_HEADER_BYTES`: 28 quoted fields,
   tab between fields, no tab after field 28, CRLF, line 15 and same SHA. A header with
   terminal tab must reject.
2. Every data record must be 28 all-quoted fields followed by exactly one ASCII tab and
   CRLF. Consume that tab as a source-specific record terminator, not a 29th semantic
   field. Preserve `raw_fields` length 28 and all numeric/index mappings unchanged.
3. Reject a data row with no terminal tab, two or more terminal tabs, spaces after the
   tab, a quoted/nonempty 29th field, unquoted last field, tab inside quoted content,
   LF-only/missing newline or any field count other than 28. Errors finite/non-content.
4. Update the project-authored synthetic fixture to exact row terminators and its tests.
   Add positives for header/no-tab plus rows/one-tab and negatives for requirement 3.
   Preserve Unicode/ambiguity/zero/determinism/resource/provenance/tamper proofs.
5. Update an explicit source-format constant/summary/receipt field for
   `data_record_terminator=TAB_BEFORE_CRLF`; bind it in provenance/result validation so
   callers cannot select a permissive mode. Shared completeness and one entry point stay.
6. Run corrected focused/full offline tests before network. Then perform exactly one
   new 006-c GET of the same canonical URL under accepted 005 controls: `curl --disable`,
   direct HTTPS/no redirect/no credentials, fail, connect <=10s, total <=900s,
   `--max-filesize 115865656`, validated owned `/tmp/...006-c.../*.part`.
7. Run accepted artifact verifier before ZIP access. Require exact size/MD5/SHA, five
   members and limits. From the selected member, inspect at most 32 complete data rows
   only for structural shape; require each has exactly 28 quoted values plus one terminal
   tab/CRLF. Emit no header/row values or per-row hashes to logs.
8. Feed exactly the 14 preamble lines, existing header and 1–32 structurally qualified
   rows to `import_unigrams` twice from the same verified archive. Use exact real
   provenance, source/query COMPLETE and import PARTIAL. Require equal immutable results,
   record counts and input/output hashes. Output only aggregate count/hashes/status.
   On any new incompatibility, stop without another request or parser weakening.
9. Close streams, delete exact owned temp tree and verify absence before commit. Add a
   new receipt recording actual UTC, exactly one 006-c GET, cumulative objective count
   five, 006-a exact-one false, 006-b blocked terminator observation, verifier facts,
   structural rows checked, smoke attempts/runs/count and equal hashes, PARTIAL import,
   no content, no retained bytes/temp and redistribution false. If blocked, null unknowns.
10. Tests validate the receipt schema/status/counts/hashes and distinguish current 006-c
    evidence from historical 006-a/b. No receipt contains product SELF commit guess.
11. Preserve all earlier tests, lock/dependencies, root source/wheel laziness, source
    inventory, protected governance/history. Generated bootstrap/inventory hashes may
    change only for ordered product docs/tests/files and must pass source-generation
    checks; candidate governance hashes cannot change.
12. Run focused/broad product, Ruff/mypy, full OAP, native baseline, transcript,
    governance/protected checks and required CI. Force-stage exact `006-c\n`; report
    uses criteria string, exact implementation SHA and sole SELF commit, with no future
    CI or retroactive prior-round claims.

## Acceptance criteria

1. Exact header/no-terminator and data-row/one-terminator contracts pass; all wider/
   missing/malformed shapes reject while existing importer semantics stay green.
2. One 006-c verifier-first GET confirms the terminal-tab pattern across 1–32 rows and
   the corrected importer runs twice identically with nonzero count/hashes under PARTIAL.
3. Receipt records cumulative five and preserves 006-a/b failures; archive/temp cleanup
   and no content logging/retention are verified.
4. Full product/OAP/native/protected/final-head checks pass; PR #7 remains unmerged;
   no index, source release, live test, milestone, release or deployment claim.

## Verification

Use owned environment and report:

```text
uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q
uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py tests/contract/test_objective_005.py -q
uv run --frozen --python 3.12 pytest tests/contract -q
uv run --frozen --python 3.12 pytest -q
uv run --frozen --python 3.12 ruff check src scripts tests
uv run --frozen --python 3.12 mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-c
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-c
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Record the one real verify/shape/twice-import/cleanup command with aggregate evidence
only. A failure publishes BLOCKED and no second request.

## Local setup and constraints

One exact 006-c source GET after offline tests. Same public artifact/host/integrity and
owned `/tmp` controls; no redirect/config/credential; no content output. All other tests
offline. Preserve ignored `.venv`/caches and protected systems/repos/settings.

## Documentation

Document header versus row-terminator distinction, current receipt/smoke outcome and
PARTIAL scope. Preserve 006-a/b incident narrative. No full-source/quality/legal/live/
release/deployment overclaim.

## Git and report publication

Stay on PR #7. Commit/push all non-report work/order/active/receipt, require implementation
CI, record SHA, then publish only
`oap/reports/006-c-support-observed-terminal-tab-and-complete-smoke.md` as SELF with
implementation parent. Push, remotely verify, send exact `OK`, exit. No merge.

## Decision classification

D0. Exact observed format correction plus one bounded public artifact verification is
reversible and fail-closed. No human intent, rights/release/live/deploy boundary changes.

## Deferred human adjudication
- Decision: NONE

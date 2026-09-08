# Work order 006-f — Support mixed terminal tab and prove import

Status: FINAL

```oap-metadata
{
  "id": "006-f",
  "title": "Support mixed terminal tab and prove import",
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
  "local_work": "Clean branch at remote 006-e COMPLETE diagnostic report head 82231a627cceda9c8533a4f37b855aec13ed0873; Git fsck clean; preserve ignored environments and private Git-damage backup.",
  "prior_review": "006-e diagnosed 32 real rows: 31 exact 28-field/no-terminal-tab and one 28 semantic fields plus one empty terminal-tab field, all UTF-8/CRLF/quoted with no nonempty extra or parse error; no importer run.",
  "provenance": [
    {"kind": "E", "reference": "006-e receipt COMPLETE_ROW_DIAGNOSTIC: field histogram 28:31/29:1, terminal tabs 0:31/1:1/2+:0, empty final 1, nonempty-after-28 0, structural failures 0, one GET/cumulative seven and cleanup."},
    {"kind": "I", "reference": "Strategic review concludes the source record contract is exactly 28 quoted semantic fields with an optional single empty terminal tab; 006-c's mandatory-tab assumption is contradicted by 31/32 rows."},
    {"kind": "A", "reference": "ARCHITECTURE §8 and S-EVIDENCE-01 require source-format fidelity, strict bounded rejection, exact evidence scope and real entry-point proof before accepting the importer."}
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

006-f is the format/proof correction on existing PR #7. Preserve 006-a–e reports,
receipts, invalid-publication recoveries, source-request counts and Git incident.

## Provenance

- E: Real aggregate disproves mandatory terminal tab while proving only two safe shapes.
- I: Optional **single empty structural terminator** is narrower than optional fields:
  both shapes retain exactly 28 semantic values and no nonempty value after field 28.
- A: Implement only those shapes, test wider negatives, then call the real importer.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`. Sole PR #7 at valid 006-e
COMPLETE diagnostic SELF `82231a627cceda9c8533a4f37b855aec13ed0873`, implementation
`6fdd5b440fc04951cde8d647c93bdeaaa61c9f18`; final checks/transcript/fsck pass.
Runtime importer remains 006-c and fails 31/32 diagnosed rows due mandatory tab.

No archive/temp remains; cumulative GETs seven. CRITICAL empty. The GitHub branch
protection API returns 404 and repository rulesets are empty, so the development gate
currently depends on OAP/agent procedure rather than a server-side refusal. Do not
change repository settings. No live/release/deployment gate is authorized.

## Governance

Compact law, LR-008, security/testing. Exact two-shape input only, no content logs.
Sequential tests/Git operations, explicit maintenance disabled. D0/NONE.

## Goal and dependencies

Correct the importer to the evidenced mixed terminator format and prove the actual
entry point twice on the same verified 32-row prefix under PARTIAL import evidence.

## Scope

1. Change importer/provenance/summary from mandatory tab to optional single empty tab.
2. Update synthetic fixture/tests and direct docs while preserving canonical API.
3. One verifier-first 006-f fetch; structural check plus twice-run importer; receipt.
4. Complete sequential verification and publish on PR #7.

## Non-goals

No arbitrary 29th column/trailing whitespace/multiple tabs, full import/index/database/
lookup/detector, n-grams/other source, committed real row/archive, automatic downloader,
dependency/root export, diagnostic-source rewrite, live Qwen, GitHub setting, merge,
release or deployment. Prior rounds remain BLOCKED/diagnostic as recorded.

## Files and boundaries

Importer, objective-006 synthetic fixture/tests, direct docs/status, new 006-f receipt,
generated manifests and protocol. Diagnostic script changes only if a direct shared
constant/test reference is strictly necessary; no scope expansion. Receipts/fixtures
remain outside package artifacts.

## Requirements

1. Replace `TAB_BEFORE_CRLF` contract with exact finite name such as
   `OPTIONAL_SINGLE_EMPTY_TAB_BEFORE_CRLF`, bound in provenance and summary. Header stays
   exact 28 fields/no trailing tab. Data row accepts exactly either (a) 28 all-quoted
   fields ending immediately before CRLF or (b) those 28 fields plus one ASCII tab
   immediately before CRLF, treated as no semantic field.
2. Reject two/more terminal tabs, tab plus spaces, a quoted/unquoted nonempty 29th field,
   any 29th semantic value, unquoted semantic field, embedded tab, wrong field count,
   LF/missing newline and all existing bad input. Raw fields stay exactly length 28;
   input hash still binds original bytes including whether terminal tab was present.
3. Synthetic fixture/tests include both accepted shapes in one deterministic stream.
   Test equal semantic parsing of otherwise identical row with/without one terminal tab
   while input hashes differ; output canonical records/hashes should match when the row
   identity/row number is the same. Retain all ambiguity/Unicode/count/provenance/
   summary/resource negatives and one public submodule entry point/no root export.
4. Update 006-c mandatory-tab documentation as superseded by 006-e aggregate; never
   rewrite old receipt/report. New docs state 31/1 bounded sample, not universal corpus
   proof. Import/source/query completeness remain explicit; real smoke import PARTIAL.
5. Run focused objective-006 plus full supported native baseline sequentially before
   source access. Use owned `/tmp` environment or known system dependency closure; never
   use/repair repository `.venv`. No overlapping full/OAP/Git operations.
6. Perform exactly one 006-f GET of canonical archive with `curl --disable`, direct
   HTTPS/no redirect/no credentials/options, fail, connect <=10s, total <=900s,
   max-filesize 115865656, owned validated `/tmp/...006-f.../*.part`.
7. Run accepted artifact verifier before ZIP access. Open selected member once. Read
   exactly 14 preamble, exact header and next 32 complete rows into one bounded in-memory
   envelope without printing/writing them. Confirm each data row is one of the two 006-e
   shapes and aggregate equals field `{28:31,29:1}`, tabs `{0:31,1:1,2+:0}`, with no
   nonempty extra/quote/UTF-8/newline failure. A mismatch stops with no retry.
8. Call `import_unigrams` twice on the same envelope with exact real provenance,
   source/query COMPLETE and import PARTIAL, limits covering only this sample. Require
   equal immutable results, exactly 32 records, equal nonnull input/output hashes and
   summary bindings. Emit only aggregate count/hashes/status, never source/header values,
   per-row hashes or model dumps. Any parse/duplicate/numeric incompatibility stops.
9. Close/delete exact temp tree and verify absence. New receipt records exact UTC,
   canonical source/verifier facts, one 006-f GET/cumulative eight, prior incident/
   diagnostic results, structural aggregate, smoke attempts=2/runs=2/count=32/equal
   hashes, PARTIAL import, no content/retention/temp and redistribution false. Null
   unobserved values if blocked; no product commit guess.
10. Receipt tests validate schema/count/hashes/completeness/no-content fields and prior
    history distinction. Direct independent-style test probes both accepted shapes and
    every rejected extension through actual importer.
11. Preserve lock/dependencies, 001 root/wheel laziness, 003–005 contracts, source
    inventory, diagnostic evidence, protected governance. Generated hashes only for
    ordered current files; fsck/protected checks pass. Force-stage exact `006-f\n`.
12. Run focused/all contract/full pytest, Ruff/mypy, OAP, native baseline, transcript,
    governance, diff/fsck and both required CI. Report criteria is a string, distinguishes
    all implementation/correction SHAs and real evidence, sole SELF commit, no future-
    CI/prior-round rewrite/live/release/deployment claim.

## Acceptance criteria

1. Exactly two evidenced row terminator shapes pass and all wider shapes fail; semantic
   records stay 28 fields with byte-sensitive input hash and stable canonical output.
2. One 006-f verifier-first fetch matches the 006-e aggregate and real importer runs
   twice on 32 rows with identical nonnull hashes/count under PARTIAL import evidence.
3. Receipt records cumulative eight/prior incidents, no content/retention, cleanup and
   redistribution false; no full-source/quality claim.
4. Full sequential local/final-head checks and fsck pass; PR #7 remains unmerged during
   coding; no live/release/deployment action.

## Verification

```text
pytest tests/contract/test_objective_006.py -q
pytest tests/contract/test_objective_006_diagnostics.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-f
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-f
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Use owned/available dependency environment. Also run one real verifier/aggregate/
twice-import/cleanup action with aggregate output only; no retry.

## Local setup and constraints

One exact 006-f request after offline green; owned `/tmp`, no repo `.venv`, no concurrent
broad checks. Preserve private Git backup. No content/credential/protected system changes.

## Documentation

Document mixed optional terminator, exact bounded sample and real-smoke outcome without
claiming full archive/index/linguistic/legal/live/release/deploy readiness.

## Git and report publication

Same PR #7. New commits only, maintenance-disabled explicit Git, no amend/force. Push
non-report work/check CI; sole `oap/reports/006-f-support-mixed-terminal-tab-and-prove-import.md`
SELF report, remote verify, exact OK, exit. No merge.

## Decision classification

D0. Evidence-fixed parser compatibility and one bounded public source smoke; no human
intent, rights/release/live/deployment decision.

## Deferred human adjudication
- Decision: NONE

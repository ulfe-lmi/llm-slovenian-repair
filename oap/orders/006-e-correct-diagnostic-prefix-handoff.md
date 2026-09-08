# Work order 006-e — Correct diagnostic prefix handoff

Status: FINAL

```oap-metadata
{
  "id": "006-e",
  "title": "Correct diagnostic prefix handoff",
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
  "local_work": "Clean branch at remote 006-d BLOCKED report head 743d633bcbcbeb3c072467fe8913282f825736a7; local Git fsck clean after recorded additive object reconstruction; preserve ignored environments and private recovery backup.",
  "prior_review": "006-d classifier/tests pass, but its real command double-skipped input and failed requested-row-incomplete without aggregate diagnosis; no importer mutation or refetch occurred during recovery.",
  "provenance": [
    {"kind": "E", "reference": "006-d receipt records verifier PASSED, one GET/cumulative six, preamble_lines_skipped 14, diagnostic_input_complete false, requested-row-incomplete, aggregate null, importer not run and cleanup true."},
    {"kind": "I", "reference": "Strategic reconstruction of the command shows producer skipped 14 then emitted 32 including header while classifier also skipped 14/requested 32; direct call on ZipExtFile with one skip of 15 removes the duplicated handoff."},
    {"kind": "A", "reference": "S-DIAGNOSE-01/S-EVIDENCE-01 require correction at earliest invocation boundary, tested real routing, no repeated source request within a suffix and no product mutation before discriminating evidence."}
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

006-e corrects only the 006-d diagnostic invocation on PR #7. Preserve all historical
BLOCKED receipts/reports, publication recoveries, failed checks and Git incident facts.

## Provenance

- E: The classifier did not receive the intended sample; its code was not disproved.
- I: One skip must occur against the original member stream: 14 preamble plus header =
  15, then exactly 32 rows. A pre-sliced pipe plus another skip is invalid routing.
- A: Test and execute the actual stream-routing boundary without changing importer.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`. Sole PR #7 at 006-d
BLOCKED SELF `743d633bcbcbeb3c072467fe8913282f825736a7`, implementation
`458481f4dc410132da9d754b75eac92691435160`; remote report/transcript/final CI pass.
Local worktree clean, fsck clean, no temp/source bytes. Cumulative source GETs six.

CRITICAL empty; branch protection/rulesets disabled. No live/release/deployment gate.

## Governance

Compact coding law, LR-008, SECURITY/TESTING. Content-free diagnostics only. Preserve
runtime importer/package/protected sources. Run tests and Git operations sequentially;
disable automatic maintenance on explicit shell Git. D0/NONE.

## Goal and dependencies

Deliver the missing real 32-row aggregate diagnosis through one correctly routed,
verified source stream. This is diagnostic evidence only; stop before parser mutation.

## Scope

1. Add a public-in-script `classify_stream`/equivalent wrapping prefix read plus existing
   classifier; CLI reuses it.
2. Add a real synthetic ZIP/member routing test for one 15-line skip and 32 data rows.
3. One verifier-first 006-e GET, direct ZipExtFile classification, aggregate receipt.
4. Direct diagnostic docs/inventories/protocol, sequential checks and publication.

## Non-goals

No change to importer/root/synthetic unigram fixture/existing receipts, no parser
acceptance decision, real importer run, second request, row/header output, full index,
dependency, live Qwen, GitHub setting, merge, release or deployment.

## Files and boundaries

Existing diagnostic script/tests, new 006-e receipt, direct docs/status/generated files
and protocol paths. Runtime `src/` bytes must be identical to 006-d. Diagnostic consumes
the original verified ZIP member stream directly; no shell producer pipe.

## Requirements

1. Add one bounded function accepting a caller-owned binary stream plus `skip_rows` and
   `requested_rows`; it calls prefix reading exactly once and classifies exactly once.
   Defaults must not hide routing. Preserve 0–1000 skip, 1–32 requested, byte/line caps,
   requested-row-incomplete and content-free aggregate contract.
2. CLI delegates to that same function. No duplicate skip/slice logic. Unit tests prove
   calls with 15/32 consume exactly 15 prefix plus 32 rows and neither more nor fewer.
3. Add an integration test creating a project-authored synthetic ZIP with one member:
   14 preamble lines, one header line and 32 mixed structural data rows. Open with
   `zipfile.ZipFile.open`, call stream function `skip_rows=15, requested_rows=32`, and
   assert read count/aggregate/first-failure. Prove no extraction/file output/content.
4. Retain all 006-d classifier shape/limit/content-leak negatives. Add double-skip and
   14-skip/header-inclusion regressions that fail `requested-row-incomplete` or produce
   a distinguishable header shape, proving the corrected integration is meaningful.
5. Run focused diagnostic/importer/all offline checks and supported native baseline
   sequentially before network. Do not use or repair repository `.venv`; use owned `/tmp`
   or `PYTHONPATH=src` only where the dependency closure is already available.
6. Perform exactly one 006-e GET of canonical archive using `curl --disable`, direct
   HTTPS/no redirect/no credentials/options, fail, connect <=10s, total <=900s,
   max-filesize 115865656, owned validated `/tmp/...006-e.../*.part`.
7. Accepted verifier must pass before member access. Open selected member once and call
   the tested stream classifier directly with `skip_rows=15`, `requested_rows=32`.
   Do not pre-read/slice/pipe rows. Output only the aggregate schema; no values/header/
   per-row hash. Stop after diagnosis even if next correction is obvious.
8. Close/delete exact temp tree and verify absence. New receipt records exact source/
   verifier identities, one 006-e GET/cumulative seven, prior a–d blocked facts, exact
   invocation 15/32/direct, aggregate histograms/first failing line, no importer run,
   no content/retention, cleanup and redistribution false. If diagnostic fails, null
   unknowns and no retry.
9. Receipt tests validate every aggregate key/type/count sums/bounds, forbidden content
   keys and distinction from prior receipts. Do not include product implementation SHA.
10. Preserve importer/package bytes exactly, dependencies, source inventory, protected
    governance and history. Generated hashes only for ordered script/tests/docs/receipt.
    Before commit compare `src/` tree to 006-d head; it must be unchanged.
11. Run all named product/OAP/native/transcript/governance/protected checks sequentially.
    Verify Git fsck before push. Force-stage exact `006-e\n`; no amend/force push.
12. Report result COMPLETE if aggregate diagnostic succeeds, otherwise BLOCKED. Criteria
    is one meaningful string and report distinguishes diagnostic completion from product
    compatibility; sole SELF commit, no future CI/content/live/release/deploy claim.

## Acceptance criteria

1. Direct stream/ZIP integration tests prove one 15-line skip and exactly 32 classified
   data rows; double-skip/header-inclusion cases distinguishably fail.
2. Exactly one verifier-first 006-e GET produces a nonnull aggregate over 32 rows with
   count-consistent histograms and first-failure line, then cleanup/no-content passes.
3. Receipt records cumulative seven/prior failures/no importer run and enough evidence
   for one next format order; runtime importer/package unchanged.
4. Full sequential checks, fsck and final-head CI pass; PR unmerged; no product/live/
   release/deployment claim.

## Verification

```text
pytest tests/contract/test_objective_006_diagnostics.py -q
pytest tests/contract/test_objective_006.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-e
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-e
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Use owned environment for commands needing locked dependencies. Also run the one real
verifier/direct-classifier/cleanup action, no retry.

## Local setup and constraints

One exact 006-e request after offline green. Owned `/tmp`; no repository `.venv`, no
concurrent broad checks/Git operations, no source content output. Preserve private Git
damage backup and protected systems/repos/settings.

## Documentation

Record corrected routing and aggregate diagnosis only. Preserve 006-a–d incidents and
avoid importer/full-source/quality/legal/live/release/deploy claims.

## Git and report publication

Same PR #7. New non-report commits only (no amend); push/wait CI, then sole
`oap/reports/006-e-correct-diagnostic-prefix-handoff.md` SELF commit. Remote verify,
exact OK, exit. No merge.

## Decision classification

D0. Corrects diagnostic routing and gathers bounded content-free evidence; no product
behavior or human/legal/live/release/deployment decision.

## Deferred human adjudication
- Decision: NONE

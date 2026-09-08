# Work order 006-b — Bind unigram provenance and complete smoke

Status: FINAL

```oap-metadata
{
  "id": "006-b",
  "title": "Bind unigram provenance and complete smoke",
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
  "local_work": "Clean objective branch at remote append-only 006-a publication-reconciliation head 767062ac2b2c543c6bc6fdffae2a3fc3a39a786c; preserve ignored environments/caches and private incident records.",
  "prior_review": "006-a is truthfully BLOCKED after three GETs, pre-verifier inspection and no real importer smoke; semantic review also found unbound provenance/header line, redundant aliases, summary tampering and a mislabeled receipt hash field.",
  "provenance": [
    {"kind": "E", "reference": "Remote 006-a history preserves product head 4f3c3d66, invalid report e16c3303 and human-authorized append-only report repair 767062ac; current final checks pass but acceptance 1 remains BLOCKED."},
    {"kind": "I", "reference": "Direct probes accepted header_line_number=1, arbitrary source/release, and a result summary with schema 99/importer bogus/all-zero output hash; three public importer aliases are identical and receipt names a 40-char Git SHA as SHA-256."},
    {"kind": "A", "reference": "ARCHITECTURE §§8.1–8.2, S-EVIDENCE-01 and 006-a requirements 1/7/9 require exact source/header binding, truthful integrity summaries, one canonical seam and an actual bounded compatibility proof before merge."}
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

006-b is a corrective suffix on objective branch/PR #7. Preserve every 006-a commit,
failed/green check and BLOCKED report, including invalid e16c3303 and append-only
reconciliation 767062ac. Do not amend, force-push or describe 006-a as complete.

## Provenance

- E: Software tests passed but acquisition replay and report-schema failure required
  recovery; actual current importer compatibility remains unproven.
- I: Direct model-construction probes demonstrate missing provenance/summary binding
  and redundant public API. These are reproducible defects, not stylistic preference.
- A: Source/release/header/integrity must be explicit before unigram evidence can be
  trusted. A new correctly ordered smoke can close current compatibility without
  rewriting the historical exact-one-fetch failure.

## Current verified state

Accepted remote main is `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #7 is the
sole open PR at remote report-reconciliation head
`767062ac2b2c543c6bc6fdffae2a3fc3a39a786c`; its parent is invalid report e16c3303,
whose parent is product implementation 4f3c3d66. Current report verifies BLOCKED and
both final checks pass. Worktree has no source archive/recovery handoff or unrelated
dirty file. Exact source inventory SHA-256 is
`439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3`.

Known verified artifact facts remain size 115865656, MD5
`b20a959f9c113aeb6504f0d753d36d10`, SHA-256
`77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a`, five
members and header SHA
`c2ce44548818b72a04691c7060c0e35106393edbfde13336c60d4cd072a00638`.
CRITICAL is empty; branch protection/rulesets remain disabled. No release/deployment.

## Governance

Apply compact coding law, LR-008 and security/testing contracts. Preserve protected
governance, source inventory facts, transcript and 006-a incident evidence. Treat the
one newly downloaded archive as untrusted data, never content for logs/Git. D0/NONE.

## Goal and dependencies

Close the current unigram importer evidence boundary: exact real/synthetic provenance,
one canonical API, internally consistent immutable results and one correctly ordered
bounded real compatibility smoke. Preserve the historical 006-a failure separately.

## Scope

1. Tighten importer provenance/header/result contracts and remove redundant API.
2. Correct the recovery receipt field and add a new 006-b compatibility receipt.
3. Perform exactly one new verified temporary fetch after code/tests are ready; import
   at most 32 rows twice without content output, then delete.
4. Expand focused negative/tamper tests and direct documentation.
5. Publish 006-b on existing PR #7.

## Non-goals

No rewriting 006-a, full archive import/index, database, runtime lookup/detector,
n-grams/Sloleks/2.2/collocations, real row fixture, automatic downloader, dependency,
live Qwen, customer data, GPU/service/network setting, GitHub setting, merge, release
or deployment. Do not claim cumulative objective acquisition count was one.

## Files and boundaries

Expected existing importer/root/test/fixture/docs/receipt paths, a new 006-b receipt,
generated inventories and protocol files. Keep runtime package free of receipts/
fixtures. The parser remains stream-only/offline; network setup stays outside it.

## Requirements

1. Remove `parse_unigram_tsv` and `import_unigram_tsv` aliases. Keep exactly one public
   entry point `import_unigrams` in `unigram_importer.__all__`. Remove all objective-006
   symbols from root `llm_slovenian_repair.__all__`/lazy map; callers explicitly import
   the submodule. Retain the module in wheel payload and prove bare root import laziness.
2. Reuse accepted `contracts.EvidenceCompleteness`; remove duplicate `Completeness`.
   Preserve separate source/query/import fields without new enum vocabulary.
3. Define explicit real-versus-project-synthetic provenance. Real version 1 must bind
   exact source ID/name/release, inventory revision `source-inventory-v1`, inventory SHA
   `439bbd...de3`, artifact SHA `77ac...67a`, member/header names/hash, line 15,
   quoted-tab/UTF-8/CRLF, normalization and redistribution false. Synthetic tests use
   an explicitly synthetic identity and their actual fixture/input hashes, never fake
   Gigafida authority. Reject arbitrary source/release/hash and `header_line_number=1`.
4. Bind all `UnigramImportSummary` constants/provenance/limits/record count. Recompute
   canonical output SHA from records during `UnigramImportResult` validation and reject
   schema/importer/hash tampering. Validate record numeric tuple/text correspondence,
   identity/key/lookup derivation and summary consistency under ordinary construction;
   do not rely on trusted factory use.
5. Rename the 006-a receipt's 40-hex `project_sha256_observed_locally` to an accurate
   Git/base-revision field with exact 40-hex validation in tests. Preserve its PARTIAL
   status and three-GET/pre-verifier/no-smoke facts. Do not call it current acquisition.
6. Add focused direct probes for requirements 1–5: no aliases/root exports; accepted
   completeness type identity; real provenance exact positive and each rebinding
   negative; header line 1 negative; summary schema/importer/output-hash tampering;
   record numeric/text/key mismatch; receipt field names/lengths/status. Retain all
   existing parsing/resource/Unicode/count/duplicate tests.
7. Only after corrected focused tests pass, perform one new GET of the exact 005 URL to
   a validated owned `/tmp/llm-slovenian-repair-006-b.*/*.part`. Use `curl --disable`,
   HTTPS, no redirects, no credentials/options override, fail-on-HTTP, connect <=10s,
   total <=900s and `--max-filesize 115865656`. This is the only 006-b source request.
8. Before any ZIP/member access, run accepted `verify_source_artifact.py` and require
   exact size/MD5/SHA/member limits. Then stream only 14 preamble lines, exact header
   and at most 32 complete data rows from the selected member into the importer twice
   with real-bound provenance: source/query completeness COMPLETE, import PARTIAL.
   Capture only record count and input/output hashes; never print/write row/header values.
   Both results/hashes must match and contain 1–32 records. Any parser incompatibility
   stops the round without weakening schema.
9. Create `gigafida-2.0-words-006-b.json` with source/license/inventory/artifact/header
   identities, verified size/MD5/SHA/member totals, exactly one 006-b GET, cumulative
   observed objective GET count four, 006-a exact-one false, smoke PASSED, sample count,
   matching two-run input/output hashes, no content, archive/temp absent, source data
   retained false and redistribution false. Record actual UTC time. Validate receipt
   schema/finite values in focused tests.
10. Close streams and delete the exact owned temp tree; verify no matching 006-b tree
    remains before commit. No external bytes/path or source content in git diff/log/report.
11. Preserve locked dependencies, 001 root import/wheel behavior, 003/004 evidence,
    005 canonical inventory, 006-a history and synthetic fixture origin. Run focused/
    broad tests, Ruff/mypy, OAP, native baseline, transcript/governance/protected checks
    and both required CI checks. Force-stage exact `006-b\n`.
12. The matching report must use a meaningful **string** for `criteria`, distinguish
    original product/006-a publication/reconciliation/006-b implementation SHAs, report
    each fetch/verification/smoke/cleanup fact and preserve historical violations. It is
    sole final SELF commit. No future CI or retroactive 006-a acceptance claim.

## Acceptance criteria

1. All provenance/header/summary/record/receipt mutation probes reject; exactly one
   submodule entry point remains and root import stays lazy.
2. Synthetic fixture imports deterministically with accepted shared completeness,
   ambiguity/Unicode/count/resource semantics preserved.
3. Exactly one new 006-b GET verifies to accepted size/MD5/SHA, and 1–32 real rows import
   twice with identical input/output hashes under PARTIAL import evidence; no content is
   logged/retained and temp cleanup passes.
4. New receipt truthfully records both current success and cumulative four-GET incident;
   006-a stays BLOCKED and its receipts/reports/history remain auditable.
5. Full product/OAP/native/protected/final-head checks pass; no archive/sample/package/
   dependency/live/release/deploy change; PR #7 stays open/unmerged during coding.

## Verification

Use a fresh owned environment and report:

```text
uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q
uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py tests/contract/test_objective_005.py -q
uv run --frozen --python 3.12 pytest tests/contract -q
uv run --frozen --python 3.12 pytest -q
uv run --frozen --python 3.12 ruff check src scripts tests
uv run --frozen --python 3.12 mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-b
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-b
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Separately record the one exact real acquisition/verify/twice-smoke/cleanup command with
only hashes/counts. Do not rerun to turn a failure green; diagnose before any new request,
which would require another explicit suffix/authority.

## Local setup and constraints

One exact 006-b GET is authorized only after focused code passes. Owned `/tmp`, accepted
verifier, exact caps and no redirect/config/credential. Normal environment proxy may be
used without reconfiguration. All CI stays offline. Preserve ignored `.venv`/caches.
No source/header/row values in command output, reports or logs; only finite metadata.
No protected model/GPU/service/gateway/neighbor/GitHub setting work.

## Documentation

Update docs/status to current exact API, provenance modes, receipt/current smoke and
limits while preserving 006-a incident. Do not imply full import/index, redistribution,
linguistic benefit, live compatibility, milestone, release or deployment.

## Git and report publication

Stay on existing branch/PR #7. Commit/push non-report correction and exact order/active/
receipts, require implementation-head CI, record literal SHA, then publish only
`oap/reports/006-b-bind-unigram-provenance-and-complete-smoke.md` as SELF with that
implementation parent. Push, remotely verify, send exact `OK`, exit. No merge.

## Decision classification

D0. The correction is bounded/reversible and one public licensed artifact fetch is
fixed by exact host/bytes/integrity/retention. Historical failure remains; no rights,
release, live or deployment judgment is made. No CRITICAL condition is met.

## Deferred human adjudication
- Decision: NONE

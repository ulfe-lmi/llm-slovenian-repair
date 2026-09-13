# Work order 006-a — Unigram/lexicon importer

Status: FINAL

```oap-metadata
{
  "id": "006-a",
  "title": "Unigram/lexicon importer",
  "objective": "006",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/006-unigram-lexicon-importer",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": ["003", "004", "005"],
  "local_work": "Clean local main equals remote main ee2d1b479719009ff1d07829478f241e3f395f7c; preserve ignored environments/caches and private strategic records.",
  "prior_review": "Objective 005 PR #6 merged after corrective exact-source binding and final-head review as ee2d1b479719009ff1d07829478f241e3f395f7c; no real artifact was retained and no PR remains open.",
  "provenance": [
    {"kind": "H", "reference": "PLAN.md §§6.1–6.3 and roadmap 006 select Gigafida unigram/lemma evidence and require reproducible sparse import with declared normalization/completeness."},
    {"kind": "A", "reference": "ARCHITECTURE.md §§8.1–8.2 require query-scoped evidence, explicit denominator/source metadata, checksum/rights provenance and no inferred zero or normalization compatibility."},
    {"kind": "E", "reference": "Accepted source-inventory-v1 binds gigafida-2.0-words to the public CC BY-SA 4.0 archive GF2.0-words-all.zip, exact 115865656 bytes and publisher MD5 b20a959f9c113aeb6504f0d753d36d10; project SHA/schema remain unobserved."},
    {"kind": "I", "reference": "Strategic acquisition review selected one direct no-redirect temporary fetch and bounded in-memory schema/sample qualification; no committed external bytes or redistribution is needed."}
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

006-a is the first round of numeric objective 006, DEMONSTRATOR, on one new branch/PR
from exact accepted main. If interrupted after branch or PR creation, recover that
same object and ID; never create a duplicate.

## Provenance

- H: PLAN selects Gigafida word/lemma lists for demonstrator evidence and requires
  sparse reproducible indexes rather than a guessed lexicon or dense matrix.
- A: Counts remain tied to source/release/scope/normalization/completeness. Original
  text is never normalized by an importer and exact zero requires complete query scope.
- E: Objective 005 proves publisher identity/size/MD5/license metadata and an offline
  ZIP-verification boundary, but not the actual archive SHA, TSV header or importer.
- I: A single temporary verified fetch is the smallest experiment that separates
  format compatibility from guessed code; external rows need not be committed/logged.

## Current verified state

Remote/local clean `main` equal merge commit
`ee2d1b479719009ff1d07829478f241e3f395f7c`; no open PR. Transcript through 005-b,
governance and exact active bytes verify. The accepted inventory contains three
downloadable publisher-labelled sources but all remain `NOT_ACQUIRED`; Gigafida 2.2
raw/query access remains `UNKNOWN_UNVERIFIED`.

CRITICAL is empty. Branch protection/rulesets remain disabled. Root source/wheel import
is dependency-lazy; the 004 synthetic fixture remains exact. Live Qwen, customer data,
milestone, external release and deployment gates remain closed.

## Governance

Apply compact coding law, LR-008, SECURITY/TESTING and accepted contracts. Preserve
PLAN, architecture, CRITICAL, role law, source lock, compact projections and transcript.
Treat downloaded ZIP/TSV as untrusted data: do not execute content/paths or print rows.
The explicit bounded acquisition below is development-only D0; it grants no data
redistribution, live-model, release or deployment authority. Decision NONE.

## Goal and dependencies

Implement a strict bounded Gigafida 2.0 unigram/form/lemma TSV import seam against its
actual observed schema, with deterministic project-authored synthetic fixtures and one
temporary permitted compatibility sample. Preserve source bytes, normalization and
frequency evidence explicitly; no detector/index/runtime lookup yet.

Objectives 003–005 provide evidence models, manifests and canonical source identity.

## Scope

1. Qualify exactly one accepted Gigafida 2.0 words artifact in owned temporary storage;
   record only non-content acquisition/schema evidence and delete the artifact.
2. Add one bounded unigram/lexicon importer module and strict immutable result/
   provenance types, without adding dependencies or import-time I/O.
3. Add only project-authored synthetic TSV fixtures/tests matching the observed header.
4. Run one bounded non-logging compatibility smoke from the verified real archive.
5. Update direct docs/status/package payload assertions and 006-a protocol files.

## Non-goals

No committed real source row/archive, full import/index build, database, runtime lookup,
detector/scoring/acceptance, n-gram parsing, Sloleks/2.2/collocation/CLASSLA access,
automatic downloader, background/network-on-import, source text rewriting, dependency,
service/GPU/Qwen/gateway/GitHub setting, live repair test, merge, release or deployment.

## Bounded source qualification

This paragraph is explicit separate acquisition authority for coding in this round only.
Fetch exactly:

`https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1273/GF2.0-words-all.zip?sequence=4&isAllowed=y`

to an owned `mktemp -d` path ending `.part`, using curl with configuration disabled,
no redirect, HTTPS, fail-on-HTTP, connect timeout at most 10 seconds, total timeout at
most 900 seconds and `--max-filesize 115865656`. Do not use credentials/proxy overrides.
The final body must be exactly 115865656 bytes and publisher MD5
`b20a959f9c113aeb6504f0d753d36d10`; run the accepted offline verifier before any ZIP
inspection and compute SHA-256. If any fact disagrees, stop acquisition/implementation
and publish truthful BLOCKED evidence rather than changing the expected identity.

After verification, inspect ZIP central metadata and stream only the header plus at
most 32 complete data rows from the member intended for all lower-case forms with
lemmas, parts of speech and taxonomy. Do not extract files, print/log row content or
retain row bytes. Record a versioned receipt containing source ID, item/artifact URLs,
publisher license label/URI, expected/observed size and MD5, computed SHA-256, selected
member name, exact ordered header names/header-line SHA-256, text encoding/newline/
delimiter observations, sampled row count, bounded importer-output hash, observation
time and `redistribution_ready=false`. Receipt contains no sample values.

Run the real sample through the importer twice in memory and require identical bounded
metadata/output hashes. Then close streams and remove the owned archive/temp tree;
verify absence. A failure to remove is a failure. Do not commit before this evidence.

## Files and boundaries

Expected paths: `src/llm_slovenian_repair/unigram_importer.py`, a versioned acquisition
receipt under `resources/source-acquisitions/`, project-authored synthetic fixtures
under `tests/fixtures/`, `tests/contract/test_objective_006.py`, direct README/status/
development/data-source docs and exact package/generated inventories, plus 006-a order/
active/report. Do not modify objective-005 inventory facts to pretend bytes are bundled.

The actual entry point parses an explicit binary/text stream or caller-owned verified
ZIP/member plus explicit provenance/limits. Network acquisition is setup outside that
entry point. Tests exercise real parsing/serialization with synthetic bytes; fakes may
block networking but do not replace the parser/file boundary.

## Requirements

1. Observe the actual selected TSV header before fixing the schema. Bind importer
   version 1 to that exact ordered header/member/delimiter/encoding/newline contract in
   code, receipt and tests. Do not infer column positions/names/types from historical
   research. If header/encoding is ambiguous or incompatible, stop rather than guess.
2. Use immutable extra-forbid strict types. Every output record retains exact source
   form/lemma/POS or other selected identity fields, absolute count as nonnegative int,
   published relative/percentage fields in lossless decimal text/`Decimal` as applicable,
   source/release/member/row identity and evidence scope. Do not use binary float or
   silently discard columns needed to interpret count/taxonomy. Finite schema versions.
3. Preserve source text bytes/decoded Unicode as the authoritative value. If a derived
   lookup form uses NFC/case folding, expose both exact source and derived value plus the
   exact named transform; never rewrite original customer text or pretend the source
   supplied another normalization. Reject invalid UTF-8, NUL/control, surrogate,
   overlong fields/lines and malformed tab structure.
4. Define source/query completeness independently from sample/import completeness.
   Published per-row counts may be exact within declared Gigafida 2.0 list scope, but a
   32-row smoke/prefix is not a complete vocabulary or denominator. Permit zero only
   when explicit metadata marks that exact query scope complete; reject zero in partial/
   unknown input and reject negative, signed, decimal, exponent, bool or overflow counts.
5. Preserve morphology ambiguity: the same form may retain multiple distinct lemma/POS
   analyses in stable source order. Define a stable composite record key. Reject exact
   duplicate keys and conflicting repeats; do not sum, choose a favorite lemma or infer
   that missing analyses/counts are zero.
6. Bound maximum input bytes, rows, line bytes, field count and field bytes with positive
   finite strict limits. Parse incrementally, not `read()`/`readlines()` of full input.
   Detect truncated final rows/newlines according to the observed source contract.
   Return finite reason labels without echoing row/token contents or arbitrary paths.
7. Determinism: importing the same exact bytes/config twice yields equal immutable
   records in source order and an identical canonical output SHA-256/manifest summary.
   Bind source inventory revision/hash, acquisition SHA, member/header hash, importer
   version, limits, normalization, record count and input/output hash in the summary.
8. Committed fixtures are clearly project-authored synthetic and licensed with project
   code; include exact positive, justified complete-scope zero, ambiguous form analyses
   and Unicode normalization distinction. Do not copy any real row or count. Tests cover
   malformed count variants, partial zero, invalid UTF-8/control/surrogate, normalization
   mismatch, duplicate/conflicting key, wrong header/columns, truncated/missing newline,
   oversized bytes/line/field/rows and deterministic repeated import.
9. The real compatibility smoke is local evidence only: at most 32 rows, no contents in
   output/log/report, no complete-import/coverage/quality claim. Tests/CI remain offline.
   The receipt may record hashes/schema/counts only and must state source data not retained,
   project SHA observed locally, importer compatibility scope, and redistribution false.
10. Preserve all 001–005 tests, lock/dependencies, root source/built-wheel laziness,
    synthetic 004 bytes/hash and 005 canonical inventory/digests. If adding a package
    module, update exact wheel payload expectation while proving no resource/acquisition/
    real fixture enters sdist/wheel. Run complete checks and required final-head CI.
11. Force-stage exact `006-a\n`, preserve full history and publish matching SELF report
    as sole final commit. Report fetch/verification/smoke/cleanup each distinctly and
    treat anything not actually observed as NOT RUN/UNPROVEN.

## Acceptance criteria

1. Exact accepted archive size/MD5 verify; computed SHA-256 and header/schema-only
   receipt commit; at most 32 unlogged real rows import twice identically; temp archive
   is absent afterward. If not, the round reports BLOCKED and makes no format claim.
2. Project-authored synthetic import succeeds twice with identical ordered output/hash,
   preserving exact versus derived Unicode and multiple analyses for one form.
3. All malformed/count/zero/duplicate/header/truncation/Unicode/resource negative paths
   fail with finite non-content errors at the real parser boundary.
4. Output summary binds accepted source/acquisition/header/importer/limits/hashes and
   never upgrades a prefix/sample into complete source evidence or denominator.
5. No external row/archive is committed/packaged/logged; no download occurs in CI. Full
   001–005/product/OAP/native/transcript/governance/protected checks and both required
   final-head checks pass; PR stays open/unmerged during coding.

## Verification

Use a fresh owned environment. Record exact commands/results without source rows:

```text
uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q
uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py tests/contract/test_objective_005.py -q
uv run --frozen --python 3.12 pytest tests/contract -q
uv run --frozen --python 3.12 pytest -q
uv run --frozen --python 3.12 ruff check src scripts tests
uv run --frozen --python 3.12 mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-a
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-a
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Additionally run the accepted 005 verifier on the temporary archive before the bounded
real smoke; record SHA/header/importer hashes and verify cleanup. Do not print the TSV
header/rows in OAP logs; the receipt is the only schema metadata artifact.

## Local setup and constraints

One exact public derived archive GET is permitted only as Bounded source qualification.
Use `curl --disable`, no redirects, exact direct URL/size/MD5, owned `mktemp -d`, finite
timeouts and no credentials. A normal HTTP proxy already imposed by the environment may
be used only if unavoidable and must not be reconfigured or logged; no VPN/firewall/
gateway changes. Delete artifact/temp before commit and prove absence.

All tests/CI use committed synthetic bytes only. Preserve ignored repo `.venv`/caches.
No raw customer/model text, source rows, prompts/responses, credentials or private
strategic content in Git/output/report. No protected Qwen/GPU/service/port/neighbor work.

## Documentation

Document exact implemented schema, source/derived normalization, ambiguity, evidence
scope, receipt and current limitations. Attribute/link the official source and CC label,
but do not call project code/data release-compatible or the importer a detector/index.

## Git and report publication

Create/adopt only branch `oap/006-unigram-lexicon-importer` and one PR. Commit/push all
non-report work/order/active, require implementation-head CI, record literal SHA, then
publish only `oap/reports/006-a-unigram-lexicon-importer.md` as SELF with implementation
sole parent. Push, verify remote head/content/path/parent, send exact `OK`, exit. No merge.

## Decision classification

D0. The one artifact is explicitly publisher-labelled CC BY-SA and is used temporarily
for local format qualification without redistribution. Scope, bytes, host, integrity,
retention and outputs are fixed/reversible; all unresolved release/legal/quality/live
boundaries remain fail-closed. No CRITICAL admission condition is met.

## Deferred human adjudication
- Decision: NONE

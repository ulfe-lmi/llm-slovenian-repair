# Development baseline

This objective establishes an installable Python 3.12 development skeleton. It
does not implement repair contracts, model calls, corpus access, linguistic
benefit, serving compatibility, ICA, milestone acceptance, release, or
deployment authority.

## Supported project

- Python: `>=3.12,<3.13`; the checked-in `.python-version` selects `3.12`.
- uv: `>=0.12.5,<0.13`; the implementation environment was created with uv
  0.12.5.
- Runtime: `pydantic>=2.13.5,<3` (MIT) and `httpx>=0.28.1,<1` (BSD-3-Clause).
- Development group: `pytest>=9.1.1,<10`, `ruff>=0.16.6,<0.17`, and
  `mypy>=2.3.1,<3`.
- The published `morphology` extra is intentionally empty. A later objective
  must select, qualify, and document any analyzer and its data rights.

Dependency resolution may use the default public registry. The committed
`uv.lock` records exact artifacts and hashes. Importing
`llm_slovenian_repair` performs no download, model/corpus discovery, or network
operation and eagerly imports no runtime dependency.

## Reproducible commands

From the repository root, using Python 3.12 and a native temporary parent:

```text
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp
```

The driver is the supported selected-workspace path. It creates one unique
`TemporaryDirectory` under the explicit native parent, refuses a parent inside
the repository, and uses that owned root for the project environment, uv cache,
Ruff/mypy caches, build output, and the second wheel environment. This matters
because the owner-selected workspace is a sync mount where repository `.venv`
creation and filesystem lookup are unsupported. The driver does not use a fixed
shared venv or remove caller paths.

The first frozen sync may use the configured package registry to populate the
isolated cache. The driver then creates a fresh second Python 3.12 environment
and runs uv's lock-driven `UV_OFFLINE=1 uv sync --frozen --no-dev
--no-install-project` against that same cache. This installs the complete exact
runtime closure without project code or private uv cache-layout assumptions. The
built project wheel is then installed normally with `uv pip install --offline`
and its declared dependencies; the lockfile remains the only dependency source.
The driver imports the package, `pydantic`, `pydantic-core`, and `httpx` from a
directory outside the repository and checks every locked runtime dependency's
version and normalized metadata. Every subprocess has a finite timeout. Failed
commands retain only a bounded, control-free, path-redacted stdout/stderr tail;
successful records contain no command output. The owned environment, cache, and
build artifacts are cleaned by context-managed temporary-directory cleanup.

The earlier `fac9f68` Application-baseline failure remains causally unresolved;
its subprocess output was suppressed before bounded diagnostics were added.
Future failures will include enough sanitized tail output to identify the
earliest failing boundary without exposing environment values or private text.

The driver also runs the focused contract tests, full pytest, Ruff, mypy,
separate OAP unittest discovery, and both sdist/wheel builds in the required
order. The package contains no production entry point, service, live-Qwen test,
corpus, GPU dependency, downloader, or release step.

## Source manifest fixture

`llm_slovenian_repair.source_manifest` exposes frozen `SourceManifest` and
`SyntheticCountRecord` models and the canonical `verify_manifest_payload`
boundary. The manifest accepts only exact `UTF-8` encoding and `jsonl`/`json`
record formats, matched to `application/jsonl`/`application/json`; alternate
field names and public aliases are rejected. The loader accepts a
caller-supplied fixture root, rejects unsafe paths and symlinks, applies finite
manifest/payload/record limits, verifies exact byte size and SHA-256, and parses
UTF-8 JSON or JSONL records without writing or using the network.

`tests/fixtures/corpus/synthetic-manifest.json` and
`tests/fixtures/corpus/synthetic-counts.jsonl` are project-authored synthetic
fixtures for `local synthetic tests only`. Their terms reference the repository
`LICENSE`, attribution states that there is no external corpus, and
`importer_schema_version` is `NOT_APPLICABLE_SYNTHETIC_FIXTURE`; no importer or
external permission is asserted. Their records exercise exact positive,
justified exact zero, censored unknown-denominator, and unavailable evidence
states. The censored record says values at/below synthetic cutoff 4 are
represented only by `[0,4]`. They are schema/checksum tests, not Slovenian
language-quality or corpus evidence. Real source names, releases, formats,
acquisition methods, rights, terms, and access remain unverified. The test-only
fixture path is not included in the runtime wheel.

## Bounded unigram importer

Objective 006 adds `llm_slovenian_repair.unigram_importer`. It parses a
caller-supplied UTF-8, CRLF, all-fields-quoted 28-field TSV stream incrementally
against the observed 28-column Gigafida 2.0 lower-case form/lemma/POS header. The
header ends immediately after its 28th quoted field, while each data record has
either 28 quoted fields ending immediately before CRLF or those same fields plus
one empty terminal tab before CRLF (`data_record_terminator=`
`OPTIONAL_SINGLE_EMPTY_TAB_BEFORE_CRLF`); the optional tab is a source-record
terminator, not a 29th semantic field. Additional tabs, whitespace, or semantic
fields are rejected. The
module does not open paths, download data, inspect ZIPs, or build a lookup index.
`UnigramProvenance` binds either the exact real source/archive identity or an
explicit project-synthetic fixture identity and uses shared
`EvidenceCompleteness`. `UnigramRecord` retains exact source fields, numeric
text/views, morphology identity, and an NFC/casefold-derived lookup view.
Frozen extra-forbid models revalidate summary constants, numeric/text/key
correspondence, and canonical output hashes. The only public parser entry point
is `import_unigrams`; the package root remains lazy.

`tests/contract/test_objective_006.py` materializes CRLF bytes from the
project-authored synthetic fixture and exercises the real parser boundary,
including the distinct header and the two accepted data-row contracts. The
fixture includes ambiguous analyses, complete-scope zero, and a decomposed
Unicode form; no external row/count is copied. The 006-a recovery receipt
preserves three earlier GETs and its blocked history. The 006-b receipt records
one verified GET and cleanup, but its real importer smoke is blocked at the first
data row by the source-specific terminal tab. The 006-c receipt records one new
verified GET and cleanup, but its bounded first-32-row structural sampler stopped
before importer execution; no real compatibility or vocabulary coverage is claimed.
Round 006-d adds `scripts/diagnose_unigram_rows.py`, a standard-library
classifier that reports only bounded row-shape aggregates and finite parser
failure labels. Synthetic tests cover terminal delimiters, field counts,
quoting, embedded tabs, newline/UTF-8 anomalies, limits, and content-free
serialization. Its single verifier-first fetch was blocked before 32 complete
member rows reached the classifier (`requested-row-incomplete`); the receipt
therefore stores null diagnosis aggregates, records no importer run, and makes
no format or compatibility claim. The temporary source tree was deleted.
Round 006-e adds the public `classify_stream` handoff around that classifier.
The CLI delegates to the same boundary, which reads one caller-owned binary
stream prefix exactly once before one classification. Synthetic tests include a
15-line preamble/header ZIP member, exact 32-row routing, double-skip failure,
header inclusion, and aggregate-count validation. Its single verifier-first
fetch completed the bounded diagnosis with 31 28-field rows and one empty
terminal 29th field; no importer compatibility or source retention is implied.
Round 006-f supersedes the 006-c mandatory-tab assumption with the narrower
evidence-fixed optional single empty terminal tab contract. Offline tests prove
both accepted shapes and reject wider extensions. Its one archive fetch passed
verification, but the bounded smoke harness failed before member access, so no
real importer compatibility evidence was obtained; the receipt records this
separately from full-source, linguistic, rights, release, or deployment claims.

Round 006-g adds `scripts/smoke_unigram_prefix.py`, a verifier-first bounded
compatibility probe. It accepts only the explicit canonical inventory, source ID,
and acquired artifact; opens the selected ZIP member once; captures exactly the
14-line preamble, 834-byte header, and 32-row prefix into a 4 MiB maximum
in-memory envelope; checks the content-free structural aggregate; and calls the
public importer twice on fresh streams with real source/query `COMPLETE` and
import `PARTIAL` provenance. Its output contains only finite verification facts,
aggregates, counts, and result hashes. It does not download, extract, retain
source data, claim full archive import or lookup readiness, or authorize rights,
acceptance, release, or deployment.
The ordered 006-g fetch reached canonical verifier success, but the committed
CLI stopped before member access because its checkout source path was unavailable
to the direct interpreter invocation. The helper now bootstraps that path and its
offline contract is green; the exact source tree was deleted, no retry occurred,
and the 006-g receipt leaves member, structural, and importer fields null. This
is a blocked real-smoke result, not a full-source or compatibility acceptance.
Round 006-h adds `--preflight`, which is mutually exclusive with `--artifact` and
requires only the canonical inventory and source ID. It validates the installed
runtime's exact header contract, real COMPLETE/COMPLETE/PARTIAL provenance,
`import_unigrams` entry point, and the bounded smoke limits, then emits only a
finite `READY` summary. The direct system-Python dependency failure from 006-g is
documented as an invocation prerequisite failure; it is not treated as evidence
that the importer or source format is incompatible.
The exact 006-h run passed this preflight in an owned isolated environment and
made one direct GET. Canonical verification, member access, the 32-row structural
aggregate, and the first importer admission completed; that importer invocation
then stopped at `import-invalid-count`. No retry or second GET was made, cleanup
was verified, and importer hashes/counts remain null. This is blocked bounded
compatibility evidence, not full-source or linguistic-quality evidence.

Round 006-i adds a `--diagnostic` mode to the verifier-first helper. It reuses
the artifact-free preflight contract, canonical verification, one selected-member
capture, and the exact 32-row structural aggregate, then classifies each of the
768 numeric cells in the eight absolute-count and sixteen published-decimal
columns. The classifier uses a documented fixed priority and a closed enum; it
does not emit numeric content, values, lengths, row hashes, or source-derived
labels. Current-parser compatibility is counted separately for counts and
decimals, and the first incompatible row/1-based column/semantic kind/category is
bounded. The importer is called once only to report an allowlisted exact
`reason:column` result. Synthetic tests cover every enum category, overlap
priority, all columns, conservation, deterministic serialization, structure-first
failure, mode exclusion, and no-content output.

Round 006-j extends the diagnostic after structural success with a closed
row-1-marker refinement and a content-free identity profile. It emits only fixed
marker categories, family distinctness/uniformity, same-column recurrence, identity
categories, equality partitions, NFC-casefold booleans, and bounded evidence
predicates; it never emits marker text, values, lengths, hashes, or record objects.
The observed row-1 profile has 24 distinct `ASCII_MIXED_OTHER` markers, no
same-column recurrence, and an identity-profile outlier. A counterfactual in-memory
envelope preserves the original preamble/header and rows 2–32, then calls the
unchanged importer once with `max_rows=31`; it reaches the safe
`invalid-decimal:6` boundary while the original envelope remains at
`invalid-count:5`. Row-role and unit meanings remain unresolved pending strategic
selection; no importer conversion or production behavior changed.

Round 006-k adds two offline process boundaries. The report-history helper scans
actual Git path events and hard-binds the two known historical report incidents;
temporary Git-history tests cover modification, deletion/recreation, parent drift,
and a new corrective suffix. The source-cache helper exposes plan, validate,
promote, repair, and lifecycle-gated cleanup operations. It does not download,
accept arbitrary paths or URLs, or emit private cache paths/content. The cache
promotes only after `scripts/verify_source_artifact.py` accepts the exact archive
identity and every consumer revalidates it.

Round 006-l replaces the sync-filesystem hardlink/fallback branch with one
lock-protected same-directory `os.replace`, post-rename canonical verification,
exclusive metadata, and fixed-artifact cleanup on expected failures. Focused tests
cover corrupt digests/metadata, duplicate or stale metadata, symlink/hardlink/
nonregular/wrong-owner seams, overwrite and lifecycle gates, rename/verification/
metadata failures, and the requested real Git-history negatives. The retained cache
was consumed twice by the content-free 006-j diagnostic with identical safe results;
the immutable receipt records cumulative fourteen GETs and the zero-retry,
zero-redistribution boundary.

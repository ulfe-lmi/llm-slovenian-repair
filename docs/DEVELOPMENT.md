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
exactly one terminal tab before CRLF (`data_record_terminator=TAB_BEFORE_CRLF`);
that tab is a source-record terminator, not a 29th semantic field. The
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
including the distinct header and exact one-tab data-row contracts. The
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

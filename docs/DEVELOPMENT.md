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
`SyntheticCountRecord` models and the explicit `verify_manifest_payload` loader.
The loader accepts a caller-supplied fixture root, rejects unsafe paths and
symlinks, applies finite manifest/payload/record limits, verifies exact byte size
and SHA-256, and parses UTF-8 JSON or JSONL records without writing or using the
network. `load_verified_corpus` is an alias for the same boundary.

`tests/fixtures/corpus/synthetic-manifest.json` and
`tests/fixtures/corpus/synthetic-counts.jsonl` are project-authored synthetic
fixtures. Their records exercise exact positive, justified exact zero,
threshold-censored unknown-denominator, and unavailable evidence states. They
are schema/checksum tests, not Slovenian language-quality or corpus evidence.
Real source names, releases, formats, acquisition methods, rights, terms, and
access remain unverified; repository Apache licensing does not resolve external
source rights. The test-only fixture path is not included in the runtime wheel.

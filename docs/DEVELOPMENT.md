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
isolated cache. The driver then materializes the locked runtime wheel entries
from that cache into an owned wheelhouse. The second fresh Python 3.12
environment switches uv to `UV_OFFLINE=1`/`--offline`, disables indexes, and
installs the built wheel with its full declared runtime dependency closure from
that wheelhouse; it deliberately does not use `--no-deps`. It then imports the
package, `pydantic`, `pydantic-core`, and `httpx` from a directory outside the
repository and checks their locked versions and package metadata. Missing
cached dependencies fail the proof. Every subprocess has a finite timeout, and
the owned environment, cache, wheelhouse, and build artifacts are cleaned by
context-managed temporary-directory cleanup.

The driver also runs the focused contract tests, full pytest, Ruff, mypy,
separate OAP unittest discovery, and both sdist/wheel builds in the required
order. The package contains no production entry point, service, live-Qwen test,
corpus, GPU dependency, downloader, or release step.

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

From the repository root, using Python 3.12:

```text
uv lock --check
uv sync --frozen --all-groups --all-extras --python 3.12
uv run --frozen pytest tests/contract/test_objective_001.py -q
uv run --frozen pytest -q
uv run --frozen ruff check src tests
uv run --frozen mypy src tests/contract
uv build --no-sources
python3 -B -m unittest discover -s oap/tests -v
```

The application workflow also builds both sdist and wheel and performs an
offline wheel installation/import proof. To reproduce that proof locally after
the ordinary frozen sync has populated uv's cache:

```text
uv build --no-sources
uv venv --python 3.12 /tmp/llm-slovenian-repair-wheel-venv
uv pip install --python /tmp/llm-slovenian-repair-wheel-venv/bin/python --offline --no-index --no-deps dist/llm_slovenian_repair-0.0.0-py3-none-any.whl
/tmp/llm-slovenian-repair-wheel-venv/bin/python -B -c 'import llm_slovenian_repair; assert llm_slovenian_repair.__version__ == "0.0.0"'
rm -rf /tmp/llm-slovenian-repair-wheel-venv dist
```

The temporary directory and build output above are disposable owned fixtures;
do not remove unrelated files. The package contains no production entry point,
service, live-Qwen test, corpus, GPU dependency, downloader, or release step.

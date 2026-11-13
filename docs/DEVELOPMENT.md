# Development guide

How to set up and verify this repository. Two areas have distinct
toolchains. The **runnable proxy** (`concept-verification/`) is pure Python
3.12 standard library plus the pinned Pandoc and needs no third-party Python
package (see [INSTALL.md](../INSTALL.md)). The **historical packaged
scaffold** (`src/llm_slovenian_repair`, not the runtime entry point) declares
runtime dependencies `pydantic>=2.13.5,<3` and `httpx>=0.28.1,<1`; its dev
group is `pytest`, `ruff` and `mypy`; the `morphology` extra is intentionally
empty until an analyzer and its data rights are qualified. For that scaffold,
the supported toolchain is Python 3.12 (`>=3.12,<3.13`; `.python-version`
selects 3.12) and uv (`>=0.12.5,<0.13`) — developer tooling and the package
baseline, not a prerequisite to launch the standalone proxy. The committed
`uv.lock` is the only dependency source; importing `llm_slovenian_repair`
performs no download, discovery or network operation.

## Machine-local environment

Development uses a machine-local environment derived from `$HOME`. The
canonical definition is the sourceable helper `scripts/project_env.sh`; it
derives every persistent path from `$HOME` and the checked-in project name and
hard-codes no username, hostname or absolute path. The layout dates from the
sync-mount host, where a persistent repository `.venv` and tool caches were
unsuitable (round 007-k; dated rationale); on the current native host the
workspace is a native ext4 checkout and the same machine-local layout remains
the supported one, with the machine-local Python 3.12 environment as the
ordered verification interpreter (`python -B` form, bytecode off).

Setup paths (all derived by the helper):

- **uv/virtual environment** — `$HOME/envs/llm-slovenian-repair`
- **Python bytecode cache (`PYTHONPYCACHEPREFIX`)** —
  `$HOME/.cache/python-pycache/llm-slovenian-repair`
- **Ruff cache** — `$HOME/.cache/ruff/llm-slovenian-repair`
- **mypy cache** — `$HOME/.cache/mypy/llm-slovenian-repair`
- **pytest cache** — `$HOME/.cache/pytest/llm-slovenian-repair`
- **Project temporary work (`TMPDIR`)** — `$HOME/.cache/tmp/llm-slovenian-repair`
- **uv package cache** — uv's default machine-local cache

First use on each machine:

1. Install compatible uv and Python 3.12 if absent.
2. Clone, mount or open the shared project.
3. In the shell you develop in: `source scripts/project_env.sh` (once per
   shell; idempotent, keeps the environment `bin` exactly once at the front
   of `PATH`).
4. Run `scripts/bootstrap_dev_env.sh` to validate repository identity, the uv
   constraint and Python 3.12, then perform the locked `uv sync --frozen`
   into the machine-local target.
5. Use ordinary `python`, `uv run`, `pytest`, `ruff` and `mypy`.

The helper must be **sourced** (or used through direnv); a plain shell cannot
receive exports from an executed child, and executing it fails with a concise
instruction. It creates only the exact project-specific parent and cache
directories, never the uv environment itself, and preserves existing nonempty
user values for the cache/`TMPDIR` variables — it does not re-qualify an
inherited value, so a shell whose `TMPDIR` is `/tmp` or beneath it must pass
an explicit supported parent to the Verification commands below. The tracked
root `.envrc` only
sources the helper; direnv is optional and not installed or required by the
tests.

Dependency updates travel only through the committed `pyproject.toml` and
`uv.lock`; each machine reruns the locked sync into its own `$HOME/envs`
path. Environments are never copied or moved between machines. Any legacy
repository-local `.venv` or transient caches on a host are left as inactive
data; this workflow neither uses nor recreates them and does not assert their
current existence. Since round 012-b every
owned driver subprocess runs in its own POSIX session with nonblocking pipe
reads, bounded group-scoped cleanup and truthful bounded-cleanup failures.

 ## Runnable proxy prerequisites

The isolated `concept-verification/` proxy additionally requires the pinned
Pandoc **3.7.0.2** at startup (`concept-verification/pandoc-dependency.json`;
exact release-archive byte count and locally computed SHA-256). The binary
resolves from `CONCEPT_PANDOC` then PATH;
`concept-verification/install_pandoc.sh` installs the pinned official Linux
amd64 archive into an explicitly passed owned prefix only (no sudo, no system
replacement, no runtime downloads). The canonical operator procedure — data
acquisition, checksums, index location, both auth hops, foreground launch —
is [INSTALL.md](../INSTALL.md).

## Verification

- Development baseline driver (disposable native temporary environment,
  frozen offline dependency policy, contract tests, full pytest, Ruff, mypy,
  OAP unittest discovery, sdist/wheel builds). Run in a shell where
  `scripts/project_env.sh` has been sourced, so `--temp-parent` is the
  supported persistent project scratch root (explicitly not `/tmp`, which the
  included forward-recovery suite rejects):

  ```bash
  python3.12 scripts/verify_development_baseline.py --temp-parent "$TMPDIR"
  ```

  In a bare shell without that setup, pass an explicit existing persistent
  parent outside the repository instead — do not weaken the scratch guard.

- Governance and proxy suites: see [TESTING.md](../TESTING.md), which states
  the same scratch prerequisite for the standalone commands.

The driver refuses a repository-local parent, runs the first frozen sync with
the configured registry and a later fully offline second environment against
that same cache, installs the built project wheel with `uv pip install
--offline`, and checks every locked runtime dependency's version and metadata.
Every subprocess has a finite timeout; failed commands retain only a bounded,
control-free, path-redacted output tail. The package contains no production
entry point, service, live-Qwen test, corpus, GPU dependency, downloader or
release step.

## Frozen whitespace contract (current state)

The repository whitespace checker accepts **exactly six pinned historical
incidents** (evolved closed-four → closed-five → closed-six by orders
027-b, 031-b and 034-b) at the two authorized bases, and fails closed on any
additional violation, a changed or trimmed issued order, path/line/message
drift, a missing prescribed recovery lineage, an unknown base or an invalid
revision. There is no configuration, flag or environment path to admit future
incidents; strategy qualifies a prospective order's whitespace before its
immutable publication. The exact pins and the historical incident records
live in the frozen orders and the checker, not in this guide.

## Historical seams (abridged)

The early engineering rounds established, on top of the bootstrap:

- **Objective 001** — the installable Python 3.12 skeleton and reproducible
  offline dependency policy described above.
- **Objective 004** — the frozen `SourceManifest`/`SyntheticCountRecord`
  models and the canonical `verify_manifest_payload` boundary; the
  checked-in `tests/fixtures/corpus/` payloads are project-authored synthetic
  fixtures for `local synthetic tests only` (no external corpus, no importer
  asserted; censored values at/below synthetic cutoff 4 are represented only
  by `[0,4]`).
- **Objective 006** — the bounded `unigram_importer` seam (28-field CRLF TSV,
  optional single empty terminal tab before CRLF, exact real vs
  project-synthetic provenance) and its verifier-first compatibility probes;
  see [DATA-SOURCES.md](DATA-SOURCES.md) and the frozen round reports.
- **Round 007-k** — the machine-local environment layout above, adopted when
  the sync mount was found unsuitable for persistent local venvs.

The per-round detail, receipts and exact changed scopes are preserved in the
immutable [orders](../oap/orders/) and [reports](../oap/reports/)
(navigation: [HISTORY](HISTORY.md)); this page does not restate them.

# Testing and verification contract

How this repository is tested and how evidence is recorded. The runnable proxy
is implemented and tested with deterministic synthetic fixtures; live-model and
linguistic evidence are separate layers.

Prerequisites for the commands below:

- **Qualified Python 3.12** as `python3.12` (installation and pinned Pandoc
  3.7.0.2: [INSTALL.md](INSTALL.md); a bare machine `python3` is not
  established to be 3.12).
- **Development environment and scratch** per
  [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): the forward-recovery suite
  requires a persistent `TMPDIR` (not `/tmp` or beneath it) or a runner-owned
  `RUNNER_TEMP`; the guard is not weakened to make a default setup pass.
- Detailed evaluation rationale: [docs/EVALUATION.md](docs/EVALUATION.md).

TEST-01. **Offline suites.** Bootstrap and governance (standard-library
disposable Git/FIFO/CLI fixtures and fake CLI/GitHub boundaries):

    python3.12 -B -m unittest discover -s oap/tests -v

The runnable proxy (local synthetic fixtures: HTTP/SSE captures, pinned
Pandoc, read-only SQLite index, fake client; no GitHub boundary):

    python3.12 -B -m unittest discover -s concept-verification/tests -v

No real model, corpus, customer data or protected service is required for the
offline suites. Tests must exercise the real helper entry point/boundary and
assert specific failure reasons.

TEST-02. **Order-bound evidence.** Each order names its focused/broader test
commands, negative cases, tested SHA and real boundary. Never substitute a
mock of the boundary being claimed. Record PASS/FAIL/SKIPPED/NOT RUN/BLOCKED/
PENDING/MISSING as distinct states. Required skipped tests never pass. The
first reproducible failure determines the smallest discriminating diagnostic
experiment and its stop condition.

TEST-03. **Separated evidence layers.** Keep these evidence layers separate:
fake-client correctness, installed CLI discovery, actual model compatibility,
human-labelled linguistic benefit, independent closure audit (ICA) and
deployment authorization. Live tests require explicit opt-in and verified
endpoints/budgets/data rights. Never weaken checks or call live Qwen to make
scaffold tests pass. Linguistic benefit remains unmeasured, and no separate
human evaluation dataset exists or is required.

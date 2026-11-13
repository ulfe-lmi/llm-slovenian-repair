# SLAIF Slovenian Repair — concept-verification proxy

**EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE**

This is one deliberately isolated research spike. It is not the production
application, a release, a deployment, a corpus redistribution, or a linguistic
quality claim. The proxy has demonstrated functional software/native
compatibility; linguistic quality is unmeasured, and no separate human
evaluation dataset is required by the current scope.

Installation is documented at the repository root, not here:

- [INSTALL.md](../INSTALL.md) — full installation: external CC BY-SA
  statistics downloads, checksums, derived SQLite index, pinned Pandoc, both
  authentication hops, foreground launch, stop/upgrade/recovery.
- [QUICKSTART.md](../QUICKSTART.md) — shortest complete path to a first
  synthetic Responses call.
- [ARCHITECTURE.md](../ARCHITECTURE.md) — current source of truth for
  components, lifecycle, contracts and failure semantics.
- [TESTING.md](../TESTING.md) — test guide with qualified interpreter and
  fixture prerequisites.
- [docs/LIVE-TEST-ENVIRONMENT.md](../docs/LIVE-TEST-ENVIRONMENT.md) — live
  qualification guide and observed native evidence.
- [docs/HISTORY.md](../docs/HISTORY.md) — abridged history with direct
  evidence links.

The proxy is one synchronous parent process with bounded owned child
processes, standard-library Python 3.12, bounded finite HTTP calls, and a
loopback-only endpoint at `127.0.0.1:18024`.

The corpus loader consumes only explicit external archive paths. It verifies
regular non-symlink owner/link-count-one files, exact size/MD5/SHA-256,
selected member names, 14-line preambles, header/marker hashes, CRLF, UTF-8,
widths, and row limits before inserting a derived SQLite index. Word absence
is `UNAVAILABLE`; missing n-grams are `CENSORED` with an unknown denominator.
The archives and index are external local data (a storage choice, not a
confidentiality claim) and must never be staged, committed or packaged.

## Current behavior

The normal launcher now provides transparent HTTP forwarding, with configurable
`CONCEPT_HOST` and `CONCEPT_PORT`. Tools, multimodal input, other routes and upstream
errors pass through; eligible final Responses text can still be repaired when tools were
declared. Structured, stored and tool-call responses bypass repair unchanged.
See [proxy chaining](../docs/PROXY-CHAINING.md) for the current forwarding layer.
The narrow profile below describes the underlying strict repair implementation,
also available through `CONCEPT_PASSTHROUGH=0`.

The current runnable proxy is the loopback OpenAI-compatible Responses
endpoint. The summary below describes its operational boundaries;
[ARCHITECTURE.md](../ARCHITECTURE.md) holds the full component and failure
semantics.

- **Request profile.** Responses JSON and SSE; input is a plain string or a
  client-managed text-only message sequence. There is no server-side storage
  or chaining; next turns are client-managed and use the delivered answer.
- **Capture.** A completed answer is buffered in full before CPU analysis.
  Only natural assistant output text can change; reasoning, tools, function
  arguments, IDs, usage, event order and count are preserved. Without
  accepted edits the delivered text stays unchanged from the original even
  though defined logprobs removal can change the envelope; with repair, only
  approved original spans change.
- **Protection.** Mandatory pinned Pandoc 3.7.0.2 with exact original spans
  and the Pandoc original mapping. Protected material is never edited, and a
  missing or failing Pandoc binary rejects startup before the proxy binds.
- **Evidence.** Read-only derived SQLite index; lookups are finite and
  budgeted. Absence and censoring keep their distinct semantics (see above).
- **Review.** Without eligible suspicion there are zero review calls;
  otherwise at most one isolated occurrence-addressed batch of one
  non-streaming Qwen request containing up to four targets, with a
  typed completed envelope. Defined logprobs are removed unconditionally before any
  eligibility decision, and main-generation usage and review usage are
  accounted separately; neither is an inference bill for the edited text
  length.
- **Acceptance.** Strict lexical acceptance: an accepted replacement is 1–4
  lexical words with summed word-character length ≤ 80; each proposed
  replacement is bounded at 128 code points and 8 words, and multiword
  cases need fixed-anchor phrase evidence. A rejected proposal keeps its
  original; an ordinary interacting conflict group reverts only its own
  spans while independently supported edits survive.
- **Failure.** Any optional-stage technical failure (Pandoc, evidence,
  batch, transport, acceptance) delivers the completed original. A
  malformed or truncated transport is an error. A valid explicitly
  incomplete envelope passes through with its status and text preserved;
  defined logprobs are still removed.
- **Cancellation.** Request-scoped cancellation on client disconnect with
  the phase and cleanup guarantees in ARCHITECTURE section 14.

## Module navigation

The current modules live in this directory (paths relative to this file),
grouped by runtime concern:

- **Request entry and delivery**
  - [proxy.py](proxy.py) — loopback listener, worker wiring, request entry.
  - [request_lifecycle.py](request_lifecycle.py) — per-request state, cancellation hooks, completion.
  - [request_admission.py](request_admission.py) — bounded accepted-connection admission.
  - [capture_transport.py](capture_transport.py) — completed main-body capture, JSON and SSE, body budget.
  - [header_transport.py](header_transport.py) — independent elapsed response-header budget.
  - [client_transport.py](client_transport.py) and [delivery_transport.py](delivery_transport.py) — client intake and bounded final delivery.
- **Main-upstream generation**
  - [upstream_setup.py](upstream_setup.py) and [upstream_worker.py](upstream_worker.py) — bounded main-upstream setup and owned fetch.
- **Reviewer**
  - [review_transport.py](review_transport.py) and [review_worker.py](review_worker.py) — isolated non-streaming reviewer exchange.
  - [batch_review.py](batch_review.py) — occurrence-addressed proposal batches and caps.
  - [qwen_client.py](qwen_client.py) — reviewer HTTP client, typed completed envelope.
- **Protection and repair**
  - [pandoc_protection.py](pandoc_protection.py), [protected.py](protected.py) and [protection_residuals.py](protection_residuals.py) — Pandoc mapping, span protection, residual checks.
  - [repair.py](repair.py) — exact span splicing, right-to-left application.
  - [composed_validation.py](composed_validation.py) — composed-result validation and conflict groups.
- **Evidence, detection and acceptance**
  - [runtime_corpus.py](runtime_corpus.py) — read-only index access, UNAVAILABLE/CENSORED semantics.
  - [detector.py](detector.py) and [runtime_detection.py](runtime_detection.py) — CPU detection and target selection.
  - [evidence_budget.py](evidence_budget.py) — finite evidence lookup budget.
  - [runtime_acceptance.py](runtime_acceptance.py) — one runtime lexical-acceptance policy.
  - [analysis_policy.py](analysis_policy.py) — bounded analysis eligibility policy.
- **Envelope, configuration and corpus build**
  - [responses_contract.py](responses_contract.py) — request/response envelope and metadata contracts.
  - [config.py](config.py) — environment configuration and defaults.
  - [corpus.py](corpus.py) — external-archive verification and SQLite build (offline preparation, not a runtime path).

## Operator and developer references

- [STATUS.md](../STATUS.md) — current programme state and topology.
- [oap/COMPLETENESS.md](../oap/COMPLETENESS.md) — current completeness
  evidence and its axes.
- [docs/OAP-RUNBOOK.md](../docs/OAP-RUNBOOK.md) — OAP operational
  procedures for this workspace.
- [docs/DATA-SOURCES.md](../docs/DATA-SOURCES.md) — external statistics
  sources and acquisition provenance.
- [oap/reports/036-a-current-functional-proxy-readiness-audit.md](../oap/reports/036-a-current-functional-proxy-readiness-audit.md)
  — latest readiness audit.

## Historical research commands (not the quickstart)

From the repository root. These commands are development-period material,
not installation prerequisites; evaluation collectors, held-out rounds and
review sheets are not required to run the proxy. The historical
trace-enabled example writes full text; the current installation guide leaves tracing
off.

```sh
python3.12 -m unittest discover -s concept-verification/tests -v
python3.12 concept-verification/eval/perturb.py
python3.12 concept-verification/corpus.py prepare \
  --words-archive EXTERNAL_WORDS_ZIP \
  --ngrams-archive EXTERNAL_NGRAMS_ZIP \
  --output EXTERNAL_SQLITE
python3.12 concept-verification/eval/run_eval.py --phase dev \
  --config concept-verification/eval/config.json \
  --index EXTERNAL_SQLITE --results LOCAL_DEV
python3.12 concept-verification/eval/run_eval.py --freeze \
  --config concept-verification/eval/config.json --index EXTERNAL_SQLITE \
  --output concept-verification/eval/frozen-experiment.json
python3.12 concept-verification/eval/run_eval.py --phase heldout \
  --config concept-verification/eval/config.json --index EXTERNAL_SQLITE \
  --frozen concept-verification/eval/frozen-experiment.json \
  --reviewer-url http://REVIEWER_HOST:PORT/v1 --reviewer-model qwen3.8-27b \
  --reviewer-profile PRIVATE_REVIEWER_PROFILE --reviewer-timeout 30 \
  --results LOCAL_HELDOUT_FINAL
CONCEPT_INDEX=EXTERNAL_SQLITE \
CONCEPT_UPSTREAM_URL=http://UPSTREAM_HOST:PORT/v1 \
CONCEPT_REVIEWER_URL=http://REVIEWER_HOST:PORT/v1 \
CONCEPT_REVIEWER_MODEL=qwen3.8-27b \
CONCEPT_REVIEWER_PROFILE=PRIVATE_REVIEWER_PROFILE \
CONCEPT_TRACE_DIR=LOCAL_TRACE CONCEPT_TIMEOUT=30 \
CONCEPT_HEADER_TIMEOUT=30 \
  ./concept-verification/run_proxy.sh
python3.12 concept-verification/eval/collect.py --cases 8 \
  --codex-bin codex --codex-home PRIVATE_CODEX_HOME --profile qwen-neumann \
  --provider-id qwen-LSI-A100 --proxy http://127.0.0.1:18024/v1 \
  --trace-dir LOCAL_TRACE --work-root LOCAL_OWNED_WORK \
  --results LOCAL_WORKLOAD_FINAL --timeout 120
python3.12 concept-verification/eval/review_sheet.py --input LOCAL_WORKLOAD_FINAL \
  --traces LOCAL_TRACE --output LOCAL_REVIEW_SHEET_FINAL
python3.12 concept-verification/eval/score.py \
  --controlled LOCAL_HELDOUT_FINAL/heldout.json --workload LOCAL_WORKLOAD_FINAL \
  --traces LOCAL_TRACE --output concept-verification/eval/results/summary.json
```

The two prompt variants and four threshold settings are dev-only. The frozen
file binds the selected mode, threshold, prompt bytes/config identity,
dataset hashes, and index identity; held-out execution refuses mismatches.
Detector selection is separate from reviewer proposal and exact acceptance.
Accepted edits are applied only to original spans right-to-left, with
protected slices and all outside code points asserted unchanged.

## Historical evaluation programme (not an installation prerequisite)

The controlled split was deterministic and project-authored: dev had 16
cases and held-out had 32, including `točnij`, `rjavo-zlati`, `lase`,
`kitaraš/vokal`, `najslovnijih`, contextual constructions, typos,
valid-word controls, mixed technical prose, Markdown, commands, URLs, and
paths. The held-out report design covered raw/no-repair, detector-only,
reviewer-decision, full conservative, unigram-only, and local-context
ablations with denominators, candidate enrichment, recall, reviewer
accuracy, accepted/correct/harmful/missed counts, protected changes,
recovery, and latency.

Under the frozen design, the held-out reviewer command and the eight-case
collector command were required to run once per frozen round; real workload benefit or harm
was to stay `AWAITING_HUMAN_REVIEW` until the owner labels the deterministic
blinded sheet, and model self-review is not a human label. The design
required the collector to use `codex exec --profile qwen-neumann` with
explicit `CODEX_HOME`, provider/base URL overrides, `--ephemeral`, and a
finite subprocess timeout, with its tool-loop case creating and reading
`codex-tool-loop-proof.txt` in an owned disposable directory. Raw traces
were to stay under the explicitly configured local trace root, and tracing
disabled wrote nothing; a missing endpoint or invalid invocation was to be
recorded once as an external availability/protocol failure, never converted
into a quality success. This programme is historical record; it is not a
current installation prerequisite and does not reopen a separate human dataset.

## Chronology (historical order notes)

Each row links the immutable order and report records; the full chronology
lives in [docs/HISTORY.md](../docs/HISTORY.md) and Git.

| Order | Established | Record |
| --- | --- | --- |
| 013-a | Mandatory pinned Pandoc with exact original spans; no regex-only structural path. | [order](../oap/orders/013-a-pandoc-original-span-protection.md) · [report](../oap/reports/013-a-pandoc-original-span-protection.md) |
| 014-a | Bounded occurrence-addressed reviewer batch with one strict result shape per target. | [order](../oap/orders/014-a-bounded-occurrence-review-batch.md) · [report](../oap/reports/014-a-bounded-occurrence-review-batch.md) |
| 015-a | Explicit supported Responses contract for text and metadata. | [order](../oap/orders/015-a-supported-responses-contract.md) · [report](../oap/reports/015-a-supported-responses-contract.md) |
| 016-a | Read-only runtime evidence lookup and completed-original fallback. | [order](../oap/orders/016-a-runtime-evidence-fallback.md) · [report](../oap/reports/016-a-runtime-evidence-fallback.md) |
| 017-a | UTF-8-safe main body capture with an elapsed body budget. | [order](../oap/orders/017-a-main-body-capture.md) · [report](../oap/reports/017-a-main-body-capture.md) |
| 018-a | Independent elapsed response-header budget. | [order](../oap/orders/018-a-response-header-budget.md) · [report](../oap/reports/018-a-response-header-budget.md) |
| 021-a | Bounded final response delivery. | [order](../oap/orders/021-a-final-delivery.md) · [report](../oap/reports/021-a-final-delivery.md) |
| 022-a | Bounded main-upstream setup. | [order](../oap/orders/022-a-upstream-setup.md) · [report](../oap/reports/022-a-upstream-setup.md) |
| 023-a | Owned startup and partial-startup cleanup. | [order](../oap/orders/023-a-owned-startup.md) · [report](../oap/reports/023-a-owned-startup.md) |
| 024-a | Finite runtime evidence lookup budget. | [order](../oap/orders/024-a-evidence-work.md) · [report](../oap/reports/024-a-evidence-work.md) |
| 025-a | Bounded analysis eligibility. | [order](../oap/orders/025-a-analysis-eligibility.md) · [report](../oap/reports/025-a-analysis-eligibility.md) |
| 026-a | Bounded accepted-connection admission. | [order](../oap/orders/026-a-request-admission.md) · [report](../oap/reports/026-a-request-admission.md) |
| 027-a | Independent support and composed-result validation. | [order](../oap/orders/027-a-repair-validation.md) · [report](../oap/reports/027-a-repair-validation.md) |
| 028-a | One runtime lexical-acceptance policy; 028-b fixture reconciliation. | [order](../oap/orders/028-a-runtime-acceptance.md) · [report](../oap/reports/028-a-runtime-acceptance.md) |
| 029-a/029-b | Runtime word/phrase target selection (029-a halted, 029-b implemented). | [order](../oap/orders/029-b-runtime-detection.md) · [report](../oap/reports/029-b-runtime-detection.md) |
| 030-a | Request-scoped cancellation on client disconnect. | [order](../oap/orders/030-a-request-cancellation.md) · [report](../oap/reports/030-a-request-cancellation.md) |
| 031-b | Owned entry-point close and reviewer-only operator deadline. | [order](../oap/orders/031-b-close-proxy-and-preserve-order.md) · [report](../oap/reports/031-b-close-proxy-and-preserve-order.md) |
| 035-c | Unconditional defined-API logprobs removal. | [order](../oap/orders/035-c-strip-defined-api-logprobs.md) · [report](../oap/reports/035-c-strip-defined-api-logprobs.md) |

Earlier development orders (000–012) and the audit/closure rounds
(032–036) are recorded in the same immutable records and summarized in
[docs/HISTORY.md](../docs/HISTORY.md).

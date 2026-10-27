# LLM Slovenian Repair

Owner-published bootstrap baseline, accepted for continued development. Role
operation is qualified and the development loop has been deliberately started.
Query current protocol state with `python3 oap/bin/check_state.py --repo-root .
--repository ulfe-lmi/llm-slovenian-repair` and inspect `oap/active`.

Product PLANNED / NOT RUN. The implemented v1 seam provides strict frozen
`SpanSelection`/`SelectionBatch`, `EvidenceRecord`, `ReviewProposal`,
`OriginalCoordinateEdit`, `RepairResult`, and `PolicyConfig` models. Span offsets
are Python Unicode code-point offsets into the immutable original string; evidence
states are `EXACT`, `CENSORED`, or `UNAVAILABLE`, and the default policy is
`detect_only` with finite conservative limits.

Objective 004 adds the frozen `SourceManifest` and `SyntheticCountRecord`
provenance seam plus the canonical `verify_manifest_payload` boundary. The
manifest schema accepts only exact `UTF-8` encoding and `jsonl`/`json` records,
matched to `application/jsonl`/`application/json`. The checked-in
`tests/fixtures/corpus/synthetic-manifest.json` and JSONL payload are tiny,
project-authored synthetic schema fixtures only. Their authorized use scope is
`local synthetic tests only`, terms reference the repository `LICENSE`, and
`importer_schema_version` is `NOT_APPLICABLE_SYNTHETIC_FIXTURE`; no importer or
external corpus permission is claimed. They demonstrate checksum, bounded
loading, explicit denominator knowledge, and exact/censored/unavailable
evidence. The censored fixture records that values at/below synthetic cutoff 4
are represented only by `[0,4]`. Real candidate sources, rights, access, formats,
and release facts remain UNVERIFIED, and the fixture is excluded from the
installed package.

Detection, review calls, strict acceptance, patch composition, live compatibility,
and linguistic quality remain unimplemented or unproven. The intended library captures
a complete Slovenian model answer, selects suspicious local spans on CPU, optionally
asks the existing Qwen in an isolated context, validates independent evidence and
patches approved spans exactly. No repair application is implemented here.

The persistent development environment and tool caches are machine-local
(`$HOME/envs/llm-slovenian-repair`) via the sourceable `scripts/project_env.sh`
helper and `scripts/bootstrap_dev_env.sh`; configured shells do not create or use
a repository `.venv`. The pre-existing repository-local `.venv` and named tool
caches remain in place as inactive legacy data; the owner deferred their removal.

Start with [development](docs/DEVELOPMENT.md), [runbook](docs/OAP-RUNBOOK.md),
[role setup](docs/CODEX-ROLE-SETUP.md),
[readiness](docs/READINESS.md) and [testing](TESTING.md). Full product agreement is
[PLAN](PLAN.md), implementation baseline [architecture](ARCHITECTURE.md), and
sole live judgment register [CRITICAL](CRITICAL.md). Coding uses the root router
and compact law; strategy reads full sources from its separate private workspace.

Objective 005 adds the dated [real-source inventory](resources/source-inventory-v1.json)
and the standard-library-only [offline artifact verifier](scripts/verify_source_artifact.py).
The inventory records three derived CC BY-SA-labelled publisher artifacts and a
Gigafida 2.2 provider-agreement query interface. All artifacts remain
`NOT_ACQUIRED`; the verifier never downloads or extracts them. See
[data-source acquisition boundaries](docs/DATA-SOURCES.md) for the nonautomatic
staging recipe, MD5/SHA-256 distinction, and censored/unknown evidence semantics.

The repository is `ulfe-lmi/llm-slovenian-repair`; the owner's [LICENSE](LICENSE)
contains Apache License 2.0 and is preserved unchanged. Live repair testing is
disabled. Qwen compatibility, linguistic quality, ICA, milestone acceptance,
release, and deployment approval are not established.

Objective 006 adds a bounded, side-effect-free `unigram_importer` seam for the
observed Gigafida 2.0 lower-case form/lemma/POS TSV contract. It requires UTF-8
CRLF, all-fields-quoted rows and preserves all 28 source fields, nonnegative
counts, lossless decimal text/`Decimal` views, source/query/import completeness,
and stable morphology-aware record keys. NFC/casefold lookup values are derived
views; source text remains authoritative. The parser is incremental, frozen,
extra-forbid, offline, and never downloads or builds an index. Tests use only
project-authored synthetic data.

The objective-006 recovery receipt records source identity/schema facts from a
prior interrupted context, but also records three earlier GETs, so the order's
exact-one-fetch and real importer-smoke evidence are not claimable. No external
archive or row is retained, committed, or packaged; see the receipt under
`resources/source-acquisitions/` and the objective-006 report for the precise
partial boundary.
Round 006-d adds a standard-library, content-free classifier for bounded
unigram-row structure. Round 006-e corrects its prefix handoff with a public
`classify_stream` boundary and synthetic ZIP-member routing tests. One
verifier-first 006-e fetch then reached exactly 32 rows: 31 had 28 fields and
one had an empty terminal 29th field. The aggregate is diagnostic evidence only;
no real importer smoke, format correction, compatibility, redistribution, or
source retention is claimed. The temporary tree and all source bytes were
removed.
Round 006-g adds a verifier-first `scripts/smoke_unigram_prefix.py` probe. Its
bounded contract opens the selected member once, captures 14 preamble lines plus
the exact header and 32 rows within a 4 MiB envelope, checks the content-free
aggregate, and runs the public importer twice on fresh streams. Evidence remains
limited to one verified compatibility prefix and partial import; it does not
claim full archive import, lookup readiness, linguistic benefit, redistribution
rights, release, deployment, or acceptance.
The single 006-g acquisition passed canonical verification but its committed
CLI stopped before member access because the direct interpreter could not resolve
the checkout `src` path. That path bootstrap is corrected and tested offline; the
source tree was deleted, no retry occurred, and the receipt records null member,
structural, and importer results.
Round 006-h adds an artifact-free `--preflight` mode that validates the canonical
inventory entry, exact 834-byte header contract, real COMPLETE/COMPLETE/PARTIAL
provenance, and installed importer entry point/limits. Preflight and artifact
smoke arguments are mutually exclusive; the bounded `READY` output contains no
header or row content. The earlier independent system-Python dependency finding
is retained as a blocked 006-g fact and does not count as runtime readiness.
The exact 006-h preflight passed in an owned isolated environment. Its one direct
GET passed canonical verification and the bounded structural aggregate, then the
first importer invocation stopped at the finite `import-invalid-count` boundary;
no second run or GET occurred, and the source/environment were removed. The new
receipt records cumulative ten GETs, null importer hashes, and no retained source
content. This remains blocked compatibility evidence, not a full-source import.

Round 006-i adds a mutually exclusive numeric-shape diagnostic mode to that
verifier-first helper. It profiles exactly 32 structurally valid rows and all 24
numeric columns with a closed, fixed-priority syntax enum, recording aggregate
current-parser compatibility and the first safe incompatibility without emitting
numeric content. The one 006-i importer call returned `invalid-count:5` after
the complete profile. Its receipt records cumulative eleven GETs, prior failures,
exact cleanup, and syntax evidence only; no locale/conversion choice, full import,
redistribution, release, or deployment claim is made.
Round 006-j keeps importer semantics unchanged and refines the row-1 `OTHER_ASCII`
boundary with fixed marker, absolute/share/relative-family, identity-equality, and
NFC-casefold relation predicates. The 24 row-1 markers are content-free
`ASCII_MIXED_OTHER` observations, all distinct and nonrecurring in their columns;
the derived identity profile is an outlier. One in-memory envelope omitting only row
1 reaches the next current-parser boundary, `invalid-decimal:6`, with `max_rows=31`.
The receipt records one new GET (cumulative twelve), exact cleanup, unresolved row
role/unit meaning, and no conversion, full-import, redistribution, release, or
deployment claim.
Do not execute the [draft roadmap](oap/strategic-instructions/INITIAL-ROADMAP.md)
without strategic reconciliation and deliberate owner activation.

Round 006-k enforces report immutability from Git history. The two known historical
006-a and 006-c report rewrites are recorded in
[`oap/REPORT-HISTORY-INCIDENTS.json`](oap/REPORT-HISTORY-INCIDENTS.json) and are
accepted only as explicit frozen violations; new report paths must be add-once with
a report-only actual implementation parent. The guard is used by transcript and
report verification and by the `OAP report history` CI check.

The round also established a reusable external cache for the exact Gigafida archive
outside Git and the wheel. Its fixed source identity, inventory digest, archive
digests, ownership/type checks, and verifier-first promotion are enforced by
[`oap/bin/source_cache.py`](oap/bin/source_cache.py). Cache validation is offline;
006-k records the failed hardlink boundary and cumulative thirteen GETs; 006-l
completes one rename-only promotion, two content-free diagnostic consumers, three
revalidations, and cumulative fourteen GETs. The retained cache remains gated until
concept-experiment completion and has no redistribution authorization.

Round 006-l closes the cache mechanism and history-negative gaps without changing
product numeric semantics. Promotion uses one lock-protected same-directory rename,
reopens and re-verifies the final before exclusive metadata, and cleans only fixed
artifacts on expected failure. Report-history tests cover implementation-head drift,
same-path repair, manifest exceptions, and a third touch to a frozen incident.

Round 012-a (2026-10-25) reconciles the migrated native runtime: the versioned
`oap/governance/WORKSPACE-LAYOUT.json` now records native strategic storage
(strict 0700/0600 private modes) and foreground-only coding dispatch that
adopts the owner's already-running pane (zero models started; owner-launched
session homes preserved as launched). The post-merge 011-e tail is
publication evidence only: the publication proof alone does not establish
integration or scientific acceptance (any later main ancestry is verified
separately) - and the owner-supplied 011 research data archive is restored
(selected files hash-verified; collection bindings checked against the frozen
011b manifest) with evaluation blocked pending separate reconciliation of
the evaluation objective (no prior draft activated). The next
separately ordered objective is the owner-selected Pandoc structural-parsing
runnable proxy; round 013-a (2026-10-26) implemented it in the isolated
concept-verification proxy with exact original spans, conservative
abstentions, fail-closed bounded failure reasons, and a pinned 3.7.0.2
dependency (see `concept-verification/README.md`) - runnable-proxy
engineering evidence only, no linguistic, experimental-MVP, or deployment
acceptance. Round 014-a (2026-10-26) added one bounded occurrence-addressed
reviewer batch (`batch-v1`) to the same runnable proxy: at most one fresh
bounded review request per completed eligible answer, exact occurrence IDs
and fixed context windows, strict duplicate-key-free parsing at both
envelope levels, whole-batch rejection versus individual evidence
rejection, and a one-answer SSE eligibility guard, while the historical
single-target evaluator prompt/API remains unchanged; round 014-b
(2026-10-26) completed the terminal-answer-copy preflight on the same
branch (every answer-bearing SSE terminal copy proved consistent before
any reviewer call; contradictory, unowned, or duplicated copies abstain
with the raw original and zero review calls); round 015-a (2026-10-26)
added the explicit text-only Responses request contract: strict
pre-forward request validation with closed 400 labels before any main
or reviewer call, one shared completed-envelope profile for the
nonstreaming JSON primary path and the retained delayed SSE path
(JSON/SSE profile parity), a narrow forwarding header allowlist with no
reviewer-key borrowing, and request-local separated review usage with
explicit unknowns plus an optional content-free stderr observer;
round 016-a (2026-10-27) made the runtime evidence access strictly
read-only and degrades safely on technical evidence failure: the index
opens read-only only (never created or written, exact escaped path,
rollback-journal format required before any SQLite open, finite
per-query busy wait), stored counts must be exact nonnegative
integers, and missing/corrupt/incompatible/invalid-count/locked
evidence returns the completed original with zero review calls (early)
or aborts the whole optional pass while preserving the actual review
attempt and honest usage (late), while valid missing evidence remains
an individual proposal rejection; round 017-a (2026-10-27) made main
response body collection UTF-8-safe and elapsed-budget-bounded: one
monotonic body deadline anchored at collection entry governs
declared, close-delimited and chunked delivery (byte arrival never
resets it), wire chunk boundaries may split code points (carried
until the body is known complete, then strictly validated), declared
lengths deliver exactly the advertised bytes and only unknown-length
SSE may end at the terminal marker, chunked framing runs a bounded
owned state machine, and bounded main failures return 502 with zero
review calls, while the header phase is bounded separately (round
018-a) and connection/DNS deadlines and total wall-clock budgeting
remain unfinished; round 018-a (2026-10-27) bounded main response
status/header acquisition with one independent elapsed header budget
(keyword-only constructor parameter header_timeout appended after the
existing positional parameters; main() reads CONCEPT_HEADER_TIMEOUT
into it): one absolute monotonic header deadline
anchored before the owned guard starts (guard startup overhead is not
concealed), the stdlib getresponse parser retained and running on the
owning thread, an owned pure-timer guard that interrupts only the
exact captured socket and is cancelled and actually joined on both
success and failure before any transfer, a racing or late parsed
response explicitly closed and never transferred, and bounded header
failures returning 502 with zero review calls and zero engine
analysis, while the CONCEPT_TIMEOUT body budget begins later and
stays independent in both directions, and DNS/connect/request-upload
(before header acquisition), incoming client timeouts, total
wall-clock budgeting, admission control and cancellation remain
unfinished; round 019-a (2026-10-27) bounded the whole batch-review
exchange with one owned elapsed deadline: one finite positive
monotonic deadline anchored at batch entry covers the owned child
process's startup, the strict versioned IPC, and the child's actual
resolver/connect/TLS/upload/status/header/body work plus result
validation - a late or racing success is a failure and the exact
child is terminated and actually reaped before return; the IPC
channel keeps explicit finite per-field caps enforced on both encode
and decode; round 020-a (2026-10-27) bounded incoming client
request intake with one finite positive monotonic intake deadline:
one absolute deadline anchored while handling the accepted
connection BEFORE any request-line/header/body read and before the
owned intake guard starts, covering the first byte, the request
line, all headers and the exact advertised body (byte arrival,
phase transitions and legitimate short reads never reset it);
strict unambiguous framing (one finite decimal Content-Length
within the existing 2,000,000-byte cap; repeated fields even when
equal, comma lists, any Transfer-Encoding and any unsupported
Expect are a fixed content-free 400, and missing, negative,
overlarge or nondecimal lengths keep the existing 413); an
incomplete advertised body is never forwarded - even when its
prefix is complete valid JSON - and closes with a fixed
content-free 400; a stalled intake closes with zero main/analysis/
evidence/review work and a bounded best-effort 408; the owned
pure-timer guard interrupts only the exact accepted client socket
and is cancelled and actually joined on every path including
partial startup; trailing bytes never become a second request; the
keyword-only constructor parameter client_timeout is appended after
the existing positional parameters with the 30-second
CLIENT_REQUEST_TIMEOUT_SECONDS default and main() reads
CONCEPT_REQUEST_TIMEOUT into it, rejecting bool, nonnumeric,
zero, negative, nonfinite and platform-unrepresentable values
before any bind allocation; the intake deadline is independent of
the CONCEPT_TIMEOUT body/socket, the CONCEPT_HEADER_TIMEOUT header
budget and the 15-second reviewer exchange, and the
historical single-target
evaluator prompt/API remains unchanged (see
`concept-verification/README.md`) - runnable-proxy engineering
evidence only; the seed 013/014/015/020 packaged objectives remain
open. A
provisional 8-15 focused-engineering-day estimate covers the
remaining packaged-MVP scope, with research-evaluation completion, ICA and
deployment as separate gates. See
[development](docs/DEVELOPMENT.md), [runbook](docs/OAP-RUNBOOK.md),
[role setup](docs/CODEX-ROLE-SETUP.md), [readiness](docs/READINESS.md) and
[roadmap](docs/IMPLEMENTATION-ROADMAP.md) for the current continuation.

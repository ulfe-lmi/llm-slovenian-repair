# Initial roadmap — controlled seed

All 56 objectives are DRAFT UNTIL STRATEGIC RECONCILIATION. Product PLANNED; evidence NOT RUN. Each is one proof-sized PR, with same-PR corrective suffixes. Dependencies identify actual seams; ascending numbering is default schedule, not authority to skip unresolved work. Strategy records remaps/abandonment and preserves published history.

| ID | Objective | Prerequisites | Evidence boundary |
|---|---|---|---|
| 000-a | Reconcile bootstrap, repository and authority | reviewed baseline | Adopt the reviewed scaffold baseline on the first product PR; prove role routing/dense projections, source identity, inactive-to-active protocol and no implementation overclaim. |
| 001-a | Reproducible application development baseline | 000 | Establish selected Python/uv packaging, lint/type/test commands and offline default dependencies; no corpus/model download at import. |
| 002-a | CPU-only CI and governance guards | 000,001 | CI runs shared OAP/governance checks, source/compact coverage, deliberate CRITICAL loading, exact DHA/provenance and append-only negatives; no blanket full-source coding preload. |
| 003-a | Typed spans, evidence, reviews, results and policy | 001 | Explicit original-index convention, evidence statuses, modes and bounded defaults; schema rejection tests. |
| 004-a | Source manifests and miniature synthetic corpus | 003 | Record provenance, normalization, license-status and completeness/cutoff; fixture counts explicitly synthetic. |
| 005-a | Real source inventory and permitted acquisition recipe | 004 | Verify actual release/format/rights and a bounded download/import plan; no scraping or invented access. |
| 006-a | Unigram/lexicon importer | 003,004,005 | Correct parsing, normalization and frequency metadata with deterministic miniature and permitted sample tests. |
| 007-a | Bigram/trigram importer with censored absence | 004,005,006 | Test threshold interpretation, malformed data and impossible-zero rejection. |
| 008-a | Read-only sparse lookup and fixed-neighbor index | 006,007 | SQLite or justified equivalent; form/context lookups preserve incomplete-denominator metadata and reproducible manifest. |
| 009-a | Unicode token/span mapping | 003 | Exact substrings for repeated words, combining characters, emoji and CRLF; no detokenization rewrite. |
| 010-a | Protected Markdown/code/URL spans | 009 | Protect supported constructs and conservatively skip ambiguity; preserve byte/text content outside editable spans. |
| 011-a | Context boundaries and terminology exclusions | 009,010 | No false adjacency across protected material; configured terms, names and mixed-language uncertainty abstain. |
| 012-a | First deterministic suspicion selector | 008,011 | Explain alarms using source evidence, choose bounded non-overlapping word/phrase spans, support zero-alarm path. |
| 013-a | Versioned targeted-review prompt serializer | 003,009 | Preserve the agreed question and keep/wider-edit options; unambiguous repeated occurrence; no corpus candidates or main history. |
| 014-a | Strict reviewer-response parser | 003,013 | Reject duplicate/unknown/missing IDs and inconsistent keep/replacement/wider-edit states; confidence non-authoritative. |
| 015-a | Isolated reviewer HTTP client with fake upstream | 013,014 | Fresh messages and private nonrecursive endpoint; no tools/images/history linkage; one bounded request, no retry. |
| 016-a | Early bounded live-Qwen reviewer feasibility | 005,015 | Explicit opt-in, verified endpoint/model and protected fixture; tiny targeted keep/replace/wider-edit probe with honest results; no server changes. |
| 017-a | Initial strict word-replacement acceptance | 008,012,014 | Distinguish typo/lexical evidence; reject popular-but-unsupported choices and neutral corpus; no confidence-only acceptance. |
| 018-a | Short-phrase acceptance boundary | 017 | Restrict to preassigned span, reject wider edits and incomparable raw length-dependent frequency comparisons. |
| 019-a | Exact patcher and conflict-group rollback | 009,010,017,018 | Preserve every untouched original slice; reject overlap/stale offsets; rollback incompatible nearby edits. |
| 020-a | Completed-text pipeline with zero/one review call | 012,015,017,018,019 | End-to-end pure library state machine; failure returns safely captured original; no iterative regeneration. |
| 021-a | Offline CLI with explicit private inspection output | 020 | Process supplied text and show diffs/reasons on request; synthetic/non-private examples; no automatic production payload logging. |
| 022-a | Demonstrator evidence and ICA request | 016,020,021 | Map D01–D07 to concrete evidence; prepare a fresh architecture-to-merged-main demonstrator audit; recommend, never self-certify the milestone. |
| 023-a | Annotation schema and evaluation provenance | 003,021 | Define genuine error, acceptable alternative, style-only and wider-edit labels; permissions and configuration provenance. |
| 024-a | Bounded real-output collection workflow | 016,023 | Approved data and measured source model/sampling metadata; isolated storage, no OAP/customer-text leak; bounded batch not unlimited generation. |
| 025-a | Correct-text negative controls | 023,024 | Include rare legitimate language, names, technical language and protected content with explicit human review status. |
| 026-a | Frozen calibration/test split and dataset integrity | 023,024,025 | Prevent cross-split duplicates/leakage; version inputs and annotation status; distinguish pending human labels. |
| 027-a | Optional CPU linguistic-analyzer adapter | 003,005,026 | Integrate verified existing lemma/tagger capability behind an optional bounded interface; no second GPU model. |
| 028-a | Contextual morphology validation | 017,027 | Judge required case/number/gender from context, not erroneous original tags; ambiguity causes abstention. |
| 029-a | Lemma statistics and normalization compatibility | 008,027 | Source-consistent lemma evidence; do not reconstruct complete lemma distributions from censored forms. |
| 030-a | Morphology-aware detector calibration features | 012,026,028,029 | Separate surface anomaly, lemma anomaly, lexical misuse and unsupported terms; bounded explanatory evidence. |
| 031-a | Evidence-driven short-phrase grouping | 018,026,030 | Extend only before review within configured word/span bounds; test multiple alarms and refusal of wider edits. |
| 032-a | Versioned strict acceptance thresholds | 026,028,029,030,031 | Tune on calibration data only, by error class; leave experimental acceptance disabled; document coverage tradeoff. |
| 033-a | Comparative evaluation runners | 020,026,032 | Original, no-edit detector, direct Qwen proofreading as benchmark only, and constrained method; bound and meter calls. |
| 034-a | Quality report with denominators and uncertainty | 025,026,033 | Report precision, harmful/style-only edits, coverage and sample sizes; no unsupported 99%/zero-harm claim. |
| 035-a | Bounded CPU execution and cancellation | 020 | Limit text/jobs/time/memory; do not block HTTP event loop or duplicate large indexes uncontrolled. |
| 036-a | Review admission, queue, timeout and fairness | 015,020,035 | One concurrent repair from component; bounded waiting; cancellation and fallback; no starvation by unbounded review workload. |
| 037-a | Narrow API capability and bypass/reject contract | 020,036 | Select one verified nonstreaming text envelope; explicit policy for tools/JSON/SSE/stateful/multiple-choice/logprobs cases. |
| 038-a | Full main-response capture and completion validation | 037 | No text forwarded before final decision; bounded capture; preserve upstream errors and finish/incomplete semantics. |
| 039-a | Repair adapter integration without recursion | 020,037,038 | Compose completed main response with library and direct private reviewer; no constitutional-context path for review. |
| 040-a | Main-history and review isolation contracts | 013,015,039 | Client-managed next turn receives final answer only; unchanged input messages; unsupported stored-state links not silently accepted. |
| 041-a | Envelope preservation, usage and private metrics | 039,040 | Separate main/review usage and fixed-label timings; no content logs or falsely aligned logprobs; no-edit preservation tested. |
| 042-a | API failure, disconnect and concurrency tests | 035,036,038,039,040,041 | Cancel owned work, handle timeout/size/invalid shape, preserve tenant request isolation and avoid orphan review tasks. |
| 043-a | Bounded live complete-main-then-review integration | 016,039,042 | Verify actual execution order and endpoint compatibility on authorized Qwen; provide scoped measured evidence without host mutation. |
| 044-a | Experimental MVP evidence and independent closure gate | 022,034,042,043 | Map M01–M07 and PLAN §16 to held-out and real-boundary evidence; request fresh ICA on current merged main; no MVP-complete label from queue completion. |
| 045-a | Collocation feasibility and bounded integration | 005,029,034 | Inspect actual structure/rights; add only if measured benefit warrants it, otherwise record evidence-backed nonadoption. |
| 046-a | Lower-cutoff/full-statistics feasibility | 005,007,008,034 | Rights-aware reproducible plan or bounded importer improvement; unavailable data recorded honestly; no fabricated complete counts. |
| 047-a | Measured latency and resource budget | 034,036,043 | Separate CPU, queue, review and main timings; report memory and workload limits on verified hardware without reconfiguring Qwen. |
| 048-a | Broader negative/harm evaluation | 025,026,034,044 | Run defined approved held-out batches, quantify uncertainty and clustered-data limitations; human annotation time explicit. |
| 049-a | Packaging and local installation templates | 001,039,042 | Reproducible package and explicit configuration/systemd examples; no startup/cutover as install side effect. |
| 050-a | Health/readiness and disable/rollback behavior | 036,041,049 | Reflect index/config availability honestly; disable optional repair without model replacement; test degraded originals and hard errors separately. |
| 051-a | Gateway boundary and usage integration contract | 037,041,043 | Define public auth/quota ownership and private review accounting; no unauthorized edits to gateway or local-coding repositories. |
| 052-a | Explicitly gated candidate deployment/rollback rehearsal | 047,049,050,051 | Operate only on verified free loopback resources under separate authorization; otherwise prepare/test rehearsal without crossing live gates. |
| 053-a | Privacy, prompt-injection and structural abuse suite | 010,013,014,042 | Test hostile content as data, bogus IDs/expansion, secret canaries, no arbitrary tools/URLs and protected-span invariants. |
| 054-a | Reproducibility, rights and truthful final documentation | 005,045,046,048,049,051,053 | Source/license manifests, verified dependencies and supported/unsupported behavior; no inferred permission to redistribute corpora. |
| 055-a | Verified-service evidence and independent handoff | 044,047,048,050,052,054 | Assemble S01–S05, quality/cost/rollback and DHA evidence; repeat independent architecture-to-main closure audit and prepare human adjudication; no automatic release. |

## Phase evidence and human gates

000–022 maps PLAN D01–D07, then ICA-DEMONSTRATOR. 023–044 maps M01–M07 and all
eight PLAN §16 criteria, then ICA-MVP. 045–055 maps S01–S05 and applicable DHA,
then ICA-SERVICE. 022/044/055 request independent audits; they cannot certify them.
After gaps are remediated, repeat architecture-to-current-main audit. Missing rights,
annotation/live evidence remain unproven. Optional 045/046 may conclude explicit
evidence-backed nonadoption only under finalized criteria; MVP morphology cannot
disappear because optional analyzer 027 is not adopted. Safe independent work may
be remapped around blocked prerequisites with disposition; no false phase label.

PLAN §16 mapping: complete capture → 038/043; zero calls → 012/020;
local keep/replace only → 013/014/018; isolated history → 015/040;
approved spans only → 009/010/019; safe failure → 020/036/042;
censored statistics → 007/008/029; measured benefit/harm/cost → 033/034/047/048.
Each also requires the distinct tests and exact revision named in its order.

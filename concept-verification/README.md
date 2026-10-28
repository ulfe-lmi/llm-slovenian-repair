# EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE

This is one deliberately isolated research spike. It is not the production
application, a release, a deployment, a corpus redistribution, or a linguistic
quality claim. It uses standard-library Python 3.12, one synchronous process,
bounded finite HTTP calls, and a loopback-only proxy at `127.0.0.1:18024`.

The loader consumes only explicit external archive paths. It verifies regular
non-symlink owner/link-count-one files, exact size/MD5/SHA-256, selected member
names, 14-line preambles, header/marker hashes, CRLF, UTF-8, widths, and row
limits before inserting a derived SQLite index. Word absence is `UNAVAILABLE`;
missing n-grams are `CENSORED` with an unknown denominator. The archives and
index are private local data and must never be staged or packaged.

## Commands

From the repository root:

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
file binds the selected mode, threshold, prompt bytes/config identity, dataset
hashes, and index identity; held-out execution refuses mismatches. Detector
selection is separate from reviewer proposal and exact acceptance. Accepted
edits are applied only to original spans right-to-left, with protected slices
and all outside code points asserted unchanged.

## Protocol and evaluation boundaries

The proxy buffers a complete Responses SSE before CPU review. It changes only
assistant `output_text` belonging to natural message items. Reasoning, tools,
function arguments, IDs, usage, event order/count, and no-safe-text responses
are preserved. Incomplete upstream generations are errors, never successful
repairs. Reviewer calls are fresh non-streaming calls containing only compact
instructions, the exact sentence, and one target; only one strict JSON result
shape is accepted, and a wider edit or uncertainty keeps the original.

The controlled split is deterministic and project-authored: dev has 16 cases
and held-out has 32, including `točniej`, `rjavo-zlati`, `lase`,
`kitaraš/vokal`, `najslovnijih`, contextual constructions, typos, valid-word
controls, mixed technical prose, Markdown, commands, URLs, and paths. The
held-out report must include raw/no-repair, detector-only, reviewer-decision,
full conservative, unigram-only, and local-context ablations with denominators,
candidate enrichment, recall, reviewer accuracy, accepted/correct/harmful/
missed counts, protected changes, recovery, and latency.

The held-out reviewer command and the eight-case collector command are each run
once per frozen round. Real workload benefit or harm is
`AWAITING_HUMAN_REVIEW` until a human labels the deterministic blinded sheet;
model self-review is not a human label. The collector uses actual
`codex exec --profile qwen-neumann` with explicit `CODEX_HOME`, provider/base
URL overrides, `--ephemeral`, and a finite subprocess timeout. Its tool-loop
case creates and reads `codex-tool-loop-proof.txt` in an owned disposable
directory. Raw traces remain under the explicitly configured local trace root,
and tracing disabled writes nothing. A missing endpoint or invalid invocation
is recorded once as an external availability/protocol failure, not converted
into a quality success.

## Structural protection (Pandoc, order 013-a)

The runnable proxy's structural protection is mandatory installed Pandoc with
exact original spans. There is no regex-only runtime structural path and no
historical pulldown-cmark discovery or fallback on the proxy path; the frozen
research trail that used pulldown-cmark remains separate and unchanged.

Dependency and startup: the pinned version is `3.7.0.2` (see
`pandoc-dependency.json`: official Linux amd64 release archive, exact byte
count and locally computed SHA-256, not an upstream signature attestation).
The binary resolves from `CONCEPT_PANDOC`, then PATH (`pandoc`), and is
checked at startup - before the proxy binds any traffic - for executable
presence, exact version, and reader capability. `install_pandoc.sh` installs
the pinned archive into an owned absolute prefix (its first argument,
defaulting to `~/.local/share/concept-verification/pandoc-3.7.0.2`; no sudo,
no system replacement, no writes outside the prefix, no runtime downloads).
A missing, wrong-version, or capability-failing binary rejects the proxy
startup with a finite reason.

Reader profile and coordinates: the fixed profile is the
`commonmark_x+sourcepos-smart` reader with the `json` writer; no dialect drift
is permitted. Source positions are 1-based line/column pairs over the
NFC-normalized document with Unicode code-point columns (a tab starting at
column `c` advances the next code point to column `((c - 1) // 4 + 1) * 4 + 1`,
as observed with the pinned binary). Position provenance is established per
node: only machine-generated positions are trusted; a user `data-pos`
conflicting with a generated position defeats provenance for that node only,
while an identical duplicate is a no-op; duplicates are never collapsed or
resolved last-wins. Documents without a final newline exhibit container
endpoints beyond the last line (column 1; observed at `L+1` for paragraphs
and `L+2` for a one-line list); such endpoints are never editable leaf
coordinates and are never granted. Multi-line positions belong to containers
and are never granted.

Deny by default: only `Str` leaf spans whose position is proven against the
unmodified original are granted as editable prose - valid coordinates, exact
original-slice equality, grapheme-safe content and boundaries, and an
NFC-stable line. Whitespace glue is granted only between two granted,
contiguous prose spans in one proven shared prose context. Everything else is
protected: code, equations, HTML (including inner text between raw inline
tags), links and images including labels, configuration, metadata, markers,
soft breaks, escapes, entities, and every unprovable region. The established
pure research residual policy is then reused as additional conservative
protection (imported as a pure function; no helper discovery), including a
bounded proxy-side addition for unterminated prose-form TeX: any opener with
no closing sequence anywhere later protects to end of line. Residual matches
overlapping granted prose are retained in full.

Documented conservative abstentions (proven input subset): a span containing
an unproved grapheme-sensitive code point (C0/C1 controls, DEL, NEL, LS, PS,
unproved combining marks, variation selectors, ZWJ/ZWNJ) is never granted; a
non-NFC line abstains for that line; unpaired quotation interiors, HTML
fragment depth, and unterminated TeX stay protected; CR (bare or as CRLF) is
a control character, so a span containing it is never granted while the
surrounding NFC-stable prose on each side may still be granted (the line
break itself stays protected); and a document whose NFC decomposition cannot
be mapped line-exactly fails closed. Whole-document failure returns the exact
completed original with zero review calls.

Bounded failure behavior: finite input/output/timeout/node limits; subprocess
argv without shell; no untrusted filters or file/network reads; bounded
non-content diagnostics. Startup failures (not found, not executable, wrong
version, reader capability) reject the proxy before any traffic is accepted,
and the version is not rechecked per answer. Runtime failures (timeout,
nonzero exit, oversized input or output, malformed JSON, schema mismatch,
node limit, mapping integrity) return the byte-exact original and
short-circuit `RepairEngine.repair` before corpus access, detection, or
reviewer calls; upstream capture errors remain errors.

This is runnable-proxy engineering evidence only. It establishes no
linguistic, experimental-MVP, or deployment acceptance.

## Bounded occurrence-addressed reviewer batch (order 014-a)

The runtime `RepairEngine` now uses one versioned, occurrence-addressed
reviewer batch per completed eligible answer: `batch-v1`. The historical
single-target prompt, `Proposal`/`parse_proposal`, and the frozen research
evaluator API remain byte-identical and unchanged; the engine never falls
back to a per-target single-target call loop.

Target preparation is CPU-owned and fail-closed: at most the existing four
selected non-overlapping detector targets, in deterministic original order,
each assigned a stable response-local id (`t0..tN`). Every occurrence is
validated for `0 <= start < end <= len(original)`, exact original-slice
equality (a stale occurrence is never relocated by first-substring
matching), no overlap or protected intersection, grapheme-safe slice and
boundaries, and a target of at most 128 code points. Repeated text therefore
has separate ids and exact per-occurrence context. Any invalid, stale, or
oversized preparation returns the completed original with zero review calls.

Per-occurrence context is a documented fixed window of 240 original code
points before and after the target, with exact boundaries and explicit
`truncated_before`/`truncated_after` flags when the window reaches the
document edge; a truncated window is never presented as a complete sentence.
The prompt is one explicit instruction plus exactly one serialized JSON
object (`{"version":"batch-v1","targets":[...]}`): targets and their context
are data, not instructions. The instruction preserves the agreed
natural-appropriate-choice question, explicitly allows keep, uncertainty
(wider edit), and a more natural appropriate replacement, and rejects
stylistic-only and factual changes. Selection ids and original coordinates
remain CPU-owned; the model returns only ids and proposals.

Finite limits (constants in `config.py`, enforced before dispatch and before
any mutation): at most 4 items; target at most 128 code points; context 240
code points per side; prompt at most 8192 code points; request at most 32768
UTF-8 bytes; response at most 32768 bytes; proposal JSON at most 8192 code
points; `max_output_tokens` 1536; replacement at most 8 words / 128 code
points; the ordered finite 15-second reviewer exchange deadline (one
monotonic deadline anchored at batch entry that covers the owned
child process's startup, IPC, and its actual resolver/connect/TLS/
upload/status/headers/body work plus result validation; deadline
expiry prevents acceptance of any late or racing result, while the
exact child's termination and reaping are awaited before return -
cleanup and OS scheduling can add elapsed time, and there is no
hard-real-time return guarantee; the
operator-configured upstream capture timeout stays separate and never
extends reviewer calls); no retries. Code-point and byte counts are
distinct quantities.
Unsupported oversized target or prompt preparation returns the
original with zero calls; oversized reviewer output returns the original
after one call. Model output is never silently truncated.

Transport: one fresh nonstreaming `store:false` request directly to the
configured private Responses endpoint with explicitly bounded model output.
No tools or images, no main credentials copied from inbound headers, no
linkage ids or history, no constitutional context, no caller-selected URL,
no recursive repair route. The operator-configured reviewer credential
mechanism is reused without reading or logging real values in tests.

Strict parsing: duplicate keys are rejected, never collapsed last-wins, at
both the outer envelope and the inner proposal level. Only a supported
successful completed reviewer envelope with exactly one assistant
`output_text` is accepted as success; tool, refusal, or incomplete output is
not success. The inner object must carry version `batch-v1` with exact keys
and exactly one result for every supplied id (no duplicate, unknown, or
missing id), exact booleans, keep ⇒ null replacement, wider ⇒ keep + null
replacement, replace ⇒ nonempty bounded string + wider false. Unknown fields
or version, malformed, fenced, or trailing output, null/bool/type
mismatches, nonfinite numbers, and oversized output reject the whole batch.
Partial JSON is never salvaged and no second call is made. Response order
may differ; results are mapped by validated id, never by array position.

Whole-batch versus individual rejection: any batch-level error, timeout,
non-200, invalid encoding, schema violation, or duplicate id returns the
byte-exact original after at most one request, with no retry and no
partially accepted edit. Structurally valid proposals rejected by current
corpus/lexicon evidence (including the barrier-aware neighbor checks) remain
individual rejections, while other independent valid proposals in the same
batch proceed. Keep and wider edits are no-ops. Original-slice patching and
protected-slice invariants are unchanged.

One-answer SSE eligibility: a completed upstream SSE representing several
assistant text answers/items/content parts, or otherwise ambiguous target
ownership, bypasses repair unchanged with zero review calls. Review covers
only one unambiguously identified assistant text answer; the per-answer
review budget is at most one batch, never reset per field, and several
answers are never collapsed into one string or picked first. Established
valid single-answer SSE behavior is preserved; unknown or ambiguous shapes
may abstain.

Terminal answer copies (order 014-b): before any reviewer call, a
preflight proves every answer-bearing terminal representation consistent
with the one confirmed answer - the same exact typed id, final list
positions, assistant role, completed status, content cardinality and part
kinds, and the exact original answer text across `output_text.done`,
`content_part.done`, and message-typed `output_item.done` copies (at most
one of each kind). Initial `added` events are supported only as empty
placeholders: their ownership (the typed confirmed id) and, for message
items, the assistant role are validated, and their content is never
rewritten. Every `output_text.delta` payload must be a string (an empty
string is a valid no-op). Any copy that cannot be proved consistent -
different text, role, status, index, or cardinality; a duplicated
terminal copy; a missing/null/non-string id; an answer event for another
id; or non-empty initial content - abstains with the raw original bytes
and zero review calls. The renderer then mutates only the explicit event
references collected during that preflight: the confirmed final answer,
each validated terminal copy, and the confirmed delta events (the first
non-empty delta carries the full repaired text, later deltas are
emptied). No value matching, no id coercion, no metadata traversal.
Order 014-a's A4 proof established that nominal terminal copies are
updated consistently through explicit validated paths; it did not prove
that contradictory, unowned, or duplicated terminal copies are rejected.
Two distinct 014-a failure modes were observed at the published head:
same-ID contradictory or extra terminal copies were blindly rewritten to
the repaired text (the extra or conflicting content was modified), while
unowned terminal copies (a missing or non-string id) were left unchanged
beside an edited final answer. The 014-b preflight rejects both: every
terminal representation is proved consistent before any reviewer call, and
any copy that cannot be proved consistent abstains with the raw original
and zero review calls, so the negative matrix - direct transform plus the
full actual HTTP chain - proves the rejection. The 014-a report remains
unchanged.

Trace additions are bounded to a per-answer `review_batch` record: fixed
call count, target count, outcome, and reason labels only. No raw prompts,
responses, or untrusted exception text is logged. This is runnable-proxy
engineering evidence only; it establishes no linguistic, experimental-MVP,
or deployment acceptance.

## Explicit text Responses contract (order 015-a)

The proxy now enforces an explicit text-only Responses request contract
on `POST /v1/responses` before any forwarding (pure module
`responses_contract.py`, content-free labels only): a strict JSON object
(no duplicate keys, no nonfinite numbers, no coercion) with a nonempty
bounded `model`, text input as a string or a client-managed text-only
message sequence, explicit `store: false`, a boolean `stream` (absent
means false), and the allowlisted ordinary fields
`temperature`/`top_p`/`top_k`/`max_output_tokens`/`stop`/`metadata` with
exact types and finite values. Any other key is an unsupported
capability and is rejected regardless of its value (stored chaining via
`previous_response_id`, `include`, `logprobs`, `tools`, `text`, `n`,
`audio`, `conversation`, `background`, ...). Rejections return HTTP 400
with one closed label (`REQUEST_INVALID_JSON`,
`REQUEST_DUPLICATE_KEY`, `REQUEST_INVALID_NUMBER`, `REQUEST_SCHEMA`,
`REQUEST_STORE_REQUIRED`, `REQUEST_UNSUPPORTED`) before any main or
reviewer call: negative request tests assert zero main HTTP calls and
zero review calls.

The exact input message shape: `input` is either a nonempty string
(1-200,000 code points) or a list of 1-64 messages, where each message
carries exactly the keys `role` and `content`; `role` is one of
`user`, `assistant`, `system`, or `developer` (exact string); and
`content` is either a nonempty string (1-200,000 code points) or a
list of 1-32 parts, where each part carries exactly the keys `type`
and `text`, `type` is exactly `input_text`, and `text` is a nonempty
string (1-200,000 code points). Client-side history conversion (for
example, a previous assistant turn) is supplied by the client in this
same shape and validated as-is; any other shape - extra keys, unknown
roles, non-text parts, or empty content - is rejected before any
forward. The 200,000-code-point bound applies per input string, per
message content string, and per part text - not as an aggregate across
the 64 messages or 32 parts; the whole request remains bounded by the
2,000,000 UTF-8 byte request limit.

Main-response eligibility is one shared profile for the nonstreaming
JSON primary path and the retained delayed SSE path: a documented
Responses object (`object == "response"`) with exactly
`status == "completed"`, an absent/null `error`, and no explicit
stored/background/linkage/incompleteness declarations (pinned typed
policy: absent or null is unset; present `store`/`background` accept
only the exact boolean `false`; a non-null `previous_response_id`,
`conversation`, or `incomplete_details` contradicts the stateless
foreground profile), at most one bounded noneditable reasoning item
(status null/missing/completed only) preceding exactly one assistant
message with an exact typed nonempty id and exactly
`status == "completed"`, carrying exactly one plain nonempty
`output_text` part with aligned `annotations`/`logprobs` absent or
empty. The delayed SSE completed event is validated with that same full
envelope validation, so JSON and SSE handle the same final
`response.output` identically (profile parity); unknown output
variants, tools/refusals, extra messages/parts, malformed or missing
identity, incomplete reasoning, contradictory declarations, and
non-empty aligned metadata all abstain with the raw original bytes and
zero review calls. Nonstreaming JSON is repaired through the real
engine on the same one-answer policy; malformed main JSON or capture
remains a main error under the finite HTTP failure contract (HTTP 502),
a declared-mode/observed-content-type mismatch returns 502
`RESPONSE_MODE_MISMATCH`, and a no-edit repair returns the raw bytes
unchanged while a changed answer mutates only the validated part text
(usage and metadata preserved as reported; metadata echoes are never
scanned).

Forwarding uses a narrow header allowlist (content-type, accept, and an
explicitly caller-provided authorization only); hop-by-hop, internal,
control, and linkage headers are never forwarded, and the reviewer API
key is never borrowed as a main credential. Reviewer usage is
request-local: it is reset on every request, absent or invalid counts
are explicit `"unknown"` (never zero, never carried over), and main
usage is preserved as reported. `CONCEPT_USAGE_OBSERVER=stderr` enables
a bounded content-free operator record (review call count plus token
counts or `unknown`; no request id, no raw text) at the normal entry
point, and an observer failure never changes a completed answer.
Client-managed history (two-turn input messages) is supported; stored
chaining is rejected before any forward. Declared request limits
(`config.py`): request body at most 2,000,000 bytes (HTTP 413 before
any forward when the declared length exceeds the bound); `model` at
most 200 code points; input string and each message content or part
text at most 200,000 code points each (per string/part, not an
aggregate); at most 64 messages and at most 32
parts per message; `stop` at most 4 sequences of at most 32 code
points; `max_output_tokens` at most 32,768; `metadata` at most 16
string keys of at most 64 code points with string values of at most
256 code points; `top_k` at most 100; `temperature` in [0, 2] and
`top_p` in (0, 1] as finite numbers (bool rejected). Total
wall-clock request budgeting, disconnect handling, admission control,
cancellation, and CPU limits are not
implemented in this proxy: the ordered finite 15-second batch-reviewer
limit is a whole-exchange deadline anchored at entry (order 019-a),
covering the owned child process's startup, IPC, and its actual wire
work (deadline expiry prevents acceptance of any late or racing
result, while the exact child's termination and reaping are awaited
before return; cleanup and OS scheduling can add elapsed time, with
no hard-real-time return guarantee); the historical single-target
evaluator prompt/API keeps its
historical per-call contract. The upstream capture timeout
(`CONCEPT_TIMEOUT`) is the connection/socket timeout and, since order
017-a, also the one elapsed main-body budget. The independent elapsed
response-header budget (`CONCEPT_HEADER_TIMEOUT`, order 018-a) bounds
status/header acquisition only. The incoming client request intake
deadline (the `client_timeout` keyword-only constructor parameter
appended after `header_timeout`, following the existing positional
parameters; the `CONCEPT_REQUEST_TIMEOUT` operator value, default
30 seconds, order 020-a) is one absolute monotonic deadline anchored
while handling the accepted connection before any
request-line/header/body read and before the owned intake guard
starts, covering the first byte, the request line, all headers and
the exact advertised body; byte arrival, phase transitions and
legitimate short reads never reset it, and OS accept-backlog
waiting (before the connection is accepted and handled) is outside
the intake clock. The budget must be a finite positive
platform-representable value and is rejected before any bind
allocation (bool, nonnumeric, zero, negative, nonfinite, or beyond
the finite threading wait bound). Strict unambiguous framing
rejects repeated Content-Length fields (even equal values), comma
lists, any Transfer-Encoding and any unsupported Expect with a
fixed content-free 400 before any body read or forward, and keeps
the existing 413 for a missing, negative, overlarge (beyond the
existing 2,000,000-byte request cap) or nondecimal length; the
supported length is a strict ASCII decimal (ASCII 0-9 only, no
signs or Unicode digits, surrounding SP/HTAB ignored for the
numeric view, leading zeros permitted, and significant digits
bounded before integer conversion while the raw request bytes are
unchanged). An incomplete advertised body - even with a complete
valid JSON prefix - is never forwarded and closes with a fixed
content-free 400 and zero downstream work (delivered where
possible; when the peer or socket is already closed, delivery is
not guaranteed); a stalled intake closes with zero
main/analysis/evidence/review work and a bounded best-effort 408
(the quiet close is the observable outcome), and trailing bytes
never become a second request (HTTP/1.0 close, single-threaded).
The owned pure-timer guard interrupts only the exact accepted
client socket and is cancelled and actually joined on every path
including partial startup, so no intake work outlives the request.
The final response delivery deadline (the `delivery_timeout`
keyword-only constructor parameter appended after `client_timeout`,
following the existing positional parameters; the
`CONCEPT_DELIVERY_TIMEOUT` operator value, default 30 seconds,
order 021-a) is one absolute monotonic deadline anchored
immediately before final response emission - status line, headers,
body and the actual flush - and before the owned delivery guard
starts, so guard startup is charged to the clock; response-ready
work (upstream capture and optional repair) is outside this phase;
byte progress, short writes and phase transitions never reset it;
a late or racing completion loses to expiry (deadline expiry
prevents acceptance of late results, while the owned guard thread
is cancelled and actually joined before return; cleanup and OS
scheduling can add elapsed time, with no hard-real-time return
guarantee); once any response emission began, no second response,
status or fallback is attempted on that socket and a failed send
before bytes is closed safely without recursive retry; the owned
pure-timer guard interrupts only the exact captured accepted socket
and is cancelled and actually joined on every path including
partial startup, so no delivery work outlives the response; a
stalled or slowly reading client is closed quietly with no body
logging, and local send completion is not proof the peer received
or read the bytes (no delivery acknowledgment or hard-real-time
claim). The budget must be a finite positive
platform-representable value and is rejected before any bind
allocation (bool, nonnumeric, zero, negative, nonfinite, or beyond
the finite threading wait bound). All five - the setup axis
being the main-upstream setup deadline in the order 022-a
section below (CONCEPT_SETUP_TIMEOUT, 30 s default) - stay
separate from the
15-second reviewer limit and from the unimplemented overall
deadlines. The frozen historical single-target evaluator prompt and
protocol remain unchanged.

## Read-only runtime evidence and completed-original fallback (order 016-a)

The proxy's runtime evidence access (the prepared tiny SQLite index)
is strictly read-only through the new `runtime_corpus.py` adapter,
which inherits the nominal `Corpus` interface so the frozen detector
and acceptance code type-check unchanged (frozen `corpus.py` is
byte-identical) and overrides the constructor and every data-access
method:

- The exact configured path (absolute or relative against the process
  working directory, percent-escaped including Unicode, spaces, `#`
  and `?`; no Python-level path resolution and no alternate-file
  search - ordinary regular-file symlink and hardlink spellings are
  followed by the OS open and remain supported) opens as a
  `file:<uri>?mode=ro` URI: no file creation, normalization, or write
  of any kind, and no `immutable=1`/no-lock assumption.
- A bounded read-only header preflight runs BEFORE any SQLite open:
  the exact file is opened read-only and non-blocking and checked with
  `fstat`, so a non-regular resource (for example a pipe reachable
  through `/proc/self/fd`) is rejected without blocking for a writer
  that never comes, while ordinary regular-file paths (including
  symlink and hardlink spellings) continue. The 100-byte header must
  carry the SQLite magic and write/read version byte 1 (the supported
  prepared rollback-journal/DELETE index); a WAL-journal index
  (byte 2) is rejected as an unsupported journal mode because even
  read-only access to it persists `-wal`/`-shm` auxiliary files, and
  any other or missing header is corrupt. No conversion, sidecar
  cleanup, copying, or chmod occurs.
- A finite per-query busy wait (`config.RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS`,
  0.25 s; `PRAGMA busy_timeout` 250 ms) bounds lock waiting per query;
  it is not a total CPU/query deadline.
- Stored counts are validated type-strictly as nonnegative Python
  integers on the returned value (no `int()` repair, no truncation,
  no invented zero): text, NULL, negative, or fractional stored
  counts are technical evidence failures, while a valid zero stays
  `EXACT(0)` and a missing row stays `UNAVAILABLE` (unigram) or
  `CENSORED` (ngram).  SQLite stores a bound boolean as integer 1, so
  no boolean origin is detected.
- Failures are one of six fixed content-free labels
  (`RUNTIME_EVIDENCE_UNAVAILABLE`, `RUNTIME_EVIDENCE_CORRUPT`,
  `RUNTIME_EVIDENCE_INCOMPATIBLE`, `RUNTIME_EVIDENCE_INVALID_COUNT`,
  `RUNTIME_EVIDENCE_LOCKED`, `RUNTIME_EVIDENCE_UNSUPPORTED_JOURNAL`);
  the detail carries at most the Python exception class name, never
  SQL text, path, value, target, or credential. Handles are closed on
  success and on construction or context failure.

The proxy opens the evidence index only after a complete main passes
eligibility (an ineligible main never opens or creates the index):

- An early technical failure (missing path, corrupt bytes,
  incompatible accessed schema, invalid stored count, lock, or
  unsupported journal during construction or detection) returns the
  exact completed original bytes with zero edits and zero review
  calls; the trace records the evidence failure.
- A late failure during per-proposal validation aborts the whole
  optional pass from the immutable original: no earlier accepted edit
  survives, while the actual review call and known or unknown usage
  are preserved.  The usage observer records the actual review call
  count and reviewer usage (it carries no rollback flag); the
  optional persisted trace separately records the aborted acceptance
  disposition, the evidence failure, and the untrusted reviewer
  proposals kept apart from the cleared replacement list.
- Ordinary missing replacement evidence remains an individual
  proposal rejection (a valid first edit survives), and the same proxy
  recovers on the next healthy request with no usage carryover.

Pandoc, main, request-contract, and historical single-target
evaluator semantics are unchanged.

## UTF-8-safe main body capture with an elapsed body budget (order 017-a)

Main response BODY collection after headers are available is bounded
and wire-fragmentation-safe through the new `capture_transport.py`
module:

- One finite positive monotonic BODY deadline is anchored at
  collection entry and governs declared Content-Length,
  close-delimited and chunked delivery (the operator value
  `CONCEPT_TIMEOUT`); byte arrival never resets it, and nonfinite or
  nonpositive operator values are rejected before any bind allocation.
  The raw body byte bound (`MAIN_BODY_MAX_BYTES`, 8,000,000 bytes) is
  independent of code points.
- Wire chunk boundaries may split a UTF-8 code point: the possibly
  incomplete trailing sequence is carried until the body is known
  complete, where a truncated or genuinely invalid encoding is a
  bounded main failure. Raw bytes, Unicode and CRLF are preserved;
  there is no ignore/replacement decoding, normalization, substring
  recovery or answer regeneration.
- Declared Content-Length bodies deliver exactly the advertised bytes:
  early EOF is a bounded main failure and over-read bytes beyond the
  declaration are ignored. Only unknown-length delivery may terminate
  at the delimited SSE terminal marker (keep-alive without EOF;
  over-reads buffered during header parsing are drained without
  entering the stdlib chunk decoder or its connection-closing read
  paths).
- Chunked bodies are decoded by a bounded owned framing state machine
  (finite size-line and trailer length and count guards) ending at the
  terminating zero chunk. The stdlib chunked decoder is deliberately
  not used: its per-read blocking sub-reads (chunk-size lines, CRLF
  discards, trailer lines) cannot respect an elapsed deadline, and it
  closes the connection file object on protocol completion.
- Bounded main failures (body timeout, hard byte limit, premature EOF,
  incomplete SSE, malformed main) return 502 with zero review calls;
  no CPU, evidence or review work starts before capture completes, and
  all owned transport handles are closed so no transport outlives the
  request.
- Useful JSON/SSE repair, one batch, exact original spans, protected
  Unicode/code/math/HTML/links, client history, credentials,
  main/reviewer usage and metadata contracts are unchanged.

The header phase (slow response headers with a fast body) is not
covered by the body budget; order 018-a bounds it separately below.

## Independent elapsed response-header budget (order 018-a)

Main response STATUS/HEADER acquisition is bounded by an independent
elapsed budget through the new `header_transport.py` module:

- One finite positive monotonic HEADER deadline is anchored
  immediately before acquisition (before the owned guard starts), so
  guard startup overhead is not concealed; byte arrival and
  legitimate interim 100 responses never reset it. The constructor
  parameter `header_timeout` is keyword-only, appended after the
  existing positional parameters, and defaults to
  `MAIN_HEADER_TIMEOUT_SECONDS` (30 s); the normal `main()` entry
  reads the operator environment value `CONCEPT_HEADER_TIMEOUT` with
  that default, and nonnumeric, bool, nonfinite or nonpositive values
  are rejected before any bind allocation.
- The stdlib `getresponse` parser is retained unchanged and runs on
  the owning calling thread; the owned guard is a pure timer that
  owns only a bounded event wait plus a shutdown of the exact
  captured owned socket object, so it never touches another owned
  connection. The guard is cancelled and actually joined on both
  success and failure before any classification or transfer; no
  header work outlives acquisition.
- A racing or late parser return after the deadline is explicitly
  closed and never transferred (completion racing expiration loses to
  expiration). Bounded header failures (slow status line, slow
  header lines, interim 100 drip, hanging upstream that never sends
  a status line) return 502 with zero review calls and zero engine
  analysis before valid capture, and the same proxy recovers on the
  next healthy request.
- The body deadline (`capture_transport`, `CONCEPT_TIMEOUT`) begins
  later and remains independent in both directions: a body arriving
  after the header budget but within the body budget succeeds, and
  slow headers under a generous header budget with a short body
  budget succeed.

Actual HTTP and real-TLS coverage includes fast-header positives with
real wire UTF-8, a useful two-target repair that applies both
supported edits while preserving protected code, TeX, HTML, link and
an NFC-unstable decomposed/combining line exactly in the final
composed answer, expiration recovery, other-connection isolation, and
subprocess children with finite parent deadlines and process-group
kill/reap. NOT covered: DNS resolution, connect and request upload
(these occur before header acquisition and stay outside the header
budget), incoming client timeouts, reviewer-total, total wall-clock
budgeting, admission control, fairness, disconnect handling,
cancellation, CPU limits, quality, or live service/packaging
qualification.

## Bounded final response delivery (order 021-a)

Final response emission on the accepted client socket is bounded by
an independent elapsed delivery budget through the new
`delivery_transport.py` module:

- One finite positive monotonic DELIVERY deadline is anchored
  immediately before final response emission (status line,
  headers, body and the actual flush) and before the owned delivery
  guard starts, so guard startup overhead is not concealed.
  Response-ready work - upstream main capture and optional repair -
  completes first and stays outside this phase. The constructor
  parameter `delivery_timeout` is keyword-only, appended after
  `client_timeout`, and defaults to
  `CLIENT_DELIVERY_TIMEOUT_SECONDS` (30 s); the normal `main()`
  entry reads the operator environment value
  `CONCEPT_DELIVERY_TIMEOUT` with that default, and bool,
  nonnumeric, zero, negative, nonfinite or platform-unrepresentable
  values are rejected before any bind allocation.
- Byte progress, short writes, phase transitions and internal
  retries never reset the deadline; a per-write idle socket timeout
  alone would not bound a slowly reading client. A late or racing
  completion loses to expiry: deadline expiry prevents acceptance
  of late results, while the owned guard thread is cancelled and
  actually joined before return (cleanup and OS scheduling can add
  elapsed time; no hard-real-time return guarantee).
- The owned guard is a pure timer that owns only a bounded event
  wait plus a shutdown of the exact captured accepted socket
  object, so it never touches another connection. The guard is
  cancelled and actually joined on every path - success, timeout,
  early disconnect, write or flush error, exception and startup
  failure (including a thread that started and already ended before
  start raises; a never-started thread is never joined) - so no
  delivery work outlives the response and no guard is armed during
  the next connection or downstream work.
- Every post-intake response write is bounded: completed 200 JSON
  and delayed SSE, unchanged bypass, an actual non-200 upstream
  status/body (kept, not blanketed to 502), the fixed content-free
  contract 400, capture/protocol 502 and existing generated
  post-intake errors. A delivery timeout or failure closes quietly
  with no body logging; once any response emission began, no second
  response, status, 502 or fallback original is attempted on that
  socket, and a failed send before any byte is closed safely
  without recursive retry. Early parser, path and framing errors
  remain bounded by their existing intake lifecycle (existing
  intake errors remain bounded best effort) and are not newly under
  this delivery guard; the delivery deadline covers post-intake
  response emission only. Local kernel acceptance of the bytes is
  not proof the peer received or read them; no delivery
  acknowledgment is claimed.
- The delivery budget is independent of the intake, header,
  body/socket and 15-second reviewer budgets: a healthy main/review
  phase may outlast a short delivery budget before the delivery
  deadline anchors, and a stalled or slowly reading client is
  closed boundedly while the same proxy recovers on the next
  healthy request.

Actual loopback coverage includes a nonreading client that stalls
at the bounded write and is closed by the handler without the
fixture closing first, a matched slowly reading paced pair where
progress would defeat an idle-only timeout, measured
status/header/body/flush phase boundaries, including the
cumulative case where each observed phase is below budget but the
total is over it (with generous positive controls on the same
producer), successful completion,
deadline races and late completion, early disconnect, write and
flush failure, before-start/after-start/already-ended startup
failures with observed joins of exact owned threads and sockets,
genuinely late other-connection traffic (B's TCP connect is
established while A is in flight) whose first request bytes are
sent only after A's real guard is released and actually joined and
the original deadline passed, and an owned finite parent-supervised
hanging-client subprocess with bounded terminate/kill/reap. Phase
timing uses controlled call-through delays at the real write and
flush boundaries, clearly separated from those native wire
proofs. NOT covered: main DNS resolution,
connect and request upload (before the response phase), overall
request/wall-clock/CPU/admission/fairness budgets, post-intake
disconnect detection while main/review runs, remote cancellation,
and quality or live service/packaging qualification.

## Bounded main-upstream setup (order 022-a)

The main upstream's preparation and request-upload phase is
bounded by an independent elapsed setup budget through the new
`upstream_setup.py` module (with the exact repository-local
`upstream_worker.py` child-side entry):

- One finite positive monotonic SETUP deadline is anchored by the
  owner (ConceptProxy.forward) at entry to the owned main forward
  setup, BEFORE any worker/guard/process/IPC startup, resolver
  call, connect/TLS or request emission, so startup overhead is
  not concealed. It covers owned transport startup, address
  resolution, bounded address attempts, the TCP connection, the
  TLS handshake and the entire request write through the last body
  byte handed to the local transport. The constructor parameter
  `setup_timeout` is keyword-only, appended after
  `delivery_timeout`, and defaults to
  `MAIN_SETUP_TIMEOUT_SECONDS` (30 s); the normal `main()` entry
  reads the operator environment value `CONCEPT_SETUP_TIMEOUT`
  with that default, and bool, nonnumeric, zero, negative,
  nonfinite or platform-unrepresentable values are rejected before
  any bind allocation and revalidated at use; an explicit upstream
  port 0 is rejected with the full 16-bit port meaning (never
  aliased to the scheme default).
- Byte progress, short writes, address attempts and phase
  transitions never reset the deadline; a per-operation socket
  timeout alone would not bound a phase composed of many short
  blocking operations. Every blocking operation is therefore
  additionally capped by the remaining deadline, and a pure timer
  guard - which can interrupt only the exact socket object it
  currently holds (adopted immediately before each potentially
  blocking phase; an already-fired guard refuses to adopt) -
  covers the phases a socket cap alone cannot express (TLS
  handshake, request write). A late or racing setup completion
  loses to expiry: deadline expiry prevents acceptance of late
  results, while the owned guard thread and any owned child are
  cancelled, terminated and actually joined/reaped before return
  (cleanup and OS scheduling can add elapsed time past the
  deadline before the bounded return; no hard-real-time
  guarantee).
- The resolver runs in the owned finite stdlib child because no
  parent socket exists yet for a timer to interrupt: a timer
  cannot interrupt getaddrinfo merely by closing a socket that
  does not exist, and timing out a Future/daemon thread does not
  cancel it. The child is one ordinary owned process - exact argv
  array, isolated interpreter flags (-I -S -B), empty
  environment, no shell, no model or agent - speaking the strict
  versioned USTX v1 frame protocol (8-byte big-endian
  payload-length prefix; request payload at most 265 bytes =
  10-byte header + host at most 255 UTF-8 bytes; response
  payload at most 1065 bytes = 9-byte header + up to 16 entries of
  2-byte overhead (one family byte + one address-length byte) plus
  at most 64 address bytes; port 1-65535; exactly one
  frame per direction, the request channel ending with EOF and
  extra reply bytes rejected; wire maxima 273/1073 bytes
  including the prefix; no body, credential or key data in the
  resolver IPC) over private pipes, with the caps enforced on
  both encode and decode; an
  IP-literal host never reaches the child; at most one resolution
  attempt occurs (no automatic retry); its stderr is silenced and
  its stdout carries only the frame, so no raw exception text,
  host or address can leak; the parent's pipe descriptors are
  nonblocking (POSIX fcntl on the qualified Linux/Python 3.12
  environment) and every partial write/read and readiness race is
  governed by the remaining deadline; on expiry the parent
  terminates and actually reaps the exact child.
- A successful setup releases its clock (the guard is cancelled
  and actually joined, including a thread that actually started
  before a startup failure and a never-started thread that is
  never joined) BEFORE actual response-header acquisition; the
  existing header/body, intake and delivery clocks then run as
  before on their own independent axes. Setup failure is a main
  failure: the handler's existing fixed content-free 502 path
  with zero engine, corpus or reviewer work and no fabricated
  completion, and the same actual proxy answers the next healthy
  request after the failed request's original deadline has passed
  and its guard has been actually joined: that healthy request
  anchors and runs under its OWN FRESH setup deadline, so a
  passed deadline is never accepted. Local write
  completion is not peer receipt or model-execution
  acknowledgment; no delivery acknowledgment is claimed.

Actual loopback coverage includes: setup-budget validator
boundaries (rejected bool, nonnumeric, zero, negative, nonfinite
and platform-unrepresentable values; accepted finite positives);
the strict versioned frame codec (trailing and malformed frames,
per-field caps at decode); the owned guard lifecycle (exact-socket
interruption, adopt refusal after expiry, partial-startup
containment with observed owner joins of the exact known threads);
the real owned resolver child (argv/env/reaping observations,
literal fast path, deadline expiry with terminate/kill/reap, late
and racing completion, controlled call-through delay, controlled
caller interruption during the real start seam before and after
actual child creation); the real
forward setup phases against owned loopback HTTP and TLS
endpoints (stalled TLS handshake, nonreading and slow-reading
upload, the cumulative case where each observed phase fits but the
sum expires at the anchored budget, with generous same-producer
positive controls that reach the actual producer, bounded connect
attempts, the exact forwarded header allowlist); the same actual
proxy answering a healthy request after a failed setup: the
failed request's original deadline is already passed and its
guard actually joined before the later request bytes, and the
healthy request succeeds under its own fresh anchored setup
deadline (not the passed one) - fixed content-free 502 first,
zero engine/corpus/reviewer work, then the exact original
answer; and the real constructor/main default,
override and invalid-before-bind behavior plus real-stack JSON and
paced delayed-SSE integration (useful two-target repair,
no-suspicion zero-review exact bytes, completed-original optional
review failure, failed-message bypass, real non-200 passthrough
with zero work, bounded synthetic canary evidence, default tracing
off), all under finite owned parent supervision where hanging
cases require it. NOT covered: overall
request/wall-clock/CPU/admission/fairness budgeting, post-intake
disconnect detection while main/review runs, remote cancellation,
packaged library/morphology/quality/live qualification, and any
live DNS, service or model.

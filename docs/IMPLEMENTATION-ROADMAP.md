# Roadmap navigation

The controlled [initial roadmap](../oap/strategic-instructions/INITIAL-ROADMAP.md)
holds 56 inert objectives and explicit dependencies. PLAN remains product authority.
000 adopts owner-reviewed published scaffold; 022/044/055 assemble evidence and
request fresh ICA for demonstrator/MVP/service. They never award milestones.
Strategy reconciles and may remap obsolete/oversized work with provenance, preserving
published IDs and unresolved PR state. Completing all rows cannot prove completeness.

Post-recovery engineering scope (012-a/012-b, 2026-10-25): the scoped 012-b
completion round resolved the two 012-a named residuals (native
report-history cache ownership; portable configuration template) and
corrected the 012-a publication-evidence overclaims in
`oap/recovery/012-b-native-migration-completion.md`.
Round 013-a (2026-10-26) implemented the owner-selected Pandoc
structural-parsing proxy for a runnable repair (engineering scope, not
scientific evaluation) in the isolated concept-verification proxy with
exact original spans. Round 014-a (2026-10-26) implemented one bounded
occurrence-addressed reviewer batch (`batch-v1`) in the same runnable
proxy. Round 014-b (2026-10-26) completed the terminal-answer-copy
preflight on the same branch. Round 015-a (2026-10-26) implemented the
explicit text-only Responses request contract (pre-forward request
validation with closed 400 labels, one shared completed-envelope profile
for the nonstreaming JSON and delayed SSE paths, request-local separated
review usage) in the same runnable proxy. Round 016-a (2026-10-27)
implemented the read-only runtime evidence and completed-original
fallback in the same runnable proxy (read-only rollback-journal index
access with exact escaped paths, a bounded header preflight that
rejects non-regular resources without blocking and unsupported journal
formats before any SQLite open, finite per-query busy wait, exact
nonnegative-integer count validation, and completed-original fallback
distinguishing early zero-call failures from late whole-pass aborts
that preserve the actual review attempt and honest usage). Round
017-a (2026-10-27) implemented the UTF-8-safe main body capture with
one elapsed body budget in the same runnable proxy (wire-
fragmentation-safe UTF-8/SSE collection where a body deadline anchored
at collection entry governs declared, close-delimited and chunked
delivery; declared lengths deliver exactly the advertised bytes and
only unknown-length SSE may end at the terminal marker; a bounded
owned chunk-framing state machine; bounded 502 main failures with
zero review calls; keep-alive and buffered-overread preservation;
the header phase is bounded separately below; connection/DNS
deadlines and total wall-clock budgeting remain unfinished). Round
018-a (2026-10-27) implemented the independent elapsed
response-header budget in the same runnable proxy (one absolute
monotonic header deadline anchored before the owned guard starts so
startup overhead is not concealed; the stdlib getresponse parser
retained on the owning thread; an owned pure-timer guard that
interrupts only the exact captured socket and is cancelled and
actually joined on both success and failure; racing or late parser
returns explicitly closed and never transferred; the
CONCEPT_HEADER_TIMEOUT operator value keyword-only after the
existing positional constructor parameters and validated before any
bind allocation; bounded 502 header failures with zero review calls
and zero engine analysis; the CONCEPT_TIMEOUT body budget independent
in both directions; real-TLS and hanging-upstream subprocess
coverage; header-phase DNS/connect deadlines, incoming client
timeouts, admission control and cancellation remain unfinished).
Round 019-a (2026-10-27) implemented one owned elapsed
reviewer-exchange budget in the same runnable proxy (one finite
positive monotonic deadline anchored at review entry covering the
owned child process's startup, the strict versioned IPC, and the
child's actual resolver/connect/TLS/upload/status/header/body work
plus result validation; byte arrival, interim 100 responses, phase
transitions and process startup never reset it; at most one HTTP
attempt in one ordinary owned stdlib child that waits for the
channel's actual EOF before HTTP and compares delivery to the
declared length captured before reading; a late or racing success is
a failure; the exact child is terminated and actually reaped before
return so no owned work outlives the exchange; strict RRTX v1 frames
with explicit finite per-field caps enforced on both encode and
decode; the legacy single-target prompt/API, proposal and envelope
parsing, and acceptance remain byte-identical; reviewer request and
response contracts unchanged). Round 020-a (2026-10-27) implemented
one finite positive monotonic incoming client request intake
deadline in the same runnable proxy (one absolute intake deadline
anchored while handling the accepted connection before any
request-line/header/body read and before the owned intake guard
starts, covering the first byte, the request line, all headers and
the exact advertised body; byte arrival, phase transitions and
legitimate short reads never reset it; strict unambiguous framing
with a fixed content-free 400 for repeated Content-Length fields
even when equal, comma lists, any Transfer-Encoding and any
unsupported Expect, the existing 413 for missing, negative,
overlarge or nondecimal lengths with very large numeric fields
rejected boundedly before integer conversion, and an incomplete
advertised body - even with a complete valid JSON prefix - never
forwarded and closed with a fixed content-free 400; a stalled
intake closes with zero main/analysis/evidence/review work and a
bounded best-effort 408; the owned pure-timer guard interrupts only
the exact accepted client socket and is cancelled and actually
joined on every path including partial startup; trailing bytes
never become a second request; the keyword-only constructor
parameter client_timeout, appended after header_timeout following
the existing positional parameters, takes the CONCEPT_REQUEST_TIMEOUT
operator value (default 30 seconds), validated before any bind
allocation; the deadline is independent of the CONCEPT_TIMEOUT
body/socket, the CONCEPT_HEADER_TIMEOUT header budget and the
15-second reviewer exchange; main DNS/connect/upload, outgoing
delivery, total wall-clock/CPU/admission/fairness budgeting,
post-intake disconnect and cancellation remain unfinished). Round
021-a (2026-10-27) implemented one independent finite elapsed
final response delivery deadline in the same runnable proxy (new
delivery_transport.py module; one absolute monotonic deadline
anchored immediately before final response emission - status line,
headers, body and the actual flush - and before the owned delivery
guard starts, so guard startup is charged to the clock;
response-ready work, including upstream capture and optional
repair, is outside the phase; byte progress, short writes and
phase transitions never reset it; a late or racing completion loses
to expiry, deadline expiry prevents acceptance of late results
while the owned guard thread is cancelled and actually joined
before return with no hard-real-time guarantee; once any response
emission began, no second response, status or fallback is
attempted on that socket and a failed send before bytes is closed
safely without recursive retry; every post-intake response write
is bounded - completed 200 JSON and delayed SSE, unchanged bypass,
actual non-200 upstream status/body preserved, the fixed
content-free contract 400, capture/protocol 502 and existing
generated post-intake errors - and a stalled or slowly reading
client is closed quietly with no body logging, where local send
completion is not proof the peer received or read the bytes; the
owned pure-timer guard interrupts only the exact captured accepted
socket and is cancelled and actually joined on every path
including partial startup, so no delivery work outlives the
response; the keyword-only constructor parameter delivery_timeout,
appended after client_timeout following the existing positional
parameters, takes the CONCEPT_DELIVERY_TIMEOUT operator value
(default 30 seconds), validated before any bind allocation; the
deadline is independent of the intake, header, body/socket and
15-second reviewer budgets; main DNS/connect/upload, overall
request/wall-clock/CPU/admission/fairness budgeting, post-intake
disconnect detection while main/review runs, remote cancellation
and package/morphology/quality/live/ICA/deployment remain
unfinished). Round
022-a (2026-10-28) implemented one independent finite elapsed
main-upstream setup deadline in the same runnable proxy (new
upstream_setup.py module plus the exact repository-local
upstream_worker.py child-side entry; one absolute monotonic
deadline anchored at entry to the owned main forward setup before
any worker/guard/process/IPC startup, resolver call, connect/TLS
or request emission, covering owned transport startup, address
resolution, bounded address attempts, the TCP connection, the TLS
handshake and the entire request write through the last body byte
handed to the local transport; byte progress, short writes,
address attempts and phase transitions never reset it, and every
blocking operation is additionally capped by the remaining
deadline plus a pure timer guard that interrupts only the exact
socket object it currently holds, so a late or racing setup
completion loses to expiry; the noninterruptible stdlib
resolution runs in one owned ordinary finite stdlib child (empty
environment, argv array, no shell, strict versioned bounded frame
protocol over private nonblocking pipes, at most one resolution
attempt, IP-literal hosts never reach the child) that the parent
terminates and actually reaps on expiry; a successful setup
releases its clock before response-header acquisition and the
existing header/body, intake and delivery clocks stay
independent; setup failure is a main failure - the existing fixed
content-free 502 - with zero engine, corpus or reviewer work, and
the same actual proxy recovers on the next healthy request,
which anchors its own fresh setup deadline after the failed
request's original deadline has passed and its guard has been
actually joined (a passed deadline is never accepted); the
keyword-only constructor
parameter setup_timeout, appended after delivery_timeout following
the existing positional parameters, takes the CONCEPT_SETUP_TIMEOUT
operator value (default 30 seconds), validated before any bind
allocation and revalidated at use, and an explicit upstream :0 is
rejected with the full 16-bit port meaning; local write completion
is not peer receipt or model-execution acknowledgment, with no
hard-real-time guarantee; overall request/wall-clock/CPU/admission/
fairness budgeting, post-intake disconnect detection while
main/review runs, remote cancellation and
package/morphology/quality/live/ICA/deployment remain
unfinished). Round
023-a (2026-10-28) completed owned partial-startup cleanup for the
Pandoc and reviewer child starts in the same runnable proxy (no new
deadline; the existing intake, header, body/socket, delivery, setup
and 15-second reviewer clocks are unchanged): with the real Popen
class the exact process object is pre-allocated and parent-owned
before the fallible start can create any child, so a caller
interruption after actual child creation still leaves the child
reachable for group kill and an actual wait/reap (Pandoc owned
session) or terminate, kill escalation and an actual wait/reap
(reviewer); a failed pre-allocation leaks no child and no owned pipe
descriptor (each closed by the single reviewer ownership guard
established before the first pipe allocation); the
never-created state (unset pid) is never signalled or waited on;
ordinary OS errors keep their fixed finite labels and nonordinary
caller control (KeyboardInterrupt, MemoryError) is cleaned first
and re-raised with its original identity; cleanup may honestly wait
for OS reaping, with no hard-real-time return guarantee; the six
inherited Pandoc generic-annotation diagnostics are fixed type-only
(concrete types plus identity-only typing.cast at the call sites;
runtime checks, branches, offsets, data and results preserved);
controlled-fault evidence only, no spontaneous-native-failure,
live-model or quality claim; overall request/wall-clock/CPU/
admission/fairness budgeting, post-intake disconnect detection
while main/review runs, remote cancellation and
package/morphology/quality/live/ICA/deployment remain
unfinished).
Coverage
remap: the runnable
proxy now covers the seed 013-a (versioned targeted-review prompt
serialization), 014-a (strict reviewer-response parsing), 015-a (isolated
reviewer HTTP transport to the configured private endpoint), and 020-a
(completed-text pipeline with at most one review call per eligible answer)
seams. Round 022-a remaps the seed 022 identity to this bounded
main-upstream-setup engineering objective without an ICA request
or milestone label; the original seed 022 demonstrator-evidence
and ICA scope remains unclosed. Round 023-a remaps the numeric 023
identity (the inert 035/042 resource/error seams) to this bounded
owned-startup-cleanup engineering objective on the actual proxy
without an ICA request or milestone label; the original
numeric-023 scope remains unclosed. Those seed objectives (including
the remapped seed 022 and numeric 023) as packaged library/milestone
objectives remain unclosed; following work stays: bounded failure/
admission/cancellation, packaged library integration, morphology/
phrases, measured labelled quality, and independent closure.
A provisional estimate for the remaining packaged-MVP engineering scope is
8-15 focused engineering days. Research-evaluation completion (requiring
separate reconciliation of the evaluation objective on the restored,
integrity-verified 011 inputs; no prior draft activated), packaged MVP, ICA
and deployment remain separate gates.

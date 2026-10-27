# 021-a — Bounded final response delivery on the owned client socket

Status: FINAL. Objective021, rounda; CREATE_NEW_PR.

## Identity

Order oap/orders/021-a-final-delivery.md; final report
oap/reports/021-a-final-delivery.md. Repository ulfe-lmi/llm-slovenian-repair,
default main, exact accepted base e340439e1e92f6a348f897f607a695bdf24d4d8f.
New branch oap/021-final-delivery, one new PR; its number does not yet exist.
Dependency020 accepted for development only.

## Provenance

H: owner continue-development authorization, runnable proxy with mandatory Pandoc
and exact original spans, only existing foreground coding agent. No research restart
or unrelated milestone gates. A: ARCHITECTURE5/13/14/16.1 and LR-001/007/010/011/
013/014. Preserve every LR-001 through LR-014. Original roadmap035/042 bounded
resource/API-failure seams are reconciled to this current proxy. The inert seed021
CLI is neither activated nor declared complete; numeric021 now denotes this coherent
proof-sized delivery objective, not a packaged-library milestone.
E: private021a-final-delivery-baseline-diagnosis.json at the exact accepted base:
real loopback upstream, actual ConceptProxy forward/transform/native write, completed
synthetic JSON7000210bytes below existing8MB capture cap. After intake release the
handler is observed in socketserver.write at proxy.py1258, accepted socket timeout
None; a second actual request waits until the first nonreading client closes, then
returns exact healthy200 on that same proxy. A no-op repair engine is outside the
delivery boundary; no Pandoc, corpus or quality claim. Parent1.335s, all28listedsource
hashes stable and owned fixture threads joined. A finite observation plus inspected
absence of a delivery deadline proves this boundary gap, not an empirically infinite
wait. Nominal .9 in the raw diagnostic is requested .7sleep+.2observation timeout,
not a measured phase duration; do not turn it into a performance claim.

## Current verified state

PR22 merged2026-10-27T17:03:49Z, reviewed report head
b51a714a59d077413de6ff7bf15bc8880b4091b7, normal merge at the exact base above,
parents656920bb/b51 and tree equality verified. Independent469tests/167subtests,
strict4/Ruff4 and all four required final-head CI passed. Native baseline actually
passed fullpytest, static checks, OAP discovery, build, offline install/import and
cleanup. Its report34930bytes/SHA3d2da5cc9dee5124deed23e5ce19debf9782adac5f9de6aeb9bb37c1df133a09
remains immutable/reachable. Remote/local main match, tracked clean before publication.
Response95370 closed after one exactOK. Sole existing coding PID3341327 is idle in
its owner foreground pane. PR13 stays open unchanged at
5b43387b1d72bbc63ceaad4420a17b0edac4c094; leave it untouched. Preserve corpus/,
.research-test-scratch/, .rclone-speed-test/, retained branches/reports, restored
private archive and caches. No reset/clean/stash/history rewrite/cache restoration.

## Governance

Read router, compact coding AGENTS, compact architecture/communication, exact active
order and relevant SECURITY/TESTING contracts. Helpers verify full source identities;
no full PLAN/strategic law/roadmap/research preload. Governance ref
3549de2a436f485a693730d0ee7d5f8c00aec0c0 and metadata's exact16identities were
compared with trusted accepted blobs and current files. No source/projection revision,
no new milestone gate. CRITICAL unchanged with zero actual entries.

## Goal and dependencies

Bound the final response write after response bytes are ready, without keeping the
incoming-intake guard alive through downstream work. One independent finite elapsed
delivery deadline includes status/headers/body/flush and guard startup. A stalled
or disconnected client must not occupy the single-threaded loopback proxy indefinitely.
This does not establish a total request, main connect/upload, CPU or admission budget.

## Scope

New concept-verification/delivery_transport.py if needed and new
concept-verification/tests/test_delivery_transport.py. In proxy.py only new imports,
post-intake response emission/error handling and its owned delivery lifecycle,
constructor validation/appended keyword-only delivery_timeout and normal main wiring
(including the existing optional budget TypedDict) may change. Inspect the actual
stdlib BaseHTTPRequestHandler send_response/end_headers/send_error/finish and
socketserver._SocketWriter.write/flush ownership so no final flush or error retry
escapes the bounded send. Retain standard header serialization, not a new HTTP parser.
config.py adds only CLIENT_DELIVERY_TIMEOUT_SECONDS=30.0 and truthful comments.
Update bounded current claims in README.md, STATUS.md, concept-verification/README.md,
docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md; matching existing
 oap/GENERATED-FILES.json pins only, same173-path set. New order/active, report counter
research/RESEARCH-STATE.md72to73 only, final sole-path report.

## Files and boundaries

Whole-frozen: all existing nine focused test modules; client_transport.py,
header_transport.py, capture_transport.py, review_transport.py/its worker and every
other existing concept Python module except proxy.py/config.py. Frozen proxy:
RepairEngine, JSON/SSE transforms, main forward, write_traces, observe_usage,
handle_error and pure existing functions/classes outside _Handler/ConceptProxy/main/
optional-main-budget TypedDict. The actual intake anchoring/framing/read/exact-body/
release-before-downstream semantics are frozen; do not refactor its guard or parser.
The private021a-reconciliation.json lists original Python hashes/physical sections
and a bounded47-file/nine-pyc cache baseline for independent verification only.

## Non-goals

No server concurrency conversion, queue/admission/fairness, main DNS/connect/TLS/upload
or overall-request/CPU budget, post-intake disconnect detection while main/review is
running, remote model/GPU cancellation, new endpoint/security posture/auth. No Pandoc/
protection/mapping/detection/corpus/acceptance/patcher/prompt/reviewer/request/envelope/
history/usage changes. No dependencies/workflows/governance/package/morphology/
quality/live/ICA/research programme work. Keep loopback-only single-threaded HTTP/1.0
close semantics, fixed limits and default disabled tracing. No actual Qwen/service call.

## Requirements

1. Add independent finite positive CLIENT_DELIVERY_TIMEOUT_SECONDS30.0 default.
   Append keyword-only delivery_timeout AFTER header_timeout/client_timeout without
   reordering/removing any old parameter. Normal main uses CONCEPT_DELIVERY_TIMEOUT;
   unconfigured normal entry and old constructor adapters retain compatible defaults
   (only explicitly configured new optional keyword need be forwarded, realconstructor
   validates default). Reject bool/nonnumeric/nonpositive/nonfinite/huge integer and
   durations unrepresentable by the actual primitive BEFORE bind, then revalidate
   at use. No client header/body override, no disabled/unbounded value. Intake,
   header, body/socket and fixed15s reviewer budgets remain separate.
2. Anchor ONE absolute monotonic deadline immediately before final response emission,
   BEFORE status/headers/body/flush and before the owned guard starts. Response-ready
   work (including upstream capture/optional repair) is outside this phase. Byte
   progress, short writes, phases and internal retries never reset it. A per-write
   idle socket timeout alone is insufficient. Complete normal send plus actual flush
   and cleanup/join must be classified against this one clock: late/racing completion
   loses to expiry. Local kernel acceptance is not proof the peer received/read the
   bytes; do not claim delivery acknowledgment or hard-real-time OS scheduling.
3. Keep writes on their owning handler. If using a timer it owns only a bounded wait
   and shutdown of the EXACT captured accepted socket object, not a numeric FD or
   another connection. Cancel and actually join on success/timeout/disconnect/write/
   flush error/exception/startup failure, including a thread that started and already
   ended before start raises; never join an unstarted thread. Include startup in the
   clock. No daemon/reaper/background delivery or worker remaining after handler return.
   Never leave a guard armed during the next connection or main/repair work.
4. Bound all post-intake response writes: completed200 JSON/delayedSSE, unchanged
   bypass, original non200 upstream status/body, contract400, capture/protocol502 and
   existing generated post-intake errors. Error payload/status semantics and exact
   successful body bytes stay compatible. Existing early parser/path/framing errors
   remain bounded by their existing intake lifecycle, and existing best-effort intake
   errors remain bounded; do not weaken intake to share a broader timer. Explicitly
   document these phase boundaries instead of claiming every HTTP action has one
   global deadline. A delivery timeout/failure closes quietly with no body logging.
   Once any response emission began, do not try a second response/status/502/fallback
   original on that socket, replay main/review, or label a partial body completed.
   A failed send before bytes is also safely closed, not recursively retried.
5. Timely healthy clients receive unchanged body bytes/status/content-type/content-
   length and existing envelope/usage/zero-or-one review behavior. Complete eligible
   main output precedes repair and any answer emission. An actual non200 upstream
   keeps its original status/body, not a blanket502. A healthy main/review phase may
   take longer than the short delivery budget and then deliver successfully: no
   earlier-started delivery guard or residual intake timer may cut it off. Optional
   repair failures still deliver only an already completed original. No callback or
   tracing redesign; do not include their unbounded execution in a delivery claim.
6. Permanent tests exercise actual ConceptProxy handler/native socket writes with
   real loopback main server and client. Prove nonreading client stalls at the named
   write then is closed boundedly without the fixture first closing it, and a slowly
   reading client whose progress would defeat an idle-only timeout still loses to
   the absolute budget. Use finite buffers/large permitted synthetic body, synchronize
   reached producer/write boundary, actually measure elapsed observations, and use a
   generous positive control with the same producer. Cover status/header and body/
   flush/cumulative boundaries where individual measured phases fit but total does
   not; controlled call-through delays clearly separated from native wire proof.
   No claiming partial capture or validation failure as proof delivery was reached.
7. Test successful completion, deadline race/late completion, early disconnect,
   write/flush failure and before-start/after-start/already-ended startup failures.
   Observe actual join of known owned worker/socket identities. On SAME real proxy
   show healthy next request after a stalled send; genuinely late other-connection
   traffic begins only after first guard actually joined and original deadline passed.
   No guard affects a reused/later socket and no duplicate response after partial send.
   A required hanging/slow-reader case runs in an owned finite parent-supervised
   ordinary test process with bounded terminate/kill/reap escape so a bug cannot hang
   CI. All fixture sockets, handlers/producers/servers/processes actually close/join;
   never call shutdown on an unstarted serve_forever fixture.
8. Exercise actual constructor and normal main default/override/invalid-before-bind.
   Actual JSON and delayedSSE integration uses real RepairEngine/Pandoc/tinySQLite/
   ResponsesReviewer and synthetic main/reviewer servers for useful two-target exact
   repair preserving Unicode/combining/code/math/HTML/links, no-suspicion0review and
   safely completed-original fallback. Preserve exact forwarded allowlisted main
   credentials/body and isolated one-review shape/usage; no real auth. Delivery
   failure must not trigger extra downstream work. Test fixed content-free failures
   with permitted fake-key/request/response/exception canaries and bounded captured
   stdout/stderr; default tracing off, no general privacy-certification claim.

## Acceptance criteria

A1: One independent validated30default/normal override delivery clock covers actual
status/header/body/flush, startup charged, no progress reset/late-success acceptance.
A2: Timely exact body/status semantics retained; native stalled and slowly reading
client closes boundedly without duplicate response and same-proxy recovery works.
A3: Every owned delivery guard actually joined with partial-start containment and
exact socket isolation; earlier intake released and downstream may outlast delivery
budget before it starts. A4: All existing469tests/167subtests stay unchanged and pass,
new real integration/negative tests and strict/Ruff pass. A5: Scope, privacy, preserved
sources, documentation, exact report/PR and all four final-head CI before strategic
development merge. Software/synthetictransport/installedPandoc evidence only; not
liveQwen/linguistic/ICA/MVP/deployment evidence.

## Verification

Qualified external Python3.12 -B -m pytest -q -p no:cacheprovider over all existing
nine modules (test_concept, test_pandoc_protection, test_review_batch,
test_responses_contract, test_runtime_corpus, test_capture_transport,
test_header_transport, test_review_transport, test_client_transport) and new
test_delivery_transport. Count tests/subtests separately with exact tested snapshot/
SHA and time. Ruff --no-cache and strict mypy ALL changed Python including newtests,
owned byte-identical shadow/actual imports/minimal strict config/no tests override;
no broad ignore/Any/config relaxation. Focused actual boundary tests before fullsuite.
Frozen strategic-prompt archive3 via unittest, offline research discovery,
rebuild_tables --check, publication_guard --root research; shared accepted-runtime
trusted3549 governance, transcript/history, pins and whitespace. Unchanged
check_whitespace.py at authorized bases2832fa1e51bdf3641aabbd81feab8ddb64a876da and
82ea1e6f4173934fa47bb34ee6a6f78338d3603a plus scoped git diff --check.
Compare listed frozen files/physical sections/current legacy tests against trusted
accepted base; bounded cache hashes/mtime/size only, no restoring/global claim. This
is independent verification evidence, not a new product AST/cache-policy test.
Counter73 anticipates final report; expected pre-report counter failure remains
FAILED and must not be relabelled. Required final-report-head checks: Application
baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history.
Pending/missing/cancelled blocks merge; source tests never imply future-commit CI.

## Local setup and constraints

Only existing foreground agent, exact codex --yolo --profile early-beta restart
ONLY if genuinely dead; no subagents/backgroundAI/model/provider/launcher. Control
consumed once outside model, no second model-side wait. Ordinary finite owned test
processes/threads permitted; no liveQwen. Qualified externalPython3.12.15 and installed
Pandoc3.7.0.2, no historical discovery/fallback. STRATEGIC_HOME/test-scratch-021a
owned disposable setup, umask077/dirs700/files600, -B/PYTHONDONTWRITEBYTECODE,
external TMPDIR/PYCACHEPREFIX/mypycache, pytest cache disabled. No repo .venv/cache
mutation/restoration. Mode-sensitive frozen research fixture may set only its test
process umask022 within private700TMPDIR matchingCI; disclose exact scope and runs.
Only ephemeral loopback ports0, tiny permitted synthetic data/fake keys/owned TLS
trust. No protected Qwen/weights/GPU/vLLM/CUDA/launch/services/occupiedports/network/
VPN/firewall/gateway/auth/profile/neighbor changes. No raw customer/model text or
real secrets in logs/OAP; permitted synthetic test fixtures/bounded private assertion
logs may contain their synthetic data and private paths, not production payloads.

## Documentation

Document phase start/release/error/quietclose/no-second-response and local-send vs
peer-read meaning, delivery30default/override, prior phase budgets unchanged, single-
threaded scope and no hard-real-time claim. Keep unfinished mainDNS/connect/upload,
overall/CPU/admission/fairness/post-intake disconnect detection/remote cancellation/
package/morphology/quality/live/ICA/deployment explicit. No new gates/research restart,
no completion percentage; provisional remaining packaged-MVP estimate8-15 focused
engineering days excludes external evidence/human waits. Same173manifest paths,
matching changed entries only. Research counter72to73 only; registry42/incidents2
and scientific identities unchanged. Historical immutable reports stay intact.

## Git and report publication

Fresh remote/default/base/source/branch/PR checks before mutation; no existing021
branch/PR expected. New named branch from exact accepted base, only ordered scope.
Commit/push non-report work and create actual singlePR before composing report.
Inspect/repair safe in-scope CI without weakening gates; record actual implementation
SHA and literal source identity for working-tree test observations. Prepare private
report draft, shared preflight against actual implementationhead, disclose path/hash/
status/limits and PAUSE before canonical copy/commit/push/response for strategic
semantic review. No responseOK yet, no new work while paused. This same order/control
stays consumed; explicit strategic continuation through the existing pane permits
only exact approved report bytes without a new signal/order/model. Then copy once,
sole-path immutable SELF commit with implementation as soleparent, push samebranch/
PR, shared remoteidentity/bytes/parent/path proof, exact responseOK once. No future
push/CI success in prewritten report; actual post-publication evidence stays private.
No later round mutation/reportrewrite/replay. Coding never merges or enables auto-
merge. Strategy independently checks finalhead/all4CI/strongest counterargument/
rollback/deployment effects before conditional development merge.

## Decision classification

D0 routine reversible finite final socket-write budget within architecture and
loopback development scope. A pure owned timer plus exactsocket interruption, joined
before return, contains the native blocking operation. A per-write idle timeout
still allows indefinite progress, and adding server threads merely multiplies
unbounded work. Strongest counterargument: an absolute30s local-send cap may drop a
legitimate slow consumer after a partial response, and interruptive shutdown can
race completion or affect the next connection if owned incorrectly. Keep a finite
operator-configured duration, no duplicate response, conservative late-result
classification, exact known socket/thread ownership and native stalled/slow-reader/
healthy-after-join tests. This neither promises remote receipt nor establishes all
service resources. Rollback uses a new bounded development PR reversing product/
config/tests/current claims/matchingpins as needed while retaining published immutable
orders/reports/reportcommit evidence and append-only bookkeeping, no wholesale report
removal/history rewrite. No data migration, live service action or human acceptance.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "313d77900f9bbf1c974e76ea3f546083b117eeaac5f5fc2e964e77b3c19b9ccc",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "d10f9a0d673bd84f91a27f4f24b8505bf966e3eb5825bdfbd9404e1385b6681e",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "db624bb41b34d8263bc5745083d86e7db5bb8907816cd8725871e7225eb6ce9d",
    "oap/governance/DISTILLATION-MAP.md": "eeaf84b26e39c1cadd5d375d8d40f21b62bcf607a18472cd426d13656d5d3e62",
    "oap/governance/WORKSPACE-LAYOUT.json": "90f8b69f4054dffb4d93313da54841ccfddafdca511b86604765d51b63631d16",
    "oap/prompts/coding-round.md": "c682b1bbe016429bf4712a4174ae5ca4ec8b78ab36ebbc2c9b3ce625d83d3ffd",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "ba91f90ef1a8692472661900f1f91faacafa1a47954222c0e75e2f9d9752f6ae",
    "oap/strategic-instructions/AGENTS.md": "c08be7ea6f50ff218948e06ca942d40ce370b041f3580035a4f8ae8ef37c8221",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "83c87a5277ca798609422927e47caa2babab2cf555824813cbbe7f4ac2531ea5",
    "oap/strategic-instructions/strategic_model_init_material.md": "ac972d8e5fcd58b263df11d044aafed9fb1017d2173157d829fbc2953a1ba3b6"
  },
  "lr": [
    "LR-001",
    "LR-002",
    "LR-003",
    "LR-004",
    "LR-005",
    "LR-006",
    "LR-007",
    "LR-008",
    "LR-009",
    "LR-010",
    "LR-011",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "id": "021-a",
  "title": "Bounded final response delivery on the owned client socket",
  "objective": "021",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_FINAL_DELIVERY",
  "base_sha": "e340439e1e92f6a348f897f607a695bdf24d4d8f",
  "branch": "oap/021-final-delivery",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "020"
  ],
  "local_work": "Tracked-clean main e340439e1e92f6a348f897f607a695bdf24d4d8f; preserve corpus/, .research-test-scratch/, .rclone-speed-test/, all retained branches/reports/private archive/caches. No reset/clean/stash/history rewrite/cache restoration.",
  "prior_review": "020-a PR22 development merged at e340439e1e92f6a348f897f607a695bdf24d4d8f after independent469tests167subtests/strict4/Ruff4 and all4finalb51CIgreen. Exact remote merge parents/tree and local fast-forward verified; report34930bytes/SHA3d2da5cc9dee5124deed23e5ce19debf9782adac5f9de6aeb9bb37c1df133a09 retained. Response95370 consumed one OK and closed. Existing foreground PID3341327 idle; no replay.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development authorization and runnable-proxy scope; mandatory installed versioned Pandoc/exact original spans, only existing foreground coding agent, no research restart or unrelated milestone gates."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE sections5,13,14,16.1 and LR001/007/010/011/013/014; bounded delivery/failure/ownership seams of original roadmap035/042 remapped to current proxy. Seed021 offline CLI remains unactivated/unclosed."
    },
    {
      "kind": "E",
      "reference": "021a-final-delivery-baseline-diagnosis.json at accepted e340439: actual ConceptProxy forward/transform/native write, real loopback upstream sends7000210-byte completed synthetic JSON. After intake guard released, handler observed blocked in socketserver.write at proxy.py1258, exact accepted socket timeoutNone; second actual request waits until first nonreading client is closed, then same proxy returns exact healthy200. Only no-op repair engine outside delivery boundary; no Pandoc/quality proof. Parent1.335s, stable28sources, joined fixtures; finite observation not proof of infinite empirical wait."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

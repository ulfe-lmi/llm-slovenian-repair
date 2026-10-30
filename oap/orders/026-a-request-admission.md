# 026-a — Bound accepted request admission in the runnable proxy

**FINAL — reconciled against accepted development main.**
Status: FINAL. Protected product agreement and sources unchanged.

## Identity

Repository/default in metadata. One objective/one NEW PR on oap/026-request-admission. Canonical order oap/orders/026-a-request-admission.md; canonical report oap/reports/026-a-request-admission.md. No future PR number fabricated.

## Current verified state

Exact accepted remote/local main: a0b62cb95c9b1f8c89bb567e8c767cf299ef0941. PR27 development merged2026-10-29T23:51:08Z, parentscbffa+931bc77, tree4021efa9f002e625c63ba239b99e98bbd455dfb4 identical reviewed931 and actualCIcheckout5e323c. All4 final931 checks SUCCESS; actual native driver13 commands+cleanupPASS; App39m31s, Bootstrap198PASS, Research409PASS/53SKIP, report history78 valid. No passed full-pytest count inferred from a predecessor. Exact34234-byte aae156e3 report/sole931parentb514/path remotely verified; root shared merge gate and remote/local FF main verified. Owner foreground3341327/%23 remains live and quiescent with exact codex --yolo --profile early-beta, cwd REPO_ROOT, owner-launched home/auth unchanged. Prior025 response32218 CLOSED0/exactONEOK/retired; all earlier readers retired; ordinaryCIwatch62739 CLOSED0 and retired. No new response reader is armed at finalization. No replay or model/CLI/background agent restart. Root will arm exactly one fresh026 receiver before response publication.

026-prework-identities.json captures accepted45source/14oldmodules/42frozen/13oldfrozen, all16 governance hashes/173manifest paths/listed47 unchanged cache identities (old failures retained), exact old-client static baseline and CIworkflow40->50 expected delta. Local tracked-clean main plus three preserved untracked roots. Existing unrelated OPEN PR13 (historical revert branch) is outside this objective; do not mutate/merge/close it. No026 branch/order/report/PR exists. Preserve restored archive/private drafts/histories and every prior test/setup/cache failure; no reset/clean/stash/restore/reseed/amend/force push.

## Provenance

Exact H/A/E/I references are machine-copied below. Private bounded receipts live in STRATEGIC_HOME/workorders/migration-20261025. Read026-prework-identities.json,026-native-server-lifecycle-qualification.json, next-proxy-queued-wait-observation.json and next-proxy-admission-oldtest-static-label.json with its raw baseline as needed. Root's private native lifecycle invocation error (Condition context result treated as the object) is preserved separately; corrected qualification passed. The original026 split-integrity seed remains unclosed. Do not load full strategic law/PLAN/roadmap/future drafts/research archives as routine coding context.

## Governance

All16 full/compact accepted identities are copied below and verified on literal accepted main. Trusted accepted governance revision3549de2a436f485a693730d0ee7d5f8c00aec0c0 remains unchanged. Preserve LR-001 through LR-014 and architectural conditions. No protected source/compact/seed/CRITICAL evolution, private law refresh or DHA append; CRITICAL exact hash a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e, zero actual entries/dispositions. No new human gate or fabricated acceptance.

## Goal and dependencies

Depends on accepted025 and existing mandatory Pandoc/request/evidence/capture contracts.

Explicit finite application-owned admission after TCP accept: one active whole
request handler, a finite number waiting, one anchored waiting deadline, and
bounded pre-main rejection/expiry. No queued request may reach intake, forward,
engine, evidence or review after expiry/closure. Existing accepted response and
phase-budget contracts remain. Kernel backlog time before accept is outside the
new measured clock and must be documented honestly.

## Scope

Existing Python allowlist under concept-verification: config.py, proxy.py and ONLY tests/test_client_transport.py's exact privacy _fail_start helper qualification. Add request_admission.py and tests/test_request_admission.py. Source45->47;14->15 test modules. All42 other existing Python files and13 other old test modules byte-frozen. No unrelated formatting/type cleanup.

In proxy.py change only admission imports, ConceptProxy base/construction and added admission/serve/shutdown/close lifecycle hooks needed by the scoped controller. Preserve existing RepairEngine, _Handler, transform functions, forward, observe_usage, write_traces and main CLI/startup behavior as literal AST boundaries; no incidental MemoryError/engine fallback rewrite. Constructor signature and all existing positional/keyword uses remain compatible; no new public configuration knobs. Safe constructor cleanup for newly owned admission state is in scope. A necessary conflict with a frozen boundary must be brought to strategy with concrete evidence before mutation.

Other allowlist: .github/workflows/application-baseline.yml ONLY existing job timeout40->50 minutes (every other byte frozen); README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md; only affected existing doc pins in oap/GENERATED-FILES.json (same173-path set; application workflow is not pinned there); exact order/active and final sole-path report; research/RESEARCH-STATE.md reviewed-report counter77->78 ONLY. Total report file count78->79 differs because historical007-o is excluded from reviewed count. Registry42/incidents2/scientific identities/history unchanged.

## Non-goals

No research restart, evaluation/data acquisition, model/host/network/credential/service change, deployment/release or milestone/ICA label. No package integration, morphology, phrase/quality calibration, true review-only queue, concurrent main handlers, active-client/remote cancellation, total elapsed/CPU/memory/I/O/fairness guarantee or kernel pre-accept waiting bound. No changes to parser/source mapping, residual protection, detector, evidence/SQLite policy, acceptance/patching, reviewer/process transports, main/client/header/body/setup/delivery phases, supported envelopes or existing deadlines. Keep the original numeric026 calibration/test-split seed unclosed; this order remaps036/042's existing resource seam to the actual runnable proxy.

## Files and boundaries

Read current ConceptProxy construction, synchronous HTTPServer lifecycle,
_Handler.handle/do_POST/finish, main forward/transform/trace/usage boundaries;
qualified Python's actual socketserver acceptance/dispatch/shutdown lifecycle;
existing guard ownership patterns; client-transport privacy start-fault helper
and actual concept-client-intake-guard identity; relevant frozen old tests;
current static and preserved-cache evidence. Coding normal compact read set only;
no requirement to load full strategic law, future drafts or historical research.
Exact source paths and frozen boundaries above. Native stdlib qualification is a bounded private evidence reference; coding may inspect actual installed stdlib lifecycle as required, not old research trees.

## Requirements

R1. Add PROXY_MAX_QUEUED_REQUESTS=16 and PROXY_QUEUE_WAIT_SECONDS=2.0 in config:16 WAITING requests,2.0 seconds accepted-queue waiting, independently of one ACTIVE whole handler. These are finite initial engineering defaults, not measured model optima. Resolve CURRENT config at each real ConceptProxy construction into an immutable owned policy before bind/thread/socket allocation; validation reads no file/model/network/index. No import-time captured-default shortcut. Running instances retain that validated policy; later defaults apply to newly constructed instances, never silent live resizing.
Count is exact positive int. Duration is exact int/float numeric (not bool), finite, positive and representable under native threading.TIMEOUT_MAX; no strings/nonnumeric coercion, None or zero-disable. Reject invalid config with plain ValueError before bind. No new environment/CLI/request/constructor knobs. Tests may patch config BEFORE construction as labelled test-only values. Native Python3.12.15 TIMEOUT_MAX=9223372036.0 and2.0s are qualified in026-native-server-lifecycle-qualification.json. The new admission module is stdlib-only, with no new pydantic/src dependency.

R2. Keep at most one whole handler active per proxy instance. Bound admitted
waiting ownership before starting any request worker; do not create unbounded
ThreadingMixIn workers and check capacity afterwards. Count all waiting/starting
ownership consistently; completed entries must not accumulate in registries.
Active and waiting slots have one exact owner and one release on every outcome. Admit unexpired waiting entries in their accepted order; expired/closed entries cannot block later eligible ones. This is internal accepted-order FIFO, not a tenant/kernel/network fairness claim.
Do not weaken existing loopback-only bind, upstream/config validation or normal
main/review load. Do not duplicate engine buffers per request or open an index
before actual eligible engine use.

R3. Anchor one absolute monotonic queue deadline at accepted dispatch entry,
before admission allocation/thread start/queue work. Startup and waiting overhead
are charged; progress and phase transitions never reset it. At the actual claim
for handler execution, elapsed expiry wins even if a timer wake-up is late/racing.
Queue expiry/full/closing never forwards main or starts engine/review. Deadline equality is expired. The clock starts at accepted dispatch entry before admission allocation and native startup, not at connect/send or a later wait call. Timer or
queue ownership must be released/joined before intake begins; an old deadline may
never shut down a later active/unrelated socket. Intake starts its OWN unchanged
clock after successful admission. The queue clock excludes kernel pre-accept time.

R4. Pre-main queue-full/expiry/closing emits a fixed content-free bounded503 where
possible, then closes that exact accepted connection. Use HTTP503, Content-Type application/json and a fixed error object with type=request_admission_error and code exactly REQUEST_QUEUE_FULL, REQUEST_QUEUE_TIMEOUT or REQUEST_QUEUE_CLOSED as applicable. No reflected identifier or payload. This is a PRE-MAIN rejection, not optional-review fallback
from a completed main and never a fabricated original/success. A client that does
not read must not stall the listener indefinitely; use an explicitly bounded
best-effort/nonblocking rejection path with a finite fixed packet, closing if
complete emission cannot be made. No caller headers/text/exceptions/queue values
in error bodies, logs or metrics. No thread per rejected connection.

R5. Every socket, slot, thread/guard and queue entry is owned before fallible
startup can create/use it. Cover allocation, start-before-creation failure,
start-after-actual-creation interruption, already-ended and never-started states.
On an interrupted start, no handler/main may escape before dispatch ownership is
committed; abort/join the exact known worker first, close only its socket, release
its slot once, preserve exact nonordinary control identity at the actual admission owner boundary after cleanup. Track the current owned operation explicitly; an ambient unrelated except block is not pending ownership/control. Never join a thread
that never started, self-join, scan/kill global processes or use deferred GC/reaper
cleanup. Name and prove any worker-control transfer back to its owner; no default
thread traceback exposing exception content, silent caller-control swallow or
unexpected replacement worker after quit/failure. Preserve existing outer HTTP error semantics; name and test where worker control is transferred to its owning supervisor. No incidental change to admitted engine fallback policy. Normal server shutdown/close
must stop admission, cancel/close waiting entries, release every owned guard and
actually join owned workers before the documented owning close returns. Active
work may take existing cleanup/OS time; no hard-real-time or remote-model-cancel
claim. Do not extend this into active-client cancellation in this round.

R6. Preserve main capture/completion, request contract, exact raw no-edit
JSON/delayed-SSE bodies, mandatory Pandoc exact-original mapping/protection,
read-only evidence budgets and original fallback, one reviewer batch, usage and
patch integrity. Useful admitted repair still works. No stale details/usage or
unapproved slice change across successive/queued requests. Main errors,
incomplete output, capture caps and unsupported envelopes retain existing
failure semantics; queue rejection never relabels them as completed answers.

R7. OLD TEST qualification ONLY: test_client_transport.py's privacy _fail_start
wrapper currently intercepts every threading.Thread.start. Capture the original
start before installing the patch; inject the same failure only for the existing
exact concept-client-intake-guard thread, delegate every other thread to the real
start. Preserve all cases, payloads, statuses, counts, privacy canary and existing
assertions. No skip, sleep/timeout enlargement, fake server/engine or relaxed
validation. Verify this actual intake fault still fires after admission rather
than passing from an earlier admission startup failure. No other old-test edits
unless strategy explicitly reconciles concrete evidence first. Preserve all
literal old assertions as a structural backstop; actual boundary review is required.

R8. Add meaningful focused actual-controller and actual-proxy tests. Native
owned loopback0/thread/socket boundaries, real Pandoc/ROSQLite/ResponsesReviewer,
fake main/review endpoints only. Concurrent fake-main positive control must not
serialize away product queue behavior. All waits/joins have finite supervisors;
held work is released and every known owned resource cleaned on every fixture
outcome. Source hashes literal before/after and later committed-blob mapping.

R9. Accurate docs: selected units/defaults/immutable instance policy, active versus
waiting counts, after-accept clock, independent existing phase clocks, exact
pre-main errors, cleanup and honest OS/reaping limits. Retain unclosed active
cancel/remote cancel/true review-only queue/CPU-total-time/package/quality scope.
Record numeric026 remap and original split-integrity seed unclosed. No queue-based
MVP claim. Update only the five scoped docs and their existing pins/path set.

R10. CI headroom ONLY: accepted025 actual Application baseline took39m31s of
40min (29s remaining). Increase that job limit to finite50min for the added
native admission coverage; retain every command, per-command1800s, required
check name, PR-only trigger, read permission, validation and cleanup. No retry,
skip, disabled test, live access or deployment change. This is CI execution
headroom, not a product latency/CPU budget or measured model throughput.

## Acceptance criteria

A1 real pre-bind policy, finite ownership cap and absolute queue clock.
A2 real full/expiry/late-claim/start-failure paths never reach main or repair and
release their exact ownership; first control identity and shutdown cleanup proven.
A3 normal raw bodies, useful repair, usage isolation and all old contracts pass.
A4 focused/new plus exact old qualified tests, all15 modules/47 source snapshot,
ALL5 strict/Ruff, shared checks/docs/scope and literal committed mapping complete.
A5 exact approved sole-path SELF publication and all4 FINAL report-head CI remain
later evidence; coding COMPLETE never authorizes merge or milestone/deployment.

## Verification

T1 pure policy invalid matrix and real occupied-port constructor differential.
T2 actual native controller capacity (active1,waitingQ), FIFO admission among live
unexpired accepted entries, overfull rejection without extra worker/thread
allocation or upstream access; no unbounded completed registry growth.
T3 accepted waiting expiry while active work remains held; normal readable client
gets exact503/fixed label; nonreader closes boundedly. Actual claim after elapsed
expiry denied even if timer notification was delayed. Expiry/claim/close races
release once and cannot close another request's socket.
T4 native partial worker/guard startup fault matrix, exact ownership and caller
control, no handler escape before commitment, never-started/already-ended cases,
shutdown/close with waiting and active work, actual joins before owner return;
fresh server/request after failed dispatch without leaked slots or delayed timer.
T5 actual proxy one active handler with concurrent fake-upstream positive control;
A held/B queued/C full, B expiry before A release; zero main/review for B/C. Then
healthy fresh request works. Two unexpired admitted requests each preserve exact
raw body/status/content-type and request-local usage; one useful repair followed
by no-suspicion zero/unknown call case proves no state leakage.
T6 supported half-close/framing/400/non200/incomplete/hard-cap/delayed-SSE and all
old tests unchanged, including actual named intake Thread.start failure. Do not
claim post-intake disconnect/remote cancellation from queued-socket closure.
Focused new module plus the bounded old client module; full15 test modules once
per FINAL source epoch with all47 literal hashes. Strict ALL5 in fresh minimal
flat byte-identical shadow/actual imports/follow_imports silent/no test override,
Ruff check --no-cache ALL5. The old client module baseline independently PASSED strict/Ruff on current
accepted-equal bytes (native78138 closed0; exact one-file scope label); no
unrelated type-only allowance is needed. No broad Any/ignores or catches that hide validation/caller-control failures. Cleanup catches must preserve and re-raise the original control after exact owned cleanup; no weakened tests.
Shared accepted-runtime governance/trusted3549, transcript index+literal revision,
report history require-manifest index+revision, both accepted historical whitespace
bases and scoped git diff/cached --check. Required exact final-head checks:
Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP
report history. Missing/pending/cancelled is not passed.

Exact focused command: qualified Python -B -m pytest -p no:cacheprovider -q concept-verification/tests/test_request_admission.py concept-verification/tests/test_client_transport.py. Broader: all concept-verification/tests (all15 modules) once per final Python source epoch, literal all47 before/after/current/committed mapping. ALL5 static targets: config.py, proxy.py, request_admission.py, tests/test_request_admission.py, tests/test_client_transport.py. The one-file old client baseline label supersedes a cloned generic runner scope string; actual commands/output prove only that one old module, not six.

## Local setup and constraints

Qualified Python3.12.15 with -B and explicit bytecode suppression, private700
TMPDIR/PYCACHEPREFIX/cache and umask077 for runtime/test/static/writer commands;
Ruff --no-cache; pytest -p no:cacheprovider. Explicit qualified pinned Pandoc
3.7.0.2 via CONCEPT_PANDOC; no downloads, historical-helper/PATH substitution,
repo cache writes, cache restore/reseed or mode sweeps. Preserve all old failed
cache epochs and exact public history. Only tiny owned synthetic DBs and bounded
owned loopback0 tests; finite known thread/process supervisors and cleanup.
No real texts, raw prompt/response/target/credential logging, live Qwen/GPU,
weights/vLLM/CUDA/service/occupied-port/network/VPN/firewall/gateway/neighbors,
corpus acquisition, scientific rerun, public exposure, licensing or deployment.
Use private026 test scratch; root prework025 receipts are read-only. Every actual runtime/test/static/writer invocation explicitly owns qualified Python-B/bytecode suppression/private environment/umask077. Public report uses logical roots and qualified interpreter version, never current host paths outside WORKSPACE-LAYOUT.json. Finite ordinary helpers/threads/processes are allowed; additional coding models/agents/background panes/codex exec/alternate providers/profiles are not. Adopt ONLY the already-running owner foreground; restart ONLY verified death, exactly the recorded argv. Preserve its launched CODEX_HOME/auth; OAP_ROLE=coding in handoff/helper environment.

## Documentation

Update only the five scoped docs with actual selected defaults, one-active versus16-waiting counts, FIFO/expiry/clock start after accept,503 fixed codes, immutable per-instance policy, bounds/cleanup and honest remaining OS/pre-accept/cancellation/CPU/review-only queue/package/quality scope. Explain numeric026 remap and original split-integrity scope unclosed. Record exact future tested candidate HEAD and later blob mapping rather than inventing future execution SHAs. CI job50min is finite infrastructure headroom (accepted025 used2371 of2400s), not a product latency/CPU/throughput claim. Same173 existing manifest paths; update only affected existing four doc pins; workflow not pinned. Research bookkeeping77->78 only, expected pre-report red78!=77 stays FAILED until actual final-head CI proves clearance.

## Git and report publication

Use literal accepted base a0b62cb95c9b1f8c89bb567e8c767cf299ef0941, branch oap/026-request-admission, CREATE_NEW_PR. Learn actual PR number before report; never invent it. One new branch/PR for a; corrections reuse it. No coding merge,
auto-merge, history rewrite or protected gate override. Push ordinary non-report
work, record literal head, compose PRIVATE report, actual preflight and PAUSE for
root exact-byte semantic approval BEFORE canonical copy/SELF/push/response.
Report distinguishes actual tested HEAD/candidate bytes from later blob mapping,
all failed/setup/nonfinal epochs from final evidence and actual past CI from
future report-head CI. Copy only approved bytes, sole-path SELF/sole parent,
actually shared REMOTE-verify exact head/parent/path/bytes, ONE responseOK to the
single armed reader, then quiesce. Root independent final-head review, all4 green,
strongest reason not to merge/rollback and expected-SHA gate control DEVELOPMENT
merge; no milestone/deployment authority. Do not start a model or another pane.
Report must machine-copy exact order/governance metadata; distinguish PASSED/FAILED/SKIPPED/NOT RUN/BLOCKED/PENDING/MISSING, local/software/native/live/scientific evidence. Record native partial-start/queue/negative-path evidence and all actual failed or non-final epochs. Root approval is of exact private report bytes only; then canonical oap/reports/026-a-request-admission.md, sole-path SELF with literal non-report head as SOLE parent, push same PR, actual shared REMOTE verification and ONE exact ASCII OK on real response FIFO, then quiesce. Do not re-send after root confirms receipt; CLI wrapper action is send (not an extra fifo argument). No future publication/CI claim inside a pre-push report. No coding merge/auto-merge.

## Decision classification

D0 routine bounded accepted-request admission and finite CI headroom inside existing architecture. Keep current serialization/request state and protected host boundaries. No new D1 provisional choice is introduced; no deployment/MVP acceptance. Coding reports any concrete authority conflict to strategy before crossing it.

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
  "id": "026-a",
  "title": "Bound accepted request admission in the runnable proxy",
  "objective": "026",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_REQUEST_ADMISSION",
  "base_sha": "a0b62cb95c9b1f8c89bb567e8c767cf299ef0941",
  "branch": "oap/026-request-admission",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "025"
  ],
  "local_work": "Tracked-clean acceptedA0b62 main; preserve .rclone-speed-test/, .research-test-scratch/, corpus/, restored archive/private histories/drafts and all old failure/cache epochs; no destructive history/cache operations.",
  "prior_review": "PR27 accepted development mergeA0b62 at2026-10-29T23:51:08Z, exactparentsCBFFA+931/tree4021efa9 equalsreviewed931/CIcheckout5e323c; all4finalchecksSUCCESS; actualnative13commands+cleanupPASS; exact34234Baae156e3 report931 soleparentb514/solepath/REMOTEverified; rootgate and remote+localFF mainverified; response32218CLOSED0ONEOKretired; ordinarywatch62739CLOSED0retired; no deployment/MVP claim.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development / mandatory exact-original-span Pandoc / only existing foreground coding agent / no research restart or unrelated milestone gates."
    },
    {
      "kind": "A",
      "reference": "PLAN13.1 finite queue waiting and13.3 fallback/cancellation; ARCH5 ownership and14 finite resources; inert036/042 resource seams. Original026 split-integrity seed remains unclosed."
    },
    {
      "kind": "E",
      "reference": "next-proxy-queued-wait-observation.json: actual serial ConceptProxy, sent second request waited2.5002s behind held firstmain; concurrent directfake positive distinguishes bottleneck; both then200/raw exact/review0/knownthreadsjoined/DB45sourceunchanged."
    },
    {
      "kind": "I",
      "reference": "026-native-server-lifecycle-qualification.json actualPython3.12.15/Condition wait/TIMEOUT_MAX/neverstarted join rejected/endedjoinvalid/owned actualthread after-start MemoryError+KI reaped and identities retained. Native API/source qualification only, not product implementation success."
    },
    {
      "kind": "I",
      "reference": "next-proxy-admission-oldtest-static-label.json actualone oldclientmodule strict/RuffPASS/45stable; existing globalThread.start privacyfault would precede intake after newdispatch, so narrowly retain actualnamedintakefault+ALLoldassertions."
    },
    {
      "kind": "E",
      "reference": "025a-final-ci-completed-checkout-proof.json finalApp actual39m31s within40min,29sheadroom; orderONLYjob40->50 for newnativecoverage, no commands/percommand1800/checks/triggers/permissions change."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

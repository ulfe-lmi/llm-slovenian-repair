# 022-a — Bound main-upstream setup before response acquisition

Status: FINAL. Objective 022, round a; CREATE_NEW_PR.

## Identity

Order oap/orders/022-a-upstream-setup.md; final report
oap/reports/022-a-upstream-setup.md. Repository ulfe-lmi/llm-slovenian-repair,
default main, accepted base 606f63c8b2049a03d9b0b0cc53abd751ccd00289.
New branch oap/022-upstream-setup, one new PR; number not yet assigned.
Dependency 021 accepted for development only.

## Provenance

H: owner continuation authorization, runnable proxy scope with mandatory installed
Pandoc and exact original spans; only the existing foreground coding agent; no
research restart or unrelated milestone gates. A: ARCHITECTURE §§5,13,14,16.1 and
LR-001/005/007/010/011/013/014; preserve all LR-001 through LR-014. The resource
and API-failure seams of inert seeds 035/042 are remapped to this actual proxy.
The inert seed 022 demonstrator/ICA request is neither activated nor declared
complete; this numeric objective is engineering only, not milestone closure.
E: private 022a-setup-boundary-diagnostic.json/.py on the exact accepted base:
actual ConceptProxy.forward with an owned synthetic loopback upstream, capture/
socket and header budgets each 0.05 seconds. Baseline succeeds in 0.001414 seconds.
Controlled call-through 0.25-second getaddrinfo delay succeeds in 0.251673 seconds;
controlled call-through request-body send delay succeeds in 0.251436 seconds.
Three exact synthetic responses, owned server joined, all Python source hashes
stable. These controlled probes establish which phases the existing clocks omit,
not native DNS failure, total resource qualification or empirical infinite waiting.

## Current verified state

PR23 merged 2026-10-27T20:55:35Z at the exact base above; merge parents
e340439e1e92f6a348f897f607a695bdf24d4d8f and
3a59440362e55c8fda0d88b22fd08b9b409414d1, merged tree identical to reviewed head.
Independent unchanged-source 510 tests/181 subtests, strict4/Ruff4 and all four
final-head CI succeeded. Immutable report 38527 bytes, SHA256
a59823e2132cb67e541daf2422bb7c4b2ffaef867082a9d13fdc7551e538ff75.
Remote/local main match; tracked clean before publication. Its one response was
consumed, reader closed; no replay. Existing foreground coding PID3341327 remains
alive/idle with exact owner argv. PR13 remains open at
5b43387b1d72bbc63ceaad4420a17b0edac4c094; leave it untouched. Pandoc PR15 is an
accepted ancestor; do not redo that implementation or migration 012-a/012-b.
Preserve corpus/, .research-test-scratch/, .rclone-speed-test/, all retained branches,
immutable orders/reports, restored private archive and configurations. No reset,
clean, stash, history rewrite or cache restoration. Prior 021 preservation check
remains FAILED for seven of its 47 listed local cache files; current bytes were
preserved and all47 later stable. Do not hide, restore or reseed that incident.

## Governance

Normal read set: root router, compact coding AGENTS, compact architecture and
communication, this exact active order, relevant SECURITY/TESTING. Helpers check
full source hashes without loading full PLAN/strategic law/roadmap/research.
Trusted governance ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0; metadata carries
the unchanged accepted16 source identities. No source/projection or workflow
revision and no new gate. CRITICAL remains unchanged with zero actual entries.

## Goal and dependencies

Give the main upstream's preparation/request-upload phase one finite positive
elapsed budget. Cover owned execution startup, resolver, address attempts, TCP
connection, TLS handshake and the entire request write before response acquisition.
Keep the accepted header/body deadlines independent and preserve completed-capture,
optional-repair and exact delivery contracts. This is not overall request/CPU,
admission/fairness, disconnect detection or remote inference cancellation.

## Scope

Add concept-verification/upstream_setup.py and, only if necessary for bounded owned
subprocess isolation, concept-verification/upstream_worker.py. Add
concept-verification/tests/test_upstream_setup.py. In proxy.py change only imports,
ConceptProxy constructor validation, forward's preparation/transport lifecycle,
normal main wiring and its optional-budget TypedDict. Add only
MAIN_SETUP_TIMEOUT_SECONDS = 30.0 and truthful phase comments in config.py.
Update current bounded claims in README.md, STATUS.md, concept-verification/README.md,
docs/READINESS.md and docs/IMPLEMENTATION-ROADMAP.md, matching existing manifest pins
only with the same173 path set. Order/active, report counter73 to74 only in
research/RESEARCH-STATE.md, then final sole-path report.

## Files and boundaries

Whole-frozen: all ten existing focused test modules, all existing transport modules
and reviewer worker, every other existing concept Python module except proxy.py/
config.py. Frozen proxy: the entire _Handler, RepairEngine, Forwarded and other
existing dataclasses, JSON/SSE transforms, all pure existing functions except main,
write_traces/observe_usage/handle_error and every ConceptProxy method except
__init__/forward. Existing response-header/body parsing, intake and delivery guard
implementations and their phase anchors remain unchanged. They must still be the
actual path, whether transport ownership stays in the handler or an owned ordinary
child. A narrowly necessary child import of those frozen modules is allowed, not
duplicating or replacing their parsers. No unrestricted refactor.

## Non-goals

No Pandoc/protection/mapping/corpus/detection/acceptance/patcher/prompt/reviewer/
request/envelope/history/usage changes. No concurrency conversion, new queue or
admission policy, remote cancel API, retry, endpoint, new dependency, library
packaging, morphology, quality, live model, ICA or research programme. Keep the
single-threaded loopback-only HTTP/1.0 close policy and default disabled tracing.
No protected Qwen/service/network/auth/profile or neighboring repository change.
No external DNS/service qualification: synthetic owned loopback resources only.

## Requirements

1. Add MAIN_SETUP_TIMEOUT_SECONDS30.0 as the independent initial engineering default.
   Append keyword-only setup_timeout AFTER header_timeout/client_timeout/
   delivery_timeout without reordering existing parameters. Wire CONCEPT_SETUP_TIMEOUT
   at normal main; only forward the new optional keyword when explicitly configured
   so old adapters retain their default compatibility. The actual constructor always
   validates the default before bind. Reject bool/nonnumeric/nonpositive/nonfinite/
   huge integers and durations unrepresentable by the selected wait primitive before
   bind and validate again at use. No unlimited/disabled/client-controlled budget.
2. Anchor ONE absolute monotonic setup deadline on entry to the owned main forward
   setup, BEFORE any worker/guard/process/IPC startup, resolver call, connect/TLS or
   request emission. Cover the entire request through the last body byte handed to
   the local transport. Startup, multiple addresses, partial writes, progress and
   phase transitions never reset it. A per-operation socket timeout alone is
   insufficient; late/racing setup completion loses to expiration. Local write
   completion is not peer receipt or model execution acknowledgment. No hard-real-
   time scheduling claim. Existing CONCEPT_TIMEOUT socket/body, header, reviewer,
   incoming-intake and final-delivery axes remain separate; a successful setup
   releases its clock before actual response-header acquisition, then the existing
   header/body clocks run as before.
3. Use a mechanism that can actually interrupt every potentially blocking phase,
   including resolver and TLS, and leaves no owned work after forward returns.
   Investigate stdlib ownership before choosing the smallest contained design:
   existing owned-process reviewer transport is precedent, not permission to change
   it; bounded resolver-only child plus deadline-aware native transport is another
   possible design. A timer cannot interrupt getaddrinfo merely by closing a socket
   that does not exist, and timing out a Future/daemon thread does not cancel it.
   If a child owns complete main capture because live TLS cannot safely transfer,
   retain actual frozen header/body functions and supervise distinct phases without
   borrowing or resetting their budgets. Bound every new IPC read/write/result
   transfer and startup/cleanup path; no unbounded post-phase result wait. Explain
   the actual additional transfer bound rather than silently changing phase claims.
   No worker, resolver, timer, socket, descriptor, callback, child or reaper thread
   may outlive its owned forward. Actually cancel/join or terminate/kill/reap the
   exact object on success, timeout, exception, caller interruption and partial
   startup, including started/already-ended cases. No global socket shutdown,
   numeric-FD reuse hazard, background wait/reaper or join-timeout-and-abandon.
4. Any child is an ordinary finite stdlib process, never AI. Use argv arrays, no
   shell, no secrets/body/request data in argv/env/tempfiles/logs. A private strict
   versioned bounded IPC, minimal explicit environment and inherited-descriptor
   hygiene must reject malformed/truncated/extra/oversize/nonfinite/duplicate or
   wrong-kind frames before using data. Preserve configured TLS trust without
   weakening verification. Bound fields, address counts, body and output by actual
   existing API/capture limits. A fake resolver/child seam is only unit evidence;
   exercise the actual production parent/child boundary as well. No retries beyond
   legitimate bounded address attempts; never replay a POST after partial upload.
5. Setup failure is a main failure: existing fixed content-free502, zero engine
   analysis/corpus/reviewer and no fabricated completed original or partial output.
   Preserve timely exact upstream status/body/content-type and actual non200
   passthrough; preserve forwarded allowlisted headers/credentials/body and isolated
   reviewer credentials. Healthy response-header/body or review work may outlast a
   short successful setup budget; no residual setup guard may cut it off. Existing
   intake and delivery semantics, complete main-before-repair and exact untouched
   slices/zero-or-one review/usage/fallback contracts remain intact.
6. Add focused actual-boundary tests: controlled call-through resolver delays,
   address attempts/connect, TLS handshake, request headers and request-body write,
   cumulative work where each phase fits but the sum expires, late/racing success,
   startup before/after start and all owned cleanup. Name controlled phase evidence
   separately from real wire tests. Native owned loopback tests must reach a real
   stalled TLS handshake and a real nonreading/slowly reading upstream request
   upload, not fail on client intake or a mocked whole forward. Use bounded socket
   buffers/permitted request sizes and synchronization to prove the named phase was
   reached. Progress must not reset the deadline. Use a same-producer generous-
   budget positive control; the fixture must not close the blocker before the proxy
   enforces its timeout. Native connect-hang/DNS claims require corresponding real
   evidence; otherwise honestly label controlled probes, not live qualification.
7. On the SAME actual proxy show a healthy request after a failed setup, with the
   first owned worker already reaped/joined and its original deadline passed before
   later traffic; no old guard affects another socket/request. Demonstrate actual
   owned identities, not merely active-thread counts. Required hanging/slow-upload
   cases run in finite parent-supervised ordinary test processes with bounded
   terminate/kill/reap escape so failures cannot hang CI. Close all fixture sockets,
   servers, handlers and producers; actually join them, never shutdown an unstarted
   serve_forever. Keep producer exceptions observed and positive controls useful.
8. Exercise actual constructor/normal main default, override and invalid-before-
   bind. Actual HTTP JSON and delayed-SSE integration uses real RepairEngine,
   qualified Pandoc, tiny synthetic SQLite and ResponsesReviewer with owned main/
   review servers for useful two-target exact repair preserving Unicode/combining/
   code/math/HTML/links. Include no-suspicion zero-review, completed-original optional
   failure, real non200 passthrough, exact allowlisted main credentials/body and
   isolated one-review shape/usage. Cover synthetic key/request/response/exception
   canaries with bounded stdout/stderr capture and default tracing off; no general
   privacy, real-model or linguistic-quality certification claim.

## Acceptance criteria

A1: One independently validated30default/operator setup clock covers actual startup,
DNS/connect/TLS/request-write; no per-phase reset or late success. A2: Main failure
returns fixed502 with zero repair/review; healthy status/body and independent existing
header/body/intake/delivery contracts retained. A3: Owned work actually terminated/
joined/reaped on all paths, native TLS/upload stalls and same-proxy late recovery
proved with positive controls. A4: All existing510tests/181subtests unchanged/pass;
new focused integration/negative suite, strict typing and Ruff pass. A5: Exact scope,
source preservation, honest documentation/report/CI and no protected-host crossing.
This is software/synthetic transport/installed-Pandoc evidence only.

## Verification

Use qualified external Python3.12 -B -m pytest -q -p no:cacheprovider on all existing
ten modules: test_concept, test_pandoc_protection, test_review_batch,
test_responses_contract, test_runtime_corpus, test_capture_transport,
test_header_transport, test_review_transport, test_client_transport,
test_delivery_transport; add test_upstream_setup. Focused new tests first, then one
unchanged-source full pass. Count tests/subtests distinctly, literal tested snapshot/
SHA and duration. Ruff --no-cache and strict mypy on ALL changed Python including
new tests/optional worker using byte-identical private shadow and actual imports,
minimal strict config with no broad test override/ignore/Any/config relaxation.
Frozen strategic-prompt archive3 via unittest; offline research discovery,
rebuild_tables --check, publication_guard --root research. Shared accepted-runtime
governance/trusted3549, transcript/history, pins, check_whitespace.py at its authorized
bases2832fa1e51bdf3641aabbd81feab8ddb64a876da and
82ea1e6f4173934fa47bb34ee6a6f78338d3603a plus scoped git diff --check. Compare frozen
files and actual proxy sections to accepted606. Never overwrite old cache evidence.
Counter74 anticipates the final report; expected pre-report count failure stays
FAILED, not retrospectively green. Required final-report-head CI: Application
baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history.
Missing/pending/cancelled blocks strategic development merge.

## Local setup and constraints

Only the existing owner foreground agent, exact codex --yolo --profile early-beta
restart ONLY if genuinely dead. No subagents/backgroundAI/codex exec/new profile/
provider/model/pane. OAP_ROLE=coding explicit in handoff/helper environment; control
consumed once outside model, no second model-side wait. Keep owner-launched CODEX_HOME.
Ordinary finite owned test/runtime transport children and timer threads allowed.
Qualified external Python3.12.15; installed pinned Pandoc3.7.0.2, no historical
discovery/fallback. Disposable STRATEGIC_HOME/test-scratch-022a, strict umask077,
dirs700/files600, -B/PYTHONDONTWRITEBYTECODE=1 for EVERY Python diagnostic/import/
helper as well as tests; external TMPDIR/PYTHONPYCACHEPREFIX/mypycache and disabled
pytest/Ruff caches. No repository .venv/cache mutation or restoration. Mode-sensitive
frozen research tests may use test-process-only umask022 inside a private700 TMPDIR
matching CI, disclosing scope/runs. Only owned ephemeral loopback ports0, synthetic
fixtures/fake keys/owned TLS trust. No real Qwen, weights, quantization, vLLM/CUDA,
launch, GPU, services/occupied ports/network/VPN/firewall/gateway/credentials/auth/
profiles/neighboring repositories. No raw customer/model text or real credentials in
logs/OAP. Bounded private test assertions may show only permitted synthetic data.

## Documentation

Document actual mechanism, setup phase start/release, independent30default/override,
failure/cleanup and IPC bounds if used, unchanged header/body/intake/delivery axes,
local write vs peer receipt, single-threaded scope and no hard-real-time guarantee.
Keep overall wall-clock/CPU/admission/fairness, post-intake disconnect detection,
remote cancellation, packaging/morphology/quality/live/ICA/deployment unproven.
Record seed022 remap to this bounded engineering objective without an ICA request
or milestone label. Retain provisional remaining packaged-MVP estimate8–15 focused
engineering days excluding external data/rights/labels/live/human waits; no invented
completion percentage. Same173 manifest path set; changed pins only. Research
counter73to74 only, registry42/incidents2/scientific identities unchanged. No edits
to immutable historical orders/reports or protected accepted sources.

## Git and report publication

Refresh remote/default/base/branch/PR before mutation. Create named branch from exact
accepted606; one new PR, number learned after actual creation. Commit/push non-report
work including exact published order/active. Inspect/repair safe in-scope CI without
weakening checks; record literal implementation SHA and snapshot identities for
working-tree tests. Prepare private draft, run shared preflight against actual head,
then PAUSE before canonical report copy/commit/push/response for strategic semantic
review. Give draft path/bytes/hash/status/limits; no response OK or next work yet.
Same order/control remains consumed; explicit continuation through existing pane
permits only exact approved bytes, no new signal/order/model. Then copy once, sole-
path immutable SELF report commit with implementation as sole parent, push same PR,
shared actual remote identity/bytes/parent/path verification, one exact response OK.
Prewritten report cannot claim future push/final-head CI; actual later evidence stays
private. No report rewrite/amend, later mutation/push/replay, merge or auto-merge.
Strategy reviews exact final head, all4 CI, risks/strongest counterargument/rollback
and merge deployment effects before any conditional development merge.

## Decision classification

D0: routine reversible owned setup/resource-bound implementation within established
architecture and contained loopback development scope. Idle socket timeouts omit
resolver and allow cumulative work; broad server concurrency only multiplies that
work. A socket-only timer has no resolver socket to interrupt. A bounded owned child
can contain noninterruptible stdlib resolution but adds IPC, startup and cleanup;
resolver-only isolation plus interruptible socket phases avoids transferring a live
TLS connection but requires precise ownership across transitions. Choose the
smallest design that proves all phases and cleanup; document the actual alternative
comparison. Strongest counterargument: absolute30s may reject a slow legitimate
request, and new transport ownership/IPC can leak credentials, orphan blocking work,
race setup completion or disturb frozen capture/TLS semantics. Mitigate with finite
operator configuration, fail-closed late results, strict private IPC/minimal env if
used, actual ownership/cleanup, TLS trust, native positive/negative tests and all
frozen integration tests. No security posture or human product agreement changes.
Rollback is a new bounded forward development PR reversing this setup/config/test/
current-doc delta and matching pins while retaining immutable orders/reports,
report-commit evidence and append-only bookkeeping. No live service/data migration,
reset/clean/history rewrite/cache restoration or human milestone acceptance.

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
  "id": "022-a",
  "title": "Bound main-upstream setup before response acquisition",
  "objective": "022",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_UPSTREAM_SETUP",
  "base_sha": "606f63c8b2049a03d9b0b0cc53abd751ccd00289",
  "branch": "oap/022-upstream-setup",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "021"
  ],
  "local_work": "Tracked-clean accepted606 main; preserve corpus/, .research-test-scratch/, .rclone-speed-test/, retained branches/orders/reports/restored private archive/configs/caches. Prior021 cache-preservationFAILED7/47 remains honest and immutable; do not restore/reseed. No reset/clean/stash/history rewrite.",
  "prior_review": "021-a PR23 development merged606 after independent510tests181subtests/strict4/Ruff4 and all4final3a594CIgreen; parents/tree/defaultmain/localFF verified. Immutable38527-byte report/a598 retained. Sole021response consumed and reader closed; existing foreground3341327 idle, no replay.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development authorization; runnable proxy with mandatory installed versioned Pandoc/exact original spans; existing foreground coding agent only, no research restart/unrelated milestone gates."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE5/13/14/16.1 and LR001/005/007/010/011/013/014; resource/API-failure seams of inert seeds035/042 remapped to actual proxy. Seed022 demonstratorICA request remains unactivated/unclosed."
    },
    {
      "kind": "E",
      "reference": "Private022a-setup-boundary-diagnostic.json/.py at accepted606: actual ConceptProxy.forward, owned loopback upstream, capture/socket+header budgets.05 each; baseline.001414s, controlled call-through resolver.25s succeeds.251673s, requestbody-send.25s succeeds.251436s. Exact three responses/stable Python source hashes/joined fixtures. Controlled phase-gap proof, not native DNS or live qualification."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

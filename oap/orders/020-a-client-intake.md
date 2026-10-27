# 020-a — Bounded client request intake and exact body capture

Status: FINAL. Objective020, rounda; CREATE_NEW_PR.

## Identity

Order oap/orders/020-a-client-intake.md; final report oap/reports/020-a-client-intake.md.
Repository ulfe-lmi/llm-slovenian-repair; default main; accepted exact base
656920bbdb845174d93839b07be75cff964d17c2. Branch oap/020-client-intake,
CREATE_NEW_PR; no PR number exists yet. Dependency019 is accepted development.

## Provenance

H: owner continue-development authorization and runnable proxy scope; mandatory
Pandoc, exact original spans, only existing foreground coding agent. No research
restart or unrelated milestone gates. A: ARCHITECTURE13/14/16.1 and LR-001,
LR-010/011/013/014 require bounded transport, no incomplete request masquerading
as valid work, and truthful evidence. All LR-001 through LR-014 remain preserved.
The initial roadmap's resource/API failure seams035/038/042 are reconciled here
against the actual proxy; the original seed020 packaged pipeline is not activated
or declared complete by reusing numeric020 for this current coherent objective.
E: private020a-ingress-baseline-probe.json at exact merged base, stable proxy
318e5494b819c126dac61fd3b4a3044b897960fcb98f172dce2a93ce7122e2d7:
actual accepted socket/parser/read on ConceptProxy waits beyond .35s for each
idle accepted connection, partial request line, partial header and stalled body,
despite .1s upstream body/header settings. After fixture EOF, a complete valid
store:false request JSON, advertised11bytes longer than actual, is forwarded once
and returns200. Only post-validation outbound forwarding was replaced by a counter;
this proves intake/validation, not actual upstream/engine integration. All finite
probe threads joined. An earlier probe omitted required store:false and its final
assertion FAILED; the corrected permitted fixture produced the above evidence.

## Current verified state

Remote and local main are656920bbdb845174d93839b07be75cff964d17c2, exact reviewed
PR21 tree, tracked clean before this publication. PR21 merged normally at
2026-10-27T13:03:36Z, reviewed report head9ab3b7a43e249973856a52322b102349cc9f1065;
414tests/160subtests, strict6/Ruff6 and all four final-head CI passed. Its exact
report remains33062bytes/SHA672d59dcb771c91e722db4f155085e11b9a8648a74e64f5e570616bf3d6af37e.
Receipt019a-development-merge-verified.json contains independent review/merge/local
proof. Response69981 closed after one exactOK; no019 replay. Sole existing coding
process is idle in its owner foreground pane, same exact permitted argv.
Preserve retained branches/reports, corpus/, .research-test-scratch/,
.rclone-speed-test/, restored private archive and existing caches. No reset, clean,
stash, history rewrite, cache restoration or unrelated cleanup. PR13 remains open
at5b43387b1d72bbc63ceaad4420a17b0edac4c094 and is unrelated; leave untouched.

## Governance

Read router, compact coding law, compact architecture/communication, exact active
order and relevant SECURITY/TESTING contracts. Helpers verify full source hashes;
do not load full strategic law/PLAN/roadmap/research programme into coding context.
Accepted governance ref3549de2a436f485a693730d0ee7d5f8c00aec0c0; exact current
16 identities in metadata verified against that trusted base. No governance or
projection/source revision, no new gate. CRITICAL byte-identical, zero live entries.

## Goal and dependencies

After accepted019, bound incoming client request intake before ANY upstream,
engine/evidence or review work. An incomplete advertised body is never forwarded,
even when its prefix is syntactically complete supported JSON. This closes one
concrete runnable-proxy resource/integrity gap and does not establish all MVP
resources, disconnect/cancellation, packaged-library or deployment readiness.

## Scope

New concept-verification/client_transport.py if needed and new
concept-verification/tests/test_client_transport.py. In proxy.py only imports,
accepted-connection/handler intake ownership lifecycle and do_POST request framing/
body-read/release boundaries, constructor validation and appended keyword-only
client_timeout, and normal main client-timeout wiring may change. In config.py
add CLIENT_REQUEST_TIMEOUT_SECONDS=30.0 with accurate bounded-intake comment.
No existing value changes. Update bounded current claims in root README.md,
STATUS.md, concept-verification/README.md, docs/READINESS.md and
 docs/IMPLEMENTATION-ROADMAP.md; only directly matching existing
 oap/GENERATED-FILES.json pins, same173-path set. New order/active and the actual
research/RESEARCH-STATE.md report counter71to72 only; final sole-path report.

## Non-goals

No threading/concurrency server conversion, queue/admission/fairness, outgoing
client delivery deadline, main DNS/connect/upload or whole-request/CPU deadline,
post-intake disconnect/remote GPU cancellation, new endpoint/auth/security posture,
model/service/packaging/morphology/quality/live/ICA/research programme work.
No Pandoc mapping/protection/detector/corpus/acceptance/patching changes. Main
forward/header/body transport, reviewer/worker/prompt/batch/request JSON contract,
JSON/SSE transforms, RepairEngine and existing eight focused test files are frozen.
No new dependencies/workflows/source-law/config/auth changes, no actual Qwen call.
The constructor remains loopback-only and single-threaded with existing HTTP/1.0
close semantics; no advertised keepalive, chunked client-body or Expect support.

## Files and boundaries

Inspect proxy._Handler and ConceptProxy ownership, existing header_transport and
capture_transport as reference only, config.py, responses_contract.py, and the
existing eight focused modules. Read actual stdlib BaseHTTPRequestHandler intake
control flow to place the guard around request line, headers and body, including
EOF and error paths. Existing stdlib finite line/header-count guards remain.
Name exact original source sections and compare to the accepted base. Do not
replace stdlib request parser, lower old tests, or mutate frozen helpers to fit
new tests. The private baseline probe is metadata evidence only, not a runtime
resource. Use actual runtime paths for new acceptance tests.

## Requirements

1. One finite positive monotonic incoming-intake deadline, anchored when handling
   the accepted connection BEFORE any request-line/header/body read and before
   guard startup. It covers waiting for first byte, request line, all headers and
   exact advertised body. Byte arrival, phase transition or legitimate short reads
   never reset it. State clearly that OS accept backlog waiting is outside scope.
   Default CLIENT_REQUEST_TIMEOUT_SECONDS30s; append keyword-only client_timeout
   after existing header_timeout without reordering/removing prior parameters.
   Normal main reads CONCEPT_REQUEST_TIMEOUT with the named default. Reject bool,
   nonnumeric, zero, negative, NaN/infinite settings BEFORE binding any socket.
   It is independent of CONCEPT_TIMEOUT, CONCEPT_HEADER_TIMEOUT and fixed15s
   reviewer budget. No request header/body override and no unbounded setting.
2. Retain stdlib request-line/header parsing; one owned interrupt mechanism may
   shut down only the EXACT accepted socket object to unblock waiting reads.
   No DNS, subprocess or AI is needed for incoming loopback socket ownership.
   If a timer/guard/thread is used, cancel and actually join it on EVERY success,
   EOF, timeout, unsupported method/path, framing rejection, parse failure,
   exception or startup failure. No worker survives intake. Include startup in
   clock, handle partial startup safely, never leave a daemon/reaper/helper behind
   or close a later/reused numeric FD. Check clock after apparent read success;
   late/racing completion loses to expiry and can never reach main. Keep CPU inputs
   finite; no hard-real-time OS scheduling guarantee. Timer joins/cleanup are real,
   not a bounded wait followed by an alive guard.
3. For supported POST require unambiguous finite decimal Content-Length within
   existing API_MAX_REQUEST_BYTES2,000,000. Retain413 for missing/negative/overlarge
   lengths as existing bounded size policy; nondecimal malformed length may use
   that policy. Reject repeated Content-Length fields (even equal), comma lists,
   any Transfer-Encoding or unsupported Expect before body forwarding, with a
   fixed content-free400 error and connection close. Do not accept chunked framing
   or silently pick the first conflicting length. Ordinary header whitespace is
   parsed under a documented strict ASCII decimal policy. Very large numeric
   fields must reject boundedly rather than escape integer conversion. Do not
   alter validate_request JSON/envelope/capability policy.
4. Read exactly the advertised length, within that one intake deadline and hard
   byte cap. EOF with fewer bytes is a fixed400 incomplete-request error where
   delivery is possible and always closes; complete valid JSON prefix is NOT a
   complete advertised body. Timeout closes connection with zero main/analysis/
   evidence/review calls: before an HTTP request line is safely available a quiet
   close is sufficient; if safe, a bounded best-effort408 may be sent, but do not
   block indefinitely trying to send an error on an interrupted connection. No
   raw exceptions, request/credential/header/text in logs or OAP artifacts. Body
   bytes beyond the one advertised request must never become a second upstream
   request; retain current HTTP/1.0 close behavior, no pipelining implementation.
5. After complete timely capture, release/join the intake guard BEFORE request
   validation/owner.forward/engine work. It must not fire later during legitimate
   slow main/review work or interrupt another connection. Main status/body errors,
   capture/protocol502, ineligible response bypass, exact optional-failure original,
   usage/history/auth/metadata and zero/one-review semantics remain unchanged.
   An actual non200 upstream retains its original HTTP status and body; never turn
   it into a blanket502. No repair before complete eligible main output. Complete
   bytes and all existing constructors/main valid defaults remain compatible.
6. Actual socket integration tests must cover idle accepted client, partial/dripped
   request line, partial/dripped headers, stalled/dripped body; cumulative line+
   headers+body where EACH actual measured phase is below budget but total exceeds
   it; generous positive control with same producer and short failure; completion
   after expiry; early EOF with a complete valid JSON prefix advertised+11;
   malformed/duplicate/conflicting/comma lengths, unsupported transfer/expect,
   missing/negative/overlimit bounds and full exactly-advertised body. Confirm
   fixtures reached claimed producer phase; synchronize actual completion before
   reading timestamps/counters, and join all owned handlers/producers before reuse.
   Do not infer phase time only from requested sleeps, or let failure be merely
   because expensive startup consumed all of a tiny positive budget.
7. Exercise real ConceptProxy, RepairEngine, Pandoc, SQLite and ResponsesReviewer
   with synthetic loopback main/review servers for JSON and delayed SSE: useful
   two-target exact-span repair preserving Unicode/combining/code/math/HTML/links,
   no-suspicion0review, incomplete/timeout ingress0main0engine0review, then a healthy
   next request on the SAME proxy. Include a complete timely intake followed by
   downstream work longer than the intake budget that still succeeds, proving
   guard release. Preserve exact main forwarded bytes/allowlisted credentials and
   private isolated review shape/usage. Observe owned guard completion and exact
   socket isolation, not just a response status or disappearance from ps; known
   owned thread/socket identities only. Do not scan unrelated processes.
8. Test actual constructor and normal main wiring/default/override/rejection before
   bind, not a copied test-only constructor. Fakes outside the boundary under claim
   can inject startup/read delays or failures, clearly labelled as controlled
   orchestration proof. At least one slow-client/hanging boundary must run in an
   owned finite parent-supervised test subprocess with kill/reap escape so a bug
   cannot hang CI. Test privacy with permitted synthetic canaries, resource cleanup
   on success/failure and independent connection isolation with genuinely late
   traffic. Existing eight focused test modules stay byte-identical. Compare all
   frozen sources/sections and any bounded cache baseline to trusted accepted base;
   never restore caches or generalize a bounded observation to every host file.

## Acceptance criteria

A1: Actual single intake deadline covers first byte/request line/headers/exact body,
no reset/late forwarding, validated30default/normal override independent downstream.
A2: Incomplete/ambiguous/unsupported framing reaches zero main/evidence/analysis/
review calls, bounded close and same-proxy recovery. A3: All owned intake guard work
joined before downstream/return, no other-socket effect; healthy main/review work
may outlast intake budget after its release. A4: All old414tests/160subtests pass
unchanged plus actual new integration/negative/constructor proofs. A5: Truthful
scope/docs/status/timing/source evidence, no privacy/protected-host crossing and
all four final-report-head checks green before any strategic development merge.

## Verification

Qualified Python3.12 -B -m pytest -q -p no:cacheprovider over old eight modules
(test_concept, test_pandoc_protection, test_review_batch, test_responses_contract,
 test_runtime_corpus, test_capture_transport, test_header_transport,
 test_review_transport) and new test_client_transport. Separate actual test counts
and subtest counts, status/timing/tested SHA. Ruff --no-cache ALL changed Python
including tests; strict mypy on ALL changed Python in owned byte-identical shadow
with actual concept/src/repository imports, minimalstrict config/no tests override,
unchanged imports silent. No broad ignores/Any casts to hide errors.
Frozen strategic-prompt archive3 via unittest from repository root; offline research
discovery, rebuild_tables --check, publication_guard --root research; shared
accepted-runtime governance, transcript/history, whitespace/pins. Use actual helper
--help/forms; check_whitespace.py EXISTS and must remain unchanged, two authorized
historical bases2832fa1e51bdf3641aabbd81feab8ddb64a876da and
82ea1e6f4173934fa47bb34ee6a6f78338d3603a, plus current scoped git diff --check.
Expected prepared counter failure before report stays FAILED; do not relabel it
passed after publication. Dirty-source tests need literal later committed blob
identity, not a fabricated execution at that later SHA. Named required final head
CI: Application baseline, Research reproducibility, OAP bootstrap acceptance,
OAP report history. Missing/pending/cancelled is not green and blocks merge.

## Local setup and constraints

Only sole existing foreground agent; exact codex --yolo --profile early-beta may
restart ONLY if genuinely dead, never for compaction/quietness/observation timeout.
No subagent/background codex exec/other model/provider/launcher. Control consumed
once outside model; do not wait on it again. Ordinary finite test processes/threads
are permitted runtime fixtures and must be joined/reaped. No live Qwen/services.
Qualified external Python3.12.15 and explicitly installed Pandoc3.7.0.2, no searches
in historical research directories. New owned STRATEGIC_HOME/test-scratch-020a,
umask077, dirs700/files600; -B/PYTHONDONTWRITEBYTECODE, external PYCACHEPREFIX,
TMPDIR and mypy cache, pytest cache disabled. No repo .venv/cache mutation or
restoration; use ast.parse rather than py_compile. Mode-sensitive frozen research
fixture may set only its test process umask022 inside private700 TMPDIR matching
CI; disclose actual separate failed/success runs. Only ephemeral loopback ports0,
tiny synthetic corpus, fake-key canaries and owned ephemeral TLS fixtures/trust.
No protected Qwen/GPU/weights/CUDA/vLLM/launch/services/occupied ports/network/VPN/
firewall/gateway/auth/profile/neighbor-repository modifications or real data rights
assumptions. Runtime/report content-free; permitted synthetic fixture source and
bounded private synthetic assertion logs may include fixture data/private paths,
not raw customer text or real secrets. No blanket all-host/private-files claim.

## Documentation

Document exact incoming30s/default/override/start/release/error/close contract and
strict request framing, and single-threaded scope. Keep explicit unfinished main
DNS/connect/upload, outgoing delivery, overall/CPU/admission/fairness/post-intake
disconnect/remote-cancellation/package/morphology/quality/live/ICA/deployment work.
No performance optimum/quality milestone from synthetic tests. Update relevant
current claims; retain historical truth rather than rewrite old reports. Remaining
packaged-MVP estimate8-15 focused engineering days remains provisional; no invented
percentage. GENERATED-FILES same173-path set, matching changed entries only.
Research machine block counter71to72 only, registry42/incidents2/scientific identity
unchanged. No research evaluation restart or any new milestone gate.

## Git and report publication

Revalidate exact remote main/base/source identities/no existing020branch or PR,
preserve unrelated work; create named branch from accepted base and carry only
ordered order/active changes. Commit/push non-report scope; create actual singlePR
before report and inspect/repair in-scope CI without disabling gates. Capture real
implementation SHA and actual command observations. Prepare private report draft,
run shared preflight against actual implementation head, show path/hash/status/
remaining risks and PAUSE before canonical report copy/commit/push/response for
strategic semantic review. No responseOK at this checkpoint. Same order/control
remains consumed; root may continue exact approved bytes through this existing
pane without another order/FIFO signal/model. No new work while paused.
After explicit continuation, copy exact approved report once, sole-path immutable
SELF commit with literal implementation as sole parent, push same branch/PR,
shared remote identity/bytes/parent/path proof and exact responseOK once. No later
mutation/replay/report rewrite. Prewritten report cannot claim future push/CI
success; actual post-publication observations belong in private strategic receipts.
Coding never merges or enables auto-merge. Strategy reviews actual final head,
all four CI, deployment effects, risk/rollback and conditional development merge.

## Decision classification

D0 ordinary bounded socket intake/complete-body integrity under existing delegated
architecture; no new trust/public surface or production/service action. Strongest
counterargument: a timer around stdlib parsing adds socket/thread lifecycle races,
and a fixed30s intake budget may reject a legitimate slow local upload. Choose
one configurable finite budget with exact-owned-socket shutdown, joined guard,
late-result rejection, strict framing and actual healthy-after-timeout/downstream
independence tests. A per-read idle timeout would still admit indefinite drips;
server threading alone moves unbounded work into more threads and broadens scope.
This reversible development choice neither certifies target throughput nor changes
the loopback-only proxy into a deployed service. Rollback is a reviewed normal
revert PR; no database migration, protected service or data changes to undo.
No D2 action or human acceptance is authored.

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
  "id": "020-a",
  "title": "Bounded client request intake and exact body capture",
  "objective": "020",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_CLIENT_INTAKE",
  "base_sha": "656920bbdb845174d93839b07be75cff964d17c2",
  "branch": "oap/020-client-intake",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "019"
  ],
  "local_work": "Tracked-clean main at 656920bbdb845174d93839b07be75cff964d17c2; preserve corpus/, .research-test-scratch/, .rclone-speed-test/, retained branches/reports and private archive/caches. No reset/clean/stash/history rewrite/cache restoration.",
  "prior_review": "PR21 development merged at656920bb after independent414tests160subtests/strict6/Ruff6, all4final9ab3CIgreen, exact reviewed tree/parents/default and local fast-forward verified. Receipt019a-development-merge-verified.json; report unchanged672d59dc/33062bytes. Sole response69981 closed after exactOK; coding idle3341327, no replay.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development authorization, runnable proxy with mandatory Pandoc/exact original spans and sole existing foreground coding agent; no research restart or unrelated milestone gates."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE sections13,14,16.1; LR001,010,011,013,014. Initial-roadmap resource/failure/API seed035/038/042 seams remapped to current proxy only; no packaged milestone closure."
    },
    {
      "kind": "E",
      "reference": "020a-ingress-baseline-probe.json at exact merged656920bb, stable proxy318e5494; actual accepted socket/BaseHTTPRequestHandler/parser/read. Idle/partial line/partial header/body stall all still waiting after .35s with configured .1s main body/header budgets; declaredbody valid store:false JSON short11 forwarded once after EOF (200), zero forwarding before EOF. Only post-validation outbound forward replaced with counter; not actual upstream integration or quality proof."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

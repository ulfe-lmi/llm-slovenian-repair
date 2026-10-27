# 018-a — Independent elapsed response-header budget

Status: FINAL. Objective018; CREATE_NEW_PR; phase RUNNABLE_PROXY_RESPONSE_HEADER_BUDGET.

## Identity

018-a; FINAL; repository ulfe-lmi/llm-slovenian-repair, default main; verified base
29ae4c1424da1140026796f7ef6129c11531106e; new branch oap/018-response-header-budget.
No branch PR exists at finalization; create one, never invent its number.

## Provenance

H: owner continuation, runnable proxy, mandatory installed Pandoc and exact
original spans, only the existing foreground coding agent, no research restart
or unrelated milestone gate. A: ARCHITECTURE13–14 capture/resource/failure contract,
all LR-001–LR-014. E/I: actual published017 header-phase observation below.

## Current verified state

PR19/017-a is accepted for continued development at the exact base above:
normal merge2026-10-27T04:49:35Z, parentsfcec700+147832e, mergedtree exactly reviewed
147832e. Independent316PASS107subtests, 28stablePythonfiles, strict4/Ruff4,
frozen19 sources/pins173; all4finalheadCIgreen (Application22m12s, bootstrap16m32s,
research30s, history8s). Remote SELF report verified: soleparent2205f76 andsolepath,
SHA25632accc32c9f0e733f763a3c1cd31fe505ccfbbf472eee1655b1474f3b316c2a3.
Its grouped pre-report research status is qualified publicly/privately as
FAILED1(expectedcount), SKIPPED53, despite PASSED group label; finalresearch passed.
Do not repeat that overstatement. Generic helper counts include007-o while the
research counter explicitly excludes007-o; compare compatible count scopes.
No deployment, quality or milestone acceptance. Governance remains accepted3549de2.

Localmain is trackedclean; preserve the three unrelated untracked directories,
all history/retained branches/old orders/reports, existing caches and restored
private archive. Reader50124 is CLOSED, exact responseOK already consumed once.
Do not replay017. Sole owner-launched foreground process3341327/%23, shell3338200,
exact argv codex --yolo --profile early-beta is live and idle.

## Governance

Read the tiny repository router, compact coding law, compact architecture,
compact communication, exact active order and relevant local contracts. Full
ARCHITECTURE13–14 is the only bounded full-source excerpt required here; helpers
verify whole source hashes without printing them. No entire roadmap, future
drafts, PLAN or strategic law in routine coding context. CRITICAL has zero
actual entries; preserve all prior bytes. Refresh actual remote/base/PR facts.

Implement only upstream RESPONSE STATUS/HEADER acquisition after connection.request
has returned. The017 body deadline begins later and remains independent.
Do not claim an end-to-end request deadline or a fix to DNS/connect/upload.

## Goal and dependencies

Dependency017 is verified accepted at the base above. Selected D0 contract:

Give getresponse status/header acquisition one finite positive monotonic elapsed
budget, independent of body/socket and reviewer budgets. Select and document:
- config.MAIN_HEADER_TIMEOUT_SECONDS = 30.0, an initial engineering default;
- ConceptProxy header_timeout keyword-only parameter, appended after existing
  positional parameters, defaulting to that constant, stored as header_timeout;
- normal main() entry reads CONCEPT_HEADER_TIMEOUT with that default.
Keep CONCEPT_TIMEOUT defaults and existing socket/body meanings, and the fixed
reviewer15-second setting. No request-supplied override/bypass.

Retain the standard HTTPConnection/HTTPSConnection and getresponse parser.
Use a small owned deadline guard/helper around that existing parser, interrupting
only its captured owned socket object at expiration. No second manual HTTP
header parser, detached read worker, growing thread pool, per-byte timeout reset
or bare-fd reuse. A contained equivalent may be used only if it preserves those
exact boundaries and proves the elapsed budget/cleanup. Ordinary guard/test
threads/processes are implementation mechanisms, never additional AI agents.

## Scope

Product: concept-verification/proxy.py header acquisition/configuration/ownership;
config.py header default; new header_transport.py.
Tests: new tests/test_header_transport.py. All existing six focused test modules
are READ ONLY; their constructor probes accept kwargs and need no binding change.
Preserve316 tests/107subtests and all meaningful assertions.
Docs: concept README, root README/STATUS, docs/READINESS.md,
docs/IMPLEMENTATION-ROADMAP.md. Bookkeeping: directly affected GENERATED-FILES
pins, exact order/active/report, research/RESEARCH-STATE.md counter68to69 only.

## Non-goals

Freeze capture_transport.py, corpus.py, runtime_corpus.py, detector.py, repair.py,
qwen_client.py, batch_review.py, responses_contract.py, pandoc_protection.py,
protected.py, protection_residuals.py, governed sources and scientific surfaces.
No dependency/workflow/baseline-driver change; no corpus acquisition/research
run/registry update, new API capability, morphology/acceptance/prompt change,
parser substitution, AST rendering, live model or protected host mutation.

## Files and boundaries

Inspect ConceptProxy.__init__/forward/main, the existing getresponse call,
configuration constants, all six retained test modules and their real socket/TLS
fixtures. Header acquisition ends before capture_transport.read_bounded_body.
Keep stdlib parsing, captured socket ownership and isolated reviewer boundaries.

## Requirements

1. Reproduce the header gap before product mutation through actual proxyHTTP,
   real engine/qualifiedPandoc/RuntimeCorpus/ResponsesReviewer and synthetic
   upstreams only. Private receipt018-header-prerequisite-at-017-final.json:
   stable6sourcehashes at147832e (same producttree as mergedbase), fast identical
   headers/body200 at.034/.009s; slow headers plus fastbodyJSON/SSE200 at.534/.576s
   despite socket/body.15; original bytes andzero reviews. New versioned tests
   must prove the actual header boundary, not replace getresponse with a fake.
2. Anchor one monotonic header deadline immediately before getresponse acquisition.
   Slow status/header bytes and legitimate interim100 responses never reset it.
   A socket/inactivity timeout alone is insufficient. Validate the separate
   finite positive header configuration before bind and again at helper use;
   reject bool, nonnumeric, nonfinite andnonpositive values.
3. Preserve stdlib status/header interpretation, HTTP/HTTPS certificate behavior,
   legitimate100-to-final parsing, caller credential forwarding and no reviewer
   credential borrowing, response modes, over-read buffered body, all017 byte/
   Unicode/declared/chunked/keepalive semantics, main error and ownership profiles.
4. Make completion versus expiration explicit, including racing completion:
   expiration is a bounded main failure even if parser returns after interruption.
   Cancel/join the owned guard before any body capture. A fastheader followed by
   body arriving after the header budget but within a generous body budget must
   succeed; no late timer may close it. Also prove slowheaders under a deliberately
   generous header budget plus fastbody under a short body budget still succeed.
5. Header timeout/transport/setup failure means bounded main failure, zero actual
   engine/Pandoc/corpus/detect/reviewer calls. No completed-original optional
   fallback for incomplete main. Observe call-through at engine entry, not only
   HTTP call counts or output-file absence. Close owned response/connection on
   every path; no header guard/read worker outlives acquisition. Test fixtures
   must terminate/join, with finite parent deadlines/kill/reap for blocking cases.
   A guard must never affect another owned connection/request.
6. Preserve useful JSON/SSE two-target repair with one isolated batch and exact
   original spans. Use supported synthetic contexts; actual2/3/4byte Unicode,
   combining text/emoji and protected code/math/HTML/links remain intact. Assert
   actual Unicode bytes in wire fixtures. Unmappable NFC-unstable prose lines
   correctly abstain; place protected decomposed text on a separate paragraph
   when a useful-repair positive requires provable prose. No weaker evidence.
7. Finish Python code/docstring edits before final focused/static/hash verification.
   Keep failures and fixture corrections; identify earliest failing boundary
   before product edits. Publish precise per-command statuses and evidence scope.
   No model startup/research/linguistic/ICA/deployment acceptance inferred.

## Acceptance criteria

A1: actualHTTP and owned authenticatedTLS fast-header positive versus slow
status-line/header-line negatives, generous finite timing tolerance, zero engine/
review before eligible capture; include interim100 deadline and positive control.
A2: header/body budget independence in BOTH directions, buffered over-read,
terminal keepalive, declared framing and useful JSON/SSE repair retained.
A3: expiration/completion races and repeated-request/other-connection isolation;
all owned guards/fixtures terminate; blocking regressions have finite parent
timeout and cleanup. Configuration tests exercise actual constructor/main wiring
without binding the normal fixed service port: only owned loopback port0.
A4: all prior316/107 and old six files unchanged; docs distinguish header phase
from all remaining axes; exact SELF publication and all4finalheadCI gate merge.

## Verification

Run qualified external Python3.12 -B -m pytest -q -p no:cacheprovider on
test_concept.py, test_pandoc_protection.py, test_review_batch.py,
test_responses_contract.py, test_runtime_corpus.py, test_capture_transport.py
and test_header_transport.py in concept-verification/tests.
Run Ruff --no-cache and strict mypy on ALL changed Python (including new test),
owned byte-identical shadow/minimal strict config without tests override,
real concept/src/repository import context, unchanged imports silent only.
Run frozen strategic-prompt archive3 via unittest discovery; offline research
discovery, rebuild_tables --check, publication_guard, shared governance,
transcript/reporthistory, whitespace andpin checks. Record FAILED1(expected
pre-report counter) and SKIPPED53 distinctly if still those observed results;
never call that discovery an unqualified PASS or predict future CI success.
All four exact final report-head checks are required: Application baseline,
Research reproducibility, OAP bootstrap acceptance, OAP report history.

## Local setup and constraints

Only the existing foreground agent/pane; owner argv is the sole permitted
relaunch if actually dead. No background/subagent/new AI or live-process restart.
Dispatcher consumes exact control once OUTSIDE the model; never wait again.
Use qualified external Python3.12.15 and installer-owned official Pandoc3.7.0.2
from private continuation qualification. Resolve host roots from
WORKSPACE-LAYOUT/private runtime; public artifacts use logical roots.
STRATEGIC_HOME/test-scratch-018a is new owned scratch, umask077, dirs700/files600.
PYTHONDONTWRITEBYTECODE=1, -B, fresh owned external PYCACHEPREFIX/TMPDIR;
disable pytest cache explicitly and use external mypy cache. Never py_compile,
reset/clean/stash, restore old caches, change .venv or shared installations.
Use ast.parse for syntax checks. The mode-sensitive frozen research fixture
needs test-process umask022 inside private700 TMPDIR, matching CI; disclose it.
Only synthetic owned ephemeral loopback servers, tiny SQLite and ephemeral TLS
certificates/trust confined to test children. No real service/GPU/network/VPN/
firewall/gateway/credential or neighboring-repository change; no raw text,
headers, prompts/responses, targets/replacements or credentials in public logs.
Private receipts/logs preserve bounded metadata only.

## Documentation

Explain default/constructor/environment header configuration, elapsed header
versus independent body/socket/reviewer settings, stdlib parsing and guard
ownership/cleanup, failure semantics, supported transport and exact spans.
Retain explicit unfinished DNS/connect/upload/incoming-client/reviewer-total/
CPU/admission/fairness/disconnect/cancellation/quality/live/packaging boundaries.
No new milestone gate or research programme. Do not claim no host-specific path
while printing one; use logical paths and content-free diagnostics.

## Git and report publication

Verify main/base and no existing018 branch PR; create the named branch from
the exact base, preserve all unrelated work and retained branches. Commit
implementation/docs/order/active/pins/counter, capture literal implementationSHA,
push and create ONE actualPR before final report. Report source identities,
numbered criteria, positive/negative/setup/provenance/limits and per-command
PASSED/FAILED/SKIPPED/NOT RUN/BLOCKED/PENDING/MISSING at tested source identity.
Pre-commit test bytes may be attributed to a later implementation commit ONLY
with recorded exact blob equivalence, never as a fabricated later-SHA rerun.
Final report is immutable sole-path SELF commit with that sole parent. Push,
shared remote verify, then exact responseOK once. No later mutation without a
corrective order. Coding never merges or enables auto-merge. Strategy owns
independent final-head review and conditional expected-SHA development merge.

## Decision classification

D0: reversible independent response-header resource bound within architecture.
No D1 or D2 action authorized. Critical register remains unchanged.
Development merge is separate from deployment, licensing and human acceptance.

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
  "id": "018-a",
  "title": "Independent elapsed response-header budget",
  "objective": "018",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_RESPONSE_HEADER_BUDGET",
  "base_sha": "29ae4c1424da1140026796f7ef6129c11531106e",
  "branch": "oap/018-response-header-budget",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "017"
  ],
  "local_work": "Trackedmainclean at29ae4c1424da1140026796f7ef6129c11531106e. Preserve existingbranches/orders/reports, untrackedcorpus/, .research-test-scratch/, .rclone-speed-test/ andignored environments/caches/private restored archive. Noreset/clean/stash/historyrewrite.",
  "prior_review": "PR19 normally merged2026-10-27T04:49:35Z to29ae4c1424da1140026796f7ef6129c11531106e, parentsfcec700+147832e; tree exactly reviewed147832e. Independent316PASS107subtests/28stablePython, strict4/Ruff4, frozen19/pins173. All4final147CIgreen: Application22m12s, bootstrap16m32s, research30s, history8s. SELF147832e solepath report/soleparent2205f76; reportSHA25632accc32c9f0e733f763a3c1cd31fe505ccfbbf472eee1655b1474f3b316c2a3. Sharedremote/report/merge gates and independent semantic review passed. Grouped pre-report research PASSED label qualified in public PR/private review as FAILED1 expectedcounter with53skips; finalresearchCIpassed. Generic report count includes007-o; researchcounter explicitly excludesit. Priorreport immutable. Localmainff/trackedclean; featurebranch retained. Reader50124closed/exactOKconsumedonce; coding3341327idle, no replay.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development goal and runnableproxy/Pandoc/exactoriginalspans/soleexistingforegroundagent decisions; no researchrestart or unrelatedmilestonegates."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE13–14/LR001,010,011,013,014 require bounded capture and main failure before optionalanalysis; allLRs preserved. This order closes response-header acquisition only."
    },
    {
      "kind": "E",
      "reference": "018-header-prerequisite-at-017-final.json atpublished147832e, stable6sourcehashes, actualproxyHTTP/realengine/qualifiedPandoc/SQLite/reviewerHTTP withsyntheticupstreams: fastheaders+fastbodyJSON/SSE200/.034/.009s; headerdrips+samefastbody200/.534/.576s atconfiguredsocket/body.15, originalbytes,0reviews."
    },
    {
      "kind": "I",
      "reference": "ConceptProxy.forward calls standard HTTPConnection/HTTPSConnection.getresponse before the017bodycollector. Socketinactivity timeout resets under headerdrips; headerphase is explicitly unfinished in017 docs. Preserve stdlib parsing, add an independent elapsed phase budget."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

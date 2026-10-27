# 016-a — Read-only runtime evidence and completed-original fallback

Status: FINAL. Objective016; CREATE_NEW_PR; phase RUNNABLE_PROXY_EVIDENCE_FALLBACK.

## Identity

016-a; FINAL; objective016; new branch `oap/016-runtime-evidence-fallback`, CREATE_NEW_PR. No future PR number is assigned.

## Provenance

H: owner continuation, runnable-proxy, installed Pandoc and foreground-only decisions. A: ARCHITECTURE4.1/14.2. E/I: actual JSON/SSE diagnostic failures at published015head53a2, whose product tree equals current main: missing/corrupt/incompatible/text counts yield502; missing creates empty file; negative/fractional counts permit repair. Replacement-only corrupt row after one valid proposal leaves a partial edit. Concrete private receipt identities appear below; no scientific/live evidence claimed.

## Current verified state

PR17 merged2026-10-27T00:02:45Z to8d53923145ef0d36d845c6529fec790ccdbec7c2 after exacthead53a2fea08f501150ae191e641a8ac411ecf48302, independent251PASS87subtests/source-equivalence and all4requiredCI SUCCESS. Parents09e4129+53a2; tree exactly reviewedhead. Localmain fast-forwarded/trackedclean; govunchanged3549de2. Sole015response61649closed; no replay. Sameforeground3341327 idle/%23. PR13 OPEN unchanged5b43387b1d72bbc63ceaad4420a17b0edac4c094.

Repository `ulfe-lmi/llm-slovenian-repair`, default `main`, base `8d53923145ef0d36d845c6529fec790ccdbec7c2`. No PR for new branch. Preserve unrelated corpus/, .research-test-scratch/, .rclone-speed-test/, ignored caches/environments and private restoration. Accepted-runtime governance3549de2 unchanged. Doctor with absolute selected paths: valid structure/errors[]; unused automatic-launch auth/loop flags disabled, accepted zero-model foreground dispatch independent of those flags.

## Governance

Read compact coding law/architecture/communication, exact order and relevant local contracts. Only bounded full-source ARCHITECTURE4.1 and14.2 may additionally be read. Helpers verify exact source hashes without dumping full sources. Preserve LR-001–LR-014, mandatory pinned Pandoc, original-span composition, complete-main-first, one isolated batch and separated usage. CRITICAL has zero actual entries; no relevant gate/new debt. Source/compact identities below remain accepted3549de2.

## Goal and dependencies

015 accepted at verified merge. Runtime proxy opens evidence read-only and returns safely completed original on technical access/integrity failure, including late proposal acceptance. Preserve ordinary unavailable evidence semantics and actual review accounting. One bounded engineering PR, no MVP/deployment certification.

## Scope

Allowlist: concept-verification/proxy.py; optional new runtime_corpus.py (one equivalently named runtime-only adapter allowed; report exact path); config.py for finite SQLite busy wait only; relevant existing focused tests and new tests/test_runtime_corpus.py. Docs: concept-verification/README.md and directly affected README.md/STATUS.md/docs/READINESS.md/docs/IMPLEMENTATION-ROADMAP.md statements. Bookkeeping: affected GENERATED-FILES pins, research/RESEARCH-STATE.md counter66→67 only, exact order/active/report. No workflow/driver change required; baseline discovers tests.

## Non-goals

No corpus acquisition/preparation/migration, normalization/statistical policy change, stronger evidence/quality claim, whole-call deadline/admission/cancellation redesign, package migration, research run/registry, liveQwen or deployment. No new milestone gates, parser fallback/AST rendering, raw logging or governance/PLAN/ARCH/CRITICAL edits. Keep corpus.py/detector.py/repair.py and historical reviewer/prompt byte-identical: runtime adapter isolates this engineering fix from frozen research behavior.

## Files and boundaries

Inspect RepairEngine.repair, JSON/SSE handler, Corpus query/count semantics, detector/accept callers, actualHTTP fixtures/observer and named docs. Read tests first. Existing Corpus may be imported/subclassed, not edited. Validate accessed technical data; do not claim full scientific source/normalization/rights qualification. No private archive or production-index scan.

## Requirements

1. Before mutation reproduce missing-index and invalid-count failure through actual proxyHTTP/real engine/Pandoc/SQLite with synthetic upstream/reviewer; separate detection failure from replacement-only late failure. Record tested bytes. Private strategic diagnostics do not replace versioned regression tests.
2. Open existing SQLite index read-only, never create/normalize/write it. Correct URI escaping for Unicode/spaces/#/?; no alternate-file search or immutable=1 assumption. Close handles on success/construction/context failure. Pin/document finite busy wait ≤0.25s; not a total CPU/query deadline. Held exclusive lock degrades within generous finite test deadline.
3. Validate every accessed unigram/ngram/alternatives count before coercion: exact nonnegative integer only. Reject text/NULL/negative/fractional/noninteger storage; no int() repair/truncation or invented zero. Preserve validzero/missing EXACT/CENSORED/UNAVAILABLE and count scopes. Detect accessed incompatible schema/resource failure; no full-index scan or invented version metadata.
4. Isolate known technical evidence errors at optional-engine boundary after complete-main eligibility. Early failure: exact original JSON/SSE bytes,0edits/0reviews. Late failure: abort entire optional pass from immutable original, no earlier applied/accepted edits or stale trace; preserve actual review attempt and known/unknown usage. Dedicated evidence error escapes existing per-proposal generic catch. Do not call late error Pandoc failure or zero reviews. Fixed content-free labels; no SQL/path/value/target/credential reflection. Main errors remain outside this fallback.
5. Ordinary valid missing replacement/context evidence remains individual rejection; independent valid proposal may apply. Healthy fixture useful repair exactly1batch. Bad request cannot poison subsequent healthy request or carry usage/edits across requests.
6. Preserve all main request/capture/completion/ownership/aligned-metadata/protection/patch checks. Invalid request, main error/malformed/incomplete output and hard capture retain established semantics; no broad catch hiding them. Ineligible main never opens evidence. Mandatory Pandoc failure behavior unchanged.

## Acceptance criteria

1. Actual HTTP JSON+delayedSSE cover healthy repair, missing path(still absent), corrupt bytes, incompatible accessed schema, text/NULL/negative/fractional counts and lock contention. Technical early failures return200 exact original/0calls, existing bytes unchanged. Real SQLite tests prove write prohibition, count validation across all query methods, validzero/missing states, escaped path and handle cleanup.
2. Two-proposal actualHTTP test: first valid, second fails queried replacement-only count after review. Both modes return exact original/no accepted edits or trace, actualcalls1 and knownusage11/5/16 retained. Also unknownusage case. Neighboring legitimate missing replacement evidence rejects only that proposal, valid firstedit survives.
3. Same proxy recovers on healthy next request with correct accounting. Synthetic bad-path/count canaries absent from error body/new logs/observer. Reuse old protection/Unicode/code/math/malformedMarkdown/patch/Responses ownership/capability/history/usage assertions. Main errors/incomplete/hardlimit retain own semantics; invalid/ineligible main must not open/create evidence.
4. Governed/frozen scientific sources byte-identical. Accurate docs and report, exact final-head4CI green before strategic merge. No full-corpus semantic compatibility, total deadline or linguistic/MVP claim.

## Verification

ExternalPython3.12 -B -m pytest -q: existing focused test_concept.py, test_pandoc_protection.py, test_review_batch.py, test_responses_contract.py plus new test_runtime_corpus.py, qualified Pandoc and owned caches/TMPDIR. Prior251tests+87subtests retained with meaningful assertions. Named actualHTTP positives/negatives above; fakes outside proxy/engine/SQLite/Pandoc. Ruff --no-cache changedPython; strict mypy changedPython in real import context/owned cache or byte-identical shadow (follow-imports=silent allowed for unchanged legacy modules, no new error ignores). Frozen strategic prompt archive3tests; offline research/rebuild/publication guard; shared transcript/report-history/whitespace and accepted-runtime governance. Four required finalCI names below. Record PASS/FAILED/NOT RUN/PENDING/BLOCKED accurately, dirty-byte hashes matched separately to committed source; no retrospective SHA or live/ICA/quality claim.

## Local setup and constraints

ONLY existing foreground `%23`/3341327, owner argv codex --yolo --profile early-beta. No child/background agent or live-process restart. External dispatcher consumes control once; never wait again. umask077, owned dirs700/files600; no recursive chmod. ExternalPython /home/janezp/envs/llm-slovenian-repair/bin/python; qualified Pandoc /home/janezp/codex-supervision/llm-slovenian-repair/test-scratch-013a/pandoc-verify/prefix/bin/pandoc. New owned test-scratch-016a below STRATEGIC_HOME for fixtures/logs/caches/shadows; PYTHONDONTWRITEBYTECODE=1, fresh external PYTHONPYCACHEPREFIX and -B. Do not py_compile (writes despite-B); ast.parse if needed. No existing .venv/cache mutation/shared installs, protected services/occupiedports/models/network/credentials or restored real data. Tests owned ephemeral loopback/disposable synthetic evidence only. Disclose deviations; preserve historical caches/no restoration claim.

## Documentation

Directly affected runtime statements only: read-only access, technical failure versus valid missing evidence, whole-pass rollback/honest usage and busy wait versus total deadline. Preserve broader limitations. No research registry/milestone label or raw prompts/answers/replacements in reports/logs.

## Git and report publication

Verify actual remote main/base/PR13 and tracked work; create named branch at exact base, one new PR. Implementation commit includes scoped counter/pins/order/active; capture literal SHA. Then immutable concise SELF report sole-path final commit with exact sole implementation parent. Report all criteria/tested bytes/negatives/setup limits and Critical action NONE; future push/finalCI remain PENDING before publication. Push, shared remote verify exactPRhead/reportbytes/parent/path, send exactresponseOK once. No later mutation without corrective order; coding never merges/automerge. Counter66→67 only new report; expected pre-report count-red not product failure. Preserve all branches/ancestry; no reset/clean/stash/forcepush/delete.

## Decision classification

D0. Already governed read-only/failure/evidence contract, contained reversible engineering, no D1 or D2 crossing/rights inference. Report authority conflict to strategy; continue independent safe requirements.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "016-a",
  "title": "Read-only runtime evidence and completed-original fallback",
  "objective": "016",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_EVIDENCE_FALLBACK",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "8d53923145ef0d36d845c6529fec790ccdbec7c2",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "branch": "oap/016-runtime-evidence-fallback",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "015"
  ],
  "local_work": "Trackedmain clean at8d53923145ef0d36d845c6529fec790ccdbec7c2; preserve all retained history/frozen scientific/governance bytes, ignored caches/environments and unrelated corpus/, .research-test-scratch/, .rclone-speed-test/. Restoration stays private.",
  "prior_review": "PR17 merged2026-10-27T00:02:45Z to8d53923145ef0d36d845c6529fec790ccdbec7c2 after exacthead53a2fea08f501150ae191e641a8ac411ecf48302, independent251PASS87subtests/source-equivalence and all4requiredCI SUCCESS. Parents09e4129+53a2; tree exactly reviewedhead. Localmain fast-forwarded/trackedclean; govunchanged3549de2. Sole015response61649closed; no replay. Sameforeground3341327 idle/%23. PR13 OPEN unchanged5b43387b1d72bbc63ceaad4420a17b0edac4c094.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development goal; runnable-proxy scope, mandatory installed Pandoc and existing foreground-only tmux/FIFO decisions."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE4.1 read-only SQLite,14.2 missing/corrupt/incompatible corpus returns degraded completed original; individual proposal failure distinct from technical failure and main/hard-capture errors."
    },
    {
      "kind": "E",
      "reference": "Private continuation-evidence-fallback-http.json actualJSON/SSE at53a2: missing/corrupt/incompatible/textcount yields502; missing creates0-bytefile; negative/fractional counts permitreview/edit. Synthetic disposableindexes only."
    },
    {
      "kind": "I",
      "reference": "Private continuation-late-evidence-failure-http.json actualJSON/SSE at53a2: replacement-only corruptcount after onevalidproposal leaves partialfirstedit; actualreview1/usage11,5,16. Source confirms sqlite3.connect createsfiles and int(count) truncates/coerces."
    }
  ],
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
  "relevant_gates": [],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "decision_class": "D0"
}
```

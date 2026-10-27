# 017-a — UTF-8-safe main body capture with an elapsed body budget

Status: FINAL. Objective017; CREATE_NEW_PR; phase RUNNABLE_PROXY_MAIN_BODY_CAPTURE.

## Identity

017-a; FINAL; objective017; CREATE_NEW_PR on `oap/017-main-body-capture`, base `fcec700488b8194c08ecc97fe48211239453a7ea`. No PR exists for this branch; no future number assigned.

## Provenance

H: owner continuation, runnable proxy, mandatory Pandoc and original spans, sole existing foreground agent. A: ARCHITECTURE13–14 capture/resource/failure contract. E/I: current reviewed588 code reproduces valid split UTF8 SSE failing502 while identical whole bytes succeed, and known-length body drips exceeding0.15s budget (~0.50s). Header-only drips separately exceed that timeout; they remain future work. Exact receipts below; no live/quality/scientific proof.

## Current verified state

Repository `ulfe-lmi/llm-slovenian-repair`, default `main`, verified base `fcec700488b8194c08ecc97fe48211239453a7ea`. PR18 normally merged2026-10-27T02:05:45Z tofcec700488b8194c08ecc97fe48211239453a7ea after exact588604e0cb8628c2995dc36f779dcd52262d5391 all4CI SUCCESS (Application34m40s/OAP12m12s/research28s/history7s), independentstable281PASS107subtests, strict5/Ruff andsource16byteequivalence. Parents8d53923+588604e; mergedtreeexactreviewedhead, localmainfast-forwarded/trackedclean. Governanceunchanged3549de2. Sole016response17093closed/exactOKconsumedonce; no replay. Existingforeground3341327idle/%23,shell3338200,exactownerargv. PR13OPENunchanged5b43387b1d72bbc63ceaad4420a17b0edac4c094. Minor016reportcachecensuswording qualified publiclyinPR18body/private review:47mixedfiles/45unchangedincluding9pyc/2pytestmutatedandpreserved; immutablehistoryintact.

Native doctor: valid structure/errors[]; accepted-runtime3549de2 valid. Unused automatic-launch auth/loop flags remain disabled; accepted foreground dispatcher starts zero models and consumes one exact control outside the existing model. No new order/model/control for016; this is new017 only after accepted merge.

## Governance

Read compact coding law, architecture, communication, exact order and local contracts. Bounded full ARCHITECTURE13–14 is allowed; helpers verify full source hashes without dumping them. Preserve LR-001–LR-014, mandatory pinned Pandoc, exact original spans, completion before optional repair, one isolated batch and separated actual usage. CRITICAL currently has zero actual entries; refresh before publication. No source-law or frozen research edits.

## Goal and dependencies

016 is accepted at the verified merge above. Repair main response BODY collection after headers are available: arbitrary wire fragmentation preserves valid UTF8/SSE, with one elapsed body budget and a separate byte bound. This is one proof-sized component. Header/connection/DNS deadlines, admission/cancellation, whole review/CPU budgets, linguistic/source/live qualification and milestone closure remain unfinished; do not claim an overall HTTP/request deadline.

## Scope

Product: concept-verification/proxy.py collector/framing and finite body-parameter validation; optional new capture_transport.py; config.py only for necessary named finite body constants. Tests: relevant existing focused modules and new tests/test_capture_transport.py. Docs: concept README and directly affected README/STATUS/READINESS/IMPLEMENTATION-ROADMAP. Bookkeeping: affected GENERATED pins, research/RESEARCH-STATE counter67→68 only, exact order/active/report. Existing baseline discovers tests; no workflow, driver or dependency changes.

## Non-goals

No parser substitution, AST rendering, evidence/acceptance/prompt/SQL changes, new API capabilities or global deadline redesign. Preserve corpus.py/detector.py/repair.py/qwen_client.py/pandoc_protection.py/protected.py. No live service/model/GPU/network/credential changes, corpus acquisition, research run/registry or new milestone gates. Preserve016 report, all ancestry and existing caches.

## Files and boundaries

Inspect _bounded_read, _complete_prefix, _split_sse, ConceptProxy.forward and existing capture/buffer-overread/keepalive/hardlimit tests. Fakes belong outside actual proxy/engine/Pandoc/RuntimeCorpus/reviewer HTTP boundaries. Keep supported request/envelope, terminal ownership, metadata/history/usage and016 fallback semantics. The existing collector has different declared-length and unknown-length behavior; preserve valid no-edit bytes and declared framing rather than discarding advertised trailing data at an internal terminal marker.

## Requirements

1. Reproduce both capture failures before mutation through real proxy HTTP and qualified engine/Pandoc/SQLite/reviewer HTTP with synthetic upstreams. Whole versus split identical bytes and fast versus slow body controls must isolate capture before protection. Add versioned regressions; private diagnostics alone are insufficient.
2. Use one finite positive monotonic BODY deadline from collection entry for declared Content-Length, close-delimited and chunked delivery. Byte arrivals must not reset it; blocking reads/waits respect remaining time. Preserve current operator values/defaults unless a concrete reason requires change; reject nonfinite/nonpositive budgets. Keep the raw body byte bound independent of codepoints.
3. Do not decode a partial UTF8 codepoint as malformed merely because a wire chunk ended. Preserve raw bytes, Unicode and CRLF; tolerate split SSE delimiters. Strictly reject genuinely invalid/truncated encoding; no ignore/replacement decoding, normalization, substring recovery or answer regeneration.
4. Preserve valid delayed SSE completion without EOF, HTTP1.1 keepalive, buffered bytes over-read with headers and partial HTTP chunk framing. Honor declared body framing and no-edit byte identity. Keep existing completion, ownership and unsupported-profile guards; no premature delivery on a partial marker.
5. Body timeout, hard limit, premature EOF, incomplete SSE and malformed main remain bounded main failures with zero review calls. Never label truncated output complete or turn main failure into optional original fallback. No CPU/evidence/review before complete eligibility; use call-through observation rather than output-file absence to prove it. Close all owned transport handles. Safely completed optional failures retain016 original/actual usage behavior.
6. Preserve useful JSON/SSE repair with one batch and exact original spans, including protected Unicode/code/math/HTML/links. Preserve client history, credentials, main/reviewer usage and metadata contracts. Retain all existing tests and meaningful assertions.

## Acceptance criteria

1. Actual HTTP known-length JSON/SSE drips exceed the body budget and fail within a generous finite tolerance; fast identical bytes succeed. Close-delimited/chunked bodies obey elapsed and byte limits. Measure the body deadline anchor accurately, separately from headers.
2. Whole versus split-at-each-byte 2/3/4-byte Unicode, combining text/emoji, CRLF and SSE delimiters produce identical valid semantics. No-edit output remains byte-identical; useful two-target repair preserves protected slices. Bad/truncated UTF8 remains502 with zero reviews.
3. Keepalive terminal completion and buffered body work; incomplete events, hard limits and declared-length truncation retain failures. Negative blocking regressions use finite parent deadlines with kill/reap/cleanup. No producer/reviewer threads or tasks outlive the tests.
4. Prior281 tests+107 subtests and frozen/governed sources remain intact. Docs distinguish body versus overall budgets. Report source identities and pre-report counter red accurately; exact report/head/parent/path and four final CI checks gate strategic merge.

## Verification

External Python3.12 -B -m pytest -q -p no:cacheprovider on concept-verification/tests/test_concept.py, test_pandoc_protection.py, test_review_batch.py, test_responses_contract.py, test_runtime_corpus.py and new test_capture_transport.py, qualified Pandoc, owned TMPDIR and fresh external PYCACHEPREFIX with PYTHONDONTWRITEBYTECODE=1. Ruff --no-cache and strict mypy on all changed Python; owned byte-identical shadow with real concept/src/repository import context, unchanged imports follow-imports=silent only. Frozen prompt3; offline research/rebuild/publication guard and shared governance/transcript/history/whitespace/pins. One research permissions fixture needs test-process umask022 matching CI inside private outer TMPDIR; keep logs/role files private. Record PASS/FAILED/NOT RUN/PENDING/BLOCKED distinctly; no later-SHA/live/quality/ICA fiction or weakened assertions.

## Local setup and constraints

Only the verified existing foreground %23/3341327, owner argv codex --yolo --profile early-beta; no background model, subagent, launcher or restart while alive. Dispatcher consumes control once; never wait again. umask077, new owned test-scratch-017a under STRATEGIC_HOME (dirs700/files600). ExternalPython /home/janezp/envs/llm-slovenian-repair/bin/python and qualified Pandoc /home/janezp/codex-supervision/llm-slovenian-repair/test-scratch-013a/pandoc-verify/prefix/bin/pandoc. No .venv/existing cache writes or restoration. Explicitly disable pytest cache; never py_compile (writes despite-B), use ast.parse. Synthetic owned ephemeral loopback fixtures only. Ordinary test children require finite timeout/kill/reap and inherited safe environment; no AI process creation.

## Documentation

Explain UTF8/framing preservation, elapsed body versus byte bounds, terminal/keepalive and main-failure behavior. Retain unresolved global budgets, quality/source/live/packaging limits. No raw text/prompts/targets/replacements/credentials in logs or reports. Finish Python doc edits before final syntax/static/test/source-hash verification.

## Git and report publication

Verify actual remote main/base and no existing017 PR before mutation; create the named branch at the exact verified base, one new PR. Preserve residues and history. Implementation includes counter/pins/order/active; capture literal SHA before concise immutable sole-path SELF report with that sole parent. Report criteria/negative evidence/setup/limits and Critical action NONE; future push/final CI remain PENDING. Push, shared remote verification, exact responseOK once; no later mutation without corrective order. Coding never merges/automerge. Counter67→68 only new report; record anticipated implementation-only count red. No reset/clean/stash/force push/history deletion.

## Decision classification

D0: contained capture/Unicode/resource repair. No D1 or D2 crossing authorized. Report concrete authority conflict while completing safe independent work.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "017-a",
  "title": "UTF-8-safe main body capture with an elapsed body budget",
  "objective": "017",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_MAIN_BODY_CAPTURE",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "fcec700488b8194c08ecc97fe48211239453a7ea",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "branch": "oap/017-main-body-capture",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "016"
  ],
  "local_work": "Verifiedtrackedmainclean atfcec700488b8194c08ecc97fe48211239453a7ea; preserve retainedbranches/orders/reports,3unrelateduntracked corpus/, .research-test-scratch/, .rclone-speed-test/ and existingignored environments/caches/private restoration. No reset/clean/stash or historyrewrite.",
  "prior_review": "PR18 normally merged2026-10-27T02:05:45Z tofcec700488b8194c08ecc97fe48211239453a7ea after exact588604e0cb8628c2995dc36f779dcd52262d5391 all4CI SUCCESS (Application34m40s/OAP12m12s/research28s/history7s), independentstable281PASS107subtests, strict5/Ruff andsource16byteequivalence. Parents8d53923+588604e; mergedtreeexactreviewedhead, localmainfast-forwarded/trackedclean. Governanceunchanged3549de2. Sole016response17093closed/exactOKconsumedonce; no replay. Existingforeground3341327idle/%23,shell3338200,exactownerargv. PR13OPENunchanged5b43387b1d72bbc63ceaad4420a17b0edac4c094. Minor016reportcachecensuswording qualified publiclyinPR18body/private review:47mixedfiles/45unchangedincluding9pyc/2pytestmutatedandpreserved; immutablehistoryintact.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner continue-development goal, runnableproxy/Pandoc/originalspans and soleexistingforegroundcodingagent decisions."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE13 and14: complete main capture before optionalrepair; finite bodycapture bounds; original/error/hardlimit and Unicode/protected structures retain semantics. This proof-sized order does not close all resource budgets."
    },
    {
      "kind": "E",
      "reference": "017-capture-current-head-diagnosis.json: actualproxyHTTP on588604e stable5sourcehashes. KnownlengthJSON/SSE drip returns200~0.495s withbodybudget0.15; samevalidUnicodeSSEwhole200 vs split502 forclose-delimited/chunked producers; all0reviews."
    },
    {
      "kind": "I",
      "reference": "Earliest failure is _bounded_read/_complete_prefix beforePandoc/SQLite/review. Knownlengthbranch usesresponse.read(length) withoutelapsedbudget; per-piece whole-bufferUTF8decode rejects incompletecodepoint beforelaterbytes arrive. Correct producer framing/whole-byte positivecontrols separate capture fromprotection."
    },
    {
      "kind": "I",
      "reference": "017-header-axis-unproven-diagnosis.json: slow headers with fast body exceed0.15s (~0.53\u20130.57s), same final588 code. Header/global deadlines remain explicit future work; this order closes body collection only."
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

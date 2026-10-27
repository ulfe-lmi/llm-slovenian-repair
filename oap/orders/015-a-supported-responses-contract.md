# 015-a — Explicit text Responses contract, completion validation and usage separation

Status: FINAL. Objective015; CREATE_NEW_PR; phase RUNNABLE_PROXY_API_CONTRACT.

## Identity

015-a; FINAL; objective015; CREATE_NEW_PR, with exact branch/base and all required protocol identities below.

## Current verified state

Repository `ulfe-lmi/llm-slovenian-repair`, default `main`, verified base `09e412942a407e94d5d3890d7749c6672e314526`; CREATE_NEW_PR on `oap/015-supported-responses-contract`, no existing PR for that branch and no assigned future number. PR16 normal merge at2026-10-26T21:55:32Z accepted reviewed0842643 after all4requiredCI SUCCESS (Application32m00s, OAP16m28s, research28s, reporthistory5s) and independent focused212PASS12subtests with tested-source hashes matching implementation46c4938. Mergeparents643ce66+0842643 and tree exactly reviewedhead; localmain fast-forwarded and trackedclean. Governance unchanged; accepted-runtime check3549de2 valid. Native doctor reports valid structure/no errors; legacy automatic-launch auth/loop flags remain disabled and are not used by the accepted zero-model foreground dispatcher. Sole priorresponse reader1051 consumedOK/closed; no replay. Existing foregroundCodex3341327 is idle in pane23 with the exact ownerlaunch; no new process. PR13 remains OPEN at5b43387b1d72bbc63ceaad4420a17b0edac4c094. Published014 orders/reports/allancestry retained. Preserve untracked corpus/, .research-test-scratch/, .rclone-speed-test/, ignored environments/caches and restored private evidence.

## Provenance

H: owner continuation goal and mandatory installed Pandoc / foreground-only decisions. A: PLAN11.3–11.4 and ARCHITECTURE13–14. E/I: metadata-only synthetic probes of actual transform_sse at both accepted643ce66 and reviewed0842643 reproduce repair on incomplete/error-bearing final envelopes and preservation of stale aligned metadata. Actual _Handler forwards nonstreaming JSON unchanged and has no request-capability gate. These are existing API gaps, distinct from014 answer identity/copy correction.

## Goal and dependencies

Dependency014 is accepted at the verified merge above. Outcome: one explicit useful text-only `/v1/responses` contract, with nonstreaming JSON as the primary path and the already supported delayed SSE representation retained. Validate main completion before CPU/review, reject unsupported request capabilities before generation, preserve client-managed history and account for main and review usage separately. This is runnable-proxy engineering; not universal Responses/Codex compatibility, linguistic acceptance or deployment.

## Governance

Read compact law/architecture/communication plus this exact order; bounded canonical excerpts ARCHITECTURE12–14 and PLAN11.3–11.4 are permitted to resolve the named contract.

## Files and boundaries

Inspect proxy.py, qwen_client.py, batch_review.py, existing three focused test modules, current direct HTTP composition fixtures and concept README. Do not read full research archives or historical CRITICAL. Exact source/compact identities and required checks appear in metadata; verify them without printing full sources. CRITICAL remains empty unless newly observed otherwise; no new D1 judgment is authorized here.

## Scope

Product allowlist: concept-verification/proxy.py, qwen_client.py (new runtime batch usage only; historical review/prompt/API byte-unchanged), batch_review.py only if a bounded result/usage carrier is necessary, config.py for named finite API limits, optional new pure responses_contract.py, focused test files including optional test_responses_contract.py. Documentation: concept-verification/README.md and directly affected rootREADME/STATUS/readiness/implementation-roadmap statements. Bookkeeping: affected GENERATED-FILES pins, research/RESEARCH-STATE.md counter65→66 only, this exact order/active/final report. The existing baseline driver runs repository-wide pytest and discovers new test modules; no driver/workflow change is authorized. No scientific registry entry.

## Non-goals

Detector, corpus, acceptance policy/morphology/phrases, Pandoc version/mapping/protection, main capture read/deadline implementation, queue/cancellation, framework/async migration, live access, package promotion, historical research replay, external services, new routes, public exposure or deployment. Do not substitute a narrower pass-through-only endpoint for useful repairs. Ordinary unsupported response abstention must not mask main errors or incomplete capture.

## Requirements

1. Reproduce and preserve the supplied pre-fix failures at the exact accepted base before product changes. Validate both the positive ordinary envelope and one-field negatives, with meaningful callback/HTTP call counts. Never infer product failure below a boundary that was not reached. Existing annotations/logprobs examples must align with the original expression so unchanged metadata demonstrably becomes stale after a length-changing edit.

2. Pin a versioned request contract before forwarding. Accept strict JSON object POST `/v1/responses`, a nonempty model name, text input as a string or a client-managed sequence of text-only user/assistant/system/developer messages (document exact accepted string/part shapes), explicit `store:false`, and a boolean stream flag (absent means false). Pin an explicit allowlist of ordinary generation fields with exact types and finite numeric values; no arbitrary object pass-through as a capability policy. Unknown/unsupported fields or shapes, tools/tool results/images, nonempty include/logprob/annotation requests, structured output, background execution, stored conversation, previous_response_id or conversation linkage and multiple-choice requests return bounded content-free 400 before upstream/reviewer. Empty capability lists may be accepted only when explicitly documented and tested. Require store:false rather than silently assuming server storage is off. Invalid UTF8/JSON, duplicate keys, NaN/Infinity/overflow and type mismatches return 400 without upstream. No caller-provided URL, proxy-control header or linkage header can bypass this policy.

3. Forward supported main body/history without mutation. Main protocol authentication remains separate from review: preserve supported incoming main Authorization, do not borrow the reviewer's API key as an implicit main credential, and never copy caller Authorization/history/session/cookies/tools into review. Pin a narrow forwarded header policy that excludes hop-by-hop/internal-control/linkage headers; document it. Do not inspect, rotate or reconfigure real credentials. Synthetic different main/review keys must prove separation through actual HTTP.

4. Implement useful nonstreaming `application/json` repair through the real engine using the same one-answer eligibility policy as SSE. A supported main envelope is a documented Responses object with completed status, absent/null error, exactly one completed assistant message with one plain output_text part and an exact typed nonempty message id; at most one recognized protected reasoning item may precede it. Reasoning and unrelated metadata are never editable. Pin treatment of missing/null status explicitly; contradictory/incomplete markers never permit repair. Unknown output variants, tools/refusals, malformed/inconsistent identity or extra answer parts are never repaired. Parse main JSON and SSE event JSON without duplicate-key, nonfinite-number or coercion ambiguity; invalid syntax/ambiguous fields must never reach repair. This authorizes parsing/validation helpers, not a capture-read/deadline redesign. Malformed main JSON/capture remains a main error under the documented finite HTTP failure contract; a well-formed unsupported or explicitly incomplete/error-bearing envelope is passed through unchanged with zero calls, retaining its original status/finish/error semantics. No successful repair trace is recorded for it.

5. Apply the same completion/error and aligned-metadata rules to the existing delayed SSE path before any callback. Every answer-bearing representation remains subject to014 terminal ownership/copy checks. Annotations with offsets, token logprobs and other recognized aligned metadata on the actual editable answer make the entire answer ineligible before reviewer dispatch; do not drop fields, invent fresh alignment, scan identical-value metadata echoes or claim unknown shapes work. A changed answer never retains stale token/offset data. Preserve main errors, incomplete stream and hard-capture failure semantics; do not wrap capture in optional-repair fallback. Unknown response structures abstain; parser failure cannot enable regex/partial-text repair.

6. Transform only the exact validated answer field(s). For JSON, unchanged/no accepted edit/unsupported/optional-review failure returns byte-identical captured body; changed text serializes only the supported envelope with unrelated values, IDs, usage and protected reasoning preserved. For SSE retain raw-byte no-edit behavior and the validated event references from014; do not substitute JSON under stream:true. Check response content-type against the declared client mode; a mismatch is a documented bounded upstream protocol failure, never a silent mode switch. No string matching to relocate an answer; engine edits remain original-span Pandoc-protected edits.

7. Keep upstream main-generation usage exactly as reported; never replace it with patched-text token counts or add reviewer tokens into it. Carry actual reviewer input/output/total token usage separately through the batch transport/engine and expose a bounded content-free operator observation using an existing seam or a small request-local observation callback, wired to the normal runnable entry point so an operator can observe or enable it without editing source (a bounded content-free stderr record is sufficient); no new HTTP route, metrics service or raw-text log. Observation failure must not change a safely completed answer or hide a main failure. Missing/unavailable/invalid usage stays explicitly unknown, not zero. Preserve exact source scopes and integer/nonnegative/type validation, including bool/nonfinite rejection. Record zero review requests versus one attempted request separately from whether usage is known. Clear request-local usage on every path to prevent previous-request carryover. Do not fabricate usage on timeout/non200/invalid JSON. Do not change the legacy single-target evaluator return/prompt API.

8. Prove next-turn history through two actual supported proxy requests: the client constructs the next request using only the final visible repaired assistant text, and the actual fake main upstream receives that history once, without an extra draft, reviewer prompt/proposals or linkage. The proxy owns no server-side conversation store and does not promise to repair a caller's independently incorrect history. Requests attempting stored chaining are rejected before main generation. This is API software evidence, not live-Qwen state compatibility.

9. Integration proof must run actual ephemeral ConceptProxyHTTP → real RepairEngine/installed Pandoc/tiny SQLite → actual ResponsesReviewerHTTP with fake main/review upstreams outside those boundaries, different synthetic keys and synthetic payloads. Prove both JSON and canonical SSE useful positives with≥2targets/1review, reordered results and protected content; no suspicion/parser failure/unsupported capability/incomplete/error/aligned metadata have zero review calls; malformed second proposal/timeout/non200 return the original after at most1review. Include no-edit raw bytes, preserved metadata/usage, absent reviewer usage, one request with usage followed by no-review/failed request, response-mode mismatch, stored history rejection, duplicate/nonfinite main JSON, observer failure, normal-entry-point observation wiring and the two-turn client history case. Negative request tests assert zero main HTTP calls as well as zero review calls. Bound server waits and join owned fixture threads; no hanging handle_request threads when requests are rejected early.

10. Keep every established protection/patch-integrity and014 terminal-copy/batch assertion. Where old transport fixtures used `{}` or status-less incomplete placeholder envelopes as nominal successes, update only the synthetic input/envelope to the newly declared valid contract while retaining all original behavior assertions; add explicit rejection tests for the old invalid shape. Do not weaken assertions, skip absent Pandoc, replace the named boundary with a mock or run live models. All existing non-API engine tests and frozen prompt tests retain meaning.

## Acceptance criteria

A1 supported JSON and delayed SSE repair useful2targets with one fresh batch and exact original protected spans. A2 unsupported requests fail before main; invalid/completion/metadata responses never reach repair; errors/capture semantics survive. A3 no-edit and optional failure preserve raw bytes, changed fields follow explicit paths and metadata/usage stay valid. A4 actual independent main/review authentication and client-managed two-turn history prove no state leakage. A5 actual separated usage with explicit unknowns and no carryover is visible to an operator without raw logs. A6 all established tests/assertions and all4final-headCI pass; truthful docs/report and immutable prior history.

## Verification

Focused commands use externalPython3.12 -B, REPAIR_ALLOW_LIVE_TESTS=NO and the installed qualified official Pandoc3.7.0.2. Run existing test_review_batch.py/test_concept.py/test_pandoc_protection.py plus the new actual-HTTP contract module. Use Ruff--no-cache and scoped strict mypy with real repository import context, owned scratch/cache and no new broad import ignores. Frozen prompt regression via unittest discovery test_strategic_prompt_archive.py. Required finalheadCI: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history. Dirty-candidate tests retain source hashes and exact attribution; finalhead CI is later evidence, not a prewritten claim. Do not duplicate the long native baseline locally once focused checks pass; required CI supplies it.

## Local setup and constraints

Only the existing foreground pane23 owner-launched Codex3341327; dispatcher consumes the exact control once outside the model. No new model/agent/session/provider, no background coding agent, no live endpoint calls or protected GPU/service/port/network changes. Ephemeral loopback fixtures and bounded helper processes only. OAP_ROLE=coding for helpers; umask077 in fresh shells; externalPython with-B; no bareuvrun or repository.venv/cache mutation. Preserve unrelated local files; never reset/clean/stash/forcepush. No raw customer/research text, prompt/response or credentials in reports/logs; use fake keys, synthetic text and bounded fixed-label diagnostics. Owned private scratch remains private.

## Documentation

Document exact endpoint/request/response profiles, unsupported capability errors, nonstreaming and delayed SSE behavior, status/error policy, aligned metadata abstention, client-owned history, separate usage and unknowns, authentication/header policy and limits. Correct directly affected stale proxy description; frozen research/evaluator protocol remains historical, not silently revised. Preserve provisional MVP estimate and all existing evidence/deployment distinctions.

## Git and report publication

CREATE_NEW_PR from the verified accepted014 merge/default head identified above. Commit allowed non-report paths/order/active, create the single PR, resolve safe in-scope CI, capture literal implementation SHA, then immutable concise SELF report as sole-path final commit with that exact sole parent. Report criteria/checks/SHA/negative boundaries/setup/limits and Critical action NONE; future publication/finalCI remain PENDING before push. Push, shared remote verify exact PR head/report bytes/parent/path, send exact responseOK once, no subsequent mutation for the round. Coding never merges/enables auto-merge. Counter65→66 only for the new final report; expected pre-report count red is not a product failure. All branches/order/report ancestry preserved.

## Decision classification

D0: reversible implementation of the already agreed explicit API, completion, isolation/history and usage contracts. No production exposure, source acquisition, real credential work, intent change or independent-evidence weakening. Report concrete scope/authority problems to strategy while continuing safe work; no invented D1 debt or human acceptance.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "015-a",
  "title": "Explicit text Responses contract, completion validation and usage separation",
  "objective": "015",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_API_CONTRACT",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "09e412942a407e94d5d3890d7749c6672e314526",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "branch": "oap/015-supported-responses-contract",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "014"
  ],
  "local_work": "Verified tracked main clean at09e4129 before publication; preserve all retained branches/orders/reports, protected/frozen scientific and governance sources, ignored environments/caches and unrelated untracked corpus/, .research-test-scratch/, .rclone-speed-test/. Private restoration/evidence stays outside Git.",
  "prior_review": "PR16 normally merged2026-10-26T21:55:32Z to09e412942a407e94d5d3890d7749c6672e314526 after exacthead0842643/all4CI SUCCESS and independent scoped review. Parents643ce66+0842643; tree identical reviewedhead. Localmain fast-forwarded, governance unchanged/accepted-runtime3549de2 valid; sole014bresponse1051closed; foreground3341327idle; PR13untouched.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner active continuation goal, runnable-proxy/Pandoc decision and foreground-only tmux/FIFO restriction."
    },
    {
      "kind": "A",
      "reference": "PLAN11.1,11.3,11.4,13.3 and ARCHITECTURE12,13,14,16: supported nonstreaming text envelope, completed main only, client-managed history, aligned-metadata policy and separated actual usage."
    },
    {
      "kind": "E",
      "reference": "Actual transform_sse at0842643 and acceptedmain643ce66 callsrepair1 on incomplete/error-bearing main envelope or finalmessage; annotations/logprobs survive changed text. Private continuation-api-boundary-probes.json and continuation-aligned-metadata-probes.json, metadata-only synthetic diagnostics."
    },
    {
      "kind": "I",
      "reference": "Independent source review: _Handler does not parse request capabilities and repairs only SSE; nonstreaming JSON passes unchanged. forward borrows reviewer credential when main Authorization absent. Review usage is discarded. These existing gaps are not closed by014."
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

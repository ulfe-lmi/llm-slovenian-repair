# Work report 015-a - Explicit text Responses contract, completion validation and usage separation (objective 015, round 1; CREATE_NEW_PR; PR #17 open; branch retained)

```oap-report
{
  "id": "015-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/015-a-supported-responses-contract.md",
  "order_sha256": "26f1a6339031d19084314a6c00609f98b2553cd5ca14907882edd9e55fdaa2a9",
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
  "publication_commit": "SELF",
  "implementation_head": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 17,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/17",
  "pr_state": "open",
  "branch": "oap/015-supported-responses-contract",
  "base_sha": "09e412942a407e94d5d3890d7749c6672e314526",
  "starting_remote_sha": "09e412942a407e94d5d3890d7749c6672e314526",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-26T23:26:30+00:00",
  "report_written_at": "2026-10-26T23:34:00+00:00",
  "checks": [
    {
      "command": "A1 - supported JSON and delayed SSE repair: useful 2-target answers with one fresh batch and exact original protected spans",
      "result": "PASSED",
      "details": "Through actual ephemeral ConceptProxy HTTP, real RepairEngine with the qualified official static Pandoc 3.7.0.2 and real tiny SQLite, actual ResponsesReviewer, and fake main/review upstreams with separate synthetic keys: the canonical 2-target TEXT answer makes exactly one batch review request on both the nonstreaming JSON primary path and the retained delayed SSE path (reordered t1/t0 results accepted), the repaired text appears consistently in every terminal representation, and the protected content span (a Markdown link label) stays byte-exact while the unprotected occurrence is replaced; the protected-span answer (prose occurrence replaced, lexicon 'konec' occurrence kept, link label not a candidate) returns the exact expected text with one review call.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "A2 - unsupported requests fail before main; invalid/completion/metadata responses never reach repair",
      "result": "PASSED",
      "details": "A 40+ case request table (unsupported capabilities: stored chaining, include, logprobs, tools, text format, n, audio, conversation, background, empty object; schema violations: empty model, oversized model, empty/empty-list input, non-text roles/parts, out-of-range optional fields, huge integer 10**500, nonfinite NaN/1e999/1e500, duplicate keys, invalid JSON, non-object JSON, invalid UTF-8) each returns HTTP 400 with one closed label and asserts zero main HTTP calls plus zero review calls. Completed-envelope contradictions - non-null incomplete_details, store true, previous_response_id, conversation, background true (JSON and SSE), unknown/tool output items, refusal part, malformed/empty message id, extra messages/parts, missing or null final-message status, incomplete reasoning, two reasoning items - abstain with the raw original bytes and zero review calls; the pinned unset policy positive (absent/null/unset and explicit false flags) still repairs. Malformed main JSON (invalid syntax, invalid UTF-8, duplicate key, nonfinite NaN/1e999) and malformed SSE event JSON (duplicate key, nonfinite) are main errors (502) with zero review calls; declared-mode/observed-content-type mismatch (both directions, valid producer source for the declared content type) returns 502 RESPONSE_MODE_MISMATCH with zero review calls. Independent pre-implementation actual-HTTP reproduction at the exact accepted base 09e4129 confirmed the gaps (nonstreaming JSON forwarded unvalidated; incomplete/error-bearing final envelopes and stale aligned metadata still repaired) and is preserved privately.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "A3 - no-edit and optional failure preserve raw bytes; changed fields follow explicit paths; metadata/usage stay valid",
      "result": "PASSED",
      "details": "A valid completed answer with zero detector candidates returns the captured bytes unchanged with zero review calls on both modes; a changed JSON answer mutates only the validated answer part text (ensure_ascii=False re-serialization of the parsed envelope) while object/id/status/usage/metadata remain exactly as reported; a metadata echo carrying the original answer text is never scanned or rewritten (both original occurrences preserved in the echo, zero in the repaired answer); main usage (absent, null, partial, or full) is preserved exactly as reported and never gates eligibility; invalid/timeout/non-200 reviewer outcomes return the original after at most one review call; invalid second proposals reject the whole batch (a valid first proposal does not survive).",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "A4 - actual independent main/review authentication and client-managed two-turn history prove no state leakage",
      "result": "PASSED",
      "details": "The forwarding allowlist is content-type, accept, and an explicitly caller-provided authorization only: hop-by-hop, internal control, session/request-id, proxy-control and linkage headers are never forwarded to main; a request carrying no main Authorization is not served the reviewer key (no borrowing) and reviewer calls always carry the reviewer key; separate synthetic main/review keys are proven independent through the actual chain. Client-managed two-turn history: turn 2's main request body carries the client-supplied messages including the final visible repaired text once (no proxy-side state, no store, no previous_response_id chaining, which is rejected before any forward), and the full two-turn exchange makes the per-turn review calls with no leakage between turns.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "A5 - actual separated usage with explicit unknowns and no carryover, visible to an operator without raw logs",
      "result": "PASSED",
      "details": "Reviewer usage is request-local: begin_request resets the request-local state on every request; a valid 3-count usage (with the documented input/output_tokens_details extras tolerated, booleans rejected) is reported; absent, null, partial, or invalid usage is explicit 'unknown' - never zero; a known-usage request followed by a no-review (zero-candidate) request on the same proxy instance reports calls=0 with usage unknown (no carryover); a failed-batch request reports calls=1 with usage unknown. The actual detailed-shape main usage is preserved as reported in the client-visible response. CONCEPT_USAGE_OBSERVER=stderr is wired at the normal main() entry point (probe test): the record is exactly review call count plus token counts or 'unknown', is content-free (a canary X-Concept-Request-ID never appears in the record), and an observer exception is isolated without changing the answer.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "A6 - all established tests/assertions, truthful docs/report, immutable prior history, all 4 required final-head CI",
      "result": "PENDING",
      "details": "The focused suite (test_review_batch.py, test_pandoc_protection.py, test_concept.py, test_responses_contract.py) passed 251 tests plus 87 subtests on pre-commit dirty candidate bytes with the exact Python 3.12 interpreter (-B, REPAIR_ALLOW_LIVE_TESTS=NO) and the qualified official static Pandoc 3.7.0.2; the nine tested files are byte-identical (verified by git blob comparison) to the final implementation head, so the focused evidence is attributable to that head's tested-file bytes; all pre-existing 014-a/014-b assertions are retained (old transport fixtures updated only where the order requires the declared valid contract shape). Docs updated truthfully (concept README section; root README/STATUS/READINESS/ROADMAP corrections); all 16 governance pins verify against disk; prior reports/orders byte-unchanged. The four required final-head CI checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) are PENDING as strategic post-publication evidence.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "Frozen historical single-target evaluator and prompt regression",
      "result": "PASSED",
      "details": "The historical single-target prompt, evaluator API, Proposal/parse_proposal, and the legacy reviewer byte path are unchanged; the frozen archive prompt hashes are byte-identical. Named frozen regression: test_strategic_prompt_archive through unittest discovery, 3 passed, exact Python 3.12 interpreter.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed Python files",
      "result": "PASSED",
      "details": "Ruff 0.16.6 with --no-cache clean on the nine changed Python files (proxy.py, qwen_client.py, batch_review.py, config.py, responses_contract.py, and the four test modules). mypy 2.3.1 (strict, python_version 3.12) clean on the same nine-file set with the actual repository import context (MYPYPATH at the repo root, --follow-imports=silent, --no-incremental on an owned scratch copy with an owned external cache); no import ignores added. Scope is the changed module set, not the whole repository.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 65 -> 66 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed from 65 to 66 only; registry_entries 42 and frozen_report_history_incidents 2 and all identity fields are unchanged. The designed implementation-head report-count red is confirmed by the observed CI: AssertionError 66 != 65, Ran 409 tests, failures=1, skipped=53, no other failure; it clears at the final head with this report commit.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "The branch carries three commits over base 09e412942a407e94d5d3890d7749c6672e314526. Implementation head 1c206dab4fabe26c5748592b794f745205246b37 (sole parent 09e4129) changes exactly the 18 authorized paths: concept-verification/{proxy.py, qwen_client.py, batch_review.py, config.py, responses_contract.py (new), README.md, tests/test_review_batch.py, tests/test_concept.py, tests/test_pandoc_protection.py, tests/test_responses_contract.py (new)}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins only - README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md; all 173 pins verified against disk), oap/active, the new 015-a order, and research/RESEARCH-STATE.md (counter only). Two subsequent docs-only commits follow: d11212f2aa5f61585659b13ab5dd613e7baab8f9 (exact input message shape and declared request limits in the concept README) and 2d7294bcd048e4feb8ab9af2f95c02eab9690028 (per-string/part 200,000-code-point bound wording), each changing only concept-verification/README.md. git diff --check is clean at every head; the tracked tree is clean at the final head; the nine focused-tested Python files are byte-identical across all three heads (verified by git blob comparison); the unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ remain unstaged and untouched.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "At report-writing time, at the final implementation/docs head 2d7294bcd048e4feb8ab9af2f95c02eab9690028: Research reproducibility FAILED solely on the designed report-count red (66 != 65; Ran 409 tests, failures=1, skipped=53; no other failure) - the same single failure was observed earlier at implementation commit 1c206dab. Application baseline and OAP bootstrap acceptance were still in progress; OAP report history posts at the report head.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "2d7294bcd048e4feb8ab9af2f95c02eab9690028",
      "publication_head_claim": false
    }
  ],
  "implementation": "New pure module responses_contract.py: strict pre-forward validation of the explicit text-only Responses request (UTF-8/JSON, duplicate-key-free, nonfinite-number-free, no coercion; nonempty bounded model; text-only client-managed input; explicit store:false; boolean stream with absent meaning false; allowlisted temperature/top_p/top_k/max_output_tokens/stop/metadata with exact types and finite values) with closed 400 labels and zero main/reviewer calls, and the shared completed-envelope profile (object=response, exactly completed status, absent/null error, pinned stateless declaration policy, at most one bounded noneditable reasoning item preceding exactly one completed assistant message with an exact typed nonempty id and exactly one plain nonempty output_text part with aligned annotations/logprobs absent or empty). proxy.py: transform_json implements the nonstreaming JSON primary path (malformed main is a main error; unsupported/incomplete/error envelopes pass through byte-identical with zero calls; only the validated part text is mutated); transform_sse validates its completed event with that same full envelope validation (JSON/SSE profile parity) while established ownership, terminal-copy, delta-type and renderer rules are unchanged; the handler adds the 400 gate, the declared-mode/observed-content-type 502 RESPONSE_MODE_MISMATCH, and the content-type allowlist (content-type/accept/authorization only; no reviewer-key borrowing); reviewer usage is request-local (reset per request; explicit unknown, never zero, never carried over); observe_usage emits a bounded content-free record and CONCEPT_USAGE_OBSERVER=stderr is wired at main(). qwen_client.py: review_batch returns the validated BatchResult (proposals plus actual reviewer usage or explicit unknown). batch_review.py: parse_batch_envelope carries usage separately and never rejects valid proposals over usage. config.py: finite API_MAX_* limits. Tests: new actual-HTTP contract module plus the ordered fixture updates; the frozen legacy single-target path is byte-unchanged.",
  "documentation": "concept-verification/README.md documents the exact endpoint/request/response profiles, the closed 400 labels, the shared completed-envelope profile (including the pinned stateless declaration policy and the JSON/SSE parity rule), nonstreaming JSON primary plus retained delayed SSE behavior, status/error policy, aligned-metadata abstention, client-owned history and stored-chaining rejection, the authentication/header allowlist, separated usage with explicit unknowns and the content-free stderr observer, and the finite limits. STATUS.md records the round; the root README, docs/READINESS.md, and docs/IMPLEMENTATION-ROADMAP.md carry the directly affected corrections (the prior 'supported API/envelope/history and usage contract' follow-up item is now implemented). The frozen research/evaluator protocol remains historical, not silently revised. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): JSON and delayed SSE useful 2-target repairs with one fresh batch, reordered results, protected spans exact. A2 SATISFIED (observed): unsupported requests fail before main with zero main plus zero review calls; invalid/completion/declaration/metadata responses never reach repair; malformed main and mode mismatch are bounded protocol failures; pre-fix gaps reproduced at the exact accepted base and preserved privately. A3 SATISFIED (observed): no-edit and optional failure preserve raw bytes; changed fields follow explicit validated paths; metadata/usage stay exactly as reported. A4 SATISFIED (observed): independent main/review authentication, no key borrowing, client-managed two-turn history with no state leakage. A5 SATISFIED (observed): separated request-local usage with explicit unknowns, no carryover, operator-visible content-free record at the normal entry point. A6 PARTIALLY OBSERVED: focused suite 251 passed plus 87 subtests (pre-commit dirty candidate bytes), truthful docs, unchanged prior history (all 16 governance pins verified), exact report parent/path; the four required final-head CI checks are PENDING as recorded (strategic post-publication evidence).",
  "negative_paths": "No live endpoints, model processes, corpus acquisition, credential, service, port or network change; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no detector/acceptance/morphology change; no registry entry; no deployment; no merge or auto-merge; no edits outside the ordered allowlist; the historical single-target evaluator prompt/API and frozen archive byte-unchanged; no stored/server-side state; no reviewer key borrowing; no general capability expansion (the contract is bounded to the explicit text-only profile and abstains on everything else); untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ preserved and unstaged.",
  "boundary_fidelity": "Main capture/completion semantics, the 013-a mandatory Pandoc startup/version/mapping/protection behavior, the 014-a batch/acceptance contract (one strict occurrence-addressed request, ordered finite 15-second reviewer timeout, closed reason vocabulary), and the 014-b terminal-copy preflight/renderer rules are preserved; the established 013/014 focused assertions all remain with their original behavior (old transport fixtures updated only to the declared valid contract shape where the order required). The change adds the pre-forward request gate, the shared completed-envelope eligibility (now also applied to the SSE completed event - a parity tightening that only turns previously-repairable explicit contradictions into raw unchanged abstentions), the mode-mismatch protocol error, the header allowlist, and the separated request-local usage; no previously valid completed answer shape loses eligibility except those explicit contradictions named in the order.",
  "setup": "External Python 3.12.15 interpreter (/home/janezp/envs/llm-slovenian-repair/bin/python) with -B for all ordered suites and OAP helpers; REPAIR_ALLOW_LIVE_TESTS=NO; OAP_ROLE=coding exported for helper commands; umask 077 for private scratch; owned scratch under the strategic home (test-scratch-015a). Pandoc qualified read-only from the installer-owned official static archive 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229); no bare uv and no repository .venv writes. Bounded setup deviations (recorded, no CRIT): (1) one early 'python -B -m py_compile' syntax check still wrote nine .pyc files into the two existing git-ignored concept-verification __pycache__ directories despite -B (private metadata receipt 015a-pycompile-cache-deviation.json); they were preserved as-is (no deletion, reset, or restoration claim) and later syntax checks used ast.parse or owned external cache prefixes; (2) the earlier 014-b .ruff_cache deviation remains historical - every 015-a Ruff run used --no-cache. mypy ran on an owned scratch copy with an owned external cache and the actual repository import context; scope recorded in the checks. Fake main/review upstreams are ephemeral loopback servers with fake keys and synthetic payloads only.",
  "privacy": "Synthetic fixtures only; no customer data, credential, private raw text, or private path in the report or logs; reviewer credentials are operator-configured and never read or logged; diagnostics are bounded fixed-label content-free reasons; private receipts are metadata-only (pre-fix actual-HTTP reproduction at the exact accepted base, independent first-contract/wired/usage-history probe receipts, the 34-case JSON/SSE profile qualification result, focused-run source hashes, the py_compile cache deviation record, and the scratch-permissions normalization record).",
  "limits": "Focused suites and the named static analyses ran on pre-commit dirty candidate bytes at base 09e4129 (dirty-candidate limitation); the nine tested files are byte-identical to the final implementation head (verified by git blob comparison), so the focused evidence is attributable to that head's tested-file bytes rather than claimed as a later-SHA rerun; after those runs only documentation (concept README shape/limits wording), the STATUS.md round paragraph, the PR body, the report counter, the GENERATED-FILES pins, and the report itself changed, none of which is exercised by the focused suites, and the commit-shape check confirms the census at each head. The mypy scope is the nine-file changed set with unchanged imported modules not re-reported, not the whole repository. The pre-fix reproduction ran against the exact accepted base 09e4129, so it is exact-SHA evidence for the pre-015-a behavior. Independent strategic probes (pre-implementation HTTP, wired v2/v3, usage/history, profile qualification) ran against stable dirty-candidate snapshots with recorded source hashes and are evidence for those candidates, not for the final commit. Final report-head CI is PENDING.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: concept-verification/{proxy.py, qwen_client.py, batch_review.py, config.py, responses_contract.py (new), README.md, tests/test_review_batch.py, tests/test_concept.py, tests/test_pandoc_protection.py, tests/test_responses_contract.py (new)}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins), oap/active, the new 015-a order, research/RESEARCH-STATE.md (counter 65 -> 66 only), and this report. No other paths or governance changes.",
  "result_summary": "015-a implemented the explicit text-only Responses contract on the runnable concept-verification proxy (new branch, PR #17, CREATE_NEW_PR). A pure pre-forward request gate rejects every unsupported capability and invalid request with one closed 400 label before any main or reviewer call; one shared completed-envelope profile now governs both the nonstreaming JSON primary path and the retained delayed SSE path (the SSE completed event is validated by the same full validation, giving JSON/SSE profile parity); explicit stored/background/linkage/incompleteness declarations, unknown variants, malformed identity, and non-empty aligned metadata abstain with the raw original bytes and zero review calls; forwarding uses a narrow header allowlist with no reviewer-key borrowing; reviewer usage is request-local with explicit unknowns and no carryover while main usage is preserved as reported; CONCEPT_USAGE_OBSERVER=stderr exposes a bounded content-free operator record; client-managed two-turn history works and stored chaining is rejected. Focused verification (251 passed plus 87 subtests) ran on pre-commit dirty candidate bytes with the exact Python 3.12 interpreter and the qualified official static Pandoc 3.7.0.2; Ruff --no-cache and scoped strict mypy are clean on the nine changed Python files; the frozen strategic-prompt archive tests pass unchanged. Implementation-head CI shows the designed report-count red only so far (66 != 65; no other failure); all four required final-head checks are PENDING as strategic post-publication evidence. No scientific, deployment, or acceptance change; no merge; PR #17 stays OPEN pending strategy review."
}
```

## Short factual summary

015-a implemented the explicit text-only Responses request contract on the runnable
concept-verification proxy (new branch `oap/015-supported-responses-contract`, PR #17,
CREATE_NEW_PR, base 09e4129). A pure pre-forward gate validates the request (strict
duplicate-key-free/nonfinite-free parsing, nonempty bounded model, text-only client-managed
input, explicit `store: false`, boolean `stream`, allowlisted ordinary fields) and rejects
any other key - stored chaining, `include`, `logprobs`, `tools`, `text`, `n`, `audio`,
`conversation`, `background`, or any unknown capability - with HTTP 400 and one closed
label before any main or reviewer call (negative request tests assert zero main HTTP calls
and zero review calls). One shared completed-envelope profile governs the nonstreaming
JSON primary path and the retained delayed SSE path: the SSE completed event is now
validated by the same full envelope validation (JSON/SSE profile parity), so explicit
stored/background/linkage/incompleteness declarations, unknown/tool/refusal variants,
extra messages/parts, malformed or missing identity, incomplete reasoning, and non-empty
aligned metadata all abstain with the raw original bytes and zero review calls. Malformed
main JSON/SSE is a main error (502); a declared-mode/observed-content-type mismatch
returns 502 `RESPONSE_MODE_MISMATCH`. Forwarding uses a narrow content-type/accept/
authorization allowlist with no reviewer-key borrowing. Reviewer usage is request-local
with explicit unknowns (never zero, never carried over); main usage is preserved as
reported; `CONCEPT_USAGE_OBSERVER=stderr` exposes a bounded content-free operator record.
Client-managed two-turn history is supported; stored chaining is rejected. The frozen
historical single-target evaluator prompt and protocol are byte-unchanged.

Verification on pre-commit dirty candidate bytes (exact Python 3.12, qualified official
static Pandoc 3.7.0.2): focused suite 251 passed plus 87 subtests (all pre-existing
013/014 assertions retained, old fixtures updated only to the declared valid contract
shape); Ruff `--no-cache` clean and scoped strict mypy clean on the nine changed Python
files; frozen strategic-prompt archive tests 3 passed. Independent strategic pre-fix and
post-fix actual-HTTP probes (metadata-only receipts, stable candidate snapshots)
confirmed the named gaps before the fix and the 34-case JSON/SSE profile parity after.
Implementation-head CI observed so far: Research reproducibility failed solely on the
designed report-count red (66 != 65; Ran 409 tests, failures=1, skipped=53); Application
baseline and OAP bootstrap acceptance were in progress; OAP report history posts at the
report head. All four required final-head checks are PENDING as strategic post-publication
evidence. Report counter advanced 65 -> 66 for final publication; no registry entry. One
bounded setup deviation is recorded (an early `py_compile` check wrote nine .pyc files
despite -B; preserved as-is, later checks used ast.parse/owned prefixes). No scientific,
deployment, or acceptance change; no merge; PR #17 stays OPEN.

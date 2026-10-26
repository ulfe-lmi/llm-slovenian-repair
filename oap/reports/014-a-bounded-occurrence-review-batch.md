# Work report 014-a - One bounded occurrence-addressed reviewer batch in the runnable proxy (objective 014, round 1; CREATE_NEW_PR; PR #16 open; branch retained)

```oap-report
{
  "id": "014-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/014-a-bounded-occurrence-review-batch.md",
  "order_sha256": "9ef74e5279368b3549e33cbd75274730280ba7a963f3ab3acf4ce1cdf34a3812",
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
  "implementation_head": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 16,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/16",
  "pr_state": "open",
  "branch": "oap/014-bounded-review-batch",
  "base_sha": "643ce66e820a9d21750309bd00b22bfc19a819cd",
  "starting_remote_sha": "643ce66e820a9d21750309bd00b22bfc19a819cd",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-26T09:29:00+00:00",
  "report_written_at": "2026-10-26T09:33:00+00:00",
  "checks": [
    {
      "command": "A1 - exactly one review request for the actual 2-target engine/HTTP path; zero calls for invalid-preparation, no-occurrence and multi-answer paths",
      "result": "PASSED",
      "details": "Focused suite (test_review_batch.py, test_concept.py, test_pandoc_protection.py) on pre-commit dirty candidate bytes at base 643ce66 with the exact Python 3.12.15 interpreter (-B, REPAIR_ALLOW_LIVE_TESTS=NO) and the qualified official static Pandoc 3.7.0.2: 172 passed plus 5 subtests (dirty-candidate source hashes recorded privately). Engine cases use real tiny SQLite, the real RepairEngine and the real Pandoc: two detected repeated target occurrences produce exactly one batch request; a selection mixing a valid candidate with an unmatched/stale candidate returns the original unchanged with zero reviewer calls (no valid subset is reviewed); zero-occurrence and invalid-preparation paths make zero calls. Multi-answer and ambiguous SSE (two assistant messages, two output_text parts, stream id mismatch, stream index mismatch, integer/null/missing stream ids) bypass unchanged with zero calls through actual ephemeral ConceptProxy HTTP.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "A2 - repeated occurrence IDs/coordinates and bounded context exact; reordered results map by validated ID",
      "result": "PASSED",
      "details": "Repeated identical target text receives distinct response-local IDs (t0, t1) with exact per-occurrence before/after context (240-codepoint windows, truncation flags, 128-codepoint target bound) and exact original coordinates; response items in an order different from the supplied ID order map by validated ID, never array position, with the exact request body, route and fake-key authorization asserted through a real HTTP fake upstream (synthetic data only).",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "A3 - batch transport isolation and strict schema/duplicate/missing/unknown/timeout/oversize negatives fail the whole batch",
      "result": "PASSED",
      "details": "Strict duplicate-key-free JSON parsing at both envelope levels rejects duplicate keys, fenced/trailing output, and nonfinite or overflowing numbers (1e999 rejected, not coerced to infinity); missing, unknown or duplicate proposal IDs, explicit non-completed status, incomplete/in_progress reasoning, tools, refusals, a second assistant output_text, empty/whitespace replacements and oversized outputs each reject the whole batch with the byte-exact original and at most one request and no retry; non-200, oversized read and invalid encoding carry labeled reasons; oversize prompt/request preparation is rejected before dispatch (zero requests). A valid first proposal does not survive an invalid second one (failure-after-first regression, also through the full chain).",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "A4 - one-answer SSE eligibility, terminal copies, no-edit raw preservation and individual evidence rejection",
      "result": "PASSED",
      "details": "Repair is invoked only for one unambiguously confirmed completed assistant output_text: typed string stream ids matching the confirmed message id (message.id equals event item_id; no invented or coerced ids), stream output/content indexes validated against actual final list positions for every delta/done event, and terminal copies (content_part.done, output_item.done) updated consistently through the explicit validated id/index paths while unrelated bytes and metadata stay untouched; every extra or other-id answer event bypasses with zero calls. When no accepted edit changes the answer, the raw original SSE bytes are returned byte-identical (proven through the full actual HTTP chain). Structurally valid proposals rejected by corpus/lexicon evidence remain individual rejections while independent valid proposals proceed (one accepted plus one kept/wider no-op; per-candidate isolated acceptance). Engine failure reasons are a finite closed vocabulary; any other exception maps to REVIEW_FAILED with no untrusted exception content in traces.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "Frozen historical single-target evaluator and prompt regression",
      "result": "PASSED",
      "details": "The historical single-target prompt, evaluator API, Proposal and review path are byte-unchanged (frozen archive prompt hashes unchanged). Named frozen regression: test_strategic_prompt_archive through unittest discovery, 3 passed, Python 3.12 interpreter; the relevant existing concept evaluator tests are covered by the focused suite.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed Python files",
      "result": "PASSED",
      "details": "Ruff 0.16.6 clean on every changed Python file (batch_review.py, proxy.py, qwen_client.py, config.py, tests/test_review_batch.py, tests/test_concept.py, tests/test_pandoc_protection.py). mypy 2.3.1 (strict) clean on the same seven changed files with the actual repository import context (MYPYPATH at the repo root, --follow-imports=silent, run on a byte-identical owned scratch copy because the concept-verification directory name is not a valid package). No import ignores were added; the only ignores are minimal targeted test-double boundary annotations in the changed test files. Scope is the changed module set, not the whole repository.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 63 -> 64 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed from 63 to 64 only; registry_entries 42 and frozen_report_history_incidents 2 and all identity fields are unchanged. The designed implementation-head report-count red is confirmed by the observed CI: AssertionError 64 != 63, Ran 409 tests, failures=1, skipped=53.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "Implementation head b5298e720e88c5b78bfc75af61ddebffcb7a8a9c (sole parent 643ce66e820a9d21750309bd00b22bfc19a819cd) changes exactly the 16 authorized paths: four changed concept-verification Python modules, new concept-verification/batch_review.py, the three concept-verification test modules, concept-verification/README.md, README.md, docs/IMPLEMENTATION-ROADMAP.md, docs/READINESS.md, STATUS.md, oap/GENERATED-FILES.json (affected pins only; existing serialization preserved), oap/active, the new 014-a order, and research/RESEARCH-STATE.md (counter only). git diff --check is clean; the tracked tree is clean at the head; all GENERATED-FILES pins verify against the committed bytes.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "At report-writing time: Research reproducibility FAILED solely on the designed report-count red (64 != 63; failures=1, skipped=53; no other failure). OAP report history PASSED (7s). Application baseline and OAP bootstrap acceptance were still in progress. Final report-head CI is recorded separately.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "b5298e720e88c5b78bfc75af61ddebffcb7a8a9c",
      "publication_head_claim": false
    }
  ],
  "implementation": "New concept-verification/batch_review.py: the batch-v1 contract - occurrence-addressed targets (exact original-slice equality, no overlap or protected intersection, grapheme-safe, deterministic t0..tN IDs, at most 4 items, 128-codepoint targets with 240-codepoint context windows and truncation flags), finite limits (8192-codepoint prompt, 32768-byte request and response bounds, 8192-codepoint proposal JSON, 1536 max output tokens, replacements of at most 8 words / 128 codepoints), bounded prompt/request builders (stream:false, store:false, no tools, no caller-selected URL), strict duplicate-key-free JSON parsing at both levels (fenced objects, Infinity/NaN/overflow rejected), and an envelope parser aligned to the documented Responses object (object=response, completed status) accepting at most one bounded noneditable completed reasoning item (status null/missing/completed; explicit incomplete/in_progress, tools, refusals, unknown variants, a second assistant text, empty replacements and oversized outputs rejected). qwen_client.py: additive review_batch transport (pre-dispatch oversize rejection, non-200 and oversize-read rejection, labeled ReviewerError reasons) with the ordered finite 15-second REVIEWER_HTTP_TIMEOUT_SECONDS separate from the upstream capture timeout; the historical single-target prompt/parse_proposal/Proposal/review path is byte-unchanged. proxy.py: whole-selection validation (any unmatched or stale selected occurrence returns the completed original with zero reviewer calls - no valid subset is reviewed), one batch call per answer, a finite closed reason vocabulary with unknown exceptions mapped to REVIEW_FAILED (no untrusted exception content in traces), and per-candidate isolated acceptance. transform_sse: minimal one-answer eligibility - typed string stream ids (no coercion) matching the single confirmed completed assistant output_text (message.id equals event item_id), stream output/content indexes validated against actual final positions, terminal copies (content_part.done, output_item.done) updated through explicit validated id/index paths, unrelated bytes and metadata untouched, every extra or other-id answer event bypassing with zero calls, and byte-exact raw-original preservation whenever no accepted edit changes the answer. config.py: the finite review-batch constants. Detector evidence/thresholds, target selection semantics, Pandoc wiring, and the strict acceptance authority are unchanged.",
  "documentation": "concept-verification/README.md documents the versioned batch schema, exact occurrence context, the finite limits, whole-batch rejection versus individual evidence rejection, the one-answer SSE eligibility guard, and the preserved historical single-target evaluator API, including the ordered 15-second reviewer HTTP timeout versus the separate upstream capture timeout. README.md, docs/IMPLEMENTATION-ROADMAP.md (013/014 continuation remap) and docs/READINESS.md carry the directly affected status statements. STATUS.md records the round. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): the actual 2-target engine/HTTP path makes exactly one review request (real SQLite + RepairEngine + Pandoc, ephemeral HTTP, and the full proxy->engine->ResponsesReviewer->fake-reviewer composition chain); zero-target, invalid-preparation and mixed-unmatched paths make zero calls; multi-answer/ambiguous SSE makes zero calls. A2 SATISFIED (observed): repeated occurrences carry distinct IDs with exact coordinates and bounded context; reordered results map by validated ID with the exact request body asserted (no substring location). A3 SATISFIED (observed): the actual batch transport isolates the request (real HTTP, fake key, synthetic data) and every strict schema/duplicate/missing/unknown/timeout/oversize negative fails the whole batch with the byte-exact original and at most one request. A4 SATISFIED (observed): safe positive original-coordinate edits plus individual evidence rejections; an invalid batch returns the exact original; one-answer SSE eligibility, terminal copies, no-edit raw preservation and the preserved Pandoc/protection/capture semantics are proven through actual HTTP. A5 PARTIALLY OBSERVED: truthful docs updated; frozen evaluator/science/governance unchanged; focused suites pass with the stated attribution; the required final-head CI is PENDING as recorded (strategic post-publication evidence), with the implementation-head CI observed so far as recorded.",
  "negative_paths": "No live endpoints, model processes, corpus acquisition, credential, service, port or network change; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no registry entry; no deployment; no merge or auto-merge; no edits outside the ordered allowlist; no general SSE expansion (the guard is bounded to answer identity/count); detector evidence/thresholds unchanged; the frozen historical single-target evaluator path and archive prompt hashes byte-unchanged; untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ preserved and unstaged.",
  "boundary_fidelity": "Upstream capture/completion semantics and the 013-a mandatory Pandoc startup/version/mapping/protection behavior are preserved (parse/map failure and no eligible suspicion remain zero-review paths; no AST rendering, substring recovery, weaker regex fallback or source normalization). The minimal SSE guard changes only answer-identity/count behavior and no-edit preservation; existing valid single-answer SSE tests are retained with confirming message identities. Trace additions are bounded fixed-label counts/reasons/version with the per-answer review-call count and no new raw payload/prompt/response logging.",
  "setup": "External Python 3.12.15 interpreter (/home/janezp/envs/llm-slovenian-repair/bin/python) with -B for all ordered suites and OAP helpers; REPAIR_ALLOW_LIVE_TESTS=NO; OAP_ROLE=coding exported for helper commands; umask 077 for private scratch; owned scratch under the strategic home. Pandoc qualified read-only from the installer-owned official static archive 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229) in an owned prefix; no bare uv and no repository .venv/cache writes. mypy ran on a byte-identical owned scratch copy with the actual repository import context; scope recorded in the checks. Fake reviewer upstreams are ephemeral loopback servers with fake keys and synthetic payloads only.",
  "privacy": "Synthetic fixtures only; no customer data, credential, private raw text, or private path in the report or logs; reviewer credentials are operator-configured and never read or logged; diagnostics are bounded fixed-label content-free reasons; private receipts are metadata-only (source hashes, binary hash, test counts).",
  "limits": "Focused suites ran on pre-commit dirty candidate bytes at base 643ce66 (dirty-candidate limitation); after those runs only documentation, the STATUS.md round paragraph, the report counter, the GENERATED-FILES pins, and the report itself changed, none of which is exercised by the focused suites, and the commit-shape check confirms the census at the implementation head. The mypy scope is the seven changed Python files with unchanged imported modules not re-reported, not the whole repository. Final report-head CI is PENDING.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: concept-verification/proxy.py, qwen_client.py, config.py, new batch_review.py, tests/test_review_batch.py (new), tests/test_concept.py and tests/test_pandoc_protection.py (necessary fixture/interface changes plus regression additions), concept-verification/README.md, README.md, STATUS.md, docs/IMPLEMENTATION-ROADMAP.md, docs/READINESS.md, research/RESEARCH-STATE.md (counter 63 -> 64 only), the affected oap/GENERATED-FILES.json pins, this order, oap/active, and this report. No other paths or governance changes.",
  "result_summary": "014-a implemented one bounded occurrence-addressed reviewer batch (batch-v1) in the runnable concept-verification proxy: exact occurrence selection with whole-batch validation (an invalid or stale selection returns the original with zero reviewer calls), one fresh nonstreaming strict batch request with the ordered 15-second reviewer timeout, strict duplicate-key-free parsing of the documented object=response envelope with bounded noneditable reasoning, per-candidate isolated acceptance, a minimal one-answer SSE eligibility guard with no-edit raw preservation, and a finite closed reason vocabulary. The historical single-target evaluator prompt/API is byte-unchanged. Focused verification (172 passed plus 5 subtests) ran on pre-commit candidate bytes with the exact Python 3.12 interpreter and the qualified official static Pandoc 3.7.0.2; Ruff and scoped mypy are clean; the named frozen strategic-prompt archive tests pass unchanged. The implementation-head CI shows the designed report-count red only so far; all four required final-head checks are PENDING as strategic post-publication evidence. No scientific, deployment, or acceptance change; no merge; PR #16 stays OPEN pending strategy review."
}
```

## Short factual summary

014-a added one bounded occurrence-addressed reviewer batch (batch-v1) to the runnable
concept-verification proxy: whole-selection validation (invalid/stale selection returns the
original with zero reviewer calls, no valid subset reviewed), a single fresh nonstreaming
strict request with the ordered 15-second reviewer HTTP timeout, strict duplicate-key-free
parsing of the documented `object=response` envelope with bounded noneditable completed
reasoning, per-candidate isolated acceptance, a minimal one-answer SSE eligibility guard
(typed stream ids, final-position index validation, terminal copies, byte-exact raw-original
preservation when nothing is edited), and a finite closed reason vocabulary. The historical
single-target evaluator prompt/API is byte-unchanged. Focused suite 172 passed plus 5
subtests on pre-commit dirty candidate bytes with the exact Python 3.12 interpreter and the
qualified official static Pandoc 3.7.0.2; Ruff clean; scoped mypy clean (changed module set,
actual repository import context); frozen strategic-prompt archive tests 3 passed.
Implementation-head CI observed so far: Research reproducibility failed solely on the
designed report-count red (64 != 63), OAP report history passed, Application baseline and
OAP bootstrap acceptance in progress; all four required final-head checks are PENDING as
strategic post-publication evidence. Report counter advanced 63 -> 64 for final
publication; no registry entry. No scientific, deployment, or acceptance change; no merge;
PR #16 stays OPEN.

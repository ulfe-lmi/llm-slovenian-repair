# Work report 014-b - Validate every terminal answer copy before bounded review (objective 014, round 2; AMEND_EXISTING_PR; PR #16 open; branch retained)

```oap-report
{
  "id": "014-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/014-b-validate-terminal-answer-copies.md",
  "order_sha256": "73478cc0fe073210520f5991f9d64379684a8dfc1cffaca2806afdaea3e046a4",
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
  "implementation_head": "46c4938bce1efb4d8acef337606b787abaab695b",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 16,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/16",
  "pr_state": "open",
  "branch": "oap/014-bounded-review-batch",
  "base_sha": "6c4bf45060300932f721b31ea51a6da3d82c2984",
  "starting_remote_sha": "6c4bf45060300932f721b31ea51a6da3d82c2984",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-26T21:17:03+00:00",
  "report_written_at": "2026-10-26T21:22:00+00:00",
  "checks": [
    {
      "command": "A1 - all newly named negative terminal copies bypass raw unchanged with 0 repair calls / 0 review HTTP requests before any side effect",
      "result": "PASSED",
      "details": "Pre-fix reproduction at the exact published 014-a head 6c4bf45 (transform_sse extracted byte-identical from that SHA): 14 of 16 negative cases called repair once and changed the body (two-part terminal item, conflicting terminal part/item text, missing/null/integer part ids, wrong-role and incomplete-status terminal item, conflicting output_text.done text, duplicate terminal part copies, and four non-string delta payloads: missing/null/number/array); the other-id and wrong-declared-index cases already bypassed, and the canonical positive called repair once. Post-fix, all 16 negatives return the byte-identical raw original with zero repair calls - proven by direct transform_sse and through the full actual ConceptProxy -> RepairEngine/Pandoc/tiny-SQLite -> ResponsesReviewer -> fake-reviewer-HTTP chain (status 200, raw bytes unchanged, zero review HTTP requests). Pre- and post-fix observations are preserved in private metadata-only receipts.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "A2 - canonical positive actual full HTTP chain retains 2-target/1-batch useful repairs, consistent known terminal copies, protected same-text metadata/reasoning and exact unapproved slices",
      "result": "PASSED",
      "details": "Through actual ephemeral ConceptProxy HTTP, real RepairEngine with real Pandoc 3.7.0.2 and real tiny SQLite, actual ResponsesReviewer, and a fake reviewer HTTP endpoint: the unmutated 2-target TEXT baseline (identical full answer in every copy) makes exactly one review request and the repaired text appears consistently in all four terminal representations (stream delta handling, content_part.done, output_item.done, response.completed) while presenetliv is absent from the result. Unrelated metadata including a same-text output_text-shaped echo in response.metadata stays byte-identical; protected reasoning bookkeeping and untouched non-answer items remain byte-identical; a valid canonical stream with protected reasoning plus the final message at a nonzero output_index passes (one request, consistent copies).",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "A3 - final renderer touches only prevalidated paths; no ID coercion, value-based matching, or unsupported copy repair",
      "result": "PASSED",
      "details": "The terminal preflight collects bounded explicit event references (confirmed final answer, each validated terminal copy, confirmed delta events) and the renderer mutates only those: no iteration over all output_text nodes of a matching-id object, no recursion into metadata, no substring or identical-value matching, no invented or coerced IDs. The no-edit canonical stream returns the raw original bytes through the full chain; delta payloads must be strings (empty is a valid no-op) and added events must be validated empty placeholders whose content is never rewritten; non-message items (reasoning, tool bookkeeping) are never touched.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "A4 - existing capture/Pandoc/batch/evidence behavior and all focused tests preserve coverage",
      "result": "PASSED",
      "details": "Focused suite (test_review_batch.py, test_concept.py, test_pandoc_protection.py) on pre-commit dirty candidate bytes at base 6c4bf45 with the exact Python 3.12.15 interpreter (-B, REPAIR_ALLOW_LIVE_TESTS=NO) and the qualified official static Pandoc 3.7.0.2: 212 passed plus 12 subtests. All 172 pre-existing 014-a tests plus 5 subtests remain with every assertion retained; 40 new tests cover the terminal-copy ownership/consistency family, the table-driven full-chain terminal-copy matrix, added-event and delta-payload-type negatives, and no-edit/invalid-batch raw-byte preservation with canonical copies. Main-capture semantics, the mandatory Pandoc 013-a behavior, and the strict batch/acceptance authority are unchanged.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "A5 - accurate corrective docs/report, unchanged old history/science/governance, exact report parent/path, all 4 required final-head CI green",
      "result": "PENDING",
      "details": "Directly affected docs updated (concept-verification/README.md terminal-copy rules plus the forward-correction of the 014-a A4 scope; STATUS.md round paragraph; PR 16 body amended with the round 014-b section); root README.md was checked and its current affected statement needed no correction. The immutable 014-a report and order remain byte-unchanged; all 16 governance pins verify against disk; the report commit is report-path-only with sole parent 46c4938bce1efb4d8acef337606b787abaab695b. All four required final-head checks are PENDING as strategic post-publication evidence.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "Frozen historical single-target evaluator and prompt regression",
      "result": "PASSED",
      "details": "The historical single-target prompt, evaluator API, Proposal and review path are byte-unchanged (frozen archive prompt hashes unchanged). Named frozen regression: test_strategic_prompt_archive through unittest discovery, 3 passed, exact Python 3.12 interpreter.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed Python files",
      "result": "PASSED",
      "details": "Ruff 0.16.6 clean on the two changed Python files (proxy.py, tests/test_review_batch.py) with --no-cache. mypy 2.3.1 (strict) clean on the seven-file changed set (batch_review.py, proxy.py, qwen_client.py, config.py and the three test modules; this round modified proxy.py and tests/test_review_batch.py) with the actual repository import context (MYPYPATH at the repo root, --follow-imports=silent, --no-incremental on an owned scratch copy with an owned external cache). No import ignores were added; the only ignores are the minimal targeted test-double boundary annotations already present in the changed test files. Scope is the changed module set, not the whole repository. One bounded setup deviation is recorded in setup/limits: a single early Ruff run before the --no-cache convention wrote a repository-local .ruff_cache/0.16.6 entry; that untracked, git-ignored cache was preserved as-is (not deleted or reset), all later runs used --no-cache, and no other repository cache or .venv was written.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 64 -> 65 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed from 64 to 65 only; registry_entries 42 and frozen_report_history_incidents 2 and all identity fields are unchanged. The designed implementation-head report-count red is confirmed by the observed CI: AssertionError 65 != 64, Ran 409 tests, failures=1, skipped=53, no other failure.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "Implementation head 46c4938bce1efb4d8acef337606b787abaab695b (sole parent 6c4bf45060300932f721b31ea51a6da3d82c2984) changes exactly the 8 authorized paths: concept-verification/proxy.py (transform_sse preflight and renderer only), concept-verification/tests/test_review_batch.py, concept-verification/README.md, STATUS.md, oap/GENERATED-FILES.json (the STATUS.md pin only; all 173 pins verified against disk), oap/active, the new 014-b order, and research/RESEARCH-STATE.md (counter only). git diff --check is clean; the tracked tree is clean at the head; the unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ remain unstaged and untouched.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "At report-writing time: Research reproducibility FAILED solely on the designed report-count red (65 != 64; failures=1, skipped=53; no other failure). Application baseline and OAP bootstrap acceptance were still in progress; OAP report history had not yet posted. Final report-head CI is recorded separately.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "46c4938bce1efb4d8acef337606b787abaab695b",
      "publication_head_claim": false
    }
  ],
  "implementation": "concept-verification/proxy.py transform_sse only: a terminal preflight before any reviewer call proves every answer-bearing terminal representation consistent with the single confirmed answer - the same exact typed id, final list positions, assistant role, completed status, content cardinality and part kinds, and the exact original answer text across output_text.done, content_part.done, and message-typed output_item.done copies (at most one of each kind); every output_text.delta payload must be a string (an empty string is a valid no-op); initial added events are supported only as empty placeholders with validated ownership (and assistant role for message items) whose content is never rewritten; any copy that cannot be proved consistent makes the entire SSE ineligible (raw original, zero calls). The renderer mutates only the explicit event references collected during the preflight (confirmed final answer, validated terminal copies, confirmed delta events: first non-empty delta carries the full repaired text, later deltas are emptied) - no value matching, no id coercion, no metadata traversal. No other product file, the callable signature, main capture behavior, mandatory Pandoc wiring, or batch/acceptance semantics changed.",
  "documentation": "concept-verification/README.md documents the exact terminal-copy eligibility and copy-consistency rules, the preflight-before-review, the validated render paths, the delta-payload string rule, the added-event empty-placeholder rule, the canonical positives and negative abstentions, and the forward-correction of the 014-a A4 scope: 014-a proved that nominal terminal copies are updated consistently through explicit validated paths; it did not prove that contradictory, unowned, or duplicated terminal copies are rejected. Two distinct 014-a failure modes were observed at the published head (same-ID contradictory or extra terminal copies were blindly rewritten to the repaired text; unowned copies with a missing or non-string id were left unchanged beside an edited final answer); the 014-b preflight rejects both, and the 014-a report remains unchanged. STATUS.md records the round; the PR 16 body carries the round section. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): all newly named negative terminal copies (two-part item, conflicting terminal texts, missing/null/integer ids, wrong role/status, other id, wrong ownership index, conflicting output_text.done, duplicate copies, non-string delta payloads) bypass raw unchanged with 0 repair calls and 0 review HTTP requests, by direct transform and through the full actual HTTP chain, after a pre-fix reproduction at the exact published 014-a head. A2 SATISFIED (observed): the canonical 2-target positive through the actual full HTTP chain makes one review request with consistent repaired terminal copies, protected same-text metadata echo, byte-identical reasoning bookkeeping, and nonzero-output_index support. A3 SATISFIED (observed): the renderer mutates only prevalidated explicit references; no ID coercion, value-based matching, or unsupported copy repair; no-edit returns raw bytes. A4 SATISFIED (observed): existing capture/Pandoc/batch/evidence behavior unchanged and all pre-existing focused tests retained with every assertion (212 passed plus 12 subtests). A5 PARTIALLY OBSERVED: truthful corrective docs, unchanged 014-a history/science/governance (all 16 pins verified), exact report parent/path; the four required final-head CI checks are PENDING as recorded (strategic post-publication evidence).",
  "negative_paths": "No live endpoints, model processes, corpus acquisition, credential, service, port or network change; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no reviewer prompt/schema/transport/timeout change; no detector/acceptance/morphology change; no registry entry; no deployment; no merge or auto-merge; no edits outside the ordered allowlist; no general SSE capability expansion (the guard is bounded to terminal-copy ownership/consistency of the one confirmed answer); the frozen historical single-target evaluator path and archive prompt hashes byte-unchanged; untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ preserved and unstaged.",
  "boundary_fidelity": "Main capture/completion semantics, the 013-a mandatory Pandoc startup/version/mapping/protection behavior, and the 014-a batch/acceptance contract are preserved (parse/map failure and no eligible suspicion remain zero-review paths; the batch remains one strict occurrence-addressed request with the ordered finite 15-second reviewer timeout). The change alters only terminal-copy eligibility and the render path: contradictory, unowned, duplicated, or malformed terminal copies now abstain raw unchanged instead of being silently edited or left inconsistent beside an edited final answer. All 172 pre-existing 014-a focused tests plus 5 subtests remain with every assertion retained.",
  "setup": "External Python 3.12.15 interpreter (/home/janezp/envs/llm-slovenian-repair/bin/python) with -B for all ordered suites and OAP helpers; REPAIR_ALLOW_LIVE_TESTS=NO; OAP_ROLE=coding exported for helper commands; umask 077 for private scratch; owned scratch under the strategic home. Pandoc qualified read-only from the installer-owned official static archive 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229) in an owned prefix; no bare uv and no repository .venv writes. Bounded setup deviation (recorded, no CRIT): one early Ruff run without --no-cache wrote the repository-local untracked/git-ignored .ruff_cache/0.16.6 entry at 2026-10-26T21:07Z; it was preserved as-is (no deletion, reset, or restoration claim) and all later Ruff runs used --no-cache. mypy ran on an owned scratch copy with an owned external cache and the actual repository import context; scope recorded in the checks. Fake reviewer upstreams are ephemeral loopback servers with fake keys and synthetic payloads only.",
  "privacy": "Synthetic fixtures only; no customer data, credential, private raw text, or private path in the report or logs; reviewer credentials are operator-configured and never read or logged; diagnostics are bounded fixed-label content-free reasons; private receipts are metadata-only (pre-/post-fix reproduction at exact 6c4bf45, independent probe results, focused-run source hashes, the Ruff cache deviation record).",
  "limits": "Focused suites ran on pre-commit dirty candidate bytes at base 6c4bf45 (dirty-candidate limitation); after those runs only documentation, the STATUS.md round paragraph, the PR body, the report counter, the GENERATED-FILES pin, and the report itself changed, none of which is exercised by the focused suites, and the commit-shape check confirms the census at the implementation head. The mypy scope is the seven-file changed set with unchanged imported modules not re-reported, not the whole repository. The pre-fix reproduction ran against the byte-identical extracted 6c4bf45 source, so it is exact-SHA evidence for the published 014-a behavior. Final report-head CI is PENDING.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: concept-verification/proxy.py (transform_sse only), concept-verification/tests/test_review_batch.py (terminal-copy regressions; test_concept.py and test_pandoc_protection.py needed no changes), concept-verification/README.md, STATUS.md, research/RESEARCH-STATE.md (counter 64 -> 65 only), the affected oap/GENERATED-FILES.json pin (STATUS.md only), this order, oap/active, and this report. Root README.md was checked and unchanged. No other paths or governance changes.",
  "result_summary": "014-b completed the corrective terminal-answer-copy validation of objective 014 on the same branch and PR #16. A terminal preflight now proves every answer-bearing terminal representation consistent with the single confirmed answer before any reviewer call (exact typed id, final positions, role, status, cardinality/kinds, exact original text; at most one copy of each kind; string-only delta payloads; empty-placeholder-only added events), and the renderer mutates only the prevalidated explicit references; any unprovable copy abstains with the raw original bytes and zero review calls. This forward-corrects the 014-a A4 scope (nominal copies only): same-ID contradictory/extra copies were blindly rewritten and unowned copies stayed unchanged at the published 014-a head - both rejected by the 014-b preflight and proven by a negative matrix through the full actual HTTP chain, with the pre-fix failures reproduced at the exact published head and preserved privately. Focused verification (212 passed plus 12 subtests) ran on pre-commit dirty candidate bytes with the exact Python 3.12 interpreter and the qualified official static Pandoc 3.7.0.2; Ruff and scoped mypy are clean; the named frozen strategic-prompt archive tests pass unchanged. The implementation-head CI shows the designed report-count red only so far; all four required final-head checks are PENDING as strategic post-publication evidence. No scientific, deployment, or acceptance change; no merge; PR #16 stays OPEN pending strategy review."
}
```

## Short factual summary

014-b corrected the terminal-answer-copy validation of the one-answer SSE guard in the
runnable concept-verification proxy (same branch, PR #16, AMEND_EXISTING_PR). Before any
reviewer call, a preflight proves every answer-bearing terminal representation consistent
with the single confirmed answer - exact typed id, final list positions, assistant role,
completed status, content cardinality and part kinds, and the exact original answer text
across output_text.done, content_part.done, and message-typed output_item.done copies (at
most one of each kind); every output_text.delta payload must be a string; initial added
events are supported only as validated empty placeholders whose content is never rewritten.
Any copy that cannot be proved consistent makes the whole SSE ineligible: raw original
bytes, zero review calls. The renderer mutates only the explicit event references collected
during the preflight (no value matching, no id coercion, no metadata traversal).

Evidence correction (forward, not a rewrite of 014-a): 014-a's A4 established nominal
terminal-copy updating only. At the exact published 014-a head, same-ID contradictory or
extra terminal copies were blindly rewritten to the repaired text, and unowned copies
(missing or non-string id) were left unchanged beside an edited final answer; 14 of 16
negative cases called repair once and changed the body (reproduced on the byte-identical
extracted 6c4bf45 source, preserved privately). The 014-b preflight rejects both failure
modes; all 16 negatives now return raw unchanged with zero repair calls / zero review HTTP
requests, proven directly and through the full actual proxy -> engine/Pandoc/SQLite ->
ResponsesReviewer -> fake-reviewer-HTTP chain.

Verification on pre-commit dirty candidate bytes (exact Python 3.12, qualified official
static Pandoc 3.7.0.2): focused suite 212 passed plus 12 subtests (all 172 pre-existing
014-a tests plus 5 subtests retained with every assertion); Ruff clean on the changed
Python files (--no-cache); scoped mypy clean over the seven-file changed set with the
actual repository import context; frozen strategic-prompt archive tests 3 passed.
Implementation-head CI observed so far: Research reproducibility failed solely on the
designed report-count red (65 != 64; Ran 409 tests, failures=1, skipped=53); Application
baseline and OAP bootstrap acceptance in progress; OAP report history not yet posted. All
four required final-head checks are PENDING as strategic post-publication evidence.
Report counter advanced 64 -> 65 for final publication; no registry entry. One bounded
setup deviation is recorded (a single early Ruff run wrote the untracked, git-ignored
repository .ruff_cache; preserved as-is, later runs --no-cache). No scientific,
deployment, or acceptance change; no merge; PR #16 stays OPEN.

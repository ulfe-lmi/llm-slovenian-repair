# Work report 016-a - Read-only runtime evidence and completed-original fallback (objective 016, round 1; CREATE_NEW_PR; PR #18 open; branch retained)

```oap-report
{
  "id": "016-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/016-a-runtime-evidence-fallback.md",
  "order_sha256": "ead9d037ac69d44529a4741073c22129aa961ecd525db439539dd076d4d862f4",
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
  "implementation_head": "53143360a64ddc08b5670db51d912bd5028913ff",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 18,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/18",
  "pr_state": "open",
  "branch": "oap/016-runtime-evidence-fallback",
  "base_sha": "8d53923145ef0d36d845c6529fec790ccdbec7c2",
  "starting_remote_sha": "8d53923145ef0d36d845c6529fec790ccdbec7c2",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-27T01:22:44+00:00",
  "report_written_at": "2026-10-27T01:25:26+00:00",
  "checks": [
    {
      "command": "A1 - read-only direct-SQLite boundaries and actual-HTTP early failures (JSON + SSE)",
      "result": "PASSED",
      "details": "Direct real-SQLite: write/creation prohibition (database bytes unchanged; explicit write attempts raise), type-strict count validation across every query method (text/NULL/negative/fractional typed storage verified by typeof/count fixtures), valid-zero EXACT(0) and UNAVAILABLE/CENSORED scopes, escaped special-character absolute and relative paths, literal %00 filename, embedded NUL rejected before URI encoding, missing path still absent, directory and non-regular resources (owned anonymous pipe via /proc/self/fd, finite subprocess deadline with kill/reap) rejected without blocking, regular-file symlink/hardlink paths supported, WAL-journal index rejected before any SQLite open with no -wal/-shm auxiliary file (directory file set and bytes equal before/after; bounded HTTP polling samples complement the before-open proof), exclusive-lock degradation within the finite busy wait with PRAGMA busy_timeout 250 ms proven in effect, and handle closure on success and construction/context failure (real-FD observation). Actual HTTP (real ConceptProxy/engine/qualified Pandoc/SQLite, synthetic upstreams only): healthy JSON and SSE repairs make exactly one batch review call each; missing, corrupt, incompatible, text/NULL/negative/fractional-count and locked indexes each return HTTP 200 with the exact original bytes and zero review calls in both modes, with the index still absent or byte-unchanged.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "A2 - two-proposal late failure: whole-pass abort, actual call plus honest usage, persisted trace",
      "result": "PASSED",
      "details": "Two-proposal actual HTTP (t0 -> 'tako' accepted, t1 -> replacement carrying an invalid TEXT count): JSON (known usage 11/5/16) and SSE (usage unknown) both return HTTP 200 with the exact original bytes, exactly one review HTTP call, and no accepted edit; the actual usage observer records the call and usage (no rollback flag), and the actual persisted trace separately records the same rollback disposition (evidence_failure INVALID_COUNT/late, repaired == original, replacements [], every decision rewritten not-accepted with reason evidence-abort and replacement None, untrusted reviewer proposals retained). A neighboring ordinary missing replacement evidence ('to': EXACT word, no local bigram) rejects only that proposal while the valid first edit survives in both modes.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "A3 - recovery, canaries, retained assertions, ineligible main never opens evidence",
      "result": "PASSED",
      "details": "The same proxy recovers on the next healthy request with distinct observed usage (11/5/16 then 21/7/28) and no carryover of edits or usage; synthetic canary paths and count values are absent from response bodies, observer records, and persisted traces; all pre-existing 013/014/015 focused assertions are retained inside the 281-test run; a constructor spy proves an ineligible main (incomplete status, raw 503, malformed JSON) never constructs or opens the evidence index and the index stays absent.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Frozen governed sources and truthful documentation",
      "result": "PASSED",
      "details": "corpus.py, detector.py, repair.py, qwen_client.py, batch_review.py, responses_contract.py and pandoc_protection.py are byte-identical to the accepted base; the historical single-target evaluator prompt/API and frozen archive are unchanged. Directly affected docs updated (concept-verification/README.md new section; root README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md round statements). All 16 governance pins verify against disk; prior reports and orders byte-unchanged.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Focused verification suite (five modules)",
      "result": "PASSED",
      "details": "test_concept.py, test_pandoc_protection.py, test_review_batch.py, test_responses_contract.py and the new test_runtime_corpus.py: 281 passed, 107 subtests passed, on pre-commit dirty candidate bytes with the exact external Python 3.12 interpreter (-B, PYTHONDONTWRITEBYTECODE=1, REPAIR_ALLOW_LIVE_TESTS=NO) and the qualified official static Pandoc 3.7.0.2 in owned scratch. The five focused-tested Python files are blob-identical (verified by git blob comparison and independently re-verified against all 16 source hashes, receipt 016a-stable-focused-independent.json) to the implementation head, so the evidence is attributable to that head's tested-file bytes; it is not a run at any later commit.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Frozen strategic-prompt archive regression",
      "result": "PASSED",
      "details": "test_strategic_prompt_archive through unittest discovery: 3 passed, exact external Python 3.12 interpreter.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed Python files",
      "result": "PASSED",
      "details": "Ruff 0.16.6 with --no-cache clean on the five changed files (runtime_corpus.py, config.py, proxy.py, tests/test_runtime_corpus.py, tests/test_pandoc_protection.py). mypy 2.3.1 (strict, python_version 3.12) clean on the same five-file set (owned scratch shadow, real repository import context via MYPYPATH, --follow-imports=silent, --no-incremental, owned external cache); no import ignores added. Scope is the changed-file set, not the whole repository.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Offline research suite, tables, publication guard and OAP helpers at the implementation head",
      "result": "PASSED",
      "details": "Offline research unittest discovery (owned 700 private TMPDIR; umask 022 matching CI for the single mode-sensitive directory-mode test): Ran 409 tests, failures=1, skipped=53 - the sole failure is the designed pre-report count red (see report bookkeeping); no other failure. research.tools.rebuild_tables --check PASS; research.tools.publication_guard --root research PASS (6520 files). OAP helpers at the implementation head: check_transcript exit 0, check_whitespace PASSED with only the three tolerated historical incidents at both authorized bases, check_report_history exit 0 (report_count 67), check_governance exit 0 (structure valid, bootstrap mode).",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 66 -> 67 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed from 66 to 67 only; registry_entries 42, frozen_report_history_incidents 2 and all identity fields are unchanged. The designed implementation-head report-count red is confirmed by the observed CI: AssertionError 67 != 66, Ran 409 tests in 12.202s, FAILED (failures=1, skipped=53), no other failure; it clears at the final head with this report commit.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "Branch oap/016-runtime-evidence-fallback at 53143360a64ddc08b5670db51d912bd5028913ff (sole parent 8d53923145ef0d36d845c6529fec790ccdbec7c2) changes exactly the 14 authorized paths: concept-verification/{runtime_corpus.py (new), config.py, proxy.py, tests/test_runtime_corpus.py (new), tests/test_pandoc_protection.py, README.md}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins only; all 173 pins verified against disk), oap/active, the new 016-a order, and research/RESEARCH-STATE.md (counter only). git diff --check is clean; the tracked tree is clean at the head; the unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ remain unstaged and untouched.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "At report-writing time, at implementation head 5314336: Research reproducibility FAILED solely on the designed report-count red (67 != 66; Ran 409 tests in 12.202s; failures=1, skipped=53; no other failure). Application baseline and OAP bootstrap acceptance were still in progress. OAP report history posts at the report head.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "53143360a64ddc08b5670db51d912bd5028913ff",
      "publication_head_claim": false
    }
  ],
  "implementation": "New concept-verification/runtime_corpus.py: RuntimeCorpus(Corpus) runtime-only adapter (frozen corpus.py byte-identical): the exact configured path spelling (absolute or relative, percent-escaped including Unicode/spaces/#/?, no Python-level path resolution, no alternate-file search; ordinary regular-file symlink and hardlink spellings remain openable) opens as a percent-escaped absolute file URI with mode=ro, e.g. file:///home/op/corpus/index%20B.sqlite?mode=ro (never created, normalized, or written; no immutable/no-lock assumption), preceded by a bounded read-only header preflight (non-blocking open plus fstat rejects non-regular resources without blocking; SQLite magic; write/read version byte 1 rollback-journal required, byte 2 WAL rejected before open because even read-only access would persist -wal/-shm; any other header corrupt); finite 0.25 s per-query busy wait (PRAGMA busy_timeout 250 ms; not a total deadline); type-strict nonnegative Python-integer count validation (no int() repair/truncation/invented zero; EXACT(0)/UNAVAILABLE/CENSORED scopes preserved); six fixed content-free failure labels with at most an exception class name as detail; handles closed on success and construction/context failure. proxy.py: the evidence index opens only after a complete main passes eligibility (an ineligible main never opens or creates it); an early technical failure returns the exact completed original bytes with zero edits and zero review calls and a trace that records the evidence failure; a late per-proposal failure aborts the whole optional pass from the immutable original (all persisted decisions rewritten not-accepted/evidence-abort with replacement None, untrusted reviewer proposals kept separate, edits=[]) while preserving the actual review call and known/unknown usage (usage observer records calls/usage; the persisted trace records the aborted acceptance disposition and the evidence failure); ordinary missing replacement evidence remains an individual rejection; the same proxy recovers with no carryover. config.py: RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS = 0.25. Tests: new tests/test_runtime_corpus.py (direct real-SQLite boundaries plus actual proxy HTTP JSON/SSE with real engine/qualified Pandoc/SQLite and synthetic upstreams only); three test_pandoc_protection.py sentinels retargeted to RuntimeCorpus with all assertions preserved.",
  "documentation": "concept-verification/README.md gains a section documenting the read-only access contract (exact path spelling, read-only URI, header preflight with non-regular rejection without blocking and the rollback-journal format requirement, WAL rejection before open), the finite per-query busy wait versus a total deadline, type-strict count validation, the six content-free labels, and the completed-original fallback (early zero-call failures versus late whole-pass aborts preserving the actual review attempt and honest usage, with the usage observer and persisted trace described separately). README.md, STATUS.md, docs/READINESS.md and docs/IMPLEMENTATION-ROADMAP.md carry the directly affected round statements. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): actual-HTTP JSON/SSE healthy repair with exactly one fresh batch; early technical failures return 200 exact original and zero calls with the index unchanged or still absent; direct real-SQLite proves write prohibition, type-strict count validation across all query methods, valid zero/missing scopes, escaped paths, non-regular rejection without blocking, WAL rejection before open without auxiliary files, finite busy wait, and handle cleanup. A2 SATISFIED (observed): the two-proposal late failure aborts the whole optional pass from the immutable original in both modes with the actual single review call, known usage 11/5/16 and the unknown-usage case preserved, and the rollback disposition in the persisted trace; neighboring missing evidence rejects only that proposal. A3 SATISFIED (observed): same-proxy recovery with no carryover, canaries absent, all prior assertions retained, ineligible main never opens or creates the index. A4 PARTIALLY OBSERVED: frozen governed sources byte-identical, truthful docs, exact 14-path commit shape observed; the four required final-head CI checks are PENDING as recorded (strategic post-publication evidence).",
  "negative_paths": "No live endpoints, model processes, corpus acquisition/preparation, credential, service, port or network change; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no frozen research (corpus.py/detector.py/repair.py) or historical reviewer/prompt change; no registry entry; no deployment; no merge or auto-merge; no edits outside the ordered allowlist; no repository cache or .venv mutation beyond the recorded pytest cache deviation; unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ preserved and unstaged.",
  "boundary_fidelity": "Main capture/completion/ownership semantics, the 013-a mandatory Pandoc startup/version/mapping/protection behavior, the 014-a batch/acceptance contract, the 014-b terminal-copy preflight, and the 015-a request contract are preserved; all pre-existing 013/014/015 focused assertions remain (three sentinels retargeted to RuntimeCorpus with assertions unchanged). The change adds read-only runtime evidence access (rollback-journal format requirement, bounded non-regular rejection, finite per-query busy wait, type-strict counts) and the completed-original fallback distinguishing early zero-call failures from late whole-pass aborts that preserve the actual review attempt and honest usage; ordinary missing replacement evidence remains an individual rejection, and an ineligible main never opens or creates the index.",
  "setup": "External Python 3.12.15 interpreter (/home/janezp/envs/llm-slovenian-repair/bin/python) with -B and PYTHONDONTWRITEBYTECODE=1 for all ordered suites and OAP helpers; REPAIR_ALLOW_LIVE_TESTS=NO; OAP_ROLE=coding exported in helper command environments; umask 077 for private scratch (owned scratch under the strategic home, test-scratch-016a, dirs 700/files 600). Pandoc qualified read-only from the installer-owned official static archive 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229); no bare uv and no repository .venv writes. Bounded setup deviation (recorded, no CRIT): the focused pytest runs updated two existing git-ignored pytest cache files (.pytest_cache/v/cache/lastfailed and .pytest_cache/v/cache/nodeids); both are preserved as-is with no deletion, reset, or restoration claim (independent receipt 016a-pytest-cache-deviation-independent.json), and all 47 files of the pre-implementation pyc cache snapshot are unchanged with no new bytecode written (no py_compile used). The offline research suite ran under an owned 700 private TMPDIR; its single mode-sensitive directory-mode test is green only under the umask 022 matching CI, which is recorded rather than masked. Ruff used --no-cache throughout; mypy ran on an owned scratch copy with an owned external cache and the real repository import context.",
  "privacy": "Synthetic fixtures only (owned ephemeral loopback upstreams with fake keys, disposable SQLite indexes in owned scratch, owned anonymous pipes for the non-regular boundary - no filesystem FIFO created); no customer data, credential, private raw text, or private path in the report or logs; diagnostics are bounded fixed-label content-free reasons; private receipts are metadata-only (pre-mutation reproduction at the exact accepted base, focused-run logs and source hashes, independent strategic qualification receipts including the 42-case before-state, path-handling, first-wired, corrected 42/42, WAL and non-regular probes, the mypy shadow hash receipts, and the pytest cache deviation record).",
  "limits": "Focused suites and the named static analyses ran on pre-commit dirty candidate bytes at base 8d53923 (dirty-candidate limitation): the five focused-tested Python files are blob-identical to the committed implementation head 5314336 (verified by git blob comparison and independently re-verified against all 16 source hashes), so the evidence is attributable to that head's tested-file bytes rather than claimed as a later-SHA rerun. The pre-mutation reproduction ran at the exact accepted base 8d53923, so it is exact-SHA evidence for the pre-016-a behavior. The mypy scope is the five-file changed set with unchanged imported modules not re-reported (follow-imports=silent), not the whole repository; the Ruff scope is the five changed Python files. Independent strategic probes ran against stable dirty-candidate snapshots with recorded source hashes and are evidence for those candidates, not for a later commit. The offline research suite result at the implementation head includes the single designed pre-report count red (67 != 66), which clears with this report commit. All four required final report-head CI checks are PENDING and can only be recorded as strategic post-publication evidence.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: concept-verification/{runtime_corpus.py (new), config.py, proxy.py, tests/test_runtime_corpus.py (new), tests/test_pandoc_protection.py, README.md}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins), oap/active, the new 016-a order, research/RESEARCH-STATE.md (counter 66 -> 67 only), and this report. No other paths or governance changes.",
  "result_summary": "016-a implemented the read-only runtime evidence and completed-original fallback in the runnable concept-verification proxy (new branch, PR #18, CREATE_NEW_PR). The runtime SQLite index is now accessed strictly read-only through a new runtime-only adapter (exact configured path spelling, rollback-journal format requirement with a bounded pre-open header preflight, non-regular resources rejected without blocking, finite 0.25 s per-query busy wait, type-strict nonnegative integer counts, six fixed content-free labels, handles closed on success and failure), and technical evidence failure degrades safely: an early failure returns the exact completed original with zero review calls, a late per-proposal failure aborts the whole optional pass from the immutable original while preserving the actual review attempt and honest usage (usage observer plus persisted trace), and ordinary missing replacement evidence remains an individual rejection with no carryover. Focused verification (281 passed plus 107 subtests) ran on pre-commit dirty candidate bytes that are blob-identical to the implementation head; Ruff --no-cache and scoped strict mypy are clean on the five changed files; the frozen strategic-prompt archive passes unchanged. Implementation-head CI shows the designed pre-report count red only (67 != 66); all four required final-head checks are PENDING as strategic post-publication evidence. No scientific, deployment, or acceptance change; no merge; PR #18 stays OPEN pending strategy review."
}
```

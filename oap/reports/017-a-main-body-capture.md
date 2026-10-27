# Work report 017-a - UTF-8-safe main body capture with an elapsed body budget (objective 017, round 1; CREATE_NEW_PR; PR #19 open; branch retained)

```oap-report
{
  "id": "017-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/017-a-main-body-capture.md",
  "order_sha256": "e5ebcc5a5611f91ef4da596bebfc868447ece2b9ffc7f3d088955b4e6f86deed",
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
  "implementation_head": "2205f7667903f34e45678de24da8867797ba21ea",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 19,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/19",
  "pr_state": "open",
  "branch": "oap/017-main-body-capture",
  "base_sha": "fcec700488b8194c08ecc97fe48211239453a7ea",
  "starting_remote_sha": "fcec700488b8194c08ecc97fe48211239453a7ea",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-27T04:20:39+00:00",
  "report_written_at": "2026-10-27T04:23:21+00:00",
  "checks": [
    {
      "command": "A1 - pre-mutation reproduction and versioned capture regressions (actual HTTP JSON + SSE)",
      "result": "PASSED",
      "details": "Pre-mutation reproduction at the exact verified base fcec700 (order receipts 017-capture-current-head-diagnosis.json and 017-header-axis-unproven-diagnosis.json; stable five source hashes): actual proxy HTTP with the real engine/qualified Pandoc/SQLite/reviewer chain and synthetic upstreams only - a valid split-UTF8 SSE answer failed with 502 while identical whole bytes succeeded, and known-length body drips returned 200 after about 0.495 s despite the 0.15 s body budget (the declared-length branch read without an elapsed bound and a per-piece whole-buffer decode rejected incomplete codepoints), each with zero review calls; the earliest failure is in _bounded_read/_complete_prefix before protection or repair. Versioned regressions in the new test module: whole versus split-at-each-byte 2/3/4-byte Unicode, combining text, emoji, CRLF and SSE delimiters produce identical valid semantics; no-edit output is byte-identical; useful two-target repair preserves protected slices; bad/truncated UTF8 remains 502 with zero reviews.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "A2 - one elapsed body budget and separate byte bound (declared length, close-delimited, chunked)",
      "result": "PASSED",
      "details": "One finite positive monotonic deadline from collection entry applies to declared Content-Length, close-delimited and chunked delivery; byte arrivals never reset it; bool, nonfinite and nonpositive budgets are rejected before use. Actual HTTP: known-length JSON/SSE drips exceed the body budget and fail within a generous finite tolerance while fast identical bytes succeed; close-delimited and chunked bodies obey the elapsed and byte limits (MAIN_BODY_MAX_BYTES 8,000,000, independent of the deadline and of codepoints); the deadline covers HTTP chunk framing including multi-read chunk-size-line handling (fast fragmented size-line positive, slow size-line/trailer negatives); the body deadline anchor is measured separately from headers, and header-only drips remain explicit future work rather than a claimed bound.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "A3 - terminal, keepalive, over-read, failure semantics and cleanup",
      "result": "PASSED",
      "details": "Unknown-length SSE may terminate early at the terminal marker only; declared Content-Length bodies deliver every advertised byte, and early EOF before the declared length is a bounded main failure rather than a silent short read; invalid chunk framing at clean EOF is a bounded failure. Keepalive terminal completion without EOF and buffered over-read (headers plus body in one segment before the read begins) work. Incomplete events, the hard byte limit and declared-length truncation retain bounded main failures with zero review calls, proven by call-through observation (no Pandoc/corpus/detect before complete eligibility). All owned transport handles are closed in finally (response and connection). Hanging-producer negatives use finite parent deadlines with process-group kill/reap (measured wall time within tolerance, zero reviews, zero engine calls). Actual-TLS children (owned ephemeral certificate trusted only inside the test child via SSL_CERT_FILE) prove the same capture semantics over nonblocking TLS readiness, with SSLWantRead on buffered probes and direct reads treated as not-ready, never EOF; no producer/reviewer threads or tasks outlive the tests.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Frozen governed sources and truthful documentation",
      "result": "PASSED",
      "details": "corpus.py, detector.py, repair.py, qwen_client.py, batch_review.py, responses_contract.py, pandoc_protection.py, protected.py and runtime_corpus.py are byte-identical to the verified base; the historical single-target evaluator prompt/API and frozen archive are unchanged. Directly affected docs updated (concept-verification/README.md new section; root README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md round statements, including the distinction between the body budget and the unfinished overall/header/admission budgets). All 16 governance pins verify against disk; all 173 GENERATED-FILES pins verify; prior reports and orders byte-unchanged.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Focused verification suite (six modules)",
      "result": "PASSED",
      "details": "test_concept.py, test_pandoc_protection.py, test_review_batch.py, test_responses_contract.py, test_runtime_corpus.py and the new test_capture_transport.py: 316 passed, 107 subtests passed, on pre-commit dirty candidate bytes with the exact external Python 3.12 interpreter (-B, PYTHONDONTWRITEBYTECODE=1, pytest cache provider disabled, owned TMPDIR and PYTHONPYCACHEPREFIX) and the qualified official static Pandoc 3.7.0.2 in owned scratch. The four focused-tested Python files (proxy.py, config.py, capture_transport.py, test_capture_transport.py) are blob-identical to the implementation head (sha256 of committed content re-verified against the tested hashes), so the evidence is attributable to that head's tested-file bytes; it is not a run at any later commit.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Frozen strategic-prompt archive regression",
      "result": "PASSED",
      "details": "test_strategic_prompt_archive through unittest discovery: 3 passed, exact external Python 3.12 interpreter.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed Python files",
      "result": "PASSED",
      "details": "Ruff 0.16.6 with --no-cache clean on the four changed files (capture_transport.py, config.py, proxy.py, tests/test_capture_transport.py). mypy 2.3.1 (strict, python_version 3.12) clean on the same four-file set, including the new test module, using an owned minimal strict config (no tests override) with the real concept/src/repository import context via MYPYPATH on an owned byte-identical scratch shadow, --follow-imports=silent, and an owned external cache; no import ignores or relaxed strictness added. Scope is the four-file changed set, not the whole repository.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Offline research suite, tables, publication guard and OAP helpers at the implementation head",
      "result": "PASSED",
      "details": "Offline research unittest discovery (owned 700 private TMPDIR; test-process umask 022 matching CI for the single mode-sensitive directory-mode test): Ran 409 tests, failures=1, skipped=53 - the sole failure is the designed pre-report count red (see report bookkeeping); no other failure. research.tools.rebuild_tables --check PASS; research.tools.publication_guard --root research PASS (6520 files). OAP helpers at the implementation head: check_transcript exit 0 (revision mode, active 017-a, report_count 68), check_whitespace PASSED at both authorized bases with only the three tolerated historical incidents, check_report_history exit 0 (report_count 68), check_governance exit 0 (structure valid, bootstrap mode).",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 67 -> 68 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed from 67 to 68 only; registry_entries 42, frozen_report_history_incidents 2 and all identity fields are unchanged. The designed implementation-head report-count red is confirmed by the observed CI: AssertionError 68 != 67 at research/tests/test_research_state_consistency.py line 216, Ran 409 tests in 6.463s, FAILED (failures=1, skipped=53), no other failure; it clears at the final head with this report commit.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "Branch oap/017-main-body-capture at 2205f7667903f34e45678de24da8867797ba21ea (sole parent fcec700488b8194c08ecc97fe48211239453a7ea) changes exactly the 13 authorized paths: concept-verification/{capture_transport.py (new), proxy.py, config.py, tests/test_capture_transport.py (new), README.md}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins only; all 173 pins verified against disk), oap/active, the new 017-a order, and research/RESEARCH-STATE.md (counter only). git diff --check is clean; the tracked tree is clean at the head; the unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ remain unstaged and untouched.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "At report-writing time, at implementation head 2205f76: Research reproducibility FAILED solely on the designed report-count red (68 != 67; Ran 409 tests in 6.463s; failures=1, skipped=53; no other failure). Application baseline and OAP bootstrap acceptance were still in progress; OAP report history at this head is SUCCESS. Report-head reruns post-publication are PENDING.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "2205f7667903f34e45678de24da8867797ba21ea",
      "publication_head_claim": false
    }
  ],
  "implementation": "New concept-verification/capture_transport.py: bounded main-body capture with one finite positive monotonic deadline validated before use (bool, nonfinite and nonpositive budgets rejected) and anchored at collection entry, applying uniformly to declared Content-Length, close-delimited and chunked delivery; byte arrivals never reset it and blocking reads/waits respect the remaining time through a typed per-step read helper (peek-gated read1 then optimistic nonblocking recv; BlockingIOError, InterruptedError and SSLWantReadError are not-ready states, never EOF, covering nonblocking TLS buffered-probe and direct-read readiness; select waits bounded by the remaining budget); a separate raw-byte bound (MAIN_BODY_MAX_BYTES, 8,000,000) independent of the deadline and of codepoints; UTF-8 split-tail preservation (one-to-three-byte live tail, no partial-codepoint decode, raw bytes/Unicode/CRLF preserved, SSE delimiters tolerated across chunks) with strict rejection of genuinely invalid or truncated encodings (no ignore/replacement decoding, no normalization, no substring recovery, no answer regeneration); bounded owned chunked framing (size line and trailer line byte caps, line-count cap, byte-hex pattern; valid framing preserved rather than rejected); declared-length bodies deliver every advertised byte (early EOF before the declared length is a bounded failure) while only unknown-length SSE may terminate early at the terminal marker; body timeout, hard limit, premature EOF, incomplete SSE and malformed main remain bounded main failures. proxy.py: _bounded_read delegates to the collector and maps capture failures to bounded ProxyError before any protection/repair/detect work; the timeout is validated before bind allocation; forward() closes the response and connection in finally. config.py: MAIN_BODY_MAX_BYTES = 8,000,000. Tests: new tests/test_capture_transport.py (35 tests) - pre-mutation reproduction, whole versus split-at-each-byte 2/3/4-byte Unicode, combining text, emoji, CRLF and SSE-delimiter identity, no-edit byte identity, useful two-target repair preserving protected slices, elapsed and byte budgets across declared-length/close-delimited/chunked, keepalive, buffered over-read, finite-parent hung-producer kill/reap negatives, and actual-TLS children with an owned ephemeral certificate.",
  "documentation": "concept-verification/README.md documents UTF-8/framing preservation, the elapsed body budget versus the separate byte bound, terminal/keepalive behavior, and main-failure semantics, explicitly distinguishing the body budget from the unfinished overall request deadline and from header/connection/DNS deadlines (future work) and from admission/cancellation (unimplemented). README.md, STATUS.md, docs/READINESS.md and docs/IMPLEMENTATION-ROADMAP.md carry the directly affected round statements. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): actual-HTTP known-length JSON/SSE drips exceed the body budget and fail within a generous finite tolerance while fast identical bytes succeed; close-delimited/chunked bodies obey the elapsed and byte limits; the body deadline anchor is measured separately from headers. A2 SATISFIED (observed): whole versus split-at-each-byte 2/3/4-byte Unicode, combining text, emoji, CRLF and SSE delimiters produce identical valid semantics; no-edit output is byte-identical; useful two-target repair preserves protected slices; bad/truncated UTF8 remains 502 with zero reviews. A3 SATISFIED (observed): keepalive terminal completion and buffered over-read work; incomplete events, hard limits and declared-length truncation retain bounded failures with zero review calls; negative blocking regressions use finite parent deadlines with kill/reap/cleanup and no producer/reviewer threads or tasks outlive the tests. A4 PARTIALLY OBSERVED: the prior 281 tests plus 107 subtests (superseded by 316 plus 107 with the new module) and frozen/governed sources remain intact, docs are truthful, the exact 13-path commit shape is observed; the four required final-head CI checks are PENDING as recorded (strategic post-publication evidence).",
  "negative_paths": "No live endpoints, model processes, corpus acquisition/preparation, credential, service, port or network change; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no frozen research (corpus.py/detector.py/repair.py) or historical reviewer/prompt change; no registry entry; no deployment; no merge or auto-merge; no edits outside the ordered allowlist; no new repository cache or .venv writes during the 017 window (all 47 baseline mixed cache/bytecode files byte-identical before and after verification); unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ preserved and unstaged.",
  "boundary_fidelity": "Main completion/ownership semantics, the 013-a mandatory Pandoc startup/version/mapping/protection behavior, the 014-a batch/acceptance contract, the 014-b terminal-copy preflight, the 015-a request contract and the 016-a runtime-evidence fallback are preserved; all pre-existing 013/014/015/016 focused assertions remain inside the 316-test run. The change repairs main BODY collection after headers are available only: UTF-8-safe split preservation, one elapsed body budget, a separate byte bound, and bounded chunked framing; it adds no parser substitution, no global deadline, and no new API capability; header/connection/DNS deadlines, admission/cancellation and whole review/CPU budgets remain explicitly unfinished.",
  "setup": "External Python 3.12.15 interpreter (/home/janezp/envs/llm-slovenian-repair/bin/python) with -B and PYTHONDONTWRITEBYTECODE=1 for all ordered suites and OAP helpers; REPAIR_ALLOW_LIVE_TESTS=NO; OAP_ROLE=coding exported in helper command environments; umask 077 for private scratch (owned scratch test-scratch-017a under the strategic home, dirs 700/files 600). Pandoc qualified read-only from the installer-owned official static archive 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229); no bare uv and no repository .venv writes. Cache census (bounded, recorded): all 47 baseline mixed cache/bytecode files (including the 9 pyc files) are byte-identical by SHA256, mtime_ns and size between the pre-implementation 017 baseline and post-verification (receipt 017a-post-verification-cache-check.json; baseline 017a-pre-implementation-cache-snapshot.json); the two .pytest_cache lastfailed/nodeids changes were introduced in round 016, already disclosed there, and are preserved as-is; no new 017 cache or .venv writes (pytest cache provider disabled, Ruff --no-cache, owned PYCACHEPREFIX). The offline research suite ran under an owned 700 private TMPDIR; its single mode-sensitive directory-mode test is green only under the umask 022 matching CI, which is recorded rather than masked. Ruff used --no-cache throughout; mypy ran on an owned scratch shadow with an owned external cache and the real repository import context.",
  "privacy": "Synthetic fixtures only (owned ephemeral loopback upstreams with fake keys, disposable SQLite indexes in owned scratch, owned ephemeral TLS certificate pair generated in owned scratch and trusted only inside test child processes); no customer data, credential, private raw text, or private path in the report or logs; diagnostics are bounded fixed-label content-free reasons; private receipts are metadata-only (pre-mutation reproduction at the exact verified base, focused-run logs and source hashes, and independent strategic qualification receipts including the 28-case capture matrix, in-flight findings and fixture corrections, the TLS matrices, the finite-parent diagnostic cleanup record, the header-axis unproven note, and the cache census records - no raw answer text).",
  "limits": "Focused suites and the named static analyses ran on pre-commit dirty candidate bytes at base fcec700 (dirty-candidate limitation): the four focused-tested Python files are blob-identical to the committed implementation head 2205f76 (sha256 of committed content re-verified against the tested hashes), so the evidence is attributable to that head's tested-file bytes rather than claimed as a later-SHA rerun. The pre-mutation reproduction ran at the exact verified base fcec700, so it is exact-SHA evidence for the pre-017-a behavior. The mypy scope is the four-file changed set (including the new test module) with unchanged imported modules not re-reported (follow-imports=silent), not the whole repository; the Ruff scope is the four changed Python files. Independent strategic probes ran against stable dirty-candidate and implementation snapshots with recorded source hashes and are evidence for those candidates, not for a later commit; the actual 28-case proxy HTTP and 20-case TLS qualification matrices are component evidence, not acceptance or final-CI proof. The body budget is one elapsed body-collection deadline plus a separate byte bound; header/connection/DNS deadlines, admission/cancellation and whole global budgets remain unimplemented. The offline research suite result at the implementation head includes the single designed pre-report count red (68 != 67), which clears with this report commit. All four required final report-head CI checks are PENDING and can only be recorded as strategic post-publication evidence.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: concept-verification/{capture_transport.py (new), proxy.py, config.py, tests/test_capture_transport.py (new), README.md}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins), oap/active, the new 017-a order, research/RESEARCH-STATE.md (counter 67 -> 68 only), and this report. No other paths or governance changes.",
  "result_summary": "017-a implemented UTF-8-safe main body capture with an elapsed body budget in the runnable concept-verification proxy (new branch, PR #19, CREATE_NEW_PR). Main body collection after headers is now safe under arbitrary wire fragmentation: split 2/3/4-byte codepoints, combining text, emoji, CRLF and SSE delimiters preserve valid semantics (no partial-codepoint decode, no ignore/replacement decoding, normalization, substring recovery or answer regeneration); one finite positive monotonic body deadline from collection entry bounds declared-length, close-delimited and chunked delivery (byte arrivals never reset it; a separate 8,000,000-byte raw bound is independent of the deadline); chunked framing is bounded and valid framing preserved; declared-length bodies deliver every advertised byte while only unknown-length SSE may terminate early at the terminal marker; body timeout, hard limit, premature EOF and incomplete or truncated UTF8 remain bounded main failures with zero review calls and all owned transport handles closed. Focused verification (316 passed plus 107 subtests) ran on pre-commit dirty candidate bytes blob-identical to the implementation head; Ruff --no-cache and scoped strict mypy (including the new test module) are clean on the four changed files; the frozen strategic-prompt archive passes unchanged. Implementation-head CI shows only the designed pre-report count red (68 != 67); all four required final-head checks are PENDING as strategic post-publication evidence. No scientific, deployment, or acceptance change; no merge; PR #19 stays OPEN pending strategy review."
}
```

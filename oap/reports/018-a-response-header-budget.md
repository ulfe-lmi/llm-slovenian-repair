# Work report 018-a - Independent elapsed response-header budget (objective 018, round 1; CREATE_NEW_PR; PR #20 open; branch retained)

```oap-report
{
  "id": "018-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/018-a-response-header-budget.md",
  "order_sha256": "f09de188c0c3e6dfe75ed0a74928a0daba0093733720fd8d0604772cfac2d5fb",
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
  "implementation_head": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 20,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/20",
  "pr_state": "open",
  "branch": "oap/018-response-header-budget",
  "base_sha": "29ae4c1424da1140026796f7ef6129c11531106e",
  "starting_remote_sha": "29ae4c1424da1140026796f7ef6129c11531106e",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-27T06:42:20+00:00",
  "report_written_at": "2026-10-27T07:10:00+00:00",
  "checks": [
    {
      "command": "A1 - pre-mutation reproduction and versioned header regressions (actual HTTP JSON + SSE)",
      "result": "PASSED",
      "details": "Pre-mutation reproduction at the exact verified base 29ae4c1 (order receipt 018-header-prerequisite-at-017-final.json; stable six source hashes): actual proxy HTTP with the real engine/qualified Pandoc/SQLite/reviewer chain and synthetic upstreams only - fast headers plus fast body 200 in about 0.034/0.009 s (JSON/SSE) while header drips plus the same fast body returned 200 in about 0.534/0.576 s despite the 0.15 s socket/body budget, with original bytes and zero reviews: the header phase was unbounded. Versioned regressions in the new test module: actual-HTTP slow status-line and slow header-line JSON/SSE negatives fail 502 within generous finite tolerances with zero engine.repair calls (call-through observation at the actual engine boundary) and zero reviewer calls while fast identical bytes succeed; the interim-100 drip expires at the deadline with a within-budget 100-to-final positive control.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "A2 - header/body budget independence in both directions and useful repair",
      "result": "PASSED",
      "details": "One absolute monotonic header deadline anchored immediately before acquisition (before the owned guard starts): guard-start overhead is not concealed (a 0.12 s delayed status delivery still expires under a 0.03 s budget), and byte arrival and legitimate interim 100 responses never reset it; bool, nonnumeric, nonfinite and nonpositive budgets are rejected before bind and re-validated at helper use. The CONCEPT_TIMEOUT body budget begins later and stays independent in both directions over actual proxy HTTP: a body arriving after the header budget but within a generous body budget succeeds, and slow headers under a generous header budget with a short body budget succeed; buffered over-read, terminal keepalive and declared-framing semantics are preserved. Useful JSON/SSE two-target repair runs under the header budget with one isolated batch and exact original spans, real 2/3/4-byte wire Unicode, and protected code, TeX, HTML, link and an NFC-unstable decomposed/combining line kept intact (decomposed line on its own separate paragraph); both modes assert the exact composed final answer and the raw protected wire markers.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "A3 - races, recovery, other-connection isolation and owned cleanup",
      "result": "PASSED",
      "details": "Completion versus expiration is explicit: a racing or late parser return after the deadline is explicitly closed and never transferred (completion racing expiration loses to expiration), proven by an observer over the real stdlib begin on owned sockets with the exception retained. Expiration recovery: the same proxy returns exact original 502 bytes and then serves the next healthy request normally; no guard threads outlive any acquisition. Other-connection isolation: while A's guard is armed and expires, B's headers are fast but B's body is delivered only after A's acquisition has finished and is read through B's real owned transport - an already-buffered body would not discriminate, so it is deliberately not used - and the concurrent other-proxy case keeps h2 genuinely in flight through h1's armed-guard window with a delayed body past h1's expiry: h1 zero analysis, h2 exact original 200 with zero reviewer calls on the no-suspicion path; the guard only ever touches the exact captured owned socket. A hanging main upstream that never sends a status fails at the short header budget with a generous socket/body budget (502, zero engine, zero review) under a finite parent deadline with process-group kill/reap; the real-TLS matrix (owned ephemeral certificate trusted only inside the child) shows the same fast/slow header semantics over nonblocking TLS.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Frozen governed sources and truthful documentation",
      "result": "PASSED",
      "details": "capture_transport.py, corpus.py, runtime_corpus.py, detector.py, repair.py, qwen_client.py, batch_review.py, responses_contract.py, pandoc_protection.py, protected.py, protection_residuals.py and all six prior focused test modules are byte-identical to the verified base (review-plan hash verification); the historical single-target evaluator prompt/API and frozen archive are unchanged. Directly affected docs updated (concept-verification/README.md new section; root README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md round statements), now separating the keyword-only header_timeout constructor parameter from the CONCEPT_HEADER_TIMEOUT environment value and stating that DNS resolution, connect and request upload occur before header acquisition and stay outside the header budget. All 16 governance pins verify against disk; all 173 GENERATED-FILES pins verify; prior reports and orders byte-unchanged.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Focused verification suite (seven modules)",
      "result": "PASSED",
      "details": "test_concept.py, test_pandoc_protection.py, test_review_batch.py, test_responses_contract.py, test_runtime_corpus.py, test_capture_transport.py and the new test_header_transport.py (34 tests): 350 passed, 107 subtests passed, on pre-commit dirty candidate bytes with the exact external Python 3.12 interpreter (-B, PYTHONDONTWRITEBYTECODE=1, pytest cache provider disabled, owned TMPDIR and PYTHONPYCACHEPREFIX) and the qualified official static Pandoc 3.7.0.2 in owned scratch. The four focused-tested Python files (proxy.py, config.py, header_transport.py, tests/test_header_transport.py) are blob-identical to the implementation head by sha256, so the evidence is attributable to that head's tested-file bytes; it is not a run at any later commit.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Frozen strategic-prompt archive regression",
      "result": "PASSED",
      "details": "test_strategic_prompt_archive through unittest discovery at the implementation head: 3 passed, exact external Python 3.12 interpreter.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed Python files",
      "result": "PASSED",
      "details": "Ruff with --no-cache clean on the four changed files (header_transport.py, config.py, proxy.py, tests/test_header_transport.py). mypy (strict, python_version 3.12) clean on the same four-file set, including the new test module, using an owned minimal strict config (no tests override) with the real concept/src/repository import context via MYPYPATH on an owned byte-identical scratch shadow, follow-imports silent, and an owned external cache; no import ignores or relaxed strictness added. Scope is the four-file changed set, not the whole repository.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Offline research suite, tables, publication guard and OAP helpers at the implementation head",
      "result": "PASSED",
      "details": "Offline research unittest discovery at the implementation head (owned 700 private TMPDIR; test-process umask 022 matching CI for the single mode-sensitive directory-mode test): Ran 409 tests, failures=1, skipped=53 - the sole failure is the designed pre-report count red (see report bookkeeping); no other failure. research.tools.rebuild_tables --check PASS; research.tools.publication_guard --root research PASS (6520 files). OAP helpers at the implementation head: transcript valid (revision mode, active 018-a, report_count 69), check_whitespace PASSED at both authorized bases with only the three tolerated historical incidents.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 68 -> 69 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed from 68 to 69 only; registry_entries 42, frozen_report_history_incidents 2 and all identity fields are unchanged. The designed implementation-head report-count red is confirmed by observed CI at both implementation heads: AssertionError 69 != 68 at research/tests/test_research_state_consistency.py line 216, Ran 409 tests, FAILED (failures=1, skipped=53), no other failure; it clears at the final head with this report commit.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "Branch oap/018-response-header-budget at 76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e changes exactly the 13 authorized paths in two commits: the initial 13-path implementation commit (sole parent 29ae4c1424da1140026796f7ef6129c11531106e) and one in-flight 5-path correction commit (test_header_transport.py A3 transport proof, concept-verification/README.md, README.md, STATUS.md, oap/GENERATED-FILES.json) - concept-verification/{header_transport.py (new), proxy.py, config.py, tests/test_header_transport.py (new), README.md}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins only; all 173 pins verified against disk), oap/active, the new 018-a order, and research/RESEARCH-STATE.md (counter only). git diff --check is clean; the tracked tree is clean at the head; the unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ remain unstaged and untouched.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "At final implementation head 76aa688: Research reproducibility FAILED solely on the designed report-count red (69 != 68; Ran 409 tests in 7.170s; failures=1, skipped=53; no other failure); Application baseline and OAP bootstrap acceptance were still in progress and OAP report history not yet observed at report-writing time. At the earlier implementation commit 3bd5d20: OAP bootstrap acceptance SUCCESS (12m02s); Application baseline FAILED solely on the same designed count red (1 failed, 1144 passed, 58 skipped, 255 subtests passed in 1137.76s; focused contract tests and cleanup PASSED); Research reproducibility likewise solely the designed red. Report-head reruns post-publication are PENDING.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
      "publication_head_claim": false
    }
  ],
  "implementation": "New concept-verification/header_transport.py: one finite positive monotonic header deadline validated before use (bool, nonnumeric, nonfinite and nonpositive budgets rejected) and anchored immediately before getresponse acquisition (before the owned guard starts), so guard startup overhead is not concealed; byte arrival and legitimate interim 100 responses never reset it. The stdlib getresponse parser is retained unchanged and runs on the owning calling thread; the owned guard is a pure timer owning only a bounded event wait plus a shutdown of the exact captured owned socket object, cancelled and actually joined on both success and failure before any classification or transfer, so no header work outlives acquisition and no other owned connection is touched; a racing or late parser return after the deadline is explicitly closed and never transferred. proxy.py: the keyword-only header_timeout parameter is appended after the existing positional parameters (existing positional order and signature preserved), validated and stored before any bind allocation, and forward() acquires the response through the helper before the 017 body collector begins; main() reads CONCEPT_HEADER_TIMEOUT with the ordered default. config.py: MAIN_HEADER_TIMEOUT_SECONDS = 30.0. Tests: new tests/test_header_transport.py (34 tests) - direct stdlib getresponse guard boundaries (delayed guard-start startup overhead, racing-completion explicit close on owned sockets, interim-100, no late timer, unbuffered post-expiry other-connection isolation, setup and transport errors), constructor/main() wiring on owned loopback port 0 (invalid budgets observed to never bind), actual proxy HTTP fast/slow/interim-100/independence/recovery/isolation cases with a useful two-target repair, a real-TLS matrix child, and a hanging-header child with a finite parent deadline and process-group kill/reap.",
  "documentation": "concept-verification/README.md documents the header configuration (constructor parameter header_timeout versus the CONCEPT_HEADER_TIMEOUT environment value), the elapsed header budget versus the independent body/socket/reviewer settings, stdlib parsing and guard ownership/cleanup, failure semantics, and the explicitly unfinished axes, now worded so that DNS resolution, connect and request upload occur before header acquisition and stay outside the header budget. README.md, STATUS.md, docs/READINESS.md and docs/IMPLEMENTATION-ROADMAP.md carry the directly affected round statements. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): actual-HTTP and real-TLS fast-header positives versus slow status-line/header-line negatives within generous finite tolerances, zero engine/review before eligible capture (call-through at the engine boundary), and the interim-100 deadline plus positive control. A2 SATISFIED (observed): header/body budget independence in both directions over actual proxy HTTP; buffered over-read, terminal keepalive and declared framing retained; useful JSON/SSE two-target repair with exact original spans, real wire UTF-8 and protected code/TeX/HTML/link and a separate NFC-unstable decomposed line intact. A3 SATISFIED (observed): delayed guard-start startup overhead, racing-completion explicit close, expiration recovery on the same proxy, other-connection isolation with B's unbuffered body delivered after A's expiry and read through B's real transport, other-proxy overlap with a delayed body, no guard threads outliving acquisition, and finite parent deadline/kill/reap for the blocking child; configuration exercised on owned loopback port 0 only. A4 PARTIALLY OBSERVED: the prior 316 tests plus 107 subtests (superseded by 350 plus 107 with the new module) and frozen/governed sources remain intact, docs are truthful, and the exact 13-path commit shape is observed; the four required final-head CI checks are PENDING as recorded (strategic post-publication evidence).",
  "negative_paths": "No live endpoints, model processes, corpus acquisition/preparation, credential, service, port or network change; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no frozen research (corpus.py/detector.py/repair.py) or historical reviewer/prompt change; no registry entry; no deployment; no merge or auto-merge; no edits outside the ordered allowlist; no new repository cache or .venv writes during the 018 window (all 47 baseline mixed cache/bytecode files byte-identical before and after verification at the final head); unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ preserved and unstaged.",
  "boundary_fidelity": "Main completion/ownership semantics, the 013-a mandatory Pandoc startup/version/mapping/protection behavior, the 014-a batch/acceptance contract, the 014-b terminal-copy preflight, the 015-a request contract, the 016-a runtime-evidence fallback and the 017-a body-capture contract are preserved; all pre-existing focused assertions remain inside the 350-test run. The change bounds main response STATUS/HEADER acquisition after connection.request has returned only: one elapsed header budget with explicit completion/expiration semantics and owned guard cleanup; it adds no parser substitution, no end-to-end request deadline, no DNS/connect/upload change and no new API capability; incoming client timeouts, reviewer-total, total wall-clock, admission, fairness, disconnect, cancellation, CPU, quality and packaging boundaries remain explicitly unfinished.",
  "setup": "Qualified external Python 3.12.15 interpreter with -B and PYTHONDONTWRITEBYTECODE=1 for all ordered suites and OAP helpers; OAP_ROLE=coding exported in helper command environments; umask 077 for private scratch (owned scratch test-scratch-018a under the strategic home, dirs 700/files 600). Pandoc qualified read-only from the installer-owned official static archive 3.7.0.2 (qualification hash recorded privately); no bare uv and no repository .venv writes. Cache census (bounded, recorded): all 47 baseline mixed cache/bytecode files (including the 9 pyc files) are byte-identical by SHA256, mtime_ns and size between the pre-verification snapshot and post-verification at the final implementation head; the two .pytest_cache lastfailed/nodeids changes were introduced in round 016, already disclosed there, and are preserved as-is; no new 018 cache or .venv writes (pytest cache provider disabled, Ruff --no-cache, owned PYCACHEPREFIX). The offline research suite ran under an owned 700 private TMPDIR; its single mode-sensitive directory-mode test is green only under the umask 022 matching CI, which is recorded rather than masked. Ruff used --no-cache throughout; mypy ran on an owned scratch shadow with an owned external cache and the real repository import context.",
  "privacy": "Synthetic fixtures only (owned ephemeral loopback upstreams with fake keys, disposable SQLite indexes in owned scratch, owned ephemeral TLS certificate pair generated in owned scratch and trusted only inside test child processes); no customer data, credential, private raw text, or private path in the report or logs; diagnostics are bounded fixed-label content-free reasons; private receipts are metadata-only, including 018-header-prerequisite-at-017-final.json, 018a-independent-review-plan.json, 018a-header-startup-draft-finding.json, 018a-late-response-draft-finding.json, 018a-isolation-buffer-proof-gap.json, 018a-own-pre-mutation-repro.json, 018a-partial-test-draft-strict.json, 018a-complete-header-draft-independent.json, 018a-recovery-fixture-discriminator.json and 018a-racing-test-fixture-finding.json - no raw answer text.",
  "limits": "Focused suites and the named static analyses ran on pre-commit dirty candidate bytes at base 29ae4c1 (dirty-candidate limitation): the four focused-tested Python files are blob-identical to the committed final implementation head 76aa688 by sha256, so the evidence is attributable to that head's tested-file bytes rather than claimed as a later-SHA rerun; the offline research suite, frozen-prompt archive, tables, publication guard and OAP helper checks ran at the committed implementation head. The pre-mutation reproduction ran at the exact verified base 29ae4c1, so it is exact-SHA evidence for the pre-018-a behavior. The mypy scope is the four-file changed set (including the new test module) with unchanged imported modules not re-reported (follow-imports silent), not the whole repository; the Ruff scope is the four changed Python files. Independent strategic probes ran against stable dirty-candidate and implementation snapshots with recorded source hashes and are evidence for those candidates, not for a later commit; the actual proxy HTTP and real-TLS qualification matrices are component evidence, not acceptance or final-CI proof. The header budget bounds only the elapsed STATUS/HEADER acquisition phase; DNS resolution, connect and request upload occur before acquisition, and incoming client timeouts, reviewer-total, total wall-clock, admission, fairness, disconnect, cancellation, CPU, quality and packaging boundaries remain unimplemented. The offline research suite result at the implementation head includes the single designed pre-report count red (69 != 68), which clears with this report commit. All four required final report-head CI checks are PENDING and can only be recorded as strategic post-publication evidence.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: concept-verification/{header_transport.py (new), proxy.py, config.py, tests/test_header_transport.py (new), README.md}, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (four changed manifest pins), oap/active, the new 018-a order, research/RESEARCH-STATE.md (counter 68 -> 69 only), and this report. No other paths or governance changes.",
  "result_summary": "018-a implemented the independent elapsed response-header budget in the runnable concept-verification proxy (new branch, PR #20, CREATE_NEW_PR). Main response STATUS/HEADER acquisition is now bounded by one finite positive monotonic header deadline anchored immediately before acquisition (before the owned guard starts): guard startup overhead is not concealed, and byte arrival and legitimate interim 100 responses never reset it; the keyword-only header_timeout constructor parameter (main() reads CONCEPT_HEADER_TIMEOUT, default 30 s) is validated before any bind allocation; the stdlib getresponse parser is retained unchanged on the owning thread, and the owned pure-timer guard interrupts only the exact captured socket and is cancelled and actually joined on both success and failure before any transfer, so no header work outlives acquisition and no other owned connection is touched; a racing or late parser return is explicitly closed and never transferred; bounded header failures return 502 with zero review calls and zero engine analysis (call-through at the engine boundary) and the same proxy recovers; the CONCEPT_TIMEOUT body budget remains independent in both directions. Focused verification (350 passed plus 107 subtests) ran on pre-commit dirty candidate bytes blob-identical to the final implementation head; Ruff --no-cache and scoped strict mypy (including the new test module) are clean on the four changed files; the frozen strategic-prompt archive passes unchanged; the offline research suite at the implementation head shows only the designed pre-report count red (69 != 68). Implementation-head CI observed so far shows the same designed count red as the sole failure where completed. No scientific, deployment, or acceptance change; no merge; PR #20 stays OPEN pending strategy review."
}
```

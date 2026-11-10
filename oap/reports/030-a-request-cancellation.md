# Work report 030-a — request-scoped cancellation on client disconnect (round 1; implemented, qualified, PR 32 OPEN)

**Result: COMPLETE** - round 030-a implements request-scoped cancellation in the runnable concept-verification proxy for client disconnects observed AFTER the fully valid ingress, until final delivery, exactly as ordered in `oap/orders/030-a-request-cancellation.md` (26605 B, SHA 3289918ba4f7667665eae21d2cd7ecf5ac314d52a6059288223064a6acd5612c). Final scope: nine Python paths (the seven modified existing files proxy.py, upstream_setup.py, header_transport.py, capture_transport.py, review_transport.py, pandoc_protection.py, runtime_corpus.py - delivery_transport.py frozen, its delivery-entry cooperation in the Handler - plus the two NEW files request_lifecycle.py and tests/test_request_cancellation.py); the other 46 concept Python files byte-frozen against accepted base 556b9ef21abecc621c9a134c544ae1cdf7010ad8 (the head after PR 31's merge). NEW final stable full-19: 931 passed plus 350 subtests in 633.77 s, literal returncode 0, all 55 source maps stable; strict9 mypy and Ruff9 clean; shared OAP helper checks pass; the only retained red is the designed pre-report research count (85 vs 84, reconciles after SELF); final-head CI is NOT RUN at the currently known I2 head (the final head will be the future canonical report commit, whose SHA is unknown in this preflight), and all four required final-head checks run after the real report publication. This report is held as an unpublished preflight for root exact-byte approval before the canonical sole-report SELF commit (sole parent = implementation head), push, remote verification and ONE response. No canonical publication has been made.

## Chronology (honest; no old-case replay)

Implementation iterations produced actual failures, closed across sixteen root review batches; each root-verified at its recorded epoch (receipts preserved, none replayed). Epoch markers below (ecebc04e, 3c616c07, 0f0d6471, ebf332) are file-content hash prefixes of the observed source tree, not Git SHAs:

1-11: first-caller control, dispatch marker, small-tests-first, join cleanup, pure capability, shared actual-join, native header wake + owned response, body hook 50 ms slice, setup socket leak, Pandoc RUNNER-ONLY + qualified explicit binary (R9 no-new-Any kept the Popen observer fully typed; the initial Any/IO[Any] was not an authorized relaxation), and the late AFTER-upload handoff fixture boundaries (direct-handler fixture POSTs first and drives the real Handler once; stimuli injected inside adopt; truthful labels; tearDown joins owned threads).
12: four actual native handoff failures under R5/R6/R7/R8 (2-for-1 POST count; 2 usage records for 1 POST; ROFD leak after the real corpus ctor; Handler passing unrelated ambient MemoryError to the finisher / suppressing the new cleanup control) - CLOSED at ecebc04e.
13: two R5 controls (first MemoryError not 502'd; real corpus close later-Memory replaces first KeyboardInterrupt) - CLOSED at 3c616c07.
14: native 12-case priority matrix (one corpus condition: first_control nonNone used as authority) - all 12 PASS at 0f0d6471.
15: late-handoff NEW fixture boundaries (ctor-before-POST closed streams early; pre-cancel matrix never opened Corpus; recovery review endpoint never replied) - CLOSED in the NEW module only, root-verified; its 13 strict9 errors fixed with fully-typed seams (no Any/ignore/noqa).
16: FINAL semantic review - ONE missing actual `run_review_exchange` pre-dispatch entry check (existing R4/R7): Root's actual native three-case proof showed healthy child1/POST1/200/reaped, while preset-cancel AND post-REAL-frame-cancel both wrongly spawned child1/marker-TRUE before stopping (POST 0). Fix: `raise_if_cancelled()` at the post-pure-frame/pre-marker/pre-launch boundary before `mark_review_dispatch_attempted()` - an already-observed pre-dispatch cancellation propagates with zero child, zero POST, marker false; pure frame/body bounds preserved. Plus the factual request_lifecycle.py docstring/ScopeSlot correction (owner-thread consumers: final-forward waits, Pandoc runner, RuntimeCorpus ctor, reviewer exchange - not the reviewer alone) and NEW `_ReviewExchangePreDispatchTests` (3 tests: healthy child/POST/200/kernel-reap control + both zero-child negative handoffs). The green full-19 at the pre-fix bytes is preserved as the earlier-epoch pass (check 7, superseded); the final-bytes full-19 is the stable claim (check 6). The pre-fix three-case exchange diagnostic intentionally exposed the two negative failures; its pre-fix JSON is not a PASS proof - the post-fix ebf332 replay is check 1, cited separately from the strict9/Ruff9 and final-931 receipts.
After final qualification, one consolidated R10 documentation-only factual correction (root I3e188/PR32 work order: the disconnect-only mask 0x2038/8248 with POLLRDHUP, the control-priority rule, the exact nine-path scope, the NVAL watcher-stop semantics, the Handler containment of the dedicated RequestCancelled, the quiet-close/transport-evidence wording and the 030 seed remap) was applied as forward docs-only commit I2 with the four doc pins re-pinned - no Python change, no test/static repeat.

Boundary attribution, never kill: cross-test child PIDs 3914648/3914670 observed in early iterations; origins UNPROVEN (lifetime belongs to their own owner); no guessed PID was ever killed.

## Verification provenance

Checks 1-8 and 11 were executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 (M29, the merge commit after PR 31) with the then-uncommitted source55 working tree (DIRTY); the branch head moved to I 3e188b0e2c2d1e22c4c4bb61a026868a3502f3d7 only after the final test runs, so they are not literal re-runs at I or I2. Committed equivalence is the 55-file source maps: the before/after maps around the final-931 run and the map re-taken at I2 (I2-55-EQUIVALENT) all carry sha256 2b3419789e530dc0af31c7020c229a675590cb6ca304b97b539e1672006cd30b, i.e. the Python bytes at I and I2 are byte-identical to the tested bytes; no test or static repeat was performed for the I2 prose delta. Checks 9, 10 and 13 were literally re-run or read back at I2 eb8a53be51bbf6508bf87b4d758395c053115d00; check 12 records the earlier read-back made when the head was I. The earlier-epoch pass (check 7) and the failed epoch (check 8) are preserved at their actual earlier source epochs, not claimed at the final bytes.

```oap-report
{
  "id": "030-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/030-a-request-cancellation.md",
  "order_sha256": "3289918ba4f7667665eae21d2cd7ecf5ac314d52a6059288223064a6acd5612c",
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
  "implementation_head": "eb8a53be51bbf6508bf87b4d758395c053115d00",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 32,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/32",
  "pr_state": "open",
  "branch": "oap/030-request-cancellation",
  "base_sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
  "starting_remote_sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-10T14:04:51+00:00",
  "report_written_at": "2026-11-10T14:07:04+00:00",
  "implementation": "Nine Python paths on oap/030-request-cancellation: NEW concept-verification/request_lifecycle.py (one request-local cancellation scope per fully admitted valid request, an exact accepted-socket watcher on the disconnect-only native poll mask POLLRDHUP|POLLHUP|POLLERR|POLLNVAL = 8248/0x2038 that deliberately excludes POLLIN, a bounded synchronous first check for already-disconnected queued clients, and the pre-dispatch reviewer-exchange guard) and NEW concept-verification/tests/test_request_cancellation.py; phase-cooperation hooks in exactly seven existing files proxy.py, upstream_setup.py, header_transport.py, capture_transport.py, review_transport.py, pandoc_protection.py (owned runner only) and runtime_corpus.py. delivery_transport.py is frozen; its delivery-entry cooperation is in the Handler. A dedicated RequestCancelled is contained before the ordinary 502/fallback and admission-worker boundary, with owned child/HTTP/pipes/corpus/guard cleanup, request-local 0/1 review counting and one content-free operator observation.",
  "documentation": "Five current docs state the actual 030 behavior (README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md); oap/GENERATED-FILES.json keeps the same 173 keys with only the four existing doc pins; research/RESEARCH-STATE.md advances oap_reports_reviewed 84 to 85 only (registry 42 and incidents 2 unchanged). The forward docs-only commit I2 corrected six factual items (disconnect-only mask 0x2038/8248 with POLLRDHUP, the control-priority rule, the exact nine-path scope, NVAL watcher-stop semantics, Handler containment of RequestCancelled, seed-remap wording); no Python change, no test/static repeat.",
  "criteria": "A1: actual accepted-socket FIN/RST before headers and during body stops owned main/delivery and prevents later review (actual TCP integration in the new module plus Root native RST receipts); an already-started actual review stays one honest attempt with the child reaped (checks 1-3, 6). A2: native disconnect-only mask with no tail reads and no data spin; the fully valid SHUT_WR half-close is documented as unsupported; incomplete-body SHUT_WR 400 and trailing-open first-response semantics are preserved (checks 2, 6). A3: one content-free observation with correct 0/1 and known-or-unknown usage on abort; scope 55 with stable before/after maps, frozen 46 files and all 18 old test modules exact; focused and final stable 19 suites plus strict9/Ruff9 on recorded actual bytes with honest failed/interim epochs (checks 1-8, 10, 11). A4: five docs, seed remap, 173 keys/4 pins, one actual PR 32, chronological private report and Root exact-byte approval BEFORE canonical sole-report SELF, forward push, normal remote verification and ONE response; Root independently requires all four final-head CI successes before any expected-head development merge (checks 9-14).",
  "negative_paths": "Proved negative paths: pre-dispatch cancellation (preset and post-real-frame) propagates with zero child, zero POST and false dispatch marker (check 1); a queued cancellation cannot later start main; foreign request/resource isolation; no tail drain/read/forward and no data-readiness spin behind unread ignored bytes (native mask proof in the new module); incomplete-body SHUT_WR still 400; the fully valid SHUT_WR half-close is documented unsupported rather than silently supported; a canceled request emits no second status/retry, no orphan review and no cross-request state; the quiet client close is expected and is established by separate actual TCP transport tests, not by the bounded unit-phase rows.",
  "boundary_fidelity": "The remaining 46 accepted concept-verification Python files and all 18 old test modules stay byte-frozen against accepted base 556b9ef21abecc621c9a134c544ae1cdf7010ad8 (55-file before/after maps stable, check 6); delivery_transport.py, request_admission.py, evidence_budget.py, config.py, qwen_client.py, the detectors and the acceptance/composition/patch/protection classifiers and defaults are untouched. strict9 ran fresh byte-identical flat shadows under minimal Python 3.12 strict with no Any/type-ignore/per-file relaxation (check 4); Ruff ran the actual nine paths with the explicit root pyproject and no cache (check 5). The initial Any/IO[Any] in the new test was removed as an unauthorized relaxation; the Popen observer remains fully typed.",
  "setup": "Qualified Python 3.12.15 with -B and the explicitly installed Pandoc 3.7.0.2 (SHA 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229), no PATH discovery; ordinary finite owned test children on loopback port 0 only; one adopted foreground pane with explicit OAP_ROLE=coding, no restart, subagents or new panes. Some generated task artifacts required subsequent permission repair: Root recorded exact task-only 0700/0600 mode reconciliation with unchanged content hashes, and preserved then relocated the three specifically identified temporary/bytecode artifacts into private storage. This does not retroactively claim that every historical shell command set umask 077. Subsequent helpers must explicitly set OAP_ROLE=coding, actual shell umask 077, and private temporary/cache/bytecode paths.",
  "privacy": "No raw customer text, prompts, credentials or private service configuration in code, logs or this report; public prose uses logical roots (STRATEGIC_HOME and artifact names) instead of physical machine paths, which belong only in the versioned workspace layout; the operator observation is content-free; tiny owned synthetic literals remain only inside their tests.",
  "limits": "Scope is 55 Python files and 19 test modules total; every existing independent absolute deadline, quota, query schedule and phase clock is preserved; no new quota, deadline, retry or budget was added; the final stable 19 suite ran in 633.77 s with literal returncode 0; no live model call and no network/service/deployment change.",
  "human_gates": "Decision NONE under D0 classification; no separate human evaluation dataset (excluded, not deferred); no additional human approval step for this round. Root is the strategic agent: its exact-byte report review is delegated internal review before canonical SELF, push, remote verification and ONE response. The human retains final milestone labeling and release/deployment authority; none is claimed here.",
  "scope": "Exactly nine Python paths: seven modified existing (proxy.py, upstream_setup.py, header_transport.py, capture_transport.py, review_transport.py, pandoc_protection.py owned runner only, runtime_corpus.py) plus two NEW (request_lifecycle.py, tests/test_request_cancellation.py); five docs; the exact order and oap/active; GENERATED-FILES.json with 173 keys and four doc pins; research counter 84 to 85 only; one new PR (number 32); the eventual sole report. No other path mutation.",
  "checks": [
    {
      "command": "Focused 16th-review regressions: _ReviewExchangePreDispatchTests (3 new) plus the two existing pre-dispatch regressions",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "5 passed in 3.44 s, exit 0 (log sha256 c6ba998af8b99567b4e2215aaa3966cf7c7b0dd83dc220a5e65385d9f71ec519). The post-fix ebf332 replay (file-content epoch prefix, not a Git SHA); executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with the then-uncommitted source55 working tree (DIRTY); committed-byte equivalence to I and I2 via the 55-file source maps (checks 6 and 10). Healthy: real owned child (real pid, rc 0, kernel waitpid reap proof, /proc gone), one POST, 200, marker true, zero survivors. Both negative handoffs: RequestCancelled, zero Popen, marker false, zero POST, no new children, empty FD delta. Manual phase-cancellation stimuli, not native RST claims; actual FIN/RST proofs live in _ProxyIntegrationTests and Root's native RST receipts."
    },
    {
      "command": "New focused module test_request_cancellation.py alone",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "63 passed plus 13 subtests in 29.72 s, exit 0 (log sha256 88bbc15e9f8a6bc1a5779fc18222ceaf17f5a4981b3e8fe02cf76d778bbba7f5). Executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with the then-uncommitted source55 working tree (DIRTY); committed-byte equivalence to I and I2 via the 55-file source maps (checks 6 and 10)."
    },
    {
      "command": "Named focused set (new module plus test_owned_startup/test_evidence_budget/test_client_transport/test_review_batch.py; ordered A3/R9)",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "316 passed plus 93 subtests in 200.22 s, exit 0 (log sha256 d10e75c5b9824edf2eca205837002881cea594af0c4d283c0724fdea88c001b1). Executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with the then-uncommitted source55 working tree (DIRTY); committed-byte equivalence to I and I2 via the 55-file source maps (checks 6 and 10)."
    },
    {
      "command": "Strict9 mypy plus seven-file precheck shadow (fresh byte-identical flat shadows, minimal Python 3.12 strict, follow_imports silent, actual import path, fresh caches, no Any/type-ignore/relaxation)",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "9-file shadow: no issues found (log sha256 46984ca20bf69f7b14ec1fd9bd82101d56a4e109e68f016fd2a04f22481b09b3); precheck shadow: no issues (log sha256 050c52a2b0c61e8b681ef5c485e0bc03340b8d55148e0acef27d744c8be42033). Executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with the then-uncommitted source55 working tree (DIRTY); committed-byte equivalence to I and I2 via the 55-file source maps (checks 6 and 10)."
    },
    {
      "command": "Ruff9 (actual nine paths, cwd repo root, explicit root pyproject, --no-cache, ruff 0.16.6)",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "All checks passed (log sha256 82b3e6a6c090a57601d22943bd23fca9218d1031dbe5a7b754092f9a156b4f18). Executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with the then-uncommitted source55 working tree (DIRTY); committed-byte equivalence to I and I2 via the 55-file source maps (checks 6 and 10)."
    },
    {
      "command": "NEW final stable full-19 (all 19 test modules; ordered A3) by Python subprocess",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "931 passed plus 350 subtests in 633.77 s, literal pytest returncode 0 (full stdout log sha256 46854dcfdea64f64cdfbeda59ed89d0882dd418915013c0bf04d14fdb580a300); all 55 source maps byte-stable before/after (both maps sha256 2b3419789e530dc0af31c7020c229a675590cb6ca304b97b539e1672006cd30b). Executed at literal accepted-main HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 (M29, the merge after PR 31) with the then-uncommitted source55 working tree (DIRTY); the branch head moved to I only after the final runs, so this is not a literal I/I2 re-run - committed equivalence is the 55-file source maps at I and I2 (checks 6 and 10). Qualified Pandoc 3.7.0.2 and Python 3.12.15, no PATH discovery."
    },
    {
      "command": "INTERIM full-19 at the pre-16th-fix source epoch (preserved earlier-epoch evidence)",
      "result": "PASSED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "928 passed plus 350 subtests in 622.52 s, exit 0 (log sha256 cbfc3f82d0a12866aa96c66c9e5d04046005e5ccfd44ec27397c353692d7e3b; 55-map sha256 50a083c329fbc0972f788cfa10556c300a7f34ce7c4f2d0620c4666eddd5dd3b at those bytes). Truthful interim pass: a real pass at the earlier pre-16th-fix source epoch, captured at literal HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with DIRTY pre-fix bytes; superseded by the check 6 final-bytes pass, never relabeled and not claimed at the final bytes. The root final review demonstrated the missing R4/R7 pre-dispatch check at these bytes (child1 + marker TRUE before stopping, POST 0)."
    },
    {
      "command": "Earlier failed full-19 at the pre-twelfth-fix source epoch (preserved failed epoch)",
      "result": "FAILED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "5 failed / 918 passed / 341 subtests (log sha256 99f5f76d21a8bf1f08559182fadd2a096bd61cadd2995823b2d4e69e69f403ab), executed at literal HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with DIRTY pre-twelfth-fix bytes. Honest attribution: two frozen delivery tests failing from the incompatible cancelled= forward keyword (the pre-supplement call shape) plus three NEW global-child fixture assertions - not the full-suite manifestation of the four later native handoff failures. Preserved, not replayed."
    },
    {
      "command": "Shared OAP helper checks re-run at docs-only head I2",
      "result": "PASSED",
      "sha": "eb8a53be51bbf6508bf87b4d758395c053115d00",
      "publication_head_claim": false,
      "details": "All exit 0 on literal re-run at I2 eb8a53be51bbf6508bf87b4d758395c053115d00 (also exit 0 earlier at I): check_governance accepted-runtime (trusted 3549de2a), check_transcript --index --expected-id 030-a and --revision HEAD, check_report_history --revision HEAD --require-manifest, check_whitespace at both accepted bases (four pinned historical diagnostics), git diff --check clean; all 173 manifest pins verified, bad: none. The four doc pins re-pinned to the I2 bytes; same 173 keys."
    },
    {
      "command": "Docs-only forward commit I2: exact delta, Python-55 byte equivalence, four doc pins",
      "result": "PASSED",
      "sha": "eb8a53be51bbf6508bf87b4d758395c053115d00",
      "publication_head_claim": false,
      "details": "I2 eb8a53be51bbf6508bf87b4d758395c053115d00 is a forward docs-only non-report commit on the same branch/PR 32 (no amend/force): exactly 6 files (README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json), 13 line changes, touching only the round-030-a doc text and the four doc pins. All 55 source maps at I2 are byte-identical to the final-931 after-map (I2-55-EQUIVALENT, map sha256 2b3419789e530dc0af31c7020c229a675590cb6ca304b97b539e1672006cd30b), so the Python bytes at I2 are byte-identical to the tested final bytes and no pytest/static repeat was performed for prose. Research counter 85, registry 42, incidents 2 unchanged."
    },
    {
      "command": "Research state consistency (unittest discover research/tests test_research_state_consistency.py)",
      "result": "FAILED",
      "sha": "556b9ef21abecc621c9a134c544ae1cdf7010ad8",
      "publication_head_claim": false,
      "details": "11 tests, 10 ok, 1 failed: test_registry_and_report_counts 85 != 84 - the designed pre-report red (counter advanced 84 -> 85 for final publication; reconciles after the sole-report SELF commit); registry_entries 42 and incidents 2 unchanged. Executed at literal HEAD 556b9ef21abecc621c9a134c544ae1cdf7010ad8 with DIRTY working tree (the counter change was then uncommitted); the research files are byte-identical between I and I2 (I2 is docs-only), so the result stands at I2 without a repeat. No counter or test change; the Research CI at I failed only because the anticipated report count 85 exceeds the currently published count 84, and final-head CI is required only after real report publication."
    },
    {
      "command": "PR 32 observed when the head was I",
      "result": "PASSED",
      "sha": "3e188b0e2c2d1e22c4c4bb61a026868a3502f3d7",
      "publication_head_claim": false,
      "details": "GitHub API read-back at report time: number 32, head 3e188b0e2c2d1e22c4c4bb61a026868a3502f3d7, base main, OPEN, MERGEABLE, created 2026-11-10T13:25:15Z, auto_merge absent, mergeCommit null. Single new PR for objective 030, pushed before the report per C-REPORT-01. Superseded head observation; check 13 records the head I2."
    },
    {
      "command": "PR 32 observed at the implementation head I2",
      "result": "PASSED",
      "sha": "eb8a53be51bbf6508bf87b4d758395c053115d00",
      "publication_head_claim": false,
      "details": "GitHub API read-back at I2: number 32, head oap/030-request-cancellation at eb8a53be51bbf6508bf87b4d758395c053115d00, base main, OPEN. The R10-corrected PR body (mask 0x2038/8248, nine-path scope, control-priority rule, NVAL semantics, Handler containment, quiet-close wording) was persisted via the GitHub REST API PATCH and read back byte-identical (4743 chars; gh pr edit was blocked by a repository projects-classic GraphQL deprecation error, so the REST PATCH was used). Single new PR for objective 030; no merge, no auto-merge. Implementation-head identity evidence, not a future publication or CI claim."
    },
    {
      "command": "Final report-head CI at the future canonical report commit (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history)",
      "result": "NOT RUN",
      "sha": "eb8a53be51bbf6508bf87b4d758395c053115d00",
      "publication_head_claim": false,
      "details": "Not run and not claimed: at the currently known implementation head I2 the final head does not yet exist - it will be the future canonical sole-report commit, whose SHA is unknown in this preflight (no fabricated future SHA). The four required final-head checks run after real report publication; no future push/CI success is claimed here."
    }
  ]
}
```

## Publication state

- Implementation heads: I `3e188b0e2c2d1e22c4c4bb61a026868a3502f3d7` (the non-report work commit: exact order, active, nine Python paths, five docs, four doc pins, research counter; 18 files, 6099 insertions) and I2 `eb8a53be51bbf6508bf87b4d758395c053115d00` (forward docs-only R10 fact corrections + four doc pins); the canonical sole-report commit will have I2 as sole parent.
- PR 32 OPEN at I2, base main; no merge, no auto-merge; the R10-corrected body is persisted and read back byte-identical. This preflight is an unpublished private draft at the STRATEGIC_HOME task-scratch store (test-scratch-030a/030a-report-preflight-draft.md); it is not in the canonical oap/reports path, not committed, not pushed, and no SELF response has been sent.
- Resource truth: the round-owned scratch baseline-head worktree and /tmp/old_class.txt were removed during this round (not claimed preserved); the immutable M29 diagnostic logs and Root receipts remain; the original uploaded 2.5 GB archive is preserved content-addressed under STRATEGIC_HOME research-preservation-20261025 (archive 2e5ae391f9b9e1aeade621b6a5bb7650c8193e8c760303a9897e6c13c499347a-missing.tar.gz, 2498407179 B, with receipts; the /tmp upload absence is not data loss); Root byte-verified and copied the remaining /tmp/new_pandoc_class.txt (6934 B, SHA f4dec99967cedb6e334902c0bf7b6188693818fba3a3020b3817733f69814709) into the STRATEGIC_HOME task-scratch preserved-task-artifacts store - Root recorded the bounded subsequent task-artifact preservation and permission reconciliation privately; coding performed no further cleanup.
- After root exact-byte approval: the canonical sole-report commit changes only this report file, has I2 as sole parent; push; independent remote head/bytes/parent/path verification; then the ONE response and exit. No later mutation/push for this round.
- Zero scientific model calls; no native Qwen, linguistic quality, research, dataset, MVP or deployment acceptance in this round. The documented-unsupported fully valid SHUT_WR half-close is stated as such in the docs; the quiet client close is expected, and the actual TCP FIN/RST tests establish the transport event separately (the direct-Handler and manual-Event rows are bounded unit phase evidence, not native peer RST proof). The ordered remap replaces the inert initial 030 morphology-calibration seed with this cancellation gap - the historical seed remains unexecuted and no calibration/packaging/research/human-dataset gate is introduced.

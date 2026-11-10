# Work report 029-a — runtime word/phrase target selection (halted before any product change)

**Result: PARTIAL** - strategy halted the 029-a product implementation before the first product change after the root actual-source finding that the preserved read-only index (7991296 bytes) has zero known bigram/trigram counts at or below the issued absolute threshold (bigram/trigram minimum 2270, unigram minimum 272), making the issued weak-context route of R3/R4 unreachable on that source. This round is a docs-only safe prerequisite/publication round: the exact immutable 029-a order and active, five current docs, the four allowed doc pins (same 173 keys) and the research counter 82 -> 83. All 51 concept Python files and all 17 test modules remain byte-equal to the accepted base 915c349; the real runtime selector remains the frozen raw detector's rare/unknown single-word behavior; the corrected same-PR round 029-b will be ordered after verified 029-a publication. The observed local check failure is the designed pre-report research count (83 vs82), expected to clear when the valid report is included; actual post-publication verification is still required. Canonical sole-path SELF publication, normal REMOTE proof and final-head CI are pending as written. Root reviewed the actor draft and prepared this copy, preserving the original privately.

Round 029-a (objective 029, round 1) publishes the halted ordered round on branch `oap/029-runtime-detection` from the exact accepted base 915c349939e1f57b759549cfd361113e25f80329 (one forward commit bdbe89d, nine scoped non-report paths; PR 31 OPEN at that head).

```oap-report
{
  "id": "029-a",
  "result": "PARTIAL",
  "order_path": "oap/orders/029-a-runtime-detection.md",
  "order_sha256": "f097f298326527682c5e8b22a0b51c0063d6012af9ba01d4b8f056929520b233",
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
  "implementation_head": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 31,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/31",
  "pr_state": "open",
  "branch": "oap/029-runtime-detection",
  "base_sha": "915c349939e1f57b759549cfd361113e25f80329",
  "starting_remote_sha": "915c349939e1f57b759549cfd361113e25f80329",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-10T01:27:30Z",
  "report_written_at": "2026-11-10T01:34:25.332767+00:00",
  "checks": [
    {
      "command": "Pre-change baseline focused 3 modules (test_runtime_acceptance, test_composed_validation, test_runtime_corpus) at base HEAD 915c349, before any change",
      "result": "PASSED",
      "sha": "915c349939e1f57b759549cfd361113e25f80329",
      "publication_head_claim": false,
      "details": "117 passed, 20 subtests in 49.48 s; qualified Python 3.12.15 -B, qualified Pandoc 3.7.0.2, private scratch, -p no:cacheprovider. Pre-change baseline only, not new-producer proof."
    },
    {
      "command": "Pre-change baseline focused 4 modules (test_evidence_budget, test_review_batch, test_analysis_policy, test_pandoc_protection) at base HEAD 915c349, before any change",
      "result": "PASSED",
      "sha": "915c349939e1f57b759549cfd361113e25f80329",
      "publication_head_claim": false,
      "details": "273 passed, 101 subtests in 104.02 s; same environment; pre-change baseline only."
    },
    {
      "command": "Actor accepted-runtime governance check at trusted3549de2a436f485a693730d0ee7d5f8c00aec0c0 during the staged-index epoch",
      "result": "PASSED",
      "sha": "915c349939e1f57b759549cfd361113e25f80329",
      "publication_head_claim": false,
      "details": "structure valid; semantic_proof and human_authorization_proof false; coding_bytes 36770."
    },
    {
      "command": "Transcript --index --expected-id 029-a at the staged-index epoch (staged tree equals the HEAD bdbe89d tree)",
      "result": "PASSED",
      "sha": "915c349939e1f57b759549cfd361113e25f80329",
      "publication_head_claim": false,
      "details": "valid; active 029-a; latest order 029-a; quarantined set unchanged (007-d, 007-n, 008-d)."
    },
    {
      "command": "Report history --index --require-manifest at the staged-index epoch",
      "result": "PASSED",
      "sha": "915c349939e1f57b759549cfd361113e25f80329",
      "publication_head_claim": false,
      "details": "valid; 83 raw report files vs 82 counted valid reports (the 029-a report is unpublished by design); the two known frozen historical incidents unchanged."
    },
    {
      "command": "Research state consistency (unittest discover research/tests test_research_state_consistency.py) at the staged-index epoch",
      "result": "FAILED",
      "sha": "915c349939e1f57b759549cfd361113e25f80329",
      "publication_head_claim": false,
      "details": "11 tests, 10 ok, 1 failed in 1.38 s: test_registry_and_report_counts 83 != 82 - the designed pre-report red (oap_reports_reviewed 83 before the actual 029-a report publication); it is expected to clear when the valid A report is included; actual post-publication verification is still required. registry_entries 42 and frozen_report_history_incidents 2 unchanged; all other consistency tests pass."
    },
    {
      "command": "Whitespace check at both accepted bases (2832fa1e and 82ea1e6f) --revision HEAD bdbe89d",
      "result": "PASSED",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "Both bases PASSED with exactly the four pinned historical diagnostics (007-e, 007-f, 027-a order, 007-d); no new incident."
    },
    {
      "command": "Transcript --revision HEAD bdbe89d and worktree git diff --check",
      "result": "PASSED",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "valid (active 029-a); diff --check clean for the worktree and for the commit."
    },
    {
      "command": "All-51 source byte equality against base 915c349 plus 173 manifest pins (bytes and sha256) at HEAD bdbe89d",
      "result": "PASSED",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "All 51 concept Python files byte-equal to the accepted base (private before-map; root interim receipt 029a-root-interim-docs-and-source-preservation-review-20261110.json confirms source51_all_base_equal); 173 manifest keys unchanged with exactly the four allowed doc pins changed; the three untracked roots and PR 13 preserved."
    },
    {
      "command": "New focused test_runtime_detection.py (ordered R6/R7)",
      "result": "NOT RUN",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "Module not written: strategy halted the 029-a product implementation before the first product change after the root actual-source finding."
    },
    {
      "command": "Broader full-18 suite (ordered A3)",
      "result": "NOT RUN",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "No 18th test module exists (implementation halted); no redundant full-suite rerun performed for an unchanged 17."
    },
    {
      "command": "Strict3 and Ruff3 over the scoped Python paths (ordered A3)",
      "result": "NOT RUN",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "No scoped Python path was written or changed (docs-only round)."
    },
    {
      "command": "Final report-head CI (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history)",
      "result": "PENDING",
      "sha": "bdbe89d84d36d19e8f175cd05f851b339b55266d",
      "publication_head_claim": false,
      "details": "At the future SELF head after canonical publication; no future pass claims are made in this report."
    }
  ],
  "implementation": "NONE for the ordered product scope. The ordered implementation (new concept-verification/runtime_detection.py, new concept-verification/tests/test_runtime_detection.py, import routing only in concept-verification/proxy.py; planned final scope 53 Python files / 18 test modules) was halted by strategy before the first product change after the root actual-source finding on the preserved read-only index (SHA-256 f769235b6af3412e65f0875f4d08231c832f60d8630b43a06ab927c2d32c739f, 7991296 bytes): unigram minimum 272, bigram/trigram minimum 2270, ZERO known counts 0..3 in any table, so the issued absolute at-most-threshold-3 weak-context route of R3/R4 is unreachable on that source. Root took responsibility for the initial threshold mistake. The source proof is source-support only (the legacy detector selected zero only in the qualified known-word and adjacent-phrase controls; unknown words remain eligible for the raw detector); no broad old-detector-zero, native, quality or MVP claim is made. All 51 concept Python files and all 17 test modules remain byte-equal to the accepted base 915c349; the real runtime selector remains the frozen raw detector's rare/unknown single-word behavior.",
  "documentation": "Single forward commit bdbe89d on oap/029-runtime-detection from the exact accepted base 915c349 (the nine scoped non-report paths): the exact immutable 029-a order and oap/active (029-a); five current docs (README.md rounds clause, STATUS.md round entry, concept-verification/README.md halted-section, docs/READINESS.md rounds line, docs/IMPLEMENTATION-ROADMAP.md coverage note) plainly state that the A implementation was halted after the Root source-incompatibility finding, that the real selector remains the rare/unknown single-word detector, and that the corrected same-PR round 029-b (context selector on the existing all-token evidence without an absolute count cutoff) will be ordered after verified 029-a publication; oap/GENERATED-FILES.json keeps the same 173 keys with only the four allowed doc pins re-pinned; research/RESEARCH-STATE.md advances oap_reports_reviewed 82 -> 83 only (registry 42 and incidents 2 unchanged). One precise STATUS overclaim fix (legacy-detector zero qualified to the actual controls) was applied before commit with only the STATUS pin re-pinned.",
  "criteria": "A1 UNMET: no new runtime word/phrase producer. A2 PARTIAL: all51 existing Python files and17 test modules remain base-equal, but the ordered new gates/bounds tests were not written. A3 NOT MET: new focused tests/full18/strict3/Ruff3 NOT RUN after Root halted implementation; actual pre-change baseline and shared checks are separately recorded. A4 PARTIAL: accurate docs/order/active/173 pins/one actual PR and private preflight exist; canonical SELF publication, normal REMOTE proof, final-head CI and strategic disposition remain pending as written. New producer requirements and proofs are NOT IMPLEMENTED. Inspection, source preservation and docs/publication prerequisites do not substitute for unmet product acceptance.",
  "negative_paths": "The stop itself is the failure cause: the issued FINAL 029-a heuristic cannot activate on the actual preserved source (zero known counts 0..3 in any table; bigram/trigram minimum 2270). The designed pre-report research count red (83 != 82) is preserved as an actual FAILED at the implementation head and clears only at the actual A report publication - no prior PASS is fabricated and the counter is not changed to force green. The one STATUS overclaim (legacy detector zero) was corrected to the precise qualified-controls wording before commit. No fake module, no fake test pass, no 53/18 final-scope claim, no new-rule substitution under the immutable A order, no B implementation.",
  "boundary_fidelity": "All 51 concept Python files and all 17 test modules are byte-equal to the accepted base 915c349 at the implementation head (private before-map plus Root immutable-commit verification receipt029a-root-bdbe89d-committed-scope-and-source-preservation-review-20261110.json); the existing parser, strict acceptance, raw detector, 50 other Python files, all defaults, budgets, transports, reviewer, config and research code are untouched. The committed delta is exactly the nine scoped non-report paths (five docs, manifest, research counter, order, active). The three untracked roots (.rclone-speed-test/, .research-test-scratch/, corpus/) and the unrelated open PR 13 are preserved; no reset/clean/stash/amend/force.",
  "setup": "Qualified Python3.12.15 -B and explicit Pandoc3.7.0.2/SHA02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229 for the controlled baseline; PYTHONDONTWRITEBYTECODE=1, private TMPDIR/PYTHONPYCACHEPREFIX and pytest -p no:cacheprovider selected there. Helpers explicitly use OAP_ROLE=coding. Owner-launched CODEX_HOME/auth/session unchanged, no global configuration changes or cache cleanup. Existing ignored caches are preserved; this report makes no blanket claim that repository caches are absent.",
  "privacy": "No product/scientific model requests or live product-Qwen qualification, no customer data or new human evaluation dataset, no acquisition/GPU/service/network-configuration/deployment changes. The existing foreground coding model operated normally, including a transient provider/tool-contract retry; that is separate from product-model testing. Owned loopback test traffic and authorized GitHub operations occurred. No customer text, private corpus word keys, raw product review prompts/responses or credentials are published here. Only count-level diagnostic facts and logical roots are reported; owned synthetic test literals remain permitted.",
  "limits": "Result PARTIAL at the halted boundary: no product change of any kind; the ordered word/phrase selector does not exist; the real runtime selector remains the rare/unknown single-word detector; the corrected same-PR round 029-b will be ordered after verified 029-a publication (a private B draft exists but is not active and was not read as an order). The four final report-head CI checks are PENDING at the future SELF head; no functional-MVP, linguistic-quality, live-Qwen, packaged-library, ICA or deployment acceptance is claimed; no merge or auto-merge.",
  "human_gates": "DecisionNONE; no CRIT entries or new DHA gate for this docs-only partial round. The same-PR correction is delegated strategic engineering, not a request for another human decision. Separate native live-test opt-in/configuration and deployment/exposure authority remain ungranted by this report. No human milestone or quality acceptance is claimed.",
  "scope": "Exactly the nine scoped non-report paths in one forward commit bdbe89d84d36d19e8f175cd05f851b339b55266d on branch oap/029-runtime-detection (parent 915c349939e1f57b759549cfd361113e25f80329): README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json, research/RESEARCH-STATE.md, oap/orders/029-a-runtime-detection.md and oap/active. One actual new PR 31 (CREATE_NEW_PR, OPEN, MERGEABLE, created 2026-11-10T01:27:15Z, observed 2026-11-10T01:27:30Z, head bdbe89d on main). The canonical sole report path oap/reports/029-a-runtime-detection.md is reserved for the root-approved bytes and is not yet created; no later mutation or push is planned for this round beyond the approved SELF publication. No merge, no auto-merge.",
  "editorial_review": "Root reviewed the actor private draft and prepared this exact publication copy; the original16465-byte draft is preserved privately. This copy corrects acceptance status, future-count wording, cache absence, product-model/privacy scope and source-receipt attribution. As-written publication_verified remainsfalse; later publication/CI evidence belongs in separate private receipts."
}
```

````oap-report
{
 "id": "037-a",
 "result": "COMPLETE",
 "order_path": "oap/orders/037-a-slaif-documentation.md",
 "order_sha256": "f7e0ad875e90bcab240c8f55d650c7fa44a4bfce8e6dcb7596c286133e1c638d",
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
 "implementation_head": "520be2ad262ca55d4c83134a23e0651adc7875c6",
 "publication_verified": false,
 "pr_mode": "CREATE_NEW_PR",
 "pr": 40,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/40",
 "pr_state": "open",
 "branch": "oap/037-slaif-documentation",
 "base_sha": "987fdb9ed07856d735f1e684f8af342461bf5236",
 "starting_remote_sha": "987fdb9ed07856d735f1e684f8af342461bf5236",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-13T03:24:15+00:00",
 "report_written_at": "2026-11-13T03:25:30+00:00",
 "implementation": "Three forward non-report commits on branch oap/037-slaif-documentation from the exact accepted main 987fdb9: (1) 54397b1 (40 files) - the professional documentation set (24 current-editable pages dispositioned: the majority rewritten for clarity, SLAIF branding and current accuracy, while research/recipes/README and tests/fixtures/unigram/README were retained unchanged with recorded review rationale; five new doc files INSTALL.md, QUICKSTART.md, docs/README.md, docs/HISTORY.md, docs/assets/slaif-logo.svg), the authorized ARCHITECTURE.md editorial revision 1.3 to 2.0 with synchronized projections (ARCHITECTURE-for-agents.md 19980 bytes, within the 20000-byte limit; CONTEXT-BUDGET.md; DISTILLATION-MAP.md; MANIFEST.json; GENERATED-FILES.json 178/178 pins), the issued order 037-a, oap/active set to 037-a, the narrow candidate-review opt-in plus architecture-revision review support in oap/bin/oap_core.py (no bootstrap-law change; a proposed bootstrap relaxation was rejected by strategy and reverted before any acceptance, and oap_core.py 8820d1bd is the verified restored state containing the authorized opt-in only), focused governance tests (existing test_candidate_review.py extended by 195 lines; B01/B03 trusted-fixture and B10 source-bound link corrections; process-boundary test binding fixes), and 6-line adjustments to the two in-scope CI workflows (application-baseline, oap-bootstrap); (2) 448e917 - normalizes the one blank-line space in docs/assets/slaif-logo.svg and repins its generated entry (whitespace/hash only, 8256 to 8252 bytes); (3) 520be2a (this implementation head) - research/RESEARCH-STATE.md machine counter oap_reports_reviewed 98 to 99 only (registry 42 / frozen incidents 2 / 178-entry generated manifest unchanged). The six ordered governance files (ARCHITECTURE.md, ARCHITECTURE-for-agents.md, SECURITY.md, TESTING.md, oap/governance/DISTILLATION-MAP.md, oap/governance/MANIFEST.json) changed under the authorized architecture revision and were validated against 987 by candidate review; PLAN, CRITICAL, source-lock and bootstrap seeds plus product runtime and dependencies are byte-identical to 987. No runtime mutation; no merge.",
 "documentation": "Complete current-editable scope per the order, verified by a 383-row per-path inventory (private inventory-037a.json; 377 tracked rows at base 987fdb9 plus 6 new rows, one of which is this round's report path): 24 current-editable rows dispositioned (all reviewed; the majority rewritten for clarity, SLAIF branding and current accuracy, research/recipes/README and tests/fixtures/unigram/README retained unchanged with recorded review rationale), 289 format-bound OAP rows (protocol-fixed structure, including the issued immutable order; no prose edits), 3 generated-projection rows synchronized with the authorized architecture revision, 60 immutable-historical rows never modified (current docs link to them), 6 new rows (INSTALL.md, QUICKSTART.md, docs/README.md, docs/HISTORY.md, docs/assets/slaif-logo.svg, oap/reports/037-a-slaif-documentation.md), 1 preserved-standard row (owner-supplied LICENSE verbatim). Architecture 2.0 keeps its good layouts and adds five diagrams with mobile-layout readability corrections (4/5), plus the factual corrections: owned DNS resolver for named main-upstream hosts (IP literals avoid it); positioned wrappers are Div/Span per _classify_inline grants, bare Str has no position; an NFC-changing line denies grants for that line only (map_span/stable flags), distinct from the document-wide NFC-line decomposition consistency failure (_nfc_lines); the lifecycle error view includes valid-200 unsupported/incomplete/error envelopes (no repair, status/error semantics preserved, defined logprobs stripped); section 11 briefly states the actual same-order fixed-anchor factor-two/no-weaker-known-context route and the narrow one-codepoint possible-typo route (runtime_acceptance.py) as positive lexical evidence with unknown/zero semantics - uncalibrated conservative rules, not proof of semantic correctness and not a general semantic analyzer; round6 means rounding to six decimal places; reviewer count at most one (zero for no eligible targets); cancellation before REVIEW dispatch promises no NEW reviewer work after completed main work. Context budget: mobile table and explicit strategic-total correction applied (coding 41322B / strategic 135761B). README/INSTALL/QUICKSTART and developer/operator/research/OAP entry points form coherent current reader journeys; HISTORY uses honest abridged framing with direct evidence links and the PR39 installation entry; WORKSPACE-PLACEMENT is marked historical with WORKSPACE-LAYOUT.json as current authority; SECURITY/TESTING keep titled scannable clauses with exact clause IDs, copyable test commands and qualified Python/Pandoc setup links; the README data-not-bundled wording is stated honestly for the current installation (installation downloads data) and INSTALL distinguishes a rejected span from whole-pass fallback (independently accepted spans can survive).",
 "criteria": "COMPLETE (round complete; this commit is the round's sole report; no merge, milestone or deployment acceptance inferred): (a) scope - all editable current pages finished with the full per-path inventory (383 rows, categories above); no separate human-dataset, research-restart or packaged-library gate; (b) evidence at honest epochs - full oap suite 219/219 OK in 1663.517s on the pre-commit working tree recorded in independent-full-suite-result-v4-pass.json (log full-suite-v2-1794535481.log sha da7df8ab; tested test/source identities 310d7567/d08d5397/5aaee2b7/8820d1bd byte-identical to commit 54397b1), i.e. a working-tree run subsequently committed as 54397b1, not a fresh run at 448e917; the 54397b1-to-448e917 delta is one SVG blank-line space plus its generated pin (whitespace/hash only, non-governance) and 448e917-to-520be2a is one counter line, assessed without rerunning all 219; CI at 448e917 all required checks green (root-confirmed); focused candidate-review module 17/17 (165.822s) with BootstrapSelfAuthorization and ArchitectureRevisionReview negatives; B01+B03 19.883s; B10 10.058s with the missing-report-link typo negative; process-boundary tests all OK in the full-suite log; live CLI candidate-review valid at 520be2a (coding_bytes 41322); whitespace PASSED at 520be2a on both authorized bases (6 pinned diagnostics); transcript and report-history valid at 520be2a (99 reports, 2 frozen incidents); pre-report counter mismatch FAILED as designed (99!=98) locally and in 520be2a CI (409 tests, failures=1); unpublished preflight PASSED on these final bytes; (c) review - strategic content/visual review is complete, not pending: root personally reviewed the final proxy-guide v4 wording/screens, runbook v3, final context budget, architecture v8, final compact header repin, and final README desktop/phone after SVG cleanup; per-page review receipts remain applicable where source hashes are unchanged; (d) governance - the report governance map is the issued order's accepted-base map (16/16, exact order pin f7e0ad87); current candidate manifest identities match candidate sources; the six ordered governance changes validated against 987 by candidate review; bootstrap law intact (oap_core.py 8820d1bd, authorized candidate-review opt-in only) with the no-self-authorizing-bootstrap regression in place.",
 "negative_paths": "The pre-report counter test FAILED (99!=98) locally at 520be2a and in 520be2a CI Research reproducibility (409 tests, failures=1, skipped=53) - the designed 011-e/036-a pre-report red; it clears at the report head (100 report files / 99 counted / block 99). The 54397b1 CI OAP bootstrap acceptance failed once in test_whitespace test_exact_incident_set_passes_both_authorized_bases (both bases, DIAGNOSTIC_SET_MISMATCH): a real defect at that head (blank-line space in the SVG beyond the six pinned incident paths), not transient infrastructure; fixed by 448e917, whose identical-code CI run passed. 520be2a CI Application baseline and OAP bootstrap runs were in progress at report writing and are NOT claimed; they are superseded by final-report-head runs for strategy to verify. publication_verified is false: no publication valid before remote verification, implementation-head CI is not final-report-head CI, no merge/milestone/deployment acceptance inferred, no SSE-failure diagnosis (the historical race remains historical), and no all-219 rerun for the whitespace/hash-only delta. The section-11 route rules are uncalibrated conservative heuristics: not proof of semantic correctness and not a general semantic analyzer. Preserved failure evidence (not acceptance): full-suite-1794532867.log (B10 FAIL + process B11 ERROR, both fixed in-test, guards intact) and governance-focused-rerun-3827090-diagnostic.log (103 tests, 2 failures/38 errors) with the distinct earlier PID 3801956 run (2+19).",
 "boundary_fidelity": "Linear from the exact accepted main 987fdb9 (54397b1, then 448e917, then 520be2a, then this report), no amend/rebase/reset; base_sha and starting_remote_sha are 987fdb9 and remote main re-verified unchanged at report writing. Order bytes f7e0ad87 immutable; the report governance map is the issued order's accepted-base map (16/16 exact); current candidate manifest identities match candidate sources; the six ordered governance files are the only governance-file differences from 987 and are validated by candidate review; PLAN/CRITICAL/source-lock/bootstrap seeds byte-identical to 987. 178/178 generated pins with 0 stale at the implementation head; the six known-incident whitespace diagnostic set is stable on both authorized bases. Three unrelated roots (.rclone-speed-test/, .research-test-scratch/, corpus/) and the ignored owner key (0600/untracked) preserved and never staged. All prior orders, reports, archives, indexes and receipt history immutable; private evidence (logs, receipts, checkpoints) is 0600 inside the 0700 task directory and is never copied into public bytes.",
 "setup": "Same owner-launched foreground CLI and pane (continuation), OAP_ROLE=coding exported for helpers, umask 077, qualified Python 3.12 -B, owned 0700 scratch child inside the private task directory set as TMPDIR for subprocesses (outside /tmp), the existing render environment used for review rendering only, read-only SLAIF references. No new CLI, model, provider or agent; no new broad or live runs beyond the justified epochs recorded above; no re-sent or replayed control signals.",
 "privacy": "No raw answers, prompts, targets, replacements, headers, IDs, keys, native URLs or private physical roots in public bytes. The report carries counts, hashes and logical paths only. The private inventory, render receipts, review feedback, checkpoints and failure logs remain 0600/0700 in the private task directory and are never copied forward; the owner key stays 0600/ignored/untracked.",
 "limits": "Documentation round under the authorized architecture revision: no product-runtime change beyond the narrow candidate-review opt-in, the focused governance tests and the two in-scope workflow adjustments; not a natural-error rate, not linguistic quality acceptance, not a human evaluation dataset, not a deployment or universal-provider-compatibility claim. Final-report-head CI, strategic independent verification and the development merge decision remain pending; coding never merges or self-accepts; the owner retains formal milestone labeling and deployment authority.",
 "human_gates": "Decision NONE under D0. No milestone labeling or deployment authority asserted; retained by the owner. Root has completed the strategic content/visual review of the documentation candidate and will personally verify final-report-head checks and decide the development merge independently.",
 "scope": "Exactly: 40-file 54397b1 + 2-file 448e917 + 1-file 520be2a bookkeeping (RESEARCH-STATE.md counter only) + this sole report. One real PR (40) on the ordered branch oap/037-slaif-documentation. No other tracked path mutation. No runtime mutation; no merge/auto-merge/deployment.",
 "checks": [
  {
   "command": "python3.12 -B -m unittest discover -s oap/tests (full oap suite; pre-commit working tree whose source became 54397b1)",
   "result": "PASSED",
   "sha": "54397b1f721afce8f62b5cbed6eb5c5f8887c341",
   "publication_head_claim": false,
   "details": "219/219 OK in 1663.517s, literal OK; log full-suite-v2-1794535481.log (sha da7df8ab, PID 4177361); tested identities test_acceptance 310d7567 / test_candidate_review d08d5397 / test_process_boundaries 5aaee2b7 / oap_core 8820d1bd byte-identical to 54397b1; honest working-tree epoch recorded in independent-full-suite-result-v4-pass.json, not a fresh run at 448e917."
  },
  {
   "command": "CI at 448e917: Application baseline, Research reproducibility, OAP bootstrap (acceptance 43353296292 + report-history job)",
   "result": "PASSED",
   "sha": "448e917a248183a6967237e1952279df31fb1a7a",
   "publication_head_claim": false,
   "details": "All required checks green at 448e917 (root-confirmed; three workflow runs cover the four required checks, OAP report history included as a job of the OAP bootstrap run). The 54397b1 OAP bootstrap run 43353140064 failed in test_whitespace test_exact_incident_set_passes_both_authorized_bases (both bases, DIAGNOSTIC_SET_MISMATCH): a real defect at that head - blank-line space in docs/assets/slaif-logo.svg beyond the six pinned incident paths, not transient infrastructure; fixed by 448e917, identical-code rerun succeeded; the 54397b1 report-history job passed."
  },
  {
   "command": "python3.12 -B -m unittest oap.tests.test_candidate_review (focused module)",
   "result": "PASSED",
   "sha": "54397b1f721afce8f62b5cbed6eb5c5f8887c341",
   "publication_head_claim": false,
   "details": "17/17 OK in 165.822s incl. BootstrapSelfAuthorization and ArchitectureRevisionReview negatives (no-self-authorizing-bootstrap regression; candidate hashes cannot authorize themselves)."
  },
  {
   "command": "python3.12 -B -m unittest test_acceptance.Acceptance.test_B01_source_integrity test_acceptance.Acceptance.test_B03_router_and_unknown_role",
   "result": "PASSED",
   "sha": "54397b1f721afce8f62b5cbed6eb5c5f8887c341",
   "publication_head_claim": false,
   "details": "2/2 OK in 19.883s; initial-bootstrap tests use an explicitly trusted genuine pre-revision governance fixture with current executable helpers, distinct from accepted-runtime and candidate-review fixtures."
  },
  {
   "command": "python3.12 -B -m unittest test_acceptance.Acceptance.test_B10_inventory_links_drafts",
   "result": "PASSED",
   "sha": "54397b1f721afce8f62b5cbed6eb5c5f8887c341",
   "publication_head_claim": false,
   "details": "1/1 OK in 10.058s (log 56179b67); oap/orders and oap/reports link targets explicitly validated against complete versioned SOURCE with isolated bootstrap state (no unconditional continue); missing-report-link typo negative retained."
  },
  {
   "command": "CI Research reproducibility @ 520be2a (run 43355630113)",
   "result": "FAILED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "Expected pre-report red: 409 tests, failures=1 (test_registry_and_report_counts 99!=98), skipped=53; established 011-e/036-a pattern, clears at report head (100 report files / 99 counted)."
  },
  {
   "command": "oap_cli.py candidate-review --order oap/orders/037-a-slaif-documentation.md --order-sha256 f7e0ad875e90bcab240c8f55d650c7fa44a4bfce8e6dcb7596c286133e1c638d --accepted-ref 987fdb9ed07856d735f1e684f8af342461bf5236 --order-id 037-a (at 520be2a)",
   "result": "PASSED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "candidate review valid; the six ordered governance changes (ARCHITECTURE.md, ARCHITECTURE-for-agents.md, SECURITY.md, TESTING.md, DISTILLATION-MAP.md, MANIFEST.json) validated against the trusted accepted ref 987; coding_bytes 41322."
  },
  {
   "command": "check_whitespace --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision 520be2ad262ca55d4c83134a23e0651adc7875c6",
   "result": "PASSED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "6 pinned incident diagnostics; no new incidents."
  },
  {
   "command": "check_whitespace --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision 520be2ad262ca55d4c83134a23e0651adc7875c6",
   "result": "PASSED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "6 pinned incident diagnostics; no new incidents."
  },
  {
   "command": "oap_cli.py transcript --revision 520be2ad262ca55d4c83134a23e0651adc7875c6 --expected-id 037-a",
   "result": "PASSED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "valid; active 037-a is the latest order; report_count 99 (pre-report)."
  },
  {
   "command": "oap_cli.py report-history --revision 520be2ad262ca55d4c83134a23e0651adc7875c6 --require-manifest",
   "result": "PASSED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "valid; 99 reports; 2 frozen incidents; 178-entry generated manifest present."
  },
  {
   "command": "python3.12 -B -m unittest research.tests.test_research_state_consistency (pre-report, at 520be2a)",
   "result": "FAILED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "10/11 OK; test_registry_and_report_counts FAILED 99!=98 as designed (counter 99 vs 98 counted report files); reconciles post-report to 100 files / 99 counted / block 99."
  },
  {
   "command": "audit_doc_links.py (render-env link audit at the 54397b1 working tree)",
   "result": "PASSED",
   "sha": "54397b1f721afce8f62b5cbed6eb5c5f8887c341",
   "publication_head_claim": false,
   "details": "380 Markdown files, 470 relative links, 0 issues (link-audit-interim-v6.json); external URLs not checked; approximate anchor matching."
  },
  {
   "command": "oap_cli.py preflight-report --id 037-a --source private-scratch-draft --expected-head 520be2ad262ca55d4c83134a23e0651adc7875c6",
   "result": "PASSED",
   "sha": "520be2ad262ca55d4c83134a23e0651adc7875c6",
   "publication_head_claim": false,
   "details": "valid unpublished report draft; canonical report absent from the repository during preflight; run against these final draft bytes immediately before the report commit."
  }
 ]
}
````

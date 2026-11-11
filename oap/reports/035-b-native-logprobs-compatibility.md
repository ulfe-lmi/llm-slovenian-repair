````oap-report
{
 "id": "035-b",
 "result": "PARTIAL",
 "order_path": "oap/orders/035-b-native-logprobs-compatibility.md",
 "order_sha256": "decdcd13a0b30a8d36b7e6f0bb2e623da5ba124fe140d6c5734ea9533da64e34",
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
 "implementation_head": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
 "publication_verified": false,
 "pr_mode": "AMEND_EXISTING_PR",
 "pr": 37,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/37",
 "pr_state": "open",
 "branch": "oap/035-native-rtx3090-qualification",
 "base_sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
 "starting_remote_sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-11T22:22:05.752392+00:00",
 "report_written_at": "2026-11-11T22:31:02.487541+00:00",
 "implementation": "The implementation head 7c8c26edc248406a92f1a30b097aa047c64c5cea is a single forward non-report commit on branch oap/035-native-rtx3090-qualification, sole parent de9a732e5c2b340798b5f6934ce454fe3cc7d981 (the verified 035-a report head; AMEND_EXISTING_PR, same PR 37, no new PR, no amend/rebase/reset). It touches exactly the five ordered non-report paths: oap/orders/035-b-native-logprobs-compatibility.md (this exact issued order), oap/active (035-a -> 035-b), concept-verification/responses_contract.py (null-only typed patch, SUPERSEDED by owner policy; committed as partial WIP for 035-c continuation, NOT claimed accepted/final/ready-to-merge/deploy), oap/audit/results/035-native-rtx3090-qualification.json (superseding compact 035-b PARTIAL evidence), and research/RESEARCH-STATE.md (machine counter oap_reports_reviewed 94 -> 95 ONLY; registry_entries 42 and frozen_report_history_incidents 2 unchanged). The null-only patch (22-line diff, SHA adb9b050667376d9925a7e04551ce500741f610e69da892b5187ee3ba7618480) adds a single condition in aligned_metadata_clean: if key == 'logprobs' and item is None: continue. No other product, parser, protection, acceptance, detector, transport, dependency, workflow, source-law, manifest or prior-artifact byte changed. No tests were added (R4 stopped at owner supersession).",
 "documentation": "No product README/PLAN/ARCHITECTURE/SECURITY/TESTING byte touched. concept-verification/README.md omitted (no verified useful operator-profile instruction established; the owner's new unconditional policy is not yet implemented and is 035-c scope). The sole docs byte change is research/RESEARCH-STATE.md machine counter oap_reports_reviewed 94 -> 95 (counters-only bookkeeping; registry 42 and incidents 2 and all historical prose unchanged).",
 "criteria": "PARTIAL: (a) exact native logprobs type established: NULL (is_none) at both ACTUAL HTTP worker boundary and independent client parse (attempt 7, 28.7449 s, 7160 bytes, HTTP 200, no eligible edit, measured main_dispatches=1, review_dispatches=0 via CONCEPT_USAGE_OBSERVER); prior 035-a NONEMPTY claim corrected; (b) the null-only typed patch was implemented and Root independently proved it via 6 actual HTTP cases (real Engine/Pandoc/SQLite/reviewer HTTP/acceptance/patcher, only external main/review endpoints fake, 0 native posts) BEFORE the owner superseded the policy; (c) owner's new unconditional ALWAYS-remove policy is documented as the next 035-c requirement on the same PR; (d) the null-only patch is preserved as SUPERSEDED WIP (committed, not reverted, not claimed final); (e) shared state/governance/transcript/report-history and both accepted-base whitespace checks pass at the implementation head; (f) machine counter is 95 with registry 42 and incidents 2 preserved. Native repair/MVP is NOT proved (full repair path not exercised under the new policy); R4 meaningful tests NOT RUN (owner superseded before writing); this is reported PARTIAL, not COMPLETE.",
 "negative_paths": "PARTIAL (truthful). The only FAILED check at the implementation head is the designed pre-report research counter test: AssertionError 95 != 94 (machine block oap_reports_reviewed 95 anticipates this 035-b report; 94 counted .md report files present after 007-o exclusion at the implementation head). This mismatch is expected and is recorded FAILED, not waived or hidden; the sole-report SELF commit reconciles it (96 total, 95 counted, block 95). Missing new-policy (035-c) tests: NOT RUN / PENDING (not passed, not claimed). The prior 035-a REMOTE verifier failed PR_CREATED_AFTER_REPORT (recorded pr_observed_at 16:02 preceded actual PR creation 16:04:40); the prior report is immutable historical evidence, never falsely accepted. No future push or final-head CI success is claimed inside this pre-push report (publication_verified false).",
 "boundary_fidelity": "Descends from the verified 035-a report head de9a732e5c2b340798b5f6934ce454fe3cc7d981 with no amend/rebase/reset/rewrite; the 035-b delta is a single forward non-report commit. All product/source/dependency/workflow/source-law bytes remain byte-equal across the branch except the single null-only patch in responses_contract.py (superseded WIP). proxy.py unchanged (836b78cc...); the original contract SHA (bed932b2...) is preserved in history. The immutable 035-a order/audit/report, the 034 order/audit/evidence/report, PRIVATE_INITIAL_034, the frozen registry (42) / incidents (2), all 173 generated-manifest identities, the old four-request ledger (frozen), and the owner key (0600/ignored/untracked) are preserved.",
 "setup": "Same adopted foreground owner-launched sole CLI process and existing chat (same PID 3341327, cwd, argv codex --yolo --profile early-beta, profile, home, authentication; no new agent, CLI, provider, model, pane, home, auth or reset). Every helper used explicit OAP_ROLE=coding, actual shell umask 077, the qualified Python 3.12.15 interpreter with -B, and a private 035 strict scratch under the supervision root with private TMP/cache. Finite owned disposable CPU/Git/HTTP children only; no process-pattern cleanup. The owner key (0600/regular/owner/75 bytes) is never printed, copied, staged or dumped. Pinned Pandoc 3.7.0.2 (02a59bd9...) is the mandatory startup check. Native opt-in (REPAIR_ALLOW_LIVE_TESTS=YES) is child-only.",
 "privacy": "No raw customer text, prompts or answers, targets or replacements, headers, response IDs, exception messages, credentials, the native endpoint URL, or native physical host paths in any public byte. The order, the audit evidence, this report and the counter byte are /home-free, key-free and URL-free (verified by count-only scans before push). The private owned harness, fixtures, ledger and diagnostics live only in the supplied strict 0700/0600 scratch and are never staged or committed. Only content-free facts are published: verdict labels, source lines, bounded counts, the known aligned-metadata field name (annotations|logprobs), byte-count/latency figures, dispatch counts, usage known/unknown and cleanup booleans.",
 "limits": "Product code mutation limited to the null-only typed patch (SUPERSEDED WIP, not final policy). The owner's new unconditional ALWAYS-remove policy is NOT implemented in this round (that is 035-c). No R4 tests were written (stopped at owner supersession). No 965 full-suite rerun, no new human dataset/quality-rate estimate, no service/weights/quantization/GPU/network/credential change, no deploy, no milestone or functional acceptance. The four required final-head CI checks and the independent strategic review precede any development merge. No future push or CI success is claimed inside this pre-push report (publication_verified false).",
 "human_gates": "Decision NONE under D0. The owner's explicit allowance of up to 1,000,000 additional RTX3090 requests persists; only the needed bounded sequential traffic (1 main, 0 reviews measured in 035-b; 4 actual main posts total across the round including 035-a, 4 reserved review slots conservatively charged, 0 actual reviews) was used. Root independently reviews the exact final remote head and owns the conditional development merge and the 035-c same-PR order. The owner retains final milestone and deployment decisions.",
 "scope": "Exactly the five ordered non-report paths in the 035-b delta (order, oap/active, responses_contract.py [superseded WIP], oap/audit/results/035-native-rtx3090-qualification.json, research/RESEARCH-STATE.md counters-only) plus this sole report. PR 37 is the single existing PR (AMEND_EXISTING_PR) from verified accepted base 7dcd186fe394c1262bfe878ba5d6527b888fc317. concept-verification/README.md omitted. The prior 035-a order/audit/report, the 034 artifacts, PRIVATE_INITIAL_034, the frozen registry (42) / incidents (2), all 173 generated-manifest identities, the old frozen ledger, the three unrelated untracked roots, the owner key, retained branches, archives and the read-only index are preserved. No other tracked path mutation.",
 "checks": [
  {
   "command": "env OAP_ROLE=coding umask 077 qualified python -B oap/bin/oap_cli.py state --repo-root . (at implementation head 7c8c26e)",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "state READY; id 035-b; branch oap/035-native-rtx3090-qualification; PR 37; no critical entries or open gates."
  },
  {
   "command": "env OAP_ROLE=coding umask 077 qualified python -B oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (at implementation head 7c8c26e)",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "structure valid; accepted-runtime valid against trusted governance revision 3549de2a; no CRIT entries; D0."
  },
  {
   "command": "env OAP_ROLE=coding umask 077 qualified python -B oap/bin/oap_cli.py transcript --repo-root . --revision 7c8c26e --expected-id 035-b",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "transcript valid; active and latest 035-b; orders list ends 035-b; report_count 95; frozen mutation paths unchanged; 2 quarantined incidents preserved."
  },
  {
   "command": "env OAP_ROLE=coding umask 077 qualified python -B oap/bin/oap_cli.py report-history --repo-root . --revision 7c8c26e --require-manifest",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "report history valid; all current generated-file manifest identities verified; report_count 95; frozen 006-a/006-c incidents preserved."
  },
  {
   "command": "env OAP_ROLE=coding umask 077 qualified python -B oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision 7c8c26e",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "closed-six contract: exactly six exact diagnostics at this authorized base; the new 035-b order introduces no new whitespace incident."
  },
  {
   "command": "env OAP_ROLE=coding umask 077 qualified python -B oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision 7c8c26e",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "closed-six contract: exactly six exact diagnostics at this second authorized base (same set as base 2832fa1e)."
  },
  {
   "command": "env OAP_ROLE=coding PATH=qualified/bin:$PATH qualified python -B -m pytest -p no:cacheprovider research/tests/test_research_state_consistency.py -k registry_and_report_counts -q (pre-report stage, at implementation head 7c8c26e)",
   "result": "FAILED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "the designed expected pre-report mismatch: AssertionError 95 != 94 (machine block oap_reports_reviewed 95 anticipates this 035-b report; 94 counted .md report files present after 007-o exclusion at the implementation head). Recorded FAILED, not waived or hidden; the sole-report SELF commit reconciles it (96 total, 95 counted, block 95)."
  },
  {
   "command": "qualified python -B -c py_compile.compile('concept-verification/responses_contract.py', doraise=True) (at implementation head 7c8c26e)",
   "result": "PASSED",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "superseded null-only WIP patch compiles cleanly."
  },
  {
   "command": "035-c new-policy tests (absent/null/empty/populated/unexpected-type, zero-review, accepted-edit, SSE parity)",
   "result": "NOT RUN",
   "sha": "7c8c26edc248406a92f1a30b097aa047c64c5cea",
   "publication_head_claim": false,
   "details": "PENDING: owner superseded the null-only policy before R4 tests were written. These tests belong to 035-c (unconditional ALWAYS-remove policy) and are not part of this 035-b checkpoint."
  },
  {
   "command": "Root actual HTTP 6-case proof of superseded null-only patch (035b-root-postfix-real-HTTP-null-and-protected-negative-checks-20261111.json)",
   "result": "PASSED",
   "sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
   "publication_head_claim": false,
   "details": "6 actual HTTP cases PASS at the superseded null-only working patch (contract SHA adb9b050...): null-edit with protected Unicode/unchanged slices, clean zero-review, annotations-NULL still denied, populated/false/object logprobs denied. Real Engine/Pandoc/SQLite/detector/reviewer HTTP/CPU acceptance/patcher; only external main/review endpoints fake; 0 native posts. Classification: BASELINE/SUPERSEDED desired policy proof."
  }
 ]
}
````

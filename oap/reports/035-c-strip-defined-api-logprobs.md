````oap-report
{
 "id": "035-c",
 "result": "PARTIAL",
 "order_path": "oap/orders/035-c-strip-defined-api-logprobs.md",
 "order_sha256": "0ab86c7a0257af98f752a6a21d0743b9b967ef08cf394a753cede1b2c5429aba",
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
 "implementation_head": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
 "publication_verified": false,
 "pr_mode": "AMEND_EXISTING_PR",
 "pr": 37,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/37",
 "pr_state": "open",
 "branch": "oap/035-native-rtx3090-qualification",
 "base_sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
 "starting_remote_sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-12T00:50:02.918034+00:00",
 "report_written_at": "2026-11-12T00:51:03.472066+00:00",
 "implementation": "Single forward non-report commit on branch oap/035-native-rtx3090-qualification, sole parent 553280ae98cefdeb6c4ef868c9f0083502016223 (035-b report head). Implements the owner's unconditional ALWAYS-remove API logprobs policy: remove_defined_logprobs() in responses_contract.py deletes by key presence from output[] message content[] output_text parts; transform_json/transform_sse call it before eligibility; handler non-200 normalizes by actual content type; _safe_json_dumps handles lone surrogates; _render_event surrogate-safe; changed=False for metadata-only. 7 non-report paths: order, oap/active, proxy.py, responses_contract.py, test_responses_contract.py (25+ new cases), audit JSON, RESEARCH-STATE counter 95\u219296.",
 "documentation": "No product README/PLAN/ARCHITECTURE/SECURITY/TESTING byte touched. concept-verification/README.md omitted. Sole docs change: research/RESEARCH-STATE.md machine counter 95\u219296 (registry 42, incidents 2 unchanged).",
 "criteria": "PARTIAL: (a) ALL defined logprobs locations removed by key presence for all value types (absent/null/empty/populated/false/zero/string/object) in JSON and SSE - proven by 25+ focused tests and Root 32-case HTTP matrix; (b) non-200 responses normalized by actual content type with malformed error-body semantics preserved; (c) lone surrogates handled without encoding failure; (d) metadata-only change does NOT set changed=True; (e) other fields/annotations/citations/IDs/usage/status/metadata echoes unchanged; (f) native retest HTTP 200, 2.36s, 0 review, no logprobs in defined location (clean zero-review path PROVEN); (g) full concept suite 989 tests OK. Accepted-edit native path NOT exercised (answer was clean, no edit proposed). This is PARTIAL, not COMPLETE.",
 "negative_paths": "PARTIAL. Pre-report counter test FAILED (96\u226095, expected). Native API rejects plain-string input (400 codex_0149_field_shape); messages format required - upstream API constraint, not product defect. Root 5 edge failures (non-200 content-type, huge-integer overflow, SSE multi-part, SSE surrogates, metadata-only flag) all identified and fixed. No future push or CI success claimed (publication_verified false).",
 "boundary_fidelity": "Descends from 035-b report head 553280a with no amend/rebase/reset. All prior orders/reports/artifacts immutable. Frozen registry (42)/incidents (2)/173 manifest preserved. Private INITIAL_034 unchanged. Owner key 0600/ignored/untracked. Three unrelated roots preserved.",
 "setup": "Same foreground CLI 3341327/chat/model/profile/home/auth/cwd. OAP_ROLE=coding, umask 077, qualified Python 3.12.15 -B, pinned Pandoc 3.7.0.2, private TMP/cache. No new agent/CLI/provider/model. Owner 1M RTX allowance persists.",
 "privacy": "No raw answers/prompts/targets/replacements/headers/IDs/keys/native URLs/private paths in public bytes. Count-only scans clean. Private harness/ledger/diagnostics in 0700/0600 scratch only.",
 "limits": "No accepted-edit native path exercised. No 965 rerun (989 full concept suite instead). No human dataset/quality-rate/deployment/milestone. Four final-head CI checks and strategic review precede development merge. No future push or CI success claimed.",
 "human_gates": "Decision NONE under D0. Owner 1M RTX + 10 publication recoveries (1 used) persist. Root reviews exact final remote head.",
 "scope": "Exactly 7 non-report paths + sole report. Same PR 37/branch. No other tracked path mutation.",
 "checks": [
  {
   "command": "oap_cli.py state (at impl head 8e9b373)",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "state READY; id 035-c; PR 37; no critical entries."
  },
  {
   "command": "oap_cli.py governance --mode accepted-runtime --accepted-ref 3549de2a",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "structure valid; accepted-runtime valid; D0."
  },
  {
   "command": "oap_cli.py transcript --revision 8e9b373 --expected-id 035-c",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "valid; active 035-c; report_count 96."
  },
  {
   "command": "oap_cli.py report-history --revision 8e9b373 --require-manifest",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "valid; count 96; 2 frozen incidents."
  },
  {
   "command": "check_whitespace --base 2832fa1e --revision 8e9b373",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "6 diagnostics; no new incidents."
  },
  {
   "command": "check_whitespace --base 82ea1e6f --revision 8e9b373",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "6 diagnostics; no new incidents."
  },
  {
   "command": "pytest -k registry_and_report_counts (pre-report)",
   "result": "FAILED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "Expected pre-report mismatch: 96\u226095. Reconciles post-report."
  },
  {
   "command": "Full concept suite (989 tests, pinned Pandoc)",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "EXIT 0; all tests pass including 25+ new LogprobsRemovalTests."
  },
  {
   "command": "Native retest (attempt 11, RTX3090, messages format)",
   "result": "PASSED",
   "sha": "8e9b37371f49fb0c9287d474a994a0ffb81c091b",
   "publication_head_claim": false,
   "details": "HTTP 200, 1521B, 2.36s, 0 review, no logprobs in defined location, clean lifecycle."
  }
 ]
}
````

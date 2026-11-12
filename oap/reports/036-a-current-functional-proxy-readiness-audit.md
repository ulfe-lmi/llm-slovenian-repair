````oap-report
{
 "id": "036-a",
 "result": "COMPLETE",
 "order_path": "oap/orders/036-a-current-functional-proxy-readiness-audit.md",
 "order_sha256": "bda6a436fef4f73a3ade3e2b39aa417937c16b856c45938fd85fb9574b38320e",
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
 "implementation_head": "20f6ec8b76c939228f1aafb40f64a97afd459709",
 "publication_verified": false,
 "pr_mode": "CREATE_NEW_PR",
 "pr": 38,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/38",
 "pr_state": "open",
 "branch": "oap/036-current-functional-readiness-audit",
 "base_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
 "starting_remote_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-12T07:06:18+00:00",
 "report_written_at": "2026-11-12T07:21:22.424613+00:00",
 "implementation": "Two forward non-report commits on branch oap/036-current-functional-readiness-audit: 4031fa76 (sole parent 1bb9eec, the exact accepted audited main) adds the exact issued order 036-a, oap/active -> 036-a, the ICA audit result, its privacy-safe evidence JSON, and the RESEARCH-STATE machine counter 97->98 (registry 42 / incidents 2 / 173-entry generated manifest unchanged); and 20f6ec8 (sole parent 4031fa76) is one doc-only wording correction (failure-boundary and owner-scope wording in the audit/evidence only, no class/status change). Exactly five allowed non-report paths across the two commits; no product/test/governance byte touched; no runtime mutation.",
 "documentation": "The ICA audit result and its privacy-safe evidence JSON carry the corrected evidence epochs (1006/718.100s suite executed at git HEAD c304bf16 + final WIP test bytes; test file and frozen runtime proxy.py 86df8af2 / responses_contract.py 0d9347c5 byte-identical to main; f64da10 a source-equivalent commit, never the execution epoch), the active-runtime paths (runtime_detection/runtime_acceptance/batch_review/composed_validation), the source-equivalent native T9 reuse under R5 (c304..main diff is only README + test file), the honest fresh-22 scope, the content-free default logs with a separately-authorized opt-in trace channel, and the full-source coverage projection (5 SERVICE rows, 8 PLAN16 criteria, all 21 architecture facets). Sole other change: research/RESEARCH-STATE.md machine counter 97->98.",
 "criteria": "COMPLETE (audit round completed and published; the assessment outcome is open and reported, not forced): (a) source-first independence - the neutral owner scope and complete PLAN/ARCHITECTURE at the exact main were read first and the initial requirements-first derivation saved and hashed (23192B, sha 1fa67b85) BEFORE any runtime/registry/README/report/deferred access; the private record is cited by identity only and stays unpublished; (b) evidence base at honest epochs - fresh 22 named existing tests at main (literal interpreter exit 0, log bbf85422, 17.020s) + source-equivalent 1006/718.100s suite at c304bf16 + WIP test bytes (literal FULL_EXIT 0, log 88593a73) + 4 final-head CI checks at tree 7b2418 via checkout f0834215 + source-equivalent native T9 at the c304 epoch (R5 reuse after verified byte-identical runtime/dependency equivalence; native_calls_by_root 0; usage 281/480/761) + the corrected first 300s invocation recorded LIMITED/INCOMPLETE (interpreter exit UNKNOWN); (c) matrix - 59 MVP rows classified 49 IMPLEMENTED / 9 PARTIAL / 1 ABSENT / 0 UNPROVEN with real paths/tests/SHA, plus a privacy-safe full-source coverage projection beyond the registry (SERVICE rows as later-stage, 8 PLAN16 criteria, 21 architecture facets); (d) same-PR history/scope/privacy/governance - exact order bytes (bda6a436), both accepted-base whitespace checks PASSED, state/governance/transcript/report-history PASSED at the non-report head, pre-report counter mismatch FAILED as expected (98!=97), unpublished preflight. Audited at the exact accepted main 1bb9eec; deployment_authorized=false; human_milestone_accepted=false.",
 "negative_paths": "The functional operating path is demonstrated; the non-IMPLEMENTED rows are scope boundaries/limits, not functional defects, and no additional functional remediation was identified in this audit: later-stage deployment/stack coupling (A-ROUTE-01, A-STACK-01) and the SERVICE rows (S01-S05); the A-ACCEPT-01 mode-progression literal boundary (the proxy runs a single strict validated-AUTO_REPAIR path; detect_only/shadow are not exposed modes); optional morphology (A-DETECT-01, M02 absent); and the unmeasured linguistic/quality axis (MVP-8, A-EVAL-01, M01, M04, M07), where a SEPARATE HUMAN EVALUATION DATASET is excluded by the owner (quality unmeasured here; this does not forbid all controlled/automatic evaluation and creates no future dataset obligation). Pre-report counter test FAILED (98!=97, expected; reconciles to 99 report files / 98 counted / block 98 post-report). The first 300s suite invocation was piped through tail (interpreter exit UNKNOWN, LIMITED/INCOMPLETE). The native observation stays at its c304 execution epoch (source-equivalent to main), not a pretend fresh main run. No future push or CI success claimed (publication_verified false).",
 "boundary_fidelity": "Descends from the exact accepted audited main 1bb9eec with two forward non-report commits (4031fa76, then the doc-only 20f6ec8) and no amend/rebase/reset; base_sha and starting_remote_sha are the accepted main. All prior orders/reports/artifacts immutable; frozen registry (42) / incidents (2) / 173-entry generated manifest preserved. The initial requirements-first derivation (23192B, sha 1fa67b85) remains immutable and unpublished in private 036 scratch, cited by identity only. Three unrelated roots (.rclone-speed-test/, .research-test-scratch/, corpus/) preserved and never committed. Owner key 0600/ignored/untracked.",
 "setup": "Same owner-launched foreground CLI 3341327/chat/model/profile/home/auth/cwd; externally consumed control, no second wait. OAP_ROLE=coding, umask 077, qualified Python 3.12.15 -B, pinned Pandoc 3.7.0.2 (binary sha 02a59bd9), private 036 TMP/cache/logs. No new agent/CLI/provider/model/home/auth. No native calls or new broad/live runs for counts (source-equivalent native T9 reused under R5).",
 "privacy": "No raw answers/prompts/targets/replacements/headers/IDs/keys/native URLs/private physical roots in public bytes. The evidence JSON and this report carry counts/hashes/logical paths only. The private initial derivation and native/harness receipts remain in 0700/0600 scratch and are never copied forward.",
 "limits": "Controlled functional-path / source-equivalent evidence only: not a natural-error rate, not linguistic quality, not statistical independence of two same-model calls, not human acceptance, not a deployment or universal-provider-compatibility claim. The native useful-edit is reused at its source-equivalent c304 epoch (R5), limits explicit (one controlled mechanism example, not quality/current availability). The four final-head CI checks and strategic independent review precede any development merge; coding never merges or self-accepts; the owner retains formal milestone labeling and deployment authority.",
 "human_gates": "Decision NONE under D0. No milestone labeling or deployment authority asserted; retained by the owner. Root continues final independent review and the CI gate.",
 "scope": "Exactly five allowed non-report paths across two forward commits (order, oap/active, audit result, evidence JSON, RESEARCH-STATE machine counter 97->98) + sole report. One real PR (38) on the ordered branch. No other tracked path mutation. No runtime mutation; no merge/auto-merge/deployment.",
 "checks": [
  {
   "command": "oap_cli.py ica --source oap/audit/results/036-current-functional-proxy-readiness-audit.md --current-main 1bb9eec (at non-report head 20f6ec8)",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "schema valid; 59 MVP rows, 49 IMPLEMENTED / 9 PARTIAL / 1 ABSENT / 0 UNPROVEN; deployment_authorized false; human_milestone_accepted false."
  },
  {
   "command": "oap_cli.py governance --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (at non-report head 20f6ec8)",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "structure valid; accepted-runtime valid; 16 governance identity hashes unchanged from the trusted ref."
  },
  {
   "command": "oap_cli.py transcript --revision 20f6ec8 --expected-id 036-a",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "valid; active 036-a is the latest order; report_count 98 (pre-report)."
  },
  {
   "command": "oap_cli.py report-history --revision 20f6ec8 --require-manifest",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "valid; count 98; 2 frozen incidents; 173-entry generated manifest present."
  },
  {
   "command": "check_whitespace --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision 20f6ec8",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "6 pinned diagnostics; no new incidents."
  },
  {
   "command": "check_whitespace --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision 20f6ec8",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "6 pinned diagnostics; no new incidents."
  },
  {
   "command": "unittest research.tests.test_research_state_consistency -k registry_and_report_counts (pre-report)",
   "result": "FAILED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "Expected pre-report mismatch: 98!=97. Reconciles post-report to 99 report files / 98 counted / block 98."
  },
  {
   "command": "Fresh bounded probe at main (22 named existing tests; qualified Python 3.12.15 -B, CONCEPT_PANDOC 3.7.0.2, private 036 TMP/cache, umask 077)",
   "result": "PASSED",
   "sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
   "publication_head_claim": false,
   "details": "literal interpreter exit 0; log bbf85422 (4007B, 'Ran 22 tests in 17.020s', OK); logprobs JSON/SSE value types + ineligible + non-200, no-edit raw-byte identity, metadata, Pandoc startup, mapping, zero-call."
  },
  {
   "command": "Full concept suite (discover -s tests -v; qualified Python 3.12.15 -B, CONCEPT_PANDOC 3.7.0.2, private TMP/cache) at git HEAD c304bf16 + final WIP test bytes",
   "result": "PASSED",
   "sha": "c304bf16e5100337d0ee02244c5a88b5be9028c6",
   "publication_head_claim": false,
   "details": "1006 tests OK in 718.100s; literal FULL_EXIT 0 (session 34148, 04:00:56.882Z to 04:17:35.747Z); log 88593a73; tested test file 86d1ae6b byte-identical to main; frozen runtime proxy.py 86df8af2 / responses_contract.py 0d9347c5 byte-identical to main; f64da10 source-equivalent, never the execution epoch."
  },
  {
   "command": "Source-equivalent native T9 (git head c304; launcher fd969206, harness d9e7948e, Pandoc 02a59bd9, RO index f769235b, Python 3.12.15, qualified matching-RTX profile)",
   "result": "PASSED",
   "sha": "c304bf16e5100337d0ee02244c5a88b5be9028c6",
   "publication_head_claim": false,
   "details": "validated real-Qwen review, approved original-span patch, defined-probability removal, clean shutdown; native_calls_by_root 0; usage 281/480/761; R5 reuse after verified byte-identical runtime/dependency equivalence (c304..main diff is only README + test file); limits explicit."
  },
  {
   "command": "oap_cli.py preflight-report --id 036-a --source private-scratch-draft --expected-head 20f6ec8",
   "result": "PASSED",
   "sha": "20f6ec8b76c939228f1aafb40f64a97afd459709",
   "publication_head_claim": false,
   "details": "valid unpublished report draft; canonical report absent from the repository during preflight."
  }
 ]
}
````

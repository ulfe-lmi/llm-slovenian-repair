````oap-report
{
 "id": "034-a",
 "result": "PARTIAL",
 "order_path": "oap/orders/034-a-functional-proxy-readiness-audit.md",
 "order_sha256": "586ca6cbea712bcfe663bcf2c73d68af9601b205c6f4f2a134c256fb58241b65",
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
 "implementation_head": "82301efb4bbc3635e8002331c21c0d44b4492c62",
 "publication_verified": false,
 "pr_mode": "CREATE_NEW_PR",
 "pr": 36,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/36",
 "pr_state": "open",
 "branch": "oap/034-functional-proxy-readiness-audit",
 "base_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
 "starting_remote_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-11T11:26:59+00:00",
 "report_written_at": "2026-11-11T11:26:59+00:00",
 "implementation": "Two forward non-report commits on branch oap/034-functional-proxy-readiness-audit descending from the accepted base c36ed4f (no amend/reset/rewrite; PR 36, CREATE_NEW_PR). (1) 3c3c7ff: the source-first Independent Closure Audit artifacts - the activated order oap/orders/034-a-functional-proxy-readiness-audit.md, oap/active=034-a, oap/audit/results/034-functional-proxy-readiness-audit.md (ICA 59-row matrix, 48 IMPLEMENTED / 7 PARTIAL / 2 UNPROVEN / 2 ABSENT; D05 PARTIAL native) and oap/audit/results/034-functional-proxy-readiness-evidence.json (fresh 965/exit0 provenance; privacy-safe source-derived projection of PRIVATE_INITIAL_034; 12 full-architecture coverage facets A-L; native real-Qwen limits), and the one-line machine counter 91->92 (registry 42, incidents 2 unchanged). (2) 82301ef (literal implementation head, sole parent 3c3c7ff): R4 citation precision only - facet A test_main_lifecycle.MainLifecycleTests.test_system_exit_primary_keeps_identity_over_nonordinary_cleanup; facet C test_analysis_policy.EngineDefaultBoundaryTests.test_oversize_gate_zero_work_separate_reasons; LR-006/A-SPAN-01/MVP-5 corrected to the real parser batch_review.parse_batch_envelope, real acceptance runtime_acceptance.accept and shared patcher repair.apply_edits. No classification, native-gap, product, dependency, test, workflow, source-law or prior-artifact byte changed. Audit-only, offline, zero live target calls. PR 36 head pinned at the literal implementation head before report composition.",
 "documentation": "No product documentation changed (audit-only). The runnable proxy is the concept-verification spike; its README protection section already documents the source-ordered protected contexts (unchanged). No README/PLAN/ARCHITECTURE/SECURITY/TESTING byte touched.",
 "criteria": "Source-first, audit-only assessment at the exact audited accepted main c36ed4f, D0, Decision NONE. MET for the audit deliverables: (a) neutral owner scope read first; (b) COMPLETE canonical PLAN.md (sha256 d2aa1d98...) and ARCHITECTURE.md (sha256 a16e0f87...) verified byte-exact at c36ed4f BEFORE any implementation/registry/closure/deferred-index inspection; (c) the immutable requirements-first derivation saved and hashed and preserved privately as PRIVATE_INITIAL_034 (24661 bytes, SHA-256 bb29467e..., byte/inode unchanged, never staged/committed/pushed); (d) the frozen registry, deferred index and prior 032/033-a claims inspected only after the derivation, as claims; (e) full-source/full-registry/runtime positive-and-negative assessment with qualified python -B, shell umask 077 and the pinned Pandoc 3.7.0.2; (f) the privacy-safe normative subset of the private record (owner scope, full source requirements LR-001..014 / all 8 PLAN-16 criteria / all D-M-S work blocks, applicability model, owner-excluded items) and the 12 full-architecture coverage facets A-L published in the evidence appendix with real named positive/negative tests and seams; (g) the ICA matrix is schema-valid (check_ica PASSED). FUNCTIONAL FINDING: the offline functional-MVP software core is substantially IMPLEMENTED and well-tested; the remaining actual applicable functional gap is native serving compatibility on the actual target Qwen (UNPROVEN; 0 authorized native calls; the earlier 031-b native RTX MAIN aggregate failed the completion-envelope validator; the four allocated target-POST slots are exhausted). Linguistic quality is owner-EXCLUDED (not a functional gate, not deferred, no human-labeling obligation). Milestone/deployment authority is separate and owner-retained.",
 "negative_paths": "PARTIAL (truthful). The two shared whitespace checks FAILED DIAGNOSTIC_SET_MISMATCH at the literal implementation head, attributed to the single sixth diagnostic: one trailing ASCII space at line 67 of the immutable Root-issued order (Root engineering mistake; my new audit/evidence bytes are whitespace-clean). The closed five-incident whitespace law is NOT altered under 034-a; the order is preserved byte-exact; Root will issue a bounded SAME-PR corrective suffix after actual publication. The designed pre-report research counter test FAILED (92 != 91) and is preserved, not waived. Native serving compatibility is UNPROVEN (no live Qwen call; real wire proven only to a synthetic in-process endpoint via the owned worker child; the owned fake-worker IPC subset is framing-only, not wire; an owned fake-worker endpoint can never satisfy the native retest). No merge, no deployment, no human acceptance. No future push/CI success is claimed inside this pre-push report (publication_verified false).",
 "boundary_fidelity": "Descends from the accepted base c36ed4f with no amend, reset or rewrite; the two forward non-report commits (3c3c7ff, 82301ef) keep all product bytes frozen (each touches only the permitted non-report paths; 82301ef touches only the two audit/evidence files). The exact frozen private initial record PRIVATE_INITIAL_034 is read-only and its bytes/inode are unchanged (re-verified before each public serialization). The 965/exit0 run is preserved as the final synchronous epoch; earlier wrong-parser (no CONCEPT_PANDOC) and async-wrapper epochs are disclosed, not claimed.",
 "setup": "Same adopted foreground owner-launched sole CLI process and existing chat (same PID 3341327, cwd, argv, profile, home and authentication; no new agent, CLI, provider, model, pane, home, auth or reset). Shared checks, ICA and scans used explicit OAP_ROLE=coding, actual shell umask 077 and the qualified Python with -B; the preserved 965 run used the ordered pinned Pandoc 3.7.0.2 via CONCEPT_PANDOC; the private 034a scratch/cache under the supervision root is strict 0700/0600. Honest setup disclosure: the first runtime run (09:28:24) used the qualified python -B but lacked an explicit CONCEPT_PANDOC and selected the wrong parser (not the exit proof); a second async wrapper epoch was not a complete exit proof; the final synchronous run is the actual 965/exit0 proof with its disclosed environment limits (no strategic TMP claimed). No live product-model request, no GPU/service/network/auth mutation, no process-pattern kill.",
 "privacy": "No raw customer text, prompts or answers, targets or replacements, headers, credentials or native physical host paths in any public byte (the audit, evidence and this report are /home-free and key-free, verified by count-only scans). The complete initial requirements-first record is private and unpublished, cited only by logical ID PRIVATE_INITIAL_034 / byte count / hash / provenance; its privacy-safe normative subset is published in the evidence appendix. No native path fields from the private record's derivation_inputs are copied. The owner key is never printed, staged or copied; only count-only scan results are recorded.",
 "limits": "Audit-only, offline: no new dependency, dataset, research restart, source-law, projection, manifest or prior-report byte changed; no product, dependency, test, workflow or implementation change; no separate human evaluation dataset; no merge/deploy/human acceptance. PARTIAL reflects the two FAILED whitespace checks (immutable order line 67), which prohibit merge but not publication. No functional-MVP milestone, linguistic-quality or deployment acceptance is self-certified; the four required final-head CI checks on the published head and Strategy's independent semantic review remain the development-merge gate. No future push or CI success is claimed inside this pre-push report (publication_verified false).",
 "human_gates": "Decision NONE under D0; no human gate created or cleared. Root independently reviews the exact final remote head and owns the conditional development merge; the four required final-head checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) and the independent semantic review precede any development merge, and the closed-five whitespace law must pass (hence the pending bounded SAME-PR corrective suffix). The owner retains final milestone and deployment decisions; development merge is distinct from deployment and from functional readiness.",
 "scope": "Exactly the five permitted non-report paths across the two forward non-report commits (oap/orders/034-a-functional-proxy-readiness-audit.md, oap/active, oap/audit/results/034-functional-proxy-readiness-audit.md, oap/audit/results/034-functional-proxy-readiness-evidence.json, research/RESEARCH-STATE.md one-line counter 91->92) plus this sole report; PR 36 created and kept in place. The three unrelated untracked roots, the owner key, retained branches, archives, the read-only index and all prior orders, reports and derivations are preserved. No other path mutation.",
 "checks": [
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py state --repo-root . (umask 077, at the literal implementation head)",
   "result": "PASSED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "state READY; id 034-a; expected branch oap/034-functional-proxy-readiness-audit; no critical gates."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (umask 077, at the literal implementation head)",
   "result": "PASSED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "structure valid; accepted runtime valid against the trusted governance revision; zero CRIT entries."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_ica.py --repo-root . --source oap/audit/results/034-functional-proxy-readiness-audit.md --current-main c36ed4f42534bc13df4dac2b418fb50262d47d06 (umask 077, at the literal implementation head)",
   "result": "PASSED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "schema valid; 59 MVP rows (48 IMPLEMENTED / 7 PARTIAL / 2 UNPROVEN / 2 ABSENT); gaps A-STACK-01, A-CORPUS-02, A-ACCEPT-01, A-API-01, A-EVAL-01, MVP-8, D05, M01, M02, M04, M07; D05 PARTIAL (native)."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py transcript --repo-root . --revision 82301efb4bbc3635e8002331c21c0d44b4492c62 --expected-id 034-a (umask 077, at the literal implementation head)",
   "result": "PASSED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "report_count 92; active and latest 034-a; frozen mutation paths unchanged."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py report-history --repo-root . --revision 82301efb4bbc3635e8002331c21c0d44b4492c62 --require-manifest (umask 077, at the literal implementation head)",
   "result": "PASSED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "report_count 92; all current generated-file manifest identities verified; frozen mutation paths unchanged."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da (umask 077, at the literal implementation head)",
   "result": "FAILED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "DIAGNOSTIC_SET_MISMATCH: the closed five-incident set is extended by a sixth diagnostic - one trailing ASCII space at line 67 of the immutable Root-issued order oap/orders/034-a-functional-proxy-readiness-audit.md. Attributed to the exact issued order (Root engineering mistake), NOT the product; my new audit/evidence bytes are whitespace-clean. Reported truthfully; not repaired/waived; prohibits merge, not publication."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a (umask 077, at the literal implementation head)",
   "result": "FAILED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "DIAGNOSTIC_SET_MISMATCH: same single sixth diagnostic (immutable order line 67 trailing space). Root will issue a bounded SAME-PR corrective suffix after actual publication; the closed-five law is not altered under 034-a."
  },
  {
   "command": "scope/frozen-byte check: git diff --name-only c36ed4f..82301efb4bbc3635e8002331c21c0d44b4492c62; restricted tree diffs (src/, concept-verification/ non-changed, docs/, oap/bin/, oap/tests/, oap/registry/, oap/governance/, oap/prompts/, oap/strategic-instructions/, oap/reports/, PLAN.md, ARCHITECTURE.md, ARCHITECTURE-for-agents.md, SECURITY.md, TESTING.md, AGENTS.md); git diff --check on new bytes (umask 077, at the literal implementation head)",
   "result": "PASSED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "the branch diff touches exactly the five permitted non-report paths; restricted tree diff for every other path is empty; all NEW scoped bytes are whitespace-clean - the only whitespace diagnostic in the diff is the immutable order line 67 trailing space."
  },
  {
   "command": "full offline suite at audited main c36ed4f (preserved final synchronous run; NOT re-run this round - no broad rerun for cosmetic setup)",
   "result": "PASSED",
   "sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "publication_head_claim": false,
   "details": "965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, umask 0077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c; run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z)."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider research/tests/test_research_state_consistency.py::ResearchStateConsistencyTest::test_registry_and_report_counts -q (umask 077, pre-report stage)",
   "result": "FAILED",
   "sha": "82301efb4bbc3635e8002331c21c0d44b4492c62",
   "publication_head_claim": false,
   "details": "the designed pre-report mismatch: AssertionError 92 != 91 (machine block oap_reports_reviewed 92 anticipates this report; 91 .md report files at the implementation head count after the 007-o exclusion); preserved as FAILED - not repaired, rolled back or waived; the report-only commit reconciles it (92 counted, block 92)."
  }
 ]
}
````

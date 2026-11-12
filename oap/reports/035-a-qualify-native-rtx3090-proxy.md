````oap-report
{
 "id": "035-a",
 "result": "PARTIAL",
 "order_path": "oap/orders/035-a-qualify-native-rtx3090-proxy.md",
 "order_sha256": "b0e2bde5af32ada59d6fdadfe6857d321be6acdc6dcc077dcd1ec60283f88cca",
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
 "implementation_head": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
 "publication_verified": false,
 "pr_mode": "CREATE_NEW_PR",
 "pr": 37,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/37",
 "pr_state": "open",
 "branch": "oap/035-native-rtx3090-qualification",
 "base_sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
 "starting_remote_sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-11T16:02:00+00:00",
 "report_written_at": "2026-11-11T16:09:49.687373+00:00",
 "implementation": "The implementation head e9eaeca7324c39c9638fef5b600105c9ce87f9bb is a single forward non-report commit on branch oap/035-native-rtx3090-qualification, sole parent 7dcd186fe394c1262bfe878ba5d6527b888fc317 (verified accepted main / PR36 merge head; CREATE_NEW_PR, real PR 37 created, no second PR, no amend/rebase/reset). It touches exactly the four ordered non-report paths: oap/orders/035-a-qualify-native-rtx3090-proxy.md (this exact issued order), oap/active (034-b -> 035-a), oap/audit/results/035-native-rtx3090-qualification.json (compact sanitized native evidence), and research/RESEARCH-STATE.md (machine counter oap_reports_reviewed 93 -> 94 ONLY; registry_entries 42 and frozen_report_history_incidents 2 unchanged). No product, parser, protection, acceptance, detector, transport, dependency, workflow, source-law, manifest or prior-artifact byte changed; the actual tested product SHA is 7dcd186fe394c1262bfe878ba5d6527b888fc317 (byte-identical product tree to the branch head). No concept-verification/README.md edit was made because no verified useful operator-profile instruction was established in this round (the finding is a native/contract compatibility gap, not an operator configuration), which the order explicitly permits omitting.",
 "documentation": "No product README/PLAN/ARCHITECTURE/SECURITY/TESTING byte touched. concept-verification/README.md was correctly OMITTED (not an unnecessary edit): this round establishes a native/contract compatibility gap and a bounded product remediation proposal, not a verified useful operator-profile configuration instruction; the order permits omission when none is established. The sole docs byte change is research/RESEARCH-STATE.md machine counter oap_reports_reviewed 93 -> 94 (counters-only bookkeeping; registry 42 and incidents 2 and all historical prose unchanged).",
 "criteria": "MET for the qualified native boundary at the accepted base 7dcd186fe394c1262bfe878ba5d6527b888fc317: (a) ACTUAL native serving behavior is observed through real proxy.main() over one owned loopback port 0 with the native RTX3090 Responses route (POST /responses, model qwen3.8-27b-rtx3090 for BOTH MAIN and REVIEW): HTTP 200, completed, ~3.6-6.4s, real transport/contract/detector/reviewer/acceptance/patcher, explicit caller Authorization, child-only in-process reviewer key, concurrency 1, zero auto-retry, zero reviews; (b) the ACTUAL worker/contract return sites are observed with the separately-qualified readonly trace (admitted to the exact transform_json / validate_completed_envelope / aligned_metadata_clean code objects only), pinned at aligned_metadata_clean@245 (field=logprobs) -> validate_completed_envelope@373 (None) -> transform_json@707 (abstain, raw unchanged) -> 0 reviews, reproduced across two independent trace-on native rounds (R4, R4b) and reproduced at the client by the trace-off baseline (R3); (c) the readonly observer is proven read-only (with/without return-value equivalence on local controls) and bound to the exact source lines on current main (local fidelity 4/4, target_posts=0), with the exact-hash 032a real-HTTP worker-observer fidelity reused with its stated local-feasibility scope; (d) the earliest precise failing boundary is preserved content-free and native resampling stops there (no blind repeated failures); (e) shared state/governance/transcript/report-history and both accepted-base whitespace checks pass at the implementation head; (f) the machine counter is 94 with registry 42 and incidents 2 preserved. Native serving/repair is NOT fully qualified: repair eligibility is BLOCKED at the strict stateless contract, so the main->review->independent-validation->exact-span-edit path is not reached; this is reported PARTIAL, not COMPLETE.",
 "negative_paths": "PARTIAL (truthful). The only FAILED check at the implementation head is the designed pre-report research counter test: AssertionError 94 != 93 (machine block oap_reports_reviewed 94 anticipates this 035-a report; 94 .md report files are present, of which 93 count after the 007-o exclusion at the implementation head). This mismatch is expected and is recorded FAILED, not waived or hidden; the sole-report SELF commit reconciles it (95 total report files, 94 counted, block 94) and the final report-head counter is verified afterward privately. The substantive finding is a native compatibility gap, not a harness or publication failure: every native round returned HTTP 200 with a clean lifecycle (normal main return, bounded shutdown complete, serving worker joined, listener closed, child reaped) and zero reviews, but the delivered envelope is not a supported completed response at the client because the native output_text part carries a non-empty logprobs aligned-metadata list. No future push or final-head CI success is claimed inside this pre-push report (publication_verified false; all four required final-head CI checks remain the development-merge gate). No merge, no deployment, no human acceptance.",
 "boundary_fidelity": "Descends from the accepted base 7dcd186fe394c1262bfe878ba5d6527b888fc317 with no amend/rebase/reset/rewrite; the 035-a delta is a single forward non-report commit whose sole parent is 7dcd186fe394c1262bfe878ba5d6527b888fc317. All product/source/dependency/workflow/source-law bytes remain byte-equal across the branch (the full base..head diff is confined to OAP order/active/audit, reports and research/RESEARCH-STATE.md). proxy.py and responses_contract.py remain byte-identical to the separately-qualified 032a observer proofs (836b78cc... / bed932b2...); the immutable 034 order/audit/evidence/report and PRIVATE_INITIAL_034 are untouched; the frozen registry (42) / incidents (2), all 173 generated-manifest identities, the old four-request ledger (a5893b8d..., frozen) and the owner key (0600/ignored/untracked) are preserved.",
 "setup": "Same adopted foreground owner-launched sole CLI process and existing chat (same PID 3341327, cwd, argv codex --yolo --profile early-beta, profile, home, authentication; no new agent, CLI, provider, model, pane, home, auth or reset). Every helper used explicit OAP_ROLE=coding, actual shell umask 077, the qualified Python 3.12.15 interpreter with -B (qualified env bin FIRST in PATH so any real review child python3 is the qualified interpreter), and a private 035 strict scratch under the supervision root with private TMP/cache. Finite owned disposable CPU/Git/HTTP children only; no process-pattern cleanup, no occupied-port or protected-host change. The owner key (0600/regular/owner/75 bytes) is rechecked by fstat boundary and loaded only into the finite owned child env (QWEN_API_KEY) and the explicit caller Authorization header; it is never printed, copied, staged or dumped. Pinned Pandoc 3.7.0.2 (02a59bd9..., verified) is the mandatory startup check before bind. Native opt-in (REPAIR_ALLOW_LIVE_TESTS=YES) is child-only; parent runtime.env/legacy activation flags, CONCEPT_REVIEWER_PROFILE and CODEX_HOME are not toggled.",
 "privacy": "No raw customer text, prompts or answers, targets or replacements, headers, response IDs, exception messages, credentials, the native endpoint URL, or native physical host paths in any public byte. The order, the audit evidence, this report and the counter byte are /home-free, key-free and URL-free (verified by count-only scans of each new blob version, the commit message and this final draft before push). The private owned harness, fixtures, ledger and diagnostics live only in the supplied strict 0700/0600 scratch and are never staged or committed. Only content-free facts are published: verdict labels, source lines, bounded counts, the known aligned-metadata field name (annotations|logprobs), byte-count/latency figures, delivered-byte SHA-256 fingerprints, usage known/unknown and cleanup booleans.",
 "limits": "Product code FROZEN under this order: no compatibility patch was applied before observing the actual case; the finding is a native/contract gap requiring a bounded same-PR product/contract change that strategy must order. No ordinary caller-profile correction is available within the current request contract (optional fields = {temperature, top_p, top_k, max_output_tokens, stop, metadata}; there is no logprobs request field, so the native logprobs emission cannot be suppressed by a request adjustment). No 965 full-suite rerun for counts, no new human dataset/quality-rate estimate, no service/weights/quantization/GPU/network/credential change, no deploy, no milestone or functional acceptance. The four required final-head CI checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) and the independent strategic review precede any development merge. No future push or CI success is claimed inside this pre-push report (publication_verified false).",
 "human_gates": "Decision NONE under D0 (explicitly authorized synthetic request-scoped investigation); this native compatibility gap creates no CRIT entry and no human gate. The owner's explicit allowance of up to 1,000,000 additional RTX3090 requests (witness 035-owner-million-additional-RTX3090-requests-authorization-20261111.json) supersedes the prior 12-request count blocker; only the needed bounded sequential traffic (3 native mains, 0 reviews) was used, stopping at the first actionable unresolved software boundary rather than at any count. Root independently reviews the exact final remote head and owns the conditional development merge and the same-PR remediation order; the owner retains final milestone and deployment decisions.",
 "scope": "Exactly the four ordered non-report paths in the 035-a delta (order, oap/active, oap/audit/results/035-native-rtx3090-qualification.json, research/RESEARCH-STATE.md counters-only) plus this sole report; PR 37 is the single new PR (CREATE_NEW_PR) from verified accepted 7dcd186fe394c1262bfe878ba5d6527b888fc317. concept-verification/README.md omitted (no verified useful operator-profile instruction). The prior 034 order/audit/evidence/report, PRIVATE_INITIAL_034, the frozen registry (42) / incidents (2), all 173 generated-manifest identities, the old four-request ledger (frozen), the three unrelated untracked roots (.rclone-speed-test/, .research-test-scratch/, corpus/), the owner key, retained branches, archives and the read-only index are preserved. No other tracked path mutation.",
 "checks": [
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py state --repo-root . (umask 077, at implementation head e9eaeca7324c39c9638fef5b600105c9ce87f9bb)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "state READY; id 035-a; branch oap/035-native-rtx3090-qualification; pr null (pre-PR); no critical entries or open gates."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (umask 077, at implementation head e9eaeca7324c39c9638fef5b600105c9ce87f9bb)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "structure valid; accepted-runtime valid against the trusted governance revision 3549de2a; no CRIT entries; D0."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py transcript --repo-root . --revision e9eaeca7324c39c9638fef5b600105c9ce87f9bb --expected-id 035-a (umask 077)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "transcript valid; active and latest 035-a; orders list ends 035-a; report_count 94; frozen mutation paths unchanged."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py report-history --repo-root . --revision e9eaeca7324c39c9638fef5b600105c9ce87f9bb --require-manifest (umask 077)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "report history valid; all current generated-file manifest identities verified; report_count 94; frozen 006-a/006-c incidents preserved."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision e9eaeca7324c39c9638fef5b600105c9ce87f9bb (umask 077)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "closed-six contract: exactly six exact diagnostics at this authorized base; the new 035-a order introduces no new whitespace incident."
  },
  {
   "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision e9eaeca7324c39c9638fef5b600105c9ce87f9bb (umask 077)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "closed-six contract: exactly six exact diagnostics at this second authorized base (same set as base 2832fa1e)."
  },
  {
   "command": "env OAP_ROLE=coding PATH=qualified/bin:$PATH qualified python -B -m pytest -p no:cacheprovider research/tests/test_research_state_consistency.py::ResearchStateConsistencyTest::test_registry_and_report_counts -q (umask 077, pre-report stage)",
   "result": "FAILED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "the designed expected pre-report mismatch: AssertionError 94 != 93 (machine block oap_reports_reviewed 94 anticipates this 035-a report; 94 .md report files present, 93 count after the 007-o exclusion at the implementation head). Recorded FAILED, not waived or hidden; the sole-report SELF commit reconciles it (95 total, 94 counted, block 94) and the final report-head counter is verified afterward privately."
  },
  {
   "command": "private owned harness: qualified python -B q035_qualification.py fidelity (OAP_ROLE=coding, umask 077, target_posts=0, no network)",
   "result": "PASSED",
   "sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
   "publication_head_claim": false,
   "details": "local fidelity 4/4 on the ACTUAL code objects (malformed->ProxyError@704; unsupported message.status->validate@357+transform@707; clean eligible->aligned@246+validate@378+transform@712; controlled edit->aligned@246+validate@378+transform@714); observer read-only with/without equivalence true for clean and controlled_edit; actual product SHA 7dcd186fe394c1262bfe878ba5d6527b888fc317."
  },
  {
   "command": "private owned harness: qualified python -B q035_qualification.py r3 (OAP_ROLE=coding, umask 077, REPAIR_ALLOW_LIVE_TESTS=YES, child-only, native RTX3090, TRACE OFF, 1 main + reserved review, zero auto-retry)",
   "result": "PASSED",
   "sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
   "publication_head_claim": false,
   "details": "native baseline: HTTP 200, 2004 bytes, 3.6343 s, client not-supported, review_calls 0; clean lifecycle (normal main return 0, bounded shutdown complete, serving worker joined, listener closed, child reaped). Reproduces the prior native client-not-supported result; no internal predicate (trace off)."
  },
  {
   "command": "private owned harness: qualified python -B q035_qualification.py r4 (OAP_ROLE=coding, umask 077, native RTX3090, TRACE ON readonly observer, 1 main + reserved review, zero auto-retry) and one targeted R4b refinement run admitting aligned_metadata_clean to pin the exact known field name",
   "result": "PASSED",
   "sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
   "publication_head_claim": false,
   "details": "ACTUAL worker boundary pinned content-free: aligned_metadata_clean@245 (field=logprobs) -> validate_completed_envelope@373 (None) -> transform_json@707 (abstain, raw unchanged) -> review_calls 0 -> independent client judge not-supported@373. R4: HTTP 200, 2366 bytes, 5.6023 s; R4b: HTTP 200, 2524 bytes, 6.3706 s, both field=logprobs, both clean lifecycle. Native serving qualified (bounded); native repair eligibility BLOCKED at the strict stateless contract. No native URL/key/private path or raw payload recorded."
  },
  {
   "command": "scope/product/source/dependency equality: git diff --name-only 7dcd186fe394c1262bfe878ba5d6527b888fc317..e9eaeca7324c39c9638fef5b600105c9ce87f9bb; restricted tree diffs (src/, tests/, scripts/, .github/, requirements*, pyproject.toml, uv.lock, concept-verification/, oap/bin/, oap/governance/, oap/prompts/, oap/strategic-instructions/, PLAN.md, ARCHITECTURE*.md, SECURITY.md, TESTING.md, AGENTS.md); git diff --check on new bytes (umask 077, at implementation head e9eaeca7324c39c9638fef5b600105c9ce87f9bb)",
   "result": "PASSED",
   "sha": "e9eaeca7324c39c9638fef5b600105c9ce87f9bb",
   "publication_head_claim": false,
   "details": "the 035-a delta touches exactly the four ordered non-report paths; the full branch diff base..head touches only OAP order/active/audit, reports and research/RESEARCH-STATE.md; every restricted product/source/dependency/workflow/source-law tree diff is empty; all new scoped bytes are whitespace-clean."
  }
 ]
}
````

````oap-report
{
 "id": "035-d",
 "result": "COMPLETE",
 "order_path": "oap/orders/035-d-useful-native-repair-and-policy-regressions.md",
 "order_sha256": "230f0d33b3811c1fcec19969cf9f1cd3cc2df8d73cf4ce354b1073d48e4b8ef7",
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
 "implementation_head": "f64da105835a194b35acb9314b518f54efc73b1f",
 "publication_verified": false,
 "pr_mode": "AMEND_EXISTING_PR",
 "pr": 37,
 "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/37",
 "pr_state": "open",
 "branch": "oap/035-native-rtx3090-qualification",
 "base_sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
 "starting_remote_sha": "c304bf16e5100337d0ee02244c5a88b5be9028c6",
 "no_merge": true,
 "critical_action": "NONE",
 "pr_observed_at": "2026-11-12T04:41:19.608400+00:00",
 "report_written_at": "2026-11-12T04:43:53.018119+00:00",
 "implementation": "Two forward non-report commits on branch oap/035-native-rtx3090-qualification: c1fa0c2 (sole parent c304bf16, the 035-c report head and actual starting remote) and the documentary correction f64da10 (sole parent c1fa0c2). Non-report paths: exact issued order, oap/active, concept-verification/README.md (contract correction, 035-c policy section, native qualification results with corrected counts/scopes), concept-verification/tests/test_responses_contract.py (net 17 new persisted policy regressions: 20 methods added, 3 old methods rewritten in place, none lost/skipped), oap/audit/results/035-native-rtx3090-qualification.json (current sanitized evidence, reconciled 46-row ledger state, truthful supersession of C's stale claims), research/RESEARCH-STATE.md (machine counter 96->97 only). Runtime bytes frozen at 035-c: proxy.py 86df8af2..., responses_contract.py 0d9347c5...; no product module mutated in either commit.",
 "documentation": "concept-verification/README.md now states the final reviewed behavior: the proxy provides no token probabilities; defined API logprobs are always removed for every value, JSON/SSE, no switch; the qualified native message-array profile with its limits; and the 035-d useful+clean native results scoped to their actual epochs (two-deadline launcher proof bound to the final qualifying pair; earlier harness/launcher epochs qualified at their own limits). Sole other docs change: research/RESEARCH-STATE.md machine counter 96->97 (registry 42, incidents 2, 173-file GENERATED-FILES manifest unchanged). No product README/PLAN/ARCHITECTURE/SECURITY/TESTING byte touched. PR37 title/description updated to the final reviewed behavior (no merge action).",
 "criteria": "COMPLETE: (a) A1 - README contract corrected and net 17 persisted regressions prove the single unconditional probability-removal policy with correct 0/1 review counts, accepted exact edits, all defined copies, unchanged unrelated data and existing failure/protection contracts (focused 206 OK; named UTF8/surrogate set 5 OK; named two-target integration 2 OK); (b) A2 - actual native matching-RTX3090 proof at the real worker boundary: 11 executed MAIN POSTs all HTTP 200 (combined envelope scope 9 completed + 2 incomplete, the latter being the 1536-budget trial and the direct diagnostic at that budget whose usage showed output_tokens at the 1536 max, reason recorded only as masked type str; 4096 used thereafter per the observed budget exhaustion), 5 same-RTX review attempts with 3 observed validated batches (attempts 25/30/32; 21/23 unclassified), the final qualifying pair's useful trial delivering one useful accepted correction (1 candidate -> 1 observed validated review, known usage 281/480/761 -> 1 approved exact original-span edit 6cp->5cp, protected interval unmodified, cross-observer original-identity/composition/untouched-slice/protected-overlap proofs all true, delivered envelope differing only by defined logprobs removals and the approved text) and its clean trial proving the genuine fully-observed clean 0-review control (0 candidates -> 0 review calls -> identical delivered answer); earlier trials preserved and qualified at their own epochs; (c) A3 - same-PR history/scope/privacy/governance and truthful publication: exact order bytes, both accepted-base whitespace checks PASSED, state/governance/transcript/report-history PASSED at the implementation head, pre-report counter mismatch FAILED as expected (97!=96), unpublished preflight, one fresh full concept suite 1006 OK literal interpreter exit 0. Controlled functional-path evidence only: not a quality rate, statistical independence, human acceptance, ICA or deployment claim.",
 "negative_paths": "Pre-report counter test FAILED (97!=96, expected; reconciles to 98 report files/97 counted/block 97 post-report; final counter checked privately). One trial (attempt 27) and one direct diagnostic (attempt 29) at the 1536 output budget returned incomplete envelopes (single reasoning item, no completed assistant message; diagnostic usage output_tokens=1536=max; incomplete reason masked as type str, no raw reason string claimed). Two review attempts (21, 23) remain unclassified from their retained observers (usage UNKNOWN); two trials (25, 30) were reviewed-but-unchanged with no accepted edit delivered (keep vs CPU-rejection UNKNOWN from those observers). Native plain-string input remains rejected by the upstream endpoint with its own field-shape 400 (upstream caller-format property, not a proxy defect). No future push or CI success claimed (publication_verified false).",
 "boundary_fidelity": "Descends from 035-c report head c304bf16 with no amend/rebase/reset; actual starting_remote_sha c304bf16 retained in this report after both implementation pushes per the order. All prior orders/reports/artifacts immutable. Forward qualification of 035-c recorded, not rewritten: C's starting_remote_sha named its implementation commit 8e9b373 rather than the actual 553280a entry head at C's start; C's 12-allocation ledger scalar did not match its actual 14-row ledger; C's clean-lifecycle wording rested on an undefined shutdown variable with false join/shutdown flags (superseded by the epoch-scoped 035-d observed lifecycle and the two-deadline launcher's offline five-case clock proof); C's 989-test suite epoch predates the final test bytes. Frozen registry (42)/incidents (2)/173-file manifest preserved. Private INITIAL_034 unchanged. Owner key 0600/ignored/untracked. Three unrelated roots preserved.",
 "setup": "Same owner-launched foreground CLI 3341327/chat/model/profile/home/auth/cwd; externally consumed control, no second wait. OAP_ROLE=coding, umask 077, qualified Python 3.12.15 -B, pinned Pandoc 3.7.0.2, private TMP/cache. No new agent/CLI/provider/model/home/auth. Owner 1M RTX allowance and 10 publication recoveries persist.",
 "privacy": "No raw answers/prompts/targets/replacements/headers/IDs/keys/native URLs/private paths in public bytes. Count-only scans clean over all new blobs, commit messages, PR body/title and this report. Private harness/ledger/diagnostics and the historical raw-prefix diagnostics remain in 0700/0600 scratch only and are never copied forward.",
 "limits": "Controlled functional-path evidence at the real worker boundary on the authorized matching-RTX3090 endpoint only: not a natural-error rate, linguistic quality, statistical independence of two same-model calls, human acceptance, ICA or deployment claim. No universal provider compatibility claimed. Earlier trial epochs are qualified at their own supervision limits, not retroactively upgraded. The four final-head CI checks and strategic independent review precede any development merge; coding never merges or self-accepts; a fresh isolated full-source closure audit is requested by strategy after verified development merge.",
 "human_gates": "Decision NONE under D0. Owner 1M RTX + 10 publication recoveries (1 used) persist. Root reviews exact final remote head.",
 "scope": "Exactly 6 non-report paths across two forward commits + sole report. Same PR 37/branch. No other tracked path mutation. No runtime mutation; no merge/auto-merge/deployment.",
 "checks": [
  {
   "command": "oap_cli.py state (at impl head f64da10)",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "state READY; id 035-d; PR 37; no critical entries."
  },
  {
   "command": "oap_cli.py governance --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (at impl head f64da10)",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "structure valid; accepted-runtime valid; coding bytes unchanged."
  },
  {
   "command": "oap_cli.py transcript --revision f64da10 --expected-id 035-d",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "valid; active 035-d; report_count 97 (pre-report)."
  },
  {
   "command": "oap_cli.py report-history --revision f64da10 --require-manifest",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "valid; count 97; 2 frozen incidents."
  },
  {
   "command": "check_whitespace --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision f64da10",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "6 pinned diagnostics; no new incidents."
  },
  {
   "command": "check_whitespace --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision f64da10",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "6 pinned diagnostics; no new incidents."
  },
  {
   "command": "unittest tests.test_research_state_consistency -k registry_and_report_counts (pre-report)",
   "result": "FAILED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "Expected pre-report mismatch: 97!=96. Reconciles post-report to 98 report files/97 counted/block 97; final counter checked privately."
  },
  {
   "command": "Focused suites at final test bytes (test_responses_contract + test_review_batch; 5 named UTF8/surrogate regressions; 2 named two-target integration tests)",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "206 + 5 + 2 tests OK, literal exits 0 (pinned Pandoc, private TMP/cache)."
  },
  {
   "command": "Full concept suite (discover -s tests -v, qualified Python 3.12.15 -B, pinned Pandoc 3.7.0.2, private TMP/cache)",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "1006 tests OK in 718.100s; literal interpreter exit 0 captured after the Python process; private complete log preserved."
  },
  {
   "command": "Native final qualifying pair (attempts 32/34, two-deadline launcher fd969206..., harness d9e7948e..., RO index f769235b..., head c304)",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "Both HTTP 200 completed; useful trial: 1 candidate, 1 observed validated review (usage 281/480/761), 1 approved edit 6cp->5cp, all cross-observer proofs true, envelope diff only defined logprobs + approved text; clean trial: 0 candidates, 0 review calls, identical answer; full observed lifecycle both trials, neither clock expired. Earlier epochs (15-25 direct-Python harness revisions; 27/30 parent-only 180s launcher da3bca36) preserved at their own limits."
  },
  {
   "command": "oap_cli.py preflight-report --id 035-d --source private-scratch-draft --expected-head f64da10",
   "result": "PASSED",
   "sha": "f64da105835a194b35acb9314b518f54efc73b1f",
   "publication_head_claim": false,
   "details": "valid unpublished report draft; canonical report absent from the repository during preflight."
  }
 ]
}
````

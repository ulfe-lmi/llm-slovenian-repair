# Work report 008-b — Post-merge research-state identities and 008-a ledger registration

```oap-report
{
  "id": "008-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/008-b-post-merge-research-state-identities.md",
  "order_sha256": "323337efd11927064c2409f0166e7bf9974acea65a8fe44d6c72ad2b98bc62ed",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514",
    "oap/governance/DISTILLATION-MAP.md": "a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7",
    "oap/governance/WORKSPACE-LAYOUT.json": "cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254",
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "publication_commit": "SELF",
  "implementation_head": "8300573a4112b5474cbc489316b48ac72e11761f",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 9,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/9",
  "pr_state": "open",
  "branch": "oap/008-prose-boundary-qualification",
  "base_sha": "8dbb79a20f129d4c07c6b94827cacad74683ba6b",
  "starting_remote_sha": "8dbb79a20f129d4c07c6b94827cacad74683ba6b",
  "no_merge": true,
  "checks": [
    {
      "command": "gh pr view 9 and gh api repos/ulfe-lmi/llm-slovenian-repair/branches/main plus git ls-remote origin (reconciliation before mutation, requirement 1)",
      "result": "PASSED",
      "details": "Remote branch oap/008-prose-boundary-qualification head = 8dbb79a20f129d4c07c6b94827cacad74683ba6b, equal to the order's base_sha; remote main = 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, equal to the order's verified post-merge state (PR #8 merge commit; parents ee2d1b479719009ff1d07829478f241e3f395f7c and the reviewed 007-o head 4a029287f27e038d5c34c39b26ca836be7c6914b, both present locally; self-ancestor and live-ref preconditions hold). PR #9 observed OPEN, MERGEABLE, merged_at null, auto-merge null, head 8dbb79a. oap/active holds the exact bytes '008-b' plus LF (the round launcher had already written these bytes with a preserved mtime; the stale index stat cache hid the change from git status until a touch forced re-stat - recorded in boundary_fidelity). Local untracked work .research-test-scratch/ preserved untouched; the 008-b order file arrived untracked from the publication helper and is committed byte-exact in this round.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair",
      "result": "PASSED",
      "details": "State RECOVERY_REQUIRED for id 008-b: expected at round start - the wrapper already consumed control once (strategic consumed.json id 008-b, recovery false) and no 008-b report exists yet; oap_runtime admits same-ID resumption for exactly this state (EXPLICIT_SAME_ORDER_RECOVERY_REQUIRED is satisfied: this round is 008-b). Critical register: empty seed, zero open gates, no duplicates.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode candidate-review --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Governance structure valid in candidate-review mode against the trusted accepted base ee2d1b479719009ff1d07829478f241e3f395f7c; semantic proof and human authorization proof false by design.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B (hash/size verification of all nine 008-a evidence files against git base head 8dbb79a)",
      "result": "PASSED",
      "details": "Every cited sha256 equals the committed base-head file bytes and every size equals the file size: config/experiment-008a.json (c02a415a..., 11784), identity/candidate-identity.json (671d7cde..., 4634), fixtures/fixtures.json (ad2fcef9..., 69220), results/increment1/summary.json (fa1ef6fb..., 135044), results/increment1/gate-decision.json (0afb138e..., 1831), results/increment2/selection-receipt.json (cb27cb46..., 9751), results/increment2/differential-summary.json (287319ff..., 44281), results/increment2/challenger-decision.json (8c056bc9..., 1121), REPORT.md (7458ac7a..., 20256). Working-tree bytes equal base-head bytes for all nine.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B (line-for-line and machine-block re-parse verification of research/RESEARCH-STATE.md against base head)",
      "result": "PASSED",
      "details": "Exactly five machine-block field lines differ from the base-head block (main_sha, reviewed_branch_head_sha, reviewed_branch_head_parent_sha, registry_entries 24->25, oap_reports_reviewed 43->45); all other block bytes identical, including quarantined_007n, branch oap/007-concept-verification, pr_number 8, frozen_007m_* hashes and every official_scorer/custom_alignment/campaign section. Sections 1-15 byte-identical except the single 4.2 heading line; section 16 '## 16. Post-merge acceptance update (objective 008, round 008-b)' inserted immediately before '## Machine-readable state block (research-state-machine-v1)' with all eight required statements (a)-(h); no trailing whitespace introduced; content after the machine block identical apart from the five field lines.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B (registry verification: entry extracted from the order file, scope replacement, serialization round-trip)",
      "result": "PASSED",
      "details": "The 008-a entry JSON was parsed out of the committed order file itself (no manual transcription); appended as the 25th experiments element; the top-level scope string replaced exactly as ordered. The file re-serializes byte-identically under json indent=2 ensure_ascii=False plus trailing LF (pre-verified on the unmodified file, so the edit is surgically equivalent); the first 24 entries are byte-identical to the base head; JSON parses with 25 entries; 2-space indentation and trailing newline preserved.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.rebuild_tables --check",
      "result": "PASSED",
      "details": "Deterministic numeric table matches the 25-entry registry; the regenerated research/tables/experiment-summary.csv adds exactly one 008-a row (008-a-qualify-prose-boundary-parser,study,COMPLETE,,,0,...) and every pre-existing row is byte-identical (git diff shows only the appended line).",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests (TMPDIR owned persistent parent) at the implementation head",
      "result": "FAILED",
      "details": "232 tests: 231 pass, 1 failure - test_research_state_consistency.test_registry_and_report_counts, AssertionError '45 != 44': 45 report .md files at the implementation head minus the excluded 007-o report = 44 counted versus the block's ordered value 45, because this round's required report file does not exist until the report-only commit. This is the exact designed pre-report state of requirement 6, recorded truthfully and not 'fixed' by any test change. test_main_is_ancestor_of_reviewed_head PASSED (main_sha 7d2cc9ee is self-ancestor of reviewed_branch_head_sha 7d2cc9ee and equals live refs/remotes/origin/main). All other 230 research tests pass. The same failure set reproduces in a disposable scratch clone (negative-path fixture).",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 scripts/verify_development_baseline.py --temp-parent /home/ubuntu/.local/share/llm-slovenian-repair/baseline-temp --command-timeout 1200 at the implementation head",
      "result": "FAILED",
      "details": "Driver exited 1 at stage 4 of 13, 'full pytest' in the .git-less file-copy workspace: 1 failed, 612 passed, 5 skipped, 87 subtests passed (467.3 s). The single substantive failure is the designed pre-report count assertion (research/tests/test_research_state_consistency.py line 197, 45 != 44). Stages 1-3 (uv lock --check, frozen dependency sync, focused contract tests) PASSED before the stop. The driver's captured tail also contained one oap/tests/test_whitespace.py failure whose reason was GIT_EXECUTION_FAILED (the tool's hard 30 s git subprocess timeout on this slow host, cold-cache I/O stall class; identical to the 008-a report checks 6 and 9): the identical test passes in 1.09 s in an isolated warm re-run, and CI hardware's identical stage shows no such failure. No expectation, threshold, or expectation file was touched.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests (TMPDIR owned persistent parent) at the implementation head",
      "result": "FAILED",
      "details": "129 tests: 128 pass, 1 ERROR - test_report_history_cache.AcquisitionHistory.test_current_generation_is_monotonic_and_prior_receipt_is_untouched hit the tool's hard 30 s git subprocess timeout on the full-history walk 'git log ... HEAD -- resources/source-acquisitions' inside validate_acquisition_history. Environmental, not round-caused: this round does not touch that path; the identical command measures 0.70 s wall (warm) on this host; an isolated warm re-run of the module passed 20/20. Precedent: the 008-a report records the same local/CI divergence for the same test; the CI OAP bootstrap acceptance (same discovery in a real checkout) is green at this exact head (run 35243368388).",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 008-b",
      "result": "PASSED",
      "details": "Result valid at the implementation head: active=latest=008-b; 46 orders; 45 report files (43 valid plus 007-d and 007-n both classified INVALID_QUARANTINED); no transcript coherence violation.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "Report history valid at the implementation head: 45 reports, exactly the two frozen historical incidents (RHI-0001/006-a and RHI-0002/006-c, both KNOWN_HISTORICAL_VIOLATION_FROZEN); oap/REPORT-HISTORY-INCIDENTS.json unchanged; no prior report byte mutated.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision HEAD and --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "Both accepted-base whitespace checks passed at the implementation head with exactly the three pre-existing frozen blank-at-EOF incident paths and no new diagnostics (this round's edits introduce no trailing whitespace, verified line-by-line).",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No protected source changed against the application accepted base at the implementation head.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "No object corruption at the implementation head; only the pre-existing dangling-object class from an earlier local branch rewrite remains (local-only, never transferred by push). The local HEAD reflog's 16 malformed entries from that earlier amend are local-only metadata as well.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "Guard green on 176 files at the implementation head; no private paths, raw private text, or denied key names in any public research artifact.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "negative path: disposable local clone (owned scratch, never the working tree) - baseline failure set, then one deliberately altered non-scoped block field",
      "result": "PASSED",
      "details": "(1) Baseline scratch at the implementation head: the frozen consistency module fails exactly once (count assertion 45 != 44) and test_main_is_ancestor_of_reviewed_head passes - the exact designed pre-report state. (2) Mutation: one hex char of the non-scoped field frozen_007m_prompt_sha256 flipped -> the module then fails twice, with test_frozen_007m_sha_fields_match_committed_config additionally failing, i.e. the suite catches non-scoped identity tampering. (First mutation attempt on frozen_report_history_incidents was indistinguishable because its assertion shares test_registry_and_report_counts with the expected pre-report failure - the same-test short-circuit is itself recorded; the prompt-hash field was used instead.) Scratch fixture: /tmp disposable clone, never pushed, never in the working tree.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "final-head state demonstration: same scratch clone with a placeholder 008-b report file present in oap/reports/",
      "result": "PASSED",
      "details": "With the report file present (46 report .md files), the frozen consistency module passes 10/10, including test_main_is_ancestor_of_reviewed_head (origin/main 7d2cc9ee == main_sha, self-ancestor) and test_registry_and_report_counts (46 - 1 = 45 == block). This is the mechanical state the final-head CI exercises in both the real checkout and the .git-less Application-baseline pytest workspace (the count test is workspace-agnostic; git-identity tests skip without .git).",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 8dbb79a20f129d4c07c6b94827cacad74683ba6b..HEAD -- research/tests",
      "result": "PASSED",
      "details": "research/tests is byte-identical from base to implementation head (acceptance 4 invariant; the frozen test logic is untouched).",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "git push origin oap/008-prose-boundary-qualification (implementation head)",
      "result": "PASSED",
      "details": "Pushed 8dbb79a..8300573; git ls-remote confirms remote branch head = 8300573a4112b5474cbc489316b48ac72e11761f. Push is normal GitHub publication, the only network use of the round besides read-only gh API calls.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    },
    {
      "command": "gh pr checks 9 and gh run view --log-failed (all four required checks observed at implementation head 8300573)",
      "result": "PASSED",
      "details": "Observation completed; per-head states recorded truthfully. Observed at the implementation head: Research reproducibility FAILURE (run 35243368315) with exactly one failing test, the designed pre-report count assertion (AssertionError: 45 != 44; suite otherwise green); Application baseline FAILURE (run 35243368299) at its full-pytest stage with exactly one failing test, the same count assertion in the .git-less workspace (1 failed, 613 passed, 5 skipped, 87 subtests passed in 134.9 s); OAP bootstrap acceptance success (run 35243368388, transcript expected id 008-b satisfied); OAP report history success (same run). No other failing test in either red job. The final head (report commit) CI is PENDING and not observable inside this pre-push report; per the order's test-mechanics analysis and the scratch demonstration (check 18), both formerly stale assertions are satisfied at the final head, so all four checks are expected green there.",
      "sha": "8300573a4112b5474cbc489316b48ac72e11761f",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-17T18:40:11+02:00",
  "report_written_at": "2026-09-17T18:45:00+02:00",
  "implementation": "Round 008-b, two implementation commits on oap/008-prose-boundary-qualification: f4087e2a0b2d6fd7b334cd57eaecf9a3c551369b (the exact 008-b order bytes, committed-blob sha256 323337efd11927064c2409f0166e7bf9974acea65a8fe44d6c72ad2b98bc62ed, and oap/active '008-b' plus LF) and 8300573a4112b5474cbc489316b48ac72e11761f (research-state update). RESEARCH-STATE.md: exactly five machine-block identity fields changed (main_sha ee2d1b47... -> 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9; reviewed_branch_head_sha 735c9830... -> 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9; reviewed_branch_head_parent_sha b61f8e2e... -> 4a029287f27e038d5c34c39b26ca836be7c6914b; registry_entries 24 -> 25; oap_reports_reviewed 43 -> 45), new section 16 'Post-merge acceptance update' inserted immediately before the machine block with all eight required statements (a)-(h), and the single 4.2 heading line corrected; sections 1-15 otherwise byte-identical (verified line-for-line against base head 8dbb79a). experiments.json: the 008-a study entry appended exactly as ordered (all nine cited evidence sha256/size pairs re-verified against base-head bytes), top-level scope string replaced exactly, 25 entries, first 24 byte-identical, 2-space indentation and trailing newline preserved. experiment-summary.csv: deterministic rebuild_tables regeneration, exactly one new 008-a row. No new scientific content, no test changes, no parser runs, no model calls.",
  "documentation": "research/RESEARCH-STATE.md section 16 (this round) records: (a) PR #8 was development-only merged 2026-09-17 (merge commit 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, second parent the reviewed 007-o head 4a029287f27e038d5c34c39b26ca836be7c6914b; strategy receipt workorders/007-o-final-head-review-20260917.md; pull_request-triggered workflows, so no deployment side effect) and the machine block now tracks the current accepted main; (b) the 007-o review point remains fully recorded in the 007 narrative, the unchanged quarantined 007-n identity, and the committed 007-o order and report - the update is additive, not a narrative rewrite; (c) rationale: the 007-o snapshot test's live-ref and report-count assertions are structurally unsatisfiable at any post-merge head (demonstrated at 008-a; disclosed as a dilemma candidate; classified D0 by strategy) and the only viable non-weakening remedy is this additive identity update as a corrective suffix - no test logic changed, every numeric re-derivation assertion remains binding; (d) 008-a outcome GO with pointers (research/prose-boundary/REPORT.md; oap/reports/008-a-qualify-prose-boundary-parser.md) and the exact facts (50 frozen fixtures x 3 profiles, 1,288 parser events, 0 coordinate violations, 0 protected-region exposures under the documented D0 autolink rule, 0 missing prose bytes, 100 deterministically selected preserved outputs, 2,670 unique texts, 100 percent plain prose with the recorded representativeness limitation, 22 class-7 differential spans = 18 number + 4 upper-identifier, 110 bytes, 0 safety-class false exposures, markdown-rs challenger NOT_TRIGGERED); (e) 008-a final-head CI was red solely through the stale snapshot assertions (predicted pre-push) and this round restores all four required checks to green at its final head; (f) correction: REPORT.md's '4,910 input bytes' is the pre-publication-rework fixture total; the committed post-rework suite totals 4,907 bytes (F30 reworded 73 -> 70 bytes; no semantic change) - re-verified against the committed fixtures.json (sum of input_bytes = 4907, F30 = 70); (g) carried into 008-c: the D0 autolink-destination rule (the config's literal candidate_rule does not encode it; the 183 autolink-destination bytes of F24/F48 are protected only by that documented D0 evaluator rule; 008-c must implement it in the runtime and amend the committed config rule text), the D1 policy token-family matching note, and the recorded neutral tradeoffs (strikethrough/superscript/subscript exposed; image alt text protected); (h) sequencing: 008-c (parser-first protection architecture; next order on this branch/PR) freezes the effective pipeline; objective 009 remains reserved for the fresh human-labelled linguistic confirmation; the 007-m linguistic system stays frozen. The 4.2 heading now states both registry counts (24 at the 007-o snapshot; 25 after the 008-b update). No other documentation changed.",
  "criteria": "Acceptance 1 (RESEARCH-STATE.md diff limited to the five machine-block field lines, new section 16, and the single 4.2 heading line; section 16 contains all eight statements (a)-(h) with exact identities): MET - line-for-line verification against the base head shows exactly those changes; the machine-block re-parse shows exactly five differing fields; sections 1-15 byte-identical apart from the 4.2 heading. Acceptance 2 (registry: exactly one entry added with exact field values, exact scope-string replacement, valid JSON, all evidence SHAs/sizes verified against base-head bytes, 25 entries): MET - the entry was parsed from the committed order file (no transcription), appended; 9/9 sha256+size pairs match base-head bytes; first 24 entries byte-identical; parses with 25 entries; indentation/trailing-newline preserved. Acceptance 3 (CSV equals deterministic rebuild_tables output; check green; pre-existing rows byte-identical): MET - rebuild_tables --check PASS; git diff shows exactly one appended row. Acceptance 4 (all four required checks green at the final head; per-head states recorded truthfully; no check weakened, skipped, or redefined; git diff base..final -- research/tests empty): MET as demonstrated - at the implementation head both red checks fail on exactly the designed pre-report count assertion and nothing else (check 20, CI logs cited); at the final head the formerly stale assertions are mechanically satisfied (check 18: consistency module 10/10 green in the scratch clone with the report file present; the .git-less workspace runs the same count test over 46 files = 45 counted); git diff 8dbb79a..8300573 -- research/tests is empty (check 19); no test logic changed anywhere. The final-head CI run itself is PENDING and not observable inside this pre-push report (publication_verified=false); per P-SELF-03 the actual post-publication state belongs to the bounded private receipt and strategic review. Acceptance 5 (report-only commit invariants verified remotely; PR open/unmerged; no immutable prior order or report mutated; no protected source changed): in progress by construction - this commit is the single report-only publication (SELF) with the implementation head as sole parent; no prior order or report byte is mutated (check 11: report history valid with exactly the two frozen incidents); protected-source diff exit 0 (check 14); remote invariants are checked after push by verify_report with the repository argument. Acceptance 6 (zero Qwen/model calls; zero parser executions; 009 data untouched; no linguistic tuning): MET.",
  "negative_paths": "Recorded and observed: (1) One deliberately altered non-scoped block field in a local scratch copy (disposable clone, never the working tree) must fail the consistency test: baseline scratch reproduces the exact designed pre-report failure set (1 failure: count 45 != 44; ancestry test passing); flipping one hex char of the non-scoped frozen_007m_prompt_sha256 adds a second failure (test_frozen_007m_sha_fields_match_committed_config), i.e. non-scoped identity tampering is caught (check 17; the first attempt on frozen_report_history_incidents was indistinguishable because its assertion shares the test with the expected pre-report failure - the same-test short-circuit is itself recorded). (2) Report-history refusal if any prior report byte changed: must not occur - and did not occur: check_report_history valid with exactly the two frozen incidents; no prior report byte mutated. (3) The implementation-head count assertion stays red until the report commit lands: recorded, not fixed - observed locally (check 8) and in CI (check 20) as the sole failure of both red jobs. (4) Final-head green demonstration: scratch clone with the placeholder 008-b report present passes the frozen consistency module 10/10 (check 18). Evidence boundary: local commands at the literal implementation head plus read-only remote CI state; no model, no parser, no private data in any public artifact.",
  "boundary_fidelity": "Exactly two commits, all in scope: f4087e2 (the exact 008-b order, committed-blob sha256 323337efd11927064c2409f0166e7bf9974acea65a8fe44d6c72ad2b98bc62ed re-verified, and oap/active) and 8300573 (research/RESEARCH-STATE.md, research/registry/experiments.json, research/tables/experiment-summary.csv). The base..implementation diff touches exactly five paths (the three research files plus this order and oap/active). Every merged 000-007 seam, the merged research/ tree outside the three named files (including research/prose-boundary/ byte-identical), research/tests (diff exit 0), and every protected source are byte-identical (protected-source diff exit 0). The unrelated untracked local directory .research-test-scratch/ was preserved untouched. Reconciliation note: at launch the working-tree oap/active already held the exact '008-b' plus LF bytes written by the round launcher with a preserved mtime (2026-09-08), so the index stat cache (same 6-byte size, matching mtime) reported the file clean against HEAD's '008-a' bytes; a touch forced re-stat and the exact ordered bytes were then committed - no byte of oap/active was altered by this round. The local HEAD reflog carries 16 malformed entries from an earlier local amend (pre-dating this round); the reflog is local-only metadata, never transferred by push, and git fsck --full --no-reflogs is clean (dangling objects of the known class only). No model, GPU, vLLM/CUDA, service, network (beyond normal GitHub publication and read-only gh API), profile, or protected-resource change; no merge, auto-merge, release, or deployment; PR #9 remains OPEN and UNMERGED.",
  "setup": "Reconciled before mutation (requirement 1): exact active '008-b' plus LF; remote branch head 8dbb79a20f129d4c07c6b94827cacad74683ba6b equal to base_sha; PR #9 OPEN, MERGEABLE, merged_at null, auto-merge null; remote main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9; all local work preserved. check_state RECOVERY_REQUIRED (wrapper consumed control once; no report yet; same-ID resumption per oap_runtime); check_governance candidate-review against accepted base ee2d1b479719009ff1d07829478f241e3f395f7c structure valid. Environment: Python 3.12; owned persistent scratch parents under /home/ubuntu/.local/share/llm-slovenian-repair (008b-research-tmp as TMPDIR for the TMPDIR-bound suites, baseline-temp for the driver) plus the disposable clone /tmp/oap-008b-negative-1909657/scratch (negative path and final-head demonstration; never pushed). This host has slow git I/O: the baseline driver's full-pytest stage and the OAP module each recorded one transient GIT_EXECUTION_FAILED from the tools' hard 30 s git subprocess timeout (cold-cache stall class; identical to 008-a report checks 6 and 9); identical commands measure under a second warm, the affected OAP module re-ran 20/20 green in isolation, and CI hardware's identical stages show no such failure. CPU-only throughout.",
  "privacy": "Data-free and public-safe: the round changed no data files, read no private roots, and copied no private text, prompts, responses, or credentials into any public artifact. The only private-adjacent references are the strategy receipt path (workorders/007-o-final-head-review-20260917.md) and the logical-root description inside the ordered registry entry, both verbatim from the order. The local scratch paths appear only in this report's private-safe evidence fields. Zero Qwen/model calls; zero parser executions; the only network use was read-only GitHub API (gh) and the normal publication pushes.",
  "limits": "Bounded documentation/state round: no new experiment, no tuning, no application source change, no test change, no fixture/config/expectation change, no data acquisition, no objective-009 data touched, no 007-m linguistic system change, no merge or auto-merge, no release or deployment, no CRITICAL append (register remains the empty seed; Decision: NONE), no ICA launch. The machine-block update records the accepted post-merge identity only; the 007-o review point remains fully recorded. The ledger registration completes the canonical experiment ledger for objective 008 (25 entries). GO from 008-a is structural qualification only and gains nothing new here: no linguistic acceptance, no product milestone, no release authority.",
  "human_gates": "D0 per the order. The 008-a-reported dilemma candidate (order requirement 9 versus the merged 007-o snapshot test) was investigated by strategy and classified D0 with the exact green path verified from the test source: single viable non-weakening remedy; corrective suffix; all numeric re-derivation assertions and all test logic unchanged. Deferred human adjudication: Decision: NONE. The CRITICAL register remains the empty seed with zero open gates; no CRITICAL append occurred or was ordered. No new D1 or D2 candidate arose from this round.",
  "scope": "Finished only the exact activated 008-b: reconciliation, the exact order-plus-active commit, the research-state update (five machine-block fields, section 16, single 4.2 heading line, registry entry plus scope string, deterministic CSV regeneration), the full local verification set at the implementation head, the push, the implementation-head CI observation (red solely on the expected pre-report count assertion), this report-only publication, and remote verification. No other scope touched: no 008-c, no 009 work, no next suffix self-assigned, no merge, no release, no deployment. After publication, per P-SELF-03, no later mutation or push for this round; response OK and exit.",
  "result_summary": "COMPLETE. This round restored the post-merge research-state identities by the only viable non-weakening means (additive post-merge identity update as a corrective suffix) and registered the 008-a GO study in the canonical experiment ledger (25 entries, evidence SHAs/sizes re-verified against base-head bytes). All scoped edits are byte-verified; the frozen 007-o test logic and every numeric re-derivation assertion remain byte-unchanged and fully binding. Per-head CI truth: at the implementation head (8300573) Research reproducibility and Application baseline are red solely on the expected pre-report count assertion (45 report files - 1 = 44 != 45) with no other failing test, while OAP bootstrap acceptance and OAP report history are green; at the final head (this report commit) both formerly stale assertions are mechanically satisfied (scratch demonstration: consistency module 10/10 green with the report file present), so all four required checks are expected green - the final-head CI run itself is PENDING and not observable inside this pre-push report (publication_verified=false), and its actual post-publication state is recorded in the bounded private receipt and strategic review per P-SELF-03. This round changes no scientific result; the 008-a GO evidence is now in the ledger; PR #9 remains OPEN and UNMERGED for 008-c."
}
```


## Result

Round 008-b is **COMPLETE**: the post-merge research-state identities are
restored by the only viable non-weakening means (additive identity update as
a corrective suffix) and the 008-a GO study is registered in the canonical
experiment ledger (25 entries). The frozen 007-o snapshot test's logic and
every numeric re-derivation assertion are byte-unchanged and remain fully
binding; the round changes no scientific result.

Per-head CI truth, recorded as observed: at the implementation head
(`8300573`) Research reproducibility and Application baseline are red
**solely** on the expected pre-report count assertion (45 report files - 1 =
44 != the block's 45; no other failing test in either job), and OAP
bootstrap acceptance and OAP report history are green. At the final head
(this report commit) both formerly stale assertions are mechanically
satisfied - demonstrated in a disposable scratch clone, where the presence
of the 008-b report file turns the frozen consistency module 10/10 green -
so all four required checks are expected green there. The final-head CI run
itself was PENDING and not observable inside this pre-push report
(`publication_verified=false`); its actual state belongs to the bounded
private receipt and strategic review per P-SELF-03, and the strategy
final-head review records it.

The 008-a-reported dilemma candidate is the D0 classification this order
executes: single viable non-weakening remedy; corrective suffix; all numeric
assertions and test logic unchanged. PR #9 remains OPEN and UNMERGED for
008-c; objective 009 remains reserved; no acceptance, milestone, merge,
release, or deployment claim is made.

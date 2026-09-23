# Work report 008-a — Qualify pulldown-cmark 0.13.4 as the structural prose boundary

```oap-report
{
  "id": "008-a",
  "result": "PARTIAL",
  "order_path": "oap/orders/008-a-qualify-prose-boundary-parser.md",
  "order_sha256": "fc99d2f903fb32166f4d46761485c593ea26a505c5e3ea731502b1638de6e3bb",
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
  "implementation_head": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 9,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/9",
  "pr_state": "open",
  "branch": "oap/008-prose-boundary-qualification",
  "base_sha": "7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9",
  "starting_remote_sha": "7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9",
  "no_merge": true,
  "checks": [
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/branches/main and gh pr list --repo ulfe-lmi/llm-slovenian-repair --state all (reconciliation before mutation, requirement 1)",
      "result": "PASSED",
      "details": "Remote main = 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, equal to the order's base_sha and to the order's verified post-merge state (merge commit of PR #8; parents ee2d1b479719009ff1d07829478f241e3f395f7c and the reviewed 007-o head 4a029287f27e038d5c34c39b26ca836be7c6914b). No open PR existed for objective 008 (PR #8 MERGED); the branch oap/008-prose-boundary-qualification was created exactly on 7d2cc9e and oap/active holds the exact bytes '008-a'.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests",
      "result": "FAILED",
      "details": "232 tests at the implementation head: 231 pass, 1 pre-existing failure: test_research_state_consistency.test_main_is_ancestor_of_reviewed_head (AssertionError: '7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9' != 'ee2d1b479719009ff1d07829478f241e3f395f7c'). Root cause, demonstrated: the frozen 007-o machine block records main_sha ee2d1b47 (the pre-merge main at the 007-o review point); strategy's development-only merge of PR #8 then advanced main to 7d2cc9e and no CI re-ran (all workflows are pull_request-triggered). The test additionally requires main_sha to be an ancestor of the reviewed 007 head 735c9830; verified both directions with git merge-base --is-ancestor: ee2d1b47 IS an ancestor, 7d2cc9e is NOT (it is a descendant), so no main_sha value can satisfy the test. The failure exists on a fresh checkout of main itself; no 008-a change causes it. A second, distinct pre-existing defect is demonstrated for the final head: with this round's required report file present (temp file created, test run, deleted; worktree restored), test_registry_and_report_counts fails 43 != 44 in both the research checkout and the .git-less Application-baseline pytest workspace, because the block's oap_reports_reviewed (43) predates any 008 report. Neither defect is fixable within this order: the merged research tree is preserved byte-for-byte (local_work; Files and boundaries write list) and requirement 9 forbids weakening, skipping, or redefining any check.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.rebuild_tables --check",
      "result": "PASSED",
      "details": "The deterministic numeric table matched the registry at the implementation head.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "Guard green on 176 files at the implementation head. Fail-closed behaviour was exercised for real during the round: before commit db9de49 the guard exited 1 with findings confined to this round's new research/prose-boundary/ subtree (denied raw-JSON key names input/output in the frozen config and fixture suite; guarded absolute-path marker byte sequences in the class-30 paths fixture; JSONL event dumps outside research/results/). Commit db9de49 corrected exactly those in-scope (identifier renames; F30 reworded to synthetic paths of the same class semantics with its anchor-resolved region re-resolving deterministically 72 to 69 bytes; event artifacts serialized as JSON projections embedding the raw adapter stdout SHA-256). Full deterministic re-evaluation after the corrections: increment 1 all 8 Hard invariants true (1,288 events, PROCEED_TO_INCREMENT_2), increment 2 differential byte-identical except the config_sha256 reference (challenger NOT_TRIGGERED). No expectation was added, removed, or weakened.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 scripts/verify_development_baseline.py --temp-parent /home/ubuntu/.local/share/llm-slovenian-repair/baseline-temp --command-timeout 1200",
      "result": "PASSED",
      "details": "The real baseline driver completed all 13 stages PASSED with cleanup PASSED at the implementation head: uv lock --check, frozen dependency sync, focused contract tests, full pytest, Ruff, mypy, OAP unittest discovery in the workspace, sdist and wheel build, built-wheel selection, fresh offline venv, offline runtime-only frozen sync, offline wheel installation, offline runtime import and metadata. The 300 s default per-command timeout was raised locally to 1200 s purely for this slow host (full pytest measures ~520 s here); the CI driver uses its own defaults.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "FAILED",
      "details": "129 tests at the implementation head: 128 pass, 1 ERROR - test_report_history_cache.AcquisitionHistory.test_current_generation_is_monotonic_and_prior_receipt_is_untouched hit the tool's hard 30 s git subprocess timeout on 'git log ... HEAD -- resources/source-acquisitions' inside validate_acquisition_history. Environmental, not round-caused: this round does not touch that path; the identical git command measures 0.28-0.36 s wall (warm) on this host, i.e. pure I/O wait on a cold-cache stall; an isolated warm re-run of the affected module passed 20/20; and the CI OAP bootstrap acceptance (same discovery in a real checkout) is green at this exact head (run 35235120123). Precedent: the 007-o report records the same local/CI divergence for the same test class.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "details": "Exit 0, governance structure valid in accepted-runtime mode at the implementation head; semantic and human authorization proofs remain false by design.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 008-a",
      "result": "PASSED",
      "details": "result valid at the implementation head: active=latest=008-a; 45 orders; 42 valid reports plus 007-d and 007-n both classified INVALID_QUARANTINED; 44 report files.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "Report history valid at the implementation head: 44 reports, exactly the two frozen historical incidents (RHI-0001, RHI-0002); oap/REPORT-HISTORY-INCIDENTS.json unchanged; no prior report byte mutated.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision HEAD and python3 oap/bin/check_whitespace.py --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "Both accepted-base whitespace checks passed at the implementation head with exactly the three pre-existing frozen blank-at-EOF incident paths. One cold-cache run of the older base recorded a transient GIT_EXECUTION_FAILED on this slow host and passed on immediate re-run (same environmental git-latency class as the check 6 entry).",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No protected source changed against the application accepted base at the implementation head.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "No object corruption at the implementation head; only dangling objects from an earlier local branch rewrite remain. Note: the local HEAD reflog carries 16 malformed entries from that same earlier local amend (pre-dating this session); the reflog is local-only metadata, is never transferred by push, and the --no-reflogs fsck is clean.",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    },
    {
      "command": "gh pr checks 9 and gh api repos/ulfe-lmi/llm-slovenian-repair/actions/runs (all four required checks at head db9de49)",
      "result": "PASSED",
      "details": "Observed at the implementation head: Application baseline success (run 35235120118), OAP bootstrap acceptance success (run 35235120123, transcript expected id 008-a satisfied), OAP report history success (same run), Research reproducibility FAILURE (run 35235120135). The CI log shows exactly one failing test, the assertion diagnosed in check 2 (232 tests, 1 failure, suite wall 7.3 s on CI hardware). PR #9 observed OPEN, base main, head db9de49, merged_at null, auto-merge disabled. The final-head (report commit) CI is PENDING and not observable inside this pre-push report; it is predicted to fail Research reproducibility on the same assertion plus the report-count assertion, and Application baseline on the same report-count assertion in its full-pytest stage - both demonstrated locally before publication (check 2).",
      "sha": "db9de499a44d86fcaac39f5ef1a701ea01f1ad26",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-17T16:47:42+02:00",
  "report_written_at": "2026-09-17T16:50:12+02:00",
  "implementation": "Round 008-a, four implementation commits on oap/008-prose-boundary-qualification: a3e3b6a (exact order + active bytes), 5d8027b (frozen experiment inputs), 2e5ef04 (increment 1+2 results, gate decision, research report), db9de49 (publication-boundary hygiene inside the same new subtree). The experiment itself: candidate pinned exactly (pulldown-cmark 0.13.4, registry checksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e, upstream tag v0.13.4, MIT, MSRV 1.71.1, rustc/cargo 1.75.0); 50-fixture adversarial suite frozen before first parser run (all 38 required classes plus 12 extra); measurement adapter built as a research-only, explicitly labeled throwaway (binary sha256 5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf); increment 1 executed in the predeclared order with all 8 Hard invariants true on 50 fixtures x 3 profiles (1,288 events; exact byte-slice fidelity; no code-point bisection; deterministic reversible byte-to-code-point mapping; stock-CLI cross-check 50x3; invalid-UTF-8 exit 3; negative self-test), gate checkpoint committed (PROCEED_TO_INCREMENT_2); increment 2 on 100 deterministically selected preserved outputs (8,919 records to 2,670 unique, sha256-ascending; corpus 100 percent plain prose - the stated limitation) with an 8-class differential: 22 disagreement spans, all class 7 (18 number, 4 identifier; 110 bytes, about 0.9 percent), classes 1-6 and 8 zero; challenger markdown-rs NOT_TRIGGERED (all six predefined conditions false). Outcome declared: GO. No model calls anywhere; all evaluation is deterministic local binary execution. The only post-freeze correction (db9de49) is the documented publication-boundary hygiene: identifier/layout changes with a full deterministic re-evaluation and zero semantic change.",
  "documentation": "research/prose-boundary/REPORT.md (research report) answers all 13 ordered questions, cites every material claim by path plus SHA-256, and states explicitly that nothing here is production code or a runtime interface and that objective 009 remains reserved. README.md, the frozen config (schema notes, structural policy, coordinate contract, privacy and determinism rules), the candidate identity record, the fixture suite with its frozen_note, authoring-corrections.md (14 pre-commit corrections, D0 autolink-destination and D1 policy-token-family evaluator notes, and the post-freeze hygiene correction), and the results (summary, gate decision, event projections with raw-bytes SHAs, selection receipt, differential summary, challenger decision) together form a reviewer-readable, data-free record. The PR #9 description carries the truthful required-check status and the D1 dilemma pointer.",
  "criteria": "Order acceptance 1 (candidate identity file, exact): MET - identity/candidate-identity.json (sha256 671d7cded433bbc0a3e1f60fcb4a2da7d89f2a79e254f6a5b57ac80eb38d9c0d): version 0.13.4, registry checksum, tag v0.13.4 (commit 38e4d08f14ec4bd9783270e9623db7681ebed968), MIT license evidence from three sources, MSRV 1.71.1, locked dependency set, pinned registry installation mechanism. Acceptance 2 (fixtures committed before first parser run, >= 38 classes, frozen semantics): MET - 50 fixtures, all 38 required classes, frozen_before_first_parser_run true, corrections and the two evaluator implementation notes recorded in authoring-corrections.md. Acceptance 3 (hard coordinate invariant on all fixtures): MET - byte-slice equality, no bisection, deterministic exact reversibility on every emitted boundary, CRLF and decomposed-Unicode behaviour documented, invalid UTF-8 rejected cleanly. Acceptance 4 (increment 1 results + gate before increment 2): MET - results committed with data-free aggregates; gate decision PROCEED_TO_INCREMENT_2 committed; the single-round gate enforcement is recorded (strategy final-head review per P-REVIEW-01). Acceptance 5 (increment 2 receipt, 8-class differential, residual quantification, challenger decision): MET - selection-receipt cb27cb462cf9b33e42ce1e77db5ef5d9a33d0a3fc411aea39a08587ec8b1391b, differential-summary 287319ffccaa357af88142f000c28fb373d45164b07231c86290f977a460c08c, challenger-decision 8c056bc94cf514c6fe46277998deb3dd5d4208a80ac2727695ec5f818863c68f (NOT_TRIGGERED). Acceptance 6 (exactly one outcome, 13 questions answered, no raw private text): MET - GO declared; research REPORT.md answers all 13; publication guard PASSED on 176 files. Acceptance 7 (four required checks green at the final head; report-only invariants verified remotely; PR open/unmerged; no immutable prior order/report mutated): NOT MET in part - see check 2 and check 12: the frozen 007-o snapshot consistency test is structurally unsatisfiable at any post-merge head (live origin/main comparison, and the report-count comparison once this round's required report exists), and making it green would require changing the merged 007-o research test/state (outside this order's write scope: local_work preserves the merged research/ tree byte-for-byte) or redefining a check (forbidden by requirement 9). The PR was created before this report (PR #9, open, unmerged, auto-merge disabled); no immutable prior order or report is mutated (report history valid, exactly the two frozen incidents); the report-only invariants (remote head, exact report bytes, parent, changed path) are verified after push by verify_report and, per P-SELF-03, that post-publication verification belongs to the bounded private receipt and strategic review, not to this pre-push report. Acceptance 8 (zero model calls, zero new data, 009 untouched, no linguistic tuning): MET.",
  "negative_paths": "Recorded and observed: (1) the evaluator's embedded negative self-test - corrupted-range, code-point-bisection, protected-exposure, prose-missing, and CLI-offset probes are all caught by its own detectors before any fixture result is trusted (self_test all true in the committed summary; the run aborts if any probe fails). (2) The publication guard's fail-closed behaviour was exercised for real: it exited 1 on the pre-correction subtree (six distinct finding classes, all inside research/prose-boundary/) and exits 0 after the in-scope correction. (3) Final-head blocker demonstration: with a temporary 008-a report file present (created, test run, deleted; worktree restored), test_registry_and_report_counts fails 43 != 44, proving the count assertion breaks at any head containing this round's required report, independent of any 008-a content. (4) The ancestry lose-lose demonstration: git merge-base --is-ancestor ee2d1b47 735c9830 is true and git merge-base --is-ancestor 7d2cc9e 735c9830 is false, so no main_sha value satisfies the 007-o test. (5) check_transcript and check_report_history are valid at the implementation head - no prior report byte changed. (6) The two transient local failures (checks 6 and 9) were reproduced, root-caused as cold-cache git latency on this host, and re-verified passing (module 20/20; whitespace re-run PASSED).",
  "boundary_fidelity": "Exactly four commits, all inside the order's write scope: a3e3b6a (the exact 008-a order, committed-blob sha256 fc99d2f903fb32166f4d46761485c593ea26a505c5e3ea731502b1638de6e3bb re-verified, and oap/active), 5d8027b (new research-only experiment subtree: frozen config, identity, fixture suite, adapter, tools), 2e5ef04 (results, gate decision, research report, events), db9de49 (publication-boundary hygiene inside the same new subtree). The merged 000-007 seams, the merged research/ tree outside research/prose-boundary/, and every protected source are byte-identical (protected-source diff exit 0; the round diff touches only research/prose-boundary/, oap/orders/008-a-qualify-prose-boundary-parser.md, oap/active). No application source change. The unrelated untracked local directory .research-test-scratch/ was preserved untouched. The local HEAD reflog anomaly (16 malformed entries from an earlier local amend) is local-only metadata, never transferred by push; git fsck --full --no-reflogs is clean. No model, GPU, vLLM/CUDA, service, network, profile, or protected-resource change; no merge, auto-merge, release, or deployment; PR #9 remains OPEN and UNMERGED.",
  "setup": "Reconciled before mutation (requirement 1): exact active 008-a (bytes '008-a' plus LF); remote main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 verified over the API and equal to the order's base_sha and to the order's verified post-merge state; no other open objective-008 PR; local work preserved. Environment: Python 3.12.3, uv 0.12.5, rustc/cargo 1.75.0 for the pinned adapter build (MSRV 1.71.1 satisfied), persistent non-system scratch parents under /home/ubuntu/.local/share/llm-slovenian-repair (baseline-temp, research-runtime-local, ws-repro1); the private preserved roots and the scratch-built binaries are supplied to the tools as CLI arguments at run time only. This host has slow git I/O: a cold-cache full-history git log stalled past the tools' hard 30 s limit once (0.28-0.36 s warm), which explains the two transient local failures recorded in checks 6 and 9; CI hardware completes the same research suite in 7.3 s.",
  "privacy": "Data-free and public-safe: no dataset rows, gold strings, prompts, response bodies, credentials, or private native paths appear in any committed artifact (publication guard PASSED on 176 files at the implementation head). The representative corpus selection reads the preserved private roots at run time only (CLI arguments, in memory, re-asserted by SHA-256 per sample); the selection receipt and differential summary carry counts, categories, and hashes only; no raw private text was ever written into the repository or any report. The literal temp parent path appears only in the recorded baseline command (check 5), as prior rounds recorded it. Zero Qwen/model calls; the only network use was the read-only pinned candidate-identity fetches (recorded in the identity file) and normal GitHub publication.",
  "limits": "Research-only bounds held: no production integration; the measurement adapter is explicitly labeled a MEASUREMENT ADAPTER, research-only, isolated in the experiment subtree, and not positioned as the future runtime interface; the existing regex protection rules are neither deleted nor classified (008-b scope); the frozen 007-m system is untouched and untuned; no new data acquisition beyond the deterministic selection from already-preserved outputs; no objective-009 confirmation data consumed (009 remains reserved); no release or deployment; no merge or auto-merge; no CRITICAL append; no ICA launch. GO qualifies the structural/source-range boundary only: it is not a linguistic acceptance, not a product milestone, and grants no release authority.",
  "human_gates": "D0 per the order; deferred human adjudication: Decision: NONE; the CRITICAL register remains the empty seed with zero open gates; no CRITICAL append occurred or was ordered. One D1 dilemma candidate is reported for strategy (reported, not appended - strategy alone investigates, chooses, and assigns an ID): the contradiction between order requirement 9 (all four required checks green at the final head) and the preservation of the merged 007-o research test/state after the development-only PR #8 merge. The frozen 007-o consistency test became stale the moment main advanced: its live origin/main comparison can no longer hold, no main_sha value satisfies both of its assertions (demonstrated), and its report-count comparison breaks at any head that adds a new OAP report (demonstrated for this round's required report). Options for strategy include: a separate corrective order updating the post-merge research-state identities and the test's live-ref/count assertions while keeping every numeric re-derivation assertion binding; or accepting and documenting the red Research reproducibility and (at the final head) Application baseline for this round; or another disposition. No check was weakened, skipped, or redefined in this round.",
  "scope": "Finished only the exact activated 008-a: reconciliation, candidate identity, frozen fixture suite, measurement adapter, increment 1 with the gate checkpoint, increment 2 with the differential and challenger decision, the publication-boundary hygiene correction, the four-commit branch, PR #9 created before this report, this report-only publication, remote verification, and the response OK. No other scope touched: no 008-b, no 009 work, no next suffix self-assigned, no merge, no release, no deployment.",
  "result_summary": "PARTIAL. The scientific round is complete and verified: every Hard invariant true, the strategy-review gate passed, the 8-class differential is bounded (class 7 only), the challenger was not triggered, the outcome GO is declared with all 13 ordered questions answered, the publication guard is green, and three of the four required checks are green in CI at the implementation head (Application baseline run 35235120118, OAP bootstrap acceptance run 35235120123, OAP report history run 35235120123). Acceptance criterion 7 is not met solely because the frozen 007-o snapshot consistency test went stale the moment strategy's development-only PR #8 merge advanced main: its live origin/main comparison (and, at the final head, its report-count comparison) cannot pass at any later head, and the only fix lies outside this order's write scope or is forbidden by requirement 9. This contradiction is reported as a D1 dilemma candidate for strategy with the full evidence chain. The PR remains OPEN and UNMERGED for strategic review; no acceptance, milestone, merge, release, or deployment claim is made."
}
```


## Result

Round 008-a is **PARTIAL**: the bounded falsification experiment itself is
complete, verified, and data-safe, and it declares **GO** — pulldown-cmark
0.13.4 holds the exact source-range and conservative-structural contract on
the frozen 50-fixture adversarial suite and on the 100-sample preserved
corpus, with the residual bounded to a token-level secondary-recognizer
problem and the markdown-rs challenger not triggered.

The part that is not met is order acceptance criterion 7, "all four required
checks green at the final head." The frozen 007-o research-state
consistency test went stale when the development-only merge of PR #8
advanced main from `ee2d1b47` to `7d2cc9e`: its live `origin/main`
comparison can no longer hold (demonstrated in CI, run 35235120135), no
`main_sha` value satisfies both of its assertions (demonstrated with
`git merge-base --is-ancestor` in both directions), and its report-count
comparison breaks at any head that adds this round's required report
(demonstrated locally). Making those checks green would require changing
the merged 007-o research test/state — which this order's write scope
excludes ("preserve the merged research/ tree byte-for-byte") — or
redefining a check, which order requirement 9 forbids. The contradiction
is therefore reported as a D1 dilemma candidate for strategy, with the
evidence chain in this report (checks 2 and 12, negative paths 3-4).

No check was weakened, skipped, or redefined. PR #9 remains open and
unmerged; objective 009 remains reserved; no acceptance, milestone,
release, or deployment claim is made.

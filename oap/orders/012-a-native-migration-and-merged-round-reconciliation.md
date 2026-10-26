# 012-a — Native-host migration and merged-round reconciliation

Status: FINAL; prepared for reviewed recovery publication. A prepared file in the private workorders directory is not active.

## Identity

One recovery objective, one new branch `oap/012-migration-reconciliation`, one new PR against main. No development beyond this bounded migration/reconciliation order. The old private 012-a/012-b evaluation drafts are superseded as continuation instructions; preserve their bytes as historical drafts. The evaluation objective will be re-planned after recovery.

## Provenance

The current owner instruction authorizes completion of migration and reconciliation. The owner also explicitly restricts coding to the already running foreground pane; no subagents, background codex exec, alternate providers, launcher-created coding processes, or process resurrection. The historical 011-e report and GitHub commit identities are evidence, not an acceptance claim. The exact recovery tuple is in metadata below.

## Current verified state

Remote main is ff08d6e34601f56fecf21eff7d3d3b0e7c68dede. PR12 is merged with frozen head 0c6a5a6c4bf96d9a5a89503c316f64445bac81aa. The retained branch ends at 8e5811ab595737a5ea9ee24e993867fc99219503, whose sole parent is 8cdbab0bc2e144b97d78af5245e829d80d2fd984 and whose only changed path is the 011-e report. Seven tail files differ from main, including the finalized collection manifest. Normal remote verification fails REMOTE_HEAD_MISMATCH. PR13 is an open 21-file revert with red Research reproducibility; leave it untouched unless strategy separately conveys the owner's disposition. The prior report contains 12 PASSED, 2 FAILED and 1 PENDING checks. Its private primary collection/packet/identity files are not present at the inspected migrated locations. There is no authorized scientific replay in this round.

## Governance

Trusted accepted governance ref: 4507cc78e333c0e48226b64266121171b7b8cea8. Metadata carries the exact old identity map generated directly from that commit. PLAN, full product architecture, immutable docs/bootstrap sources, source lock, CRITICAL, historical orders/reports and scientific method artifacts remain byte-identical.

Bounded current-governance evolution is authorized for these exact paths, and only for native-host placement, foreground execution, and merged-tail publication/recovery semantics:
- oap/governance/WORKSPACE-LAYOUT.json
- oap/strategic-instructions/AGENTS.md
- oap/strategic-instructions/OAP-COMMUNICATION-strategic.md
- oap/strategic-instructions/strategic_model_init_material.md
- oap/coding-instructions/AGENTS.md
- OAP-COMMUNICATION-coding-agent.md
- oap/prompts/coding-round.md
- oap/prompts/strategic-start.md
- SECURITY.md
- oap/governance/DISTILLATION-MAP.md
- oap/governance/MANIFEST.json
Record the accepted old hashes, changed clauses, rationale, D0 classification and tests in a versioned migration revision record. Update every affected projection/manifest together. Keep private strategic law at accepted-old until strategy reviews/merges and deliberately refreshes it. Current explicit owner foreground instructions govern immediately. No current-source hash can authorize its own acceptance.

## Goal and dependencies

Restore a usable, testable development control loop on the current host while preserving the entire prior research and report history. This round is successful when ordinary diagnostics can truthfully distinguish published-but-unintegrated merged-tail evidence, foreground-only dispatch is enforceable, all four required final-head checks pass, and a continuation inventory accurately names available and missing data. No MVP or deployment label is conferred.

## Scope

Allowed implementation: oap/bin/{oap_core.py,oap_cli.py,oap_runtime.py,oap_install.py} and bounded new OAP helper modules if needed; oap/tests/; relevant research tests of OAP integration only; .github/workflows/application-baseline.yml and oap workflow only for the narrowly ordered governance guard; current governance paths above; docs/OAP-RUNBOOK.md, docs/CODEX-ROLE-SETUP.md, docs/DEVELOPMENT.md, docs/IMPLEMENTATION-ROADMAP.md, docs/READINESS.md; README.md and STATUS.md for accurate navigation/status; research/RESEARCH-STATE.md for an additive recovery note and exact identity/counter advance; research/registry/experiments.json and regenerated research/tables/experiment-summary.csv for one non-scientific recovery entry if required by the established ledger; oap/GENERATED-FILES.json for affected generated pins; a data-free migration/recovery evidence record under oap/recovery/; this order, active pointer and the final 012-a report. Do not edit unrelated code, tests or workflows.

## Non-goals

No corpus acquisition, model call, annotation, evaluation rerun, parameter/prompt/scoring change, production service, network/gateway change, credential copying or disclosure. No change to PR13. No deletion or replacement of prior branches, private datasets, untracked residues or preserved archives. No claim that unavailable private files were restored or that old tests were rerun successfully. No force push, reset, clean, stash, history rewrite, merge, auto-merge, or additional agent.

## Files and boundaries

Use the compact coding read set and this exact order. Inspect oap_core transition/verify_report/report-history/governance, oap_runtime role_context/launch/tmux_plan, oap_install runtime_config, current workflow protected-source guards, research-state identity tests and corresponding runbook sections. Read only S-PLACEMENT-01, S-PROTOCOL-01, S-RECOVER-01, S-EVOLVE-01 of full strategic law and communication sections 3, 6, 7, 9, 11 as needed for the ordered projections. Do not load the strategic history or raw private research text. Strategy owns private runtime updates and the initial recovery publication.

## Requirements

1. Preserve original commits. Create the 012 branch from the exact retained 011-e report commit, then merge the verified remote main using a normal merge, preserving both as ancestors. Do not cherry-pick/copy the historical report into a new commit. Keep activation changes separate and confirm no unrelated staged paths. The final PR must contain the complete seven-file scientific/bookkeeping tail as inherited evidence; do not modify its frozen manifest. Never replay collection work.
2. Fix merged-PR report reconciliation with explicit, pinned evidence. Keep normal open-PR exact-head equality. A merged PR with a later report on its original retained branch may be recognized only after proving original same-repository PR identity, original branch/ref, real merged state and merge ancestry on current default, frozen PR head ancestor of report, current retained branch head equal to the specified report commit, exact report parent/only-path/content, exact original order, and check-SHA ancestry. Classify this as post-merge branch publication, not integrated or accepted work. A new-objective transition must require an explicit metadata receipt binding the full recovery tuple and require preservation by ancestry. No synthetic PR response, forged head, unconditional bypass or local-only success. Refresh/review commands must retain truthful distinction after integration. Normal report-history strictness remains.
3. Support the selected current native layout. The actual repository and strategic roots are supplied by strategy through private runtime configuration. The two real FIFOs reside under the user's native home in .oap-fifos/llm-slovenian-repair; none live in the workspace. Native private directories/files use 0700/0600; reject symlinks, wrong owners/types and overlaps. Preserve support for the historical exact sync exception without applying it to native roots. The dedicated WORKSPACE-LAYOUT record is the only versioned place authorized to contain the selected machine roots. Elsewhere use logical names or environment variables.
4. Enforce foreground-only coding for this owner-selected runtime. Adopt the already running pane; inspect its PID/cwd/argv and explicitly convey OAP_ROLE=coding in the handoff and helper command environment. Do not restart it to change process environment. Its launch is exactly codex --yolo --profile early-beta in the coding directory if it later dies. Existing owner-launched session homes remain as launched; preserve historical private role homes and do not copy authentication. Implement an explicit foreground mode that prevents legacy launch/tmux helpers from spawning a coding model (including codex exec), auto-restarting one, or creating background panes. A diagnostic/preflight and exact FIFO receipt may run outside the model. Consume control once outside coding, verify durable order state, then strategy may paste the handoff into the named existing pane. Duplicate completed signals cannot dispatch implementation. Missing/dead/wrong-cwd/wrong-argv panes fail closed. Existing generic fake-runtime tests may retain their isolated legacy fixtures; selected real runtime must not silently fall back to legacy mode.
5. Advance only the machine-block main_sha/reviewed_branch_head_sha to ff08d6e34601f56fecf21eff7d3d3b0e7c68dede and reviewed_branch_head_parent_sha to 0c6a5a6c4bf96d9a5a89503c316f64445bac81aa. Retain branch=oap/007-concept-verification and pr_number=8: they deliberately identify the historical 007-o evidence. Preserve all frozen scientific values and quarantine records. Re-derive registry/report counters, disclose the expected implementation-head report-count mismatch if used, and make them exact at the final report head. Add a short section correcting the obsolete handoff claims without rewriting historical reports. Preparation and test activity is not scientific progress.
6. Keep meaningful CI protection. Current workflow's blanket historical protected-source diff cannot admit authorized current governance evolution. Replace only that boundary with shared candidate-review against the literal trusted accepted ref and the exact ordered source-path set; bind the authorization to this immutable order/revision. Preserve PLAN, architecture, CRITICAL, source-lock and docs/bootstrap protection, and reject unlisted governance changes, drift or candidate self-authorization. Do not disable/skip checks or relabel red as success. Add negative tests at actual CLI boundaries.
7. Use the newly rebuilt machine-local Python 3.12 environment and committed uv.lock. Setup is reversible and scoped; no changes to the shared Python/CUDA/model environment. Resolve native-host assumptions in the authorized OAP/setup boundaries only. Inventory required research inputs by existence/hash without opening or printing raw texts or credentials. Strategy owns locating/restoring missing private data; product development may continue independently of that prerequisite, and evaluation remains explicitly blocked until its inputs are verified.
8. Document the exact current continuation command, foreground/FIFO workflow, original 011-e evidence identities, old merge/publication exception, data availability, next engineering scopes and the provisional 8–15 focused-day MVP estimate. Distinguish research evaluation completion, packaged MVP, ICA and deployment. No activation or deployment side effect on merge; all workflows inspected are PR tests only.

## Acceptance criteria

A1. Original 011-e report commit and owner merge are ancestors of the 012 final head; every original report/order byte and protected scientific surface is unchanged. Local and remote report integrity checks succeed without falsifying PR12's head.
A2. Actual verify-report, state, new-objective transition and refresh/review paths recognize only the explicit merged-tail case and report its evidence scope accurately. Negatives reject unrelated PR/branch/fork, stale branch tip, wrong merge/main ancestry, modified report/order, wrong parent/path, missing receipt and replay.
A3. Current native layout passes ownership/type/mode/symlink guards and doctor, with exact real FIFO paths; historical sync exception remains narrowly scoped.
A4. The selected foreground-mode launch/dispatch entry point starts zero models, rejects legacy background launch and wrong/dead panes, consumes one exact OK frame and suppresses completed replays. Test fakes sit outside the named process/FIFO boundary.
A5. Research-state identities/counters re-derive at final head; immutable scientific method, data-free manifest and historical reports retain their hashes. No model/scientific/deployment calls occurred.
A6. Focused and broader tests plus all four final-head required checks are green. Report only observed tested-SHA results; absent primary data and future publication checks remain explicitly unproven/pending.

## Verification

Run Python 3.12 focused OAP tests for merged-tail reconciliation, native layout and foreground dispatch through actual CLI entry points; include positive and negative cases in A2–A4. Run `python3.12 -B -m unittest discover -s oap/tests -v`; `python3.12 -B -m unittest research.tests.test_research_state_consistency -v`; `python3.12 -B -m unittest discover -s research/tests -v` with owned native TMPDIR and CI-parity umask; `python3.12 -B -m research.tools.rebuild_tables --check`; `python3.12 -B -m research.tools.publication_guard --root research`; shared report-history/transcript and governance candidate-review with the exact allowed path list; and the native development baseline driver `python3.12 scripts/verify_development_baseline.py --temp-parent <owned persistent scratch> --command-timeout 600`. Use bounded outputs and record actual limitations. At final head run the report/count-sensitive checks again as necessary. Required GitHub jobs: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history. Missing/pending/cancelled checks never count as passed.

## Local setup and constraints

Only the existing foreground coding agent may implement. No subagents, background coding processes, separate inference workers, alternate model/provider, or unrelated session changes. This migration round makes zero research model calls. The normal research live-test opt-in remains NO. Existing private receipts may contain credentials: inspect metadata only, never print/copy them to artifacts. Preserve untracked work. Use private persistent native scratch under the strategic workspace, not shared scratch names. User instruction supersedes the historical wrapper-launch profile.

## Documentation

Update the named runbooks/status/revision record to observed behavior. Preserve earlier drafts and reports; mark historical advice superseded in a new record. Missing private data is a named evaluation prerequisite, not fabricated proof or a requirement for unrelated software work. Source licenses and human deployment gates remain separate.

## Git and report publication

CREATE_NEW_PR, same branch for all corrections. First open the PR, report its real number, and keep it open. Push implementation and ordered activation before writing the report. Final commit contains only `oap/reports/012-a-native-migration-and-merged-round-reconciliation.md`, has the literal implementation head as sole parent, and uses SELF. No future CI/push success claim inside that report. After push, verify the remote current PR/report bytes and parent/path, then send exactly ASCII OK (two bytes, no LF) to the configured response FIFO and stop at the foreground prompt. Do not run the obsolete launcher or exit/restart Codex automatically. Coding never merges or enables auto-merge. Strategy independently reviews the final diff, evidence, final-head CI, rollback and governance before any development merge/refresh.

## Decision classification

D0: bounded reversible host/protocol reconciliation preserving the existing authority boundary, exact immutable history and explicit owner foreground constraint. Missing data and a mechanical PR-head bug are engineering prerequisites; no new consequential product/security discretion is introduced. Production/deployment remains outside this order.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "012-a",
  "title": "Reconcile migrated native runtime and preserve the published post-merge 011-e tail",
  "objective": "012",
  "status": "FINAL",
  "phase": "DEVELOPMENT_RECOVERY",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ff08d6e34601f56fecf21eff7d3d3b0e7c68dede",
  "governance_ref": "4507cc78e333c0e48226b64266121171b7b8cea8",
  "branch": "oap/012-migration-reconciliation",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "011"
  ],
  "local_work": "Preserve original 011 branch at 8e5811ab595737a5ea9ee24e993867fc99219503 and all immutable orders/reports. Preserve pre-existing untracked corpus/, .research-test-scratch/, .rclone-speed-test/. Preserve private research and configuration backups. Current tracked tree is clean before strategic publication.",
  "prior_review": "Private migration-20261025/011e-reconciliation.json: original report validates locally and remote commit/order/report bytes, sole parent/path, retained branch identity and ancestry were checked independently. Standard remote report gate fails REMOTE_HEAD_MISMATCH because PR12 was merged mid-round. Report result remains PARTIAL; scientific primary-data replay is UNPROVEN. No replay of 011-e.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner strategic thread 2026-10-25: finish migration/reconciliation, prepare continuation, first estimate MVP; only existing foreground coding pane and codex --yolo --profile early-beta restart if it dies; no background coding agents."
    },
    {
      "kind": "A",
      "reference": "S-STATE-01, S-RECOVER-01, S-EVOLVE-01, S-PROTOCOL-01; native-home real FIFO placement and independent final-head development review."
    },
    {
      "kind": "E",
      "reference": "Observed 2026-10-25: obsolete /home/ubuntu runtime paths; absent migrated FIFOs; verify_report(011-e, remote) REMOTE_HEAD_MISMATCH; native ext4 workspace; missing 011 private data at inspected locations; current remote main ff08d6e34601f56fecf21eff7d3d3b0e7c68dede and retained 011 branch 8e5811ab595737a5ea9ee24e993867fc99219503."
    }
  ],
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
  "lr": [
    "LR-001",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "decision_class": "D0",
  "merged_tail_recovery": {
    "prior_id": "011-e",
    "pr": 12,
    "frozen_pr_head": "0c6a5a6c4bf96d9a5a89503c316f64445bac81aa",
    "merge_commit": "ff08d6e34601f56fecf21eff7d3d3b0e7c68dede",
    "retained_branch": "oap/011-target-distribution-confirmation-study",
    "publication_commit": "8e5811ab595737a5ea9ee24e993867fc99219503",
    "implementation_parent": "8cdbab0bc2e144b97d78af5245e829d80d2fd984",
    "report_path": "oap/reports/011-e-confirmation-stage1-collection-recovery.md",
    "report_sha256": "6e65c5c074718439c46c44a6f277b4afaf34699d14c150beb7e0164e6c67982d",
    "order_path": "oap/orders/011-e-confirmation-stage1-collection-recovery.md",
    "order_sha256": "872ad6e265d3f0db2045980aa9bd73348fbe48ed22b67f04e4bdeebf71fc0f1c",
    "classification": "PUBLISHED_POST_MERGE_BRANCH_REPORT",
    "acceptance": "PUBLICATION_EVIDENCE_ONLY_NOT_SCIENTIFIC_ACCEPTANCE"
  }
}
```

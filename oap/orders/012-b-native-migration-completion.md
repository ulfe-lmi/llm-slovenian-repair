# 012-b — Complete native migration and bounded test cleanup

Status: FINAL. Publication and FIFO signalling are separate actions; this private source is not active until durable publication.

## Identity

Objective 012, corrective round b. AMEND_EXISTING_PR: PR #14, branch `oap/012-migration-reconciliation`. Continue the same foreground coding session after one externally consumed control frame.

## Provenance

H: the owner's migration/reconciliation request and foreground-only workflow; the Pandoc decision requires migration reconciliation first, with no research restart or unrelated milestone gates. E: actual cache ownership failures, stale configuration example, native baseline timeout and orphaned child, and historical-main equality that fails after a normal merge. I: independent review of PR #14, its report, protected files, actual CI and the native timeout. A: existing recovery, evidence, bounded execution and protected-history contracts. Exact references and source identities are in metadata.

## Current verified state

PR #14 is open. Published 012-a report commit is `3d8f8148188a5b961dd747edee57c1272b31ac94`, with sole parent `b1c274530b81aaa4c79ecaeaef83af071d83ba1d` and only the 012-a report changed. Shared remote verification passed and exact response OK was consumed. Report SHA-256 is `9a6fafb8987771cb6afa9a3d8670cf243e0e7c15eb17d89f57e1de2fb352e015`; preserve its bytes. The report is PARTIAL, with semantic overstatements requiring explicit supersession, not rewriting.

At the final report head, Research reproducibility and OAP report history passed. OAP bootstrap acceptance was cancelled after 10m15s during its tests. Application baseline reported full-pytest TIMEOUT at 600s; its child continued and completed in 771.73s with 794 passed, 58 skipped, 148 subtests passed and only the obsolete example failing. These are not green checks or merge approval. Logs are preserved in `ci-3d8-oap.log` and `ci-3d8-application-failed.log`. Main remains `ff08d6e34601f56fecf21eff7d3d3b0e7c68dede`; publication rechecks all remote identities. PR #13 remains untouched. Preserve the original 011 branch/report ancestry and the three unrelated untracked directories: `corpus/`, `.research-test-scratch/`, `.rclone-speed-test/`.

## Governance

Accepted governance remains `4507cc78e333c0e48226b64266121171b7b8cea8`; its exact identity map is in metadata. Existing candidate governance is authorized by immutable 012-a order SHA-256 `e320df8eb44e76877ec063abf5ca0bd6af6306684beb1bf985cfc25fafd22b34`. Keep those candidate governance bytes unchanged in this round; metadata records the current manifest digest. Use the pinned 012-a candidate-review check against the trusted accepted revision. Do not create another merged-tail receipt: the original 012-a receipt is the unique authority for 011-e reconciliation.

No changes to PLAN, ARCHITECTURE, CRITICAL, source lock or bootstrap seeds. No private governance refresh before accepted merge. No open CRIT entries; no new judgment debt is admitted here.

## Goal and dependencies

Finish the native migration on the existing PR, preserve inherited evidence and prepare reliable development continuation. Pandoc remains the next separately ordered proxy change. This round does not grant scientific, MVP, deployment or release acceptance.

## Scope

Exact allowed implementation paths:

- `oap/bin/source_cache.py`, `oap/runtime.env.example`.
- `oap/tests/test_report_history_cache.py`, `oap/tests/test_split_layout.py`, and bounded new OAP tests solely for these contracts.
- `research/tests/test_research_state_consistency.py` and bounded new synthetic tests solely for the historical identity contract.
- `scripts/verify_development_baseline.py`, `tests/contract/test_objective_001.py`.
- `.github/workflows/oap-bootstrap.yml` and `.github/workflows/application-baseline.yml`, **only their ordered timeout limits**; retain triggers, commands, checks and governance guards.
- `research/RESEARCH-STATE.md`, only additive recovery evidence and accurate report counters. Preserve scientific fields and historical registry entries.
- `README.md`, `STATUS.md`, `docs/OAP-RUNBOOK.md`, `docs/WORKSPACE-PLACEMENT.md`, `docs/DEVELOPMENT.md`, `docs/CODEX-ROLE-SETUP.md`, `docs/READINESS.md`, `docs/IMPLEMENTATION-ROADMAP.md`, only directly affected continuation/status contracts.
- `oap/recovery/012-b-native-migration-completion.md`, affected pins in `oap/GENERATED-FILES.json`, this order, active pointer and the final 012-b report.

No other implementation, workflow or governance edits.

## Non-goals

No research collection, annotation, evaluation rerun, model call, scientific parameter/prompt/scoring/data change or corpus acquisition. No Pandoc/proxy changes in this round. No GPU/Qwen, service, network/VPN/firewall, credential or deployment changes. No new agent, provider, background coding process or history rewrite. No amendment of published orders/reports.

## Files and boundaries

Inspect the named cache ownership/lifecycle code and tests; example/configuration schema and layout tests; immutable 012-a order and historical state identities; the baseline driver's `run_command`, subprocess, readers and cleanup; and the two CI timeout settings. The native timeout receipt documents the exact owned child and manual cleanup. Inspect private receipts by bounded metadata only, never raw primary texts or credentials.

## Requirements

1. Resume the verified 012-a publication head on PR #14 and its existing branch. Do not replay 012-a, create another PR, amend reports, reset, clean, stash, rebase or force-push. Preserve all unrelated local work.

2. Replace source-cache ownership selection based on the unrelated historical `ubuntu` account with the current authorized native process/project owner. Preserve wrong-owner, symlink, hardlink, file-type, hash, inventory, lifecycle, failed-promotion cleanup and read-only consumption protections. Do not chown files or access another user's cache. Exercise actual cache operations in owned temporary directories; an existing unrelated historical account must not redirect authority.

3. Make `runtime.env.example` a portable explicit configuration example. Concrete selected machine roots belong only in WORKSPACE-LAYOUT/private configuration. Replace the obsolete example-equals-this-host assertion with meaningful example/schema/selection checks, including invalid configuration cases. Preserve role-home separation, native real FIFOs and the foreground workflow. Do not weaken runtime ownership/path checks.

4. Treat the research machine block as an authorized historical review snapshot. Bind expected identities to the immutable 012-a order and its pinned digest, not candidate state values alone: `main_sha` and `reviewed_branch_head_sha` remain `ff08d6e34601f56fecf21eff7d3d3b0e7c68dede`; `reviewed_branch_head_parent_sha` remains `0c6a5a6c4bf96d9a5a89503c316f64445bac81aa`. Require the snapshot to be an ancestor of available current `origin/main`, rather than equal to every future main revision. Reject tampered order/snapshot, an unauthorized older snapshot and foreign lineage. Retain the exact 007-o branch/PR/quarantine bindings and all scientific values. Synthetic tests make no network calls; file-only workspace history skips remain explicitly limited.

5. Fix the actual baseline timeout boundary. The driver killed only its direct launcher; orphan pytest retained output pipes and blocked reader closure until strategy terminated that exact owned process. Isolate owned command process groups/sessions on the supported POSIX host; bound termination, escalation and reader completion. Do not signal unrelated processes. Test a real child/grandchild retaining stdout/stderr across timeout **and** a parent exiting while a descendant retains a pipe. Prove bounded return, no surviving owned descendants, preserved unrelated sentinel, and correct success/nonzero/TIMEOUT behavior. Preserve bounded diagnostics and cleanup. This is a focused trusted-test-command fix, not a general sandbox or cross-platform rewrite.

6. Increase finite verification headroom: OAP job timeout 30 minutes; application job timeout 40 minutes; its baseline command timeout 1800 seconds. Keep every test/check/trigger/guard. Actual prior CI took 583.354 seconds for OAP and 564.23 seconds for full pytest; native baseline hit 600 seconds. Do not relabel the old timeout as passed.

7. Explicitly supersede the following 012-a report claims in the new recovery record and report, preserving the original report bytes: `publication_guard --root research` passed for 6,518 research files, not OAP/report/all committed artifacts or universal absence of secrets; earlier dirty-candidate runs retain their actual base, interpreter and limitations, not retrospective exact-commit labels; real pane read-only proof, external FIFO handoff and synthetic CLI/dispatch tests are distinct evidence layers. Remove any carried-forward universal network/temp/exhaustive-test claims unsupported by observations. Approved machine roots intentionally exist in WORKSPACE-LAYOUT. The normal remote report proof is valid; no invented quarantine or forward-recovery metadata is needed.

8. Update directly affected docs and the additive data-free recovery record. Preserve prior registry entries and frozen scientific bytes. Keep report counters accurate under the established report-only publication convention; do not rewrite the historical 012-a PARTIAL record as accepted. Record source revisions, changed contracts, D0 rationale, actual test results and remaining limitations. No new human or milestone gate.

## Acceptance criteria

A1: actual native cache lifecycle passes with correct ownership, while meaningful wrong-owner/type/symlink/hardlink negatives remain.

A2: the portable example and selected configuration contract pass positive and negative checks without embedding new machine roots elsewhere.

A3: the exact authorized historical snapshot accepts normal descendant main and rejects tampering, unauthorized old identities and unrelated history.

A4: real subprocess/pipe timeout and parent-exit cases return within a finite bound, clean owned descendants and preserve the unrelated sentinel and result semantics.

A5: protected history, reports and scientific bytes remain unchanged; the new record explicitly corrects the named evidence overstatements.

A6: all four required final-head CI checks must be observed green before a merge recommendation. Failed, skipped, pending, interrupted and timed-out work remains accurately distinguished.

## Verification

Use the machine-local Python 3.12 interpreter, `-B`, `PYTHONDONTWRITEBYTECODE=1`, `REPAIR_ALLOW_LIVE_TESTS=NO`, owned TMPDIR and CI-parity umask 022. Run focused OAP cache and split-layout unittest modules; research state consistency and new synthetic identity cases; `pytest tests/contract/test_objective_001.py`, including actual subprocess cases. Run applicable Ruff/mypy checks for changed driver/tests.

Run the native baseline driver with an owned persistent temp parent and `--command-timeout 1800`. Keep full OAP, offline research, table regeneration, publication scan, transcript/report-history, protected-source and whitespace coverage. Use actual `--root research` scope when citing that scan; cite an actual staged-index scan separately if performed. Reuse valid unchanged evidence rather than duplicating long suites solely to relabel a SHA. Record exact tested commits and dirty-candidate limitations.

Required CI remains: Application baseline; Research reproducibility; OAP bootstrap acceptance; OAP report history. Use the existing pinned 012-a candidate-governance review. No check disabling, broad catches or fake live success. Diagnose the earliest failing boundary before further changes.

## Local setup and constraints

Only the existing foreground coding agent may implement. Do not launch another coding model, change provider, spawn a subagent or create a background coding agent. Restart only if it dies, using exactly `codex --yolo --profile early-beta` in the coding directory. Preserve the launched CODEX_HOME/auth context. Ordinary bounded owned test processes are allowed. Consume control once externally; coding must not wait for it again. Existing archive restoration is complete; no credential activation or research replay.

## Documentation

Explain current-owner cache authority, portable example usage, historical review snapshot semantics and bounded test cleanup. Correct current continuation/status instructions where directly affected. The new recovery record must distinguish actual observations from limitations and explicitly supersede the named 012-a claims. Do not claim deployment/MVP acceptance or rewrite audit seeds.

## Git and report publication

Use existing PR #14 and normal implementation commits. No merge, auto-merge, force-push or history rewrite. Verify actual PR identity before composing the final report. Record literal implementation head and `SELF`, with `publication_verified=false`. Validate a concise private draft before installing it. Use required metadata and a short acceptance/evidence table without duplicating long narrative; the 49 KB 012-a report is not a length template. The final commit changes only the immutable report path and has the implementation head as sole parent. Push and verify actual remote head/report bytes/parent/path before exact response OK. No further mutations in that completed round. Post-publication CI belongs in private review evidence, not a prewritten future-success claim.

Strategy reviews all rounds and required final-head CI before a normal expected-SHA development merge preserving original ancestry. Development merge is not deployment approval. Private governance refresh happens only after accepted merge at a quiescent checkpoint with backups.

## Decision classification

D0: bounded reversible corrections to observed native migration, historical identity, test-runtime and evidence defects. No new D1 judgment debt; D2 actions remain outside scope.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "012-b",
  "title": "Complete native migration, bounded test cleanup and historical-state reconciliation",
  "objective": "012",
  "status": "FINAL",
  "phase": "DEVELOPMENT_RECOVERY",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ff08d6e34601f56fecf21eff7d3d3b0e7c68dede",
  "governance_ref": "4507cc78e333c0e48226b64266121171b7b8cea8",
  "branch": "oap/012-migration-reconciliation",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 14,
  "dependencies": [
    "011"
  ],
  "local_work": "Preserve original 011 branch/report ancestry, immutable 012-a report 3d8f814, all prior orders/reports and untracked corpus/, .research-test-scratch/, .rclone-speed-test/. Tracked tree is clean after 012-a.",
  "prior_review": "012-a remote report verified at 3d8f8148188a5b961dd747edee57c1272b31ac94, parent b1c274530b81aaa4c79ecaeaef83af071d83ba1d. PARTIAL; native owner, example, driver cleanup and historical snapshot corrections required. Final-head research and report-history CI passed; OAP job cancelled; application driver reported TIMEOUT after 600 seconds with its descendant completing in 771.73 seconds (794 passed, 58 skipped, one example failure). Overbroad report claims are explicitly superseded in this round, never rewritten.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner migration/reconciliation and foreground-only instructions; owner Pandoc decision requires active migration reconciliation first, without research restart or unrelated milestone gates."
    },
    {
      "kind": "E",
      "reference": "PR #14 final head 3d8f814: application TIMEOUT with child pytest 794 passed/58 skipped/one example failure; OAP cancelled; research and report-history passed. Native cache-owner failures and observed orphan-pipe hang are preserved in private receipts."
    },
    {
      "kind": "I",
      "reference": "Independent report verification, protected-file preservation, native-baseline-orphan-cleanup.json and 012a-publication-independent-review.json; immutable 012-a order digest e320df8eb44e76877ec063abf5ca0bd6af6306684beb1bf985cfc25fafd22b34."
    },
    {
      "kind": "A",
      "reference": "Strategic S-RECOVER-01, S-EVIDENCE-01, S-MERGE-01; existing protected-history and bounded-runtime contracts."
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
  "prior_round_publication": "3d8f8148188a5b961dd747edee57c1272b31ac94",
  "candidate_governance_manifest_sha256": "8f2641bbd85a2df29b373853b0add6d979138adde1a15ec4c8e5f8674b4afc72"
}
```

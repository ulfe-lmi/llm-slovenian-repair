# 012-a migration revision record — native host and merged-round reconciliation

Order: 012-a, `oap/orders/012-a-native-migration-and-merged-round-reconciliation.md`,
sha256 `e320df8eb44e76877ec063abf5ca0bd6af6306684beb1bf985cfc25fafd22b34`.
Date: 2026-10-25. Classification: D0 — bounded reversible host/protocol
reconciliation preserving the existing authority boundary and exact immutable
history. Accepted governance ref: `4507cc78e333c0e48226b64266121171b7b8cea8`.

This record is data-free: no machine roots, credentials, raw text or private
paths. The selected machine roots are versioned only in
`oap/governance/WORKSPACE-LAYOUT.json` (the only versioned place authorized to
contain them); elsewhere only logical names (OAP_STRATEGIC_HOME,
OAP_FIFO_HOME, REPO_ROOT) and environment variable names are used.

## Rationale

1. Native migration. The obsolete host's layout (obsolete `/home/ubuntu`
   roots, owner-selected-sync strategic subtree) no longer matches the
   migrated host. The owner-directed 2026-10-25 migration moves the whole
   runtime to the current native host: STRATEGIC_HOME and the two real FIFOs
   under the user's native home (OAP_FIFO_HOME), strict 0700/0600 for native
   private directories/files, symlink/owner/type/overlap rejection. The
   historical exact owner-selected-sync POSIX exception remains supported in
   code for the legacy subtree only and is not applied to native roots.
2. Foreground-only coding dispatch (owner-selected). The dispatcher adopts
   the already-running pane, verifies its PID/cwd/argv, consumes one exact OK
   control frame outside the model, writes the durable consumed record and
   returns a paste-ready handoff explicitly conveying OAP_ROLE=coding. Legacy
   coding launch/tmux entry points fail closed (FOREGROUND_DISPATCH_ONLY)
   instead of falling back; no background panes, no codex exec, no
   auto-restart. If the coding pane later dies, the only authorized relaunch
   is the exact argv recorded in the layout record, in the coding directory.
   The owner-launched session home is preserved as launched: adoption never
   relocates CODEX_HOME or copies authentication.
3. Merged-tail publication semantics. The 011-e report was published after
   its PR (PR12) merged mid-round, on the original retained branch. Both role
   laws and the strategic recovery table now state the shared classification:
   such a report is recognized only as post-merge branch publication evidence
   under an explicit pinned recovery receipt (original same-repository
   PR/branch, real merge ancestry, frozen head ancestor, exact report
   parent/path/bytes, exact original order, check-SHA ancestry). The
   publication proof alone does not establish integration or scientific
   acceptance; any later integration must be verified separately on current
   main.

## Changed clauses

| Path | Clause(s) | Change |
|---|---|---|
| oap/governance/WORKSPACE-LAYOUT.json | record | Native roots (logical names), strategic_storage native, coding_dispatch foreground, exact foreground_launch argv, authority/permission semantics updated |
| oap/strategic-instructions/AGENTS.md | S-PLACEMENT-01 | Native migration wording: strict native 0700/0600 (FIFO modes unchanged), roots only-versioned, legacy sync exception code support only, foreground-only dispatch, session home preserved |
| oap/strategic-instructions/AGENTS.md | S-RECOVER-01 | Added merged-tail classification and receipt requirement |
| oap/strategic-instructions/OAP-COMMUNICATION-strategic.md | §3, §6, §9, §11 | Native storage wording; foreground dispatcher handoff; recovery-table merged-tail row; foreground-dispatch operator command |
| oap/strategic-instructions/strategic_model_init_material.md | startup paragraph | 2026-10-25 native migration, foreground dispatch, legacy exception scope |
| oap/coding-instructions/AGENTS.md | C-PLACEMENT-01, C-FG-01 (new), C-RECOVER-01 | Native wording + session home preserved; new foreground-only execution clause; merged-tail classification |
| OAP-COMMUNICATION-coding-agent.md | P-PLACEMENT-01, P-FIFO-01 | Native wording + session home preserved; foreground dispatcher handoff and fail-closed legacy entry points |
| oap/prompts/coding-round.md | prompt | Foreground adoption note; retains literal OAP_ROLE=coding; no FIFO wait instructions |
| oap/prompts/strategic-start.md | prompt | Foreground-dispatch adoption instruction |
| SECURITY.md | SEC-05 | Strict native modes; legacy exception remains code support only |
| oap/governance/DISTILLATION-MAP.md | map | GOV_SOURCE hashes refreshed; layout-delta section updated (rows S/C/P-PLACEMENT-01, SEC-05, new C-FG-01); main-table rows C-RECOVER-01/P-FIFO-01 extended; new merged-tail delta section |
| oap/governance/MANIFEST.json | manifest | identities/layout_revision/coding_bytes/coverage updated together with the projections |

## Accepted old hashes (at 4507cc78e333c0e48226b64266121171b7b8cea8)

| Path | sha256 | bytes |
|---|---|---|
| oap/governance/WORKSPACE-LAYOUT.json | cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254 | 688 |
| oap/strategic-instructions/AGENTS.md | ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c | 19704 |
| oap/strategic-instructions/OAP-COMMUNICATION-strategic.md | 6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf | 23172 |
| oap/strategic-instructions/strategic_model_init_material.md | 813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d | 1217 |
| oap/coding-instructions/AGENTS.md | 55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514 | 7695 |
| OAP-COMMUNICATION-coding-agent.md | 6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b | 6736 |
| oap/prompts/coding-round.md | fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611 | 353 |
| oap/prompts/strategic-start.md | 40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b | 742 |
| SECURITY.md | 0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6 | 1756 |
| oap/governance/DISTILLATION-MAP.md | a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7 | 63613 |
| oap/governance/MANIFEST.json | 22a2a103a6c2a9e5a6534c14f94dc9bcd9bfce5852b7f0f65db156fa28447b68 | 69978 |

Candidate hashes and byte counts are recorded in the candidate
`oap/governance/MANIFEST.json` identities and in the final 012-a report.

## Preserved

- Exact OK FIFO framing, role locks, activation gates, publication/SELF
  mechanics, report-history strictness: unchanged.
- LR-001–LR-014 coverage intact; coding read-set total 36770/50000 bytes with
  all per-file budgets satisfied.
- PLAN, ARCHITECTURE, CRITICAL, source lock and docs/bootstrap bytes:
  unchanged (protected surfaces).
- Private strategic law remains accepted-old until strategy reviews/merges and
  deliberately refreshes it (S-EVOLVE-01).
- No new scientific or live model calls; no activation or deployment side
  effect; historical sync exception retained as legacy code support only.

## Tests (observed; tested SHAs recorded in the final 012-a report)

- Focused CLI-boundary suites: oap/tests/test_merged_tail.py,
  oap/tests/test_foreground_pane.py, oap/tests/test_candidate_review.py
  (positive and negative cases for merged-tail evidence, foreground
  process/pane boundary, and order-bound candidate review). These ran on the
  dirty implementation tree; final-SHA re-verification is recorded in the
  final 012-a report.
- Real-host probes (read-only): actual selected-pane foreground verification
  (positive) and background-child negative (PANE_NOT_FOREGROUND);
  verify_report(011-e) remote: PASSED after the HEAD literal-SHA boundary fix.
  Native real-host doctor: NOT RUN at this record's time; result recorded in
  the final 012-a report once the probe passes on the committed tree.
- Shared candidate review against the literal trusted accepted ref and the
  exact ordered 11-path allowlist: valid (this PR).

# Two-role development runbook

Layout authority: the versioned `oap/governance/WORKSPACE-LAYOUT.json` is the
only versioned place holding the selected machine roots. The
[workspace placement](WORKSPACE-PLACEMENT.md) document is the historical
2026-09-07 sync-mount record, superseded for root placement by the 012-a
native migration; its sync-exception semantics survive only in the narrow
legacy code path. All regular strategic files are under the selected
workspace (native storage, strict 0700/0600 private modes); the actual FIFOs
are `OAP_FIFO_HOME/control.fifo` and `OAP_FIFO_HOME/response.fifo` in the
native home `.oap-fifos/llm-slovenian-repair`. Use the relocated strategic
`runtime.env`; never derive FIFO paths from cwd.

The installed repo is owner-published bootstrap infrastructure accepted for
continued development. Role operation is qualified and the development loop has
been deliberately started. Query current protocol state from `oap/active` or with
`python3 oap/bin/check_state.py --repo-root PATH --repository OWNER/REPO`. The
separate strategic workspace contains full
law, mutable drafts, configuration and role homes; the unsignaled real FIFOs reside
in OAP_FIFO_HOME. No model starts here.

Review `oap/GENERATED-FILES.json`, `oap/INSTALLATION.json`, source lock, current
governance map and bootstrap receipt. Run `bash oap/bin/doctor.sh --config
PRIVATE_RUNTIME_PATH`. The helper is read-only and reports structural, activation,
live-test and product statuses independently. Repeat fixture tests with TESTING.md.

Materialization: `bash oap/bin/bootstrap-two-codex-oap.sh --repo-root PATH
--strategic-home PATH --bootstrap-root INPUT_PATH --dry-run` prints scoped actions
without files/locks/Git creation. Omit --dry-run to install. Source repo defaults to
the helper's own checkout. Identical reruns preserve bytes/modes/mtime; changed
generated files need explicit --refresh and backups. Private drafts/config/history
are preserved; divergent law needs accepted-governance refresh, never silent overwrite.

The owner-published remote baseline is accepted for continued development.
Review/stage only manifest-listed related files, never blind git add -A over dirty
work. Establish protected development branch, required checks and approved merge
method; inspect merge deployment side effects before allowing strategic merge.
Select separate role models/profiles/auth and literal accepted Git SHA in private
runtime.env. The allowlisted KEY=JSON-string format is data; do not shell-source.

Historical legacy instructions (superseded for current native operation by
the foreground dispatch section below; retained for the legacy sync layout):

Setup: `bash oap/bin/launch-codex-setup-tmux.sh --config PRIVATE_RUNTIME_PATH
--print-only` previews; without preview opens coding left/strategy right live
shells, correct cwd/CODEX_HOME, no prompts/signals/model/auth prerequisite. Owner
may invoke configured CLI manually; exiting returns to the same live shell.

Operation: after doctor, deliberate OAP_ACK_DANGER_FULL_ACCESS=YES and
OAP_ACK_START_LOOP=YES plus qualified roles/baseline enable launch-oap-tmux.sh.
Coding waits externally; strategy reconciles and publishes orders. No background
startup hooks or automatic quit resurrection. Live repair testing remains disabled;
product readiness, ICA, milestone acceptance, release and deployment retain their
separate gates.

Foreground coding dispatch (012-a selection): under
`coding_dispatch: "foreground"` the legacy tmux launch path above must not
start the coding model. The owner launches the coding session; strategy
adopts it with the exact continuation command:

PANE_PID is the shell PID of the explicitly selected tmux pane.

    OAP_ROLE=strategic $HOME/envs/llm-slovenian-repair/bin/python -B \
      oap/bin/oap_cli.py foreground-dispatch \
      --config PRIVATE_RUNTIME_PATH --repo-root . --pane-pid PANE_PID

For an already-consumed unfinished round in a reconciled state, add
`--resume-id ROUND_ID` for the explicit same-ID resume. The helper verifies
the selected pane and its actual Codex descendant (working directory, full
launch argv, foreground process-group ownership), reconciles the active
order/branch/PR peers, waits on the actual control FIFO for exactly one ASCII
OK consumed outside the coding model, records the atomic consumed receipt,
and returns the handoff to paste into the named pane; it starts zero models
and rejects closed/merged PR peers, dead/wrong-cwd/wrong-argv panes, and
duplicate or replayed signals. The handoff conveys OAP_ROLE=coding, and the
coding pane exports `OAP_ROLE=coding` in helper command environments. If the
pane later dies, the authorized relaunch is exactly
`codex --yolo --profile early-beta` in the coding directory; the coding agent
never starts background coding agents or models (no background codex/exec, no
alternate providers, no relaunch or resurrection of the coding pane) - other
background test/helper processes remain normal. Read-only doctor reports the
selection and activation boundary independently:

    OAP_ROLE=strategic $HOME/envs/llm-slovenian-repair/bin/python -B \
      oap/bin/oap_cli.py doctor --config PRIVATE_RUNTIME_PATH --repo-root .

Publication/signal/review/merge follow full strategic communication. Open D1 gates
allow contained development only; deployment always has separate human authority.

Transcript guard sequence: before implementation, resolve the exact active round,
explicitly run `git add -f oap/active` even when status is silent, and prove the
staged pointer with `git show :oap/active` (for example, compare its exact hex
bytes, including the final LF). Run
`python3 oap/bin/check_transcript.py --repo-root PATH --index --expected-id NNN-a`.
Commit all non-report work, including the order and active pointer, then rerun
`python3 oap/bin/check_transcript.py --repo-root PATH --revision HEAD
--expected-id NNN-a`. Create the PR before composing the immutable SELF report;
the report-only commit must have the implementation head as its sole parent and
must change only the report. CI repeats committed-mode transcript validation at
the final report head. Publication helpers do not implicitly stage, commit or
signal the pointer.

The 001-b/001-c active snapshots were not staged in the historical 001 commits;
they remain recorded as an incident and are not reconstructed as fabricated
commits.

Round 006-k adds the history-aware report guard. `oap/REPORT-HISTORY-INCIDENTS.json`
is a strict record of the two frozen 006-a/006-c violations; executable identities
in `oap/bin/oap_core.py` prevent the record from granting another exception.
Run `python3 oap/bin/check_report_history.py --repo-root PATH --revision HEAD
--require-manifest` on a full-history checkout. Normal reports are add-once,
report-only commits whose sole parent is the recorded implementation head.

The objective-006 archive cache is an explicit external experiment resource at
`OAP_STRATEGIC_HOME/source-cache/concept-verification/gigafida-2.0-words`.
`python3 oap/bin/source_cache.py plan --strategic-home PATH` and `validate`
perform no network operation. Promotion consumes only the fixed `part.zip` after
the checked-in verifier passes; it uses one lock-protected same-directory rename
and refuses overwrite, symlinks, hardlinks, unexpected files, stale metadata, and
arbitrary URLs. Cleanup requires an explicit completed/abandoned concept-experiment
lifecycle. The 006-k receipt preserves the failed hardlink boundary at cumulative
thirteen GETs; the immutable 006-l receipt records one verified rename-only
establishment at cumulative fourteen, two content-free consumers and three
revalidations. A valid generation is reused with zero later GETs.

Post-merge publication exception (merged tail): a merged PR whose later
report lives on its original retained branch is recognized only as
post-merge branch publication evidence, never as integrated or accepted
work - the publication proof alone does not establish integration, and any
later main ancestry must be verified separately; the normal open-PR exact-head
gate is unchanged, and the exception binds to the explicit
merged_tail_recovery receipt (original PR identity,
branch/ref, merged state and merge ancestry on the current default branch,
frozen PR head ancestor of the report, current retained-branch tip, exact
report parent/only-path/content, exact original order). The 011-e tail is
that case: PR #12 (merged mid-round at
ff08d6e34601f56fecf21eff7d3d3b0e7c68dede; frozen head
0c6a5a6c4bf96d9a5a89503c316f64445bac81aa), retained branch
oap/011-target-distribution-confirmation-study at publication commit
8e5811ab595737a5ea9ee24e993867fc99219503 (implementation parent
8cdbab0bc2e144b97d78af5245e829d80d2fd984), report
oap/reports/011-e-confirmation-stage1-collection-recovery.md (sha256
6e65c5c074718439c46c44a6f277b4afaf34699d14c150beb7e0164e6c67982d) and order
oap/orders/011-e-confirmation-stage1-collection-recovery.md (sha256
872ad6e265d3f0db2045980aa9bd73348fbe48ed22b67f04e4bdeebf71fc0f1c). The
publication proof alone does not establish integration or scientific
acceptance; any later main ancestry must be verified separately.

Data availability (012-a): the privately missing 011 research data archive
was historically absent at the migrated locations; the owner supplied it and
strategy restored it on 2026-10-25: the 926 selected files are
hash-verified (923 restored as new, 3 pre-existing identity files
byte-identical and untouched) with their collection bindings - 134 inputs,
134 main answers, 247 scaffold texts, 381 raw capture integrity records, and
20 calibration + 109 confirmation queue memberships - checked against the
frozen 011b manifest; receipts are private and metadata-only. Evaluation
remains blocked pending separate reconciliation of the evaluation objective
(no prior draft activated). Known
residuals named for the scoped 012-b follow-up: oap/bin/source_cache.py
native owner-account ownership and oap/runtime.env.example stale roots.

Next engineering scope (post-recovery): the owner-selected Pandoc
structural-parsing proxy for a runnable repair is the next separately
ordered objective and is not implemented; a provisional estimate for the
remaining packaged-MVP engineering scope is 8-15 focused engineering days.
Research-evaluation completion, packaged MVP, ICA and deployment remain
separate gates; no activation or deployment side effect occurs on merge,
and all inspected workflows are PR tests only.

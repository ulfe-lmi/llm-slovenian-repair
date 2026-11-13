# Two-role development runbook

Operating runbook for the two-role OAP development loop (strategic and
coding). Layout authority: the versioned
`oap/governance/WORKSPACE-LAYOUT.json` is the only versioned place holding the
selected machine roots; the [workspace placement](WORKSPACE-PLACEMENT.md)
document is the historical 2026-09-07 sync-mount record, superseded for root
placement by the 012-a native migration (its sync-exception semantics survive
only in the narrow legacy code path). All regular strategic files are under the
selected workspace (native storage, strict 0700/0600 private modes); the actual
FIFOs are `OAP_FIFO_HOME/control.fifo` and `OAP_FIFO_HOME/response.fifo` in the
native home `.oap-fifos/llm-slovenian-repair`. Use the relocated strategic
`runtime.env`; never derive FIFO paths from cwd. No model starts here.

## Current state and doctor

The installed repo is owner-published bootstrap infrastructure accepted for
continued development. Role operation is qualified and the development loop has
been deliberately started.

Commands run from the repository root with the qualified development
interpreter ([setup](DEVELOPMENT.md)):

- Query current protocol state from `oap/active`, or with

  ```sh
  python3.12 oap/bin/check_state.py --repo-root PATH --repository OWNER/REPO
  ```

- Review [oap/GENERATED-FILES.json](../oap/GENERATED-FILES.json),
  [oap/INSTALLATION.json](../oap/INSTALLATION.json), the
  [source lock](../oap/bootstrap-sources.lock.json), the
  [current governance map](../oap/governance/MANIFEST.json) and the
  [bootstrap receipt](../oap/BOOTSTRAP-MANIFEST.sha256).
- Run the read-only doctor, which reports structural, activation,
  live-test and product statuses independently:

  ```sh
  bash oap/bin/doctor.sh --config PRIVATE_RUNTIME_PATH
  ```

- Repeat the fixture tests per [TESTING.md](../TESTING.md).

## Materialization

```sh
bash oap/bin/bootstrap-two-codex-oap.sh --repo-root PATH --strategic-home PATH \
  --bootstrap-root INPUT_PATH --dry-run
```

prints scoped actions without files/locks/Git creation. Omit `--dry-run`
to install. The source repo defaults
to the helper's own checkout. Identical reruns preserve bytes/modes/mtime;
changed generated files need explicit `--refresh` and backups. Private
drafts/config/history are preserved; divergent law needs accepted-governance
refresh, never silent overwrite.

## Role selection and dispatch

Helper-managed fresh setup selects separate role models/profiles/auth and a
literal accepted Git SHA in the private `runtime.env`; the allowlisted
KEY=JSON-string format is data, never shell-sourced. Adoption of the
owner-launched foreground session reconfigures nothing: the exact
foreground argv comes from the
[layout](../oap/governance/WORKSPACE-LAYOUT.json) and the launched
`CODEX_HOME`, authentication and configuration are preserved exactly as
launched ([role setup](CODEX-ROLE-SETUP.md)).

### Foreground coding dispatch (012-a selection)

Under `coding_dispatch: "foreground"` the legacy tmux launch path below must
not start the coding model. The owner launches the coding session; strategy
adopts it with the exact continuation command (PANE_PID is the shell PID of the
explicitly selected tmux pane):

    OAP_ROLE=strategic $HOME/envs/llm-slovenian-repair/bin/python -B \
      oap/bin/oap_cli.py foreground-dispatch \
      --config PRIVATE_RUNTIME_PATH --repo-root . --pane-pid PANE_PID

For an already-consumed unfinished round in a reconciled state, add
`--resume-id ROUND_ID` for the explicit same-ID resume. The helper verifies the
selected pane and its actual Codex descendant (working directory, full launch
argv, foreground process-group ownership), reconciles the active
order/branch/PR peers, waits on the actual control FIFO for exactly one ASCII
OK consumed outside the coding model, records the atomic consumed receipt, and
returns the handoff to paste into the named pane; it starts zero models and
rejects closed/merged PR peers, dead/wrong-cwd/wrong-argv panes, and duplicate
or replayed signals. The handoff conveys OAP_ROLE=coding, and the coding pane
exports `OAP_ROLE=coding` in helper command environments. If the pane later
dies, the authorized relaunch is exactly `codex --yolo --profile early-beta` in
the coding directory; the coding agent never starts background coding agents or
models (no background codex/exec, no alternate providers, no relaunch or
resurrection of the coding pane) — other background test/helper processes
remain normal. Read-only doctor reports the selection and activation boundary
independently:

    OAP_ROLE=strategic $HOME/envs/llm-slovenian-repair/bin/python -B \
      oap/bin/oap_cli.py doctor --config PRIVATE_RUNTIME_PATH --repo-root .

### Legacy tmux launch (superseded for current native operation)

Retained for the legacy sync layout.

Setup preview (without `--print-only` the helper opens coding
left/strategy right live
shells; the same live shells remain after exiting):

```sh
bash oap/bin/launch-codex-setup-tmux.sh --config PRIVATE_RUNTIME_PATH --print-only
```

The helper opens correct cwd/CODEX_HOME shells with no
prompts/signals/model/auth prerequisite. The owner may invoke the configured
CLI manually; exiting returns to the same live shell.

Operation: after doctor, deliberate `OAP_ACK_DANGER_FULL_ACCESS=YES` and
`OAP_ACK_START_LOOP=YES` plus qualified roles/baseline enable
launch-oap-tmux.sh. Coding waits externally; strategy reconciles and publishes
orders. No background startup hooks or automatic quit resurrection. Live repair
testing remains disabled; product readiness, ICA, milestone acceptance, release
and deployment retain their separate gates.

## Branching and publication discipline

Review/stage only manifest-listed related files; never a blind `git add -A`
over dirty work. Establish the protected development branch, required checks and
approved merge method; inspect merge deployment side effects before allowing a
strategic merge. Publication/signal/review/merge follow the full strategic
communication law. Open D1 gates allow contained development only; deployment
always has separate human authority.

## Transcript guard sequence

Before implementation, resolve the exact active round, explicitly run
`git add -f oap/active` even when status is silent, and prove the staged
pointer with `git show :oap/active` (for example, compare its exact hex bytes,
including the final LF). Then run the index check, commit all non-report work
(order and active pointer included), and rerun the committed check:

```sh
python3.12 oap/bin/check_transcript.py --repo-root PATH --index --expected-id NNN-a
python3.12 oap/bin/check_transcript.py --repo-root PATH --revision HEAD \
  --expected-id NNN-a
```

Create the PR before composing the immutable SELF report;
the report-only commit must have the implementation head as its sole parent and
must change only the report. CI repeats committed-mode transcript validation at
the final report head. Publication helpers do not implicitly stage, commit or
signal the pointer.

## Report-history guard (006-k)

Round 006-k adds the history-aware report guard.
`oap/REPORT-HISTORY-INCIDENTS.json` is a strict record of the two frozen
006-a/006-c violations; executable identities in `oap/bin/oap_core.py` prevent
the record from granting another exception. Run the guard on a
full-history checkout:

```sh
python3.12 oap/bin/check_report_history.py --repo-root PATH \
  --revision HEAD --require-manifest
```

Normal reports are add-once, report-only commits whose sole parent is the
recorded implementation head.

## Historical incident and recovery records (abridged)

- **001-b/001-c active snapshots** — not staged in the historical 001
  commits; recorded as an incident, not reconstructed as fabricated commits.
- **Objective-006 archive cache** — an explicit external experiment
  resource at
  `OAP_STRATEGIC_HOME/source-cache/concept-verification/gigafida-2.0-words`;
  `python3.12 oap/bin/source_cache.py plan --strategic-home PATH` and `validate`
  perform no network operation. Promotion consumes only the fixed `part.zip`
  after the checked-in verifier passes; it uses one lock-protected
  same-directory rename and refuses overwrite, symlinks, hardlinks, unexpected
  files, stale metadata and arbitrary URLs. Cleanup requires an explicit
  completed/abandoned concept-experiment lifecycle. The frozen 006-k/006-l
  receipts preserve the failed hardlink boundary (cumulative thirteen GETs) and
  the verified rename-only establishment (cumulative fourteen, two
  content-free consumers, three revalidations); a valid generation is reused
  with zero later GETs.
- **Post-merge publication exception (merged tail)** — a merged PR whose
  later report lives on its original retained branch is recognized only as
  post-merge branch publication evidence, never as integrated or accepted
  work: the publication proof alone does not establish integration, and any
  later main ancestry must be verified separately. The exception binds to the
  explicit `merged_tail_recovery` receipt (original PR identity, branch/ref,
  merged state and merge ancestry on the current default branch, frozen PR head
  ancestor of the report, current retained-branch tip, exact report
  parent/only-path/content, exact original order). The 011-e tail is that
  case: PR #12 merged mid-round at `ff08d6e34601f56fecf21eff7d3d3b0e7c68dede`
  (frozen head `0c6a5a6c4bf96d9a5a89503c316f64445bac81aa`), retained branch
  `oap/011-target-distribution-confirmation-study` at publication commit
  `8e5811ab595737a5ea9ee24e993867fc99219503` (implementation parent
  `8cdbab0bc2e144b97d78af5245e829d80d2fd984`), report
  `oap/reports/011-e-confirmation-stage1-collection-recovery.md` and order
  `oap/orders/011-e-confirmation-stage1-collection-recovery.md`; the
  [012-a reconciliation record](../oap/recovery/012-a-migration-reconciliation.md)
  is the authoritative source. The normal open-PR exact-head gate remains
  unchanged: this exception is not general permission to publish or accept
  merged work, and the current receipt conditions stand.
- **012-a data availability and 012-b completion** — the privately
  missing 011 research data archive was historically absent at the migrated
  locations; the owner supplied it and strategy restored it on 2026-10-25: 926
  selected files hash-verified (923 restored as new, 3 pre-existing identity
  files byte-identical and untouched) with their collection bindings — 134
  inputs, 134 main answers, 247 scaffold texts, 381 raw capture integrity
  records, and 20 calibration + 109 confirmation queue memberships —
  checked against the frozen 011b manifest; receipts are private and
  metadata-only. Evaluation of that archived objective remained historically
  blocked pending its own separate reconciliation (no prior draft activated);
  the status is historical, not a current instruction to restart research. Known 012-a residuals
  (`oap/bin/source_cache.py` native owner-account ownership and
  `oap/runtime.env.example` stale roots) were resolved by the scoped 012-b
  completion round: the report-history cache now uses the current process UID
  as its only ownership authority, and the committed example is a portable
  template containing no machine roots (see the
  [012-b completion record](../oap/recovery/012-b-native-migration-completion.md)).

## Current scope

The owner-selected Pandoc structural-parsing proxy for a runnable repair is
implemented (rounds 013-a through 036-a; see [STATUS](../STATUS.md) and
[IMPLEMENTATION-ROADMAP](IMPLEMENTATION-ROADMAP.md)). Further scope follows
separately ordered objectives. Research-evaluation completion and packaged
MVP are separate out-of-scope programmes, not gates for the runnable proxy;
ICA and deployment remain separate authorities, independent closure and
deployment authority unchanged and the owner no-separate-human-dataset
decision standing. No activation or deployment side effect occurs on merge,
and all inspected workflows are PR tests only.

# Inactive two-role runbook

Owner layout update: see [workspace placement](WORKSPACE-PLACEMENT.md).
All regular strategic files are under the selected workspace; actual FIFOs are
`OAP_FIFO_HOME/control.fifo` and `OAP_FIFO_HOME/response.fifo` in the native home.
Use the relocated strategic `runtime.env`; never derive FIFO paths from cwd.

The installed repo is bootstrap infrastructure, uncommitted on a local main unless
an existing checkout was preserved. The separate strategic workspace contains full
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

Owner chooses remote/visibility and authorized baseline publication separately.
Review/stage only manifest-listed related files, never blind git add -A over dirty
work. Establish protected development branch, required checks and approved merge
method; inspect merge deployment side effects before allowing strategic merge.
Select separate role models/profiles/auth and literal accepted Git SHA in private
runtime.env. The allowlisted KEY=JSON-string format is data; do not shell-source.

Setup: `bash oap/bin/launch-codex-setup-tmux.sh --config PRIVATE_RUNTIME_PATH
--print-only` previews; without preview opens coding left/strategy right live
shells, correct cwd/CODEX_HOME, no prompts/signals/model/auth prerequisite. Owner
may invoke configured CLI manually; exiting returns to the same live shell.

Operation: after doctor, deliberate OAP_ACK_DANGER_FULL_ACCESS=YES and
OAP_ACK_START_LOOP=YES plus qualified roles/baseline enable launch-oap-tmux.sh.
This bootstrap leaves both NO. Coding waits externally; strategy reconciles and
publishes first order. No background startup hooks or automatic quit resurrection.
Publication/signal/review/merge follow full strategic communication. Open D1 gates
allow contained development only; deployment always has separate human authority.

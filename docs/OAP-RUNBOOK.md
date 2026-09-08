# Two-role development runbook

Owner layout update: see [workspace placement](WORKSPACE-PLACEMENT.md).
All regular strategic files are under the selected workspace; actual FIFOs are
`OAP_FIFO_HOME/control.fifo` and `OAP_FIFO_HOME/response.fifo` in the native home.
Use the relocated strategic `runtime.env`; never derive FIFO paths from cwd.

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
the checked-in verifier passes; it refuses overwrite, symlinks, hardlinks,
unexpected files, stale metadata, and arbitrary URLs. Cleanup requires an explicit
completed/abandoned concept-experiment lifecycle. Acquisition receipts bind the
twelve legacy GETs and the current generation/count; a valid generation is reused
with zero later GETs.

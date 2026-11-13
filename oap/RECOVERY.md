# Durable recovery

Recovery rules for the two-role OAP loop. Resolve both actual pipe paths
through OAP_FIFO_HOME, the only place holding real pipes; the current
strategic roots and storage semantics come from
[WORKSPACE-LAYOUT.json](governance/WORKSPACE-LAYOUT.json), and the current
native strategic homes contain regular files only. The narrow historical
legacy sync-mount exception (a synced strategic workspace held regular
files only) is historical, not current placement. Never reconstruct a
missing pipe as an empty regular file or signal a stale pre-relocation
path.

## Round identity

- No active: inactive/wait outside the model.
- Empty or malformed active: invalid, no guessing.
- Consumed signal with no report: explicit recovery, same ID/branch/PR and the
  first unfinished criterion. An interrupted a with a PR reuses it, never
  creates a duplicate. Record the reason in the private workorders before a
  deliberate `--resume-id` and re-signal.
- Process/context/model/provider/host replacement changes no
  objective/suffix/authority.

## Publication and remote state

- Local report, remote unverified: reconcile/finish publication without
  rewriting the immutable report.
- Remote final report, lost notification: strategic review; a duplicate
  signal suppresses coding.
- Publication crash between order write and active update: an identical
  still-unresolved retry may finish activation; a conflicting/completed order
  cannot reactivate.

## Critical register

- Critical append crash: compare full prior/payload; an exact replay is a
  no-op, and partial/stale history stops. No seed reconstruction of a missing
  CRITICAL.

## Boundaries

- A nonzero role exit or inconsistent publication records a bounded private
  incident, never an automatic restart or a false OK.
- Pending required CI means wait/recheck, no busywork/suffix.
- Explicit quit returns to the shell; no watchers/services/autostart.
- Read current GitHub/OAP before relying on a handoff. Preserve observations;
  supersede incorrect interpretations explicitly. Private logs contain
  status/SHA/counts only.

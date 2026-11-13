# Concentrated OAP infrastructure

This directory is the concentrated OAP development infrastructure for this
repository: the immutable transcript history, the current-round pointer, and
the shared standard-library helpers.

- **Orders and reports** ([`orders/`](orders/), [`reports/`](reports/)) —
  published orders and reports are immutable transcript history;
  [`oap/active`](active) names the current round. Drafts live in
  [strategic-instructions/initial-orders](strategic-instructions/initial-orders)
  and in private drafts, never in an active queue.
- **Helpers** ([`bin/`](bin/)) — shared standard-library helpers implement
  publication, integrity, exact FIFO, SELF, transcript coherence,
  state/recovery and the audit schema; tests use disposable fixtures and fake
  boundaries. Use each helper's `--help` and the [runbook](../docs/OAP-RUNBOOK.md).

## Transcript guard

Commands run from the repository root with the qualified development
interpreter (setup: [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md)). Before an
implementation commit, force-stage the active pointer and verify the index
directly:

```sh
git add -f oap/active
python3.12 oap/bin/check_transcript.py --repo-root . --index --expected-id NNN-a
```

After non-report work is committed, rerun the guard against the committed
tree:

```sh
python3.12 oap/bin/check_transcript.py --repo-root . --revision HEAD \
  --expected-id NNN-a
```

The guard reads exact index/commit blobs and compares them with the worktree
pointer; Git status, stat cache and mtime are not transcript evidence.

## Manifests

[Current governance](governance/MANIFEST.json), the [immutable source
lock](bootstrap-sources.lock.json), the [handoff file
snapshot](BOOTSTRAP-MANIFEST.sha256) and [mutable runtime
state](INSTALLATION.json) are distinct manifests.
BOOTSTRAP-MANIFEST.sha256 is a handoff snapshot, not a permanent freeze of
valid development. INSTALLATION records scoped owned files.

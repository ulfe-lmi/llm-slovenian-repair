# Concentrated OAP infrastructure

Published orders and reports are immutable transcript history; `oap/active` names
the current round. Drafts are in strategic-instructions/initial-orders and private
drafts, never an active queue. Shared standard-library helpers implement
publication, integrity, exact FIFO, SELF, transcript coherence, state/recovery and
audit schema; tests use disposable fixtures and fake boundaries. Use each helper
`--help` and the [runbook](../docs/OAP-RUNBOOK.md).

Before an implementation commit, force-stage the active pointer and verify the
index directly:

    git add -f oap/active
    python3 oap/bin/check_transcript.py --repo-root . --index --expected-id NNN-a

After non-report work is committed, rerun the guard against the committed tree:

    python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id NNN-a

The guard reads exact index/commit blobs and compares them with the worktree
pointer; Git status, stat cache and mtime are not transcript evidence.

Current governance, immutable source lock, handoff file snapshot and mutable runtime
state are distinct manifests. BOOTSTRAP-MANIFEST.sha256 is a handoff snapshot, not
a permanent freeze of valid development. INSTALLATION records scoped owned files.

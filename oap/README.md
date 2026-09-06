# Concentrated OAP infrastructure

Orders/reports directories are empty except .gitkeep. No active exists. Drafts are
in strategic-instructions/initial-orders and private drafts, never an active queue.
Shared standard-library helpers implement publication, integrity, exact FIFO, SELF,
state/recovery and audit schema; tests use disposable fixtures and fake boundaries.
Use each helper --help and the [runbook](../docs/OAP-RUNBOOK.md).

Current governance, immutable source lock, handoff file snapshot and mutable runtime
state are distinct manifests. BOOTSTRAP-MANIFEST.sha256 is a handoff snapshot, not
a permanent freeze of valid development. INSTALLATION records scoped owned files.

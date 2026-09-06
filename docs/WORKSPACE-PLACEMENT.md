# Workspace placement — owner update 2026-09-07

| Purpose | Location |
|---|---|
| Coding checkout | `~/workspace/codex-work/llm-slovenian-repair` |
| Strategic files, drafts, logs, configuration and role homes | `~/workspace/codex-supervision/llm-slovenian-repair` |
| Control and response FIFOs only | `~/.oap-fifos/llm-slovenian-repair` |

The owner explicitly selected this layout after the workspace mount's behavior
was observed. `~/workspace` is Dropbox-backed `fuse.rclone`: it does not support
named FIFOs and does not preserve requested per-file POSIX private modes. Regular
strategic files stay there as requested. Native FIFO directory/files retain
0700/0600; the exact selected strategic subtree uses the sync mount's access
semantics, with ownership, type and symlink checks still enforced. Other paths
retain strict private-mode checks. No mount or global configuration was changed.

This sync mount also rejects hard links and no-replace rename flags. Immutable
publication therefore uses a per-target lock and an existence/content check before
renaming a fully flushed temporary file when hard linking is unsupported. The
guard coordinates local helper processes, not independent machines editing the
same synced file concurrently. OAP's single-host role locks and Git verification
remain required; a changed existing order/backup is still rejected.

The versioned `oap/governance/WORKSPACE-LAYOUT.json` records the explicit roots
and exception. Runtime `OAP_FIFO_HOME` must match the selected layout. Both roles
use its `control.fifo` and `response.fifo`; neither looks for pipe files inside
STRATEGIC_HOME. No FIFO symlinks or empty-file substitutes are installed.

Use the `runtime.env` inside the strategic workspace. It is parsed as
allowlisted data, never sourced as shell code. Setup previews and doctor consume
the same layout. All regular role-home configuration stays under the strategic
workspace; no model/profile/authentication is selected by relocation. Exact OK
framing, no idle model calls, role retention and activation gates are unchanged.

The existing coding `.git`, root `.gitignore` and LICENSE are preserved; normal
commits/pushes update Git metadata through Git. Upstream is
`ulfe-lmi/llm-slovenian-repair`. Use documented interpreter commands (`bash` for
shell helpers, `python3 -B` for Python helpers) on the sync mount. Git retains
executable metadata for native checkouts. This layout update is not operational,
live-model, audit or deployment activation.

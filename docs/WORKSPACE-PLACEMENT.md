# Workspace placement

The coding checkout is `~/workspace/codex-work/llm-slovenian-repair`.
The owner supplied the existing Git repository, root `.gitignore` and `LICENSE`;
the latter two are preserved byte-for-byte. The configured upstream is
`ulfe-lmi/llm-slovenian-repair`. Bootstrap publication does not activate OAP.

On this machine `~/workspace` is a Dropbox-backed `fuse.rclone` mount. A direct
attempt to create a named FIFO failed with EIO, leaving an empty regular file;
a directory requested as 0700 appeared as 0755. That mount cannot satisfy this
bootstrap's strategic-home contract (real FIFOs, 0700 directories, 0600 files).
The incomplete strategic copy was removed after checking that its files were
duplicates; the original strategic workspace remains intact on the local filesystem.

The strategic home therefore remains temporarily at
`~/codex-supervision/llm-slovenian-repair`, pending an owner-selected native local
destination. Its runtime paths can reference this relocated coding checkout.
Do not weaken private-mode or FIFO checks, create fake FIFO files, or relocate
credentials to the cloud mount to bypass the incompatibility. No model, agent,
watcher or service has been activated.

Run scripts using their documented interpreter commands (`bash oap/bin/...sh`
and `python3 -B oap/bin/...py`); this mount's displayed permission bits do not
provide normal per-file POSIX mode control. The repository's executable metadata
is retained for checkouts on native filesystems.

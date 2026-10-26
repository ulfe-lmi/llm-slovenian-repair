# 012-b completion record — scoped corrections and 012-a evidence supersession

Order: 012-b, `oap/orders/012-b-native-migration-completion.md`,
sha256 `b17068812317cd0d687e9f07668efa2a9f00fba4170f21eba8f65adef0b564d2`.
Date: 2026-10-25. Classification: engineering-only completion round for the
named 012-a residuals; no scientific protocol, model, dataset, prompt, or
result change. Accepted governance ref (unchanged, old-accepted law):
`4507cc78e333c0e48226b64266121171b7b8cea8`; candidate governance bytes stay
unchanged and are checked against the pinned 012-a authorization; the
accepted private law is not refreshed before merge.

This record is data-free: no machine roots, credentials, raw text, or private
paths. Logical names (OAP_STRATEGIC_HOME, OAP_FIFO_HOME, REPO_ROOT) and
environment variable names only; the selected machine roots remain versioned
only in `oap/governance/WORKSPACE-LAYOUT.json`, the one versioned record
authorized to contain them.

The superseded document is the immutable published 012-a report,
`oap/reports/012-a-native-migration-and-merged-round-reconciliation.md`
(sha256 `9a6fafb8987771cb6afa9a3d8670cf243e0e7c15eb17d89f57e1de2fb352e015`);
its bytes are preserved exactly, and this record supersedes its overbroad
evidence claims by name below rather than editing them.

## Superseded 012-a evidence claims (corrected here, in order)

1. Publication-guard scope. The 012-a report's credential-scan claim is
   superseded: `publication_guard --root research` observed on the real host
   scans the 6,518 research files only. It does not cover OAP files, reports,
   or all committed artifacts, and it cannot prove universal absence of
   secrets. Any broader absence claim would require a separate actual
   staged-index scan, cited separately; no such claim is made here.
2. Retrospective SHA relabeling. Earlier local full/focused suites ran on
   working-tree candidate bytes (base plus uncommitted edits) and must be
   read as tested-base-plus-dirty-candidate evidence, including the
   interpreter actually used for each stage (some early local runs used the
   host default 3.14 interpreter before the ordered 3.12 environment was
   enforced). They are not relabeled as tests of a later exact commit; the
   final-head CI per published commit is the separate actual proof, reported
   with its own identity.
3. Conflated evidence layers. Three layers are distinct and each proves only
   its own boundary: (a) the real-pane read-only proof (explicit pane
   selection, verified foreground Codex PID/argv/cwd, terminal foreground
   group); (b) the external one-shot FIFO control handoff (one exact OK
   consumed once, outside this model); and (c) the synthetic
   CLI/dispatch/foreground tests (fake `gh`, inert processes, owned tmux
   fixtures, and the owned-group negatives built from inert stubs). A
   fake-driven dispatch test is not an actual existing-pane dispatch
   execution, and no test layer is cited for another layer's claim.
4. Universal operational claims. Carried-forward universals ("every
   verification used 3.12/-B", "no shared /tmp writes", "gh strictly
   read-only with no other network activity", "every negative case proven")
   are superseded: earlier 3.14-based local runs occurred and are retained
   as such; push/PR writes and dependency sync did occur and are the
   authorized publication/verification activity; and negative coverage is
   stated per check (local fixture, copied workspace, or CI) in the 012-b
   report instead of as a universal.
5. Machine roots. The approved machine roots intentionally exist in the
   versioned `oap/governance/WORKSPACE-LAYOUT.json` record (and in the
   private materialized runtime configuration). The 012-a wording suggesting
   their absence from versioned records is superseded: they are versioned
   exactly where the layout record authorizes them. Scoped statement for
   this round: the committed `oap/runtime.env.example` currently contains no
   machine roots, the layout record is the approved versioned location, and
   the private materialized configuration is not versioned; no
   repository-wide absence claim is made without an actual scan.
6. Remote report proof. The normal remote `verify_report` proof published
   for 012-a (open-PR head equality, remote parent, sole-path, content, and
   order-byte checks) remains valid as published. This round invents no
   quarantine classification and no forward-recovery metadata; the 011-e
   merged-tail classification stays post-merge branch publication evidence,
   and the publication proof alone does not establish integration or
   scientific acceptance.

## What 012-b changed (engineering only)

- `oap/bin/source_cache.py`: report-history cache ownership now uses the
  current process UID as the only authority; the fixed host-account lookup is
  removed, with a wrong-owner negative that patches the UID authority.
- `oap/runtime.env.example`: portable schema template — all configuration
  keys present as JSON strings, the five root values explicit placeholders,
  no machine roots, fail-closed parse negatives.
- `scripts/verify_development_baseline.py`: every owned command runs in its
  own POSIX session (pgid == child pid); pipes are read nonblocking through
  a selector with a bounded per-call drain budget; timeout escalation is
  SIGTERM, bounded grace, SIGKILL, bounded reap of the direct child, and a
  bounded drain to EOF; group liveness distinguishes runnable members from
  zombie-only state; only the owned group is ever signaled; a
  bounded-cleanup failure fails the command with a truthful diagnostic while
  TIMEOUT stays a distinct result.
- CI budgets (ordered limits only): application baseline job 15 to 40
  minutes and driver `--command-timeout` 600 to 1800 seconds; OAP bootstrap
  acceptance job 10 to 30 minutes; the short OAP report-history job stays at
  10 minutes.
- `research/` snapshot binding: the historical research-state snapshot is
  validated file-only against the pinned immutable 012-a order (tamper
  detection, block identities, and ancestry of the available current main —
  ancestry, not equality); in copied workspaces without Git history the
  actual-ancestry test is explicitly skipped, and synthetic lineage tests
  cover accept/reject boundaries.
- `research/RESEARCH-STATE.md`: `oap_reports_reviewed` advances to the
  final-report-head value (62; registry entries unchanged at 42); the
  designed implementation-head report-count red clears at the report-only
  commit. Additive data-free section 31 records this round.

## Current verified state (exact, from the 012-b order)

Final 012-a report head `3d8f8148188a5b961dd747edee57c1272b31ac94`:
Research reproducibility PASSED; OAP report history PASSED; OAP bootstrap
acceptance CANCELLED after 10m15s (during tests); Application baseline FAILED
after the driver TIMEOUT at 600 s, with the descendant pytest completing in
771.73 s (794 passed, 58 skipped, one failure — the obsolete example roots).
No earlier implementation-head shorthand (three-red/one-green) is carried
forward. The 012-b CI at the final report head is necessarily
post-publication strategic receipt evidence: the report is written before
publication, cannot claim results of a CI that runs after it, and therefore
states it as PENDING.

## Observed local verification (pre-commit candidate bytes, exact Python 3.12)

Driver contract suite passed, including the real descendant/pipe-retention
timeout and sweep cases, flooding-child bounded timeout and success,
unrelated-session survival, FD-leak release on pipe-allocation failure, and
zombie-only group liveness; split-layout module passed; report-history cache
module passed; research consistency plus synthetic snapshot suites passed.
Real-host doctor (observed during 012-a, premerge; not rerun in this
round): `UNACCEPTED_GOVERNANCE`, expected while candidate governance is
unmerged and the accepted private law is old; the native fixture doctor
positives/negatives prove the layout behavior, and the clean real
accepted-runtime check remains a strategic post-merge/refresh
verification.

## Local environment deviation (disclosed)

During 012-b verification a bare local `uv` invocation recreated the
repository-local `.venv` (the prior one was a broken migrated environment
whose interpreter link no longer existed). No retained original `.venv` was
found after the recreation, and nothing was restored. The git-tracked tree
and the separately preserved literal backslash-named `.venv` residue were
untouched. This is a local environment deviation only: no tracked file,
order, report, gate, or scientific record was changed by it. Verification
afterward uses the ordered Python 3.12 interpreter, owned scratch paths, and
the driver's owned temporary roots; repository-local environments are not
written to by verification commands.

## Preserved

Immutable 012-a report bytes, all historical orders/reports, PR13, the
corpus/scratch untracked residues (never staged), the pinned 012-a
authorization binding, and the owner's existing session homes. No merge or
auto-merge; no 011-e replay; no model calls, live tests, or deployment. The
owner-selected Pandoc structural-parsing runnable proxy remains the next
separately ordered engineering objective and is not implemented by this
round.

# Work report 012-b - Complete native migration, bounded test cleanup and historical-state reconciliation (objective 012, round 2; scoped completion of the named 012-a residuals on the existing PR; foreground-only coding; PR #14 open; branch retained)

```oap-report
{
  "id": "012-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/012-b-native-migration-completion.md",
  "order_sha256": "b17068812317cd0d687e9f07668efa2a9f00fba4170f21eba8f65adef0b564d2",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514",
    "oap/governance/DISTILLATION-MAP.md": "a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7",
    "oap/governance/WORKSPACE-LAYOUT.json": "cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254",
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "publication_commit": "SELF",
  "implementation_head": "53d2f491adf84e4df90c7d02b15665a4e4cdcc1e",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 14,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/14",
  "pr_state": "open",
  "branch": "oap/012-migration-reconciliation",
  "base_sha": "ff08d6e34601f56fecf21eff7d3d3b0e7c68dede",
  "starting_remote_sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-26T00:12:27+00:00",
  "report_written_at": "2026-10-26T00:13:47+00:00",
  "checks": [
    {
      "command": "Requirement 1 / A5 - resume from the exact 012-a publication head; PR/branch identity; no replay, merge or rewrite",
      "result": "PASSED",
      "details": "Round started at the published 012-a report commit 3d8f814 (PR #14 open, head 3d8f814; remote main ff08d6e3). No 012-a replay, no new PR, no merge, no reset/rebase/force-push; PR #13 and all prior orders/reports preserved. Limitation: the later commit-shape assertions are made at the implementation head (separate check).",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head: path census against the ordered scope; prior orders/reports preserved, the new 012-b order/active added; 012-a report bytes; pins",
      "result": "PASSED",
      "details": "Implementation head 53d2f49 (sole parent 3d8f814) changes exactly the 22 authorized paths (two workflow timeout lines, STATUS.md, six directly affected status contracts, GENERATED-FILES, active, source_cache, the new 012-b order, the new 012-b recovery record, runtime.env.example, two OAP test modules, RESEARCH-STATE, three research test files, the driver, the driver contract tests). Prior orders and reports preserved; the 012-a report is byte-identical at the head (sha256 9a6fafb8987771cb6afa9a3d8670cf243e0e7c15eb17d89f57e1de2fb352e015); all 173 GENERATED-FILES pins verify against committed bytes; the committed whitespace suite passes 6/6 at the head (both authorized bases plus the fail-closed negatives).",
      "sha": "53d2f491adf84e4df90c7d02b15665a4e4cdcc1e",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 2 / A1 - source-cache ownership: current process UID the only authority; no host-account lookup; protections retained",
      "result": "PASSED",
      "details": "oap/bin/source_cache.py drops the fixed host-account lookup; the current process UID is the only ownership authority at both call sites, with the documented authority paragraph. Focused module 21/21 on Python 3.12, including the wrong-owner negative (a simulated unrelated account cannot redirect authority) and the retained symlink/hardlink/type/hash/inventory/lifecycle protections. Limitation: candidate working tree at base 3d8f814 (dirty-candidate bytes; committed bytes identical, confirmed by the commit-shape check).",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 3 / A2 - portable runtime.env.example: exact schema, placeholder roots, no machine roots in the example, fail-closed negatives, parsed selected-layout substitution",
      "result": "PASSED",
      "details": "All 25 keys present as JSON strings; the five root values are explicit placeholders and no example value embeds a machine root; the obsolete example-equals-this-host assertion is replaced by schema positive, parsed-value substitution of the selected fixture layout (no placeholder surviving in any parsed value), and fail-closed negatives (missing/unknown/duplicate keys, syntax, non-string value, escaped newline). Split-layout module 9/9, preserving role-home separation, real FIFOs, the historical sync exception and all ownership/path checks. Limitation: candidate tree at base 3d8f814 as above.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 4 / A3 - historical snapshot bound to the pinned immutable 012-a order: exact identities, ancestry of available current main (not equality), tamper/older/foreign rejections",
      "result": "PASSED",
      "details": "New file-only contract validates the machine-block identities against the pinned 012-a order digest (computed before any mutation), and requires the snapshot to be an ancestor of the available current main where Git history exists; the actual-ancestry test is explicitly skipped in copied workspaces without history. Synthetic suite: descendant main accepted, equality accepted, binding-only, tampered order, missing order, unauthorized older snapshot, foreign lineage and future snapshot rejected - 8/8; focused consistency plus synthetic 19/19. The 007-o branch/PR/quarantine bindings and all scientific values are retained. Limitation: candidate tree at base 3d8f814 as above.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 5 / A4 - driver bounded cleanup: owned POSIX sessions, nonblocking selector pipe reads with per-call drain budget, bounded SIGTERM-to-SIGKILL-to-reap-to-drain, zombie-aware liveness, owned group only, truthful cleanup failure reporting",
      "result": "PASSED",
      "details": "run_command rewritten as described in the order: per-command session (pgid == child pid), immediate pipe-fd ownership registration, bounded per-call drain (a flooding child cannot starve the deadline), bounded escalation and reap, bounded drain to EOF, zombie-only groups not reported as surviving, only the owned group signaled, and a bounded-cleanup failure that fails the command (TIMEOUT stays distinct). Real-subprocess contract cases: child plus grandchild retaining stdout/stderr across a 1 s timeout (bounded return, no owned survivors via /proc marker scan), parent exit rc 0 with a pipe-retaining descendant (swept, exact success record), flooding child bounded at the deadline and a 20 MB flooding success, unrelated sentinel in its own session preserved, pipe-allocation EMFILE with the FD table returning to baseline, and zombie-only group liveness. Focused driver contract 13/13 plus the copied-workspace runner case 1/1; Ruff clean on changed driver/tests. Limitation: candidate tree at base 3d8f814 as above.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 6 - ordered CI timeout limits only: application job 15 to 40 minutes and driver 600 to 1800 seconds; OAP bootstrap acceptance 10 to 30 minutes; report-history job unchanged",
      "result": "PASSED",
      "details": "Both workflow diffs contain only the ordered timeout lines; every trigger, step, pin, candidate-review step, protected-source diff and whitespace/transcript check is otherwise byte-identical. The prior 600-second timeout is not relabeled as passed. Limitation: candidate tree at base 3d8f814; the committed limits take effect in the implementation-head CI check.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 7 / A5 - explicit supersession of the named 012-a evidence overclaims in the new data-free recovery record; 012-a report bytes preserved",
      "result": "PASSED",
      "details": "oap/recovery/012-b-native-migration-completion.md names and corrects each superseded claim (publication-guard scope: 6,518 research files only, not OAP/report artifacts or universal secret absence; dirty-candidate run labels with actual base/interpreter; the three distinct evidence layers with the inert-stub negatives in the synthetic layer; removed unsupported universal network/temp/exhaustive-test claims; approved machine roots versioned in the WORKSPACE-LAYOUT record with a scoped example statement and no repository-wide absence claim; the valid normal remote report proof with no invented quarantine or forward-recovery metadata) and records the current verified state, observed local verification, the disclosed local .venv deviation, and what is preserved. The 012-a report bytes are unchanged and its PARTIAL record is not rewritten. Limitation: candidate tree at base 3d8f814; byte identity at the head is asserted in the commit-shape check.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 8 - directly affected docs, additive data-free RESEARCH-STATE section, and report counters under the report-only convention",
      "result": "PASSED",
      "details": "Updated only docs/OAP-RUNBOOK.md, docs/WORKSPACE-PLACEMENT.md, docs/DEVELOPMENT.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md and STATUS.md where directly affected; RESEARCH-STATE gains only data-free section 31 and the oap_reports_reviewed advance to the final-report-head value 62 (registry_entries 42 and all scientific fields unchanged); the designed implementation-head count red (62 vs 61 files) is locally counted to clear at this report commit (62 = 62). Limitation: candidate tree at base 3d8f814 as above.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Verification - committed-base and candidate pre-commit checks (Python 3.12, -B, owned scratch, umask 022)",
      "result": "PASSED",
      "details": "At committed base 3d8f814: check_whitespace.py against the accepted base PASSED (three historical 007 incident paths only). On the candidate tree: working-tree and index git diff --check clean; table regeneration --check PASS; publication_guard --root research PASS over the 6,520 research files (cited with that actual scope, not as a repository-wide scan); pinned 012-a candidate review (order digest e320df8e, accepted ref 4507cc78) VALID, proving candidate governance bytes unchanged this round. Limitation: candidate checks ran at base 3d8f814 with uncommitted 012-b bytes; some early local helper runs in this round used the host 3.14 interpreter before the ordered 3.12 environment was enforced and are labeled as such in the recovery record.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Verification - native baseline driver, owned persistent temp parent, --command-timeout 1800, Python 3.12, REPAIR_ALLOW_LIVE_TESTS=NO",
      "result": "PASSED",
      "details": "Native baseline driver with owned persistent temp parent under the strategic home, --command-timeout 1800, Python 3.12 -B, REPAIR_ALLOW_LIVE_TESTS=NO: all 13 ordered stages PASSED (uv lock --check; frozen dependency sync; focused contract tests; full pytest; Ruff; mypy; OAP unittest discovery; sdist and wheel build; wheel selection; fresh offline venv; offline runtime-only frozen sync; offline wheel installation with dependencies; offline runtime import and metadata), cleanup PASSED, DRIVER_EXIT=0. The earlier interrupted detached attempt is preserved as NOT COMPLETE evidence and is superseded by this run. Limitation: the driver copies the candidate working tree (base 3d8f814 plus uncommitted 012-b bytes) into its owned temporary workspace; the run log is the result record - bounded, control-free, path-redacted failure diagnostics plus per-command result lines, not full successful-test stdout.",
      "sha": "3d8f8148188a5b961dd747edee57c1272b31ac94",
      "publication_head_claim": false
    },
    {
      "command": "Verification - implementation-head CI after the implementation push (observed jobs recorded; remainder PENDING at publication)",
      "result": "PENDING",
      "details": "Observed at approximately 00:12Z after the implementation push 53d2f49: OAP report history PASSED (observed); Research reproducibility FAILED exactly at the designed report-count assertion (AssertionError 62 != 61 in test_registry_and_report_counts; 409 tests, 1 failure, 53 skipped) - the designed red this report commit clears; Application baseline and OAP bootstrap acceptance were in_progress at publication and are not claimed here. The full four-check CI at the final report head remains the mandatory strategic merge gate (see A6).",
      "sha": "53d2f491adf84e4df90c7d02b15665a4e4cdcc1e",
      "publication_head_claim": false
    },
    {
      "command": "A6 - CI at the final report head (post-publication)",
      "result": "PENDING",
      "details": "Necessarily post-publication strategic receipt evidence: this report is written before publication and states it PENDING rather than claiming future results. The designed research report-count red at the implementation head (62 vs 61) is arithmetically cleared by this report commit (locally counted 62 = 62 before committing). No merge recommendation is made here; merge remains a strategic decision requiring all four final-head CI checks observed green.",
      "sha": "53d2f491adf84e4df90c7d02b15665a4e4cdcc1e",
      "publication_head_claim": false
    }
  ],
  "implementation": "One implementation commit on oap/012-migration-reconciliation (sole parent 3d8f814) plus this report-only commit. The implementation commit changes exactly the 22 authorized paths (commit-shape check): source_cache current-process ownership, the portable example, two OAP test modules, the new research snapshot contract plus synthetic suite with the updated consistency test, the driver rewrite plus seven real-subprocess contract cases, the two workflow timeout lines, RESEARCH-STATE section 31 plus the counter advance, six directly affected status contracts, the new data-free recovery record, and the affected GENERATED-FILES pins. No governance, PLAN/ARCHITECTURE/CRITICAL, source-lock or bootstrap-seed change; candidate governance bytes unchanged against the pinned 012-a authorization; prior orders and reports preserved, with the new 012-b order and active pointer added.",
  "documentation": "The new data-free recovery record oap/recovery/012-b-native-migration-completion.md (supersession of the named 012-a claims, current verified state, observed local verification, disclosed local .venv deviation, preserved items), the additive RESEARCH-STATE section 31, and the six directly affected status contracts (residuals resolved, portable template, bounded driver contract, raised budgets, 012-b status, and the next separately ordered Pandoc structural-parsing runnable proxy objective - engineering scope, not implemented).",
  "criteria": "A1 SATISFIED (observed): cache lifecycle passes with current-process ownership and the meaningful negatives retained (21/21 focused; CI as recorded). A2 SATISFIED (observed): portable example and selected-configuration contract pass positive and negative checks without embedding machine roots in the example. A3 SATISFIED (observed): the pinned snapshot accepts a normal descendant main and equality and rejects tampered order, missing order, unauthorized older identities, foreign and future lineage (19/19 focused; copied workspaces file-only with the ancestry test explicitly skipped). A4 SATISFIED (observed): the real pipe-retention timeout and parent-exit cases return within finite bounds, clean the owned descendants, preserve the unrelated sentinel, and keep success/nonzero/TIMEOUT semantics. A5 SATISFIED (observed): protected history, reports and scientific bytes unchanged at the head; the new record explicitly corrects the named overstatements. A6: implementation-head CI recorded as observed where observed (OAP report history PASSED; Research reproducibility at the designed 62-vs-61 count red; Application baseline and OAP bootstrap acceptance in progress at publication, not claimed); final report-head CI PENDING post-publication; no merge recommendation.",
  "negative_paths": "Wrong-owner cache authority redirected by a simulated unrelated account: rejected. Placeholder surviving into a parsed configuration value: rejected. Invalid configurations (missing/unknown/duplicate keys, syntax, non-string value, escaped newline): fail closed. Tampered or missing 012-a order, unauthorized older snapshot, foreign lineage, future snapshot: rejected. Flooding child starving the deadline: bounded per-call drain, proven. Descendant pipe retention across timeout or parent exit: owned-group sweep, no survivors. Unrelated session signaled: preserved. Pipe-allocation failure: descriptors released, FD table restored. Zombie-only group: not reported surviving. The old 600-second timeout is not relabeled as passed.",
  "boundary_fidelity": "Fakes stay at the external boundary: the driver cases use real children, real pipes and real /proc scans (no fake command boundary); the candidate review binds to the literal pinned order digest and accepted ref. No synthetic CI, no fake live success, no check disabling, no broad catches. Evidence layers stay distinct and are not cited for each other: real-host observations (pre-012-b doctor, CI receipts), candidate-tree focused suites (base 3d8f814 plus uncommitted bytes, labeled), and implementation-head CI (observed per job).",
  "setup": "Machine-local rebuilt Python 3.12 (3.12.15) with -B and PYTHONDONTWRITEBYTECODE=1, REPAIR_ALLOW_LIVE_TESTS=NO, an owned persistent scratch under the strategic home as TMPDIR and as the baseline --temp-parent, CI-parity umask 022, full logs and real exit statuses in that owned scratch. The driver refuses a repository-local temp parent and keeps its project environment, caches and builds inside its owned temporary root. After the disclosed one-time local .venv recreation deviation (see limits), the subsequent named checks in this round used the external Python 3.12 interpreter and owned scratch paths and did not write to a repository-local environment.",
  "privacy": "No raw private text, credential, endpoint value, bearer string, or private absolute path appears in this report or the new recovery record; the approved layout record holds the versioned machine roots, the current committed example contains no roots, and no repository-wide absence claim is made without a scan; private receipts are cited by logical name. The publication scan is cited with its actual --root research scope (6,520 files), not as a repository-wide absence proof.",
  "limits": "Candidate-tree checks (focused modules, pre-commit checks, native baseline) ran at base 3d8f814 with uncommitted 012-b bytes; committed-bytes identity is established by the commit-shape check (22-path census, 012-a report hash, 173/173 pins, whitespace 6/6 at the head). Some early local helper runs in this round used the host Python 3.14 interpreter before the ordered 3.12 environment was enforced; they are labeled as such in the recovery record and are not cited as product evidence. One bounded local deviation: a bare local uv invocation recreated the git-ignored repository-local .venv; no retained original was found, nothing was restored, and no tracked file or scientific record was affected (disclosed in the recovery record). The driver run log is the result record - per-command result lines plus bounded failure diagnostics - not full successful-test stdout. Implementation-head CI was observed for 2 of 4 jobs at publication (1 PASSED, 1 designed count red, 2 in progress); final report-head CI is PENDING post-publication.",
  "human_gates": "The owner's 2026-10-25 migration and foreground-only authorization, the owner-selected Pandoc proxy decision (next separately ordered objective, not executed), the single externally consumed 012-b control frame, and the completed owner archive restoration (integrity-verified; no credential activation) bound this round. No new human or milestone gate; merge remains a strategic decision requiring all four final-head CI checks observed green.",
  "scope": "Executed exactly the bounded order: resume at the 012-a head without replay or rewrite; current-process cache ownership; portable example and selected-configuration contract; pinned historical snapshot with ancestry semantics; bounded driver cleanup with real subprocess/pipe tests; the ordered CI timeout limits only; explicit supersession of the named 012-a overclaims; directly affected docs, the additive RESEARCH-STATE section, accurate counters and pins. No Pandoc/proxy change, no research replay or evaluation, no model calls, no deployment, no merge.",
  "resources": "Owned scratch (preserved): focused module logs, driver contract log, whitespace/tables/publication-guard/candidate-review logs, and the native baseline driver run log (the result record: per-command result lines plus bounded failure diagnostics) with its real exit status; the earlier interrupted detached attempt and its temp tree are preserved as NOT COMPLETE evidence. Implementation-head CI job logs are preserved privately by the CI receipt; the final report-head CI receipt remains post-publication.",
  "result_summary": "012-b is complete and published on PR #14 (branch retained, no merge). The two named 012-a engineering residuals are fixed and focused-verified (current-process cache ownership; portable configuration example); the baseline driver has a bounded, session-isolated, fail-truthful cleanup contract with real subprocess/pipe tests; the research-state snapshot is bound to the pinned immutable 012-a order with available-current-main ancestry semantics; only the ordered CI timeout limits were raised; and the new data-free recovery record explicitly supersedes the named 012-a evidence overclaims while preserving the immutable 012-a report bytes. The native baseline passed 13/13; the implementation head 53d2f49 is verified (22 authorized paths, 012-a report byte-identical, 173/173 pins, whitespace 6/6); implementation-head CI shows OAP report history PASSED and the designed 62-vs-61 report-count red (cleared by this report commit) with the two long jobs in progress at publication. Final report-head CI (all four checks) is PENDING as post-publication strategic receipt evidence. No scientific protocol, model, dataset, prompt, or result changed; no merge."
}
```

## Short factual summary

012-b completed the two named 012-a engineering residuals (report-history
cache ownership now uses the current process UID only; the committed
configuration example is a portable template with no machine roots),
strengthened the baseline driver to a bounded, session-isolated,
fail-truthful cleanup contract with real subprocess/pipe tests, bound the
research-state historical snapshot to the pinned immutable 012-a order with
available-current-main ancestry semantics, raised only the ordered CI timeout
limits, and published the new data-free recovery record that explicitly
supersedes the named 012-a evidence overclaims while preserving the immutable
012-a report bytes. The 012-a PARTIAL record is historical and was not
rewritten. One bounded local deviation (a repository-local `.venv` recreated
by a local uv invocation; no retained original found; nothing restored; no
tracked file or scientific record affected) is disclosed in the recovery
record. No scientific protocol, model, dataset, prompt, or result changed; no
model calls, no live tests, no deployment, no merge. The owner-selected
Pandoc structural-parsing runnable proxy remains the next separately ordered
engineering objective.

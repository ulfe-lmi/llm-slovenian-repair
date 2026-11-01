# Work report 027-b — Preserve the issued order and close the exact whitespace recovery contract

**Result: COMPLETE** — the closed-4 fail-closed whitespace contract is enforced and passes at both
accepted bases with all ordered evidence truthful; the final report-head CI at the future SELF commit
remains pending, and this report is held for root exact-byte approval before the canonical sole-path
SELF commit, push, remote verification and ONE response. No canonical publication has been made.

Round 027-b (objective 027, round b) is the same-PR correction following the truthful FAILED 027-a
report: the accepted-base whitespace checker now tolerates exactly the three pinned historical 007
diagnostics plus the root-authored trailing space at line 11 of the issued 027-a order (issued bytes
preserved exactly), and the special forward-recovery merge is bound to its exact ancestry, ordered
parents, tree delta and historical blobs. Branch `oap/027-repair-validation` from accepted main
`d39f629dabdb635a3b02fabb6840122cc8d181a2`; PR 29 OPEN at implementation head
`1c79d928534eacf567ab862a897122429013107e`.

## Order identity and the closed four

- Issued immutable FINAL order: `oap/orders/027-b-preserve-issued-order-and-whitespace-contract.md`,
  sha256 `b2ccdef752dff1c8acaac8fa369bb54060e909331ada55a65ce755250571b370` (18865 bytes), committed
  byte-exact as part of the single 027-b implementation commit.
- Fourth exact incident (R2): `oap/orders/027-a-repair-validation.md` line 11 "trailing whitespace." -
  original introduction `d572b19c86a555ae3e8a4a8bbb99da5bd39a68ea`, current blob
  `8f9def83edfa98d66d8012557b521d3d392c25d9`, sha256
  `d640fb360e55b80649c83d207e9c21e47f4b42223e6a012e46b7800bc4ed8012`, 24341 bytes with the one
  ASCII space preserved; placed at Git's actual diagnostic position between the 007-f and 007-d
  diagnostics (derived from the real diff order, not appended by guess).
- Recovery binding (R3): merge `73f9f3d10cc602781f8a49e22a7dd342165ea8d9` required as ancestor,
  exact ordered TWO parents [`4e601d31ccce7fa2f7652e67af524bb95c761078`,
  `db20450c3dd4ad93a559613c704a9fac1c625298`] compared as a full header, tree delta against the first
  parent limited to the order file, merge order blob equal to the issued original, original
  introduction's own order blob and content bound, normalized introduction
  `85826fd0c5a15f6aa883001b412cdf0259de7dfa` bound to blob
  `6f2690ba42d1c92589491942557b40731c3b2dae` (sha256
  `ca0795f60adf1d5be4036a3d875d51885281b504c12cad07135ad3ab32ee2a29`, 24340 bytes - preservation
  evidence, never the authorized source); default-path introductions [d572], full-history
  introductions [d572, 858].
- Historical context (not re-litigated): the 027-a truthful FAILED report (sole-path SELF e157a40,
  36521 B / `5defc5a44d34a649f1ecc31455bf0442211b5731aa79fffd8d5864bb3ca7e05b`, REMOTE-verified, ONE
  response received) and its Bootstrap CI failure - exactly two whitespace subcases with
  DIAGNOSTIC_SET_MISMATCH at both bases (Research reproducibility and OAP report history succeeded;
  Application baseline also failed on those same subcases) - remain the historical record for
  round a; this round closes that actual failure without touching any A byte.

## Changes (allowlist)

- `oap/bin/check_whitespace.py` (final sha256 `2b7ee027`): closed-4 incident set with the fourth
  incident at its actual diagnostic position; `_verify_recovery` binding the merge to full parent
  header, first-parent tree delta, merge blob, original-introduction blob/content, normalized
  introduction blob/content and full-history introductions; docstring now states the closed four;
  baseline I001 import-ordering correction only.
- `oap/tests/test_whitespace.py` (final sha256 `2c02202b`): original six actual-Git tests preserved
  (positive now asserts the exact 4 diagnostics); five new fail-closed cases covering the issued-order
  trim, deletion/re-addition, missing lineage, the appended third parent (exact [73, 4e, db, D39]
  fixture header asserted before the CLI) and the substituted original-introduction blob; nested
  tree-swap helper walks oap/orders level by level; fixture-only git replace refs deleted after each
  case.
- `docs/DEVELOPMENT.md` (+31 lines): the bounded 027-b operational note (pins, authority-over-cosmetic
  rationale, rejection of additional/drifting incidents, strategic prospective-order whitespace
  qualification as a strategic review step).
- `research/RESEARCH-STATE.md`: oap_reports_reviewed 79 -> 80 only.
- `oap/orders/027-b-preserve-issued-order-and-whitespace-contract.md`: issued order committed
  byte-exact; `oap/active`: 027-a -> 027-b.

## Preserved failed / interim epochs (never relabelled)

- `027b-root-first-exact-history-proof-review.json` (03:21Z): candidate guard 04edd535 accepted BOTH
  of root's concrete negative cases (an appended third parent via a `header[:3]` prefix comparison, and
  a substituted original-introduction blob never bound) - fixed in the 2b7ee027 guard and
  independently re-proven by root.
- `027b-root-second-candidate-focused-test-review.json` (03:45Z): root's whole-module run on an
  immutable copy - 11 tests in 9.368 s, exit 1, the one failure inside the new fixture's
  non-recursive `ls-tree` helper (a fixture-only defect, corrected in the final test bytes); this
  epoch is preserved as a failure, never relabelled as a focused pass.
- The interim full OAP (201 tests OK, 1372.982 s, private log full-oap-final.log) ran at the
  pre-gap-fix bytes and is superseded by the final 203-test run; both epochs are preserved privately.
- The 027-a FAILED report, its exact bytes, and its Bootstrap CI failure (two whitespace subcases)
  remain published historical evidence; nothing here rewrites or supersedes them.

## Shared checks at this head

At `1c79d928534eacf567ab862a897122429013107e`: whitespace checker CLI PASSED with the exact 4
diagnostics at BOTH accepted bases; governance accepted-runtime valid; transcript (index and literal
HEAD) valid with active 027-b; report-history require-manifest valid (report_count 80); git diff
--check clean. Research state consistency is the single truthful FAILED row: the counter (80) stands
ahead of the 79 counted report files by design until this report exists. Final report-head CI (the
four required checks) remains PENDING and is not claimed.

## Scope, limits and gates

Exactly the six ordered non-report paths in one implementation commit (sole parent e157a40) plus this
held seventh report path; all 49 concept Python, the 16 governance identities, the 173-path manifest
and every prior order/report byte frozen; the three untracked roots preserved; PR 13 untouched. No
MVP/linguistic-quality/packaged-library/ICA/deployment acceptance is claimed; the owner's
no-separate-human-evaluation-dataset decision (excluded, not deferred, not merely optional) does not
waive the retained fresh independent software/operating-path audit or the separately
owner-authorized deployment/exposure. Coding never merges or enables auto-merge; root verifies the
publication and all four final SELF-head CI before any conditional development merge.

```oap-report
{
  "id": "027-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/027-b-preserve-issued-order-and-whitespace-contract.md",
  "order_sha256": "b2ccdef752dff1c8acaac8fa369bb54060e909331ada55a65ce755250571b370",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "313d77900f9bbf1c974e76ea3f546083b117eeaac5f5fc2e964e77b3c19b9ccc",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "d10f9a0d673bd84f91a27f4f24b8505bf966e3eb5825bdfbd9404e1385b6681e",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "db624bb41b34d8263bc5745083d86e7db5bb8907816cd8725871e7225eb6ce9d",
    "oap/governance/DISTILLATION-MAP.md": "eeaf84b26e39c1cadd5d375d8d40f21b62bcf607a18472cd426d13656d5d3e62",
    "oap/governance/WORKSPACE-LAYOUT.json": "90f8b69f4054dffb4d93313da54841ccfddafdca511b86604765d51b63631d16",
    "oap/prompts/coding-round.md": "c682b1bbe016429bf4712a4174ae5ca4ec8b78ab36ebbc2c9b3ce625d83d3ffd",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "ba91f90ef1a8692472661900f1f91faacafa1a47954222c0e75e2f9d9752f6ae",
    "oap/strategic-instructions/AGENTS.md": "c08be7ea6f50ff218948e06ca942d40ce370b041f3580035a4f8ae8ef37c8221",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "83c87a5277ca798609422927e47caa2babab2cf555824813cbbe7f4ac2531ea5",
    "oap/strategic-instructions/strategic_model_init_material.md": "ac972d8e5fcd58b263df11d044aafed9fb1017d2173157d829fbc2953a1ba3b6"
  },
  "publication_commit": "SELF",
  "implementation_head": "1c79d928534eacf567ab862a897122429013107e",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 29,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/29",
  "pr_state": "open",
  "branch": "oap/027-repair-validation",
  "base_sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
  "starting_remote_sha": "e157a40cf26fb4d1096c2cf75b80b4a1421c4ddb",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-01T04:19:12.726834+00:00",
  "report_written_at": "2026-11-01T04:22:21.937815+00:00",
  "checks": [
    {
      "command": "Focused actual-CLI whitespace module (test_whitespace.py, 11 tests) at the final stable bytes",
      "result": "PASSED",
      "details": "11/11 OK in 9.780 s at literal execution head e157a40 with the dirty-2 final bytes (checker 2b7ee0272d2f327d653e04a02ae2ff0994b026e4bf0446ac50d8d1da8b16d795, test 2c02202b5aee25fd055defad7befd9db8e67736357bd3731bc08bcccc450c13b); all 49 concept Python at the tested epoch byte-equal to the committed head 1c79d92 (committed equivalence proven separately, not by execution at a later commit). Root independently ran the whole module on an immutable copy at 03:45Z (11 tests, one fixture-only nested-tree helper failure, receipt 027b-root-second-candidate-focused-test-review.json); that interim failure is preserved and superseded by this final byte.",
      "sha": "e157a40cf26fb4d1096c2cf75b80b4a1421c4ddb",
      "publication_head_claim": false
    },
    {
      "command": "Final full OAP suite (unittest discover -s oap/tests) at the tested epoch bytes",
      "result": "PASSED",
      "details": "203 tests OK in 1331.587 s, exit 0 (private log full-oap-final-stable.log), executed at literal execution head e157a40 with the dirty-2 final bytes; the earlier 201-test interim run (1372.982 s, full-oap-final.log) predates the two gap-fix tests and is preserved as superseded evidence; no product 747 rerun for the frozen 49; committed 49-file equivalence at 1c79d92 proven separately.",
      "sha": "e157a40cf26fb4d1096c2cf75b80b4a1421c4ddb",
      "publication_head_claim": false
    },
    {
      "command": "Strict mypy (exact two changed Python files) and Ruff at the final bytes",
      "result": "PASSED",
      "details": "Fresh byte-identical flat shadow with the minimal ordered config (python_version 3.12, strict true, follow_imports silent), fresh private cache: Success - no issues found in 2 source files; Ruff check --no-cache: All checks passed (the only baseline finding was I001 import ordering in each file, the one correction R1 allows). Executed at literal execution head e157a40 with the final dirty-2 bytes.",
      "sha": "e157a40cf26fb4d1096c2cf75b80b4a1421c4ddb",
      "publication_head_claim": false
    },
    {
      "command": "Root independent actual-CLI guard proof (both accepted bases plus both concrete negative cases)",
      "result": "PASSED",
      "details": "027b-root-second-candidate-exact-history-proof-review.json (2026-11-01T03:47:35Z): corrected guard 2b7ee0272d2f327d653e04a02ae2ff0994b026e4bf0446ac50d8d1da8b16d795 passes both accepted bases with the exact 4 diagnostics and rejects the real appended-third-parent fixture [73f9f3d, 4e601d3, db20450, d39f629] and the real substituted original-introduction blob with RECOVERY_LINEAGE_MISSING in each case; all git replace mutations were fixture-only inside disposable clones and deleted after each case; actual-CLI guard proof only, not final-source or CI acceptance.",
      "sha": "e157a40cf26fb4d1096c2cf75b80b4a1421c4ddb",
      "publication_head_claim": false
    },
    {
      "command": "Checker CLI at both accepted bases at the implementation head",
      "result": "PASSED",
      "details": "oap/bin/check_whitespace.py with --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da and with --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a, --revision HEAD: both PASSED with diagnostics 4 and incident order 007-e, 007-f, 027-a order, 007-d, at literal head 1c79d928534eacf567ab862a897122429013107e.",
      "sha": "1c79d928534eacf567ab862a897122429013107e",
      "publication_head_claim": false
    },
    {
      "command": "Shared OAP helper checks at the implementation head",
      "result": "PASSED",
      "details": "At 1c79d92: governance accepted-runtime at trusted 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (structure valid); transcript index mode and literal HEAD revision mode both valid (active 027-b, latest 027-b, embedded report history valid, report_count 80); report-history require-manifest valid; git diff --check and git diff --cached --check clean; prospective changed-source whitespace: the committed six-path delta carries only the pinned fourth incident (enforced by the checker row above), and the pending report file is checked with git diff --check before its commit.",
      "sha": "1c79d928534eacf567ab862a897122429013107e",
      "publication_head_claim": false
    },
    {
      "command": "Research state consistency (tests and count) at the implementation head",
      "result": "FAILED",
      "details": "test_research_state_consistency: 11 tests, 10 ok, test_registry_and_report_counts FAIL with 80 != 79 - the ordered 79 -> 80 counter increment for the actual additional B report stands ahead of the 79 counted report files by design until this report exists (the expected pre-report red, not a data error); registry_entries 42 and frozen_report_history_incidents 2 pass. Recorded truthfully as FAILED at this head; it is expected to clear only at the report commit.",
      "sha": "1c79d928534eacf567ab862a897122429013107e",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape, allowlist, and committed 49-file equivalence at the implementation head",
      "result": "PASSED",
      "details": "Single implementation commit 1c79d928534eacf567ab862a897122429013107e, sole parent e157a40cf26fb4d1096c2cf75b80b4a1421c4ddb, exactly the six ordered non-report paths (checker, focused test, docs/DEVELOPMENT.md, research/RESEARCH-STATE.md one-line counter, the new issued order file, oap/active); staged delta git diff --check clean; all 49 concept Python at this head byte-equal to the tested epoch (private source maps record the pre-fix 04edd535/c729c0e5, the post-fix 2b7ee027/2c02202b and the committed map).",
      "sha": "1c79d928534eacf567ab862a897122429013107e",
      "publication_head_claim": false
    },
    {
      "command": "PR 29 observed at the current head",
      "result": "PASSED",
      "details": "OPEN, head 1c79d928534eacf567ab862a897122429013107e after the forward push e157a40..1c79d92 (no force); machine-recorded remote observation at 2026-11-01T04:19:12.726834+00:00 (private receipt pr29-observation-1c79.json); the title and body were refreshed to state the 027-b implementation head, the published 027-a FAILED report, and the held 027-b report without implying acceptance.",
      "sha": "1c79d928534eacf567ab862a897122429013107e",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (the four required checks)",
      "result": "PENDING",
      "details": "Application baseline, Research reproducibility, OAP bootstrap acceptance and OAP report history at the future SELF report head remain PENDING; the designed research count red (80 versus 79) is expected to clear at that commit, but later workflow steps are not pre-proven and no future SELF check is claimed passed. Root independently verifies the publication and all four final SELF-head CI before any conditional development merge; coding does not merge.",
      "sha": "1c79d928534eacf567ab862a897122429013107e",
      "publication_head_claim": false
    }
  ],
  "implementation": "oap/bin/check_whitespace.py (2b7ee0272d2f327d653e04a02ae2ff0994b026e4bf0446ac50d8d1da8b16d795): the fail-closed accepted-base whitespace checker now enforces the closed four: the three pinned historical 007 incidents preserved exactly (same paths, lines, messages, introductions, blobs, hashes, sizes and failure conditions) plus the fourth incident - the root-authored trailing space at line 11 of the issued 027-a order (blob 8f9def83edfa98d66d8012557b521d3d392c25d9, sha256 d640fb360e55b80649c83d207e9c21e47f4b42223e6a012e46b7800bc4ed8012, 24341 bytes, introduced at d572b19c86a555ae3e8a4a8bbb99da5bd39a68ea) - inserted at Git's actual diagnostic position (derived, not guessed), between 007-f and 007-d. The special forward-recovery merge 73f9f3d10cc602781f8a49e22a7dd342165ea8d9 is bound as an ancestor of the checked revision with its exact ordered TWO-parent header compared in full (an appended third parent fails), a tree delta against the first parent limited to the order file, the merge order blob equal to the issued original, the original introducing commit's own order blob and content bound to the incident (root-found gap), the unauthorized normalized introduction 85826fd0c5a15f6aa883001b412cdf0259de7dfa bound to Git blob 6f2690ba42d1c92589491942557b40731c3b2dae (sha256 ca0795f60adf1d5be4036a3d875d51885281b504c12cad07135ad3ab32ee2a29, 24340 bytes, preservation evidence never the authorized source), and full-history additions limited to [d572, 858] while the default path lists d572 alone. Only the harmless baseline Ruff import-ordering correction (I001) was applied to the two edited Python files. oap/tests/test_whitespace.py (2c02202b5aee25fd055defad7befd9db8e67736357bd3731bc08bcccc450c13b): the original six actual-Git tests preserved (the positive now asserts the exact 4 diagnostics) plus five new fail-closed cases: issued-order line-11 trim (INCIDENT_BLOB_MISMATCH), issued-order deletion and re-addition with identical bytes (INCIDENT_BLOB_MISMATCH then RECOVERY_LINEAGE_MISSING), missing recovery lineage (fixture update-ref), an appended third recovery parent whose exact [73, 4e, db, D39] fixture header is asserted before the actual CLI (RECOVERY_LINEAGE_MISSING; reproduces the original prefix-bug case), and a substituted original-introduction blob via a fixture-local commit-tree with the same parents, identities and message plus git replace (RECOVERY_LINEAGE_MISSING); the nested tree-swap helper walks the oap/orders path level by level. Every git replace ref and synthetic commit exists only inside the disposable per-test clone and is deleted after each case.",
  "documentation": "docs/DEVELOPMENT.md: one bounded 027-b operational note recording the exact four immutable incident pins and the recovery pins (merge, ordered parents, original and normalized introductions and blobs, normalized content hash), the rationale of preserving authority over cosmetic cleanup, the rejection of all additional or drifting incidents, and the strategic prospective-order whitespace qualification as a strategic review step before immutable publication (not a claim that the unchanged publisher performs it). research/RESEARCH-STATE.md: oap_reports_reviewed 79 -> 80 only, for the actual additional B report (registry_entries 42 and frozen_report_history_incidents 2 unchanged). oap/orders/027-b-preserve-issued-order-and-whitespace-contract.md: the issued immutable FINAL order committed byte-exact (b2ccdef752dff1c8acaac8fa369bb54060e909331ada55a65ce755250571b370, 18865 bytes). oap/active: 027-a -> 027-b.",
  "criteria": "A1 SATISFIED (observed): the exact issued A bytes and history are preserved (issued d640/24341 restored under merge 73f9f3d; the original chain retained under refs/oap-preserved/027-a-original-db20450) and the narrow fixed-4 contract is enforced at the actual workflow CLI at both accepted bases (PASSED, exact 4 diagnostics in Git's actual order) with all historical pins unchanged. A2 SATISFIED (observed): positive and negative actual-Git tests prove exact acceptance and fail-closed rejection (focused module 11/11 at the final bytes; the two root-reproduced negative cases - the appended third parent [73, 4e, db, D39] and the substituted original-introduction blob - now have versioned tests and were independently rejected by root's actual CLI per 027b-root-second-candidate-exact-history-proof-review.json); strict2 and Ruff2 clean at the final bytes; the full OAP suite 203 tests OK in 1331.587 s at the tested epoch bytes with all 49 concept Python byte-equal to the committed head; the shared current-source checks are truthful (the research state-consistency count is red by design pre-report, 80 versus 79, clearing at the report commit). A3 SATISFIED at the implementation boundary (observed): all 49 product Python and all frozen boundaries unchanged (byte maps recorded before, after and committed-equivalent); truthful docs and counter; same branch and PR 29 under AMEND_EXISTING_PR (head 1c79d92 pushed). The concise exact-source report publication under the SELF/REMOTE/ONE-response convention remains PENDING root exact-byte approval of this draft; no future CI or merge success is claimed.",
  "negative_paths": "All negative evidence used tiny disposable per-test Git clones (git clone --shared --no-checkout of the actual repository) mutated only through owned synthetic commits, git replace refs and update-ref inside those clones; every replace ref is deleted in a finally block and each clone is removed at test teardown. No live inference, no protected endpoint, no network traffic, no data acquisition, and no mutation of the real repository refs, history, index or worktree.",
  "boundary_fidelity": "All 49 concept Python files including all 16 test modules are byte-equal between the tested epoch and the committed head (pre-fix, post-fix and committed maps recorded privately); the 16 governance identities, the 173-path generated manifest, all prior order and report bytes (including the exact d640 A order and its truthful FAILED report), workflows, dependencies, core and every unnamed helper are unchanged; the old three incident values, accepted bases, CLI and actual diff boundary are preserved exactly; no configuration, flag or environment path accepts arbitrary future incidents; no checker weakening (no broadened exception, no ignore, no normalization of any historical byte); the frozen 027-a implementation is neither retested as product nor modified (no product 747 rerun).",
  "setup": "Qualified Python 3.12.15 with -B (logical interpreter designation per WORKSPACE-LAYOUT.json; exact private invocation paths remain in the private receipts, not in this versioned report), PYTHONDONTWRITEBYTECODE=1, umask 077, private 700 TMPDIR and external PYTHONPYCACHEPREFIX for every runtime/test/static/writer invocation; Ruff check --no-cache; strict mypy over exactly the two changed files in a fresh byte-identical flat shadow (python_version 3.12, strict true, follow_imports silent, fresh private cache, no tests override/Any/ignore); owner-launched CODEX_HOME/auth/session preserved exactly as launched; no repository cache writes, restore or reseed, no mode sweeps, no new installer/model/auth/home/session/pane.",
  "privacy": "No raw texts, credentials, canaries or host paths in this report; logical roots and receipt names only; tiny clearly-synthetic software fixtures exclusively (synthetic Git identities inside disposable clones); no live model, protected service or customer data touched.",
  "limits": "Result COMPLETE at the implementation boundary: the closed-4 contract is enforced and passes at both accepted bases and all ordered evidence is truthful, but the final report-head CI (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the future SELF report commit remains PENDING and is not claimed passed; the pre-report research count red (80 versus 79) is expected to clear only at the report commit; no MVP, linguistic-quality, packaged-library, ICA, milestone or deployment acceptance is claimed; the owner's no-separate-human-evaluation-dataset decision and the retained fresh-audit and deployment-authority duties are unchanged; the 027-a FAILED report and its Bootstrap CI failure (exactly two whitespace subcases) remain the historical record for round a.",
  "human_gates": "No new human gate is created by this round; the decision classification is D0 (ordinary contained process defect repair) and the strongest counterargument (growing exceptions could normalize future source mistakes) is constrained by the exact pins, old-3 preservation and all drift/new-incident negatives as recorded in the order; the separate ICA and deployment human gates are unchanged and untouched.",
  "scope": "Exactly the six ordered non-report paths (oap/bin/check_whitespace.py, oap/tests/test_whitespace.py, docs/DEVELOPMENT.md, research/RESEARCH-STATE.md, oap/orders/027-b-preserve-issued-order-and-whitespace-contract.md, oap/active) in one implementation commit 1c79d92 with sole parent e157a40, plus the seventh canonical report path held pending approval; all 49 concept Python, all 16 governance identities, the 173-path manifest, all prior orders and reports, and the three untracked roots (.rclone-speed-test/, .research-test-scratch/, corpus/) preserved; unrelated PR 13 untouched; no reset, amend, rebase, force-push, clean or stash."
}
```

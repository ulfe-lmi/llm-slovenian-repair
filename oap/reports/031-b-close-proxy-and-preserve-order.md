# Work report 031-b — Close the proxy, configure review time and preserve the order

Corrective round 031-b on the existing 031 functional-proxy objective (same
branch, same PR 33, AMEND_EXISTING_PR; the 031-a audit report remains a truthful
PARTIAL and is NOT accepted). **Round result: PARTIAL** - every scoped product
fix (owned server close with first-control preservation, reviewer-only
CONCEPT_REVIEWER_TIMEOUT, closed-five whitespace contract, docs, counter) is
implemented and verified at the single implementation commit
`296aa8ee0767c0ce5e70d0458f059941185eb285` (sole parent
`9d5f012cb3731043c442af57e076a2e89229a1b3`); acceptance A1-A3 are met. The R13
bounded native round trip was executed exactly once on the owner-steered RTX 3090
model (final two ledger slots; ledger now exhausted 4/4) and FAILED at the
product supported-completed envelope contract (actual reason preserved:
ENVELOPE_INVALID; HTTP 200, 2105 B, 4.721 s), so the live native compatibility
and native-edit layers remain UNPROVEN - the experiment stopped per R13 with the
actual reason, no retry, no native success claimed. The same run actually
demonstrated the owned lifecycle end to end: normal main() return, joined
serving worker, closed listener. No merge, no milestone or deployment
acceptance; the A4 normal publication sequence completes in this round without
any added Root pre-publication pause.

```oap-report
{
  "id": "031-b",
  "result": "PARTIAL",
  "order_path": "oap/orders/031-b-close-proxy-and-preserve-order.md",
  "order_sha256": "871cdf0d40ec7c4ca084a60c3cca93748fbfd2b13eb8c0c99e9dd9bf4f4ac9ac",
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
  "implementation_head": "296aa8ee0767c0ce5e70d0458f059941185eb285",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 33,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/33",
  "pr_state": "open",
  "branch": "oap/031-functional-proxy-audit",
  "base_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
  "starting_remote_sha": "9d5f012cb3731043c442af57e076a2e89229a1b3",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-10T21:26:12+00:00",
  "report_written_at": "2026-11-10T21:34:30+00:00",
  "implementation": "Single non-report commit 296aa8ee over 9d5f012 (nine paths, +1038/-18). (1) concept-verification/proxy.py: after successful ConceptProxy construction the exact owned server is closed on normal serve_forever() return and on every unwind (KeyboardInterrupt/SystemExit/MemoryError) through the documented owning server_close() boundary (admission stop, exact worker joins, listener close); the exact first pending nonordinary caller control (including MemoryError) keeps identity over later cleanup failures, an ordinary pending error cannot suppress a later nonordinary cleanup control, with no pending error the cleanup failure propagates; the catch settles cleanup only and re-raises the applicable original object (no error conversion, no product-wide refactor, config.py and the 15 s default constant untouched). (2) NEW concept-verification/tests/test_main_lifecycle.py: 12 tests / 16 bounded owned-child scenarios driving the actual main() - normal serve completion, failed serve, a primary nonordinary control followed by a cleanup control, cleanup failure with absent/ordinary primary, native SIGINT with natural process exit (Popen returncode -2 = shell 130) within a finite bound plus actual thread/listener cleanup (forced kill cannot establish PASS), reviewer setting absent (15.0 default) / explicit 45.0 / invalid values (nonnumeric, empty, nonpositive, NaN, infinity) rejected before BOUND, and the main intake/setup/header/body/delivery budgets (30.0 x4) proven independent of the reviewer budget. (3) oap/bin/check_whitespace.py + oap/tests/test_whitespace.py: closed-four -> closed-five contract adding ONLY the exact pinned 031-a order incident (line 161; introduction da6892e3ab1f4a05bb1f792b9acb6852145e688b; blob 154087c510433f229c39cee4bafded877b40b671; SHA-256 b4e4a2a485304893d228eb35d59e91cc229ddcea95a8160e536262e759004d10; 18351 B; bytes immutable); all four prior incidents, 027-a recovery pins, ordered-parent/blob/full-history pins and both authorized bases preserved; no configuration, flags, environment input or bypass added. (4) concept-verification/README.md and docs/DEVELOPMENT.md per R9 (entry-point cleanup; default 15 vs selected native 45; whole-exchange semantics; independent other clocks; one pass, zero retries; 027-b pin preserved with closed-five supersession). (5) research/RESEARCH-STATE.md exactly one counter increment 86 -> 87. (6) Order and oap/active. The other 54 proxy Python files, all 19 pre-existing test modules, the 16 governance files, the 173-entry manifest, registry 42 and incidents 2 are byte-frozen (Root source-bound scope verification + CURRENT 173-identity verification).",
  "documentation": "README and DEVELOPMENT updated per R9 without readiness/URL/credential claims. research/RESEARCH-STATE.md machine block oap_reports_reviewed 86 -> 87 in the non-report commit only (031-a pattern: the report-only commit stages only the report path). At the implementation head the counted report files are 86 (87 .md files minus the excluded 007-o file) against block 87: the designed expected pre-report mismatch, observed in Root's decoded interim CI logs as the sole failure test_registry_and_report_counts (87 != 86) in both Application baseline and Research reproducibility, while OAP bootstrap acceptance and OAP report history succeeded. The report-only commit adds the 88th .md (87th counted) and reconciles the counter; no second bump. registry_entries 42 and frozen_report_history_incidents 2 unchanged; all 173 manifest identities unchanged.",
  "criteria": "A1: MET - focused lifecycle tests prove the operator path keeps the 15-second default when absent, accepts the explicit 45-second finite setting, and rejects nonnumeric/empty/nonpositive/NaN/infinite before any listener creation; the real main() exits naturally on native SIGINT (owned child, port-0 fixture, natural Popen returncode -2 = shell 130) and settles owned resources on every tested exit with correct first-control priority; the new regression meaningfully fails the old product bytes (bounded owned-child negative at 9d5f012 proxy.py bytes, finite bound, wall 31 s). A2: MET - the closed-five CLI passes exactly five diagnostics at BOTH authorized bases (2832fa1e, 82ea1e6f), re-verified at 9d5f012 and 296aa8ee; 14 focused tests pass retaining every old negative plus the new 031-a negatives (changed/trimmed bytes, deletion/readdition with identical bytes, sixth incident, old-incident mutation, drift, unknown base, invalid revision, missing 027-a lineage all fail closed); the issued 031-a bytes remain immutable. A3: MET - the actual diff is exactly the nine scoped paths; frozen boundaries, statics, docs, provenance and counters accurate (Root-qualified strict mypy 0 + Ruff 0 on exactly the four Python paths with fresh real imports, source hashes matching committed bytes; expected pre-report counter mismatch recorded honestly as FAILED interim CI, not reversed or waived). A4: COMPLETING in this round - normal unpublished preflight while the canonical report is absent (all shared checks RC 0 at the implementation head; state RECOVERY_REQUIRED as the expected in-progress state), private known-key checks, sole SELF report commit (sole parent 296aa8ee), forward push, normal REMOTE verification and ONE response on the same PR 33 with no added Root pre-publication pause; all four final-head CI checks plus Root's independent semantic review still precede any development merge; the fix certifies no MVP readiness.",
  "negative_paths": "Lifecycle: invalid reviewer values (nonnumeric/empty/nonpositive/NaN/infinity) rejected before BOUND; a first pending nonordinary control (including MemoryError) keeps identity over later cleanup failures; an ordinary pending error cannot suppress a later nonordinary cleanup control; with no pending error the cleanup failure propagates; no error conversion; forced kill cannot establish PASS (natural exit, actual reap and actual thread/listener cleanup asserted; Popen returncode -2 = shell 130). Whitespace: changed/trimmed 031-a bytes, deletion/readdition even with identical bytes, a new sixth incident, old-incident mutation or readdition, path/line/message drift, unknown base, invalid revision and missing 027-a recovery lineage all fail closed. Old-bytes: the SIGINT lifecycle test fails within a finite bound on the 9d5f012 product bytes, so the regression is meaningful. Native: the actual failed round trip is preserved with its real reason (ENVELOPE_INVALID; no structural failing field retained or diagnosed); no rerun/recycle/reset of the reserved review slot (ledger exhausted 4/4, 0 remaining); the review slot is RESERVED_UNKNOWN, not a false zero (0 reviewer calls observed; dispatch unprovable after a failed round trip); no GET /models, unauthenticated probe, fixed port or raw content in output ever occurred. Private harness (pre-dispatch, owned fake-child probes, no HTTP/ports/key/model calls): the pre-fix driver's false PASS reproduced (child exit 7 printing PASS -> parent rc 0 / receipt PASSED) and the corrected driver requires actual child returncode 0 + success markers + no forced kill (same probe -> rc 1 / FAILED, ledger copy unchanged); slot accounting verified on ledger copies only (RESERVED_UNKNOWN on failure; EXECUTED calls=1 on a passed fake).",
  "boundary_fidelity": "Implementation head 296aa8ee is a single commit over 9d5f012 with exactly nine paths (listed in implementation); committed byte equivalence proven for all four Python paths; R1 baseline hashes retained. The native fixture changed only the hardcoded bind address to an OS-assigned loopback port 0 and observed the real serve entry (real main/constructor/admission/qualified Pandoc 3.7.0.2/real reviewer construction); default 18024 never bound. The caller's explicit Authorization header is the only credential on the main POST (the proxy forwards only explicit caller auth and never borrows the reviewer key); the reviewer key exists only as a child-local environment export inside the finite diagnostic child (the parent never reads, prints or copies it). Sanitized child env: explicit OAP_ROLE=coding, explicit live opt-in, no CODEX_HOME/CONCEPT_REVIEWER_PROFILE, private HOME/TMPDIR/PYTHONPYCACHEPREFIX. The interim CI checkout 55ca6cbe9de12f2513c75339e07746a83a1b80a0 is GitHub's PR synthetic merge, not accepted main (recorded honestly). The A100 reviewer diagnostics (ledger attempts 1-2, model qwen3.8-27b) remain separate evidence from the RTX 3090 native round trip (attempts 3-4, model qwen3.8-27b-rtx3090).",
  "setup": "Same adopted foreground owner CLI (same process, cwd, argv, profile, home, auth; no new agent/CLI/provider/pane/restart/context reset; no other agent or historical research scan). Every helper: explicit OAP_ROLE=coding, shell umask 077, qualified Python 3.12.15 with -B, qualified Pandoc 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229; explicit path, no discovery), authorized read-only index (SHA-256 f769235b6af3412e65f0875f4d08231c832f60d8630b43a06ab927c2d32c739f, 7991296 B), private 0700 dirs / 0600 files. The owner key (repo root, 0600, untracked, locally excluded) was consumed only inside the finite native child via the existing private key helper; never printed, staged, copied or logged. The two remaining authorized native requests were ordinary finite diagnostic traffic (one main POST + at-most-one review) under the hard four-attempt ledger (initial private ledger SHA-256 a19a5220de9f0988dc731f9b0d631f12bb7aa8179041e53bc54bca476c2fcddc, 2/4); the ledger is now exhausted (4/4; post-execution SHA-256 a5893b8db6d9d623dacb0a72aad74fb13cb251eb0d8babc7ebdfa292580a1978).",
  "privacy": "No raw customer text, model prompts/answers, targets/replacements, credentials, headers or private resource paths in any public artifact; the native receipt, ledger and all diagnostic output are content-free (counts, hashes of private comparisons, reasons, timings); the owner key file was not staged, printed or copied into reports; public prose uses logical roots (STRATEGIC_HOME-relative workorder receipts, private scratch descriptors) instead of physical machine paths.",
  "limits": "PARTIAL solely because the live native layer is unproven: the R13 round trip failed at the product supported-completed envelope contract (actual reason ENVELOPE_INVALID preserved; no diagnosis invented, no parser weakened, no product change made to chase it); the native edit remains UNPROVEN; no quality-rate, dataset or corpus claim is made or implied; the ledger is exhausted (4/4, 0 remaining) so no further native request is possible under this order; the prior A100 45 s batch-client proof remains separate from a full native round trip or accepted edit. No broad-suite rerun beyond the ordered scope (final CI runs the full suites); no human dataset (excluded, not deferred); no merge, auto-merge or MVP/deployment acceptance.",
  "human_gates": "Decision NONE under D0. Root's independent exact-byte review of the published head/report and all four required final-head CI checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) plus independent semantic review precede any development merge; at the interim head 296aa8ee two checks (Application baseline: 1 failed / 1745 passed / 58 skipped / 504 subtests, 1195.08 s; Research reproducibility: 409 tests, 1 failure) failed solely on test_registry_and_report_counts 87 != 86 - the expected pre-report counter mismatch (block 87 anticipates this report; counted files 86 = 87 .md minus excluded 007-o) - with subsequent driver commands NOT RUN and not claimed passed; that status is preserved and reconciled by the report-only commit (88 .md files, 87 counted, block stays 87), while OAP bootstrap acceptance (run 42892681685) and OAP report history already succeeded at the interim head. The 031-a private-byte gate remains mandatory for that prior round. The human retains final milestone labeling and release/deployment authority; none is claimed.",
  "scope": "Nine scoped non-report paths (concept-verification/proxy.py, NEW concept-verification/tests/test_main_lifecycle.py, oap/bin/check_whitespace.py, oap/tests/test_whitespace.py, concept-verification/README.md, docs/DEVELOPMENT.md, research/RESEARCH-STATE.md one-line counter 86 -> 87, oap/orders/031-b-close-proxy-and-preserve-order.md, oap/active) plus this sole report; PR 33 amended in place (title unchanged; body refreshed for the scoped fixes, corrected to PENDING by Root, then set to the actual native outcome). The three unrelated untracked roots, the owner key file, retained branches, archives, the read-only index and private failed epochs are preserved. No other path mutation.",
  "checks": [
    {
      "command": "pytest (focused 5-module set incl. test_main_lifecycle, test_whitespace, test_proxy, test_pandoc_protection, test_concept) -q",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "153 passed + 66 subtests in 114.21 s, rc 0; qualified python -B, private caches; the new lifecycle module is covered at the current bytes."
    },
    {
      "command": "pytest oap/tests/test_whitespace.py -q (focused, closed-five suite)",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "14 passed, rc 0; all old negatives retained plus the new 031-a incident negatives; disposable-Git/real-CLI cases."
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da (CI: OAP bootstrap acceptance)",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "exactly five diagnostics (007-e order, 007-f order, 027-a order, 031-a order:161, 007-d report), RC 0; also passed at 9d5f012."
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a (CI: Application baseline)",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "identical five-diagnostics set, RC 0; also passed at 9d5f012."
    },
    {
      "command": "strict mypy + Ruff on exactly the four Python paths (Root-qualified fresh real-imports proof; cited, not rerun)",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "Root's fresh proof: strict mypy 0 and Ruff 0 on exactly proxy.py, tests/test_main_lifecycle.py, oap/bin/check_whitespace.py, oap/tests/test_whitespace.py with precise frozen-module real imports; its source_sha256 map matches the committed bytes (proxy 836b78cc..., test_main_lifecycle 042447b9..., check_whitespace 61dfb231..., test_whitespace 4bd6f65b...); no broad Any/ignores; the interim follow_imports=skip epoch was limited interim, not the qualified evidence."
    },
    {
      "command": "old-bytes regression negative: SIGINT lifecycle test against the 9d5f012 proxy.py bytes (bounded owned child)",
      "result": "FAILED",
      "sha": "9d5f012cb3731043c442af57e076a2e89229a1b3",
      "publication_head_claim": false,
      "details": "failed within a finite bound (wall 31 s) on the old product bytes - the new regression meaningfully fails the old bytes, as required; recorded as a design-expected negative, not a product failure of the new head."
    },
    {
      "command": "python3 oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "RC 0 at the implementation head (unpublished preflight, canonical report absent)."
    },
    {
      "command": "python3 oap/bin/oap_cli.py transcript --repo-root . --revision 296aa8ee0767c0ce5e70d0458f059941185eb285",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "RC 0; report_count 87; active=latest=031-b; frozen mutation paths unchanged."
    },
    {
      "command": "python3 oap/bin/oap_cli.py report-history --repo-root . --revision 296aa8ee0767c0ce5e70d0458f059941185eb285 --require-manifest",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "RC 0; report_count 87; all 173 manifest identities; frozen mutation paths (006-a, 006-c) unchanged."
    },
    {
      "command": "python3 oap/bin/oap_cli.py state --repo-root . --strategic-home STRATEGIC_HOME --repository ulfe-lmi/llm-slovenian-repair",
      "result": "PENDING",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "RC 0; observed RECOVERY_REQUIRED for 031-b with branch oap/031-functional-proxy-audit and PR 33 - the expected in-progress state of a round whose sole report is not yet published; reconciled by the report-only commit + remote verification, not by any state mutation."
    },
    {
      "command": "git diff --check --no-ext-diff --no-textconv",
      "result": "PASSED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "RC 0; all newly introduced bytes whitespace-clean."
    },
    {
      "command": "R13 bounded native proxy round trip (real proxy.main(), loopback port 0, qwen3.8-27b-rtx3090, final two ledger slots)",
      "result": "FAILED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "executed once at 2026-11-10T21:22Z (owner-steered RTX 3090 model; main POST + reserved review slot; ledger 2/4 -> 4/4, 0 remaining): bound port 0 (46525); HTTP 200, 2105 B, 4.721 s; the response envelope did not satisfy the product supported-completed contract -> ENVELOPE_INVALID (no structural failing field retained or diagnosed; the rejected field is unknown and not guessed); native edit UNPROVEN; review slot RESERVED_UNKNOWN (0 reviewer calls observed; no false zero asserted); owned cleanup actually proven end to end (main_return 0, no main error, shutdown finished, worker joined, listener closed, no forced kill; child rc 1); content-free private receipt SHA-256 4102f8feb9588f0108b701dbbe2e10e254e3bfd12d0f8dcf2555bdab6a91b805; harness child SHA-256 90bbfcb6e13a6d671e6edb80f363674d850260d6633edb42baa93ce5579ee447 / driver SHA-256 d646b34f3281c96d270e64be8ba27e73aafe1103ed024476bcd5fb63cb05c16d (both verified pre-dispatch, incl. the owner-reviewed auth/bounds/cleanup/label corrections); experiment stopped per R13 with the actual reason preserved; no rerun/recycle/reset/retry."
    },
    {
      "command": "interim CI observation at 296aa8ee (GitHub PR synthetic merge 55ca6cbe9de12f2513c75339e07746a83a1b80a0; Root decoded job logs)",
      "result": "FAILED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "OAP bootstrap acceptance (run 42892681685) and OAP report history (same run) success; Application baseline (run 42892681727: 1 failed / 1745 passed / 58 skipped / 504 subtests, 1195.08 s) and Research reproducibility (run 42892681608: 409 tests, 1 failure) failed solely on research test_registry_and_report_counts 87 != 86 - the expected pre-report counter mismatch (block 87 anticipates this report; counted files 86 = 87 .md minus excluded 007-o); subsequent driver commands NOT RUN and NOT claimed passed; status preserved, not reversed or waived; the report-only commit reconciles (88 .md files, 87 counted, block stays 87) and all four final-head checks remain mandatory on the published head."
    }
  ]
}
```

This report is the PRIVATE unpublished preflight (round result PARTIAL - see
`human_gates` and the R13 native check: all scoped product work is complete and
verified; the live native compatibility/edit layers remain UNPROVEN with the
actual failure reason preserved and the native ledger exhausted 4/4). The
publication sequence now executes: the report-only SELF commit (sole parent
`296aa8ee0767c0ce5e70d0458f059941185eb285`, only this report path), forward
push, `verify-report --repository ulfe-lmi/llm-slovenian-repair` remote
verification, then ONE FIFO response and quiescence. No future push/CI success
is claimed inside this pre-push report (`publication_verified: false`); the
final-head four CI checks and Root's independent semantic review remain the
development-merge gate.

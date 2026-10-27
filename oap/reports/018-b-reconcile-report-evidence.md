# Work report 018-b - Reconcile published header-budget report evidence (objective 018, round b; AMEND_EXISTING_PR; PR #20 open; branch retained)

```oap-report
{
  "id": "018-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/018-b-reconcile-report-evidence.md",
  "order_sha256": "ba80b485e80c2d15f382ce18ffa57af507e8ec1a8f51482a04f1e01067ae695b",
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
  "implementation_head": "23344144afbc1d1942e6db934aae4855e4bdeb04",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 20,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/20",
  "pr_state": "open",
  "branch": "oap/018-response-header-budget",
  "base_sha": "146feda1445e82702a3a2d1757064474253714e2",
  "starting_remote_sha": "146feda1445e82702a3a2d1757064474253714e2",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-27T07:44:34+00:00",
  "report_written_at": "2026-10-27T08:03:12+00:00",
  "superseded_report": {
    "path": "oap/reports/018-a-response-header-budget.md",
    "commit": "146feda1445e82702a3a2d1757064474253714e2",
    "parent": "76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e",
    "sha256": "2403e5603124de2777b64806d7030fd25bb70528cdd82a5fa3e2016a824c0ee2",
    "bytes": 26149,
    "status": "IMMUTABLE_PRESERVED_BYTE_FOR_BYTE"
  },
  "superseded_claims": [
    {
      "claim": "A check row 'Offline research suite, tables, publication guard and OAP helpers at the implementation head' was labeled PASSED while the offline discovery actually ran 409 tests, FAILED 1 (report-count 69 vs 68) and SKIPPED 53.",
      "corrected_fact": "The offline research discovery FAILED with the single expected bookkeeping cause and 53 distinct skips in both rounds, with different count pairs: A's actual pre-report discovery at 76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e ran 409 tests, FAILED 1 (report-count 69 vs 68) and SKIPPED 53, while B's actual discovery at the non-report head 23344144afbc1d1942e6db934aae4855e4bdeb04 ran 409 tests in 23.018 s, FAILED 1 (70 != 69) and SKIPPED 53, because oap_reports_reviewed was prepared for this one B report; 70 vs 69 is B's actual result, not A's original result. rebuild_tables, publication guard, accepted-runtime governance, transcript/history, pins and whitespace each actually PASSED and are recorded as separate rows in B; a later successful report-head CI cannot retroactively turn the pre-report discovery into PASSED; the count check was not weakened and the expected counter was not manipulated to force pre-report green."
    },
    {
      "claim": "A attributed the pre-mutation reproduction 'at the exact verified base 29ae4c1' to the order receipt 018-header-prerequisite-at-017-final.json and combined the two receipts' timings into one statement.",
      "corrected_fact": "That receipt (observed 2026-10-27T04:35:13Z) was tested at 147832e7fd8199309f7894cb16893a40e080ad85, the 017-a report commit whose six product source bytes are identical to the accepted merge 29ae4c1424da1140026796f7ef6129c11531106e - this establishes equality of those six source files, not an execution of that receipt at 29ae - with header-drip walls 0.534 s JSON and 0.576 s SSE (fast 0.034/0.009 s) at the configured 0.15 s socket/body budget, original bytes, one main call and zero review calls. The own receipt 018a-own-pre-mutation-repro.json (observed 2026-10-27T05:19:11Z) was tested at the exact base 29ae4c1424da1140026796f7ef6129c11531106e with the same six stable source hashes and its own recorded walls (drip 0.374 s JSON / 0.375 s SSE; fast 0.034/0.013 s). Source-byte equality and exact tested revision are separate; no claim is made that the new header configuration existed at the old baseline (it is new in 018-a)."
    },
    {
      "claim": "A described the startup-overhead regression as 'a 0.12 s delayed status delivery still expires under a 0.03 s budget'.",
      "corrected_fact": "The startup regression injects the delay in the guard's own Thread.start (the guard-start path itself), not merely delayed status delivery; the single absolute deadline is anchored before the guard starts, so completion after that startup overhead is rejected."
    },
    {
      "claim": "A stated 'the same proxy returns exact original 502 bytes' for a bounded header failure.",
      "corrected_fact": "A bounded header failure is a main 502 with zero analysis and zero review; no main response was validly captured at that point, so there is no original-answer 502 fallback for an incomplete main; the next healthy request on the same proxy is 200 with original bytes."
    },
    {
      "claim": "A's phase wording could be read as involving the 017 nonblocking collector in header acquisition.",
      "corrected_fact": "Header acquisition uses the standard blocking stdlib HTTP/HTTPS getresponse parser with an owned timer; the 017 nonblocking body collector is a later phase (body collection) and is not part of header acquisition."
    },
    {
      "claim": "A described the USEFUL_018 NFC-unstable decomposed/combining material as 'on its own separate paragraph'.",
      "corrected_fact": "The fixture keeps the NFC-unstable material on a separate SOURCE LINE from the protected line, with no blank paragraph separator; the actual tested layout is described here and the frozen tests are not changed to match report wording."
    },
    {
      "claim": "A used pr_observed_at equal to the PR createdAt (2026-10-27T06:42:20Z).",
      "corrected_fact": "That timestamp is the PR creation time, not a head observation; B records the actual observation 2026-10-27T07:44:34Z (gh plus a clock command) of PR 20 at head 23344144afbc1d1942e6db934aae4855e4bdeb04, with the creation time labeled as creation."
    },
    {
      "claim": "A's report_written_at (2026-10-27T07:10:00Z) was a hand-picked rounded timestamp rather than the actual finalization time.",
      "corrected_fact": "B records the actual draft finalization time (this report_written_at), measured at write time, not a hand-picked or rounded value."
    },
    {
      "claim": "A's operative wording 'it clears at the final head with this report commit' and 'which clears with this report commit' asserted a prospective publication result.",
      "corrected_fact": "Removed from operative claims: the research counter is prepared for this one 018-b report (70), but the actual post-publication count result must be observed after publication; no future publication or CI success is asserted in this prewritten report."
    },
    {
      "claim": "A's privacy line asserted no private path 'in the report or logs'.",
      "corrected_fact": "Published OAP artifacts contain no real customer text, credentials or private review payloads and use logical roots publicly; private setup and CLI logs may contain their permitted host paths and failed synthetic fixtures, so no assertion is made that private paths are absent from logs generally."
    },
    {
      "claim": "A's setup line stated 'no new repository cache or .venv writes during the 018 window' without scoping the evidence.",
      "corrected_fact": "The evidence is a bounded census: the 47 baseline-listed mixed cache/bytecode files (including the nine-pyc subset) are unchanged in bytes, mtime_ns and size between the recorded snapshots; that is scoped evidence, not proof about all unlisted files globally; all caches are preserved and none is restored, deleted or rewritten."
    }
  ],
  "checks": [
    {
      "command": "A report supersession: immutable A identity and enumerated corrected claims (requirement 6)",
      "result": "PASSED",
      "details": "A report oap/reports/018-a-response-header-budget.md at commit 146feda1445e82702a3a2d1757064474253714e2 (sole parent 76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e) is preserved byte-for-byte: SHA256 2403e5603124de2777b64806d7030fd25bb70528cdd82a5fa3e2016a824c0ee2, 26149 bytes, re-verified at this head. Its final 16 governance identities are valid and match the published 018-a order; the bad hashes that existed only in the earlier PRIVATE draft were fixed before publication, and this report does not repeat them nor alleges a published integrity failure. The superseded_claims field enumerates each superseded A claim with its actual corrected fact.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Offline research unittest discovery at non-report head 2334414 (owned 700 private TMPDIR, test-process umask 022 for the single mode-sensitive test)",
      "result": "FAILED",
      "details": "Ran 409 tests in 23.018s, FAILED (failures=1, skipped=53): the sole failure is test_registry_and_report_counts with AssertionError 70 != 69, the expected bookkeeping cause (oap_reports_reviewed is prepared for the new 018-b report; the research count excludes 007-o, so generic and research totals differ by one). The 53 skips are recorded distinctly. This explicitly supersedes the A report's grouped row that labeled this discovery PASSED; a later successful report-head CI cannot retroactively turn the pre-report discovery into PASSED; the count check was not weakened and the expected counter was not manipulated.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "research.tools.rebuild_tables --check at non-report head 2334414",
      "result": "PASSED",
      "details": "exit 0; numeric table: PASS.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "research.tools.publication_guard --root research at non-report head 2334414",
      "result": "PASSED",
      "details": "exit 0; publication guard: PASS (6520 files).",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Shared accepted-runtime governance at non-report head 2334414 (accepted ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0)",
      "result": "PASSED",
      "details": "check_governance --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 exit 0 (structure valid; semantic_proof and human_authorization_proof remain false as expected for a coding round).",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Transcript and report history at non-report head 2334414",
      "result": "PASSED",
      "details": "transcript valid (revision mode, active 018-b, report_count 70; the prior order/report history including the quarantined 007-d/007-n/008-d entries and the frozen 006-a/006-c incidents is unchanged); check_report_history valid at the same revision (report_count 70).",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Pins and whitespace at non-report head 2334414",
      "result": "PASSED",
      "details": "All 173 GENERATED-FILES pins verify against disk (the 173-path set is unchanged; no bookkeeping path is pinned, so the manifest itself is unchanged in this commit). check_whitespace PASSED at both authorized bases (2832fa1 and 82ea1e6) with only the three tolerated historical incidents.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "A2 - frozen product/test/source identity (reuse by exact source identity, not a newly executed B run)",
      "result": "PASSED",
      "details": "No product, test, Python, docstring, configuration, dependency, workflow or source-law change in 018-b; the non-report commit 2334414 changes exactly the new 018-b order, oap/active (018-a to 018-b) and research/RESEARCH-STATE.md (oap_reports_reviewed 69 to 70 only; registry_entries 42, frozen_report_history_incidents 2 and all identity fields unchanged). All tracked concept/research Python blobs (including the 30 concept/eval/test files, the eleven frozen modules and the six older test modules) match the trusted report head 146feda, and the 018-a evidence (350 tests plus 107 subtests, strict four files, Ruff four files at 76aa688) is identified as reuse by exact source identity, not a newly executed B run. No product functionality is claimed by B.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Precursor attribution reconciliation (requirement 2)",
      "result": "PASSED",
      "details": "Each private receipt is preserved with its exact SHA, timing and scope rather than recombined facts: the strategy prerequisite receipt tested 147832e (same six product source bytes as the accepted merge 29ae4c1; observed 04:35:13Z; drip walls 0.534/0.576 s), and the own pre-mutation receipt tested the exact base 29ae4c1 (observed 05:19:11Z; drip walls 0.374/0.375 s), both with the same six stable source hashes. Source-byte equality and exact tested revision are separate, and no new header configuration is claimed at the old baseline.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Mechanism and API result reconciliation (requirement 3)",
      "result": "PASSED",
      "details": "The startup regression injects delay in the guard Thread.start and rejects completion after that startup overhead using the deadline anchored before startup; a header failure is main 502 with zero analysis and zero review, there is no original-answer 502 fallback for an incomplete main, and the next healthy request is 200 with original bytes; header getresponse uses the standard blocking stdlib HTTP/HTTPS parser with an owned timer while the 017 nonblocking body collector is a later phase; USEFUL_018 keeps the NFC-unstable material on a separate source line with no blank paragraph separator, described as actually tested without changing the frozen tests.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Timestamp and publication-claim reconciliation (requirement 4)",
      "result": "PASSED",
      "details": "PR state and head were fetched now: PR 20 OPEN, head 2334414, base main, observed at 2026-10-27T07:44:34Z from a clock command (pr_observed_at); the historical PR createdAt 2026-10-27T06:42:20Z is labeled as creation, not a new head observation; report_written_at is the actual draft finalization time, not a hand-picked or rounded timestamp; SELF and publication_verified=false are retained at this prewritten-report time and all future publication/final-head CI results are PENDING until actually observed; A's prospective it-clears-with-this-report wording is removed from operative claims (the counter is prepared for this one report, and the actual post-publication result must be observed).",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Privacy and cache claim bounding (requirement 5)",
      "result": "PASSED",
      "details": "No real customer text, credentials or private review payloads in published artifacts; logical roots and environment names are used publicly; private setup/CLI logs may contain their permitted host paths and failed synthetic fixtures, so no assertion is made that private paths are absent from logs generally; the unchanged-47-files statement is bounded census evidence (bytes, mtime_ns and size of the listed baseline files), not proof about all unlisted files globally; all caches are preserved and none is restored, deleted or rewritten.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "B governance identities obtained programmatically and disk-verified (requirement 6)",
      "result": "PASSED",
      "details": "This report's 16 governance identities were parsed programmatically from the exact 018-b order metadata and each was re-verified against both the current worktree and the trusted accepted governance ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0; no manual hex transcription. The A report's final 16 governance pins are valid and match the published 018-a order; B does not repeat the private draft's bad hashes and does not allege a published integrity failure.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Bounded bookkeeping at the non-report head (requirement 7)",
      "result": "PASSED",
      "details": "The non-report commit 2334414 (pushed on the same branch and PR 20) contains only the ordered bookkeeping paths: the new 018-b order, the oap/active pointer 018-a to 018-b, and research/RESEARCH-STATE.md counter 69 to 70 only; registry_entries 42, frozen_report_history_incidents 2 and all identity fields are unchanged; no GENERATED-FILES pin path is affected (the 173-path set is unchanged and none of the bookkeeping paths is pinned). The generic count includes 007-o while the research counter excludes it, so the totals differ by one: prior 70 generic / 69 research; with this one B report the expected post-publication totals are 71 / 70, subject to actual observation. No extra Markdown was created under oap/reports.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Private B draft preflight at the non-report head (requirement 8)",
      "result": "PASSED",
      "details": "preflight-report --id 018-b --expected-head 23344144afbc1d1942e6db934aae4855e4bdeb04 against this private draft: valid unpublished report draft (exit 0). The final rendered JSON/Markdown was reread for the specific semantic claims of requirements 1-6; a schema pass is not treated as a truthfulness audit.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "B sole-path SELF publication and remote proof (requirement 9)",
      "result": "PENDING",
      "details": "The sole-path SELF report commit (sole parent 23344144afbc1d1942e6db934aae4855e4bdeb04), the push, the independent remote PR/head check, the exact report bytes/hash and parent/path verification, and the exact final response OK occur after this prewritten draft and cannot be claimed here.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    },
    {
      "command": "Final B-head CI (post-publication)",
      "result": "PENDING",
      "details": "The four required checks at the final B head - Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history - are strategic post-publication evidence and cannot be claimed by this prewritten report. The initial A-head CI observations are separate evidence and do not replace the future B-head gate; missing, pending or cancelled is not PASSED.",
      "sha": "23344144afbc1d1942e6db934aae4855e4bdeb04",
      "publication_head_claim": false
    }
  ],
  "implementation": "No implementation change in 018-b: the 018-a software at 76aa68894d7476a5bd9aca9a8fbb3f3c47f5cd4e remains the product baseline (new concept-verification/header_transport.py, the keyword-only header_timeout constructor parameter with the CONCEPT_HEADER_TIMEOUT environment default in main(), and the new 34-test module). 018-b is a report-evidence reconciliation: one non-report bookkeeping commit (the new order, the active pointer, the counter 69 to 70) and this superseding report. Product behavior, tests, dependencies and source law are frozen and unchanged.",
  "documentation": "The new B report and order are the evidence-reconciliation record; the A report is preserved as immutable history. The existing PR body is updated truthfully to describe the whole final header-budget change, the current implementation/report identity, the qualified software results and the actual CI observations without stale hashes or future success. No README/STATUS or other doc was modified merely to repeat the new report, and no raw answer, target, replacement, prompt, response or credential appears in any OAP artifact.",
  "criteria": "A1 SATISFIED (observed): B supersedes each named A inaccuracy with the corrected fact, and every command status, tested SHA, source-byte identity, timestamp and evidence scope is attributable separately; no grouped PASS hides a failure and no future publication or CI success is claimed. A2 SATISFIED (observed): all product/test/source-governance/older-report bytes match the trusted 146feda; the 350/107/strict4/Ruff4 evidence at 76aa688 is identified as reuse by exact source identity, not a newly executed B run; no product functionality point is claimed. A3 OBSERVED AT DRAFT TIME: the exact bounded bookkeeping, same PR 20/branch, validated private B draft (preflight exit 0) and the non-report head checks are recorded; the sole-parent/sole-path SELF publication, actual remote proof and the response OK are PENDING by design of this prewritten report and are recorded by the post-publication verification as strategy-owned evidence. A4 REQUIRED: the four current final B-head CI checks remain required for strategic merge; development merge is no deployment.",
  "negative_paths": "No product/test/Python/docstring/configuration/dependency/workflow change; no new parser or model; no research, data, registry, scoring or protocol change (the research suite ran read-only at the committed head); no source-law or projection refresh; no new milestone gate; no live endpoint, real text, credential or deployment; no merge or auto-merge; no branch or PR creation (AMEND_EXISTING_PR on PR 20); no report rewrite or re-seeding (the A report bytes are preserved); no background AI or subagent; the unrelated untracked corpus/, .research-test-scratch/ and .rclone-speed-test/ are preserved and unstaged; all caches are preserved without restore, delete or rewrite.",
  "boundary_fidelity": "LR-001 through LR-014 remain preserved; CRITICAL has zero actual entries and its bytes are protected and unchanged; the governance identities are unchanged (no governance change in this round); the immutable 018-a report and all earlier orders/reports and Git history are preserved byte-for-byte; the 013/014/015/016/017 contracts remain as previously recorded. 018-b changes only report evidence and bookkeeping: distinct per-command statuses, exact precursor SHAs/timings, corrected mechanism wording, actual timestamps, bounded privacy/cache claims, and the explicit supersession list.",
  "setup": "Qualified external Python 3.12 interpreter with -B and PYTHONDONTWRITEBYTECODE=1; OAP_ROLE=coding exported in helper command environments; new owned private scratch test-scratch-018b (umask 077, dirs 700, files 600) with external TMPDIR and cache prefixes; the frozen mode-sensitive research test ran under test-process umask 022 only inside a private 700 TMPDIR, matching CI (scope recorded); no repository .venv, dependency install, py_compile, cache restoration or unrelated cleanup. Private receipts are metadata-only and stay in owned scratch and workorders; public artifacts use logical roots. The private setup and CLI logs may contain permitted host paths and failed synthetic fixtures, so no global no-private-path claim about logs is made.",
  "privacy": "Synthetic fixtures and fake keys only in the underlying 018-a tests; no real customer text, credential or private review payload in any published artifact; logical roots and environment names publicly; private receipts (the two precursor receipts, the independent review receipts and the private B draft) are metadata-only evidence, never code or runtime dependencies, and are not paths to publish; no raw answer, target, replacement, prompt, response or credential in this report.",
  "limits": "018-b is evidence reconciliation, not a new verification run: the 350 tests plus 107 subtests, strict mypy on four files and Ruff on four files at 76aa688 are reused by exact source identity (all tracked concept/research Python blobs match the trusted 146feda), not re-executed in this round. The research discovery at the non-report head includes the single expected pre-report count mismatch (70 != 69) with 53 distinct skips; its post-publication clearing, or lack of it, must be actually observed and is not claimed here. All publication and final-head CI results are PENDING at this prewritten-report time. The bounded 47-file cache census is scoped evidence, not a global statement about unlisted files. The supersession list is complete for the named A inaccuracies; A wording not enumerated here stands as published.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order; no agent-authored human acceptance, disposition or milestone/deployment label).",
  "scope": "Exactly the ordered allowlist: the new 018-b order, oap/active, research/RESEARCH-STATE.md (counter 69 to 70 only), directly matching existing GENERATED-FILES pins (none of the bookkeeping paths is pinned, so the 173-path set and the manifest are unchanged), and this new report oap/reports/018-b-reconcile-report-evidence.md. The PR body update is truth-keeping for the existing PR 20. No other paths or governance changes.",
  "result_summary": "018-b reconciles the published 018-a header-budget report evidence on the same PR 20 and branch (AMEND_EXISTING_PR; no merge): the A report at 146feda (SHA256 2403e5603124de2777b64806d7030fd25bb70528cdd82a5fa3e2016a824c0ee2) is preserved immutable, and this report explicitly supersedes its named inaccuracies with the corrected facts - the grouped offline row is unwrapped into distinct statuses (the research discovery FAILED solely with the expected pre-report count cause, with different count pairs by round: 69 vs 68 for A's actual discovery at 76aa688 and 70 vs 69 for B's actual discovery at 2334414, each with 53 distinct skips; rebuild tables, publication guard, accepted-runtime governance, transcript/history, pins and whitespace each PASSED separately), the precursor receipts are attributed to their exact tested revisions (the 147832e strategy receipt versus the exact-29ae own receipt with their separate recorded timings), the startup regression is described as a guard Thread.start delay under a pre-startup deadline, the header failure as a main 502 with zero analysis and no original-answer fallback followed by a healthy 200, the header parser as the standard blocking stdlib getresponse with an owned timer, the fixture as a separate source line without a blank paragraph separator, and the timestamps, prospective clearing wording and privacy/cache claims are bounded to their actual evidence. The non-report bookkeeping commit 2334414 (order, active, counter 69 to 70) is pushed on PR 20; all 30 concept/eval/test Python blobs and the frozen modules match the trusted 146feda, so the 018-a software evidence is reused by exact source identity. The round started at the PR 20/branch head 146feda1445e82702a3a2d1757064474253714e2 (starting_remote_sha); remote main and the PR base remained 29ae4c1424da1140026796f7ef6129c11531106e, unchanged throughout this round. Publication of this sole-path SELF report, its remote verification and the final B-head CI are PENDING by design at this prewritten-report time; no scientific, deployment or acceptance change; no merge; PR 20 stays OPEN for strategy review."
}
```

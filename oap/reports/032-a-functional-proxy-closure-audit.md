```oap-report
{
  "id": "032-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/032-a-functional-proxy-closure-audit.md",
  "order_sha256": "76ff26a803b84f8cb6a14f430778ff5294f55e085c53a906d67f89c43448c7d3",
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
  "implementation_head": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 34,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/34",
  "pr_state": "open",
  "branch": "oap/032-functional-proxy-closure-audit",
  "base_sha": "2f0d9c4719486b86821c989ec9add9f0254a1e72",
  "starting_remote_sha": "2f0d9c4719486b86821c989ec9add9f0254a1e72",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-11T02:10:39+00:00",
  "report_written_at": "2026-11-11T02:10:40+00:00",
  "implementation": "One non-report commit on accepted main 2f0d9c4719486b86821c989ec9add9f0254a1e72; the literal implementation head 8549db27cb8761e33301f516ef95cae9a0edfb4a has that main as its sole parent and touches exactly the six permitted non-report paths: NEW oap/orders/032-a-functional-proxy-closure-audit.md (SHA-256 76ff26a803b84f8cb6a14f430778ff5294f55e085c53a906d67f89c43448c7d3), oap/active 031-c -> 032-a, NEW oap/audit/results/032-functional-proxy-requirements-first.json at the frozen original bytes (SHA-256 2c5899726f4fafa0b080ba63951db613339fe37d566037845c98b037205dd052, 51948 B; the R2 working-copy change was detected and the exact initial bytes restored before commit), NEW oap/audit/results/032-functional-proxy-closure-audit.md (181887 B, 815 lines, single oap-ica fence) and NEW oap/audit/results/032-functional-proxy-closure-evidence.json (105007 B, valid JSON, logical resource references only), and research/RESEARCH-STATE.md machine block oap_reports_reviewed 88 -> 89 only (registry 42 and frozen report-history incidents 2 unchanged). No product, test, governance, manifest, registry or prior-evidence byte changed. PR 34 was created (CREATE_NEW_PR) on branch oap/032-functional-proxy-closure-audit before the literal implementation head was captured.",
  "documentation": "The source-first derivation, the audit and the evidence appendix are the documentation deliverables. The requirements-first JSON records the independent source-derived requirements and applicability written before implementation inspection, at its exact frozen original bytes; the superseded R2 digest is disclosed and the registry projection is kept in the audit and the allowed appendix. The 815-line audit (single oap-ica fence) leads with the concrete functional gaps and closes with authority and non-claims: of the 59-row MVP matrix, 43 IMPLEMENTED, 13 PARTIAL and 3 ABSENT (full 64-row registry projection with applicability: 48 APPLICABLE_FUNCTIONAL, 4 EXCLUDED_OWNER, 7 FOUNDATION_PRIOR_STAGE, 5 LATER_STAGE); 77 separately derived F-rows in 13 areas plus the eight PLAN section 16 criteria (C1-C8) and four owner-scope rows (O1-O4); traced runtime paths at the audited bytes; and evidence at the audited SHA. The post-derivation reconciliation records that Root's counterexample receipts changed the protection assessment: the actual installed Pandoc, engine, strict acceptance and real loopback path edited protected source in Slovenian quotations, lazy Markdown blockquote continuations and misclosed HTML, so the first failing boundary is the protection map admitting the span before the detector or reviewer (QUOTE constants pandoc_protection.py:129-132; shared quote state :797-835; identity-free raw-tag depth :654-680; lazy blockquote grant :920-922), affecting LR-007, A-PROTECT-01, A-SPAN-01, A-ACCEPT-02, MVP-5 and D03; the auditor's Probe D independently reproduced the gap offline (14/14 red, 4/4 controls held, real read-only index with the checked-in miniature corpus fixture for R11-R13/K4). The evidence JSON preserves actual test provenance with the auditor executions (S1/S2/PA/PC/PD), the carried 031-a/031-b evidence under proved source and dependency equivalence (B-v3 synthetic loopback e2e at 3bd6ffd; R13 native bounded round trip) and the twenty Root strategic receipts by name and SHA-256, keeping literal-execution, byte-equivalence and Root-verified provenance separate.",
  "criteria": "A1: MET - fresh-context provenance (fresh chat in the same owner-launched foreground CLI, the single consumed control frame, dispatcher handoff), the exact accepted product (main 2f0d9c47..., tree d404c7ad..., governance 3549de2a..., frozen registry fe49c8ea..., 64 rows / 59 MVP) and the saved independent requirements-first derivation (frozen bytes 2c589972..., R2 restore recorded) establish the audit sequence. A2: MET - the full source-derived assessment (LR-001..LR-014, PLAN section 16, D01-D07/M01-M07/S01-S05, 77 F-rows, C1-C8, O1-O4) and the exact registry projection link traced runtime paths, positive and negative evidence, first failing boundaries and explicit limits, with owner-scope applicability recorded (deployment_authorized false, human_milestone_accepted false). A3: MET - actual check_ica (rc 0, schema valid, 16 gaps = 13 PARTIAL + 3 ABSENT, interpreted at the schema boundary) and the full shared-check set validate the artifacts and the exact six-path scope at the literal implementation head; the designed pre-report counter mismatch is preserved as FAILED; publication preserves the audited revision and the evidence history. A4: STANDING - the actual unpublished preflight passed on the exact final draft with the canonical report absent; the report is the sole-path SELF commit with sole parent 8549db27cb8761e33301f516ef95cae9a0edfb4a, forward push, REMOTE verification and the one OK response complete the audit publication; Strategy independently verifies the exact head and evidence and applies the existing development-merge conditions separately from readiness.",
  "negative_paths": "The focused research counter consistency FAILED pre-report with exactly the designed AssertionError 89 != 88 (block 89 anticipates this report; 89 .md files at the implementation head count 88 after the 007-o exclusion) - preserved as FAILED, not repaired, rolled back or waived; the report-only commit reconciles it (90 .md files, 89 counted, block 89) and the reconciliation is re-verified privately after publication. The 031-b R13 native bounded round trip is carried unchanged as FAILED (ENVELOPE_INVALID, exact rejected field unknown and undiagnosed; native compatibility and native edit UNPROVEN; sha 296aa8ee0767c0ce5e70d0458f059941185eb285; NOT rerun; ledger exhausted 4/4, no reset/recycling/retry or new live traffic). No retrospective or substituted checks: the preflight proves only 032-a; the carried native result is never relabeled as a rerun; the Probe D first-run stop at R11 on the real index is a provenance-only fixture observation per the Root receipt, not a product failure; the blocking-read supplemental driver is disclosed where PA A6 supports A-FAIL-01, and PD K2 (plus S1) carries the zero-review proof while PC C1, which made one scripted review call, is never cited as zero-call. No target calls, no GET /models, no unauthenticated probes, no live model traffic, no fixed ports. Earlier scratch inspection/generation commands lacking explicit role/umask lines are disclosed per the Root mode receipts (0664 helper modes recorded and corrected), never claimed uniformly qualified.",
  "boundary_fidelity": "Starting from accepted main 2f0d9c4719486b86821c989ec9add9f0254a1e72 (PR 33 merged 2026-11-10T23:01:08Z; local and remote main verified equal, tree d404c7ad...) with no amend, reset or rewrite; the single non-report commit and the report-only commit descend from it on the one branch, and the audited revision is pinned inside the audit artifacts although they are published at 8549db27cb8761e33301f516ef95cae9a0edfb4a... The requirements-first derivation bytes are the exact frozen original (2c589972...): the R2 registry-script change to the uncommitted copy was detected, the initial private artifact was restored verbatim, and Root recorded the actual provenance - the initial derivation and its observed sequence are preserved, not regenerated. The audit and evidence artifacts are final at commit: every post-derivation correction (protection reconciliation, counterexample attribution, citation fixes, cancellation wording, runtime_corpus locators, logical resource references, the 20-test-module inventory) was applied before the commit, and no artifact byte changed afterwards. Literal-execution (S1/S2/PA/PC/PD at the audited SHA), byte-equivalence (carried 031-a/031-b evidence under proved source and dependency equivalence) and Root-verified (strategic receipts by name and SHA-256) provenance are kept strictly separate in every claim.",
  "setup": "Same adopted foreground owner-launched CLI process (same pane, directory, argv, profile, home and authentication; no new agent, CLI, provider, pane or reset; no other agent or historical research scan). The evidence executions S1/S2/PA/PC/PD and the ordered OAP checks used explicit OAP_ROLE=coding, actual shell umask 077 and the qualified Python 3.12.15 with -B and private caches under the scratch root (0700 dirs, 0600 files); several earlier scratch inspection/generation commands omitted some of those settings and created 0664 helpers, recorded and corrected in the Root mode receipts and disclosed in the audit. Probe D used the explicitly supplied installed Pandoc 3.7.0.2 (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229) and the read-only real index (SHA-256 f769235b6af3412e65f0875f4d08231c832f60d8630b43a06ab927c2d32c739f, 7991296 B) plus owned tiny synthetic inputs: a local product execution at the audited SHA with zero network and zero live model calls. The owner key (repo root, 0600, untracked) was read only inside the private known-key scans; never printed, staged or copied. No product runtime change, no service or host mutation, no historical executable or resource search.",
  "privacy": "No raw customer text, prompts or answers, targets or replacements, headers, credentials or native physical host paths in any public artifact; the evidence JSON references resources logically (CONCEPT_PANDOC and REAL_INDEX with their recorded version, SHA-256 and byte size) instead of machine paths. Known-key scans emit PASS/FAIL, counts and affected paths only, never the key value. The twenty Root strategic receipts are cited by name and SHA-256, with independently verified Root evidence kept distinct from the auditor's own probe executions. The private preflight record, key-scan outputs, post-publication counter run and final-head CI observation stay under the private scratch root (0700/0600).",
  "limits": "Audit-only D0: no product, test, dependency or governance byte changed; no local full product or OAP suite, no mypy or Ruff rerun, no native rerun (031-b ledger exhausted 4/4; no reset/recycling/retry); no broader-suite execution beyond the identified gaps (Probe D bounded to the protection, acceptance, quotation, blockquote, raw-tag, cancellation and corpus boundaries). Live model compatibility, corpus coverage and unmeasured linguistic quality are accounted separately; the protected-source gap leaves its rows PARTIAL, not met. No quality, dataset, package, morphology, milestone or deployment claim; deployment_authorized false and human_milestone_accepted false. No future push or CI success is claimed inside this pre-push report (publication_verified false); the four required final-head checks are observed at the published head with actual status and timestamps in the private receipt, not claimed here.",
  "human_gates": "Decision NONE under D0; no human gate created or cleared. Strategy independently verifies the exact head and evidence and performs the conditional development merge; the four required final-head checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) and the independent semantic review precede any development merge, and a missing, pending, cancelled or failed check blocks it. The owner retains final milestone and deployment decisions and excluded a separate human evaluation dataset and a research restart. A fresh current-main architecture audit remains required for any later development-merge acceptance; development merge remains distinct from deployment and from functional readiness.",
  "scope": "Exactly six non-report paths in one non-report commit (oap/orders/032-a-functional-proxy-closure-audit.md, oap/active, oap/audit/results/032-functional-proxy-requirements-first.json at frozen bytes, oap/audit/results/032-functional-proxy-closure-audit.md, oap/audit/results/032-functional-proxy-closure-evidence.json, research/RESEARCH-STATE.md one-line counter 88 -> 89) plus this sole report; PR 34 created new and not amended; no merge. The three unrelated untracked roots, the owner key file, retained branches, archives, the read-only index, private failed epochs and all prior orders, reports and derivations are preserved. No other path mutation.",
  "checks": [
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_ica.py --repo-root . --source oap/audit/results/032-functional-proxy-closure-audit.md --current-main 2f0d9c4719486b86821c989ec9add9f0254a1e72 (umask 077, before the scoped commit)",
      "result": "PASSED",
      "sha": "2f0d9c4719486b86821c989ec9add9f0254a1e72",
      "publication_head_claim": false,
      "details": "RC 0, schema valid at the audited main; gap list = the 13 PARTIAL + 3 ABSENT rows of the 59-row MVP matrix (43 IMPLEMENTED); interpreted at the schema boundary; the same artifact bytes were committed at the implementation head."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (umask 077, at the implementation head)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "RC 0 at the literal implementation head; accepted runtime valid against the trusted governance revision; zero CRIT entries."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py transcript --repo-root . --revision 8549db27cb8761e33301f516ef95cae9a0edfb4a --expected-id 032-a (umask 077, at the implementation head)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "RC 0; report_count 89; active and latest 032-a; frozen mutation paths unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py report-history --repo-root . --revision 8549db27cb8761e33301f516ef95cae9a0edfb4a --require-manifest (umask 077, at the implementation head)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "RC 0; report_count 89; all current generated-file manifest identities verified; frozen mutation paths unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da (umask 077, at the implementation head)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "exactly the five pinned historical incidents (007-e order, 007-f order, 027-a order, 031-a order, 007-d report); RC 0; the 032-a order file is clean."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a (umask 077, at the implementation head)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "exactly the five pinned historical incidents; RC 0 at the literal implementation head."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider research/tests/test_research_state_consistency.py::ResearchStateConsistencyTest::test_registry_and_report_counts -q (umask 077, pre-report stage)",
      "result": "FAILED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "the designed expected pre-report mismatch: assertion oap_reports_reviewed (89) != counted report files (88 = 89 .md files at the implementation head minus the 007-o exclusion); preserved as FAILED - not repaired, rolled back or waived; the report-only commit reconciles it (90 .md files, 89 counted, block 89), re-verified after publication and recorded privately."
    },
    {
      "command": "scope/frozen-byte check: git diff --name-only main..8549db27cb8761e33301f516ef95cae9a0edfb4a; restricted tree diffs (src/, concept-verification/, docs/, oap/bin/, oap/tests/, oap/registry/, PLAN.md, ARCHITECTURE.md, ARCHITECTURE-for-agents.md, SECURITY.md, TESTING.md, AGENTS.md, oap/governance/); requirements-first blob digest; git diff --check on new bytes (umask 077, at the implementation head)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "diff touches exactly the six permitted non-report paths; restricted tree diff empty; the requirements-first committed blob equals the frozen original bytes 2c5899726f4fafa0b080ba63951db613339fe37d566037845c98b037205dd052 (51948 B); all new bytes whitespace-clean with a single final LF."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py preflight-report --repo-root . --id 032-a --source PRIVATE_FINAL_DRAFT (private scratch root, logical name retained privately) --expected-head 8549db27cb8761e33301f516ef95cae9a0edfb4a (umask 077, canonical 032-a report ABSENT)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "actual unpublished preflight executed on the exact final draft while the canonical 032-a report was absent: valid unpublished report draft, expected-head match against the literal implementation head, all check SHAs verified as real ancestor commits; private record retained under the scratch root; the draft was copied to the canonical path only after this pass."
    },
    {
      "command": "private known-key scans: the six staged non-report blobs before the scoped commit and both non-report commit messages; the report draft plus the report commit blob and message before publication (counts only)",
      "result": "PASSED",
      "sha": "8549db27cb8761e33301f516ef95cae9a0edfb4a",
      "publication_head_claim": false,
      "details": "actual owner key value compared privately against the scoped blobs and commit messages; emitted result/counts/affected paths only, never the value; all PASS, count 0, affected none."
    },
    {
      "command": "031-b R13 native bounded round trip (carried forward; NOT rerun under this order)",
      "result": "FAILED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "preserved unchanged: qwen3.8-27b-rtx3090, one main POST plus reserved review slot (ledger 4/4, zero remaining): HTTP 200, 2105 B, 4.721 s; ENVELOPE_INVALID (exact rejected field unknown and undiagnosed); native compatibility and native edit UNPROVEN; review slot RESERVED_UNKNOWN (zero observed calls, no false zero); owned cleanup actually proven (main return 0, worker joined, listener closed, no forced kill, child rc 1); no reset/recycling/retry or new live traffic under this order; earlier A100 15 s/45 s reviewer measurements remain separate evidence."
    }
  ]
}
```

This report is the pre-publication evidence record for round 032-a
(round result COMPLETE for the audit-only functional proxy closure audit).
Publication sequence executed on PR 34: the six-path non-report work committed
and pushed and the PR created before the literal implementation head
8549db27cb8761e33301f516ef95cae9a0edfb4a; the exact final draft validated by
the real unpublished preflight (private source, canonical 032-a report
absent); this report is the sole-path SELF commit with sole literal parent
8549db27cb8761e33301f516ef95cae9a0edfb4a; forward push, normal REMOTE
verification, ONE exact OK response and quiescence follow. The audit records
43 IMPLEMENTED, 13 PARTIAL and 3 ABSENT of the 59-row MVP matrix within the
64-row frozen registry projection, with the protected-quote/HTML first
failing boundary reconciled against the Root counterexample receipts and
independently reproduced offline; this round establishes no functional-MVP
readiness, quality or deployment acceptance. No future push or CI success is
claimed inside this pre-push report (publication_verified false); the four
required final-head CI checks on the published head and Strategy's
independent semantic review remain the development-merge gate.

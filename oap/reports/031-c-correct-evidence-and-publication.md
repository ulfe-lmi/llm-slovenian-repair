# Work report 031-c — Correct execution evidence and complete publication checks

Evidence/publication correction round 031-c on the existing 031 functional-proxy
objective (same branch, same PR 33, AMEND_EXISTING_PR), starting from the
immutable 031-b report head `c29337422d7f1ea84cb8af3ce625b476ff5ffd50`.
**Round result: COMPLETE** - the 031-b report's six material execution/
provenance statements are superseded by the bounded correction artifact
grounded in the actual command history and Root source-bound receipts; the
full publication boundary (actual unpublished preflight with private final
source and canonical report absent, sole-path SELF commit, forward push,
normal REMOTE verification, ONE response) is executed for real in this round.
Product bytes, all prior reports/orders, governance and the manifest stay
byte-frozen; no new native request (ledger exhausted 4/4); no merge, no
milestone or deployment acceptance. The failed RTX 3090 native result and all
other substantive 031-b evidence are preserved unchanged.

```oap-report
{
  "id": "031-c",
  "result": "COMPLETE",
  "order_path": "oap/orders/031-c-correct-evidence-and-publication.md",
  "order_sha256": "e511b5fc49b6ad3d83c855fd1166c65c3c9c69362908bba7c1146168b3eab323",
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
  "implementation_head": "6a971c455832f29583a762d282c238982a749bc8",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 33,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/33",
  "pr_state": "open",
  "branch": "oap/031-functional-proxy-audit",
  "base_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
  "starting_remote_sha": "c29337422d7f1ea84cb8af3ce625b476ff5ffd50",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-10T22:10:50+00:00",
  "report_written_at": "2026-11-10T22:11:30+00:00",
  "implementation": "Two non-report commits on the 031-b report head c293374, same branch: (1) 93d3a15 - NEW oap/audit/results/031-c-evidence-and-publication-correction.md (the bounded correction artifact), NEW oap/orders/031-c-correct-evidence-and-publication.md, oap/active 031-b -> 031-c, research/RESEARCH-STATE.md machine block oap_reports_reviewed 87 -> 88 only (registry 42 and incidents 2 unchanged); (2) 6a971c4 - artifact-only follow-up qualifying the helper-qualification sentence as a going-forward requirement with the prior unestablished role/umask scope disclosed (Root first artifact review 2026-11-10T22:03:25Z). Final literal implementation head 6a971c4; the diff c293374..6a971c4 touches exactly the four allowed non-report paths and nothing else. The PR 33 body was refreshed (22:02:07Z) for the bounded 031-b implementation plus this evidence correction, preserving the failed native result and no acceptance claim.",
  "documentation": "The correction artifact is the sole bounded documentation deliverable: it names the exact prior report bytes (oap/reports/031-b-close-proxy-and-preserve-order.md, 24642 B, SHA-256 d73ec576157f2daba5a6484babe041e8ed9baf51074aae7c04f9d83a215e7788, published at c293374) and supersedes exactly six execution/provenance statements - (1) the actual focused 153/66/114.21 s five-module list (test_main_lifecycle, test_owned_startup, test_request_admission, test_request_cancellation, test_concept) with literal-head 9d5f012 / dirty-source / later-proven-equivalence-to-296aa8ee provenance and the pipeline-tail rc caveat; (2) the actual unittest-based whitespace verification (14 tests, 6.455 s, literal closed 0) with the two file hashes later proven equal to 296aa8ee; (3) FIVE independent 30.0 s main budgets (not 30.0 x4), observed 12 tests + 6 subtests, unsupported 16-scenario count withdrawn; (4) the overbroad every-helper qualified-interpreter/umask claim corrected, with going-forward requirement and prior unestablished scope disclosed; (5) the 031-b unpublished preflight marked NOT RUN/UNPROVEN, never retroactively PASSED, not repaired; (6) published-report framing corrected and the old-bytes negative preserved under its 9d5f012-epoch test-source provenance. Counter 87 -> 88 anticipates this report only: at the 031-b head 88 .md reports (87 counted after the existing 007-o exclusion) reconcile block 87; at this report head 89 .md reports (88 counted) will reconcile block 88. No README/architecture/readiness text changed.",
  "criteria": "A1: MET - the correction artifact resolves every R2 claim against actual execution/source evidence (actual command history, the BUDGETS assertion in test_main_lifecycle.py, the 031-b report bytes and Root source-bound receipts), explicitly supersedes the erroneous claims, and preserves the prior report bytes and the substantive native failure unchanged. A2: MET - product and all other frozen bytes unchanged: git diff c293374..6a971c4 is exactly the four non-report paths; the 031-b report blob (39f3fc18...) is identical at all three heads; product/test/governance/manifest/prior-report trees diff empty; scope is the four non-report paths plus this sole report; the counter advances only 87 -> 88. A3: MET - the actual qualified bounded checks pass at the literal implementation head with correct literal-execution/dirty-source/equivalence labels (governance accepted-runtime, transcript report_count 88, report-history require-manifest report_count 88 with all 173 current identities, both real whitespace CLI bases with exactly five incidents); the expected pre-report counter mismatch (88 != 87) is preserved as FAILED, not repaired; the exact final draft passes the real unpublished preflight with canonical 031-c absent, expected-head 6a971c4, before being copied to the canonical path; publication is the exact sole-path SELF commit with sole literal parent 6a971c4, forward push and normal REMOTE verification. A4: STANDING - all four required final-head checks on the exact final remote head (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) and Root's independent semantic review precede any expected-head development merge; missing/pending/cancelled/failed checks block merge; this round establishes no native compatibility, functional-MVP readiness, quality or deployment acceptance.",
  "negative_paths": "Focused research counter consistency at the implementation head (pre-report stage) FAILED with exactly the expected 88 != 87 assertion (block 88 anticipates this report; 88 .md files at the head count 87 after the 007-o exclusion) - preserved as the designed pre-report mismatch, not repaired, rolled back or waived. The 031-b preflight-report boundary is NOT RUN/UNPROVEN and is never retroactively labeled PASSED; no retrospective preflight was faked; this round's preflight proves only 031-c. The earlier 031-c invocations lacking explicit role/umask lines in their command texts are disclosed as unestablished scope (no inherited environment value asserted), not claimed uniformly qualified. The old-bytes regression negative of 031-b is preserved under its 9d5f012-epoch product/test-source provenance, not relabeled as a literal rerun at 296aa8ee. No target calls, no GET /models, no unauthenticated probes, no fixed ports; the native ledger stays 4/4 with no reset/recycling/retry. No fake check below its named boundary was invented or substituted.",
  "boundary_fidelity": "Starting head c293374 (031-b report, sole parent 296aa8ee) and all earlier history preserved exactly; no amend/reset/rewrite of the 031-b report; both non-report commits descend from that exact head on the same branch. The 031-b report bytes are immutable across c293374/93d3a15/6a971c4 (blob 39f3fc18..., 24642 B, d73ec576...). The failed actual RTX 3090 native result is preserved verbatim (HTTP 200, 2105 B, 4.721 s, ENVELOPE_INVALID, exact rejected field unknown and undiagnosed, native compatibility/edit UNPROVEN; main return 0, no main error, shutdown finished, worker joined, listener closed, child rc 1, no forced kill; review slot RESERVED_UNKNOWN with 0 observed calls; ledger 4/4; A100 15/45 s measurements separate). No protection or product mutation chased the unlocalized failure. All literal-execution vs dirty-source vs byte-equivalence distinctions are kept separate in every check label; equivalence to 296aa8ee is cited where Root proved it and never relabeled as an execution at that SHA.",
  "setup": "Same adopted foreground owner CLI (same process, cwd, argv, profile, home, auth; no new agent/CLI/provider/pane/reset; no other agent or historical research scan). All Python helpers in this round used the qualified Python 3.12.15 with -B and private cache roots. Per Root's first artifact review (2026-11-10T22:03:25Z), every new shared-check, preflight and publication helper invocation from that point is actually prefixed with explicit OAP_ROLE=coding, actual shell umask 077 and the qualified interpreter; the 031-c invocations before that review had no explicit role/umask lines in their command texts (qualified interpreter used for the Python writer/scan commands; no inherited environment value is asserted) and remain disclosed as unestablished scope. The owner key (repo root, 0600, untracked, locally excluded) was read only inside the private known-key scans; never printed, staged or copied. No product runtime or Pandoc execution, no network/model/server/port/GPU mutation, no historical executable/resource search.",
  "privacy": "No raw customer text, prompts/answers, targets/replacements, headers, credentials or native physical paths in any public artifact; public prose uses logical roots and supplied private evidence references; known-key scans emit only PASS/FAIL, counts and affected paths, never the key; the private preflight record, key-scan outputs and post-publication counter run stay under the private scratch root (0700/0600).",
  "limits": "Metadata-only correction: no product/test/dependency/governance byte changed, no local full product/OAP suite, no mypy/Ruff rerun, no native rerun, no broad-suite or count-chasing execution; final CI supplies the required broader regressions on the published head. The native compatibility/edit layers remain UNPROVEN with the ledger exhausted 4/4 (no further request possible under this order regardless of any separately discussed future allowance). No future push/CI success is claimed inside this pre-push report (publication_verified false); the interim observation recorded in the order metadata (Research reproducibility run 42907565735 success at the 031-b head; other current-head checks pending when the order was drafted) is cited as observed, not as a claim at this head. No quality, dataset, package, morphology, milestone or deployment claim.",
  "human_gates": "Decision NONE under D0; no human gate created or cleared. Root's independent semantic review of the published exact head/report and all four required final-head CI checks precede any expected-head development merge; a missing/pending/cancelled/failed check blocks merge. The 031-a private-byte gate remains mandatory for that prior round; the 031-b report remains immutable and its PARTIAL round result stands for that round. The human retains final milestone labeling and release/deployment authority; none is claimed. A fresh current-main architecture audit remains required for any later development-merge acceptance; development merge remains distinct from deployment and functional readiness.",
  "scope": "Exactly four non-report paths across two non-report commits (oap/audit/results/031-c-evidence-and-publication-correction.md, oap/orders/031-c-correct-evidence-and-publication.md, oap/active, research/RESEARCH-STATE.md one-line counter 87 -> 88) plus this sole report; PR 33 amended in place (031-c correction paragraph, failed native result preserved, no acceptance claim). The three unrelated untracked roots, the owner key file, retained branches, archives, the read-only index, private failed epochs and all prior orders/reports/derivations are preserved. No other path mutation.",
  "checks": [
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (umask 077)",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "RC 0 at the literal implementation head; explicit OAP_ROLE=coding prefix, qualified interpreter -B, umask 077; accepted runtime valid, zero CRIT entries."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py transcript --repo-root . --revision 6a971c455832f29583a762d282c238982a749bc8 (umask 077)",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "RC 0; report_count 88; active=latest=031-c; frozen mutation paths unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py report-history --repo-root . --revision 6a971c455832f29583a762d282c238982a749bc8 --require-manifest (umask 077)",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "RC 0; report_count 88; all 173 current generated-file identities verified; frozen mutation paths (006-a, 006-c) unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da (umask 077)",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "exactly five incidents (007-e order, 007-f order, 027-a order, 031-a order:161, 007-d report), RC 0 at the literal implementation head; closed-five contract unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a (umask 077)",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "identical five-incident set, RC 0 at the literal implementation head."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider research/tests/test_research_state_consistency.py::ResearchStateConsistencyTest::test_registry_and_report_counts -q (umask 077, pre-report stage)",
      "result": "FAILED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "the designed expected pre-report mismatch: assertion oap_reports_reviewed (88) != counted report files (87 = 88 .md minus the 007-o exclusion); same assertion observed at 93d3a15; preserved as FAILED - not rolled back, repaired or waived; the report-only commit reconciles it (89 .md, 88 counted, block 88), re-verified after publication and recorded privately."
    },
    {
      "command": "scope/frozen-byte check: git diff c293374..6a971c4 name-only; 031-b report blob identity; product/test/governance/manifest/prior-report tree diffs",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "diff touches exactly the four allowed non-report paths; 031-b report blob 39f3fc18... identical at c293374/93d3a15/6a971c4; restricted tree diff (concept-verification/, docs/, oap/bin/, oap/tests/, oap/governance/, oap/prompts/, oap/strategic-instructions/, oap/reports/, the seven root governance files, research/registry/, oap/GENERATED-FILES.json) is empty; all newly written bytes whitespace-clean (git diff --check RC 0, no tabs/trailing whitespace, single final LF)."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py preflight-report --repo-root . --id 031-c --source PRIVATE_FINAL_DRAFT (private scratch root, logical name retained privately) --expected-head 6a971c455832f29583a762d282c238982a749bc8 (umask 077, canonical 031-c report ABSENT)",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "actual unpublished preflight executed on the exact final draft while the canonical 031-c report was absent: 'valid unpublished report draft', expected-head match against the literal implementation head, all check SHAs verified as real ancestor commits; private record retained under the scratch root; the draft was copied to the canonical path only after this pass; no retrospective 031-b preflight was run or claimed."
    },
    {
      "command": "private known-key scans: staged non-report blobs before each non-report commit; report draft + all new commit messages/blobs before publication",
      "result": "PASSED",
      "sha": "6a971c455832f29583a762d282c238982a749bc8",
      "publication_head_claim": false,
      "details": "actual owner key value compared privately against the scoped staged blobs (non-report commit 1: 4 blobs; follow-up commit: 1 blob; report commit: 1 blob) and against the report draft and every new commit message/blob; emitted result/counts/affected paths only, never the value; all PASS count=0 affected=none."
    },
    {
      "command": "031-b R13 native bounded round trip (carried forward; NOT rerun under this order)",
      "result": "FAILED",
      "sha": "296aa8ee0767c0ce5e70d0458f059941185eb285",
      "publication_head_claim": false,
      "details": "preserved unchanged: qwen3.8-27b-rtx3090, one main POST + reserved review slot (ledger 4/4, 0 remaining): HTTP 200, 2105 B, 4.721 s; ENVELOPE_INVALID (exact rejected field unknown and undiagnosed); native edit UNPROVEN; review slot RESERVED_UNKNOWN (0 calls observed, no false zero); owned cleanup actually proven (main return 0, worker joined, listener closed, no forced kill, child rc 1); no reset/recycling/retry or new live traffic under this order, regardless of any separately discussed future allowance; earlier A100 15 s/45 s reviewer measurements remain separate evidence."
    }
  ]
}
```

This report is the pre-publication evidence record for round 031-c
(round result COMPLETE for the bounded evidence/publication correction).
Publication sequence executed on the same PR 33: non-report work committed
and pushed and PR refreshed before the literal implementation head
`6a971c455832f29583a762d282c238982a749bc8`; exact final draft validated by
the real unpublished preflight (private source, canonical absent); this
report is the sole-path SELF commit with sole literal parent
`6a971c455832f29583a762d282c238982a749bc8`; forward push, normal REMOTE
verification, ONE exact OK response and quiescence follow. No future push/CI
success is claimed inside this pre-push report (`publication_verified:
false`); all four required final-head CI checks on the published head and
Root's independent semantic review remain the development-merge gate, and
this round establishes no native compatibility, functional-MVP readiness,
quality or deployment acceptance.

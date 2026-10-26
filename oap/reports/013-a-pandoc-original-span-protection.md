# Work report 013-a - Mandatory Pandoc original-span protection in the runnable proxy (objective 013, round 1; CREATE_NEW_PR; PR #15 open; branch retained)

```oap-report
{
  "id": "013-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/013-a-pandoc-original-span-protection.md",
  "order_sha256": "285e5538b604dd66d536e8e2afeefbd9a5b058f6795894ae3958674326206031",
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
  "implementation_head": "d4ad6301cd42781792384062622bf232270a5102",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 15,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/15",
  "pr_state": "open",
  "branch": "oap/013-pandoc-original-span-protection",
  "base_sha": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "starting_remote_sha": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-26T03:45:00+00:00",
  "report_written_at": "2026-10-26T03:47:22+00:00",
  "checks": [
    {
      "command": "A1/A4 - mandatory qualified-Pandoc startup on the actual proxy path; no pulldown discovery or fallback; fail-closed engine boundary before corpus/detect/reviewer",
      "result": "PASSED",
      "details": "Focused actual-Pandoc suite (67 protection + 19 concept tests, 86 total, 3 subtests) on pre-commit candidate bytes with the exact Python 3.12.15 interpreter (-B, REPAIR_ALLOW_LIVE_TESTS=NO) under both the local Debian pandoc 3.7.0.2 and the official static archive 3.7.0.2 binary (strategy-independently re-run; private receipts record the dirty-candidate source hashes and the binary hash). A missing dependency fails rather than skips. The startup check (executable presence, exact version, reader capability) runs before the HTTP bind. The engine boundary is proven with a reviewer that fails if called and a corpus-open sentinel: every parse/map failure (malformed JSON, valid-JSON invalid schema, nonzero exit, runtime timeout, oversized input) returns the byte-exact original with zero review calls before corpus access. A no-pulldown-invocation proof runs on the actual proxy path.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "A2/A3 - exact original-span mapping and full protection on the actual pinned binary",
      "result": "PASSED",
      "details": "Useful positives: NFC Slovenian prose with and without a final LF, emoji prefixes, lists, emphasis, and prose around protected content grant exact original spans. Trap cases: NFD lines abstain per line, control characters (including NEL/LS/PS/CR) are never granted, tabs follow the documented tab-stop rule, duplicate data-pos defeats provenance for the conflicting node only, repeated words, CRLF, combining marks, ZWJ/variation selectors, HTML interiors (including raw-inline inner text), link/image labels, configuration and TeX/XML residual fragments, and unterminated prose-form TeX remain protected in the final composed intervals (point-level coverage asserted, not raw-grant absence). Whole-document failure returns the exact original with zero review calls.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "A5 - original-slice patch boundary (stale, overlapping, out-of-bounds, protected, grapheme-split)",
      "result": "PASSED",
      "details": "accept() validates candidate bounds (0 <= start < end <= len), exact original-slice equality, and neighbor bounds using the tokenizer key convention before any corpus access; stale-candidate-bounds, stale-neighbor-bounds, and barrier-between-neighbor rejections are proven (a protected interval strictly between a neighbor and the candidate blocks acceptance), as is the grapheme-sensitive split rejection; edits apply right-to-left with unchanged unapproved slices and no Markdown regeneration.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Requirement 8 - bounded streaming capture and owned cleanup on every exit path",
      "result": "PASSED",
      "details": "Real-child cases: write-before-read without deadlock, early exit, timeout group kill, flood with immediate cap enforcement, selector allocation failure (child group signalled, pipes closed, unrelated sentinel process preserved, FD count restored), and timeout with a descendant that outlived the parent and retained a pipe (descendant killed via the owned group). All exit paths close the selector and pipes; the owned session is signalled unconditionally in cleanup. The two new regressions fail when the pre-fix setup ordering or conditional kill is reintroduced (checked on scratch copies).",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Frozen historical research protection suites run unchanged",
      "result": "PASSED",
      "details": "test_parser_first_protection (48 ran, 9 skipped), test_raw_document_fragment_protection (34 ran, 12 skipped), test_008h_dialect_edge_protection (44 ran, 17 skipped), test_008i_composition_and_class_boundary (38 ran, 15 skipped) - all OK through unittest discovery with the Python 3.12 interpreter. Skips are historical pinned-helper unavailability and are not Pandoc evidence.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the changed files",
      "result": "PASSED",
      "details": "Ruff (E,F,I,UP,B,SIM; line length 100) clean on every changed Python file. mypy 2.3.1 clean on the seven changed-module set; because the concept-verification package __init__ name is invalid for in-place checking, mypy ran on a byte-identical scratch copy with the actual repository import context (MYPYPATH at the repo root); no import ignores were added. Scope recorded here, not claimed for the whole repository.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Report bookkeeping: counter 62 -> 63 for final publication; no registry entry",
      "result": "PASSED",
      "details": "research/RESEARCH-STATE.md advances oap_reports_reviewed to 63 only (registry_entries 42 and frozen_report_history_incidents 2 unchanged; identity fields unchanged). test_research_state_consistency shows the designed implementation-head report-count red (63 vs 62) that clears at the report commit; the implementation-head CI job confirms failures=1 (AssertionError 63 != 62) with skipped=53 and no other failure.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist at the implementation head",
      "result": "PASSED",
      "details": "Implementation head d4ad6301cd42781792384062622bf232270a5102 (sole parent 3549de2a436f485a693730d0ee7d5f8c00aec0c0) changes exactly the 18 authorized paths: five concept-verification Python modules, four new concept-verification files (pandoc_protection.py, protection_residuals.py, install_pandoc.sh, pandoc-dependency.json), the new focused test module, concept-verification/README.md, the workflow install step, README.md, docs/DEVELOPMENT.md, STATUS.md, oap/GENERATED-FILES.json (affected pins only; existing Unicode key serialization preserved), oap/active, the new 013-a order, and research/RESEARCH-STATE.md. Prior orders/reports and frozen research are byte-identical at the head; all 173 GENERATED-FILES pins verify against the committed tree; git diff --check is clean; the tracked tree is clean.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI (observed so far)",
      "result": "PENDING",
      "details": "Research reproducibility (implementation head) FAILED solely on the designed report-count red (63 vs 62; failures=1, skipped=53; the captured 'synthetic worker setup failure' line is the deliberate broken-factory negative of test_strategic_addendum_fidelity). Application baseline and OAP bootstrap were in progress at report-writing time. The OAP report-history job is observed at the final report head.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final report head are strategic post-publication evidence and cannot be claimed by this prewritten report.",
      "sha": "d4ad6301cd42781792384062622bf232270a5102",
      "publication_head_claim": false
    }
  ],
  "implementation": "New concept-verification/pandoc_protection.py: fixed commonmark_x+sourcepos-smart -> json profile, NFC-line code-point column model with the documented tab-stop rule, per-node data-pos provenance, deny-by-default exact original-span Str grants (valid coordinates, exact original-slice equality, grapheme-safe content and boundaries, NFC-stable line) with whitespace glue only in a proven shared prose context, virtual no-final-LF container endpoints never granted, and bounded multiplexed subprocess capture (argv only, no shell; finite input/output/timeout/node limits; immediate output cap; content-free diagnostics; unconditional owned group cleanup). New concept-verification/protection_residuals.py: the established pure research residual policy reused as a pure function (no helper discovery) plus one bounded proxy-side addition for unterminated prose-form TeX. proxy.py: Reviewer protocol, mandatory startup check before bind, fail-closed original before corpus/detect/reviewer, ReviewEngine wiring. repair.py: acceptance bounds, neighbor bounds in the tokenizer key convention, barrier-aware neighbor rejection, grapheme-split rejection. protected.py: Pandoc-backed protected_intervals composition with residual retention over granted prose. config.py: bounded parser configuration constants. concept-verification/install_pandoc.sh and pandoc-dependency.json: pinned 3.7.0.2 dependency record (byte count + locally computed SHA-256) and owned-prefix-only installer. The application-baseline workflow installs the pinned archive into a runner-owned temporary prefix and exports CONCEPT_PANDOC for the actual integration tests; no other step, trigger, or timeout was touched.",
  "documentation": "concept-verification/README.md documents the exact reader profile, coordinate conventions (NFC line model, tab-stop rule, data-pos provenance, virtual container endpoints, multi-line positions never granted), the deny-by-default grant policy, documented conservative abstentions, the dependency pin/installation/startup behavior, and the bounded startup-versus-runtime failure behavior; docs/DEVELOPMENT.md records the development dependency and CI installation; README.md and STATUS.md carry the directly affected status statements. The publication proof alone does not establish integration or scientific acceptance; any later main ancestry must be verified separately.",
  "criteria": "A1 SATISFIED (observed): the runnable proxy requires the qualified pinned Pandoc at startup with the explicit installed dependency and no historical discovery or fallback (focused suite; startup before bind). A2 SATISFIED (observed): useful exact original-span positives and trap-case abstentions/protection on the actual pinned binary (both local Debian and official static 3.7.0.2). A3 SATISFIED (observed): code, equations, HTML, link destinations/images with labels, configuration and machine fragments stay protected; barrier-aware neighbors at detector and acceptance. A4 SATISFIED (observed): parse/map failure returns only the safely completed original before corpus/detection/reviewer, with explicit missing/wrong-version/startup and runtime timeout/nonzero/malformed cases. A5 SATISFIED (observed): original-slice patching rejects stale, overlapping, out-of-bounds, protected and grapheme-splitting edits. A6 PARTIALLY OBSERVED: the focused actual-Pandoc/proxy tests and the frozen research suites pass; the required final-head CI is PENDING as recorded (strategic post-publication evidence).",
  "negative_paths": "No pulldown-cmark discovery or invocation on the proxy path; no regex-only runtime structural path; no substring position recovery; no AST-to-Markdown answer rendering; no scientific protocol, dataset, model, prompt, corpus, scoring or result change; no live Qwen/GPU/service/port/network or credential change; no deployment; no merge or auto-merge; no registry entry; no edits outside the ordered allowlist; concept-verification/tests/test_concept.py is byte-unchanged; frozen research bytes unchanged.",
  "boundary_fidelity": "The proxy entry chain (run_proxy.sh -> proxy.main -> RepairEngine.repair -> protected_intervals/detect/accept/apply_edits) is preserved; upstream incomplete-main and capture-error semantics are unchanged (parse/map failures do not broaden exception handling around incomplete main responses); the detector's existing open-gap adjacency semantics are retained with the new acceptance barrier; historical research label-exposure policy remains a distinct, unchanged policy.",
  "setup": "External Python 3.12.15 interpreter (/home/janezp/envs/llm-slovenian-repair/bin/python) with -B for all ordered test suites, static analysis, and OAP helpers; REPAIR_ALLOW_LIVE_TESTS=NO; owned scratch TMPDIR under the strategic home. Pandoc qualified read-only from /usr/bin/pandoc (Debian 3.7.0.2) and from the installer-owned official static archive (3.7.0.2) in an owned prefix; no bare uv, no repository .venv change. mypy ran on a byte-identical scratch copy with the actual repository import context (MYPYPATH); scope recorded in the checks. The only bare-python invocations were trivial syntax parses of candidate files during development; no test evidence derives from them.",
  "privacy": "Synthetic fixtures only; no customer data, credential, private raw text, or private path in the report or logs; private receipts are metadata-only (source hashes, binary hash, test counts); diagnostics are bounded and content-free by construction (stderr drained and never retained).",
  "limits": "Focused suites ran on pre-commit candidate bytes at base 3549de2 (dirty-candidate limitation); after those runs only documentation, the report counter, and generated pins changed (not exercised by the test suites), and the commit-shape check confirms the committed census at the implementation head. The local Debian binary and the official static binary are both 3.7.0.2 and both qualified; they are not assumed behavior-identical beyond the passing suites. Final report-head CI is PENDING. The mypy scope is the changed module set, not the whole repository.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered allowlist: the five listed concept-verification Python modules (detector.py untouched - its existing open-gap semantics already carry the detector-side barrier), the two new concept-verification modules, run_proxy.sh untouched (its python3.12 interpreter line is a version-pinned interpreter name, not bare uv or a repository .venv), README.md, the installer and dependency record, the workflow install step, the two new test-adjacent additions, README.md, docs/DEVELOPMENT.md, STATUS.md, research/RESEARCH-STATE.md (counter only), the affected GENERATED-FILES pins, this order, the active pointer, and this report. No other paths or governance changes.",
  "result_summary": "013-a implemented the owner-selected mandatory Pandoc structural protection with exact original spans in the runnable concept-verification proxy: pinned 3.7.0.2 dependency with startup qualification before traffic, deny-by-default exact-span grants with documented conservative abstentions, established residual policy reused as additional protection, bounded fail-closed failure behavior with owned cleanup on every exit path, and the acceptance barrier/bounds fix. Focused actual-Pandoc and frozen research suites pass on the exact Python 3.12 interpreter; the required final-head CI is PENDING as recorded. No linguistic, experimental-MVP, or deployment acceptance; no merge; PR #15 stays OPEN pending strategy review."
}
```

## Short factual summary

013-a replaced the runnable concept-verification proxy's structural protection with mandatory installed Pandoc 3.7.0.2 and validated original coordinates (fixed commonmark_x+sourcepos-smart -> json profile; NFC-line code-point column model; per-node data-pos provenance; deny-by-default exact original-span grants; established pure research residual policy reused plus one bounded proxy-side unterminated-TeX addition; bounded multiplexed subprocess capture with unconditional owned group cleanup; acceptance bounds and barrier fix). The focused actual-Pandoc suite (86 tests) passed on the exact Python 3.12 interpreter under both the local Debian and the official static 3.7.0.2 binaries on pre-commit candidate bytes; the four named frozen research protection suites ran unchanged (OK with historical optional-helper skips); the report counter advanced 62 -> 63 for final publication. The implementation-head Research reproducibility CI failed solely on the designed report-count red (63 vs 62); Application baseline and OAP bootstrap were in progress and all four required final-head checks are PENDING as strategic post-publication evidence. No scientific, deployment, or acceptance change; no merge; PR #15 stays OPEN.

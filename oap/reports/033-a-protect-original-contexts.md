````oap-report
{
  "id": "033-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/033-a-protect-original-contexts.md",
  "order_sha256": "35885a036728dba7e870cab603ed0b0e655cced558575ba53b66536fc6c77dad",
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
  "implementation_head": "e401852dc561900dd8d671f44660a92473ccf3ea",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 35,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/35",
  "pr_state": "open",
  "branch": "oap/033-protected-quote-html-contexts",
  "base_sha": "ad513664d5a02488c3447e786f1595c146fe249c",
  "starting_remote_sha": "ad513664d5a02488c3447e786f1595c146fe249c",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-11T07:55:18+00:00",
  "report_written_at": "2026-11-11T07:55:18+00:00",
  "implementation": "Three forward non-report commits on branch oap/033-protected-quote-html-contexts descending from the accepted base ad513664 (no amend/reset/rewrite; PR 35, NEW_PR). (1) 6ae0e784: the document-level source-ordered finalization - coalesce repeated physical Note payloads, replay quote/HTML context stacks sorted by proven source position, filter exact-source candidate grants against the merged denied intervals via standard-library binary search over sorted endpoints (D0); distinct quotation families (Slovenian low/high double, both guillemet directions, curly/straight double and single) with same-provenance closer release only; complete BlockQuote structures denied in full with a proven denial extent; the six permitted non-report paths plus the machine counter 90 -> 91. (2) c21c784: Root independent regression-review corrections - R3 adds the Slovenian low/high single family U+201A...U+2018 (the closing U+2018 no longer opens a spurious unclosed curly-single level that denied the outside token while granting the protected interior); R4 adds the Engine recorded quoted repeated-note source-order control; R9/A1 embeds and replays the exact 18 preserved old-baseline synthetic vectors (14 red + 4 controls) at the mapper level with independent original-source oracles (required protected range fully protected, non-ordinary target occurrences not granted, ordinary outside occurrence granted) covering the old opener-inside/target-outside emphasis shape, plus the literal-outer/entity-inner cross-family non-release case; R10 makes the owned no-edit upstream source deliberately non-canonical (indent + trailing newline) so exact no-edit envelope-byte preservation is meaningfully exercised. (3) e401852 (literal implementation head, sole parent c21c784): the R2/R7 conservative original-source bounds correction - _segment_offset no longer converts reader sourcepos columns measured on an NFC-normalized line into a guessed original offset when the original line is not NFC-stable (and additionally validates the offset against the document bound), so an unproved quotation/HTML extent on a non-NFC-stable line is rejected and the existing fail-closed rule retains a conservative original line/document denial instead of dropping a degenerate (past-line/past-EOF) interval. The proved ordinary-span converter (map_span/map_block_span) and all valid compound LF/CRLF and useful outside repairs are unchanged; no normalization/regeneration, substring recovery, opener ignore, protection weakening or parser substitution. PR 35 head pinned at the literal implementation head before report composition.",
  "documentation": "The concept-verification README protection section documents the source-ordered protected contexts: the quotation-family list now names the Slovenian low/high single U+201A...U+2018 alongside the double, and the existing prose already states that an unproved extent protects to the end of the document and that every unprovable region is protected - the R2/R7 correction makes a non-NFC-stable-line structural extent unproved and therefore fail-closed, which that prose already covers, so no further documentation byte changed for this precise behavior beyond the family-list update.",
  "criteria": "A1: MET - the old-byte baseline is preserved immutable (probe_d receipt) and the corrected code replays the exact 18 owned old-baseline synthetic vectors (14 red + 4 controls) through the actual pinned mapper with independent original-source oracles: each required protected range stays fully protected, every non-ordinary target occurrence is not granted, and the ordinary outside occurrence is granted (R14 outside-only duplicate; K1 useful outside; K2 zero-call; K3/K4 protected controls); the R2/R7 actual pinned map/compose/Engine fail-open repros are fixed to byte-exact original with zero candidates/review against independent original protected ranges. A2: MET - the existing useful behavior and machine-content protection hold under the positive controls, Unicode/malformed cases, compound source positions and physical footnote ordering (base 83 and all focused7 negatives retained); every approved edit is exactly one approved original slice with all other code points preserved (Engine outside-only and recorded source-order controls). A3: MET at the literal implementation head for every check actually run: focused 7-file suite 436 passed, two-file Ruff clean, strict flat-shadow mypy clean (byte-identical shadow, real imports, no relaxation), and the same bounded 3-size observation 0.229/0.403/0.808 s with all exact outside grants correct (earlier quadratic/indexed/R3 epochs preserved, not a timing SLO). A4: MET at the literal final head - accepted-runtime governance RC 0, transcript report_count 91, report-history with required manifest report_count 91, both accepted whitespace bases with exactly the five pinned incidents, exact six-path scope with empty restricted tree diff and clean diff --check, the designed pre-report counter mismatch recorded separately as FAILED (91 != 90), and owner-key count-only scans (0) over the changed blobs, all branch commit messages and the private report draft; no future check is claimed as executed.",
  "negative_paths": "The pre-report research counter consistency at the implementation head FAILED with exactly the designed mismatch (AssertionError 91 != 90: machine block oap_reports_reviewed 91 anticipates this report; 90 .md files at the implementation head count after the 007-o exclusion) - preserved as FAILED, not repaired or waived; the report-only commit reconciles it (91 counted, block 91) and the actual post-publication reconciliation is recorded only in the private receipt. The R2/R7 fail-open repros are recorded as FAILED at the pre-fix source ef450574 (the motivating evidence) and PASS at the literal implementation head. The added 033-a JSON/HTTP R10 tests script the batch reviewer at the engine seam only (real proxy/worker/Pandoc/detector/acceptor/patcher, fake only the external main endpoint) and do NOT exercise the real ResponsesReviewer HTTP transport - that boundary is the frozen test_responses_contract.py in the focused7 suite; no native or model serving success is claimed from either. No target calls, no GET /models, no unauthenticated probes, no live model traffic (main model traffic zero), no fixed ports. No future push or CI success is claimed inside this pre-push report (publication_verified false).",
  "boundary_fidelity": "Descends from the accepted base ad513664 with no amend, reset or rewrite; the three forward non-report commits (6ae0e784, c21c784, e401852) keep all product bytes frozen at each predecessor head (each correction commit touches only concept-verification/pandoc_protection.py and concept-verification/tests/test_pandoc_protection.py; 6ae0e78 touched the six permitted non-report paths and the 90 -> 91 counter). The exact R2/R7 and R3/R4/R9-A1/R10 owned synthetic inputs and their independent original-source oracles are Root receipts (root-NFC-expansion-unproved-quote/HTML-synthetic-input.json, root-quoted-note-and-lowhigh-single-engine-review, root-exact-old-18-synthetic-protection-vectors.json, root-source-order-and-lowhigh-single-synthetic-inputs.json); every input hash matched the preserved baseline. The prior 87/434/static/slow/failure evidence is preserved as older epochs, not overwritten.",
  "setup": "Same adopted foreground owner-launched CLI process and existing chat (same PID 3341327, cwd, argv, profile, home and authentication; no new agent, CLI, provider, pane or reset; no context reset). Shared checks and scans used explicit OAP_ROLE=coding, actual shell umask 077 and the qualified Python 3.12.15 with -B, the ordered pinned installed Pandoc (3.7.0.2) via CONCEPT_PANDOC, and the private 033a scratch/cache under STRATEGIC_HOME (0700/0600). Actual setup disclosure (honest incident report): during an earlier diagnostic step a pkill -f process-pattern cleanup was run OUTSIDE the ordered owned-child boundary; its shell exited 143 and the external matching-process effect is UNKNOWN, so no pristine-environment claim is made for that step. Five misplaced diagnostic objects were preserved unchanged under the private scratch with strict modes (root receipt 033a-root-misplaced-foreground-diagnostic-preservation-and-mode-repair-20261111.json); early scratch runs that used wrong-location objects and unqualified /usr/bin/pandoc + REPO_ROOT/.venv/bin/python are NOT qualified pinned-Pandoc evidence and are not claimed as such. Every subsequent helper sets umask 077 first and uses the qualified pinned Pandoc and qualified Python. The owner key was read only inside the private count-only key scans; never printed, staged or copied; output is counts only. No live product-model request, no GPU/service/network/auth mutation, no process-pattern kill.",
  "privacy": "No raw customer text, prompts or answers, targets or replacements, headers, credentials or native physical host paths in public evidence; the report cites logical identifiers, SHAs, receipt names and count-only key-scan results; the private receipts (3-size observations, fail-open repros, key-scan outputs, preflight record, post-publication counter/REMOTE/CI observations) stay under the private 033a scratch root (0700/0600); Root receipts are cited by name and the specific observed values this round needed.",
  "limits": "Evidence and in-scope bug correction only: no new dependency, dataset, research restart, source-law, projection, manifest, audit or prior-report byte changed; no parser substitution, position regeneration, substring recovery or protection weakening; no functional-MVP readiness, linguistic-quality, milestone or deployment acceptance; the four required final-head CI checks on the published head and Strategy's independent semantic review remain the development-merge gate. No future push or CI success is claimed inside this pre-push report (publication_verified false); final-head CI observations and post-push REMOTE results are private post-observation records.",
  "human_gates": "Decision NONE under D0; no human gate created or cleared. Root independently reviews the exact final remote head and owns the conditional development merge; the four required final-head checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) and the independent semantic review precede any development merge, and a missing, pending, cancelled or failed check blocks it. The owner retains final milestone and deployment decisions; development merge remains distinct from deployment and from functional readiness.",
  "scope": "Exactly the six permitted non-report paths across the three forward non-report commits (oap/orders/033-a-protect-original-contexts.md, concept-verification/pandoc_protection.py, concept-verification/tests/test_pandoc_protection.py, concept-verification/README.md, oap/active, research/RESEARCH-STATE.md one-line counter 90 -> 91) plus this sole report; PR 35 created and kept in place across recovery; no merge. The three unrelated untracked roots, the owner key, retained branches, archives, the read-only index and all prior orders, reports and derivations are preserved. No other path mutation.",
  "checks": [
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0 (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "RC 0 at the literal implementation head e401852; accepted runtime valid against the trusted governance revision; zero CRIT entries."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py transcript --repo-root . --revision e401852dc561900dd8d671f44660a92473ccf3ea --expected-id 033-a (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "RC 0; report_count 91; active and latest 033-a; frozen mutation paths unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py report-history --repo-root . --revision e401852dc561900dd8d671f44660a92473ccf3ea --require-manifest (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "RC 0; report_count 91; all current generated-file manifest identities verified; frozen mutation paths unchanged."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "exactly the five pinned historical incidents (007-e order, 007-f order, 027-a order, 031-a order, 007-d report); RC 0."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "exactly the five pinned historical incidents; RC 0 at the literal implementation head."
    },
    {
      "command": "scope/frozen-byte check: git diff --name-only ad513664..e401852; restricted tree diffs (src/, concept-verification/ non-changed, docs/, oap/bin/, oap/tests/, oap/registry/, oap/governance/, oap/prompts/, oap/strategic-instructions/, oap/reports/, PLAN.md, ARCHITECTURE.md, ARCHITECTURE-for-agents.md, SECURITY.md, TESTING.md, AGENTS.md); git diff --check on new bytes (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "the branch diff touches exactly the six permitted non-report paths (oap/orders/033-a-protect-original-contexts.md, concept-verification/pandoc_protection.py, concept-verification/tests/test_pandoc_protection.py, concept-verification/README.md, oap/active, research/RESEARCH-STATE.md one-line counter 90 -> 91); restricted tree diff for every other path empty; all new bytes whitespace-clean."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider concept-verification/tests/test_pandoc_protection.py (umask 077, CONCEPT_PANDOC pinned 3.7.0.2, private TMP/cache, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "89 passed (base 83; +4 R3/R4/R9-A1/R10 corrections; +2 R2/R7 NFC-unstable-line regressions). Real pinned-Pandoc map/compose/Engine coverage; no skips."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider concept-verification/tests/{test_pandoc_protection,test_responses_contract,test_runtime_detection,test_runtime_acceptance,test_composed_validation,test_analysis_policy,test_review_batch}.py (umask 077, pinned Pandoc, private scratch, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "focused 7-file suite 436 passed (base 430; +6). The frozen test_responses_contract real-HTTP harness is part of this suite and is the real ResponsesReviewer HTTP-transport boundary, which the added 033-a JSON/HTTP tests deliberately do not exercise."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B -m ruff check --no-cache --config pyproject.toml concept-verification/pandoc_protection.py concept-verification/tests/test_pandoc_protection.py (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "two-file Ruff clean at the final bytes (source SHA-256 27fe01c... blob 6f3f316...; test SHA-256 f703898... blob dcaa31d...)."
    },
    {
      "command": "flat-shadow strict mypy: copy the two final files byte-identically to a fresh private shadow; qualified python -B -m mypy --config-file PRIVATE_MINIMAL_CONFIG(python_version 3.12, strict, follow_imports silent) --no-incremental --cache-dir PRIVATE_FRESH_CACHE shadow/pandoc_protection.py shadow/test_pandoc_protection.py with MYPYPATH ordered shadow:concept-verification:src:repo-root (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "strict flat-shadow mypy clean (shadow byte-identical to the final WIP files); no import skipping/ignoring, no broad Any, no per-file relaxation; actual imported types preserved."
    },
    {
      "command": "bounded 3-size same-input source-context filtering observation (1000/2000/4000 quoted contexts, 6000/12000/24000 bytes; pinned public mapper; stop on mapping failure or a case > 1.5 s) (umask 077, at the literal implementation head)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "0.229/0.403/0.808 s with map_ok and all exact outside grants correct (granted_count == N, no leak). Not a timing SLO. Earlier epochs preserved: quadratic 0.370/0.961/3.117 s (the D0 attack surface), indexed-filter 0.210/0.391/0.818 s, R3 epoch 0.246/0.429/0.811 s."
    },
    {
      "command": "R2/R7 fail-open reproduction at the pre-fix source ef450574 (32 x U+0344 + an unclosed double-quote marker; 32 x U+0344 + an unclosed inline-HTML opening tag, each over the planted sentence; actual pinned map/compose/Engine, real owned SQLite, scripted batch reviewer outside the boundary, zero live target calls)",
      "result": "FAILED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "reproduced at the pre-correction source and fixed by the e401852 correction: before the fix the unproved context opener was placed from NFC-normalized columns into a past-line/past-EOF offset, the degenerate extent was dropped, the protected body was granted and one review call changed the output (protected [41,52] / [44,55] accepted). After the fix both inputs are byte-exact original with zero candidates and zero review calls. Preserved as the failure evidence that motivated the correction."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider research/tests/test_research_state_consistency.py::ResearchStateConsistencyTest::test_registry_and_report_counts -q (umask 077, pre-report stage)",
      "result": "FAILED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "the designed expected pre-report mismatch: AssertionError 91 != 90 (machine block oap_reports_reviewed 91 anticipates this report; 90 .md files at the implementation head count after the 007-o exclusion); preserved as FAILED - not repaired, rolled back or waived; the report-only commit reconciles it (91 counted, block 91) and the actual post-publication reconciliation is recorded only in the private receipt."
    },
    {
      "command": "private owner-key count-only scans (value never printed): the five changed non-report blobs at e401852; all three branch commit messages (6ae0e78, c21c784, e401852); the private 033-a report draft (this round) (umask 077)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "all scans count 0 (no owner key in any changed blob, commit message, or the draft); the report-commit blob and message scan is executed after creation and before push and recorded only in the private receipt."
    },
    {
      "command": "env OAP_ROLE=coding qualified python -B oap/bin/oap_cli.py preflight-report --repo-root . --id 033-a --source PRIVATE_FINAL_DRAFT (private scratch root, logical name retained privately) --expected-head e401852dc561900dd8d671f44660a92473ccf3ea (umask 077, canonical 033-a report ABSENT)",
      "result": "PASSED",
      "sha": "e401852dc561900dd8d671f44660a92473ccf3ea",
      "publication_head_claim": false,
      "details": "actual unpublished preflight executed on the exact final draft while the canonical 033-a report was absent: valid unpublished report draft, expected-head match against the literal implementation head, all check SHAs verified as real ancestor commits; private record retained under the scratch root; the draft is copied to the canonical path only after this pass."
    }
  ]
}
````

This report is the pre-publication evidence record for round 033-a
(protected original quote and HTML source contexts in the concept-
verification Pandoc mapper; round result COMPLETE). Three forward
non-report commits were made on PR 35 (NEW_PR, base main at
ad513664): the implementation, the Root regression-review corrections
(R3 low/high single, R4/R9/A1 replay, R10 non-canonical no-edit
envelope), and the R2/R7 NFC-unstable-line unproved-context fail-open
correction; the literal implementation head
e401852dc561900dd8d671f44660a92473ccf3ea is pinned before report
composition. The exact final draft was validated by the real
unpublished preflight (private source, canonical 033-a report absent);
this report is the sole-path SELF commit with sole literal parent
e401852dc561900dd8d671f44660a92473ccf3ea; the actual report-commit
scan, forward push, normal REMOTE verification, ONE exact OK response
and quiescence follow, recorded privately where post-publication. The
prior 87/434/static/slow/failure evidence is preserved as older epochs;
this round establishes no functional-MVP readiness, quality, milestone
or deployment acceptance, and no native or model serving success. No
future push or CI success is claimed inside this pre-push report
(publication_verified false); the four required final-head CI checks on
the published head and Strategy's independent semantic review remain
the development-merge gate.

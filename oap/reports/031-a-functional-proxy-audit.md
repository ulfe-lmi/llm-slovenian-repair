# Work report 031-a — fresh source-first functional proxy audit (audit-only)

Audit-only D0 round on accepted main `3bd6ffdd96bda95bd4c6de447b56cce76fe5a058`.
**Round result: PARTIAL** - the required shared whitespace checks fail at every
implementation head (Root-owned immutable-order formatting error; bounded forward
correction after publication; no CI bypass); the audit evidence and classification
remain final; no milestone acceptance. No product edits, no target-model calls
under this order (R6, 0 calls), no merge, no milestone or deployment acceptance.
The ICA matrix (59 rows: 48 IMPLEMENTED / 8 PARTIAL / 3 ABSENT after Root's
consolidated + evidence-fidelity corrections) and the concrete findings are in
`oap/audit/results/031-functional-proxy-audit.md`; non-raw probe/check evidence is
in `oap/audit/results/031-functional-proxy-audit-evidence.json`; the immutable
requirements-first derivation is in
`oap/audit/results/031-functional-proxy-requirements-first.json` (SHA-256
`fbcda5cf77d65914f87892e2de797589c549383b71bb3c1e0db6eb8afea9322d`, saved
2026-11-10T15:13:42Z before any claims/code inspection).

Headline results: the runnable proxy's core behavior is verified at the
evaluated SHA by focused probes and focused test reruns (byte-identical
unchanged envelope with 0 replacements; strict independent acceptance with both
accept and reject probed; fresh isolated review request; startup Pandoc gate
before bind; bounded phases; B-runner owned cleanup - explicit harness cleanup,
distinct from real-main shutdown). One confirmed concrete functional finding:
the actual runnable `main()` lacks owner cleanup around
`proxy.serve_forever()` (Root's closed experiment, private receipt, NOT rerun;
native SIGINT left the real process alive 2.0084 s with the two non-daemon
admission threads; exact-PID reap -9; the counterfactual server_close-in-finally
case is proof-of-shape only, not an implemented fix) - mapped to A-FAIL-01
(PARTIAL), with the smallest bounded follow-up named for a LATER order (real
main / native SIGINT / normal and failing cleanup paths, preserving first
caller-control semantics); B-v3 does NOT prove `main()` shutdown. Honest PARTIAL
bounds kept (corpus qualification bounded; mode matrix not proxy-runtime-
verified; live-Qwen layer UNPROVEN with 0 calls; morphology bounded; evidence
layers; reporting mechanism assessed normally with quality content owner-
excluded). Owner-excluded rows (M01/M04/M07, A-EVAL-01, MVP-8 quality content)
and later-service rows (S01-S05) are kept distinct and non-blocking. Root's
consolidated review correction and final evidence-fidelity correction (six
concrete evidence/negative-path fixes) are recorded in the audit supplement;
Root's 2 post-epoch native diagnostics (actual 15 s deadline FAILED; 45 s
diagnostic: valid local proposal in 22.453 s) are outside this audit's
execution scope (private receipts); a separate 031-b operator-setting decision
is in preparation and is not implemented here.

```oap-report
{
  "id": "031-a",
  "result": "PARTIAL",
  "order_path": "oap/orders/031-a-functional-proxy-audit.md",
  "order_sha256": "b4e4a2a485304893d228eb35d59e91cc229ddcea95a8160e536262e759004d10",
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
  "implementation_head": "380c5331f423547088dbee5cac80efcd6a9c1a37",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 33,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/33",
  "pr_state": "open",
  "branch": "oap/031-functional-proxy-audit",
  "base_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
  "starting_remote_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-10T18:09:27+00:00",
  "report_written_at": "2026-11-10T18:35:33+00:00",
  "implementation": "Audit-only; zero product/source/helper/registry mutation. Four non-report commits on oap/031-functional-proxy-audit from accepted main 3bd6ffd (heads da6892e, 16354d6, 2a9f6da, 380c533 = final implementation head); six distinct non-report paths in union (exact order, oap/active, three oap/audit/results files, research/RESEARCH-STATE.md one-line counter 85->86 only). Commit 1: source-first audit artifacts (immutable requirements-first JSON fbcda5cf... saved before claims/code inspection; ICA 59-row matrix; evidence JSON). Commit 2: whitespace fixed-contract conflict documentation. Commit 3: consolidated Root review correction (source-semantics/owner-scope reclassifications to 48/8/3; confirmed real-main SIGINT owner-cleanup finding mapped to A-FAIL-01; whitespace Root ownership + bounded forward correction after publication; public hygiene). Commit 4: Root final evidence-fidelity correction (six concrete evidence/negative-path fixes; post-epoch native diagnostics note - outside this audit's execution scope). Actual evidence: A probes (Pandoc startup gate before bind; exact reason labels; exit codes), C engine probes (zero-call path; strict abstention on the truncated real index; independent-evidence accept; keep/wider unchanged; C5 = direct parse_batch_envelope boundary rejecting the unknown id, no engine/HTTP, no original delivered), the corrected B-v3 full loopback HTTP e2e (OS-assigned port 0 from owned children; sanitized child environment; bounded IO; byte-identical raw envelope with 0 replacements; fresh strict review shape; content-free usage separation; explicit B-runner harness cleanup - distinct from real-main shutdown), focused D1/D2 reruns at 3bd6ffd, and the Root closed main()-SIGINT experiment (private receipt; not rerun). The RC124 B epoch is recorded as a failed harness epoch (fixed ports, inherited environment, unbounded live-pipe read), not a product failure; its children's origin is unprovable (PIDs never recorded) and was not touched; no residual probe children or old fixed-port listeners were observable.",
  "documentation": "No product docs, README or STATUS readiness claims (order: none in this audit). research/RESEARCH-STATE.md machine block advances oap_reports_reviewed 85 -> 86 in the first non-report commit only (030-a pattern: the report-only commit stages only the report path); at the implementation head the machine block (86) vs 85 published reports is the designed expected pre-publication mismatch that reconciles at the report-only publication commit - recorded as the actual precise state, not a failed check and not a future PASS; no further counter bump for the same-round corrections. registry_entries 42 and frozen_report_history_incidents 2 unchanged; oap/GENERATED-FILES.json and all 173 manifest keys/identities unchanged; frozen registry, ICA protocol/templates and all prior orders/reports unchanged.",
  "criteria": "A1: actual fresh-context source-first sequence on the same adopted foreground process (/new conversation, current worktree, no new agent/provider/model): owner scope then full PLAN/ARCH read at the pinned product, immutable requirements-first artifact saved and hashed (fbcda5cf..., 53339 B, 2026-11-10T15:13:42Z) BEFORE any strategic-claims or code inspection; the normative pre-artifact registry inspection (after the independent derivation) was ID reconciliation (schema/coverage reference against the frozen 59-row MVP registry), not claims inspection; declared independence corroborated by the observed workflow, not statistical. A2: all 59 frozen registry rows assessed with actual paths/evidence/negative cases/tested provenance plus the 13 full-source extras separately; after Root's consolidated + fidelity corrections the matrix is 48 IMPLEMENTED / 8 PARTIAL / 3 ABSENT; the confirmed concrete functional finding (real main() lacks owner cleanup around serve_forever; Root closed experiment, private receipt, not rerun) is mapped to A-FAIL-01 with a smallest bounded follow-up named for a LATER order (real main / native SIGINT / normal and failing cleanup paths, preserving first caller-control semantics); honest PARTIAL bounds kept (corpus qualification, mode matrix, live-Qwen UNPROVEN with 0 calls, morphology, evidence layers, reporting content owner-excluded); owner-excluded dataset/research/package conditions kept non-blocking and never revived as functional gates. A3: check_ica schema valid at 3bd6ffd (RC 0; 11 non-IMPLEMENTED gaps as designed); governance accepted-runtime, transcript and report-history require-manifest at the final implementation head 380c533 all PASSED (173 manifest identities; report_count 86; frozen paths unchanged); both accepted whitespace bases FAILED at every implementation head with the single documented Root-owned root cause (immutable order trailing blank line; Git blob 154087c5...; sole added diagnostic order:161) - failed evidence retained, no manufactured PASS, the forward correction after publication belongs to Root, no CI bypass; product/source/registry/helpers byte-unchanged (no product path in any commit; tracked state = scoped protocol/artifact dirty state only). A4: one actual PR 33 (OPEN, non-draft, head oap/031-functional-proxy-audit at 380c533) created and read back (2026-11-10T18:09:27Z) BEFORE this report; this is the chronological private unpublished preflight; the canonical sole-report SELF commit (sole parent 380c533), forward push, remote verification and ONE response happen only after Root exact-byte review; no coding merge/automerge/MVP/deployment acceptance.",
  "negative_paths": "Proved at 3bd6ffd: wrong-path POST rejected 404 with zero outbound; no Authorization on any outbound request (sanitized child environment by construction); X-Probe-Marker not forwarded to upstream; review request fresh with no linkage keys (empty set probed) and store:false/stream:false/max_output_tokens 1536; unknown proposal ID rejected whole-batch at the direct parse_batch_envelope boundary (REVIEW_UNKNOWN_ID; no RepairEngine/HTTP run for that case, no original delivered in the C5 boundary test - the crashed fakeReviewer returning an invalid BatchResult was a harness artifact, not an original-fallback test); strict abstention on the truncated real index (missing data never zero); keep/wider-edit proposals leave the target unchanged; optional-review failure never damages the completed answer (the engine only ever sees protocol-valid BatchResults; the completed-original fallback on optional-review failure while the caller can receive it per source + qualified named tests, not C5); disconnected client -> quiet abort with owned upstream/review canceled and NO original/second response (030 semantics; proxy.py _deliver: no second response/status/fallback on a disconnected socket); owned B-v3 children SIGTERM-terminated, reaped and pipe-drained on every path (proxy exit 0 CLEAN_SHUTDOWN through the owning admission close; upstream exit -15), no forced kill, parent 1 thread / 4 open FDs - this is the B-runner explicit harness cleanup, NOT real-main shutdown (real-main SIGINT behavior is the confirmed A-FAIL-01 finding: Root closed experiment, private receipt, not rerun). The RC124 epoch's unbounded live-pipe read is recorded as the harness failure the corrected B-v3 design eliminates (select-bounded READY reads; EOF-drain only after terminate+reap).",
  "boundary_fidelity": "Evaluated product bytes are exactly accepted main 3bd6ffd: none of the four non-report commits touches any product, test, helper, registry, governance or manifest path (six distinct non-report paths in union: order, active, three audit-result files, RESEARCH-STATE one-line counter). The audit's probes bind OS-assigned loopback port 0 and drive the actual ConceptProxy constructor (same class main() instantiates; real _Handler/RepairEngine/ResponsesReviewer/check_pandoc) because main() hardcodes 127.0.0.1:18024 - constructor-driven entry point stated honestly, with the CLI/main() startup proofs kept in the distinct A epoch; only external upstream/review endpoints are synthetic. The frozen registry stayed byte-identical at 3bd6ffd (check_ica ICA_MATRIX_SOURCE_DRIFT gate). The prior 931-pass full suite at the M30-era tree (NOT newly executed at M30; App successful logs do NOT print a total of 931) and the four-check CI / 13 development-baseline driver commands at PR32 reviewed head 8fc14c3 are cited strictly as a claims index with the order's verified merged-tree-equals-reviewed-head equivalence (re-verified in this epoch: git diff 8fc14c3..3bd6ffd is empty), never relabeled as executions at 3bd6ffd.",
  "setup": "Same adopted foreground pane (fresh /new conversation, same process, current worktree, cwd, profile, home and auth); qualified Python 3.12.15 (project venv) with -B and private TMPDIR/PYTHONPYCACHEPREFIX; qualified Pandoc 3.7.0.2 (SHA 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229) by explicit path, no discovery; authorized read-only private corpus index (truncated release). Every helper: explicit OAP_ROLE=coding, shell umask 077, private 0700 dirs / 0600 files; probe children ran under a minimal sanitized environment (no QWEN_API_KEY/CONCEPT_REVIEWER_PROFILE/provider credentials; parent CODEX_HOME/profile/auth unchanged and never read). The owner-supplied throwaway native key file (repo root, mode 0600, untracked, locally excluded) was not read, staged, copied or logged by coding. No new agent, CLI, model, provider, pane or restart; no live target call under this order (R6; 0 calls); Root's 2 post-epoch native reviewer diagnostics (actual 15 s exchange deadline: FAILED by deadline; 45 s diagnostic bound: valid local proposal in 22.453 s) are later Root diagnostics outside this audit's execution scope with private source-bound receipts - not executions by this auditor; the remaining 2 authorized calls are not used under 031-a and the separate 031-b operator-setting decision is not implemented here. Actual resource paths supplied privately in the phase-1 handoff, not searched historically.",
  "privacy": "No customer text, raw model prompts/responses, targets/replacements, credentials or private service configuration in any public artifact; probe literals are tiny owned synthetic strings; raw probe logs and stderr remain private 0600 under the private test-scratch root and are preserved without being echoed (failed RC124 epoch, v2 harness-crash epoch, v3 canonical epoch and the Root closed SIGINT experiment all retained). Content-free channels are the stderr usage observer and public evidence; the explicitly opt-in 0600 trace files carry original/candidates/decisions/repaired data when enabled (private, off by default; B-v3 enabled them only for owned synthetics) - an evidence/diagnostic-surface distinction, not a privacy defect, and no production text-logging authorization is claimed. Public prose uses logical roots (STRATEGIC_HOME-relative scratch, logical artifact names) instead of physical machine paths.",
  "limits": "Audit-only: no product change, no broad-suite rerun (R5), no live-Qwen qualification (R6; 0 target calls under this order; the live row is NOT RUN, not passed), no human dataset (excluded, not deferred), no merge. Round result PARTIAL because the required shared whitespace checks fail (Root-owned immutable-order formatting error; bounded forward correction after publication; no CI bypass). Focused probe budget: five A startup cases, six C engine cases, one corrected B-v3 e2e run (~1.6 s wall, ports 45627/45777) plus its one minimal wrong-path negative control; two focused module reruns (67+3 subtests; 19). The Root closed main()-SIGINT experiment is cited from its private receipt and NOT rerun. The native-Qwen compatibility and linguistic-quality layers remain UNPROVEN/unmeasured bounded facts of this offline audit (Root's 2 post-epoch diagnostics are outside this audit's execution scope).",
  "human_gates": "Decision NONE under D0; no separate human evaluation dataset (excluded, not deferred); no additional human approval step. Root is the strategic agent: its exact-byte review of this private unpublished preflight (round result PARTIAL) precedes the canonical sole-report SELF commit (sole parent 380c533), forward push, remote verification and ONE response. The human retains final milestone labeling and release/deployment authority; none is claimed. Root's later development-merge gate requires all four final-head CI checks - of which the two accepted-base whitespace steps fail at the final implementation head, root-caused exclusively to the immutable 031-a order's trailing blank line (fifth whitespace diagnostic; fixed contract closed at four by order 027-b; Root owns the formatting error; not remediable by coding per R2/R9; Root will issue an explicit bounded forward correction after truthful 031-a publication; no CI bypass; no milestone acceptance).",
  "scope": "Six distinct non-report paths in union across the four non-report commits (oap/orders/031-a-functional-proxy-audit.md, oap/active, oap/audit/results/031-functional-proxy-requirements-first.json, oap/audit/results/031-functional-proxy-audit.md, oap/audit/results/031-functional-proxy-audit-evidence.json, research/RESEARCH-STATE.md one-line counter 85->86 only) plus this sole report; one new PR (33). No other path mutation; the three unrelated untracked roots, the owner-supplied key file (untouched), retained branches, archives/index/private artifacts, role homes/auth and PR13 are preserved.",
  "checks": [
    {
      "command": "python3 oap/bin/oap_cli.py ica --repo-root . --source oap/audit/results/031-functional-proxy-audit.md --current-main 3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "schema valid, RC 0, 11 non-IMPLEMENTED gaps (8 PARTIAL + 3 ABSENT) as designed after the consolidated + fidelity corrections; registry byte-identical at 3bd6ffd (ICA_MATRIX_SOURCE_DRIFT gate); re-verified at each correction head, final re-run at 380c533."
    },
    {
      "command": "python3 oap/bin/oap_cli.py governance --repo-root . --mode accepted-runtime --accepted-ref 3549de2a436f485a693730d0ee7d5f8c00aec0c0",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "structure valid, RC 0, at the evaluated main."
    },
    {
      "command": "python3 oap/bin/oap_cli.py state --repo-root . --strategic-home STRATEGIC_HOME --repository ulfe-lmi/llm-slovenian-repair",
      "result": "PENDING",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "observed RECOVERY_REQUIRED for 031-a with branch oap/031-functional-proxy-audit and pr null, pre- and post-branch/PR (the helper's pr field reflects the immutable order's pr:null metadata snapshot); the expected in-progress state of a round whose sole report is not yet published; reconciled by the report-only commit + remote verification, not by any state mutation."
    },
    {
      "command": "python3 oap/bin/oap_cli.py transcript --repo-root . --revision 380c5331f423547088dbee5cac80efcd6a9c1a37",
      "result": "PASSED",
      "sha": "380c5331f423547088dbee5cac80efcd6a9c1a37",
      "publication_head_claim": false,
      "details": "RC 0 (result valid; active=latest=031-a; report_count 86; frozen mutation paths unchanged) at the final implementation head; the pre-commit HEAD 3bd6ffd run showed ACTIVE_INDEX_MISMATCH by design (worktree active=031-a vs committed 030-a before the non-report commits) and is recorded as such."
    },
    {
      "command": "python3 oap/bin/oap_cli.py report-history --repo-root . --revision 380c5331f423547088dbee5cac80efcd6a9c1a37 --require-manifest",
      "result": "PASSED",
      "sha": "380c5331f423547088dbee5cac80efcd6a9c1a37",
      "publication_head_claim": false,
      "details": "RC 0; report_count 86; all 173 manifest identities; frozen mutation paths (006-a, 006-c) unchanged; also PASSED at HEAD 3bd6ffd in the earlier epoch."
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --repo-root . --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da (CI: OAP bootstrap acceptance)",
      "result": "FAILED",
      "sha": "380c5331f423547088dbee5cac80efcd6a9c1a37",
      "publication_head_claim": false,
      "details": "DIAGNOSTIC_SET_MISMATCH, RC 1 at 380c533 (also at da6892e/16354d6/2a9f6da; Root independently reproduced at 16354d6). Diagnostic set = the four pinned historical incidents + the sole new diagnostic oap/orders/031-a-functional-proxy-audit.md:161 (new blank line at EOF); committed order blob 154087c510433f229c39cee4bafded877b40b671 (18351 B, immutable) verified at the head; diagnostic introduced in da6892e. Root owns this formatting error; no order/history rewrite and no helper repair within 031-a; Root will issue an explicit bounded forward correction AFTER truthful 031-a publication; no CI bypass. All OTHER round-added audit/bookkeeping artifacts whitespace-clean. Round result: PARTIAL."
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --repo-root . --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a (CI: Application baseline)",
      "result": "FAILED",
      "sha": "380c5331f423547088dbee5cac80efcd6a9c1a37",
      "publication_head_claim": false,
      "details": "DIAGNOSTIC_SET_MISMATCH, RC 1 at 380c533; identical diagnostic set and single root cause as the 2832fa1e base (verified identical at the final head)."
    },
    {
      "command": "pytest concept-verification/tests/test_pandoc_protection.py -q (D1, focused)",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "67 passed + 3 subtests in 7.47 s, rc 0; prior epoch of this order at literal 3bd6ffd with scoped protocol/artifact dirty state (M oap/active; untracked 031-a order), product bytes unchanged at 3bd6ffd; qualified python -B, private caches."
    },
    {
      "command": "pytest concept-verification/tests/test_concept.py -q (D2, focused, CONCEPT_PANDOC=qualified)",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "19 passed in 5.07 s, rc 0; same epoch/dirty-state provenance as D1; qualified python -B, private caches, explicit CONCEPT_PANDOC."
    },
    {
      "command": "A probes: Pandoc startup gate (qualified 3.7.0.2 pass; missing path PANDOC_NOT_EXECUTABLE; fake 3.6.0 PANDOC_WRONG_VERSION; full main() with bad pandoc exit 1 before bind; empty PATH PANDOC_NOT_FOUND)",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "five bounded startup cases at 3bd6ffd (this order's epoch); gate verified before any bind allocation (fixed port 18024 never bound in the failure cases); private 0600 logs retained."
    },
    {
      "command": "C probes: engine-level strict acceptance (clean zero-call; truncated-index abstention; independent-evidence accept; keep/wider unchanged; C5 unknown-id boundary)",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "six bounded engine cases at 3bd6ffd with the injected fake reviewer and the real/fixture indexes. C5 is ONLY the direct parse_batch_envelope(envelope, {t0}) call rejecting the unknown t9 payload as BatchError(REVIEW_UNKNOWN_ID) before any BatchResult exists - no RepairEngine/HTTP run for that case and no original delivered; the earlier fakeReviewer that returned an invalid BatchResult crashed the harness (harness artifact, not a passed original-fallback test); the engine only ever sees protocol-valid BatchResults."
    },
    {
      "command": "B probe, initial harness epoch (fixed 127.0.0.1:18091/18024, inherited environment, unbounded live-pipe read)",
      "result": "FAILED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "RC124 external timeout - recorded as a FAILED HARNESS epoch, not a product failure (harness SHA 4ab8700f... preserved verbatim by Root under observed-probes/); child PIDs were never recorded so the timed-out children's origin is unprovable and were not touched; no residual probe children or old fixed-port listeners were observable at the corrected run."
    },
    {
      "command": "B-v3 corrected probe: full loopback HTTP e2e (OS-assigned port 0 from owned children; real ConceptProxy constructor; sanitized child env; bounded IO; terminate-then-drain harness cleanup) plus one minimal wrong-path negative control",
      "result": "PASSED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "rc 0, ~1.6 s wall (ports 45627/45777): 404 wrong-path with zero outbound; 200 completed in 0.162 s; 0 replacements - raw envelope byte-identical to the synthetic original (sha256 bb8aad1b...; the unchanged-path proof, including protected content); output text equals original (sha256 2fa48227..., 78 codepoints, URL + inline code intact); the positive changed-span proof is the C2 fixture-accept case plus the qualified existing patch tests (D1/D2), not B-v3; 1 main + 1 review outbound, no Authorization, X-Probe-Marker not forwarded, review fresh/strict (store:false, stream:false, max_output_tokens 1536, no linkage); usage observer one content-free line (calls=1, 10/20/30) separate from main usage (7/25/32) - content-free channels are the stderr observer/public evidence, while the opt-in 0600 trace (acceptance, 1 candidate, 0 replacements; review_batch call/usage omitted - minor finding) carries data when enabled, off by default, enabled here only for owned synthetics; both children SIGTERM-terminated/reaped/pipe-drained (proxy exit 0 CLEAN_SHUTDOWN; upstream exit -15), no forced kill, parent 1 thread / 4 open FDs - the B-runner's explicit harness cleanup, NOT real-main shutdown; the v2 attempt crashed in its own report writer AFTER clean child reap (no orphans) and is retained as a harness-development epoch."
    },
    {
      "command": "Root closed experiment: actual main() native SIGINT, owned port 0, two cases (private receipt; NOT rerun in this audit)",
      "result": "FAILED",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "executed at implementation HEAD 16354d6 on product bytes equivalent to 3bd6ffd (this audit re-verified: git diff 8fc14c3..3bd6ffd empty); code mutations false; real proxy.main() (normal config/qualified Pandoc/real ConceptProxy-serve_forever-admission); fixture changed only the hardcoded bind address to an owned OS loopback port 0 (37021/36591); default 18024 never bound or probed; zero HTTP/model requests; sanitized child env. actual_main (DEFECT): PID 57747 alive 2.0084 s after native SIGINT with MainThread + two non-daemon admission threads; fixture killed only the exact owned child, reaped -9 (KeyboardInterrupt on stderr; 1054 B stderr/145 B stdout; total 2.6691 s). reference_finally (COUNTERFACTUAL, proof-of-shape only - NOT an implemented fix or production PASS): PID 57764 with the real server_close in a finally exited naturally -2 in 0.0318 s. All owned processes reaped. Mapped to A-FAIL-01 (PARTIAL); distinct from the B-v3 constructor runner."
    },
    {
      "command": "Full 19-suite regression at 3bd6ffd (broad suite)",
      "result": "NOT RUN",
      "sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
      "publication_head_claim": false,
      "details": "R5-bounded (no broad-suite repeat in this order). Claims index only: 931 passed at the M30-era tree - that 931 result was NOT newly executed at M30 and App successful logs do NOT print a total of 931; H30/actual-CI-checkout/M30 trees match; all 13 Application-baseline development-baseline driver commands and the four required final-head checks passed at the tree-equal PR32 reviewed head 8fc14c3258aa8712ecd53be81abe3e62c798d04b (CI observation at the reviewed head); git diff 8fc14c3..3bd6ffd is empty (re-verified in this audit). Never relabeled as a new execution at 3bd6ffd."
    }
  ]
}
```

This report is the PRIVATE unpublished preflight (round result PARTIAL - see
`human_gates` and the whitespace checks; the audit evidence and classification
remain final). After Root exact-byte review and approval ONLY: the report-only
commit (sole parent `380c5331f423547088dbee5cac80efcd6a9c1a37`, only this
report path), forward push, `verify-report --repository ulfe-lmi/llm-slovenian-
repair` remote verification, then ONE FIFO response and exit. No future push/CI
success is claimed inside this pre-push report (`publication_verified: false`);
the final-head four CI checks (two of which - the accepted-base whitespace
steps - fail at the final implementation head pending Root's bounded forward
correction of the immutable order's trailing blank line) remain Root's later
development-merge gate.

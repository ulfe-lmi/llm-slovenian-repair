# 034-a — Source-first functional proxy readiness audit (Independent Closure Audit)

Status: FINAL. Fresh audit of the accepted merged runnable proxy at the exact audited
accepted main `c36ed4f42534bc13df4dac2b418fb50262d47d06` (tree
`df075746203c1eb6d6e3a288f3e2d7eede2d92de`), D0, Decision NONE, source-first and
audit-only (zero live target requests, no product/dependency/test/workflow changes,
no implementation, no separate human evaluation dataset, no research restart).

## 1. Scope and objective

Owner scope (read first, verbatim in the requirements derivation): assess the runnable
Slovenian repair proxy and report when the **functional MVP** is ready; Pandoc is the
**mandatory structural parser**, explicitly installed and versioned with a startup check;
corrections operate **only on proved exact spans** of the original answer — never
regenerate by rendering the AST, no ambiguous substring recovery, unproved regions remain
unchanged, and a parse/mapping failure returns the safely completed original without
repair; preserve established code, equations, HTML, links, configuration, quoted and other
machine-sensitive content, Unicode and all unapproved slices. No separate human evaluation
dataset (excluded, not deferred; NOT a functional-readiness gate, no human-labeling
obligation); no research restart. The owner retains final milestone labeling and
deployment/exposure decisions.

The runnable proxy is the deliberately isolated standard-library spike under
`concept-verification/` (loopback `127.0.0.1:18024`; one active server request plus a
bounded queue, owned reviewer/upstream subprocess workers and monitors; bounded finite HTTP
calls; pinned Pandoc). It is explicitly "EXPERIMENTAL / CONCEPT VERIFICATION / NOT
PRODUCTION CODE". The `src/llm_slovenian_repair` package is a separate 5-module development
skeleton and is NOT the runnable proxy.

## 2. Method and source-first sequence

Input order: `human_scope -> full_architecture -> current_main -> strategic_claims`. The
checker validates the **declared** list/schema, not actual chronology or statistical
independence; the actual full-source-before-claims sequence is established by the Root
rollout observations (provenance in section 3 and the oap-ica `context_provenance`). Neutral
owner scope read first; then the COMPLETE canonical `PLAN.md` (sha256 d2aa1d98...) and
`ARCHITECTURE.md` (sha256 a16e0f87...) Git bytes at the exact audited main, verified
byte-exact; then the requirements-first derivation saved and hashed; only afterwards the
frozen registry (64 rows / 59 MVP), the deferred evidence index and the prior 032/033-a
claims, always as claims. The complete privacy-safe source derivation and the full-
architecture coverage facets are published in the evidence appendix (section 4b); the frozen
initial record is cited by identity only (section 5).

## 3. Fresh offline evidence (at audited main c36ed4f)

- **Full offline suite (final synchronous run)**: 965 tests, 584.337 s, **OK, exit 0**, with
  the pinned `CONCEPT_PANDOC`, qualified python -B, OAP_ROLE=coding, shell umask 0077
  (private run log SHA-256 `b0d53b2d...`; run began 09:35:44; SUITE_EXIT 0 observed
  09:46:53.975Z). Honest setup note: the **first run (09:28:24) DID use the qualified python
  -B** but lacked an explicit `CONCEPT_PANDOC` and selected the wrong parser binary, so it
  was NOT the exit proof (its log is retained, private); a second asynchronous wrapper epoch
  was not a complete exit proof; and that final run's initial environment had no
  TMPDIR/PYTHONPYCACHEPREFIX and owned temporary fixtures under /tmp appeared in its private
  output, so no supplied strategic TMP is claimed throughout (Root receipt
  `034a-root-direct-runtime-965-tests-real-exit-zero-review-20261111.json`). A separate run
  without `CONCEPT_PANDOC` selecting a different `pandoc` build failed the precise byte/slice
  boundary tests; with the pinned binary it passes. This is consistent with the mandatory
  pinned-parser design: `resolve_pandoc_spec` (pandoc_protection.py:241ff) selects the
  explicit configured binary OR `shutil.which('pandoc')`, then the startup check validates
  the exact `3.7.0.2` version + positioned-JSON capability before bind; the prohibition is a
  historical research executable-search / a silent weaker-regex fallback, NOT normal PATH
  discovery of the required installed version. The earlier unqualified-Pandoc run selecting a
  different build does NOT prove a production downgrade. The blanket "965 passed" is broad
  evidence; each named boundary is additionally cited to its real positive/negative tests and
  fake seams in the matrix and the coverage facets.
- **Direct pinned-Pandoc probe**: binary SHA-256 `02a59bd9...` matches the integrity pin,
  version exactly `3.7.0.2`, reader `commonmark_x+sourcepos-smart`; the positioned-JSON
  capability the startup check asserts is reproduced (wrapper `Div` `data-pos 1:1-2:1`; the
  positioned `Str` leaf's source position is carried on its positioned `Span` wrapper).
- **Mandatory startup check (real)**: `proxy.main()` runs `resolve_pandoc_spec()` +
  `check_pandoc(spec)` **before any HTTP bind** (executable presence, exact `--version`
  match, positioned-JSON capability probe) and raises `SystemExit` on any finite reason. The
  bind is loopback-only.
- **Independent probe of the 033-a changed protection consumer** (real
  `protect_with_pandoc`, pinned binary): a Slovenian low/high `„…"` quote's interior is
  denied while outside prose is granted; a raw inline HTML tag's interior is denied while
  surrounding prose is granted; fenced code is denied while surrounding prose is granted
  (deny-by-default, exact code-point grants, no AST rendering, no substring recovery). This
  is a **mapping-only three-case probe**: it does not by itself prove the real Engine / real
  HTTP / all 14 prior counterexamples — those are covered by the actual tests in the 965
  suite, and the verified 033 Root probes may be reused with stated source/dependency
  equality.

## 4. Findings

**Software / behavioral core — IMPLEMENTED with fresh offline evidence.** The audited main
implements, and the fresh suite + independent probes confirm: complete completion-gated
capture before review/delivery; CPU-gated zero-review on no suspicion; preassigned
word/short-phrase targets (deterministic, non-overlapping, cap 8); strict isolated
one-batch review (`ResponsesReviewer.review_batch` -> `batch_review.build_prompt` /
`build_request_body` + `review_transport.run_review_exchange`; fresh single-turn request, no
`previous_response_id`/session/tools, one monotonic deadline, no retry, strict per-id
schema); strict independent-evidence acceptance **as wired**
(`runtime_acceptance.accept`: the replacement side must be an EXACT positive row, the
original side matched by the anchored comparable EXACT factor-two margin on the SAME ngram
order, with the narrow one-codepoint R5 possible-typo route not subject to that floor;
EXACT(0) a known zero, never positive; CENSORED/UNAVAILABLE never zero; unknown-count
opposition; every replacement word EXACT) + `composed_validation.validate_composed/_revalidate`
group revalidation; exact original-slice patching (descending offsets, non-overlap,
protected-slice byte-identity assertion); composed conflict-group validation (arithmetic
rebasing, never substring search; an unprovable mapping makes the WHOLE pass abstain to the
completed original while a live recipient remains); mandatory pinned-Pandoc deny-by-default
protection (033-a quote/HTML/BlockQuote remediation in place and independently reproduced);
bounded limits and a failure contract that preserves the completed original; request-scoped
cancellation (a client disconnect is a quiet in-handler `RequestCancelled` abort, distinct
from optional-repair-failure original preservation) and owned entry-point close. This
reconciles the earlier 032 closure audit (which found LR-007/A-PROTECT-01/A-SPAN-01/
A-ACCEPT-02/MVP-5/D03 PARTIAL at a pre-remediation main): at the current audited main the
protection consumer is remediated, so those rows are now IMPLEMENTED, independently
confirmed by the positive + fail-closed probe above. The legacy `repair.accept` /
`_positive_local` and the single-target `qwen_client.prompt(frozen-v1)` review path are NOT
the wired runtime; only the shared `Acceptance` type/`apply_edits` patcher remain in the
runtime.

## 4b. Complete source-derived coverage and full-architecture facets (R3/R4)

Because the immutable initial record is private, its **privacy-safe normative subset is
published here** in the evidence appendix `source_derived_projection`: the owner-scope
derivation, the full source-derived requirements (LR-001..LR-014, all 8 PLAN-16 criteria,
and all D/M/S work blocks with applicability), the applicability model, and the owner-
excluded items — cited to the frozen private record by logical ID / byte count / hash /
length, with no native host paths and the private original unchanged. The evidence appendix
`full_architecture_coverage` adds the 12 full-architecture technical facets (A–L: capture/
MAIN_FINISHED; independent clocks; eligibility/admission/caps; Unicode source mapping;
physical contexts; read-only corpus; detector; isolated batch; strict lexical routes +
composed revalidation; JSON/SSE completion/terminal-copy; cancellation/owned shutdown;
content-free trace-OFF profile) each with its source clause, actual entry/function, actual
positive+negative tests/seams, class, applicability and limit. A 59-row schema pass or the
965 summary alone does not prove these clauses.

**Remaining gaps and separate evidence layers (not waived, not conflated).**
- *Native serving compatibility (live target Qwen)* — **UNPROVEN here (D05 PARTIAL).** This
  offline audit makes 0 authorized native calls. The real `ResponsesReviewer` HTTP client is
  proven only as SOFTWARE/TRANSPORT (real wire) against an owned in-process endpoint —
  `test_review_batch.py::TransportTests.test_single_request_exact_route_body_and_reordered_
  result` (real worker -> `HTTPServer 127.0.0.1:0`; negative `test_non_200_fails_whole_batch`),
  `CompositionChainTests`, `test_responses_contract.py::ContractHttpTests` and
  `test_review_transport.py::BatchExchangeTests`; the `WorkerSubprocessTests` fake-worker
  subset (via `_REVIEW_WORKER_PATH`) is IPC framing only, NOT wire. The real-Qwen condition
  is unproven: the prior 031-b native RTX MAIN (HTTP 200 / 2105 B / 4.721 s) failed the
  actual completion-envelope validator (the exact rejected clause is not retained here) and
  the four allocated slots are TARGET POST slots counting MAIN and REVIEW separately
  (exhausted). Historical A100 isolated-review success is a different model/quantization/
  evidence layer. LR-014 / A-API-01 / A-TEST-01-live require separate live evidence. The
  smallest sufficient next step (no live call in 034) is ONE authorized MAIN-path
  reproduction with a minimal content-free observer of the ACTUAL failed completion-envelope
  predicate, stopping at the first unresolved boundary (reserve one main plus a possible
  review under new owner allowance); a subsequent actual-Qwen isolated batch can then
  qualify the reviewer condition — an owned fake-worker endpoint can never satisfy the
  native retest. The extra 12-slot allowance is unanswered.
- *Linguistic quality / benefit* — **EXCLUDED by the owner (not deferred).** No separate
  human evaluation dataset and no current or future human-labeling obligation; quality is
  unmeasured by this audit and no separate dataset gate applies (historical source labels,
  where present, are historical only). This is NOT a functional-readiness gate in the owner's
  selected scope. The deterministic held-out framework (dev 16 / held-out 32, frozen split,
  ablations with denominators) exists, but measured benefit/harm is not produced. The
  approximate 99% precision and 1 harm/10k remain unmeasured goals, not results or release
  authority. (A-EVAL-01 unproven; M01, M07 unproven/absent; M04 and MVP-8 partial.)
- *Production stack / library* — the runnable proxy is a stdlib concept spike, not the
  A-STACK-01 production library; `src/` is a 5-module skeleton (PARTIAL).
- *Selectable acceptance modes* — the spike is a single conservative (strict-like) repairer;
  the detect_only/shadow/experimental modes are not selectable in the spike (A-ACCEPT-01
  PARTIAL) — not a new functional gate.
- *Corpus manifest completeness* — the index provenance records source identity/checksums,
  cutoff and "denominator unknown", and absence semantics, but not explicit rights/license,
  normalization/tagging, importer-version or deterministic-build-parameter fields
  (A-CORPUS-02 PARTIAL). Non-redistribution of the private local archives/index is a handling
  practice, NOT rights/license authorization; the existing authority is bounded read-only,
  with no acquisition / public redistribution / full-corpus gate in this audit.
- *History edge* — final-answer delivery, review-JSON exclusion, main/review usage
  separation and no-history-mutation are implemented; logprobs/annotations invalidation on
  changed text and server-managed history chaining are not exercised in the loopback concept
  (later integration).

## 5. Provenance and the private initial record

The complete initial requirements-first record is **private and unpublished**: logical ID
`PRIVATE_INITIAL_034`, 24661 bytes, SHA-256 `bb29467e...`, preserved by Root (byte/inode
unchanged; the formerly untracked public candidate was moved to the private record before
any commit/push, and was never staged/committed/pushed). It is **not** a tracked public file
and its bytes were **not** rewritten. It is cited here by logical ID, byte count, hash and
provenance only — never by a native host path. Its privacy-safe normative subset (owner
scope, full source requirements, applicability model, owner-excluded items) is published in
the evidence appendix `source_derived_projection`; the complete coverage and the full-
architecture facets are in `full_architecture_coverage`. The 09:05:59 figure is a pre-
generation source observation, not the write time; the actual initial exec/save/hash was
09:08:52, before the first deferred-content read at 09:09:27. Early/private builder setup
had honest omissions (first run 09:28:24 used qualified python -B but no explicit
CONCEPT_PANDOC and the wrong parser; a second async wrapper epoch not a complete exit proof;
some early cat/heredoc writers not initially role/umask-qualified) with Root repair (builder
modes 0664->0600, bytes/inode preserved); no perfect whole-order setup is claimed.

## 6. Readiness conclusion (not predetermined; D0)

The owner's selected functional scope is the runnable proxy's functional readiness, with no
separate human evaluation dataset (excluded, not deferred; NOT a functional-readiness gate,
no human-labeling obligation, and no new functional gates invented). Against that scope:

(a) **Owner-selected runnable functional assessment** — the offline functional-MVP software
core (mandatory pinned Pandoc, exact-span deny-by-default protection, isolated one-batch
review, strict independent acceptance as wired via `runtime_acceptance.accept` + composed
revalidation, exact-slice patching, bounded limits, cancellation, owned lifecycle,
failure->original) is substantially IMPLEMENTED and well-tested at the audited main. The
remaining **actual applicable functional gap** is native serving compatibility on the actual
target Qwen: UNPROVEN here (0 authorized native calls; the earlier 031-b native RTX MAIN
aggregate failed the completion-envelope validator; the four allocated target-POST slots are
exhausted). It is reported concretely, not suppressed, and not redefined around the tests.

(b) **Historical experimental / quality criteria** — the deterministic held-out framework and
the ~99%-precision / 1-harm-per-10k goals are unmeasured and owner-EXCLUDED (not deferred);
they are not a functional-readiness gate in this scope.

(c) **Milestone / deployment authority** — separate and owner-retained. This audit does not
self-certify a functional milestone or deployment: `deployment_authorized=false` and
`human_milestone_accepted=false`. Strategy independently reviews and gates any development
merge on the actual final-head checks; the owner retains the final milestone label and
deployment/exposure decisions.

No optional morphology, full-corpus acquisition, selectable library-mode matrix, packaged
stack or quality programme is promoted into a new functional gate; source classes may remain
PARTIAL/ABSENT with honest applicability.

## 7. Authority

Audit-only. No merge, no auto-merge, no product edits, no deployment, no human acceptance,
no live target requests. Sole report: `oap/reports/034-a-functional-proxy-readiness-audit.md`
(SELF publication). This audit is independent architecture-to-main evidence, not execution
self-approval.

```oap-ica
{
 "status": "FINAL",
 "milestone": "MVP",
 "main_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
 "architecture_sha256": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
 "plan_sha256": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
 "auditor": "fresh-context coding pane (OAP_ROLE=coding), the same adopted owner-launched sole foreground CLI (codex --yolo --profile early-beta, pane pid 3341327), a new conversation at the quiescent pane, current worktree, low-effort; declared independence from the source-first workflow and the Root preservation/sequence receipts, not statistical independence. No new CLI/agent/provider/model/service/network; zero live target requests.",
 "context_provenance": "Source-first per order R1/R2: (1) neutral owner scope (034a-neutral-source-first-audit-inputs, logical reference, not a native path) read FIRST; (2) COMPLETE canonical PLAN.md (sha256 d2aa1d98..., 757 lines, git show at c36ed4f, reads ~09:02:08 and the missing-middle re-read ~09:02:21) and COMPLETE ARCHITECTURE.md (sha256 a16e0f87..., 516 lines, git show at c36ed4f, reads ~09:04:40 head-400 and ~09:05:03 lines 400-600) at the exact audited accepted main c36ed4f, BEFORE any implementation/registry/closure/deferred-index inspection. (3) The immutable requirements-first derivation was then saved and hashed: the exact initial record PRIVATE_INITIAL_034 (24661 bytes, SHA-256 bb29467e687ad8d75810d8c6290225e5818b3a61b8e6e5acccb38e54bd3ade21) was preserved privately by Root and is NOT a tracked public file and its bytes were NOT rewritten (the 09:05:59 source-observation time is pre-generation, NOT the write time; actual initial exec/save/hash 09:08:52, before the first deferred-content read 09:09:27; a transient privacy stop at 09:11:06Z before any commit/push moved the untracked public candidate to the private record - see the private preservation receipt). It is cited here only by logical ID, byte count, hash and provenance, never by a native host path. (4) Only AFTER the derivation were the frozen registry (oap/audit/requirements.json, 64 rows / 59 MVP), the deferred evidence index, and the prior 032 closure-audit / 033-a report claims inspected, and always as claims. (5) Setup honesty: early/private builders had omissions and NO perfect whole-order setup is claimed - the first runtime-suite run (09:28:24) DID use the qualified python -B but lacked an explicit CONCEPT_PANDOC and selected the wrong parser binary, so it was not the exit proof (its log is retained, private); a second asynchronous wrapper epoch was not a complete exit proof; and several early cat/heredoc writers did not begin with explicit OAP_ROLE=coding / umask 077, which Root later repaired (builder file modes 0664->0600, bytes/inode preserved; this writer was likewise repaired; see Root receipt 034a-root-direct-runtime-965-tests-real-exit-zero-review-20261111.json). (6) The FINAL synchronous full suite DID use qualified python -B, the pinned Pandoc 3.7.0.2 (CONCEPT_PANDOC), OAP_ROLE=coding and shell umask 0077 with actual SUITE_EXIT 0 observed at 09:46:53.975Z for the 09:35:44 run (965 tests, 584.337 s; private log SHA-256 b0d53b2d...); that run's initial environment had no TMPDIR/PYTHONPYCACHEPREFIX and owned temporary fixtures under /tmp appeared in its private output, so no supplied strategic TMP is claimed throughout. The checker validates the DECLARED input-order list/schema, not actual chronology/independence; the actual full-source-before-claims sequence is established by these Root rollout observations. EVERY subsequent helper/writer this round began with actual umask 077 + explicit OAP_ROLE=coding, qualified python -B and private TMP/cache. No strategic closure claim was used as a premise.",
 "input_order": [
  "human_scope",
  "full_architecture",
  "current_main",
  "strategic_claims"
 ],
 "matrix": [
  {
   "id": "LR-001",
   "class": "IMPLEMENTED",
   "runtime_path": "capture_transport.py read_bounded_body/scan_complete_prefix/require_complete -> proxy._Handler.do_POST -> forward() -> RepairEngine.repair",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; direct code read: SSE collection terminates only at a delimited response.completed event, completion validated before CPU analysis (not socket closure).",
   "negative_paths": "incomplete/corrupt capture -> no review, no repaired delivery; truncated or invalid UTF-8 tail held and reported incomplete, never presented as whole."
  },
  {
   "id": "LR-002",
   "class": "IMPLEMENTED",
   "runtime_path": "detector.py select + runtime_detection.py (deterministic, cap min(maximum,8)) -> proxy RepairEngine",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch and test_pandoc_protection (safe-known zero review calls; protected-only body returns exact original with zero calls).",
   "negative_paths": "no eligible suspicion -> zero review calls and unchanged text; prompt over bound returns None -> original with zero calls."
  },
  {
   "id": "LR-003",
   "class": "IMPLEMENTED",
   "runtime_path": "detector.py tokenize/select + runtime_detection.py phrase grouping (1-unit=word; 2-4 units within 128 code points = one exact original slice)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_detection (one-unit stays a word; 2-4-unit phrase within 128 code points; over-4 or over-128 yields NO targets).",
   "negative_paths": "model cannot expand/reposition/invent; over-128 or over-4 run leaves ALL its context-only candidates ungrouped -> no targets; protected boundaries never crossed."
  },
  {
   "id": "LR-004",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client.ResponsesReviewer.review_batch -> batch_review.build_prompt (BATCH_INSTRUCTION) + batch_review.build_request_body + review_transport.run_review_exchange (fresh single-turn user request); acceptance via runtime_acceptance.accept. The legacy qwen_client.prompt(frozen-v1) belongs to the single-target review() path and is NOT the runtime authority.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch (keep accepted; needs_wider_edit leaves target unchanged; identity rejected) + test_runtime_acceptance (test_identity_replacement_rejects / test_wider_edit_rejects). The batch prompt enforces the semantic narrow keep/wider-edit contract (not the literal PLAN §8.2 Slovenian system instruction, which is not an implementation gate).",
   "negative_paths": "needs_wider_edit=true or identity replacement -> rejected, target unchanged; no change is demanded (keep is a valid outcome). The exact literal PLAN-language prompt is not a new implementation gate; the semantic narrow natural-expression/keep/wider-edit contract is what is enforced."
  },
  {
   "id": "LR-005",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client.ResponsesReviewer.review_batch -> batch_review.build_prompt + batch_review.build_request_body (imported by qwen_client) + review_transport.run_review_exchange (fresh single-turn request; the real owned worker child performs the actual reviewer HTTP call to the configured private /responses endpoint). Real wire is proven by test_review_batch.py::TransportTests / CompositionChainTests and test_responses_contract.py::ContractHttpTests (real ResponsesReviewer -> real worker -> HTTPServer 127.0.0.1:0). The test_review_transport.py::WorkerSubprocessTests subset (owned fake worker via _REVIEW_WORKER_PATH) proves IPC framing / subprocess lifecycle only, NOT wire.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_transport::BatchExchangeTests (real-wire route/auth/body) + test_review_batch::TransportTests (test_single_request_exact_route_body_and_reordered_result / test_non_200_fails_whole_batch) + test_review_batch::CompositionChainTests (full real ConceptProxy HTTP chain) + test_review_batch (no previous_response_id, no main history/session linkage, no tools, no images, no project constitution). Seam declared: real owned worker child -> real HTTP to a synthetic in-process endpoint; the fake-worker IPC subset is framing-only.",
   "negative_paths": "no main session IDs/previous_response_id/conversation linkage/tools/images/tool-results; no recursion (reviewer never calls the public repair endpoint); no arbitrary caller destination or public bypass header; a non-200 reviewer reply fails the whole batch (no retry). (Software/transport real-wire proof; native real-Qwen serving is a separate layer - see D05.)"
  },
  {
   "id": "LR-006",
   "class": "IMPLEMENTED",
   "runtime_path": "batch_review.parse_batch_envelope (strict whole-batch parser; imported by qwen_client and called in review_batch) + runtime_acceptance.accept + repair.apply_edits (shared patcher) + composed_validation.validate_composed (code composes from exact original slices). The legacy qwen_client.parse_proposal is the single-target path, not the runtime.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_composed_validation + test_review_batch + test_runtime_acceptance (model returns only a local replacement; code validates and inserts).",
   "negative_paths": "code-fenced/oversize/invalid JSON/unknown-or-duplicate-or-missing id -> whole batch rejected; model never supplies a rewritten sentence or new coordinates; only one bounded assistant output_text accepted."
  },
  {
   "id": "LR-007",
   "class": "IMPLEMENTED",
   "runtime_path": "pandoc_protection.protect_with_pandoc + compose_protection (protected = complement of granted prose + retained machine residuals) + repair.apply_edits (post-composition protected-slice assertion)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c). + Independent offline probe of the 033-a changed protection consumer via the real protect_with_pandoc on the pinned binary: Slovenian low/high quote interior denied while outside prose granted; raw inline HTML tag interior denied while surrounding prose granted; fenced code denied while surrounding prose granted (deny-by-default, exact code-point grants, no AST rendering).; independent probe: quote/HTML/code interiors denied, outside prose granted; test_pandoc_protection exact-body and protected-outside-only rows.",
   "negative_paths": "a protected slice changed after composition raises AssertionError; unprovable/unproved regions stay protected; 032-era quote/HTML admission gaps are closed at this main (033-a remediation independently reproduced positive + fail-closed)."
  },
  {
   "id": "LR-008",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_corpus.RuntimeCorpus.unigram/ngram (Evidence state EXACT/CENSORED/UNAVAILABLE at runtime; EXACT(0) is a known zero, never positive support; unknown denominator preserved as unknown). Producer corpus.py separately describes the index manifest/type; the legacy repair._positive_local is NOT the wired runtime path.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_corpus (status per record; EXACT(0) known-zero never positive; CENSORED/UNAVAILABLE absence stays unknown) + test_analysis_policy content-free observations.",
   "negative_paths": "CENSORED/UNAVAILABLE absence stays unknown, never zero; EXACT(0) cannot count as positive local support; unknown denominator preserved as unknown. Legacy repair._positive_local is not the wired runtime path."
  },
  {
   "id": "LR-009",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_acceptance.accept (the replacement side must be an EXACT positive row; the original side is matched by the anchored comparable EXACT factor-two margin candidate_count >= 2*max(original_count,1) on the SAME ngram order - the R4 route; the narrow R5 possible-typo route accepts a single EXACT positive adjacent count where count 1 suffices and it is NOT subject to the factor-two floor; an unknown replacement context opposes; every replacement word EXACT) + composed_validation.validate_composed/_revalidate group revalidation. The legacy repair.accept / _positive_local is materially different and NOT the wired runtime path; only the shared Acceptance type/patcher remain in the runtime.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_acceptance named positive/negative tests: test_r4_factor_two_accepts / test_below_factor_two_rejects (factor-two margin); test_single_edit_accepts / test_zero_or_multi_edit_reject (one-codepoint edit route); test_r5_count_one_accepts_censored_original (narrow R5 count-1 route); test_unknown_original_context_rejects; test_known_zero_replacement_opposes_immediately; test_identity_replacement_rejects; test_wider_edit_rejects; test_reviewer_kept_rejects_before_queries. Plus test_composed_validation group revalidation.",
   "negative_paths": "A non-EXACT or unknown-count replacement word/context -> rejected/opposed; neutral or incomparable data insufficient; the narrow one-codepoint route is a single EXACT adjacent count on a one-codepoint edit, NOT a generic '>=1 positive bigram' statement; a self-reported confidence field is not used as an acceptance authority."
  },
  {
   "id": "LR-010",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client.review_batch (one bounded request, one monotonic deadline, no retry) + composed_validation (bounded CPU revalidation, no new generative pass)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch (one combined request; malformed JSON not re-queried; late/racing success is a failure).",
   "negative_paths": "malformed reviewer JSON is never repaired by another model call; no automatic generative repair/retry loop; the composed revalidation is CPU-only bounded checks."
  },
  {
   "id": "LR-011",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py failure contract + composed_validation.ComposedMappingError (whole pass abstains to the completed original while a live recipient remains) + request_lifecycle.RequestCancelled (client disconnect = quiet in-handler abort, proxy.py:1726ff; NOT original delivery to the closed client).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_request_cancellation (test_rst_cancels; test_fin_behind_unread_tail_cancels_without_reading; test_live_peer_with_unread_tail_is_not_cancelled; test_racing_completion_with_cancel_closed_and_cancelled; _ProxyLateHandoffRegressionTests order 030-a late-handoff boundary regressions) + test_main_lifecycle + test_runtime_acceptance.",
   "negative_paths": "Distinguished: (a) optional repair failure / unprovable composed mapping with a live recipient -> the whole optional pass abstains to the conservatively completed original; (b) client disconnect -> quiet in-handler RequestCancelled abort, no body delivered to the closed socket; (c) main generation error/incomplete -> documented error/finish semantics, never a repaired success; (d) hard capture limit -> bounded API failure, never truncated-as-whole."
  },
  {
   "id": "LR-012",
   "class": "IMPLEMENTED",
   "runtime_path": "concept-verification package is CPU-only standard-library Python; no model/quantization loading, no GPU; the MAIN upstream and the REVIEWER model are configured independently (no automatic same-model enforcement); the reviewer is a configured/injected operator endpoint (CONCEPT_REVIEWER_MODEL).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; direct code read: no model loading or deployment mutation anywhere in the proxy path; config read shows the main upstream and the reviewer model are set independently.",
   "negative_paths": "no second large GPU model loaded; no protected deployment/weights/vLLM/CUDA/launch-flag/port mutation; main and reviewer model IDs are configured independently, so qualification requires the actually configured/exercised main and reviewer routes to be shown to match (no automatic same-model guarantee); native real-Qwen reuse is a separate serving-compatibility layer, not exercised here."
  },
  {
   "id": "LR-013",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py content-free finite reason vocabulary + opt-in bounded stderr usage observer (CONCEPT_USAGE_OBSERVER=stderr) in the default TRACE-DISABLED functional profile (no trace file written); opt-in CONCEPT_TRACE_DIR write_traces (proxy.py:2112ff) serializes FULL content (original/repaired/candidates/corpus_summaries/reviewer_decisions/acceptance/replacements), files 0600 (mkstemp tmp + os.replace).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_analysis_policy content-free observations (default profile: reason labels / usage observer carry no user text); direct code read of write_traces (proxy.py:2112ff) and the CONCEPT_TRACE_DIR opt-in (proxy.py:2357/2417).",
   "negative_paths": "In the default (trace-disabled) functional profile no trace file is written and production reason labels / usage observations are content-free (no user text, target/replacement strings, prompts or raw responses). The opt-in trace is content-carrying RAW and is an operator disclosure, NOT a production default; a trace-directory write failure is a known caveat that can turn completed-original delivery into a 502 (032), NOT an unconditional fallback. The real evaluation channel is separate and owner-authorized."
  },
  {
   "id": "LR-014",
   "class": "IMPLEMENTED",
   "runtime_path": "this audit keeps the four evidence layers separate (software offline-tested; native serving 0 target calls/unproven; linguistic quality excluded; deployment owner-retained)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "This audit: 0 target calls; deployment_authorized=false; human_milestone_accepted=false; software vs serving vs linguistic vs deployment kept distinct throughout.",
   "negative_paths": "native serving compatibility, linguistic benefit and deployment authority are NOT conflated with the offline software evidence; each is reported as its own layer."
  },
  {
   "id": "A-SCOPE-01",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py Responses envelope handling + responses_contract.py (only assistant output_text of natural message items is edited)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_responses_contract + test_pandoc_protection (reasoning/tools/function-args/IDs/usage preserved).",
   "negative_paths": "no factual correction/translation/whole-answer rewriting; tool/unsupported/no-safe-text responses are bypassed (not recursively repaired)."
  },
  {
   "id": "A-SEAM-01",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client.ResponsesReviewer (injectable) + proxy.py (no conversation store; request-local state; sequential main->review)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; fake deterministic reviewer used across the offline suite (test_review_batch, test_runtime_acceptance).",
   "negative_paths": "no shared mutable conversation list or response buffer across requests; the reviewer is injectable so the full logic is testable without a model; cancellation targets only request-owned work."
  },
  {
   "id": "A-STACK-01",
   "class": "PARTIAL",
   "runtime_path": "concept-verification/* (stdlib) vs src/llm_slovenian_repair/* (skeleton)",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The runnable proxy is a deliberately isolated standard-library concept-verification spike (http.client, unittest; no uv/HTTPX/Pydantic/FastAPI), not the A-STACK-01 production library baseline. The src/llm_slovenian_repair production library is a 5-module development skeleton (__init__, contracts, policy, source_manifest, unigram_importer), not the runnable proxy. Module responsibilities (contracts/policy, protected/tokenizer, corpus, detector, prompts/reviewer, acceptance, patcher, pipeline, CLI, API) and no-import-time-network hold in the spike; the production typed-HTTPX stack is not where the runnable proxy lives."
  },
  {
   "id": "A-ROUTE-01",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client.responses_path + configured reviewer base URL (operator-controlled private /responses endpoint; no public recursion/bypass)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_transport (no recursion, no arbitrary caller destination).",
   "negative_paths": "the isolated review never calls the public repair endpoint from itself; no public bypass header; production gateway public-auth/quotas integration is a later-stage (S03) connection, not part of the loopback concept."
  },
  {
   "id": "A-SPAN-01",
   "class": "IMPLEMENTED",
   "runtime_path": "pandoc_protection.map_span/map_block_span + _Document (Unicode code-point offsets into the unmodified original) + runtime_acceptance.accept stale-slice validation",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c). + Independent offline probe of the 033-a changed protection consumer via the real protect_with_pandoc on the pinned binary: Slovenian low/high quote interior denied while outside prose granted; raw inline HTML tag interior denied while surrounding prose granted; fenced code denied while surrounding prose granted (deny-by-default, exact code-point grants, no AST rendering).; test_pandoc_protection (repeated occurrences via before_target/target/after_target; Unicode/CRLF/combining marks).",
   "negative_paths": "0<=start<end<=len; text[start:end]==original enforced; stale or out-of-bounds coordinates rejected before slicing; no protected intersection; repeated identical words disambiguated by exact occurrence context; no UTF-8/UTF-16/model-token offsets used for grants."
  },
  {
   "id": "A-PROTECT-01",
   "class": "IMPLEMENTED",
   "runtime_path": "pandoc_protection._classify_inline/_walk_blocks/_walk_inlines (deny-by-default; only proven Str leaf spans granted) + compose_protection",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c). + Independent offline probe of the 033-a changed protection consumer via the real protect_with_pandoc on the pinned binary: Slovenian low/high quote interior denied while outside prose granted; raw inline HTML tag interior denied while surrounding prose granted; fenced code denied while surrounding prose granted (deny-by-default, exact code-point grants, no AST rendering).; independent probe: code/HTML/quote interiors denied, outside prose granted; BlockQuote denied in full.",
   "negative_paths": "tools/functions/IDs/schemas/structured output/reasoning/images/binary data uneditable; only supported assistant text fields selected (no recursive JSON string repair); fenced/inline code, URLs, emails, paths, commands, numbers/units, quotes, config, metadata, escapes, entities and every unprovable region protected; protected intervals are linguistic boundaries (no artificial adjacency)."
  },
  {
   "id": "A-CORPUS-01",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_corpus.RuntimeCorpus.unigram/ngram (Evidence status/count at runtime); producer corpus.py prepare provenance separately describes the manifest/type (source sha256s, member names, ngram_cutoff, denominator unknown, absence semantics).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_corpus (status per record; denominator known/unknown separated).",
   "negative_paths": "retained n-gram sums are not a complete denominator; censored surface-form aggregation is not a complete lemma distribution; comparisons require compatible scope/normalization/units."
  },
  {
   "id": "A-CORPUS-02",
   "class": "PARTIAL",
   "runtime_path": "corpus.py prepare (provenance dict); bounded read-only authority over private local index.",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The index provenance manifest records source identity (member names), checksums (words/ngrams archive SHA-256), the n-gram cutoff and an explicit 'denominator unknown', and the UNAVAILABLE/CENSORED absence semantics, and the index is private external data never bundled or packaged. It does NOT explicitly record, as named fields, rights/license status, normalization/tagging conventions, importer version, or deterministic build parameters (these are implicit in the code/design). NON-REDISTRIBUTION IS NOT rights/license authorization: the existing authority is bounded read-only access to the private local archives/index, and non-redistribution is a handling practice, not a license grant; there is no acquisition, public redistribution, runtime scraping, or full-corpus gate in this audit. Public query access != bulk permission."
  },
  {
   "id": "A-DETECT-01",
   "class": "IMPLEMENTED",
   "runtime_path": "detector.py + runtime_detection.py (suspicions, deterministic non-overlap, ordered by position, cap 8; excess/ambiguous unchanged with finite reason labels)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_detection + test_analysis_policy.",
   "negative_paths": "unknown/rare/name is a reason to investigate only, not a verdict; weak surroundings give weak evidence; no ranked corpus alternatives are sent to the reviewer; excess/ambiguous targets remain unchanged with bounded reason codes."
  },
  {
   "id": "A-QUESTION-01",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client.ResponsesReviewer.review_batch -> batch_review.build_prompt (BATCH_INSTRUCTION: narrow target review; preserve meaning/register; no rewrite; keep/replace/wider; data-not-instruction). The legacy qwen_client.prompt(frozen-v1) belongs to the single-target review() path, NOT the runtime authority.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch (embedded instructions in the reviewed material are data; no tool/URL execution; no main history).",
   "negative_paths": "material is untrusted data including embedded instructions (never become reviewer authority); threads/async alone are not the isolation guarantee; the batch prompt enforces the semantic narrow keep/wider-edit contract rather than the literal PLAN §8.2 Slovenian system instruction (an engineering variant per ARCH §10.3); the exact literal PLAN-language prompt is not an implementation gate."
  },
  {
   "id": "A-SCHEMA-01",
   "class": "IMPLEMENTED",
   "runtime_path": "batch_review.parse_batch_envelope/strict_json_object (one result per id; keep=>replacement=null; keep=false=>nonempty replacement; needs_wider_edit=>keep=true, replacement=null)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch (unknown/duplicate/missing ids, invalid/oversized JSON, fenced output all reject the whole batch).",
   "negative_paths": "unknown/duplicate/missing ids, invalid JSON, invalid field types, contradictory fields or oversized output reject the whole batch (never salvaged); response order is never used to align proposals with targets."
  },
  {
   "id": "A-ACCEPT-01",
   "class": "PARTIAL",
   "runtime_path": "runtime_acceptance.py (single conservative path)",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The runnable concept spike implements the single conservative (strict-like AUTO_REPAIR) acceptance path only. The named selectable modes detect_only / shadow / experimental and the detect_only -> shadow -> measured-limited-strict development sequence are not present as selectable modes in the spike; it is a fixed conservative repairer."
  },
  {
   "id": "A-ACCEPT-02",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_acceptance.accept (all conditions: EXACT positive replacement; anchored comparable factor-two R4 margin / narrow R5 typo route; unknown-count opposition) + composed_validation.validate_composed (group revalidation) on the 033-a protection map. The legacy repair.accept is NOT the wired runtime path; only the shared Acceptance type/patcher remain in the runtime.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; Independent offline probe of the 033-a changed protection consumer via the real protect_with_pandoc on the pinned binary (mapping-only three-case probe; it does not by itself prove the real Engine/real HTTP or all 14 prior counterexamples, which the 965 suite covers): Slovenian low/high quote interior denied while outside prose granted; raw inline HTML tag interior denied while surrounding prose granted; fenced code denied while surrounding prose granted (deny-by-default, exact code-point grants, no AST rendering). + test_runtime_acceptance + test_composed_validation; 033-a protection gaps (032) independently confirmed closed at this main.",
   "negative_paths": "identity/forbidden-newline/control/markup/overlong/scope-expansion rejected; neutral or incomparable data insufficient; LLM_CONFIRMED_REPAIR without sufficient independent evidence remains disabled for automatic user-text changes; conflicting nearby changes reject the group and rebuild from the original."
  },
  {
   "id": "A-PATCH-01",
   "class": "IMPLEMENTED",
   "runtime_path": "repair.apply_edits (descending offsets; non-overlap; protected-slice assertion) + composed_validation (conflict-group rejection)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_composed_validation + test_pandoc_protection (exact untouched content; no-edit equality).",
   "negative_paths": "overlap/stale/protected/incompatible edits raise; no silent last-wins; no model answer/detokenization/Markdown renderer substitutes for the document; no surviving edit -> exact original text; text equality vs HTTP-byte equality distinct."
  },
  {
   "id": "A-API-01",
   "class": "PARTIAL",
   "runtime_path": "proxy.py (one nonstreaming Responses text shape) + capture/delivery transports",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "A single nonstreaming Responses text shape is implemented and offline-tested with a fake upstream (JSON and SSE round trips on loopback), and no universal Chat/Responses compatibility is claimed. The ACTUAL native Qwen endpoint/schema compatibility is a separate live-serving layer not exercised in this 0-target-call offline audit; the deferred index records that an earlier RTX main failed a completion-envelope validator before repair."
  },
  {
   "id": "A-HISTORY-01",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py delivery (final delivered answer only; usage preserved) + batch_review (reviewer usage carried separately) + no mutation of input history",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_responses_contract (delivered content is the final text; usage/event order preserved).",
   "negative_paths": "the delivered answer is the final text, never an extra draft or review prompt/JSON; main-generation usage and review usage are separate (final token count is neither inference bill). LIMIT: logprobs/annotations invalidation on changed text is not exercised in the loopback concept (the fake upstream carries no logprobs) and server-managed history chaining is unsupported - a later-integration concern."
  },
  {
   "id": "A-LIMIT-01",
   "class": "IMPLEMENTED",
   "runtime_path": "config.py (bounded finite defaults) + detector cap 8 + qwen_client.review_batch deadlines + proxy independent budgets",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_analysis_policy (byte/codepoint boundary; oversize gate zero work; separate reasons).",
   "negative_paths": "at most 1 review request per response, 1 pass, 0 automatic retries, at most 8 targets, bounded target/replacement sizes; capture/analysis/context/prompt/output/queue/total-review bounds finite; no fabricated target-machine throughput; CPU work bounded and cancellable."
  },
  {
   "id": "A-FAIL-01",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py + composed_validation.ComposedMappingError + request_lifecycle + corpus missing/corrupt handling",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_main_lifecycle + test_request_cancellation + test_runtime_corpus + test_analysis_policy.",
   "negative_paths": "no suspicion -> unchanged/zero calls; missing/corrupt/incompatible corpus -> degraded original, no invented counts; queue full/timeout/transport/invalid batch -> cancel owned work, return completed original; client disconnect -> cancel owned upstream/review, no orphan work; optional fallback never bypasses auth/validation/hard limits/isolation."
  },
  {
   "id": "A-SECURITY-01",
   "class": "IMPLEMENTED",
   "runtime_path": "qwen_client (no tools; reviewed material as data) + config/env credentials external to Git + content-free reason labels in the default trace-disabled profile; the opt-in CONCEPT_TRACE_DIR write_traces is content-carrying raw (operator disclosure).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch (prompt-injection material is data, not executed); direct code read (credentials via env/profile, never in Git; write_traces proxy.py:2112ff is content-carrying and opt-in).",
   "negative_paths": "embedded instructions/paths/URLs in output are never executed; the reviewer has no tools and no file/conversation-write authority; credentials are external to Git and referenced without logging values; no unnecessary cross-user text caching. The content-free reason/usage labels hold in the default trace-disabled profile; the opt-in trace is content-carrying raw (an operator disclosure, not a default) and a trace write failure is a known 502 caveat, not an unconditional fallback."
  },
  {
   "id": "A-TEST-01",
   "class": "IMPLEMENTED",
   "runtime_path": "concept-verification/tests (synthetic deterministic suite: capture/isolation/mapping/protected/corpus/reviewer/acceptance/patching/operations/API)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c). (965 synthetic deterministic tests, exit 0) at the audited main with the pinned Pandoc.",
   "negative_paths": "a green test that mocked the named boundary would not certify it; the suite exercises the real boundary with the pinned Pandoc and owned loopback; NOTE: live opt-in tests (real Qwen) are a separate evidence layer not exercised in this 0-call offline audit."
  },
  {
   "id": "A-EVAL-01",
   "class": "UNPROVEN",
   "runtime_path": "concept-verification/eval/ (run_eval.py, score.py, review_sheet.py, dev16/heldout32, frozen-experiment.json) - framework present, unmeasured.",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The deterministic held-out evaluation framework exists (dev 16 / held-out 32 cases, frozen calibration/held-out split, ablations with denominators, candidate enrichment, recall, reviewer accuracy, accepted/correct/harmful/missed counts) and the held-out reviewer/collector commands are defined. Measured linguistic benefit/harm is OWNER-EXCLUDED, NOT deferred: there is no separate human evaluation dataset and no current or future human-labeling obligation, so quality is unmeasured by this audit and no separate dataset gate applies; historical source labels, where present, are historical only. The approximate 99% precision and 1 harm/10k remain unmeasured goals, not results or release authority. Qwen is not the final judge of its own changes; useful benefit and bounded harm are both required before any quality claim."
  },
  {
   "id": "A-GOV-01",
   "class": "IMPLEMENTED",
   "runtime_path": "OAP governance (root router, coding/strategic constitutions, order/active, CRITICAL, report-history, whitespace, transcript) + this audit follows the ordered round",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Order 034-a metadata (governance 3549de2a, all 16 identities) validated by the ordered OAP checks; this audit uses the exact active order and SELF publication contract.",
   "negative_paths": "no private canonical PLAN/ARCH/CRITICAL mirrors; the audit does not merge, deploy, or author human acceptance; one numeric objective = one branch/PR; D0, Decision NONE."
  },
  {
   "id": "A-CLOSE-01",
   "class": "IMPLEMENTED",
   "runtime_path": "this Independent Closure Audit (fresh source-first context; complete requirements; IMPLEMENTED/PARTIAL/ABSENT/UNPROVEN; real paths/evidence/SHA; reports treated as claims)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "This audit (034-a) performs the ICA on current merged main c36ed4f; check_ica enforces schema/scope/coverage/revision/input-order; strategy recommends, human decides.",
   "negative_paths": "queue completion is no completeness proof; the audit does not merge code or authorize deployment; a fresh ICA repeats after remediation; this audit is independent architecture-to-main evidence, not execution self-approval."
  },
  {
   "id": "MVP-1",
   "class": "IMPLEMENTED",
   "runtime_path": "capture_transport (full completion before analysis/review/delivery) -> proxy delivery",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; direct code read + fresh suite.",
   "negative_paths": "no provisional original text reaches the user; the full main answer is captured and completion-validated before any review call or delivery."
  },
  {
   "id": "MVP-2",
   "class": "IMPLEMENTED",
   "runtime_path": "detector (no eligible suspicion) -> zero review calls",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch + test_pandoc_protection (zero review calls).",
   "negative_paths": "without sufficient suspicion there is no additional Qwen call and the text is unchanged."
  },
  {
   "id": "MVP-3",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_acceptance.accept (only the assigned span replaced or left) + batch_review (one result per id).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_acceptance + test_review_batch.",
   "negative_paths": "Qwen may only replace the assigned span or answer keep/wider-edit; it cannot expand the target or rewrite the sentence."
  },
  {
   "id": "MVP-4",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py (delivered content is the final text; no review JSON/prompt in delivered content) + no input-history mutation",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_responses_contract.",
   "negative_paths": "the main history does not contain the repair conversation or its internal results; the review JSON/prompt is never delivered to the user or stored as main history."
  },
  {
   "id": "MVP-5",
   "class": "IMPLEMENTED",
   "runtime_path": "pandoc_protection (deny-by-default grants) + runtime_acceptance.accept protected/barrier checks + repair.apply_edits protected-slice assertion",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c). + Independent offline probe of the 033-a changed protection consumer via the real protect_with_pandoc on the pinned binary: Slovenian low/high quote interior denied while outside prose granted; raw inline HTML tag interior denied while surrounding prose granted; fenced code denied while surrounding prose granted (deny-by-default, exact code-point grants, no AST rendering).; independent probe (quote/HTML/code denied, outside granted); test_pandoc_protection.",
   "negative_paths": "no change happens outside programmatically verified exact original spans; a protected or barrier-crossing edit is rejected and any changed protected slice raises."
  },
  {
   "id": "MVP-6",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy failure contract + composed_validation.ComposedMappingError (abstain to completed original while a live recipient remains) + request_lifecycle.RequestCancelled (client disconnect = quiet in-handler abort, not original delivery to the closed client).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_main_lifecycle + test_request_cancellation (test_rst_cancels; test_racing_completion_with_cancel_closed_and_cancelled) + test_composed_validation (test_mapping_abort_known_usage_whole_pass_abstains).",
   "negative_paths": "an invalid proposal or an optional repair failure does not damage the already completed answer while a live recipient remains (exact original preserved, exact review-call/usage accounting); a client disconnect is a quiet in-handler RequestCancelled abort, NOT original delivery to the closed client; the opt-in trace write failure is a known 502 caveat, not an unconditional fallback."
  },
  {
   "id": "MVP-7",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_corpus.RuntimeCorpus.ngram/unigram (ngram_absence=CENSORED; ngram_cutoff 'denominator unknown'; EXACT(0) not positive). Producer corpus.py separately describes the index manifest/type; the legacy repair._positive_local is NOT the runtime path.",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_corpus + test_analysis_policy (EXACT(0) is a known zero, never positive support).",
   "negative_paths": "published cut frequencies are not treated as complete statistics; CENSORED absence is not zero; a known zero is not positive support."
  },
  {
   "id": "MVP-8",
   "class": "PARTIAL",
   "runtime_path": "eval/score.py + eval/results/summary.json + proxy usage observer (bounded stderr) + timings",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "A transparent reporting infrastructure exists (accepted/correct/harmful/missed counts, denominators, latency, separate main vs review usage, ablations). The MEASURED benefit and damage on held-out real answers depends on the owner-EXCLUDED human evaluation dataset, so the measured benefit/damage figures are not produced here; the reporting structure is implemented but the benefit/damage numbers are unmeasured."
  },
  {
   "id": "D01",
   "class": "IMPLEMENTED",
   "runtime_path": "config.py + qwen_client.Proposal + batch_review.BatchResult + repair.Acceptance (span/evidence/proposal/result contracts; keep vs replace separated)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_review_batch + test_runtime_acceptance.",
   "negative_paths": "keep and replace are distinct first-class outcomes with strict, validated contracts."
  },
  {
   "id": "D02",
   "class": "IMPLEMENTED",
   "runtime_path": "corpus.py prepare (reproducible index from explicit external archives with byte/MD5/SHA-256, member, header/marker, CRLF, UTF-8, width and row-limit verification) + provenance (UNAVAILABLE/CENSORED distinction)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_corpus (missing index -> degraded original, no invented counts).",
   "negative_paths": "a missing/corrupt index -> degraded original, no invented frequencies; word absence is UNAVAILABLE, missing n-grams are CENSORED with unknown denominator; import is reproducible from explicit archive paths."
  },
  {
   "id": "D03",
   "class": "IMPLEMENTED",
   "runtime_path": "pandoc_protection (mandatory pinned Pandoc source-position mapping to the unmodified original; tokenization without changing the original) + detector",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c). + Independent offline probe of the 033-a changed protection consumer via the real protect_with_pandoc on the pinned binary: Slovenian low/high quote interior denied while outside prose granted; raw inline HTML tag interior denied while surrounding prose granted; fenced code denied while surrounding prose granted (deny-by-default, exact code-point grants, no AST rendering).; test_pandoc_protection (code/URL/Unicode tests; startup check before bind).",
   "negative_paths": "tokenization never changes the original; code, URLs, links, quotes, numbers, mixed languages and ambiguous Markdown are protected; no reserialization/detokenization is used to patch."
  },
  {
   "id": "D04",
   "class": "IMPLEMENTED",
   "runtime_path": "detector.py + runtime_detection.py (selects a bounded set of suspicious spots; does not send everything to the model)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_detection + test_analysis_policy.",
   "negative_paths": "the detector distinguishes selected suspicious spots on a small set and does not send the whole answer to the model; at most 8 targets."
  },
  {
   "id": "D05",
   "class": "PARTIAL",
   "runtime_path": "qwen_client.ResponsesReviewer (real HTTP client) whose real owned worker child performs the actual reviewer HTTP call to a synthetic in-process endpoint (HTTPServer 127.0.0.1:0); the four allocated slots are TARGET POST slots counting MAIN and REVIEW separately. Native real-Qwen serving is NOT exercised in this offline order.",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "Native real-Qwen serving compatibility is UNPROVEN in this offline order (0 authorized native calls; the four allocated slots are TARGET POST slots counting MAIN and REVIEW separately, NOT four proven review requests). IMPLEMENTED SEPARATELY (proven as REAL wire / software-transport): the real ResponsesReviewer + owned worker child make real reviewer HTTP to a synthetic in-process endpoint, asserted on route/auth/body and the whole-batch result - test_review_batch.py::TransportTests.test_single_request_exact_route_body_and_reordered_result (real ResponsesReviewer -> real worker -> HTTPServer 127.0.0.1:0; negative test_non_200_fails_whole_batch), test_review_batch.py::CompositionChainTests (real ConceptProxy HTTP -> RepairEngine/Pandoc/tinySQLite -> real ResponsesReviewer -> fake MAIN/REVIEW HTTP endpoints), test_responses_contract.py::ContractHttpTests (real reviewer HTTP), test_review_transport.py::BatchExchangeTests (real owned worker child -> real HTTP per wire case). The test_review_transport.py::WorkerSubprocessTests subset (owned fake worker via mock.patch.object(qwen_client, '_REVIEW_WORKER_PATH', ...)) proves the IPC framing / subprocess lifecycle only and is NOT wire proof. NOT PROVEN: the real-Qwen condition - the prior 031-b native RTX MAIN (HTTP 200 / 2105 B / 4.721 s) failed the actual completion-envelope validator (the exact rejected clause is not retained here) and the allocated slots are exhausted; historical A100 isolated-review success is a different model/quantization/evidence layer. An owned fake-worker endpoint can NEVER satisfy the native retest. Smallest sufficient next step (no live call in 034): ONE authorized MAIN-path reproduction with a minimal content-free observer of the ACTUAL failed completion-envelope predicate, stopping at the first unresolved boundary (reserve one main plus a possible review under new owner allowance); a subsequent actual-Qwen isolated batch can then qualify the reviewer condition. No live requests in 034; the extra 12-slot allowance is unanswered."
  },
  {
   "id": "D06",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_acceptance.accept + repair.apply_edits (the shared patcher) + composed_validation (accept/reject proposals; preserve all other segments).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_composed_validation (test_mapping_abort_known_usage_whole_pass_abstains; test_multiword_adjacent_group_rejects_whole) + test_runtime_acceptance.",
   "negative_paths": "code accepts or rejects proposals and preserves all other segments exactly; a protected slice changed after composition raises."
  },
  {
   "id": "D07",
   "class": "IMPLEMENTED",
   "runtime_path": "run_proxy.sh (owned entry) + eval/collect.py + eval/review_sheet.py + eval/score.py (local inspection; real cases are not hard-coded special rules)",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_concept + test_main_lifecycle (owned main() driven in bounded owned children; the real RepairEngine with real pinned Pandoc).",
   "negative_paths": "the entry point drives the real engine and the real pinned Pandoc in bounded owned children; real evaluation cases are not embedded as special-cased rules in the detector/acceptance."
  },
  {
   "id": "M01",
   "class": "ABSENT",
   "runtime_path": "(absent in the runnable concept spike)",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The owner EXCLUDES a separate human evaluation dataset (excluded, not deferred). No human-labeled real-answer set is present in the runnable concept spike; only synthetic deterministic cases (dev 16 / held-out 32) exist. A separate threshold-tuning split over real answers is therefore out of scope for this audit."
  },
  {
   "id": "M02",
   "class": "ABSENT",
   "runtime_path": "(absent; no morphology/lemma CPU analyzer in the spike)",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The runnable concept spike has no CPU morphology/lemma analyzer; detection uses unigram/n-gram lexical evidence only, so it does not separate a wrong lexeme choice from a wrong inflection at the morphology layer. Morphology/lemmatization is an optional bounded later-stage dependency (PLAN section-6.1, ARCH section-4.1), not present here; it is not a functional-MVP blocker for the conservative lexical path."
  },
  {
   "id": "M03",
   "class": "IMPLEMENTED",
   "runtime_path": "runtime_detection.py (2-4 unit phrase grouping within 128 code points; clear edit width) + batch_review needs_wider_edit",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_runtime_detection (grouped phrase target; over-128/over-4 -> no targets).",
   "negative_paths": "limited alarm merging with clear edit width; a working needs_wider_edit path leaves the target unchanged; merging never crosses protected material or grows to a paragraph."
  },
  {
   "id": "M04",
   "class": "PARTIAL",
   "runtime_path": "batch_review.build_prompt (BATCH_INSTRUCTION, the runtime batch path) + qwen_client prompt-variant versioning (frozen-v1 vs dev-v2 on the legacy single-target path) + config.py (rule versioning) + eval/score.py (measurement harness).",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "Acceptance rule/prompt versioning (frozen-v1 vs dev-v2, bounded thresholds) is implemented and offline-testable; the runtime batch path uses BATCH_INSTRUCTION. The measured calibration of correctness/damage/coverage by error class on real held-out data depends on the owner-EXCLUDED human evaluation dataset (excluded, not deferred; no separate dataset gate), so the measured calibration is not produced in this audit; the reporting/measurement harness exists but is unmeasured."
  },
  {
   "id": "M05",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy independent budgets + request_lifecycle.RequestCancelled (client disconnect = quiet in-handler abort, not original delivery to the closed client) + review_worker/deadlines + failure->original (exact original preserved while a live recipient remains).",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f (broad evidence only - not each named boundary by itself): 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC 3.7.0.2, qualified python -B, OAP_ROLE=coding, shell umask 0077 (final synchronous run began 09:35:44; SUITE_EXIT 0 observed 09:46:53.975Z; private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_request_cancellation + test_main_lifecycle + test_analysis_policy.",
   "negative_paths": "queue/time/size bounds; the exact original is preserved on any optional repair failure while a live recipient remains; a client disconnect is a quiet in-handler RequestCancelled abort (cancels only owned work, no delivery to the closed socket); no unbounded growth."
  },
  {
   "id": "M06",
   "class": "IMPLEMENTED",
   "runtime_path": "proxy.py (one explicitly supported nonstreaming Responses text shape; loopback HTTP adapter) + capture/delivery transports",
   "tested_sha": "c36ed4f42534bc13df4dac2b418fb50262d47d06",
   "evidence": "Fresh full offline suite at audited main c36ed4f: 965 tests, 584.337 s, OK, exit 0, pinned CONCEPT_PANDOC, qualified python -B, shell umask 077 (private run log SHA-256 b0d53b2da371136da5f947e8dece6e984fe525eb066aeff056a8039e9a4ed27c).; test_responses_contract + test_concept (JSON and SSE round trips on a real loopback).",
   "negative_paths": "one clearly supported nonstreaming text shape; context preserved; no recursion; the loopback adapter is the concept-level nonstreaming API path (the production FastAPI adapter is the later src/ library, not the runnable concept spike)."
  },
  {
   "id": "M07",
   "class": "UNPROVEN",
   "runtime_path": "concept-verification/eval/ (ablation report: raw/no-repair, detector-only, reviewer-decision, full conservative, unigram-only, local-context)",
   "tested_sha": "",
   "evidence": "",
   "negative_paths": "",
   "gap": "The comparison/ablation framework (agreed method vs original and basic comparison methods, with denominators and candidate enrichment) exists and is deterministic. The actual measured comparison on real held-out Qwen answers requires the live reviewer plus human labeling, which the owner EXCLUDES; so the measured comparison report is unproven/unproduced in this offline audit."
  }
 ],
 "deployment_authorized": false,
 "human_milestone_accepted": false,
 "private_initial_record": {
  "logical_id": "PRIVATE_INITIAL_034",
  "bytes": 24661,
  "sha256": "bb29467e687ad8d75810d8c6290225e5818b3a61b8e6e5acccb38e54bd3ade21",
  "tracked_public_file": false,
  "bytes_rewritten": false,
  "Root_preserved": true,
  "note": "The complete initial requirements-first record is private and unpublished; it is cited by logical ID, byte count, hash and provenance only. Its public citation path is omitted by placement handling (no new public projection path is authorized); the privacy-safe normative subset (owner scope, full source requirements, applicability model, owner-excluded items) is published in the evidence appendix source_derived_projection; the complete source-derived requirements/coverage and registry projection are published in this audit and its evidence appendix."
 }
}
```

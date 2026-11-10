# ICA 031-a — fresh source-first functional proxy audit (audit-only)

Evaluated product: accepted merged main `3bd6ffdd96bda95bd4c6de447b56cce76fe5a058`
(= HEAD = main = origin/main at audit time; tracked-clean except the pending
031-a dispatch edits `oap/active` and `oap/orders/031-a-functional-proxy-audit.md`,
which this round commits as scoped non-report artifacts). Full PLAN 1.0
SHA-256 `d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0`,
full ARCHITECTURE 1.1 SHA-256
`a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7` (both
verified byte-equal to the pinned governance identities).

Product under audit: the runnable proxy `concept-verification/` (27 top-level
modules + tests + eval) and the library core `src/llm_slovenian_repair/`
(contracts/policy/unigram importer). This is an audit-only D0 round: no
product edits, no target-model calls, no merge, no milestone or deployment
acceptance is claimed or granted.

```oap-ica
{
  "status": "FINAL",
  "milestone": "MVP",
  "main_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058",
  "architecture_sha256": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
  "plan_sha256": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
  "auditor": "fresh-context codex coding pane (OAP_ROLE=coding), same adopted foreground process, /new conversation at the quiescent pane, current worktree, early-beta model; declared independence corroborated by the observed source-first workflow, not statistical independence",
  "context_provenance": "Source-first per order R1/R2: owner scope (order Provenance H + phase-1 resource handoff) then full PLAN.md and full ARCHITECTURE.md read at the pinned product BEFORE any strategic claim or implementation-code inspection; immutable requirements-first artifact saved and hashed before continuing (oap/audit/results/031-functional-proxy-requirements-first.json, 53339 bytes, SHA-256 fbcda5cf77d65914f87892e2de797589c549383b71bb3c1e0db6eb8afea9322d, 2026-11-10T15:13:42Z); README/STATUS/implementation reports/strategic claims read only AFTER derivation, as claims indexes",
  "input_order": ["human_scope", "full_architecture", "current_main", "strategic_claims"],
  "deployment_authorized": false,
  "human_milestone_accepted": false,
  "matrix": [
    {"id": "LR-001", "class": "IMPLEMENTED", "runtime_path": "concept-verification/proxy.py _Handler.do_POST -> forward(); capture_transport.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3 e2e at 3bd6ffd: 200 completed only after full capture (0.162 s); protocol completion checks (exact Content-Length/chunked/SSE response.completed) in capture_transport.py; D2 test_concept.py 19 passed at 3bd6ffd", "negative_paths": "incomplete main never delivered as success: honest protocol error (A-FAIL-01 path, request_lifecycle abort); hard capture limit -> bounded failure (config max_safe_capture_*)", "gap": ""},
    {"id": "LR-002", "class": "IMPLEMENTED", "runtime_path": "proxy.py RepairEngine path -> runtime_detection.py detect()", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C engine probe at 3bd6ffd: clean synthetic text + real truncated index -> 0 candidates, 0 review calls, byte-identical original; B-v3: exactly one review call only for the one eligible planted candidate", "negative_paths": "no eligible suspicion -> zero review calls and unchanged text, proven at the real engine boundary", "gap": ""},
    {"id": "LR-003", "class": "IMPLEMENTED", "runtime_path": "runtime_detection.py (CPU target preassignment); batch_review.py (serialization of marked occurrences)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: targets are CPU-preassigned words/short phrases with stable IDs; model output constrained to one result per supplied ID", "negative_paths": "unknown/duplicate/missing proposal ID -> whole batch rejected at the real boundary (C5: REVIEW_UNKNOWN_ID); model cannot expand, reposition or invent IDs", "gap": ""},
    {"id": "LR-004", "class": "IMPLEMENTED", "runtime_path": "batch_review.py BATCH_INSTRUCTION (line 88)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "instruction asks expression suitability and permits keep / insufficient-context / wider-edit decline; rejects stylistic-only and factual changes (source text; B-v3 review request carries the batch instruction); C probe keep and wider-edit proposals left the target unchanged", "negative_paths": "no change is demanded; wider edit leaves target unchanged (C probe); the wording-fidelity deviation is tracked separately under A-QUESTION-01", "gap": ""},
    {"id": "LR-005", "class": "IMPLEMENTED", "runtime_path": "qwen_client.py ResponsesReviewer (one fresh POST to operator-configured endpoint)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: review request is fresh (no previous_response_id/conversation/tools keys - probed empty set; store:false; stream:false; model=probe-model; no Authorization header); main and review are separate sequential requests", "negative_paths": "no linkage keys present (probed); no recursion through a repair/public adapter (reviewer destination is operator-configured, never caller-supplied)", "gap": ""},
    {"id": "LR-006", "class": "IMPLEMENTED", "runtime_path": "batch_review.py (validation) -> repair.py apply_edits", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe accepted case: code validated the local proposal and inserted the exact replacement only; changed output differs from the original solely inside the validated span", "negative_paths": "the model never regenerates the answer or supplies replacement sentences (schema admits per-ID replacements only); invalid batch rejected whole (C5)", "gap": ""},
    {"id": "LR-007", "class": "IMPLEMENTED", "runtime_path": "repair.py + protected.py + pandoc_protection.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: unchanged-path output byte-identical to the original including URL and inline code (sha256 2fa482278af0ae99f4dc46ccfbb280928ff69905a773a3f242dfe6bb2861176c); C probe changed path preserved all material outside the accepted span", "negative_paths": "raw envelope byte identity (hash-equal, 78 codepoints) on the unchanged path; protected content untouched", "gap": ""},
    {"id": "LR-008", "class": "IMPLEMENTED", "runtime_path": "runtime_corpus.py + src/llm_slovenian_repair/unigram_importer.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: real truncated index (min counts 2270/272) -> strict abstention, missing data never treated as zero; loader semantics: unigram-missing -> UNAVAILABLE, ngram-missing -> CENSORED with unknown denominator (README + source)", "negative_paths": "no EXACT(0) without justified query completeness; truncated frequencies not complete statistics (C abstention)", "gap": ""},
    {"id": "LR-009", "class": "IMPLEMENTED", "runtime_path": "runtime_acceptance.py accept()", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: real truncated index -> change rejected (independent evidence not stronger); fixture index with supporting context -> accepted (accepted-independent-evidence); model self-reported confidence alone never authorizes (source)", "negative_paths": "a same-Qwen second call is not an accepted independent evidence source (no such path exists in the product)", "gap": ""},
    {"id": "LR-010", "class": "IMPLEMENTED", "runtime_path": "batch_review.py (one combined batch per response)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: exactly one review request per response (upstream total 2 = 1 main + 1 review); C probe: one call per candidate set", "negative_paths": "no automatic generative repair/retry loop: malformed batch is rejected whole with no re-request (source)", "gap": ""},
    {"id": "LR-011", "class": "IMPLEMENTED", "runtime_path": "proxy.py 502/fallback + request_lifecycle.py abort scope", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C5 epoch: fake reviewer crash -> engine sees protocol-valid results only; real boundary rejected honestly (REVIEW_UNKNOWN_ID) and the safely captured original was delivered; 030-a disconnect handling (owned upstream/review canceled, original delivered) at the byte/tree-equal PR32 reviewed head", "negative_paths": "main error/incompleteness never masked as successful repaired output (honest protocol error path in source)", "gap": ""},
    {"id": "LR-012", "class": "IMPLEMENTED", "runtime_path": "qwen_client.py (operator-configured endpoint/profile reuse of the existing Qwen)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: reviewer transport exercised against the synthetic endpoint with the real client shape; CPU infrastructure (detector/corpus/acceptance) loads no model", "negative_paths": "no second large GPU model, no vLLM/CUDA, no weight loading anywhere in the product tree", "gap": ""},
    {"id": "LR-013", "class": "IMPLEMENTED", "runtime_path": "proxy.py _stderr_usage_observer + opt-in trace writer (0600)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: usage observer emitted exactly one content-free line (calls=1, usage 10/20/30) separated from main usage 7/25/32; trace file mode 0600, opt-in via CONCEPT_TRACE_DIR", "negative_paths": "no user text, targets/replacements, prompts or secrets in operator channels (content-free counts only); sanitized child environment carried no credentials, so no Authorization on the wire", "gap": ""},
    {"id": "LR-014", "class": "PARTIAL", "runtime_path": "n/a (evidence-layer requirement)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Distinct evidence layers exist but are not all measured: software correctness has focused + probe evidence at 3bd6ffd (this audit); native-Qwen serving compatibility is UNPROVEN (no live target call in this offline order, R6 - a bounded unproven runtime fact, not a license to borrow coding-provider endpoints/credentials); linguistic benefit/harm and the ~99% / <=1-harm-per-10k goals remain unmeasured (owner-excluded, not deferred); deployment/release authority is not granted. No milestone claim is made."},
    {"id": "A-SCOPE-01", "class": "IMPLEMENTED", "runtime_path": "concept-verification/ as a whole (conservative repair of completed Slovenian responses)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3/C probe behavior: word/short-phrase repair only; abstention on weak evidence (C); no factual correction, translation or whole-answer rewriting in any exercised path", "negative_paths": "instruction rejects stylistic-only and factual changes and treats targets as data, not instructions; unknown/ambiguous material abstained (C)", "gap": ""},
    {"id": "A-SEAM-01", "class": "IMPLEMENTED", "runtime_path": "proxy.py (adapter: capture/delivery) vs RepairEngine core (library); qwen_client.py (injected reviewer)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe drove the core directly with an injected fake reviewer; B-v3 drove the adapter over real loopback HTTP; the reviewer performs one fresh outbound request per response", "negative_paths": "no conversation store or shared mutable history (stateless proxy; B-v3 history passthrough byte-identical); no recursion", "gap": ""},
    {"id": "A-STACK-01", "class": "PARTIAL", "runtime_path": "pyproject.toml + uv.lock (uv, Python 3.12.15), typed dataclass contracts, pytest suites", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Planned HTTPX baseline is replaced by standard-library http.client transports (no httpx import in the product); uv-locked Python 3.12, typed contracts, pytest and no import-time network are present. Documented deviation from the proposed baseline with no observed functional impact; a future order may re-pin the transport baseline."},
    {"id": "A-ROUTE-01", "class": "PARTIAL", "runtime_path": "qwen_client.py (operator-controlled private direct reviewer endpoint)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "In-product isolation is implemented and probed (B-v3: X-Probe-Marker not forwarded, no Authorization, fixed operator-configured destination, no public repair recursion). The 'existing gateway keeps public auth, route rights, quotas/accounting' half belongs to the adjacent system, outside the audited product revision: no change and no claim made here."},
    {"id": "A-SPAN-01", "class": "IMPLEMENTED", "runtime_path": "protected.py + pandoc_protection.py (data-pos wrapper spans) + composed_validation.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "D1 test_pandoc_protection.py 67 passed + 3 subtests at 3bd6ffd; C probe: slices rechecked immediately before apply; B-v3: exact-span surgery on the unchanged/changed paths", "negative_paths": "overlap/incompatible slices rejected, no silent last-wins; group rollback in composed_validation; repeated occurrences disambiguated by exact before/after context (source + D1 tests)", "gap": ""},
    {"id": "A-PROTECT-01", "class": "IMPLEMENTED", "runtime_path": "pandoc_protection.py (Pandoc-AST span location) + protected.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "A probes at 3bd6ffd (qualified Pandoc 3.7.0.2 exact-version + capability gate before bind; bad path/version fail closed); D1 67 passed; B-v3: URL and inline code intact inside the byte-identical output", "negative_paths": "protected intervals act as linguistic boundaries (no artificial adjacency across excluded material, source + D1 tests); fenced/indented code, URLs, emails, numbers protected (D1 test coverage)", "gap": ""},
    {"id": "A-CORPUS-01", "class": "IMPLEMENTED", "runtime_path": "runtime_corpus.py (per-record status, denominator tracking)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: truncated index -> abstention rather than fabricated completeness; loader preserves EXACT/CENSORED/UNAVAILABLE with source/version/completeness metadata (README + source)", "negative_paths": "retained n-gram sums never presented as the complete denominator; censored surface aggregation not a complete lemma distribution (source + tests)", "gap": ""},
    {"id": "A-CORPUS-02", "class": "PARTIAL", "runtime_path": "corpus.py + src/llm_slovenian_repair/unigram_importer.py (archive validation, manifest)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "The bounded-import mechanism is implemented (explicit archive paths, regular non-symlink files, exact size/MD5/SHA-256, preambles, header/marker hashes, CRLF/UTF-8/widths/row limits, manifest). The audited index is a private truncated release (min counts 2270/272 observed in the C probe); full-source qualification (release cutoff, Sloleks, collocations, rights/license) is not complete for it, and no bulk-access or current-access claim is made. Consequence: evidence strength is bounded, which the strict abstention behavior correctly reflects."},
    {"id": "A-DETECT-01", "class": "IMPLEMENTED", "runtime_path": "detector.py + runtime_detection.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: 1 candidate for the planted malformed form, 0 for clean text; bounded suspicious-place selection (maximum=4 at the engine call, policy max_targets 8); nearby alarms grouped into a bounded phrase BEFORE review (source)", "negative_paths": "unknown/rare/name is not automatically wrong (C abstention); no ranked corpus alternatives fed to the reviewer by default (source)", "gap": ""},
    {"id": "A-QUESTION-01", "class": "PARTIAL", "runtime_path": "batch_review.py line 88 (BATCH_INSTRUCTION)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "CONCRETE GAP (question wording): the exact agreed Slovenian question ('Ali se ti zdi uporaba besede oziroma besedne zveze X najboljša naravna izbira v tem slovenskem stavku? Če ne, s čim bi jo nadomestil?') does not appear anywhere in the product prompt - verified by literal search across concept-verification/ and src/ (it occurs only in PLAN.md, ARCHITECTURE.md and research/prompts/targeted-review.md). BATCH_INSTRUCTION conveys the same semantics in English (suitability question; keep/insufficient-context/wider-edit; data-not-instructions). First failing boundary: batch prompt construction, batch_review.py:88. Consequence: prompt-fidelity deviation from the agreed question; no observed behavioral break (semantics preserved; keep/wider/insufficient paths behave in the C probe). Smallest bounded remediation: use the exact agreed Slovenian question wording in the batch instruction (or pin it as a separate clause) plus a regression test asserting the wording; retest scope: batch prompt construction and the schema round-trip tests only."},
    {"id": "A-SCHEMA-01", "class": "IMPLEMENTED", "runtime_path": "batch_review.py (batch validation)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C5 at the real boundary: unknown ID -> whole-batch rejection (REVIEW_UNKNOWN_ID); keep=true => replacement null and needs_wider_edit=false, keep=false => nonempty replacement, needs_wider_edit=true => keep=true and replacement null (source invariants + C keep/wider paths); B-v3: review response schema round-trip with version batch-v1", "negative_paths": "invalid JSON/types, unknown/duplicate/missing IDs, contradictory fields or oversized output reject the WHOLE batch; no salvage and no JSON-repair request (source)", "gap": ""},
    {"id": "A-ACCEPT-01", "class": "PARTIAL", "runtime_path": "src/llm_slovenian_repair/contracts.py (RepairMode, shadow invariants) + policy.py (schema v1); proxy.py (strict instantiation)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "The runnable proxy instantiates only the strict behavior (validated AUTO_REPAIR; both accept and reject paths probed in C). detect_only is the library policy default and shadow is codified in the library contracts (shadow results require exactly one structured review call and cannot contain edits), with experimental repair hard-rejected in policy schema v1. Concrete gap: detect_only/shadow have no dedicated tests and no focused run in this order, and the proxy exposes no selectable mode switch, so the mode matrix is not runtime-verified end-to-end at 3bd6ffd."},
    {"id": "A-ACCEPT-02", "class": "IMPLEMENTED", "runtime_path": "runtime_acceptance.py accept()", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: reject path (independent evidence not stronger on the truncated real index) and accept path (fixture index with supporting context -> accepted-independent-evidence); all applicable conditions enforced (CPU-selected target, valid local proposal, exact slice/nonprotected bounds, independent evidence, no contradiction, valid composed result)", "negative_paths": "identity replacements rejected; neutral/incomparable data insufficient; forbidden newlines/control/markup/code structure rejected (source rules); LLM_CONFIRMED_REPAIR without independent evidence cannot auto-change (policy allow_evidence_insufficient_acceptance=False)", "gap": ""},
    {"id": "A-PATCH-01", "class": "IMPLEMENTED", "runtime_path": "repair.py apply_edits + composed_validation.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: unchanged path returned the byte-identical raw upstream envelope (sha256 bb8aad1b17ed924af3e2e0ecf74ac5a96f969f70ece2478759a19f8b04aea916, hash-equal and length-equal); C probe changed path composed from untouched original slices plus the exact replacement; slices rechecked immediately before apply (source)", "negative_paths": "composing conflict -> group rollback and rebuild from original (composed_validation); no model answer/detokenization/Markdown renderer substitutes for the document (source)", "gap": ""},
    {"id": "A-API-01", "class": "IMPLEMENTED", "runtime_path": "proxy.py forward() + capture_transport.py (bounded SSE capture, ownership prefetch)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: the verified nonstreaming text shape end-to-end over real loopback; upstream completion verified per protocol (CL-exact/chunked/SSE response.completed) before any analysis; internal streaming bounded-captured with completion validated before analysis (source, order 015-a ownership prefetch)", "negative_paths": "unsupported requests rejected before the main call with closed labels (404 wrong path probed in B-v3 with zero outbound; store:true/background:true -> closed 400 labels in source)", "gap": ""},
    {"id": "A-HISTORY-01", "class": "IMPLEMENTED", "runtime_path": "proxy.py (stateless passthrough) + responses_contract.py aligned_metadata_clean", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: client-managed input history forwarded unmodified (byte-identical unchanged envelope); delivered history content is the final answer only; main and review usage reported separately (7/25/32 vs 10/20/30)", "negative_paths": "changed text with stale annotations/logprobs is rejected (aligned_metadata_clean requires absent or empty aligned lists); external server-managed chaining unsupported (no previous_response_id linkage anywhere)", "gap": ""},
    {"id": "A-LIMIT-01", "class": "PARTIAL", "runtime_path": "config.py (validated phase budgets) + request_admission.py (1+16 queue, 2 s wait, 503)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "CONCRETE GAP (overall deadline): every phase budget is finite and validated before bind (intake/header/setup/delivery defaults 30 s, reviewer exchange 15 s, queue 2 s, <=1 review, 1 pass, 0 retries, <=8 targets, review max_output_tokens 1536 - B-v3 probed), but no single enforced OVERALL request deadline exists: config.py (lines 77, 84, 94, 107, 123, 129) states 'overall request deadlines remain unimplemented' and the README capture section agrees. First failing boundary: absent (by design, documented) - the total wall clock is only bounded by the sum of the sequential phase budgets. Smallest bounded remediation: one monotonic total deadline checked at phase boundaries, value selected by order."},
    {"id": "A-FAIL-01", "class": "IMPLEMENTED", "runtime_path": "proxy.py + request_lifecycle.py + request_admission.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: no eligible suspicion -> original/zero calls; unknown proposal ID -> honest rejection with the captured original delivered; queue rejection packets are content-free fixed 503s (request_admission); 030-a disconnect -> owned upstream/review canceled, no orphan work (CI at the byte/tree-equal PR32 reviewed head)", "negative_paths": "transport/invalid batch -> cancel owned optional work, return completed original (source); main failure/incomplete -> honest protocol error, never a truncated success (source); missing/corrupt corpus -> degraded original, no invented counts (C)", "gap": ""},
    {"id": "A-SECURITY-01", "class": "IMPLEMENTED", "runtime_path": "qwen_client.py (external credentials, opt-in profile file) + trace writer (0600)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: sanitized child environment (explicit allowlist, no QWEN_API_KEY/CONCEPT_REVIEWER_PROFILE) -> no Authorization header on any outbound request (probed); targets treated as data, no URL/tool execution in the reviewer path; trace files 0600 and opt-in", "negative_paths": "no production credentials or customer data in the product tree; embedded instructions in targets are not executed (data-only reviewer contract)", "gap": ""},
    {"id": "A-TEST-01", "class": "PARTIAL", "runtime_path": "concept-verification/tests (19 test modules) + src library (no dedicated test modules in-repo)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Synthetic deterministic coverage exists across the named areas (source-verified) and the focused re-runs at 3bd6ffd pass (D1 test_pandoc_protection.py 67 passed + 3 subtests, 7.47 s, rc 0; D2 test_concept.py 19 passed, 5.07 s, rc 0 - prior epoch of this order, clean tracked state). Concrete gap for this audit: the full 19-suite regression was NOT rerun at 3bd6ffd (R5-bounded; no broad-suite repeat), and the live-Qwen qualification row is NOT RUN (opt-in; offline order, R6). Corroboration only: the full suite (931 passed) at the M30-era tree and the four required checks green at PR32 reviewed head 8fc14c3, whose tree the order verifies equals the merged tree - an equivalence statement, not a new execution at 3bd6ffd."},
    {"id": "A-EVAL-01", "class": "PARTIAL", "runtime_path": "concept-verification/eval/ (run_eval.py, perturb.py, config.json)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Owner-excluded, non-blocking: no separate human evaluation dataset will be created or requested (excluded by the owner, not deferred); no human labels exist in the repo; precision/harm/coverage are unmeasured and the ~99% / <=1-harm-per-10k figures are goals, not results. The evaluation mechanism (phases, freeze, config) exists and usage is separated (B-v3), but the linguistic-quality layer is unmeasured. No fabricated quality or general experimental-MVP acceptance is claimed."},
    {"id": "A-GOV-01", "class": "IMPLEMENTED", "runtime_path": "oap/ governance (frozen registry, distillation map, manifests)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "frozen oap/audit/requirements.json byte-identical to the 3bd6ffd blob (verified by the check_ica ICA_MATRIX_SOURCE_DRIFT gate in the R9 run); one current full ARCHITECTURE; no private PLAN/ARCH/CRITICAL mirrors", "negative_paths": "historical seeds and inert 031 phrase-grouping seed preserved unexecuted; registry/incidents unchanged by this audit", "gap": ""},
    {"id": "A-CLOSE-01", "class": "IMPLEMENTED", "runtime_path": "oap/audit/ICA-PROTOCOL.md + oap/bin/check_ica.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "this document is a fresh architecture-to-current-main ICA with real paths/tests/SHA at the accepted merged main; the check_ica helper validates the fence and the 59-row matrix (R9 run, recorded in the evidence JSON)", "negative_paths": "reports are claims: this audit certifies no milestone, no product completeness and no human release; parser success is not independence or semantic acceptance", "gap": ""},
    {"id": "MVP-1", "class": "IMPLEMENTED", "runtime_path": "proxy.py forward()/capture path", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: the entire main answer was captured before the repair call and before any user-visible delivery (200 completed only after capture; 0.162 s end-to-end)", "negative_paths": "no provisional original text to the user while repair is pending (single final delivery path)", "gap": ""},
    {"id": "MVP-2", "class": "IMPLEMENTED", "runtime_path": "runtime_detection.py -> review gate", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: no eligible suspicion -> zero additional Qwen (reviewer) calls; B-v3: exactly one review call for the eligible candidate", "negative_paths": "zero-call path proven at the real engine boundary", "gap": ""},
    {"id": "MVP-3", "class": "IMPLEMENTED", "runtime_path": "batch_review.py + runtime_acceptance.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: the reviewer may propose only a replacement of its assigned span or keep; unknown ID rejected (C5)", "negative_paths": "no whole-answer regeneration; per-ID schema enforced", "gap": ""},
    {"id": "MVP-4", "class": "IMPLEMENTED", "runtime_path": "proxy.py (stateless) + qwen_client.py (fresh request)", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: the main conversation history contains no repair conversation or internal results (byte-identical passthrough; no linkage keys probed absent)", "negative_paths": "no previous_response_id/conversation/tools in the review request (empty set probed)", "gap": ""},
    {"id": "MVP-5", "class": "IMPLEMENTED", "runtime_path": "repair.py + composed_validation.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: no change outside programmatically validated spans (byte-identical unchanged path including protected material); C probe: changed path alters only the validated span", "negative_paths": "protected spans and all other bytes untouched (hash evidence)", "gap": ""},
    {"id": "MVP-6", "class": "IMPLEMENTED", "runtime_path": "request_lifecycle.py (030) + batch failure handling", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C5: invalid optional process (crashed fake reviewer, unknown ID) did not damage the already completed answer - original delivered honestly; 030-a cancellation preserves the captured original (CI at the tree-equal reviewed head)", "negative_paths": "cancellation/invalid batch -> no partial mutation, no orphan work", "gap": ""},
    {"id": "MVP-7", "class": "IMPLEMENTED", "runtime_path": "runtime_corpus.py + runtime_acceptance.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: published truncated frequencies (min counts 2270/272) were not treated as complete statistics - strict abstention instead of a change", "negative_paths": "missing truncated data is not zero; unknown denominator stays unknown", "gap": ""},
    {"id": "MVP-8", "class": "PARTIAL", "runtime_path": "proxy.py usage observer + trace timings + eval review sheets", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "The transparent-reporting MECHANISM exists and is probed (B-v3: separated content-free main vs review usage, trace timings, opt-in 0600 traces), but the benefit/harm CONTENT is unmeasured (owner-excluded; no human dataset, no measured precision/harm/latency benefit). Non-blocking functional rationale: reporting scaffolding without measured quality is not a functional defect of the proxy path."},
    {"id": "D01", "class": "IMPLEMENTED", "runtime_path": "src/llm_slovenian_repair/contracts.py + policy.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "typed span/evidence/proposal/decision/result structures with keep/replace separated (schema invariants: keep => replacement null; wider => keep + null); policy schema v1 bounds enforced by validators (maxima 1/1/0/1/8/6/8, finite character/byte bounds)", "negative_paths": "experimental mode and enable_experimental_repair rejected in policy v1; schema_version != 1 rejected", "gap": ""},
    {"id": "D02", "class": "IMPLEMENTED", "runtime_path": "corpus.py + src/llm_slovenian_repair/unigram_importer.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "bounded data import with reproducible manifest and correct missing-data semantics (EXACT/CENSORED/UNAVAILABLE) - exercised against the real private index in the C probe; archive verification (size/MD5/SHA-256, preambles, CRLF/UTF-8/widths/row limits) in source", "negative_paths": "invalid archive rejected before insert (loader checks); no runtime scraping; archives/index never staged", "gap": ""},
    {"id": "D03", "class": "IMPLEMENTED", "runtime_path": "protected.py + pandoc_protection.py + detector.py tokenize()", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "D1 67 passed + 3 subtests at 3bd6ffd (code/URL/Unicode protection and mapping tests); B-v3: protected spans intact in byte-identical output; tokenization never alters the original (source)", "negative_paths": "repeated substrings/Unicode/CRLF/Markdown boundary cases covered by D1 test module; unsafe partial-grapheme targets abstain (source)", "gap": ""},
    {"id": "D04", "class": "IMPLEMENTED", "runtime_path": "detector.py + runtime_detection.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: selects plausible suspicious places (1 for the planted form, 0 for clean text) with bounded output; does not send everything to the model (zero-call path proven)", "negative_paths": "clean text -> zero candidates -> zero review calls", "gap": ""},
    {"id": "D05", "class": "PARTIAL", "runtime_path": "qwen_client.py ResponsesReviewer + injected reviewer seam", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Fake/injected clients are fully proven (C and B-v3 return validated local decisions through the real validation/acceptance path) and the real client's transport shape is verified against the synthetic endpoint (B-v3: exact request shape, 15 s bounded exchange). Concrete gap: actual live-Qwen behavior (model identifier, supported shape, cancellation, usage) is UNPROVEN at 3bd6ffd - no live target call in this offline order (R6), and missing target configuration is a bounded unproven runtime fact, not a license to borrow coding-provider endpoints/credentials."},
    {"id": "D06", "class": "IMPLEMENTED", "runtime_path": "runtime_acceptance.py + repair.py + composed_validation.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: code accepted (independent evidence) or rejected (insufficient evidence) proposals and preserved all other slices exactly (changed-path output differs only inside the validated span)", "negative_paths": "overlap/stale/nearby conflicts -> group rollback; identity replacement rejected", "gap": ""},
    {"id": "D07", "class": "PARTIAL", "runtime_path": "proxy.py main() (runnable CLI entry, A probes) + opt-in 0600 traces (request_id, candidates, reviewer_decisions, acceptance, timings) + eval review sheets", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "CONCRETE GAP (inspection surface): the proxy is runnable via the real CLI entry (A probes: pandoc gate before bind, exact exit codes) and inspection exists via opt-in 0600 trace files (B-v3 probed file/mode/keys) plus eval review sheets, but there is no standalone cli.py operator command showing original/proposals/final text/reasons as a first-class inspection surface (src/ has no CLI module), and the persisted trace omits the review_batch call/usage (in-memory plus the content-free stderr observer only). Consequence: operator inspection is less direct than the D07 wording; no functional break of the repair path."},
    {"id": "M01", "class": "ABSENT", "runtime_path": "n/a", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Owner-excluded, non-blocking: the initial labelled set (real target responses, correct/rare/technical negative controls, separate threshold-calibration split) does not exist and will NOT be created or requested - excluded by the owner, not deferred. This audit creates no future human-dataset obligation."},
    {"id": "M02", "class": "PARTIAL", "runtime_path": "detector.py (unigram/lexicon, bigram/trigram, fixed-neighbor alternatives)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Detection signals are implemented and probed (C), but no verified CPU lemma/morphology analysis separating wrong lexeme choice from wrong inflection exists in the product (no morphology/lemma module; only policy-level mentions in config.py). Consequence: morphological disagreement is not independently evidenced; acceptance leans on the form/lexicon/n-gram evidence that does exist, with strict abstention when it is insufficient (C)."},
    {"id": "M03", "class": "IMPLEMENTED", "runtime_path": "runtime_detection.py (bounded phrase grouping) + batch_review.py needs_wider_edit", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "C probe: wider-edit proposal -> target left unchanged (clear edit width honored); B-v3: batch schema round-trip with the needs_wider_edit field; nearby alarms grouped into a bounded phrase before review (source)", "negative_paths": "grouping never crosses protected material; excess/ambiguous targets remain unchanged with finite reason labels (source)", "gap": ""},
    {"id": "M04", "class": "ABSENT", "runtime_path": "n/a (calibration measurement)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Owner-excluded/unmeasured, non-blocking: acceptance calibration with rule versions and measured precision/harm/coverage per error class does not exist (no labelled data). The strict acceptance RULES themselves are implemented (runtime_acceptance.py, probed in C), but they are not calibrated against measured quality."},
    {"id": "M05", "class": "IMPLEMENTED", "runtime_path": "request_admission.py + request_lifecycle.py + config.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "queue 1+16 with 2 s wait and content-free 503 (request_admission source); cancellation of owned work (030, CI at the tree-equal reviewed head); finite phase budgets validated before bind; safe fallback to the completed original (C5/B-v3)", "negative_paths": "queue full/timeout -> 503 without starting work; disconnect -> no orphan upstream/review; limits do not starve main requests (per-phase independence in source)", "gap": ""},
    {"id": "M06", "class": "IMPLEMENTED", "runtime_path": "proxy.py nonstreaming path + responses_contract.py", "tested_sha": "3bd6ffdd96bda95bd4c6de447b56cce76fe5a058", "evidence": "B-v3: one clearly supported text shape end-to-end; context (history) preserved unmodified; no recursion (reviewer destination operator-fixed)", "negative_paths": "store:true/background:true and unknown fields rejected with closed labels before any upstream/reviewer call", "gap": ""},
    {"id": "M07", "class": "ABSENT", "runtime_path": "n/a (comparative report)", "tested_sha": "", "evidence": "", "negative_paths": "", "gap": "Owner-excluded/unmeasured, non-blocking: the comparative report (agreed method vs original and basic comparison methods) is not produced - no measured comparison exists. The eval mechanism (concept-verification/eval/) can host it when (and only when) the owner later approves evaluation data; this audit neither requests nor implies it."}
  ]
}
```

## Concrete functional gaps first (R8)

Current functional gaps of the audited product at 3bd6ffd, in decreasing
concreteness. Each names the minimal evidence, the first failing boundary, the
consequence and the smallest bounded remediation/retest scope. None is
implemented in this audit-only order.

1. **A-QUESTION-01 — question wording (PARTIAL).** The exact agreed Slovenian
   question wording does not appear in the product prompt; `BATCH_INSTRUCTION`
   (`concept-verification/batch_review.py:88`) conveys the same review
   semantics in English. Literal search: the agreed question occurs only in
   PLAN.md, ARCHITECTURE.md and research/prompts/targeted-review.md, never in
   concept-verification/ or src/. First failing boundary: batch prompt
   construction. Consequence: prompt-fidelity deviation from the agreed
   question (register/language of the review prompt differs from the agreement)
   without an observed behavioral break. Smallest remediation: embed the exact
   agreed Slovenian question in the batch instruction (or pin it as a separate
   clause) plus a regression test asserting the wording; retest scope: batch
   prompt construction and schema round-trip tests only.
2. **A-LIMIT-01 — overall request deadline (PARTIAL).** Every phase budget is
   finite and startup-validated, but no single enforced total request deadline
   exists; `config.py` (lines 77, 84, 94, 107, 123, 129) and the README
   capture section state this explicitly. First failing boundary: absent by
   documented design. Consequence: total wall clock bounded only by the sum of
   the sequential phase budgets. Smallest remediation: one monotonic total
   deadline checked at phase boundaries (value to be selected by order).
3. **D07 — inspection surface (PARTIAL).** No standalone `cli.py` operator
   command showing original/proposals/final text/reasons; inspection is via
   opt-in 0600 trace files and eval review sheets. Related minor: the
   persisted trace omits the `review_batch` call/usage (in-memory plus the
   content-free stderr observer only; trace keys at 3bd6ffd: acceptance,
   candidates, corpus_summaries, message_index, original,
   protected_difference_count, protocol, repaired, replacements, request_id,
   reviewer_decisions, timings). Smallest remediation: a small CLI entry that
   renders the existing trace/review-sheet records, and persisting the
   review-batch call/usage record in the trace; retest scope: trace writer and
   the new CLI smoke test.
4. **A-STACK-01 — transport baseline (PARTIAL).** The planned HTTPX baseline is
   replaced by standard-library `http.client` transports (no httpx import in
   the product). Functional behavior is bounded and verified (B-v3); this is a
   documented deviation, not a break.
5. **A-CORPUS-02 — corpus qualification (PARTIAL).** The audited private index
   is a truncated release (min counts 2270/272 observed in the C probe);
   full-source qualification (release cutoff, Sloleks, collocations,
   rights/license) is not complete. Consequence: evidence strength is bounded,
   correctly reflected by strict abstention (C probe).
6. **A-ACCEPT-01 — mode matrix (PARTIAL).** The proxy instantiates strict only;
   detect_only/shadow exist as library contracts/policy with no dedicated
   tests or focused run, and no selectable mode in the proxy.
7. **D05 — live-Qwen layer (PARTIAL/UNPROVEN).** The real reviewer client is
   implemented and its transport shape verified against the synthetic endpoint,
   but actual live-Qwen behavior is UNPROVEN at 3bd6ffd (offline order, R6).
8. **M02 — morphology (PARTIAL).** No verified CPU lemma/morphology analysis
   separating wrong lexeme from wrong inflection (form/lexicon/n-gram signals
   only).
9. **A-QUESTION-01-adjacent labeling nuance (minor, non-matrix).**
   `resolve_pandoc_spec` does not existence-check a configured path; a
   configured-but-missing path surfaces as `PANDOC_NOT_EXECUTABLE` (from
   `check_pandoc`'s isfile/executable check) rather than `PANDOC_NOT_FOUND`.
   The startup gate still fails closed before bind in all A-probe cases; this
   is a reason-label nuance, not a gate gap.
10. **Native-Qwen compatibility and linguistic quality: UNPROVEN/unmeasured.**
    Bounded unproven runtime facts of this offline audit, not product defects:
    no target call was made, none is licensed, and quality remains
    owner-excluded.

### Concrete governance/CI conflict found by this audit (not a product functional gap)

**Whitespace fixed-contract conflict on the immutable 031-a order.** Both
accepted whitespace bases (`2832fa1e51bdf3641aabbd81feab8ddb64a876da` and
`82ea1e6f4173934fa47bb34ee6a6f78338d3603a`) now fail at the implementation
head with `DIAGNOSTIC_SET_MISMATCH`: the immutable 031-a order file
(SHA-256 `b4e4a2a485304893d228eb35d59e91cc229ddcea95a8160e536262e759004d10`,
pinned by the order itself and by the requirements-first artifact) ends with a
trailing blank line (diagnostic `oap/orders/031-a-functional-proxy-audit.md:161:
new blank line at EOF.`), which adds a FIFTH whitespace diagnostic on top of
the four pinned historical incidents whose fixed contract order 027-b closed
("a changed, missing, re-added, or additional whitespace incident fails rather
than becoming a new allowlist entry"). Verified: every other file added or
changed by this round is whitespace-clean (`git diff --check` over
3bd6ffd..head for the audit artifacts is empty); the only new diagnostic is
the order file's. The 030-a order (for contrast) ends without the blank line.
Coding cannot remediate this within the order: the order bytes are immutable
(R2) and the helper/registry may not be mutated (R9). The historical precedent
for a root-issued order whitespace defect (incident 4, 027-a order) was a
root-adjudicated dedicated forward recovery. Consequence: the two final-head
CI whitespace steps (Application baseline; OAP bootstrap acceptance) will fail
on any final report head of this branch until Root adjudicates the new
incident; this does not block the audit itself, its publication path, or the
round's unpublished preflight, and it is surfaced here for Root's exact-byte
review and the final-head CI gate.

### Owner-excluded and later-stage rows (distinct from the gaps above)

- **Owner-excluded, not deferred, non-blocking functional:** M01 (labelled
  set), M04 (acceptance calibration), M07 (comparative report), A-EVAL-01
  (evaluated quality layer), the benefit/harm content of MVP-8. These rows are
  ABSENT/UNMEASURED by owner decision (NO separate human evaluation dataset);
  this audit revives none of them as a functional gate and creates no future
  human-dataset obligation.
- **Later-service stage (SERVICE), outside the 59-row MVP matrix:** S01
  (broader negative tests + statistically meaningful harm report), S02
  (broader data support, rights ordered), S03 (production connection: explicit
  gateway path, separate repair usage, bounded load), S04 (deployment and
  rollback), S05 (final documentation). All are later-stage applicability, not
  current functional gaps of the proxy.
- **Adjacent system, no claim:** the public-auth/route-rights/quotas side of
  A-ROUTE-01 belongs to the existing gateway, outside the audited product
  revision.

## Full-source extras (13 derived requirements outside the frozen 59-row matrix)

Derived from full PLAN/ARCH before claims/code inspection (requirements-first
artifact); assessed here for completeness. Coverage/provenance stays separate
from the matrix by design.

- CAP-2 (protocol completion verification, not socket closure): IMPLEMENTED —
  completion checks for CL-exact/chunked/SSE `response.completed` in
  capture_transport.py; exercised indirectly by the B-v3 completed envelope;
  covered by D1/D2 focused runs.
- CAP-3 (one explicitly supported nonstreaming shape; unsupported capabilities
  rejected before the main call): IMPLEMENTED — B-v3 end-to-end; closed-label
  pre-main rejection (404 wrong path probed with zero outbound; store/background
  true rejected in source).
- CAP-4 (hard capture limit is a bounded API failure, never labelled
  complete): PARTIAL — the bounded-failure path exists in source (config
  max_safe_capture_* + capture error handling) but no direct limit-exceeded
  probe was run in this order.
- DET-3 (bounded target selection, at most 8 places, checkable rules):
  IMPLEMENTED — source + policy bounds (max_targets 8; engine maximum=4); C
  probe bounded output.
- TGT-2 (repeated occurrences marked unambiguously): IMPLEMENTED — serializer
  uses exact before/after context (source + D1/D2 coverage).
- ISO-2 (client-managed main history = prior history + final delivered answer
  only): IMPLEMENTED — B-v3 byte-identical passthrough.
- ISO-3 (reviewer on operator-controlled private route; no caller destination,
  no public bypass header): IMPLEMENTED — B-v3 probed (X-Probe-Marker not
  forwarded; operator-fixed URLs).
- ISO-4 (same-Qwen second call is not independent evidence): IMPLEMENTED — no
  such path exists; strict evidence rules in runtime_acceptance.py (C probe).
- REV-2 (whole-batch rejection on invalid JSON/types/unknown/duplicate/missing
  IDs/contradictions/oversize; never salvage): IMPLEMENTED — C5 real-boundary
  rejection (REVIEW_UNKNOWN_ID).
- SPAN-4 (text equality vs HTTP byte equality; unchanged envelope bytes
  preserved): IMPLEMENTED — B-v3 raw envelope hash-equal to the original
  upstream bytes.
- ACC-4 (LLM_CONFIRMED_REPAIR disabled for automatic changes): IMPLEMENTED —
  policy `allow_evidence_insufficient_acceptance=False`; strict acceptance
  requires independent evidence (C probe).
- LIM-4 (main/review strictly sequential per answer; bounded queue; no
  starvation): IMPLEMENTED — per-request sequential path (B-v3: one main then
  one review); admission controller 1+16/2 s.
- TEST-2 (before any real-Qwen connection: qualify model identifier, API shape,
  rules, cancellation, usage): NOT RUN / UNPROVEN — offline order (R6); the
  live opt-in mechanism exists, qualification was not performed, and no
  historical live fact is inferred.

## Evidence and probe provenance (all at tested SHA 3bd6ffd unless stated)

Private evidence lives under the private scratch root (logical:
STRATEGIC_HOME-relative test scratch 031a); public prose uses logical names
only. Raw probe logs are private 0600 and are never echoed here.

- **Requirements-first artifact (immutable):** SHA-256
  `fbcda5cf77d65914f87892e2de797589c549383b71bb3c1e0db6eb8afea9322d`, 53339
  bytes, saved 2026-11-10T15:13:42Z (derived_at 15:13:27Z), before any
  claims/code inspection. 81 derived requirements + 7 owner-scope + 13
  full-source extras; all 59 frozen MVP IDs mapped.
- **A probes (Pandoc startup gate, CLI/main entry):** qualified Pandoc 3.7.0.2
  (SHA-256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229)
  passes the exact-version + capability probe; configured-but-missing path ->
  PANDOC_NOT_EXECUTABLE; fake 3.6.0 -> PANDOC_WRONG_VERSION; full `proxy.py`
  main() with bad pandoc -> exit 1, "pandoc startup failure", fixed port 18024
  never bound (gate before bind proven); empty PATH -> PANDOC_NOT_FOUND.
- **C probes (engine level, injected fake reviewer, real + fixture index):**
  clean text + real truncated index -> 0 candidates, 0 review calls,
  byte-identical original; planted malformed form + real index -> exactly 1
  review call, rejected (independent evidence not stronger), byte-identical
  original (strict abstention; min counts 2270/272); planted + fixture index
  with supporting context -> accepted (accepted-independent-evidence) with the
  exact replacement inserted; keep/wider-edit proposals -> unchanged; unknown
  proposal ID -> whole batch rejected at the real boundary (REVIEW_UNKNOWN_ID).
  (First C5 fake crashed the engine process - a probe artifact: the engine only
  sees protocol-valid BatchResults; the real boundary was tested directly.)
- **B probe epochs (full loopback HTTP e2e):**
  - *Failed harness epoch (RC124):* the initial B harness (private script
    SHA-256 4ab8700fed782a18540b89321f93b79f6185736eb933360e681876ecf26d6e2c,
    preserved verbatim by Root under observed-probes/) used fixed loopback
    ports 18091/18024, inherited the full parent environment (including raw
    header/body echoing), and performed an unbounded `stderr.read()` ordering
    against a still-live child pipe; it timed out externally (RC124). **RC124
    is recorded as a FAILED HARNESS epoch, not a product failure.** The
    harness never recorded its Popen child PIDs, so the timed-out children's
    origin is unprovable and was not touched; at the corrected run no residual
    probe children or listeners on the old fixed ports were observable
    (proc/net/tcp + /proc cmdline scans, content-free).
  - *v2 attempt (harness crash):* first corrected-harness attempt crashed in
    its own report writer (TypeError after both children were already
    SIGTERM-terminated, reaped and pipe-drained; no orphans - verified).
    Partial v2 artifacts retained unmodified.
  - *Canonical corrected run (v3, PASS, rc 0, 1.6 s wall):* OS-assigned port 0
    for both owned children (actual bound ports 45627/45777 from the children's
    own READY lines); minimal sanitized child environment (explicit allowlist;
    no QWEN_API_KEY/CONCEPT_REVIEWER_PROFILE/provider credentials by
    construction; OAP_ROLE=coding; private TMPDIR/PYTHONPYCACHEPREFIX);
    bounded IO on every path (select-bounded READY reads with 10 s deadlines;
    15 s client timeout; EOF-drain only after terminate+reap); real product
    boundary via the actual `ConceptProxy` constructor (same class `main()`
    instantiates; real `_Handler`/`RepairEngine`/`ResponsesReviewer`/
    `check_pandoc`) bound to port 0 because `main()` hardcodes
    127.0.0.1:18024 - entry-point honesty: constructor-driven, while the
    CLI/main() startup proofs remain the distinct A epoch. Results (all
    content-free): 404 wrong-path negative with zero outbound; named boundary
    200 completed in 0.162 s; raw envelope byte-identical to the synthetic
    original (sha256 bb8aad1b17ed924af3e2e0ecf74ac5a96f969f70ece2478759a19f8b04aea916);
    output text equals original (sha256 2fa482278af0ae99f4dc46ccfbb280928ff69905a773a3f242dfe6bb2861176c,
    78 codepoints, URL + inline code intact); exactly 1 main + 1 review
    outbound; no Authorization anywhere; X-Probe-Marker not forwarded; review
    shape fresh and strict (store:false, stream:false, max_output_tokens 1536,
    input array, no linkage keys, model=probe-model); usage observer one
    content-free line (calls=1, 10/20/30) separated from main usage (7/25/32);
    trace file 0600 with acceptance/candidates (1 candidate, 0 replacements);
    owned children SIGTERM-terminated, reaped and pipe-closed (proxy exit 0
    with CLEAN_SHUTDOWN through the owning admission close boundary; upstream
    exit -15), parent 1 thread / 4 open FDs at report time.
  - Corrected harness SHAs (private): probe_b_v2.py
    c9f56c9bc4c062a8170865673509a3b10c3ad04b7ee96f68606c33610f6c6906,
    fake_upstream_v2.py f86aca68df7903e690890fa024798e2dc6f08a5fb625f426600057b740852c00,
    proxy_runner_v2.py e442d371bc472050e0011bd9503e3bb98e4871d50a7b24e9474145c60d6afb8c;
    v3 report e6f5a14923dc71817b42d521f00755416a978315b4ee743b1be3d765d112dec0.
- **Focused test re-runs at 3bd6ffd (prior epoch of this order, clean tracked
  state, qualified Python 3.12.15 -B, private caches, CONCEPT_PANDOC=qualified
  where needed):** D1 `pytest concept-verification/tests/test_pandoc_protection.py`
  -> 67 passed + 3 subtests in 7.47 s, rc 0; D2 `pytest
  concept-verification/tests/test_concept.py` -> 19 passed in 5.07 s, rc 0.
- **Prior-run equivalence (claims index only, NOT relabeled as executions at
  3bd6ffd):** the full 19-suite (931 passed) ran at the M30-era tree; the four
  required checks were green at PR32 reviewed head
  8fc14c3258aa8712ecd53be81abe3e62c798d04b, whose tree the order's verified
  prior_review states equals the exact merged tree of 3bd6ffd. This is
  source-byte/tree equivalence corroboration of the current main, not a new
  literal execution.

## Governance, state and shared checks (R9)

- check_ica runs against the exact evaluated merged-main SHA (recorded in the
  evidence JSON with command/rc); no helper/registry mutation.
- Shared accepted-runtime governance, transcript (at the implementation head),
  report history (require-manifest, at HEAD and at the implementation head),
  all 173 manifest identities and research counter consistency: PASSED (exact
  results in the evidence JSON). Both accepted whitespace bases: FAILED at the
  implementation head with `DIAGNOSTIC_SET_MISMATCH`, root-caused exclusively
  to the immutable 031-a order's trailing blank line (see the governance/CI
  conflict subsection above); all round-added files are whitespace-clean.
- **Designed counter mismatch (reported honestly before publication):**
  `research/RESEARCH-STATE.md` machine block advances
  `oap_reports_reviewed` 85 -> 86 in THIS round's non-report commit (the
  030-a pattern: a report-only commit stages only the report path, so the
  counter bump belongs to the non-report commit). The counter therefore points
  at this round's report one commit before the report's own report-only
  publication commit; the report-only commit touches no counter. Registry
  42 and frozen incidents 2 remain unchanged; the 173 manifest keys/
  identities remain unchanged.
- The final-head four CI successes (Application baseline, Research
  reproducibility, OAP bootstrap acceptance, OAP report history) on the final
  report head remain Root's later development-merge gate; nothing here claims
  them.
- No README/STATUS readiness assertion is made in this audit; README/STATUS
  were read post-derivation as claims indexes only.

## Authority, gates and non-claims

- D0 read-only internal audit within the owner functional scope; Decision
  NONE; no additional human gate, no D1 admission.
- `deployment_authorized: false`, `human_milestone_accepted: false`. This
  report is a claims document: parser validity is not independence,
  completeness or semantic acceptance; no milestone, release or deployment
  authority is granted or claimed; no merge or automerge is performed by
  coding.
- Independence is declared, not statistical: same model family, fresh /new
  context on the same adopted foreground process; mitigated by the
  source-first derivation before claims, full-source extras, actual
  positive/negative runtime evidence at the evaluated SHA, and Root's later
  semantic review of the exact final diff.

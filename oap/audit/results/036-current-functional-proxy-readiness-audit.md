# Independent Closure Audit 036-a — Current functional proxy readiness

Status: FINAL. Fresh source-first audit of the exact accepted merged runnable
Slovenian-repair proxy at objective 036, round 036-a. Audit only; no product
changes. Functional operating-path readiness is assessed and is deliberately
kept distinct from linguistic quality, formal milestone acceptance and
deployment authority. deployment_authorized=false; human_milestone_accepted=false.

```oap-ica
{
  "status": "FINAL",
  "milestone": "MVP",
  "main_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
  "tree": "7b2418dea1de25734cc12e633344e320e533eb7e",
  "architecture_sha256": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
  "plan_sha256": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
  "auditor": "036-a fresh isolated coding-chat ICA, OAP_ROLE=coding, no second CLI/subagent/background model",
  "context_provenance": "fresh chat 01a1ce37-3bea-7fd3-ba75-bfe8625370c2 in owner-launched foreground CLI pid 3341327 (codex --yolo --profile early-beta, tmux), same home/auth/cwd; source-first: owner scope + complete PLAN/ARCHITECTURE read and frozen (23192B sha 1fa67b855bdbed14cd1b1905d59b02e59079bb3b6fe999048817b6a8af2fb989) before runtime/registry/README/reports/deferred-index",
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
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "proxy.py _Handler.do_POST - ConceptProxy.forward - capture_transport.read_bounded_body (completion validated; SSE requires response.completed event)",
      "evidence": "fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero; full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source trace of bounded capture with hard byte cap",
      "negative_paths": "incomplete SSE (no completed event) to CaptureError; truncated body to 400 REQUEST_BODY_INCOMPLETE; hard capture cap to bounded API failure"
    },
    {
      "id": "LR-002",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "RepairEngine.repair - runtime_detection.detect(text, corpus, intervals, mode, maximum=4); no candidates or no prepared targets means zero review calls and unchanged text",
      "evidence": "fresh 22 at main: test_high_identity_alternative_zero_calls, test_safe_known_zero_calls; full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "high-identity alternative to zero review calls; safe known-word to zero calls; weak/absent evidence to no candidate"
    },
    {
      "id": "LR-003",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "runtime_detection.detect returns Candidate(start,end,text) in original codepoint coords; batch_review.prepare_targets assigns preassigned span ids; build_prompt targets those ids (model answers per assigned id only)",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: BatchProposal carries only keep/replacement/needs_wider_edit (no positions)",
      "negative_paths": "stale-candidate-bounds reject in runtime_acceptance.accept; model cannot invent or omit ids (batch_review.parse_batch_envelope rejects unknown/duplicate/missing ids)"
    },
    {
      "id": "LR-004",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "batch_review.build_prompt (BATCH_INSTRUCTION batch-v1) preserves the agreed Slovenian suitability question meaning per assigned target; parse_batch_envelope + _validate_proposal_item enforce keep and needs_wider_edit semantics",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: BATCH_INSTRUCTION question text + _validate_proposal_item keep/needs_wider_edit constraints",
      "negative_paths": "keep-with-replacement rejected; wider-edit-with-replacement rejected; contradictory fields reject the batch"
    },
    {
      "id": "LR-005",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "ResponsesReviewer.review_batch - batch_review.build_request_body (store:false, stream:false single user input_text; no previous_response_id/conversation/tools) to separate CONCEPT_REVIEWER_URL outbound HTTP",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: reviewer endpoint separate from main, no self-recursion",
      "negative_paths": "no session/conversation linkage in request body; reviewer never calls the proxy public endpoint (no recursion)"
    },
    {
      "id": "LR-006",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "batch_review.parse_batch_envelope - BatchProposal - Proposal - runtime_acceptance.accept validates; repair.apply_edits composes original-slice + replacement; model output is an untrusted local proposal only",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (no-edit raw bytes, metadata)",
      "negative_paths": "parse_batch_envelope rejects a full-answer or sentence rewrite (expects one local replacement per id); apply_edits raises on protected overlap"
    },
    {
      "id": "LR-007",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "repair.apply_edits reverse-order original-slice splicing + protected-interval assertion; compose_protection protected = complement of granted + residual machine",
      "evidence": "fresh 22 at main: test_json_no_edit_raw_bytes; full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch (protected-overlap and no-edit cases)",
      "negative_paths": "no-edit to byte-identical; edit intersecting protected to raise; protected slice changed to AssertionError"
    },
    {
      "id": "LR-008",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "corpus.py Evidence.state EXACT/CENSORED/UNAVAILABLE via runtime_corpus.RuntimeCorpus; runtime_acceptance._positive_exact requires an EXACT positive count",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: CENSORED/UNAVAILABLE absence never treated as zero; unknown denominator preserved",
      "negative_paths": "EXACT(0) not positive support; known-zero bigram to no signal (test_known_zero_bigram_no_signal)"
    },
    {
      "id": "LR-009",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "runtime_acceptance.accept: SAME-ORDER factor-two anchored-context comparison (candidate count at least twice the corresponding original-context count) with the narrow R5 possible-typo route (a single EXACT positive adjacent count, count 1); replacement words must be EXACT lexical units; model confidence is never consulted",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: runtime_acceptance._evaluate_pairs / _classify_pair factor-two floor + R5 narrow route",
      "negative_paths": "local-evidence-not-stronger reject; replacement-unigram-uncertain reject; frequency or self-reported confidence alone insufficient"
    },
    {
      "id": "LR-010",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "RepairEngine.repair issues at most one review_batch call per completed answer (review_batch.calls at most 1); no generative retry loop",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "malformed/oversize batch to reject with no second model call to repair JSON"
    },
    {
      "id": "LR-011",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "RepairEngine._fail_closed_original / _fail_closed_evidence / _fail_closed_analysis; late_aborted resets all edits to zero; composed_validation.ComposedMappingError abstains the whole optional pass",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "RuntimeCorpusError during acceptance to whole-pass abort to immutable original; main error/incomplete stays honest (not masked)"
    },
    {
      "id": "LR-012",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "reviewer is an outbound HTTP client (qwen_client.ResponsesReviewer) to a configured endpoint; the CPU path (runtime_detection/runtime_corpus/runtime_acceptance) loads no model",
      "evidence": "source inspection: no model/weights load in the CPU modules; reviewer reuses existing Qwen via HTTP; full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "no second large GPU model load; protected deployment resources unmutated"
    },
    {
      "id": "LR-013",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "qualified default (CONCEPT_TRACE_DIR unset) path is content-free: write_traces returns empty for a None trace_dir, _Handler.log_message returns (access log suppressed), usage_observer is content-free; the full-text trace is a separately-authorized, explicitly opted-in controlled evaluation channel with concrete guards (no-symlink, atomic write, generated request_id, no caller-supplied id)",
      "evidence": "source: proxy.py trace_dir=None default, write_traces early return, log_message suppression; full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch (content-free logging tests)",
      "negative_paths": "trace-off default to no full-text persistence; opted-in trace confined to a controlled channel; production-operator confinement of the opted-in channel is a later deployment control, not a functional defect in the qualified default profile"
    },
    {
      "id": "LR-014",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "governance/report evidence structure (this ICA + 035 reports) keeps software/compatibility/linguistic/deployment axes separate",
      "evidence": "this ICA separates operating-path from linguistic/milestone/deployment; deployment_authorized=false, human_milestone_accepted=false",
      "negative_paths": "no readiness inflation; the native useful-edit at the c304 source-equivalent epoch is reused under R5, not retrofitted as a fresh main acceptance"
    },
    {
      "id": "A-SCOPE-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "validate_request + analysis_policy gate completed Slovenian assistant-text only; conservative malformed-form/word/short-phrase repair; no factual/translation/whole-answer rewriting",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (non-200, metadata, unsupported bypass)",
      "negative_paths": "tool/unsupported-structure responses bypass repair; whole-answer rewrite not performed"
    },
    {
      "id": "A-SEAM-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "library/adapter/reviewer/CPU separation; request-local immutable original (RepairEngine.begin_request); no shared mutable history",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "cancellation targets only request-owned work (no orphan repair); no cross-request buffer sharing"
    },
    {
      "id": "A-STACK-01",
      "class": "PARTIAL",
      "gap": "Python 3.12 and a read-only SQLite index are satisfied; transport uses stdlib http.client rather than the declared HTTPX and the adapter is a raw BaseHTTPRequestHandler rather than the later FastAPI adapter - the architecture labels these future boundaries, so acceptable for the isolated concept-verification prototype but not the declared production baseline (later-stage item, not a functional operating-path defect)"
    },
    {
      "id": "A-ROUTE-01",
      "class": "PARTIAL",
      "gap": "isolated operator-controlled review endpoint with no self-recursion is implemented; real public-gateway coupling (public auth, routes, quotas, accounting) is the later S03 service integration, absent from the standalone loopback prototype (later-stage deployment item, not a functional operating-path defect)"
    },
    {
      "id": "A-SPAN-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "original codepoint offsets with start strictly before end and both within text length; text slice equals original; unique target id; protected non-intersection; runtime_acceptance whole-token span proof",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (mapping/pandoc tests)",
      "negative_paths": "repeated-occurrence before/after disambiguation; combining/emoji/CRLF abstain when unprovable"
    },
    {
      "id": "A-PROTECT-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "pandoc_protection.compose_protection: granted single-line mappable prose editable; complement + residual machine protected",
      "evidence": "fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (pandoc protected/denied/mapping: nfd abstain, nfc-unstable fail-closed, blockquote denied); full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "code/URL/quote/footnote regions protected; no n-gram adjacency manufactured across protected material"
    },
    {
      "id": "A-CORPUS-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "corpus.py Evidence state + scope via runtime_corpus; conservative count-ratio bounds; runtime_acceptance factor-two anchored comparison",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "censored absence not zero; unknown denominator preserved; incompatible normalization/scope not compared"
    },
    {
      "id": "A-CORPUS-02",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "corpus.py archive identity checks (md5+sha256+header/marker) + manifest (source sha256, cutoff 2-per-million, denominator unknown)",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "wrong checksum/size to reject; no runtime scraping; sparse available records only"
    },
    {
      "id": "A-DETECT-01",
      "class": "PARTIAL",
      "gap": "runtime_detection.detect implements bounded non-overlapping deterministic target selection and no-ranked-alternatives-to-reviewer; the lexical-vs-morphological disagreement separation depends on an optional morphology analyzer absent from the prototype (optional per architecture; not a functional operating-path defect)"
    },
    {
      "id": "A-QUESTION-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "batch_review.build_prompt (BATCH_INSTRUCTION batch-v1) preserves the agreed suitability question meaning (natural/appropriate in context, keep/replacement/needs_wider_edit, no factual or stylistic-only edits) with data-not-instructions framing; the verbatim single-sentence Slovenian form is the frozen-v1 single-review variant (qwen_client.prompt); reviewed material is untrusted data, no tools/URL execution, auth separate from conversation state",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch (reviewer request-isolation and main-capture synthetic tests)",
      "negative_paths": "embedded instructions in reviewed text do not become reviewer authority (no tools/URL execution); no main history or shared mutable messages"
    },
    {
      "id": "A-SCHEMA-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "batch_review.parse_batch_envelope + _validate_proposal_item strict schema (keep/replacement/needs_wider_edit semantics per supplied id)",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "unknown/duplicate/missing IDs, invalid JSON, oversized output to whole-batch reject; no salvage or repair call; wider edit leaves target unchanged"
    },
    {
      "id": "A-ACCEPT-01",
      "class": "PARTIAL",
      "gap": "the MVP-relevant strict validated-AUTO_REPAIR acceptance is implemented and proven (every applied edit passes runtime_acceptance.accept + composed_validation); the explicit detect_only/shadow mode progression of ARCH section 11.1 is not exposed as configurable modes - RepairEngine.mode is a detector mode (local-context/unigram-only) and the proxy runs a single strict path with no-suspicion-to-no-review as the natural detection outcome. This is a development-progression literal-contract boundary, not a functional defect (the proxy never delivers an unvalidated edit)"
    },
    {
      "id": "A-ACCEPT-02",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "runtime_acceptance.accept enforces target/valid-proposal/nonprotected-bounds/size/evidence/composed conditions; SAME-ORDER factor-two anchored-context + narrow R5 possible-typo + composed_validation.validate_composed",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: runtime_acceptance reason vocabulary (stale-candidate-bounds, protected, wider-or-identity, control-or-newline, markup, replacement-size, local-evidence-not-stronger, accepted-possible-typo)",
      "negative_paths": "identity replacement, forbidden newline/control/markup, overlong, scope expansion, weak evidence all rejected; LLM_CONFIRMED without sufficient independent evidence stays disabled for automatic MVP changes"
    },
    {
      "id": "A-PATCH-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "repair.apply_edits (immutability, reverse splice, protected assertion) + composed_validation.validate_composed revalidation with arithmetically rebased coordinates",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (no-edit raw bytes)",
      "negative_paths": "overlap/stale to raise; nearby-conflict group rolls back to original; no surviving edit to exact original"
    },
    {
      "id": "A-API-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "validate_request (reject unsupported before main) + JSON and SSE supported shapes; stream/content-type match enforced",
      "evidence": "fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (json + sse logprobs paths, non-200); full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch (including the real 32-case HTTP value matrix and all-copy tests)",
      "negative_paths": "unsupported capability to 400 before main; stream/content-type mismatch to 502 RESPONSE_MODE_MISMATCH"
    },
    {
      "id": "A-HISTORY-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "stateless store:false; main history not mutated; next turn is the final delivered answer; remove_defined_logprobs unconditionally removes logprobs (owner override 08 removes instead of reject/bypass)",
      "evidence": "fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (metadata echo preserved, no-edit byte-identical, all value types); full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "previous_response_id/conversation/incomplete_details to bypass unchanged; no stale logprobs retained (unconditionally removed)"
    },
    {
      "id": "A-LIMIT-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "config finite bounds (capture bytes, codepoint/byte analysis limits, max 4 targets, 1 review, 0 retries, timeouts); analysis_policy.current_limits gate before any optional work",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; source: analysis_policy gate",
      "negative_paths": "oversize answer to fail-closed original with zero optional work; queue/timeout to cancel owned work"
    },
    {
      "id": "A-FAIL-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "failure-contract paths in RepairEngine + _Handler.do_POST (no-suspicion, corpus-fail, queue/timeout, individual reject, conflict rollback, main error, hard capture, disconnect)",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "each failure returns completed original or an honest protocol error; no masked incompleteness; disconnect to cancel owned work"
    },
    {
      "id": "A-SECURITY-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "data-not-instruction (no tools/URL execution); credentials external to Git via env (CONCEPT_REVIEWER_URL/MODEL) referenced without logging values (content-free usage observer); the full-text eval channel is a separately-authorized opt-in surface (write_traces) distinct from the content-free production logs; stateless store:false (no cross-user caching)",
      "evidence": "source: env-credential externalization, log_message suppression, write_traces opt-in confinement (no-symlink/atomic/generated-id); full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch (no-logging tests)",
      "negative_paths": "reviewed material never executed as instruction; no credential values logged; opted-in trace confined to a controlled channel (production operator confinement is a later deployment control, not a functional defect)"
    },
    {
      "id": "A-TEST-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "concept-verification synthetic deterministic suite (1006 methods) + src contract tests",
      "evidence": "fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero; full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; 4 final-head CI checks success at audited tree 7b2418dea1de25734cc12e633344e320e533eb7e via checkout f0834215 (tree equals merge tree); CI epoch distinct from and independent of the suite execution epoch",
      "negative_paths": "negative cases across capture/isolation/mapping/protection/corpus/reviewer/acceptance/patching/operations/api present in the suite; live tests opt-in (a skipped live test is not passed or proof of Qwen quality)"
    },
    {
      "id": "A-EVAL-01",
      "class": "PARTIAL",
      "gap": "eval harness (dev/heldout/frozen/score/review_sheet) is present and Qwen-not-final-judge is upheld, but human-labelled linguistic benefit is not established - the owner excluded a separate human evaluation dataset and heldout scoring requires a live reviewer not re-run at main (quality/eval axis, not an operating-path defect)"
    },
    {
      "id": "A-GOV-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "OAP governance (single full architecture, immutable seeds, D0/D1 policy, one PR per objective, SELF publication)",
      "evidence": "governance accepted-runtime valid at trusted ref; this ICA follows the ordered protocol",
      "negative_paths": "no PLAN/historical-seed mutation; no self-merge; strategy owns the development merge"
    },
    {
      "id": "A-CLOSE-01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "Independent Closure Audit protocol (fresh source-first ICA on current merged main; classification with real paths/SHA)",
      "evidence": "this fresh ICA + prior 034/035 ICA; classifications at the exact revision",
      "negative_paths": "reports treated as claims until corroborated; strategy recommends and the human decides milestone/deployment"
    },
    {
      "id": "MVP-1",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "same operating path as LR-001: whole main answer captured and completion-validated before repair and delivery",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (non-200, metadata)",
      "negative_paths": "incomplete/truncated main not entered into the repairable path"
    },
    {
      "id": "MVP-2",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "same operating path as LR-002: no additional Qwen call without sufficient CPU suspicion",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (zero-call tests)",
      "negative_paths": "no-suspicion / weak-evidence to zero review calls"
    },
    {
      "id": "MVP-3",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "batch_review.parse_batch_envelope + runtime_acceptance.accept: the model may only propose the assigned-span replacement or keep/leave",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "model returning a full sentence/answer or an unassigned span is rejected"
    },
    {
      "id": "MVP-4",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "stateless store:false; the main history is never mutated and carries no review prompt/JSON",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (metadata echo, no-edit byte-identical)",
      "negative_paths": "previous_response_id/conversation present to bypass unchanged; review JSON never enters main history"
    },
    {
      "id": "MVP-5",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "repair.apply_edits mutates only accepted candidate spans; protected-interval assertion",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (no-edit raw bytes)",
      "negative_paths": "any change outside programmatically-confirmed spans to raise / reject"
    },
    {
      "id": "MVP-6",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "fail-closed: invalid proposal or optional abort preserves the already-completed answer",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "invalid/failed batch or late evidence abort to completed original, no damage"
    },
    {
      "id": "MVP-7",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "CENSORED/UNAVAILABLE preserved; truncated frequencies never treated as complete statistics",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "censored absence never converted to zero; unknown denominator stays unknown"
    },
    {
      "id": "MVP-8",
      "class": "PARTIAL",
      "gap": "per-response latency (timings) and additional review usage are reported in the detail/trace, but benefit/harm (accepted-edit precision, harmful edits per originally-correct words) require linguistic evaluation the owner excluded (no separate human dataset) - a quality-measurement boundary, not an operating-path defect"
    },
    {
      "id": "D01",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "responses_contract.py (validate_request, RequestContractError, aligned_metadata_clean, remove_defined_logprobs, validate_completed_envelope) + analysis_policy.py (current_limits, classify_original)",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (logprobs value types, non-200)",
      "negative_paths": "contract negatives (bad shapes/types, unsupported capability) rejected in the suite"
    },
    {
      "id": "D02",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "corpus.py prepare + manifest with identity/cutoff/completeness via runtime_corpus",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "wrong archive checksum/size to reject; missing-data distinction preserved"
    },
    {
      "id": "D03",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "pandoc_protection tokenization/mapping without modifying the original; code/URL/Unicode tests",
      "evidence": "fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (pandoc mapping/protection: nfd abstain, nfc-unstable fail-closed, blockquote denied); full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "NFD/non-NFC lines, unprovable mapping, code/URL/quote regions to abstain/protect"
    },
    {
      "id": "D04",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "runtime_detection.detect selects bounded suspicious sites on a small set",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (zero-call tests)",
      "negative_paths": "everything-correct text to no candidate sent to the model"
    },
    {
      "id": "D05",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "isolated reviewer: fake client proven offline at main (full suite + fresh 22 fake-client paths) and the real-Qwen client proven at the c304 source-equivalent native epoch (T9: validated real-Qwen review, approved original-span patch, defined-probability removal, clean shutdown); c304 and audited main share byte-identical runtime proxy.py 86df8af2, responses_contract.py 0d9347c5 and all runtime/config/dependency bytes (git diff c304..main -- concept-verification changes ONLY README.md and tests/test_responses_contract.py; the tested test file 86d1ae6b is byte-identical to main)",
      "evidence": "native T9 receipt (git_head_at_native_trial=c304bf16e5100337d0ee02244c5a88b5be9028c6; proxy 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2; contract 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7; launcher fd969206; harness d9e7948e; Pandoc 02a59bd9; RO index f769235b; Python 3.12.15; qualified matching-RTX profile; native_calls_by_root=0; validated usage 281/480/761); fake-client half at main; R5 source-equivalent native reuse after byte-identical runtime/dependency equivalence established",
      "negative_paths": "the real-Qwen observation stays at its honest c304 execution epoch (not a pretend fresh main run); limits explicit: one controlled mechanism example, not a quality/precision/harm rate, not statistical independence, not current universal service availability; no new native calls authorized in this offline audit"
    },
    {
      "id": "D06",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "runtime_acceptance.accept accept/reject + repair.apply_edits keeps all other segments",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (no-edit raw bytes)",
      "negative_paths": "rejected proposal leaves the rest of the answer byte-identical"
    },
    {
      "id": "D07",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "write_traces detail records original/candidates/reviewer_decisions/acceptance/replacements + eval/review_sheet.py rendering (opt-in eval channel)",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "no baked special-case rules for specific examples; real cases not hard-coded"
    },
    {
      "id": "M01",
      "class": "PARTIAL",
      "gap": "synthetic dev/heldout labelled cases are present at main; the real target-model answer was observed at the c304 source-equivalent native epoch (T9) plus correct controls; the separate human evaluation dataset is excluded by the owner (quality/eval axis, not a functional operating-path defect)"
    },
    {
      "id": "M02",
      "class": "ABSENT",
      "gap": "no morphology analyzer module exists in the concept-verification prototype; lemmatization/inflection analysis (separating wrong-choice from wrong-inflection) is not implemented (optional per architecture; the M02 deliverable is absent; not a functional operating-path defect)"
    },
    {
      "id": "M03",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "bounded alarm grouping before review; clear edit width (max 4-word replacement); working needs_wider_edit",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch",
      "negative_paths": "grouping never crosses protected material; needs_wider_edit leaves the target unchanged"
    },
    {
      "id": "M04",
      "class": "PARTIAL",
      "gap": "acceptance rule variants and thresholds exist, but precision/harm/coverage measurements by error class are not produced (linguistic evaluation excluded / not run at main); calibration is a quality axis, not an operating-path guarantee"
    },
    {
      "id": "M05",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "queue/cancellation/time/size bounds with safe return to the original",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero",
      "negative_paths": "queue full / timeout / oversize to cancel owned work and return completed original"
    },
    {
      "id": "M06",
      "class": "IMPLEMENTED",
      "tested_sha": "1bb9eec748bda198e52781f2b96cbea37760a172",
      "runtime_path": "one clearly-supported nonstreaming text shape (JSON) with context preservation and no recursion",
      "evidence": "full suite 1006/718.100s/interpreter-exit0 (log 88593a73) executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6+ final WIP test bytes (test_responses_contract.py 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4, byte-identical to audited main); frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are byte-identical to main; f64da10 is a source-equivalent commit, not the execution epoch; fresh 22 named existing tests at main, literal interpreter-exit0 (log bbf85422): logprobs JSON/SSE null/empty/populated/unexpected/object/string + ineligible + non-200; no-edit raw-byte identity; metadata echo preserved; Pandoc startup wrong-version/capability/timeout; mapping NFD-abstain/NFC-unstable fail-closed/blockquote-denied; zero-call high-identity + safe-known-zero (json paths, non-200)",
      "negative_paths": "unsupported streaming / SSE mismatch to bounded rejection"
    },
    {
      "id": "M07",
      "class": "PARTIAL",
      "gap": "eval/score.py provides comparison scaffolding (agreed method vs baselines), but a full comparative report at this revision is not produced (a heldout run requires a live reviewer and is not re-run at main)"
    }
  ],
  "deployment_authorized": false,
  "human_milestone_accepted": false
}
```

## 1. Identity, chronology and frozen initial derivation

Exact accepted audited main 1bb9eec748bda198e52781f2b96cbea37760a172 (tree 7b2418dea1de25734cc12e633344e320e533eb7e); PLAN sha256 d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0; ARCHITECTURE
sha256 a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7. The audit ran in a fresh chat in the SAME owner-launched
foreground CLI (pid 3341327, argv "codex --yolo --profile early-beta", tmux),
same home/auth/cwd; no second CLI, subagent, background model or provider
switch. Control OK was consumed once outside the model and was never waited on
again inside it.

Source-first chronology (verified): the neutral attributable owner scope and the
COMPLETE canonical PLAN.md and ARCHITECTURE.md at the exact audited main were
read first, and the initial requirements-first derivation was SAVED AND HASHED
BEFORE any runtime, registry, README conclusion, prior report/audit, or
deferred-evidence-index access. The immutable private initial record is
identified by byte length 23192 and sha256 1fa67b855bdbed14cd1b1905d59b02e59079bb3b6fe999048817b6a8af2fb989; it lives in the
supplied private 036 scratch, remains unpublished, and is byte-identical to its
private backup. No physical root or credential appears in any public artifact;
this audit cites it by identity only.

Independence limit: a fresh chat of the same model may retain correlated blind
spots, and tests can miss architecture requirements. That is mitigated by the
complete independent source derivation before claims, explicit fake seams and
negative evidence, and independent strategic review. No statistical
independence or predetermined outcome is claimed.

## 2. Owner-scope override coverage (beyond the frozen registry)

The following are independently derived from the neutral owner scope and remain
visible beyond the 59-row registry. EXCLUDED_OWNER items are excluded, not
deferred.

| ID | Owner requirement | Audit status | Where |
|---|---|---|---|
| OV-01 | Pandoc as structural prose-vs-protected parser; replace pulldown-cmark | IMPLEMENTED | pandoc_protection (commonmark_x+sourcepos-smart); no pulldown-cmark in runtime |
| OV-02 | Exact original spans; never regenerate via AST-to-Markdown | IMPLEMENTED | repair.apply_edits original-slice splicing; no Markdown reserializer in the patch path |
| OV-03 | Test how Pandoc maps to source positions; no ambiguous substring match | IMPLEMENTED | _Document.map_span column-exact, single-line, None-when-unprovable; fresh probe mapping tests |
| OV-04 | Mapping failure to region unchanged / document to original | IMPLEMENTED | ungranted spans stay protected; protect_with_pandoc fail-closed returns original |
| OV-05 | Installed, versioned Pandoc with startup check; no historical-dir search; no silent regex fallback | IMPLEMENTED | resolve_pandoc_spec env-var-then-PATH only; check_pandoc exact-version + positioned-JSON capability probe; fail-closed on any reason (fresh probe: wrong_version/capability_failure/startup_timeout) |
| OV-06 | Scoped to runnable proxy; no research restart; no unrelated gates | IMPLEMENTED | audit scope confined to the concept-verification proxy; no new gates introduced |
| OV-07 | NO separate human evaluation dataset | EXCLUDED_OWNER | not a functional prerequisite; benefit/harm measurement boundary noted in MVP-8/A-EVAL-01/M01 |
| OV-08 | ALWAYS remove API logprobs regardless of repair/acceptance; must not prevent repair | IMPLEMENTED | remove_defined_logprobs by presence before eligibility; transform_json/normalize_* run on every answer-bearing representation (fresh probe all value types) |
| OV-09 | Remove logprobs from defined token-prob locations only; no recursive same-name deletion | IMPLEMENTED | remove_defined_logprobs targets recognized output_text parts only; no recursive traversal of user data/metadata echoes (test_json_metadata_echo_preserved) |
| OV-10 | Consistent across supported JSON and SSE | IMPLEMENTED | transform_json + transform_sse + normalize_json_body/normalize_sse_body cover 200 and non-200 by actual content type (fresh probe json+sse) |
| OV-11 | Preserve citations, annotations, usage, IDs, completion status, other metadata | IMPLEMENTED | aligned_metadata_clean + strict reviewer usage + validated message id preserved; test_json_metadata_echo_preserved |
| OV-12 | Preserve malformed/incomplete/capture-limit/cancellation semantics | IMPLEMENTED | malformed JSON/SSE returned unchanged; incomplete SSE to CaptureError; hard cap to bounded API failure; cancellation to abort owned work |
| OV-13 | Keep mandatory pinned Pandoc protection + exact-span corrections unchanged | IMPLEMENTED | installed pinned Pandoc 3.7.0.2 binary sha256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229 (the release-archive/tarball sha256 8f8f67fd is a different artifact, not the installed binary); exact-span correction path unchanged |
| OV-14 | One consistent behavior; no configuration switches for the policy | IMPLEMENTED | single unconditional code path; no feature flag toggling logprobs removal |
| OV-15 | Document no token probabilities; answer text identical without correction | IMPLEMENTED | transform_json: no-edit path returns byte-identical answer text; only probability-field removal may change wire data (test_json_no_logprobs_no_edit_byte_identical) |
| OV-16 | Tests for absent/null/empty/populated/unexpected-type logprobs incl. zero-review and accepted-edit paths | IMPLEMENTED | fresh probe covers null/empty/populated/unexpected-type/object/string + zero-review at main; the accepted-edit HTTP value matrix and all-copy tests come from the source-equivalent full suite (D real 32-case matrix), named at that boundary, not from the fresh 22 |
| OV-17 | Persistent allowances (1M RTX, 10 publication recoveries) | CONTEXT | not a functional requirement; not exercised by this offline audit |

## 3. Full-source coverage projection (beyond the 59-row registry)

R3 requires the full-source-derived coverage and separately derived architecture
facets, not just the registry rows. The projection below is privacy-safe (no
physical roots, credentials, or native content) and is IN ADDITION to the 59-row
MVP registry and the 17 owner overrides.

### 3a. The 5 SERVICE rows (later stage; NOT MVP functional gates)

| ID | Requirement (PLAN section 15) | Stage | Applicability at this revision |
|---|---|---|---|
| S01 | wider negative tests (more correct/technical text; statistically meaningful harm report) | LATER_STAGE | breadth of A-EVAL-01 linguistic axis; not an MVP functional gate |
| S02 | wider data support (collocations/fuller n-grams when measurements show benefit; ordered usage rights) | LATER_STAGE | data-acquisition axis (A-CORPUS-02 source candidates); not an MVP functional gate |
| S03 | production coupling (explicit gateway path, separated repair spend, load limits) | LATER_STAGE | deployment integration absent from the standalone loopback prototype (see A-ROUTE-01); not an MVP functional gate |
| S04 | installation and rollback (packaging, health checks, config, repair-disable without changing Qwen) | LATER_STAGE | packaging/ops deliverable absent from the prototype; not an MVP functional gate |
| S05 | final documentation (supported/unsupported cases, data versions, known limits, repeatable tests) | LATER_STAGE | README present; full service documentation not produced; not an MVP functional gate |

### 3b. The 8 PLAN16 criteria (section 16)

| Criterion | Status / path |
|---|---|
| MVP-1 | IMPLEMENTED - same operating path as LR-001: whole main answer captured and completion-validated before repair and delivery |
| MVP-2 | IMPLEMENTED - same operating path as LR-002: no additional Qwen call without sufficient CPU suspicion |
| MVP-3 | IMPLEMENTED - batch_review.parse_batch_envelope + runtime_acceptance.accept: the model may only propose the assigned-span re |
| MVP-4 | IMPLEMENTED - stateless store:false; the main history is never mutated and carries no review prompt/JSON |
| MVP-5 | IMPLEMENTED - repair.apply_edits mutates only accepted candidate spans; protected-interval assertion |
| MVP-6 | IMPLEMENTED - fail-closed: invalid proposal or optional abort preserves the already-completed answer |
| MVP-7 | IMPLEMENTED - CENSORED/UNAVAILABLE preserved; truncated frequencies never treated as complete statistics |
| MVP-8 | PARTIAL - per-response latency (timings) and additional review usage are reported in the detail/trace, but benefit/harm (accepted-edit precision, harmful edits  |

### 3c. Architecture sections and facets (ARCHITECTURE 1-21)

| Architecture section | Primary registry rows | Actual path / proof / applicability |
|---|---|---|
| 1 Purpose/authority/change control | A-GOV-01 | one current full architecture + immutable historical seeds + ordered D0/D1; change control via OAP law |
| 2 Fixed product invariants | LR-001..LR-014 | operating-path invariants proven offline/synthetically at main (suite + fresh 22 + source) |
| 3 Scope and non-goals | A-SCOPE-01 | completed Slovenian text only; no factual/translation/whole-answer rewriting |
| 4 Components/deployment boundary (4.1 baseline) | A-STACK-01; A-ROUTE-01 | stdlib http.client + BaseHTTPRequestHandler now; HTTPX/FastAPI later; isolated endpoint now, gateway later (S03) |
| 5 End-to-end state and ownership | A-SEAM-01; A-SCOPE-01 | request-local immutable original; no shared mutable history; bounded per-request ownership |
| 6 Text/span/result contracts | A-SPAN-01; D01; A-ACCEPT-02 | original codepoint spans; responses_contract/analysis_policy; strict acceptance bounds |
| 7 Protected material and context segmentation | A-PROTECT-01; D03 | pandoc_protection granted prose vs protected complement; no cross-protected adjacency |
| 8 Corpus evidence and reproducible indexes (8.1/8.2) | A-CORPUS-01; A-CORPUS-02; D02; LR-008 | corpus.py evidence states + scope; archive identity + manifest; CENSORED/UNAVAILABLE preserved |
| 9 CPU detection and target selection | LR-002; D04; A-DETECT-01 | runtime_detection.detect bounded non-overlapping targets; morphology separation optional |
| 10 Isolated Qwen review (10.1/10.2/10.3) | A-QUESTION-01; LR-005; LR-004; A-SCHEMA-01; D05 | batch_review prompt (suitability meaning); isolated store:false request; strict schema; fake+real client validated decisions |
| 11 Acceptance policies (11.1/11.2) | A-ACCEPT-01; A-ACCEPT-02 | strict validated-AUTO_REPAIR path; mode-progression literal boundary (11.1) vs strict rules (11.2) |
| 12 Exact patching and composed validation | A-PATCH-01; LR-007; D06 | apply_edits original-slice + protected assertion; composed_validation revalidation |
| 13 HTTP and main-history integration | A-API-01; A-HISTORY-01; LR-001 | validate_request + JSON/SSE; stateless; capture before delivery |
| 14 Bounded resources/cancellation/fallback (14.1/14.2) | A-LIMIT-01; A-FAIL-01; M05 | finite bounds before optional work; full failure contract |
| 15 Security, privacy and protected environment | A-SECURITY-01; LR-013 | data-not-instruction; credentials external; content-free default logs; separately-authorized opt-in eval channel |
| 16 Verification and evidence layers (16.1/16.2/16.3) | A-TEST-01; D05; A-EVAL-01 | software-contract suite; source-equivalent native live compatibility; linguistic evaluation owner-excluded |
| 17 Concentrated OAP operating architecture | A-GOV-01 | concentrated HWP/HJP/DHA roles; one PR per objective; SELF publication |
| 18 Deferred judgment and deliberate CRITICAL loading | A-GOV-01; A-CLOSE-01 | deferred evidence index; prior reports treated as claims until corroborated |
| 19 Milestones, progress and Independent Closure Audit | A-CLOSE-01 | this fresh source-first ICA; classification with real paths/SHA |
| 20 Bootstrap acceptance versus product acceptance | A-GOV-01; A-CLOSE-01 | bootstrap proves inactive infrastructure only; product acceptance separate; deployment/milestone retained by owner |
| 21 Source and revision notes | provenance | PLAN sha d2aa1d98cc51...; ARCH sha a16e0f87bdb2...; audited main 1bb9eec748bd...; tree 7b2418dea1de... |

## 4. Evidence base and reuse provenance

- **Fresh bounded probe at 1bb9eec748bda198e52781f2b96cbea37760a172:** 22 named existing tests run with the
  qualified setup (qualified Python 3.12.15 -B, CONCEPT_PANDOC at the neutral
  pinned 3.7.0.2 binary sha256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229, private 036 TMP/cache/logs, shell
  umask 077). Literal interpreter exit 0 captured before any tail; log bbf8542221be3c78ba8fefa7a55bf23258a5781e688b42ff5be744d752dd6b02
  (4007B, "Ran 22 tests in 17.020s", OK). Scope: logprobs JSON/SSE across
  null/empty/populated/unexpected-type/object/string + ineligible + non-200;
  no-edit raw-byte identity; metadata preservation; Pandoc startup
  (wrong-version / capability / timeout); mapping abstention and fail-closed;
  zero-call paths. It does NOT itself contain the accepted-edit HTTP value
  matrix or a protected-overlap acceptance case; those are named at their
  actual boundary below.
- **Source-equivalent reuse of the 035-d full suite (honest epoch):** the
  independently verified full concept suite (1006 tests, 718.100s, literal
  interpreter exit 0; log 88593a73822461bd1ebac2e1e1cf3c0416e563766770401014561931dfba5204, 169538B) was executed at git HEAD c304bf16e5100337d0ee02244c5a88b5be9028c6
  PLUS the final ordered working-tree test bytes: its tested
  test_responses_contract.py hash 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4 is byte-identical to the audited
  main 1bb9eec748bda198e52781f2b96cbea37760a172, while the frozen runtime proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and
  responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7 are also byte-identical to main. Session
  34148 returned literal FULL_EXIT 0 (04:00:56.882Z to 04:17:35.747Z).
  **f64da10 is a source-equivalent commit and was NEVER the execution epoch**;
  c1fa and f64 were committed after that run. This suite is reused as
  source-equivalent evidence at 1bb9eec748bda198e52781f2b96cbea37760a172; it is named at its real epoch
  (c304bf16e5100337d0ee02244c5a88b5be9028c6 + WIP test bytes) and is NOT claimed to have been freshly run at
  1bb9eec748bda198e52781f2b96cbea37760a172. It supplies the accepted-edit HTTP 32-case value matrix and the
  all-copy tests that the fresh 22 does not cover.
- **CI at the exact tree:** the four required final-head CI checks
  (Application baseline, Research reproducibility, OAP bootstrap acceptance,
  OAP report history) succeeded at the audited tree 7b2418dea1de25734cc12e633344e320e533eb7e via checkout
  f0834215 (tree equals merge tree). The CI epoch is distinct from and
  independent of the suite execution epoch.
- **First test invocation (corrected):** the initial 300s invocation piped the
  interpreter through "tail", so its observed shell status was tail's, not the
  interpreter's, and no full-suite completion summary was captured. It is
  recorded as LIMITED/INCOMPLETE with interpreter-exit UNKNOWN and is used for
  nothing beyond documenting the boundary; it is neither a fresh successful
  full suite nor a product-failure diagnosis.
- **Deferred index / native epoch (equivalence established):** prior
  reports/audits/README are claims, not authorities. The native target
  qualification (T9) was executed at the c304bf16e5100337d0ee02244c5a88b5be9028c6 native epoch, and that epoch is
  SOURCE-EQUIVALENT to the audited main for the relevant software:
  `git diff c304bf16e5100337d0ee02244c5a88b5be9028c6..1bb9eec748bda198e52781f2b96cbea37760a172 -- concept-verification` changes ONLY README.md and
  tests/test_responses_contract.py, so all runtime/config/dependency bytes are
  identical (proxy.py 86df8af2f082389935e0c407bee6ae1c33f91721b7a600f73f2b8985995b67d2 and responses_contract.py 0d9347c57ce56ea134012a7065ea238d0c0aede5ea5cc87a85dd6c76ca2c38a7
  sha-identical at both epochs; the tested test file 86d1ae6be3c8f2b8a1f2305472800550630e218e5b7c3970f69686aaa42f11c4 equals main).
  The final qualifying pair used launcher fd969206, harness d9e7948e, Pandoc
  02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229, RO index f769235b, Python 3.12.15 and the qualified
  matching-RTX message-array profile. Under R5 this native observation is
  reusable after this actual source/dependency/profile equivalence. No native
  calls are made in this offline audit; the historical execution stays at the
  c304bf16e5100337d0ee02244c5a88b5be9028c6 epoch/time/profile, not a pretend fresh 1bb9eec748bda198e52781f2b96cbea37760a172 run. Limits stay
  explicit (one controlled mechanism example, not quality/universal service/
  current availability).

## 5. Findings and concrete gaps

Coverage of the frozen 59-row MVP registry: 49
IMPLEMENTED, 9 PARTIAL, 0
UNPROVEN, 1 ABSENT. Independently derived owner-scope
(section 2) and full-source coverage (section 3) are in addition to the
registry.

Concrete bounded gaps (earliest failing boundary, concrete proof, consequence,
smallest sufficient fix):

- **A-STACK-01** (PARTIAL): Python 3.12 and a read-only SQLite index are satisfied; transport uses stdlib http.client rather than the declared HTTPX and the adapter is a raw BaseHTTPRequestHandler rather than the later FastAPI adapter - the architecture labels these future boundaries, so acceptable for the isolated concept-verification prototype but not the declared production baseline (later-stage item, not a functional operating-path defect)
- **A-ROUTE-01** (PARTIAL): isolated operator-controlled review endpoint with no self-recursion is implemented; real public-gateway coupling (public auth, routes, quotas, accounting) is the later S03 service integration, absent from the standalone loopback prototype (later-stage deployment item, not a functional operating-path defect)
- **A-DETECT-01** (PARTIAL): runtime_detection.detect implements bounded non-overlapping deterministic target selection and no-ranked-alternatives-to-reviewer; the lexical-vs-morphological disagreement separation depends on an optional morphology analyzer absent from the prototype (optional per architecture; not a functional operating-path defect)
- **A-ACCEPT-01** (PARTIAL): the MVP-relevant strict validated-AUTO_REPAIR acceptance is implemented and proven (every applied edit passes runtime_acceptance.accept + composed_validation); the explicit detect_only/shadow mode progression of ARCH section 11.1 is not exposed as configurable modes - RepairEngine.mode is a detector mode (local-context/unigram-only) and the proxy runs a single strict path with no-suspicion-to-no-review as the natural detection outcome. This is a development-progression literal-contract boundary, not a functional defect (the proxy never delivers an unvalidated edit)
- **A-EVAL-01** (PARTIAL): eval harness (dev/heldout/frozen/score/review_sheet) is present and Qwen-not-final-judge is upheld, but human-labelled linguistic benefit is not established - the owner excluded a separate human evaluation dataset and heldout scoring requires a live reviewer not re-run at main (quality/eval axis, not an operating-path defect)
- **MVP-8** (PARTIAL): per-response latency (timings) and additional review usage are reported in the detail/trace, but benefit/harm (accepted-edit precision, harmful edits per originally-correct words) require linguistic evaluation the owner excluded (no separate human dataset) - a quality-measurement boundary, not an operating-path defect
- **M01** (PARTIAL): synthetic dev/heldout labelled cases are present at main; the real target-model answer was observed at the c304 source-equivalent native epoch (T9) plus correct controls; the separate human evaluation dataset is excluded by the owner (quality/eval axis, not a functional operating-path defect)
- **M02** (ABSENT): no morphology analyzer module exists in the concept-verification prototype; lemmatization/inflection analysis (separating wrong-choice from wrong-inflection) is not implemented (optional per architecture; the M02 deliverable is absent; not a functional operating-path defect)
- **M04** (PARTIAL): acceptance rule variants and thresholds exist, but precision/harm/coverage measurements by error class are not produced (linguistic evaluation excluded / not run at main); calibration is a quality axis, not an operating-path guarantee
- **M07** (PARTIAL): eval/score.py provides comparison scaffolding (agreed method vs baselines), but a full comparative report at this revision is not produced (a heldout run requires a live reviewer and is not re-run at main)

## 6. Distinctions (kept separate, not inferred)

- **Functional operating path** (capture, protection, detection, isolated
  review, strict acceptance, patching, delivery, unconditional typed logprobs)
  is what this audit calls "functional readiness." It is demonstrated
  offline/synthetically at 1bb9eec748bda198e52781f2b96cbea37760a172 via the source-equivalent full suite, the
  fresh probe, and the source-equivalent native observation.
- **Linguistic quality** (accepted-edit precision, harmful edits) is NOT
  established; the owner excluded a separate human evaluation dataset.
- **Formal milestone acceptance** is retained by the owner.
- **Deployment authority** is retained by the owner; no deployment side effect
  is authorized.
- **Statistical independence**: the same-Qwen review is context-isolated but
  not statistically independent; independent CPU evidence (LR-009) remains
  required.

## 7. Verdict and bounded remediation

The runnable proxy implements and proves the functional operating path at the
exact audited revision, including the owner's unconditional typed logprobs
policy across JSON and SSE and exact-original-span correction with mandatory
pinned Pandoc. The strict validated-AUTO_REPAIR acceptance (every applied edit
passes runtime_acceptance.accept + composed_validation) is the single operating
acceptance path; the explicit detect_only/shadow mode progression (ARCH 11.1)
is not exposed as modes (a development-progression literal boundary, not a
functional defect). The isolated-reviewer contract (fake client at main;
real-Qwen client at the source-equivalent c304 native epoch) is satisfied under
R5 after verified byte-identical runtime equivalence. The qualified default
logs are content-free and the full-text trace is a separately-authorized
opt-in evaluation channel.

Full section 16 MVP closure is NOT complete. The bounded residual items are:
later-stage deployment/stack coupling (A-ROUTE-01, A-STACK-01) and the SERVICE
rows (S01-S05); the A-ACCEPT-01 mode-progression literal boundary; optional
morphology (A-DETECT-01, M02 absent); and the excluded/unmeasured linguistic
axis (MVP-8, A-EVAL-01, M01, M04, M07). Each is named at its earliest boundary
with concrete proof, consequence and smallest sufficient remediation in
section 5. No deployment, no human milestone acceptance, and no
linguistic-quality claim is made. An incomplete/negative result is a valid
truthful outcome; these concrete gaps return bounded remediation to strategy.

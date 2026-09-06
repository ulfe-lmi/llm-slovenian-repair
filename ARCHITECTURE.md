# LLM Slovenian Repair — Architecture

**Version:** 1.1 (governance reconciliation; product sections 2–16 unchanged).  
**Date:** 2026-09-06.  
**Status:** Human Work Preloading implementation baseline, not implementation evidence.  
**Product agreement:** [PLAN.md](PLAN.md), preserved byte-for-byte.  
**Deferred judgment:** [CRITICAL.md](CRITICAL.md).  
**Bootstrap specification:** supplied INSTRUCTIONS and its specifications; installed as reference under `docs/bootstrap/`.

## 1. Purpose, authority and change control

This full architecture implements the agreed completed-response repair design.
The bootstrap generator installs these bytes rather than inventing a replacement.
It may generate a compact executor projection, never a competing product design.

### 1.1 Document roles and authority

| Document | Role |
|---|---|
| `PLAN.md` | Protected product agreement, including rationale, proposals and measured-versus-unmeasured distinctions. |
| Root `ARCHITECTURE.md` | Single canonical full current implementation architecture; strategy reads it directly. |
| Root `ARCHITECTURE-for-agents.md` | Dense coding projection with source revision/hash and complete executor-relevant coverage. |
| Root `AGENTS.md` | Tiny role router, not either operational constitution. |
| `oap/coding-instructions/AGENTS.md` | Dense coding operational law. |
| `oap/strategic-instructions/AGENTS.md` | Canonical full strategic constitution; controlled copy installed in STRATEGIC_HOME. |
| Root `CRITICAL.md` | Single canonical live DHA register; loaded deliberately, not always. |
| Orders/reports/tests/PRs | Scope and evidence under these sources, not invented human authority. |

Explicit human decisions and higher-priority environment instructions control.
PLAN controls agreed product behavior. Concentrated OAP, as supplied by the owner,
controls the process extensions to ordinary OAP. Concrete role-routing, token
budgets, FIFO framing and report-commit conventions are project implementation
choices, not falsely attributed universal OAP requirements.

The full architecture must exist even when coding does not load it. Compact law
must preserve every relevant obligation, exception, prohibition, authority and
failure behavior. It is an operational projection, not a license to omit an
invariant. Inconsistency stops affected work and returns to strategy; an executor
must not silently choose the easier version.

### 1.2 Context loading and recovery

Coding normally loads only the repository router, dense coding constitution,
compact architecture, compact coding communication contract, the exact active
order, and relevant local security/testing/subtree contracts. Do not require full
PLAN, full architecture, the roadmap, strategic constitution, original OAP chapters
or complete CRITICAL history in every coding context. Full-source existence and
hash checks are performed by helpers without injecting that source into the model.

A specific order or explicit human instruction may require named full-source
sections for a bounded task. Unresolved compact-law ambiguity is reported to
strategy; it does not authorize unrestricted context loading or invented law.

Strategy starts in its separate workspace, reads its full constitution and the
canonical full PLAN/ARCHITECTURE from REPO_ROOT, reconciles current GitHub/OAP,
and reads the current critical register. Subsequent loads are relevance-based;
CRITICAL is revisited for related dilemmas, aggregate risk and gates. Process,
provider and context replacement preserve the same logical role and objective.

### 1.3 Copy and revision law

Bootstrap preserves supplied PLAN/ARCHITECTURE/CRITICAL bytes and immutable audit
seeds. The current full architecture lives only at repository root; do not create
independently editable full architecture or PLAN mirrors in STRATEGIC_HOME or the
strategic seed. A private reference file records resolved source paths/hashes.
The full strategic constitution has one versioned source and one deliberate
runtime copy; drafts/configuration remain private mutable state.

After bootstrap, strategy may order bounded implementation-detail changes
consistent with PLAN and delegated D0/D1 authority. Record old revision/hash,
changed clauses, rationale, tests, classifications and affected projections. D1
adds a qualifying exact critical entry; D2 does not become allowed by registration.
Foundational human intent and protected boundaries need explicit human authority.

Update the canonical document, compact projections and distillation manifest in
the same authorized PR. Compare against a trusted accepted base, not just candidate
hashes. Refresh the private strategic constitution at a quiescent checkpoint after
accepted merge; reread before the next order. Never install an unaccepted candidate
as unrelated runtime law or rewrite historical seeds to hide a revision.


## 2. Fixed product invariants

The identifiers below are stable references for work orders, compact views and tests. They express the agreed design and its safety boundaries; they are not a claim that the tests already exist.

| ID | Mandatory invariant | PLAN basis |
|---|---|---|
| LR-001 | Complete main generation and capture before CPU review, repair inference and delivery of answer text. | §§1, 3, 11.3 |
| LR-002 | CPU evidence chooses whether review is warranted; no eligible suspicion means zero review calls and unchanged text. | §§1, 7 |
| LR-003 | Review targets are preassigned words or short phrases, not model tokens or unrestricted sentences. | §§1, 7.2, 8 |
| LR-004 | Ask about the suitability of the specific expression; permit `keep` and `needs_wider_edit`; do not demand a change. | §8 |
| LR-005 | Construct a new isolated review request; never contaminate the main conversation, inherit its linkage, or recurse through repair. | §§4, 11.2 |
| LR-006 | Reviewer output is an untrusted local proposal; code validates and inserts replacements. The model never regenerates the answer. | §§8–10 |
| LR-007 | Preserve every original substring outside accepted spans, including protected material and original formatting. | §§5, 10 |
| LR-008 | Preserve `EXACT`, `CENSORED` and `UNAVAILABLE` evidence semantics; missing truncated data is not zero. | §6 |
| LR-009 | Strict acceptance needs appropriate independent evidence; frequency or self-reported model confidence alone is insufficient. | §9 |
| LR-010 | Use bounded, one-pass initial review; do not introduce an automatic generative correction/retry loop. | §§3, 13 |
| LR-011 | Optional repair failure preserves an already safely captured original; never mask main errors, incomplete output or hard capture limits. | §13.3 |
| LR-012 | Reuse the existing Qwen; CPU-side repair infrastructure must not load another large GPU model or mutate the protected deployment. | §§1, 11–13 |
| LR-013 | Production logs contain no user text, target/replacement strings, prompts or secrets; evaluation is separately authorized. | §13.4 |
| LR-014 | Code correctness, model compatibility, linguistic benefit and deployment/release authority require separate evidence. | §§14–16 |

## 3. Scope and non-goals

The first product supports completed Slovenian natural-language responses, including conservative review of malformed forms, local morphological mismatches and contextually inappropriate words or short phrases. Every candidate must be attributable to a precisely bounded original span.

Do not implement whole-answer rewriting, translation, factual correction, autonomous editing of generated files, code or tool arguments, self-training, an additional large GPU corrector, or live token-by-token correction. General proofreading may exist only as an explicitly separate evaluation baseline.

Do not infer that every observed error is caused by quantization. The initial error-rate estimate and the example words in PLAN are observations and motivating examples, not calibrated statistics or a hardcoded repair dictionary.

Ambiguous language, insufficient data, unknown terminology and structures that cannot be safely mapped back to the original are abstention cases. Useful low coverage is preferable to unsupported automatic changes.

## 4. Components and deployment boundary

The library is independent of HTTP, the gateway and conversation storage. Its reviewer dependency is injectable so the full logic can be tested without a model.

```text
Client
  -> existing public gateway, where applicable
  -> explicitly enabled repair adapter
       -> existing MAIN model route -> existing Qwen
       <- complete main response, safely captured
       -> CPU analysis
       -> isolated REVIEW client -> same Qwen, private nonrecursive route
       <- bounded structured proposal
       -> CPU validation and deterministic patching
  <- one final response through the original delivery path
```

The gateway retains public authentication, route permissions, quotas and public accounting policy. Existing `slaif-local-coding` remains a separate project and may participate in the main route; its context compilation must not run on the isolated review route. This architecture does not authorize edits to either neighboring repository or a production cutover.

The review client uses a trusted configured endpoint or injected client. It cannot accept a caller-supplied destination, forward main-conversation credentials indiscriminately, or rely on a public bypass header. Diagnostic correlation can remain internal without creating a conversation linkage.

### 4.1 Selected implementation baseline

The initial engineering baseline follows PLAN §12: Python 3.12, a locked `uv` environment, typed validated contracts, HTTPX for the review request, `pytest` with fake upstreams, and FastAPI only for the later narrow adapter. Verify dependency compatibility before pinning actual versions. Do not claim current CLI/model/server compatibility from a historical example.

Use read-only sparse SQLite indexes initially unless measured evidence justifies an alternative. CPU linguistic analyzers are optional bounded dependencies. Avoid multiplying large analyzers/indexes across uncontrolled worker processes. No corpus/model downloads or network calls occur merely on package import.

The bootstrap generates these module boundaries and their work orders, **not the application implementation**:

| Module | Responsibility |
|---|---|
| `contracts.py`, `policy.py` | Original-span, evidence, review, decision, result and finite policy contracts. |
| `protected_spans.py`, `tokenizer.py` | Source-preserving segmentation and original-position mapping. |
| `corpus.py`, optional `morphology.py` | Provenance-aware CPU evidence and uncertainty. |
| `detector.py` | Explainable suspicion and bounded target selection. |
| `prompts.py`, `reviewer.py` | Versioned narrow question and isolated same-Qwen request. |
| `acceptance.py` | Structural, contextual and policy decisions on proposals. |
| `patcher.py` | Exact original-slice composition and conflict-group rejection. |
| `pipeline.py` | Completed-text orchestration, resource budgets and fallback. |
| `cli.py` | Explicit local inspection of supplied/evaluation text. |
| `api.py` | Later bounded capture, supported envelope mapping and final delivery. |

## 5. End-to-end state and ownership

Each response has request-local immutable input text, bounded analysis state, selected targets, at most one initial review batch, validated decisions and one final result. No mutable conversation list or response buffer is shared across requests.

```text
MAIN_FINISHED
  -> CAPTURED
  -> ANALYZED
       -> RETURNED_ORIGINAL          [no eligible target / analysis bypass]
       -> REVIEWED
            -> RETURNED_ORIGINAL     [optional review failure]
            -> VALIDATED
                 -> RETURNED_ORIGINAL [no accepted edit / shadow]
                 -> PATCHED
                 -> RETURNED_FINAL
```

A main failure or truncation does not enter the successful `CAPTURED` path by pretending the partial content is complete. Completion must be checked according to the explicitly supported upstream protocol, not simply by treating socket closure as success.

The adapter owns main-response capture and delivery. The library operates on already completed text. The reviewer owns one new outbound request. CPU workers own only bounded analysis tasks. Cancellation propagates to work owned by the disconnected request; it must not cancel unrelated requests or launch an orphaned repair.

Main generation and review for one answer are sequential. A global bounded review admission policy is still needed because other users may be generating concurrently. This design makes no claim that one Python thread creates extra GPU capacity.

## 6. Text, span and result contracts

Use Python-string Unicode code-point offsets into the **unmodified original string** for the initial library contract, matching PLAN §5.2. Offsets are not UTF-8 byte positions, JavaScript UTF-16 positions or Qwen tokenizer positions. Any future boundary conversion must be explicit and tested.

A selected span has at least an internal `span_id`, inclusive `start`, exclusive `end`, exact `original`, containing sentence/context boundaries and evidence references. Required conditions include:

```text
0 <= start < end <= len(original_text)
original_text[start:end] == selected_span.original
span_id is unique within this response
selected span does not intersect protected material
```

Internal IDs and offsets are CPU-assigned. Qwen may not choose new positions, invent IDs or extend a target. Repeated identical words must be distinguished by the serializer through exact target occurrence, such as `before_target`, `target` and `after_target`.

The result contains final text, whether it changed, original-coordinate edits, suspicion/decision metadata, counted review calls and timings. Exposing these details through a local evaluation CLI is not permission to log them in production or add them to the main chat.

Lookup normalization, case folding and linguistic tokenization may operate on derived views only. They must not normalize the original, rebuild Markdown or change whitespace. Combining marks, emoji and CRLF require explicit tests; unsafe partial-character/grapheme targeting should abstain rather than damage the source.

## 7. Protected material and context segmentation

The adapter must select explicitly supported assistant-text fields. Never recursively repair every string in a response object. Tool/function fields, model/response IDs, schemas, structured JSON output, reasoning fields, images and binary data are not editable natural-language text.

Within eligible text, protect fenced and indented code, inline code, URLs and link destinations, email addresses, filesystem paths, commands, numbers and units, citations and other machine-significant or quoted material as specified in PLAN. Proper names, titles, technical terms and mixed languages require conservative exclusion or a clearly bounded terminology policy.

The initial adapter bypasses entire responses containing tools or unsupported structures. A future partial-field policy requires explicit architecture and contract tests, not an optimistic recursive traversal.

A protected interval is also a linguistic-context boundary. Removing it from a token list must not manufacture a new bigram or trigram between the text on either side. Markdown parsing may locate spans, but Markdown reserialization is not an acceptable patcher.

## 8. Corpus evidence and reproducible indexes

### 8.1 Evidence values

An evidence record contains source/version, normalization and annotation conventions, measurement scope, completeness/cutoff metadata and one of:

| Status | Meaning |
|---|---|
| `EXACT` | The count is known for this query and its declared scope; zero requires a source complete enough to justify it. |
| `CENSORED` | Only a range or threshold-derived bound is justified. Missing does not mean zero. |
| `UNAVAILABLE` | The source/query cannot support an interpretable value; abstain from that inference. |

The complete context denominator must be separately marked known or unknown. A sum of retained n-grams cannot be presented as the full denominator. Nor can aggregating retained surface forms reconstruct a complete lemma distribution.

Comparisons require compatible source scope, normalization and units. Conservative count-ratio bounds may be used when their bounds are valid; they are not semantic proof. For different-length phrase replacements, comparing whole-phrase raw counts alone is not a valid acceptance rule.

### 8.2 Resource selection and manifests

PLAN identifies Gigafida frequency/n-gram resources, Sloleks and potential collocation/linguistic-analyzer support. Those are inputs to verify, not bundled data or proof of current access. In particular, PLAN's approximate 2-per-million n-gram cutoff is a warning about a reported release, not a hardcoded threshold for every future source.

Every imported index requires a manifest containing source identity/version, acquisition reference, checksum, rights/license status, format, thresholds, completeness, normalization/tagging conventions, importer version and deterministic build parameters. Preserve attribution and redistribution conditions. Public query access does not authorize bulk extraction or redistribution.

Store only available sparse records. Candidate-middle-word indexes must retain the same uncertainty metadata as ordinary trigram lookups. No runtime corpus scraping is needed. Large indexes, model weights and private evaluation corpora stay out of Git; permitted miniature synthetic fixtures are clearly labelled as such.

## 9. CPU detection and target selection

CPU detection produces suspicion, not automatic correction. Signals may include unigram/lexicon status, adjacent bigrams, neighboring trigrams, fixed-neighbor alternatives, lemma evidence and optional contextual morphology or collocations.

Treat an unknown form, rare complete phrase or unusual name as a reason for investigation only. Weakly represented surroundings are not evidence that the middle word is wrong. A trigram alarm may identify a short construction rather than an unambiguously wrong middle token.

Select a finite number of original-coordinate targets. Nearby alarms may be grouped into a short phrase **before review**, without crossing protected boundaries or growing to an unrestricted sentence/paragraph. Sort selected targets deterministically. Excess or ambiguous targets remain unchanged with bounded internal reason codes.

Separate lexical misuse from morphological disagreement. Required morphology comes from context and analysis confidence; do not insist that the replacement copy the tags of a form that is itself wrong. Ambiguous lemma/tagging evidence may cause abstention.

Do not give the reviewer ranked corpus replacements by default. Preserve its narrow independent reconsideration of the expression, while recognizing that the same generating model is not statistically independent of itself.

## 10. Isolated Qwen review

### 10.1 Reviewer question

Preserve this question and the surrounding abstention requirements from PLAN §8:

> Ali se ti zdi uporaba besede oziroma besedne zveze X najboljša naravna izbira v tem slovenskem stavku? Če ne, s čim bi jo nadomestil?

Ask the reviewer to keep acceptable wording, reject mere stylistic preference, preserve meaning/register/grammar, avoid factual correction and report when a wider edit is necessary. It receives the completed target sentence and bounded neighboring context, not the whole main history.

The reviewed material is data. Instructions embedded in the response must not become reviewer authority. Delimiting a prompt is not sufficient enforcement: strict output parsing, fixed IDs and local patch validation establish the executable boundary.

### 10.2 Request isolation

Build fresh request messages and explicit review settings. Do not reuse a mutable main-history object. Do not include `previous_response_id`, main server-managed conversation/session linkage, tools, images, main tool results, project constitutions or context-reconstruction instructions. Keep protocol-required authentication separate from conversation state.

Call the already configured private reviewer route directly; never call the public repair endpoint from itself. The endpoint must be operator-controlled and tests must record both outbound main and review shapes using synthetic data to prove isolation.

A thread, process or asynchronous task is an implementation mechanism, not the context-isolation guarantee. The same model may repeat its mistake; neither repeated agreement nor a `confidence` value establishes independent confirmation.

### 10.3 Structured output

The selected initial schema follows PLAN §8: one result per supplied ID, with `keep`, nullable `replacement`, `needs_wider_edit`, and optionally a bounded self-reported `confidence`. Exact field/version names are engineering choices to pin in the implementation order.

```text
keep=true  -> replacement=null
keep=false -> replacement is nonempty; needs_wider_edit=false
needs_wider_edit=true -> keep=true; replacement=null
```

Unknown, duplicate or missing IDs, invalid JSON, invalid field types, contradictory fields and oversized output reject the whole batch. Do not silently salvage malformed output or add another model call to repair its JSON. One structurally valid but unacceptable replacement can be rejected individually during acceptance.

The model returns only the local replacement, never the rewritten sentence or complete answer. A request for a wider edit leaves that target unchanged in this pass. Server-constrained output is optional until actual compatibility is verified; do not reconfigure the protected model server merely to obtain it.

## 11. Acceptance policies

### 11.1 Initial modes

| Mode | Model calls and user-visible behavior |
|---|---|
| `detect_only` | CPU only; return original. |
| `shadow` | Eligible targets may be reviewed and scored; return original; inspect results only through approved evaluation channels. |
| `strict` | Apply only fully validated `AUTO_REPAIR` proposals. |
| `experimental` | Future explicitly configured/evaluated alternatives; not automatically enabled or required for MVP. |

The development sequence is `detect_only`, then `shadow`, then measured limited `strict` use. If a response has no eligible suspicion, even `shadow` and `strict` make no review request.

### 11.2 Strict acceptance

Require all applicable conditions: CPU-selected target; valid local proposal; target equality and non-protected bounds; configured size/structure limits; appropriate independent corpus/lexicon/morphology evidence; no detected contextual or semantic contradiction; and a valid composed result.

Different error classes may need different evidence rules. A malformed form can rely on valid-form, orthographic and contextual evidence; replacing one valid lexeme with another needs stronger contextual support. More frequent does not automatically mean more correct. Neutral or incomparable data is insufficient for strict lexical acceptance.

Reject identity replacements as no-ops. Reject forbidden newlines, control/markup/code structure, overlong replacements and any expansion outside the original authorized span. Do not normalize adjacent punctuation or formatting as an unreported side effect.

`LLM_CONFIRMED_REPAIR` without sufficient independent evidence remains disabled for automatic user-text changes in the MVP. A higher model confidence threshold alone cannot enable it. Proposals may be studied in shadow evaluation without changing the product's strict authority boundary.

## 12. Exact patching and composed validation

The original string stays immutable until final composition. Validate each selected original slice immediately before applying edits. Reject overlapping or otherwise incompatible edits; do not silently select the last one.

Construct the final result from untouched original slices plus approved replacements, or use an equivalently tested descending-offset implementation. Preserve everything else exactly. No detokenization, Markdown renderer or model response may replace the original document.

After composition, recheck affected local contexts and sentences. If adjacent individually acceptable changes conflict, reject their conflict group and rebuild from the original. This remains bounded CPU validation, not a new generative pass. No surviving edits means exact original text.

Text equality and HTTP-byte equality are distinct. On a true pass-through path preserve the original envelope bytes where possible. On a changed-text path serialize only the supported envelope transformation and account explicitly for affected metadata.

## 13. HTTP and main-history integration

Start with one explicitly supported nonstreaming text shape and one response choice. Select and test the actual endpoint/envelope during the appropriate work order; this document does not assert universal Chat/Responses compatibility.

Reject unsupported request capabilities before main generation where possible, or use an explicitly configured unchanged bypass route. Unknown response structures are not repaired. No silent JSON response under an SSE contract, no rewriting tool results and no accidental public bypass for internal controls.

The upstream may stream internally, but the adapter accumulates it under a hard bound and validates completion before CPU analysis. No provisional answer text reaches the user. Future delayed SSE support must synthesize a protocol-correct consistent final event sequence and requires separate tests; it does not reduce time to first answer content.

For client-managed conversation history, the next main turn contains the final answer visible to the user, not an additional original draft and never the review prompt/JSON. The library itself owns no conversation store. Server-managed response/conversation chaining is unsupported until there is a verified way to keep displayed and stored answers consistent.

Changed text invalidates original token-aligned probabilities and potentially annotations/offsets. Initially reject or bypass such repair requests under the declared capability policy. Do not silently keep stale `logprobs`, fabricate probabilities, or claim offset-bearing annotations still align.

Maintain original-generation usage separately from review usage. Counting tokens in the final patched string does not measure either actual inference bill. Integration must make review cost visible to the operator without silently misrepresenting upstream usage semantics.

## 14. Bounded resources, cancellation and fallback

### 14.1 Selected initial defaults

These follow PLAN §13 as initial configurable engineering defaults, not measured optima or immutable product limits:

| Setting | Initial value |
|---|---|
| Review requests per response | At most 1. |
| Generative review passes | 1. |
| Automatic review retries | 0. |
| Concurrent review requests from this component | At most 1. |
| Targets per response | At most 8. |
| Target length | Normally at most 6 words, with a finite character bound. |
| Replacement length | At most 8 words, with a finite character bound. |
| Automatic evidence-insufficient acceptance | Disabled. |
| Persistent production text logging/storage | Disabled. |

Implementation orders must select finite bounds for capture bytes, analysis length, context per target, total prompt/output, queue length/waiting time and total review time. These bounds belong in validated versioned policy; do not fabricate target-machine throughput to set them. CPU work must not block the HTTP event loop indefinitely or continue unbounded after cancellation.

### 14.2 Failure contract

| Condition | Required result |
|---|---|
| No eligible suspicion | Original; zero review calls. |
| Corpus missing, corrupt or incompatible | Degraded original; no invented counts. |
| Analysis size exceeded after safe capture | Original without analysis. |
| Review queue full, timeout, transport failure or invalid batch | Cancel owned optional work and return completed original. |
| Individual proposal fails evidence or structure | Reject that proposal; process remaining valid independent proposals under policy. |
| Composed edits conflict | Reject affected group and rebuild from original. |
| Main generation errors or is incomplete | Preserve documented error/finish semantics; do not repair or hide incompleteness. |
| Hard capture limit exceeded | Bounded API failure, never truncated text labelled complete. |
| Client disconnect | Cancel owned upstream/review tasks and stop delivery; do not create background repair. |

Optional linguistic fallback is not permission to bypass authentication, request/response validation, hard limits or isolation. Internal reasons use a finite safe vocabulary and do not expose text or secrets.

## 15. Security, privacy and protected environment

Treat main output, review output, local evaluation files and downloaded corpus content as data. Do not execute embedded instructions, paths, URLs or code. The reviewer has no tools and no authority to write files or mutate conversation state.

Keep credentials outside Git and use explicit environment/config references without logging values. Private text is not a metric label, cache key exposed to logs or an OAP report excerpt. Production metrics contain bounded counts, timings, policy/source versions and reason labels only.

Real evaluation examples require explicit permission and controlled storage. Human annotation, private evaluation inspection and production logging are distinct channels. Test fixtures in Git must be permitted and clearly synthetic or deliberately published. Cross-user text caching is unnecessary for MVP.

The existing Qwen service, model/quantization files, vLLM/CUDA environment, launch flags, port ownership, shared GPU allocation, gateway and neighboring adapters are protected resources. Neither bootstrap generation nor an ordinary product order authorizes their mutation. Exact endpoints, model IDs and compatibility must be verified later by bounded read-only/opt-in tests.

No live service is required for bootstrap structural validation or offline product development. Passwordless sudo or a full-access CLI does not grant deployment, data-acquisition or publication authority.

## 16. Verification and evidence layers

### 16.1 Software contracts

Test all invariants with miniature synthetic data and deterministic reviewer fakes before live model use. Required tests include:

| Area | Evidence required |
|---|---|
| Capture | Full completion before analysis/review/delivery; errors and truncation remain visible. |
| Isolation | Inspect exact main/review request shapes; no shared history mutation, tools, session linkage or recursion. |
| Original mapping | Repeated substrings, Unicode/combining marks, emoji, CRLF, Markdown and immutable original slices. |
| Protected spans | No edits or artificial n-gram adjacency across excluded material. |
| Corpus | Exact zero versus censored absence, unknown denominator, incompatible normalization/source scope. |
| Reviewer | Keep, replacement, wider-edit response, prompt injection as data, duplicate/missing/unknown IDs, invalid/oversized JSON. |
| Acceptance | Common-but-wrong alternatives, mere style changes, weak evidence, phrase-length comparison and morphology uncertainty. |
| Patching | Overlap, stale offsets, nearby conflicts, exact untouched content and no-edit equality. |
| Operations | Zero/one review count, bounded queue, timeout, cancellation, tenant/request separation and no raw logging. |
| API | Explicit supported envelope, unsupported capabilities, finish status, usage and history consistency. |

The governance/orchestration guards specified by INSTRUCTIONS are executable bootstrap tests, not substitutes for these later product tests.

### 16.2 Live compatibility

Live tests are explicit, low-concurrency and bounded. Record verified model/endpoint capabilities and actual call sequencing without changing the host or exposing credentials. A skipped live test is not a pass. Synthetic fake-upstream success does not establish Qwen quality or serving compatibility.

### 16.3 Linguistic evaluation

Follow PLAN §14: real target-model outputs, correct-text negative controls, human labels that distinguish error from stylistic preference, frozen calibration/held-out splits and meaningful denominators. Do not tune on the held-out set or allow the generating Qwen to be the final judge of its own correctness.

Report accepted-edit precision, harmful edits per originally correct words, unnecessary style edits, detection versus repaired coverage, review-call rate, actual usage, latency and resource/failure behavior. Report sample sizes and uncertainty. The approximate 99% precision and one harmful edit per 10,000 correct words are goals, not results or self-executing release permission.

An implementation that mostly abstains is not automatically successful: demonstrate useful measured benefit as well as limited harm. Conversely, low coverage is not a reason to weaken evidence gates merely to produce a more impressive demonstration.

## 17. Concentrated OAP operating architecture

The bootstrap generator runs in a third directory and installs the two operational
workspaces without activation. REPO_ROOT/AGENTS.md routes by an explicitly selected
role. The dense coding constitution is behind that router. STRATEGIC_HOME/AGENTS.md
is the full strategic constitution; a strategic agent inspecting the coding repo
does not become the executor.

HWP comprises this architecture, role constitutions, SECURITY, TESTING, readiness,
D0/D1/D2 policy, detailed roadmap and inert initial orders, runtime constraints,
recovery and critical-register schema. HJP requires forced provisional D1 decisions,
not repeated routine human interruption. DHA retains exact human gate ownership.

Every final order has durable H/A/E/I/C provenance, explicit scope/non-goals,
observable boundary-faithful evidence and `Decision: NONE` or an exact strategic
`APPEND CRIT-NNNN` payload. Mechanical enforcement validates structure; strategy
owns semantic classification. Coding only reports candidate dilemmas or performs
exact ordered appends. Strategy alone reviews and may merge development PRs after
current-head required checks and independent evidence review.

One numeric objective is one PR. Corrective suffixes amend it. A process or context
reset does not create another objective/order. Orders and final reports are durable;
FIFO is synchronization only. The selected exact transport, suffix, locking and
SELF-publication contracts are defined by the bootstrap protocol specification,
then encoded in runtime role-specific communication files and tested helpers.

Concentrated OAP permits development merge, not deployment or release authority.
A merge that itself deploys to production crosses D2 and needs human authorization.
No bootstrap or routine development action changes the protected Qwen environment.

## 18. Deferred judgment and deliberate CRITICAL loading

Root CRITICAL is mandatory but is not routine model context. Its current canonical
rules and exact five-condition threshold come from the supplied Concentrated OAP
chapter. D0 continues normally. D1 requires investigation, a best provisional
choice, containment, evidence, exact registration and continued safe work. D2 stops
before the real boundary; independent safe work may proceed.

Coding may append only exact strategic-authored bytes in implementation work,
**before** capturing the implementation SHA, never inside the final report-only
commit. Prior entries remain intact. Agents may add ordered mitigation/evidence,
not purported human acceptance. Human dispositions are exactly ACCEPTED, REJECTED,
CHANGE REQUIRED and DEFERRED. Only latest attributable human ACCEPTED clears the
registered gate; mitigation or a superseding implementation does not.

CRITICAL is not for ordinary bugs, TODOs, failed tests, setup prerequisites or
speculative concern. Absence of a safe provisional path is not solved by inventing
an entry. Development and relevant deployment gates are checked separately; the
register never supplies otherwise missing human authority.

## 19. Milestones, progress and Independent Closure Audit

PLAN §15 defines product phases; the bundled work-program specification expands
56 initial objectives. Duration estimates are planning estimates, not timers or
claims. Code production, diagnostic work and documentation have distinct progress
axes: functionality, evidence confidence, uncertainty reduction, debt/attack-surface
reduction and capability breadth.

| Milestone | Initial objective range | Closure condition |
|---|---|---|
| Demonstrator | 000–022 | PLAN D01–D07 evidence, fresh ICA and an honestly scoped human milestone decision. |
| Experimental MVP | 023–044 | PLAN M01–M07 and all eight §16 criteria; fresh ICA on current merged main; no self-certification. |
| Verified service | 045–055 | PLAN S01–S05 evidence and applicable human gates; repeated independent closure audit. |

All 56 rows are an initial coverage hypothesis, not a completeness proof. Before
MVP complete, release candidate or another architecture-defined closure claim,
require an **Independent Closure Audit (ICA)**. Use a fresh isolated model/context
or independent human/audit agent. Start from human scope, full architecture and
current merged main, not the strategist's completed queue or claimed percentage.

Classify every requirement IMPLEMENTED, PARTIAL, ABSENT or UNPROVEN. Link actual
runtime paths, entry points, negative tests and evidence at an exact revision.
Reports/README/CI summaries are claims until corroborated. A green test exercising
a replacement of the boundary under test cannot certify the real boundary.

Translate gaps into provenance-linked bounded work and repeat ICA after remediation.
The audit does not merge code or authorize deployment. Strategy recommends closure;
human retains the final milestone label and release/deployment judgment. Preserve
observations and explicitly supersede false interpretations rather than rewriting
old reports.

## 20. Bootstrap acceptance versus product acceptance

Bootstrap acceptance proves populated inactive workspaces, complete role-correct
instructions, source-preserving full/compact architecture, the empty canonical
register, detailed drafts, tested helpers, recovery and context-loading separation.
It does not prove the application, linguistic benefit or a live Qwen result.

Future product acceptance needs all eight PLAN §16 criteria and the relevant
independent audit. Source rights, actual model compatibility, text quality and
resource measurements remain measured prerequisites, not made-up successes.
Human deployment authorization and applicable DHA dispositions remain separate
from development merge and from a successful ICA.

## 21. Source and revision notes

Product sections 2–16 are preserved verbatim from architecture 1.0. Revision 1.1
changes only governance framing/§1 and §§17–21 to implement the owner's role-router,
dense coding/full strategic requirements and the two subsequently supplied OAP
chapters. PLAN is unchanged.

The primary process sources are the owner's attached `concentrated-oap.md` and
`oap.md`, preserved in the input package under `sources/` and installed as immutable
reference snapshots under `docs/bootstrap/sources/`. Their hashes and exact section
mapping are in the package SOURCE-MAP. Reading these attachments is not a claim
of successful live-site retrieval.

The previously inspected local-coding implementation supplies workflow precedents
for separate workspaces, fresh coding rounds, compact architecture and exact
FIFO/SELF mechanics. It does not define this product and does not already implement
the owner's new minimal-root-router design. Concrete project extensions and their
source distinctions are recorded in the bootstrap specifications.

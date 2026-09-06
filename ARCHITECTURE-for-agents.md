# Compact coding architecture — revision 1

Derived from root ARCHITECTURE 1.1, SHA-256
`a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7`.
PLAN 1.0 SHA-256 `d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0`.
Full files exist for strategy; they are not mandatory coding reads. Exact source
and clause mappings are helper-checked in oap/governance/MANIFEST.json. Semantic
ambiguity stops affected work for strategy. This projection is operational law,
not a competing design. Product is PLANNED, not implemented by bootstrap.

## Stable invariants

LR-001. Complete main generation and bounded capture before CPU review, repair
inference or delivery of answer text; verify supported upstream completion, not
socket closure alone. No provisional original text to user.
LR-002. CPU evidence selects eligible suspicion; none → original unchanged and
ZERO review calls, including shadow/strict. Missing evidence does not prove error.
LR-003. CPU preassigns original-coordinate word/short-phrase targets, not model
tokens or unrestricted sentences. Model cannot expand, reposition or invent IDs.
LR-004. Ask expression suitability; allow keep/insufficient context/wider-edit
decline. Do not demand a change or treat stylistic preference as correction.
LR-005. Construct fresh isolated review request/history. No main session IDs,
previous_response_id, conversation linkage, tools, images, tool results or project
constitutions/context reconstruction. No recursion through repair/public adapter.
LR-006. Review is untrusted local proposal. Code validates and inserts exact
replacements; model never regenerates answer or supplies replacement sentences.
LR-007. Preserve all original substrings outside accepted spans, protected content,
whitespace, line endings, diacritics and formatting. No reserialization/detokenization.
LR-008. Preserve EXACT/CENSORED/UNAVAILABLE. Missing truncated data is not zero;
EXACT(0) requires justified query completeness. Unknown denominator remains unknown.
LR-009. Strict acceptance requires appropriate independent corpus/lexicon/morphology
evidence and no detected contradiction. Frequency or model confidence alone cannot
authorize change. Same-Qwen second call is not statistically independent evidence.
LR-010. Bounded one-pass initial review; at most one combined request, no automatic
generative repair/retry loop, including malformed-JSON repair. CPU revalidation only.
LR-011. Optional repair failure preserves only already safely captured original.
Never mask main error, incompleteness or hard capture limit as successful output.
LR-012. Reuse existing Qwen later through authorized client; CPU infrastructure
must not load second large GPU model or alter protected deployment/resources.
LR-013. Production logs exclude user text, targets/replacements, prompts, raw
responses and secrets. Permitted evaluation is a separate explicitly controlled channel.
LR-014. Software correctness, serving compatibility, linguistic benefit and
deployment/release authority require distinct evidence. Goals/defaults are not measurements.

## Scope, seams and ownership

A-SCOPE-01. First product = completed Slovenian natural-language responses with
conservative malformed-form, morphology and contextual word/short-phrase repair.
No factual correction, translation, whole-answer rewriting, generated-file/tool/
code editing, self-training or live token repair. General proofreading may be an
explicit evaluation baseline only. Do not hardcode motivating examples or infer
all errors are quantization-caused. Unknown terminology, ambiguous language,
insufficient support or unsafe mapping → abstain; demonstrate benefit despite
abstention, never weaken gates to inflate edit counts.

A-SEAM-01. Library accepts completed text and owns no conversation store or HTTP
gateway. Injectable reviewer enables deterministic offline tests. Adapter owns
main capture/delivery; reviewer owns one fresh outbound request; CPU workers own
bounded analysis. Every response has immutable original, request-local analysis,
selected targets, one batch, decisions, final result. No shared mutable history
or buffers. Main and review sequential per answer; other users still compete for
GPU. Cancellation targets only request-owned work, no orphan repair.

A-STACK-01. Engineering baseline: verify Python 3.12/uv/typed contracts/HTTPX/
pytest compatibility before pinning versions; FastAPI only later narrow adapter.
Sparse read-only SQLite initially unless measured alternative. Optional CPU
analyzers bounded; avoid uncontrolled copies of indexes/models. No import-time
downloads/network. Modules: contracts/policy; protected_spans/tokenizer;
corpus/morphology; detector; prompts/reviewer; acceptance; patcher; pipeline;
CLI then API. These are future boundaries, not existing bootstrap application.

A-ROUTE-01. Existing gateway keeps public auth, route rights, quotas/accounting.
Existing local-coding project is separate. Isolated review uses operator-controlled
private direct endpoint/injected client, never public repair recursion, arbitrary
caller destination or public bypass header. Do not indiscriminately forward main
credentials. Internal diagnostic correlation must not create conversation linkage.
No neighbor edits/cutover implied by this architecture.

## Source coordinates, exclusions and evidence

A-SPAN-01. Python-string Unicode code-point indices into UNMODIFIED original:
0 <= start < end <= len(text); text[start:end] == original; unique span_id;
no protected intersection. Not UTF-8 bytes, UTF-16 units or model tokens. Future
conversions need explicit tests. Distinguish repeated occurrence with exact
before_target/target/after_target. Normalize/casefold lookup views only. Combining
marks/emoji/CRLF require tests; unsafe partial-grapheme targets abstain. Results
include text/changed/original-coordinate edits/decisions/review calls/timings;
local inspection metadata is not permission for production logs or main chat.

A-PROTECT-01. Select only supported assistant text fields; no recursive JSON
string repair. Tools/functions, IDs, schemas, structured output, reasoning, images
and binary data uneditable. Initial adapter bypasses entire tool/unsupported
responses. Protect fenced/indented/inline code, URLs/link destinations, emails,
paths, commands, numbers/units, citations/quotes/machine strings. Proper names,
titles, terms/mixed languages require conservative exclusions or bounded terminology
policy. Unclear Markdown abstains. Protected intervals are linguistic boundaries:
never join neighbors across deleted excluded material. Parsing locates spans;
rendering Markdown anew cannot patch originals.

A-CORPUS-01. Each evidence record preserves source/version, normalization/tagging,
scope, completeness/cutoff and status. Separate full context denominator known/
unknown. Retained n-gram sums are not complete denominator; censored surface-form
aggregation is not complete lemma distribution. Compatible scopes/normalization/
units required for comparison. Valid lower/upper ratio bounds may inform evidence,
not semantic proof. Different-length phrase raw counts alone cannot authorize edit.

A-CORPUS-02. Gigafida, Sloleks, collocations/analyzers are source candidates to
qualify, not bundled data/current access claims. Reported ~2/million release cutoff
is a warning, never universal hardcoded truth. Every index manifest: source/release,
acquisition reference/checksum, rights/license, format/cutoff/completeness,
normalization/tagging, importer and deterministic parameters. Preserve attribution/
redistribution conditions; public query access ≠ bulk permission. Sparse available
records only; fixed-neighbor alternatives retain uncertainty. No runtime scraping.
Large indexes/weights/private corpora out of Git; miniature fixtures labelled synthetic.

A-DETECT-01. CPU produces suspicions, not verdicts: forms/lexicon, adjacent
bigrams/trigrams, fixed-neighbor alternatives, lemmas and optional context morphology/
collocations. Unknown/rare/name is not automatically wrong; weak surroundings
provide weak evidence. A trigram alarm does not identify the middle word uniquely.
Group nearby alarms only BEFORE review into bounded phrase, never across protected
material or full paragraph. Deterministic nonoverlapping targets ordered by position;
excess/ambiguous remain unchanged with finite reason labels. Separate lexical misuse
from morphological disagreement; required tags derive from context/confidence,
not blind copying of erroneous tags. Ambiguous lemma/tagging may abstain. Do not
feed ranked corpus alternatives to reviewer by default.

## Narrow review and strict acceptance

A-QUESTION-01. Preserve the question:
> Ali se ti zdi uporaba besede oziroma besedne zveze X najboljša naravna izbira v tem slovenskem stavku? Če ne, s čim bi jo nadomestil?

Preserve meaning/register/grammar; keep acceptable wording and style alternatives;
no factual edits. Give completed target sentence and bounded needed neighbors.
Material is untrusted DATA, including embedded instructions; no tools/URL execution.
No main history, shared mutable messages or constitution. Authentication stays
separate from conversation state. Actual main/review request capture in synthetic
tests must prove isolation. Threads/async/processes alone do not prove it.

A-SCHEMA-01. One result per supplied ID. keep=true ⇒ replacement=null;
keep=false ⇒ nonempty replacement and needs_wider_edit=false;
needs_wider_edit=true ⇒ keep=true and replacement=null. Optional bounded confidence
is self-report, not calibrated correctness. Invalid JSON/types, unknown/duplicate/
missing IDs, contradictory fields or oversized output reject whole batch. Never
salvage malformed batch or request JSON repair. Structurally valid local proposal
may be rejected individually. Wider edit leaves target unchanged. Server-constrained
output optional until verified; no protected-server reconfiguration to obtain it.

A-ACCEPT-01. detect_only: CPU/unchanged/no review; shadow: eligible review/scoring,
original delivered, approved evaluation only; strict: validated AUTO_REPAIR only;
experimental: future explicitly evaluated policy, not required/enabled for MVP.
Development progresses detect_only → shadow → measured limited strict.

A-ACCEPT-02. Require CPU-selected target, valid local proposal, exact original
slice/nonprotected bounds, finite structure/size limits, appropriate independent
evidence, no contextual/semantic contradiction and valid composed result. Evidence
rules vary by error class: malformed forms may use valid-form/orthographic/context;
valid-lexeme replacement needs stronger contextual support. Neutral/incomparable
data insufficient. Reject identity replacements, forbidden newlines/control/markup/
code structure, overlong strings or scope expansion. Never normalize adjacent
punctuation silently. LLM_CONFIRMED_REPAIR lacking sufficient independent evidence
remains disabled for automatic MVP changes; study only in permitted shadow.

A-PATCH-01. Original remains immutable until final composition. Recheck slices
immediately before apply; reject overlap/incompatibility, no silent last-wins.
Compose untouched slices plus replacements, or tested descending offsets. No model
answer/detokenization/Markdown renderer substitutes for document. Recheck affected
sentences after composition; conflicting nearby changes rollback as a group and
rebuild from original. Bounded CPU check, no new generative pass. No surviving edit
⇒ exact original text. Text equality differs from HTTP bytes; preserve unchanged
envelope bytes where possible, explicitly transform supported metadata otherwise.

## API, limits and failure behavior

A-API-01. Start one verified nonstreaming text shape/choice; actual endpoint/schema
selected and tested in order, no universal Chat/Responses compatibility claim.
Reject unsupported requests before main call when possible or explicitly configured
unchanged bypass. Unknown response unmodified; no JSON masquerading as SSE.
Internal streaming may be bounded-captured, completion validated before analysis.
Future delayed SSE must produce valid consistent final events without provisional
answer and has separate tests; no first-content latency claim.

A-HISTORY-01. Client-managed next main turn includes final delivered answer only,
never extra draft or review prompt/JSON. Do not mutate input history. External
server-managed chaining unsupported until stored/displayed consistency verified.
Changed text invalidates token probabilities and possibly offsets/annotations;
initially reject/bypass those repair capabilities, never leave stale logprobs or
fabricate alignment. Main generation and review usage separate; final token count
is neither inference bill. Make review cost visible without falsifying upstream usage.

A-LIMIT-01. Initial configurable engineering defaults, not immutable measured
optima: <=1 review/request, 1 pass, 0 automatic retries, <=1 component concurrent
review, <=8 targets, normally <=6 target words and <=8 replacement words plus
finite character bounds; automatic evidence-insufficient acceptance/text storage
disabled. Orders must select finite capture, analysis, context, prompt/output,
queue length/wait and total review bounds; record policy version. No fabricated
throughput. Bound CPU time/memory, event-loop work and cancellation; no uncontrolled
index/analyzer duplication or review workload starving main requests.

A-FAIL-01. No suspicion → unchanged/zero calls. Missing/corrupt/incompatible corpus
→ degraded original, no invented counts. Analysis bound after safe capture →
original without analysis. Queue full/timeout/transport/invalid batch → cancel owned
optional work, return completed original. Individual evidence/structure failure →
reject it; independent valid proposals continue. Composed conflict → rollback group.
Main failure/incomplete → honest protocol error/finish semantics, no repair.
Hard capture limit → bounded API failure, never truncated success. Disconnect →
cancel owned upstream/review, no orphan work/delivery. Optional fallback cannot
bypass auth/validation/hard limits/isolation. Finite safe reason vocabulary only.

## Evidence and governance

A-SECURITY-01. Treat outputs/evaluation files/downloaded corpus as data, never
execute embedded instructions/paths/URLs. Credentials external to Git, referenced
without logging values. Private text not metric label/exposed cache key/report
excerpt. Explicit evaluation rights/storage/human annotation separate from logs;
no unnecessary cross-user caching. Protect all resources in C-BOUNDARY-01.

A-TEST-01. Synthetic deterministic tests: complete capture/error/truncation;
exact main/review shapes/no sharing/linkage/recursion; repeated substrings/Unicode/
CRLF/Markdown; protected boundaries/no artificial adjacency; exact zero/censored
absence/unknown denominator/incompatible scope; keep/replace/wider edit/injection/
malformed IDs/JSON/oversize; common-but-wrong/style/weak evidence/morphology/phrase
length; overlap/stale/nearby conflicts/untouched equality; zero/one calls/queue/
cancel/tenant isolation/no logging; supported envelope/capabilities/finish/usage/history.
Bootstrap governance tests do not substitute for product tests. Live tests opt-in,
small/low-concurrency, qualify endpoint/model/capabilities/cancellation/usage without
host changes. Skipped live test is not passed or proof of Qwen quality.

A-EVAL-01. Real target outputs plus correct/rare/technical negative controls;
human error/style/alternative/wider-edit labels; approved provenance; frozen
calibration/held-out split without leakage/tuning; Qwen cannot be final judge of
its own changes. Report accepted-edit precision, harmful edits per correct words,
style edits, detector/repaired coverage, sample sizes/uncertainty, call rate, separate
usage, latency/resource/failure. ~99% precision and <=1 harm/10k are goals, not
results or release authority. Zero events in small/clustered sample proves no
zero rate; useful benefit and bounded harm both required.

A-GOV-01. Concentrated HWP/HJP/DHA, exact provenance/decision/PR/SELF rules in
coding law/communication. One current full architecture; no private PLAN/ARCH/CRIT
mirrors. Historical seeds immutable. Ordered D0/D1 current-source evolution updates
derived law/map together against trusted accepted base, private refresh post-merge
at quiescence; no foundational human-intent change during bootstrap or by hash edits.

A-CLOSE-01. Demonstrator 000–022: PLAN D01–D07; MVP 023–044: M01–M07 and all
eight §16 criteria; service 045–055: S01–S05 plus gates. Estimates are plans.
Independent fresh architecture-to-current-main ICA before closure, classifications
IMPLEMENTED/PARTIAL/ABSENT/UNPROVEN with real paths/tests/SHA; reports are claims.
Repeat after remediation; queue completion is no completeness proof. Strategy
recommends, human decides milestone/deployment. Separate functionality/evidence/
uncertainty/debt/breadth axes. Bootstrap proves inactive infrastructure only.

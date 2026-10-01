# PROTOCOL-009 REVISION 012 (additive) - amendment of the registered
# SCAFFOLD_GENERATION call class; stage-1 recovery clause - 2026-10-02

Status: REGISTERED. Committed byte-exact by order 011-e BEFORE any
live call. Additive: PROTOCOL-009.md remains byte-frozen (sha256
cc5e9089510dcb4be6fd2ec3cef1890c515ec9e6edd585da1dd25e70e1dabd2a);
PROTOCOL-009-REVISION-011 (sha256
609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43,
19,049 B) remains byte-frozen; this revision supersedes ONLY the
named call-contract parameters of its section 8 and nothing else:
(i) the "output-token cap 600" clause of the call contract; (ii) the
absence of a reasoning-effort pin (the REVISION-011 payload left the
effort to the server default, then the 011-d driver probed values);
(iii) the budget clause (re-registered per round, below). Every
other element of PROTOCOL-009 and of REVISION-011 (population,
mechanical assembly, PRNG mechanics, selection, partition, ground-
truth rule, span-correspondence matcher, discard rule, score
scoping, labeler tasking, comparators, metric families, stopping
rules, (m) failure decomposition, (n) no-tuning, data rights) is
UNCHANGED.

## 1. Recorded finding (evidence for the amendment)

011-d (first collection round) BLOCKED truthfully at the pre-
declared floor-50 gate: 134/134 selected documents excluded by
failed terminal scaffold attempts (135 calls: 134 terminal attempts,
one per document, plus 1 standalone diagnostic; budget 135/402).
- 8 x HTTP 200 incomplete (documents 011b-0001..0008): under server-
  default effort xhigh (2) and effort low (6),
  incomplete_details.reason = max_output_tokens with
  usage.output_tokens = 600 = the full registered cap, of which
  output_tokens_details.reasoning_tokens = 600 - the entire cap was
  consumed by reasoning with zero message content. The 8 raw
  responses are stored verbatim privately (0600), never committed.
- 127 x HTTP 400 (documents 011b-0009..0134 + the diagnostic): the
  probed effort "minimal" is rejected; the server's verbatim
  message: 'Unexpected reasoning effort minimal. Supported types
  are xhigh (default), medium, and low.'
Finding: on this deployment (vLLM 0.28.0; qwen3.8-27b;
Qwen3.8-27B-FP8; the E2(b)-designated A100-FP8 regime as verified at
011-c) the model's reasoning overhead on the registered scaffold
task exceeds 600 output tokens at every supported reasoning effort
(supported set: xhigh / medium / low; minimal UNSUPPORTED), so the
registered 600-token output cap structurally prevented scaffold-
section completion. Corroboration: the frozen 007-m evidence base
holds 1,901 stored completed responses at effort low with reasoning
of 16-4,417 tokens under no output cap.

## 2. Superseded element: section-8 call-contract parameters

- Output-token cap: 600 -> 8,192. Rationale (data-free): 8,192
  bounds (a) the registered scaffold message budget (150-250 words
  ~ <= 500 message tokens) plus (b) the observed low-effort
  reasoning maximum of 4,417 tokens in the frozen 007-m corpus
  (1.85x margin), plus the 600 observed on this task class before
  truncation. The cap is a ceiling, not a target.
- Reasoning-effort pin: the scaffold payload carries the reasoning
  effort field pinned to "low" - the same field value as the frozen
  007-m main-capture contract (configuration pin
  0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26).
  "low" is supported (measured HTTP 200 in 011-d) and is the
  frozen-method effort. "xhigh" (server default) and "medium" are
  supported but MUST NOT be used for scaffold calls; "minimal" is
  UNSUPPORTED (HTTP 400; verbatim message in section 1) and MUST
  NEVER be sent. Sending any effort value other than "low" (or
  omitting the field) is a driver defect, not a registered variant.
- UNCHANGED within the call contract: one fresh isolated request
  per section on the designated target only; Responses wire API,
  non-streaming; NO main history, NO session linkage, NO tools, NO
  images, NO constitutional-adapter recursion (S-PRODUCT-02);
  profile (both bases + bearer) read ONLY from the private
  011b-identity credentials receipt (the sole profile source; never
  committed, logged, or echoed); 300 s timeout; 2,000,000-byte
  response bound; ONE terminal attempt; NO resampling, NO retry;
  response handling (store verbatim privately, 0700/0600, never
  committed; strip exactly one trailing LF; strip exactly one outer
  code-fence pair iff the first and last lines are exactly three
  backticks with nothing outside; otherwise as received; failure or
  empty processed section -> document EXCLUDED, failure named, no
  replacement, no re-sampling, counted operationally); the
  registered prompt (byte-exact, 402 B,
  005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc)
  and the registered 12-topic list.
- Budget (re-registered per round): each collection round that
  issues scaffold calls carries an explicit per-round cap. The 011-
  e recovery round's cap: at most 402 terminal scaffold attempts
  (134 documents x up to 3 sections per the committed per-document
  k) plus 1 standalone diagnostic. The 135 calls consumed at 011-d
  are accounted under the REVISION-011 cap and are NOT charged
  against the 011-e cap.

## 3. Stage-1 recovery clause (order 011-e)

- The committed selection, draws, per-document assembly draws (k,
  topics, layout), collection IDs, and partition (pilot 5 /
  calibration 20 / confirmation 109) from the 011-d-committed
  manifest STAND unchanged. NO re-selection, NO re-draw, NO
  replacement records, NO renumbering. The 134 exclusions of 011-d
  are terminal for that round's attempts.
- The recovery round regenerates the SAME 134 documents: the
  deterministic assembly (registered PRNG instances, seeds, and per-
  document draws committed in the 011-d manifest) reproduces byte-
  identical document structure, layout, and topic assignment; only
  the scaffold section texts are new (fresh generation calls under
  the amended class). The round MUST assert reproducibility against
  the 011-d private per-document ledger (k, topics, layout,
  collection ID, record ID, arm) BEFORE the first live call; any
  mismatch is BLOCKED with the mismatch named.
- The 011-d private round state (progress ledger, assembly
  summary, the 8 stored incomplete raw responses) is preserved
  immutable. The recovery round appends round-tagged (011-e)
  records to the ledger and writes new raw responses under an
  attempt-tagged name; the collection of record remains the single
  committed manifest, extended and finalized in this round.
- The 011-d order's floor-50 gate (its scope item 3d) applies
  verbatim to the recovery round's survivors: genuine-arm survivors
  < 50 -> Result BLOCKED on the named shortfall with zero samples
  opened beyond the failed attempts.

## 4. Scope statement: not a method change

The scaffold sections are discarded before scoring (REVISION-011
sections 5-6: OUT_OF_SCOPE, never labeled, never scored). This
revision changes only an operational generation parameter of the
discarded-scaffold mechanism. It changes no frozen method element
(ranking, detector thresholds, candidate semantics, validator
prompt/parser, main-capture contract reasoning level, acceptance
policy, protection rules) and is informed by no calibration or
confirmation content (zero samples were opened at 011-d; the
confirmation subset is untouched). The no-tuning rule of PROTOCOL-
009 (n) is NOT triggered. The study label (development-
distribution re-measurement), the authorized-reuse disclosure, the
reclassification statement, and all PLAN section 14.2/14.3
comparator and metric requirements are UNCHANGED.

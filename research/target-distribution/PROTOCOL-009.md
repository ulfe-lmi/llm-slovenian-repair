# PROTOCOL-009 — Pre-registered frozen protocol for the fresh human-labelled
# target-distribution confirmation study

Status: FROZEN (pre-registered, data-free, round 009-a, objective 009).
This document is the single source of truth for objective-009 rounds 009-b
onward (collection, annotation, evaluation, comparative report). It is
data-free: it contains no confirmation sample, no raw Slovenian text, no
endpoint values, no credentials, and no private paths. It changes no frozen
mechanism and authorizes no tuning. Collection, annotation, and evaluation
happen only in subsequent proof-sized suffixes, under this frozen protocol,
after the E2 target-deployment decision is resolved by an attributable
owner decision (see `DEPLOYMENT-IDENTITY-009.md`).

## 0. Authority and consistency anchors

- PLAN v1.0 sections 14.2/14.3 (linguistic evaluation design and main
  criteria) remain authoritative for population sizes, comparators,
  denominators, and the calibration-target semantics; PLAN section 15.2
  work groups M01 (initial labelled set with correct controls and a
  separate threshold/calibration part), M04 (calibration of acceptance —
  here pre-registered, never executed against the confirmation set), and
  M07 (comparative report) are the delivery containers; PLAN section 16
  (MVP criteria: measured quality on cases that did not serve development)
  applies to the final disposition.
- RESEARCH-STATE section 13 (objective 009 reserved design) and section 14
  (explicit no-tuning boundary) are restated and extended below, not
  re-opened.
- The frozen system entering 009 is exactly the identity pinned in section
  2 below: the frozen 007-m linguistic method plus the accepted
  objective-008 structural protection layer (policy of record v5).

## 1. Cited records (sha256)

| Record | sha256 |
| --- | --- |
| PLAN.md v1.0 (protected bytes) | `d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0` |
| research/RESEARCH-STATE.md at accepted main `185dc3d9c654991619ae5c57b64e0c54f4550a16` | `00f3b8a7a4e1819e61ada1fcaf8f1bc6ededd4fb44662d14b543ee4d23d1e4c2` |
| research/registry/experiments.json at accepted main (33 entries, last 008-i PASS) | `4204d6614f606f924b7d0aac7ab1844f29ebd9e260cb54b433db6c90e8011c53` |
| research/configs/007-m-rank-ambiguous-levenshtein-candidates.json (public data-free projection) | `41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0` |
| research/curated/prose_boundary.py (objective-008 protection layer) | `c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50` |
| research/curated/protected.py (objective-008 protection layer) | `27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f` |
| research/prose-boundary/config/structural-policy-v5.json (policy of record) | `915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542` |
| research/prose-boundary/config/structural-policy-v4.json (byte-identical in-tree) | `f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f` |
| research/prose-boundary/config/experiment-008i.json (frozen protection census) | `24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685` |
| CRITICAL.md (seed-identical, zero entries at the frozen base) | `a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e` |
| oap/orders/009-a-target-distribution-confirmation-preregistration.md (activating order) | `dcee0004d37f6b061fb469c59484b1f0ce4f5d445ac2e2fa5f6248331ff58303` |
| Frozen 007-m private configuration (sha256 pinned inside the committed config, `private_evidence.configuration_sha256`) | `0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26` |
| Frozen 007-i validator prompt (private; sha256 pinned inside the committed config, `prompt.sha256`) | `572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d` |
| Frozen 007-m implementation head (git commit) | `537aa6a3ff03c60dd1b2c7f697c577940d52e88d` |
| Frozen 007-j deployment profile (out-of-band private file; sha256 per RESEARCH-STATE section 3) | `c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60` |
| Frozen 007-m deployment profile (sha256 pinned inside the committed config, `deployment.profile_sha256`) | `0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e` |
| Research accepted main (objective-008 merge commit; order base) | `185dc3d9c654991619ae5c57b64e0c54f4550a16` |

## 2. Frozen-system identity pin (the system under confirmation)

The confirmation study evaluates the COMPLETE effective pipeline as frozen
after 008. No element below is re-tuned, re-ranked, re-prompted, or
re-parameterized against the confirmation set or any subset of it.

### 2.1 Frozen 007-m linguistic method

- Private frozen configuration sha256: `0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26`;
  public data-free projection file sha256: `41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0`
  (research/configs/007-m-rank-ambiguous-levenshtein-candidates.json).
- Candidate rule (frozen): deterministic unique single-letter unigram
  substitution attested in the exact frozen unigram vocabulary (141,162
  rows; English suppression precedes lookup) plus the complete standard
  Levenshtein distance-one expansion (SUBSTITUTION/INSERTION/DELETION;
  transposition excluded) over the frozen vocabulary union; C>1 targets
  proceed to the predeclared ranking.
- Predeclared lexicographic ranking tuple (frozen verbatim, over the frozen
  immediate left/right context; substitution is a hypothetical candidate
  insertion into that context only): (1) trigram exactness flag, (2)
  trigram exact count, (3) exact bigram side count, (4) sum of exact bigram
  counts, (5) unigram exact count. An exact top-score tie selects nothing
  (original retained, no validator call). Gold is structurally absent from
  ranking and score inputs (post-ranking headroom analysis only).
- Validator protocol (frozen): strict binary-choice protocol
  USE_CANDIDATE / KEEP_ORIGINAL / UNCERTAIN; extra text, malformed JSON,
  wrong model/effort, incomplete status, missing token accounting, timeout,
  or transport failure is a distinct conservative FAILURE. One terminal
  attempt per candidate; uncertain deliveries are never resampled.
- Frozen prompt sha256: `572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d`
  (owner-supplied frozen 007-i validator prompt, shared unchanged by
  007-i/j/m).
- Protocol limits (frozen): 300 s timeout; 2,000,000-byte response bound;
  one terminal attempt per candidate; no resampling; `new_call_budget` 0 in
  the final root; retry policy NONE (no corrective retry).
- Frozen implementation head: `537aa6a3ff03c60dd1b2c7f697c577940d52e88d`.
- Frozen 007-lineage deployment profiles (out-of-band identity, endpoint
  value never committed): profile sha256 `c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60`
  (007-j) and `0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e`
  (007-m). The confirmation TARGET deployment is NOT presumed to be this
  regime: see element (a) below and DEPLOYMENT-IDENTITY-009.md.

### 2.2 Frozen objective-008 structural protection layer

- research/curated/prose_boundary.py sha256 `c57e2901e52af962546ee83651850e22c91655a8cc822f2c43b1284da16b8c50`.
- research/curated/protected.py sha256 `27f22eaee129190b880851b958a8aa5a38d357cb4e711d70e762b2353d32e78f`.
- structural-policy-v5.json sha256 `915f70d34ecc69ab6fea0b273f24ca20f251b6e181bd5e9281c5c012de2fe542`
  is the POLICY OF RECORD; structural-policy-v4.json sha256
  `f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f`
  remains byte-identical in-tree; experiment-008i.json sha256
  `24e25edafbbf0b1d67dc405440ea78c0b76a9011c00d5e53c82fe3c00fef6685` is the
  frozen four-file protection census (the PASS-branch FROZEN declaration at
  the 008-i census).
- The objective-008 verdict was PASS (all eight predeclared fields) on the
  sealed v4 hidden set; that verdict is structural-safety evidence only and
  carries no linguistic acceptance.

### 2.3 No-tuning list (RESEARCH-STATE section 14, verbatim)

> Until fresh (009) evidence exists, NO further tuning on DASSLE or any
> already-inspected benchmark of:
>
> - the candidate rule (deterministic unique single-letter unigram
>   substitution + complete standard Levenshtein distance-one expansion),
> - the predeclared lexicographic ranking tuple (section 3),
> - the validator prompt (frozen 007-i prompt, section 3),
> - the acceptance/conservativeness thresholds,
> - the validator protocol limits (300 s / 2,000,000 bytes / one terminal
>   attempt / no resampling),
> - the retry policy (no corrective retry in the frozen method).
>
> Rationale: researcher degrees of freedom on this one population are
> substantially consumed — four successive same-sample mechanism changes
> (007-h -> 007-i -> 007-j -> 007-m), each selected on the same 2,973 paired
> records. Any further same-sample variant (new ranking functions, prompt
> edits, threshold sweeps, C>1 runner-ups, top-k>1 with resampling) carries
> overfit risk: a same-sample improvement cannot be distinguished from noise
> or adaptation to the inspected gold. No 007-p or later same-sample variant
> is authorized. Any future mechanism change requires a new objective, fresh
> data, and a new PR.

## 3. Pre-registered study elements

### (a) Target deployment/model identity (HARD GATE)

TARGET DEPLOYMENT HARD GATE. The target configuration is the PLAN-identified
intended deployment: strongly quantized Qwen3.8-27B on RTX 3090 (PLAN v1.0
header line 6: "Ciljna namestitev: obstoječi, močno kvantizirani Qwen3.8-27B
na RTX 3090"). Confirmation collection is authorized ONLY from a deployment
whose pinned identity (model identifier, quantization, serving framework and
version, wire protocol, max model length, endpoint class) matches the
owner-designated target and was pinned and verified by the procedure in
DEPLOYMENT-IDENTITY-009.md BEFORE the first sample is collected. The 007
evidence regime (A100-FP8, model `qwen3.8-27b`, Responses non-streaming,
vLLM 0.28.0 observed) is NOT deployment-equivalent, and NO 007 live result
transfers to the intended deployment without replication (RESEARCH-STATE
section 9). Until the owner resolves E2 with an attributable decision, NO
confirmation data is collected from any deployment and the loop idles at
that boundary. No confirmation work occurs before that decision, in any
subsequent 009 suffix.

### (b) Sampling population and collection procedure

COLLECTION PROCEDURE. The population is: genuine Slovenian-language outputs
of the pinned target configuration, generated under the product's intended
use (complete stored main answers per LR-001: full main generation and
bounded capture before any review), PLUS human-authored fully-correct
control documents under explicit rights and controlled storage. No synthetic
stand-in may replace genuine target outputs in the confirmation population.
A collection manifest is created BEFORE the first sample is opened:
collection IDs, domain tags, source kind (genuine target output /
human-authored control), collection timestamps, the pinned deployment
identity reference (section 2.1 profiles and the E2-resolved target
identity, by hash reference only), and private-root file hashes
(content-free). Within the genuine-output population, selection uses a
seeded PRNG — pre-registered seed string `009a-target-distribution-20260930`
fed to Python 3.12 `random.Random` (frozen environment) — applied to the
eligible inventory sorted lexicographically by collection ID, without
replacement, to avoid selection bias. The manifest is committed data-free
(counts, IDs, tags, hashes; no text).

### (c) Domain mix

DOMAIN MIX. Pre-declared domain tags: (1) general Slovenian prose; (2)
technical language; (3) a mix including rare expressions and proper names;
(4) any further domains the owner adds at E2 resolution (recorded, not
invented). Per-stage minimum counts per domain are pre-registered: no
domain below 10 percent of stage size at stage 1. A violation triggers
expansion, never re-labeling of already-collected documents.

### (d) First-stage size and expansion criteria

STAGE SIZES AND EXPANSION CRITERIA. Stage 1 = 50-100 genuine outputs
(target 100, floor 50 with the reason for any shortfall recorded at
collection). Stage 2 expansion toward 100-500 (target 300, cap 500) across
domains, triggered ONLY by the pre-registered criteria: (i) the stage-1
accepted-repair correctness 95 percent confidence interval is too wide to
decide against the approximately 99 percent calibration goal; (ii) a
pre-registered domain is under-represented against its minimum count; (iii)
the stage-1 operational failure rate exceeds the pre-registered stop
threshold of element (l)(d). Expansion adds only fresh, uncollected,
unopened samples from the same pinned target configuration; no re-sampling,
no re-collection of opened samples, no method change.

### (e) Correct-text negative controls

CONTROLS QUOTA. At least 25 percent of stage-1 documents are FULLY_CORRECT
controls: fully correct Slovenian text including technical language, rare
expressions and proper names (PLAN 14.2), of which at least 10 are
human-authored technical/rare/name documents. Controls carry the harm-rate
denominator (originally-correct words) and the preservation metrics.

### (f) Annotation taxonomy

ANNOTATION TAXONOMY (exact labels, pre-registered).

Source ground truth per span/document:
- ACTUAL_ERROR — genuine error in the target span;
- ACCEPTABLE_UNCHANGED — acceptable as-is;
- FULLY_CORRECT_DOCUMENT — control document;
- NEEDS_WIDER_EDIT — genuine error whose correct fix is non-local.

Intervention outcome per accepted edit:
- CORRECTS_ERROR — the edit genuinely fixes the error and creates none;
- ACCEPTABLE_ALTERNATIVE — acceptable alternative rendering; no error fixed;
  optional change;
- HARMLESS_STYLISTIC — unnecessary but harmless stylistic preference;
- HARMFUL_CHANGE — correct text made incorrect or semantically different;
- NO_CHANGE — the pipeline left the text unchanged.

Layer-failure classes:
- PROTECTION_FAILURE — the frozen v5 protection layer exposed or
  over-protected against policy, with byte-level attribution;
- DETECTOR_MISS — a genuine error not flagged by the detector (MANDATORY
  label on every genuine error not flagged);
- CANDIDATE_GENERATION_MISS — the correct replacement was not generated;
- RANKING_MISS — the correct candidate existed but ranked below the
  selected one (or an exact top-score tie selected nothing);
- VALIDATOR_REJECTION_OR_FAILURE — the validator rejected, returned
  UNCERTAIN, or failed conservatively;
- ACCEPTANCE_POLICY_REJECTION — the acceptance layer rejected a valid
  proposal (insufficient evidence, structural contradiction, identity
  replacement, forbidden content, scope expansion);
- PATCH_FAILURE — composition/patching failed or rolled back.

### (g) Independent human adjudication procedure

ADJUDICATION PROCEDURE. Two independent human labelers (Slovenian-native;
trained on the committed data-free annotation guide before first label) per
detected span and per document. The two-labeler disagreement is recorded.
Ambiguous cases are adjudicated by the owner or a named human with a
recorded rationale class. Qwen is NEVER the final judge of its own changes
(PLAN 14.2). A 5-document calibration pilot (genuine outputs, excluded from
the confirmation set and the calibration subset) aligns the labelers before
labeling starts and is never scored or used for method decisions. Labelers
do not see internal stage decisions before final scoring.

### (h) Calibration versus untouched confirmation split

SPLIT RULE. At collection time, before any opening, a document-level split
is fixed by a deterministic rule on collection IDs: 15 percent calibration /
85 percent confirmation. Pre-registered rounding and selection: let N be
the number of collected documents at split time and k = ceil(0.15 x N); the
calibration subset is the first k documents ordered by the lexicographic
hex of sha256(collection ID) (deterministic, ID-based, no further
randomness). The calibration subset is used ONLY for operational
verification of the frozen pipeline on the target configuration (call /
parse / patch mechanics) and NEVER for behavior change — a verification
failure that suggests a behavior change stops the round and escalates. The
confirmation subset is untouched until final scoring. Zero leakage between
subsets or with any 007/008 material: the 009 confirmation population
contains no case generated or inspected for any earlier objective (manifest-
asserted at collection).

### (i) Comparator methods

COMPARATORS (PLAN 14.2, required):
1. ORIGINAL — unmodified target output;
2. DETECTOR_ONLY — CPU detector output, no intervention;
3. DIRECT_QWEN_PROOFREADING — one fresh bounded request per document under a
   pre-registered comparator protocol (isolated context, no repair history,
   settings recorded); explicitly NOT the production architecture;
4. FROZEN_RESTRICTED_METHOD — the complete frozen system (007-m linguistic
   method plus the 008 protection layer) as pinned in section 2;
5. CORPUS_ONLY — optional research arm (corpus repair without Qwen
   adjudication), may be enabled by a recorded budget decision and never
   blocks the required four.

### (j) Metrics and denominators

METRICS (six families, each with its denominator):
1. Accepted-repair correctness = CORRECTS_ERROR edits / all assessed
   accepted edits, with the assessed count reported and a 95 percent
   Clopper-Pearson interval;
2. Harmful interventions per 10,000 originally-correct words = 10000 x
   (HARMFUL_CHANGE count on originally-correct spans) / originally-correct
   word count (frozen word counter), with the 3/N 95 percent upper bound at
   zero events and the intra-document correlation caution;
3. Coverage, reported separately: detector coverage = genuine errors
   flagged / all genuine errors; final-repair coverage = genuine errors
   finally repaired as CORRECTS_ERROR / all genuine errors;
4. Stylistic-only rate = (ACCEPTABLE_ALTERNATIVE + HARMLESS_STYLISTIC)
   assessed edits / all assessed accepted edits, a separate metric;
5. Preservation: unchanged-correct-document rate over FULLY_CORRECT
   controls, and edit units introduced on originally-correct text per
   10,000 correct words;
6. Operational cost: review-call rate (answers with at least one repair
   call / all answers), token totals per answer (main and repair
   separately), p50/p95 latency with and without repair, failure/timeout
   rate per attempt.

### (k) Uncertainty intervals

UNCERTAINTY RULES. 95 percent Clopper-Pearson for all proportions on their
assessed denominators; the 3/N upper bound for zero-event rates (events
treated as independent, simplification stated); no pooling of
different-scope counts; EXACT/CENSORED/UNAVAILABLE evidence states
preserved — missing or censored evidence is NEVER reported as zero
(LR-008 semantics).

### (l) Stopping/falsification rules

STOPPING RULES (pre-registered, all four):
- (a) STOP AND REPORT if accepted-repair correctness falls materially below
  the approximately 99 percent goal with an assessed count large enough
  that the 95 percent confidence interval decides it — no rescue tuning
  (any mechanism change requires a new objective, fresh data, and a new PR);
- (b) every established HARMFUL_CHANGE is reported individually with full
  attribution; the study falsifies the strict-mode harm goal when the
  one-sided 95 percent lower bound of the harmful rate exceeds 1 per
  10,000 originally-correct words; zero events at small N are always
  reported as upper bounds, not achievement (the 1 per 10,000 bound
  needs approximately 30,000 correct words at zero events);
- (c) if final-repair coverage is negligible relative to genuine-error
  incidence, the round reports the coverage limitation with the measured
  benefit/harm statement (PLAN 14.3: lower coverage is acceptable if the
  measured benefit is clear and harm is small);
- (d) STOP AND REPORT if the operational failure rate makes the service
  path unreliable (pre-registered threshold: more than 5 percent of
  attempts as distinct conservative failures, or a deterministic repeated
  transport failure).
A pass does not auto-accept the MVP; it enables the human milestone
decision (S-ICA).

### (m) Failure decomposition

FAILURE DECOMPOSITION. Every genuine error not finally repaired is assigned
EXACTLY the first failing stage in the order: PROTECTION_LAYER -> DETECTOR
-> CANDIDATE_GENERATION -> RANKING -> VALIDATOR -> ACCEPTANCE_POLICY ->
PATCH, using the layer-failure classes of element (f). A low end-to-end
recall must stay attributable to a stage.

### (n) No-tuning-after-unblinding rule

NO-TUNING-AFTER-UNBLINDING RULE. Once the confirmation subset is opened, or
once any decision is informed by its content, NO change of any frozen
element is permitted against the confirmation set, ever: the candidate rule
(deterministic unique single-letter unigram substitution plus complete
standard Levenshtein distance-one expansion), the predeclared lexicographic
ranking tuple, the detector thresholds/eligibility, the candidate semantics
(frozen unigram vocabulary, expansion), the validator prompt/parser/protocol
(USE_CANDIDATE/KEEP_ORIGINAL/UNCERTAIN), the reasoning level, the
acceptance policy (conservative acceptance; EXACT/CENSORED/UNAVAILABLE
handling), the protocol limits (300 s / 2,000,000 bytes / one terminal
attempt / no resampling), the retry policy (none), and the protection rules
(policy v5, curated prose_boundary.py, protected.py). The rule also covers
the calibration subset: operational verification must not lead to behavior
change. Any mechanism change requires a new objective, fresh data, and a new
PR (RESEARCH-STATE section 14).

### Calibration-targets statement

The approximately 99 percent accepted-repair correctness and at most 1
harmful intervention per 10,000 originally-correct words are
EVALUATION/CALIBRATION TARGETS, NOT AUTOMATIC RELEASE AUTHORIZATION (PLAN
14.3 [S1]). They calibrate the acceptance policy; release, deployment, and
milestone authority remain human decisions (PLAN section 16; S-ICA).

## 4. Data rights and privacy

Confirmation data require explicit rights and controlled storage. Outputs
are private. No raw confirmation text, no endpoint values, no credentials,
and no private paths appear in any committed artifact, log, or report;
public artifacts carry data-free aggregates, counts, and hash references
only (LR-013; A-CORPUS-02 public-posture convention).

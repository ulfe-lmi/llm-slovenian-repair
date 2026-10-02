# ANNOTATION-GUIDE-011 - data-free labeler operationalization for the
# development-distribution re-measurement (objective 011, round 011-d;
# operationalizes PROTOCOL-009 (f)/(g)/(j)/(k) AS AMENDED BY
# PROTOCOL-009-REVISION-011; consumed by the 011-e evaluation round)

Status: COMMITTED (data-free; round 011-d, scope item 8a). This guide is
the operational manual for the two independent Slovenian-native labelers
of the 011-e evaluation round. It transcribes, without weakening, the
pre-registered taxonomy, adjudication procedure, metric denominators, and
uncertainty semantics of PROTOCOL-009.md (byte-frozen; label names
UNCHANGED) AS AMENDED by PROTOCOL-009-REVISION-011 (registered byte-exact
by the 011-d round; sha256 609751c15d76416f46358bbde0a03b7b2c68637fe338b96c88df2d85796c5e43).
This document is data-free: it contains no corpus text, no confirmation
sample, no raw Slovenian document, no endpoint values, no credentials,
and no private paths (private locations are named by relative directory
name only).

## 0. Study label and authorized-reuse disclosure (recorded once)

This study is a development-distribution RE-MEASUREMENT, not a fresh
target-distribution confirmation (PROTOCOL-009-REVISION-011 section 1).
Every DASSLE text in the stage-1 population was previously inspected:
objective 007 ran the campaign8 full-dataset phase over all 7,385
spelling records and all 7,381 preservation records, and the 2,973-pair
007-h/i/j/m method-development chain consumed the category-Crkovanje
subset. The population is an AUTHORIZED REUSE of DASSLE by the owner's
2026-10-01 directive (private decision receipt; referenced by name only).
No case in this population is fresh or uninspected; this is disclosed,
not hidden. Consequences for labelers: (1) results support no fresh
target-distribution confirmation claim; (2) the E2(b) target designation
(A100-FP8) and the frozen system under measurement are unchanged; (3)
every downstream report uses the re-measurement label.

Per-document attestation is carried in the 011-d collection manifest
(`research/target-distribution/011b-collection-manifest.json`), which
records, per collection ID: the DASSLE record id, the dataset sha256
references, and the CONSUMPTION TIER - TIER-2 (method development) for
records with category == Crkovanje (the 2,973-pair 007-h/i/j/m chain),
TIER-1 (campaign8 full-dataset only) for all others.

## 1. What labelers see (packet contents)

Labeler work queues live under the private `011b-packets/` directory
(0700/0600; never committed). Each packet contains:

1. the assembled input document (the collected document: one verbatim
   DASSLE block plus k = 1..3 interleaved LLM-generated Slovenian
   technical scaffold sections, joined by exactly two LF characters);
2. the collected main answer (the complete stored target output);
3. the DISCARD MAP - per document, the code-point (start, end-exclusive)
   offsets of every scaffold block and of the DASSLE block within the
   assembled input (scope item 3e/4vii);
4. the DASSLE reference for the scored span (genuine arm: the record's
   human `reference`; control arm: the preservation text, which equals
   its reference by construction);
5. the frozen CPU detector's span output on that main answer (frozen
   detector, no intervention, no review call, no accepted edit, no
   scoring in the 011-d round).

The per-span/per-document queue structure for the calibration and
confirmation subsets (collection IDs and file hashes only) is opened by
the 011-e round AFTER the span-correspondence matcher of section 3 is
applied; the confirmation subset stays untouched until final scoring
(the PROTOCOL-009 (h) split rule, unchanged by the revision).

## 2. The discard rule (OUT_OF_SCOPE / OUT_OF_SCORED_SPANS)

- SCAFFOLD blocks are DISCARDED before any human or machine scoring:
  they carry no denominator, no word count, no coverage, no harm rate,
  and no preservation metric; labelers NEVER label them. Packets mark
  scaffold regions OUT_OF_SCOPE via the discard map; a labeler who
  notices a suspicious scaffold region records the observation and
  moves on (it is not scored and does not enter any metric).
- The SCORED content of a main answer is the DASSLE span located by the
  section-3 matcher. Every accepted edit is classified as: within the
  scored span (scored per sections 4-5) or wholly outside it (recorded
  as OUT_OF_SCORED_SPANS: counted operationally in the report, never
  scored, never counted in harm, coverage, or preservation).
- Edits that straddle the scored-span boundary are recorded as
  OUT_OF_SCORED_SPANS with a straddling note (conservative: the edit is
  never split-scored).

## 3. The span-correspondence matcher (registered deterministic
   matcher; run in 011-e BEFORE any scoring)

The pipeline operates on the collected main answer. The scored DASSLE
span of a main answer is located as follows (PROTOCOL-009-REVISION-011
section 5, verbatim mechanics):

1. Let M = the main answer truncated to its first 50,000 code points
   (registered cap; a longer main answer is UNALIGNABLE by cap).
2. For candidate c in the ORDER (1) the verbatim DASSLE `input` of the
   document's record, (2) the DASSLE `reference`: compute
   `m = difflib.SequenceMatcher(None, c, M, autojunk=False)` and take
   `(i1, i2, j) = m.find_longest_match(0, len(c), 0, len(M))`.
3. If `(i2 - i1) >= 0.8 * len(c)`, the scored span is
   `M[j : j + (i2 - i1)]` (code points, end-exclusive). Candidate (1)
   is tried first; if it reaches the 0.8 ratio, candidate (2) is not
   used for that document.
4. If NO candidate reaches the 0.8 ratio, the document is UNALIGNABLE:
   a named conservative state, recorded in the 011-e report; the
   document is excluded from span scoring and counted operationally.
   An unalignable document is NEVER reported as zero or as
   fully-correct (S-PRODUCT-02; missing or censored evidence is never
   reported as zero).

The matcher runs before any labeler sees a document; labelers receive
the located span (or the UNALIGNABLE marking) with the packet. Labelers
never relocate spans manually; a labeler who believes the located span
is wrong records the doubt on the label sheet (a named mismatch note)
and labels the located span as given - doubts are aggregated for
adjudication, never acted on per-document.

## 4. Source ground truth per scored DASSLE span (verify, never create)

GROUND-TRUTH RULE: the DASSLE human `reference` is the SOURCE GROUND
TRUTH for DASSLE-derived spans (the dataset's own per-record human
correction). For control documents (preservation records) the DASSLE
block is FULLY CORRECT by construction (input == reference;
dataset-attested). The labeler VERIFIES / ADJUDICATES the dataset
reference; the labeler NEVER creates new ground truth, never rewrites
the reference, and never introduces a "better" correction. If the
reference itself looks wrong or ambiguous, the labeler marks the span
NEEDS_WIDER_EDIT only where the correct fix is non-local, otherwise
records an AMBIGUOUS-REFERENCE doubt note for owner/named-human
adjudication (section 7); the doubt never substitutes a new reference.

Labels (exact, pre-registered; PROTOCOL-009 (f), names unchanged):

- ACTUAL_ERROR - the scored span in the main answer deviates from the
  reference in a way that is a genuine error (the target failed to
  correct, or the deviation is an error);
- ACCEPTABLE_UNCHANGED - the span is already correct or an acceptable
  variant relative to the reference (no genuine error present);
- FULLY_CORRECT_DOCUMENT - control document (the entire DASSLE block is
  fully correct by construction; the labeler verifies the
  by-construction claim against the packet reference and records any
  doubt);
- NEEDS_WIDER_EDIT - a genuine error whose correct fix is non-local
  (cannot be expressed as a local edit of the span).

Per scored DASSLE span, the labeler assigns EXACTLY ONE of
ACTUAL_ERROR / ACCEPTABLE_UNCHANGED / NEEDS_WIDER_EDIT for genuine-arm
documents, or verifies and records FULLY_CORRECT_DOCUMENT for
control-arm documents.

## 5. Intervention outcome per accepted edit (within scored spans)

For every accepted edit within a scored span, the labeler assigns
EXACTLY ONE outcome relative to the reference (PROTOCOL-009 (f), names
unchanged):

- CORRECTS_ERROR - the edit genuinely fixes the error and creates
  none;
- ACCEPTABLE_ALTERNATIVE - acceptable alternative rendering; no error
  fixed; optional change;
- HARMLESS_STYLISTIC - unnecessary but harmless stylistic preference;
- HARMFUL_CHANGE - correct text made incorrect or semantically
  different.

NO_CHANGE is a pipeline state (the pipeline left the text unchanged),
not an accepted-edit outcome; documents with no accepted edits carry
NO_CHANGE at document level and contribute to the operational cost
metrics only.

## 6. Layer-failure classes and mandatory attribution

For EVERY genuine error not finally repaired, the labeler assigns
EXACTLY the first failing stage in the fixed order (PROTOCOL-009
(m)): PROTECTION_LAYER -> DETECTOR -> CANDIDATE_GENERATION -> RANKING
-> VALIDATOR -> ACCEPTANCE_POLICY -> PATCH, using the layer-failure
classes of PROTOCOL-009 (f) (names unchanged):

- PROTECTION_FAILURE - the frozen v5 protection layer exposed or
  over-protected against policy, with byte-level attribution;
- DETECTOR_MISS - a genuine error not flagged by the detector.
  MANDATORY label on every genuine error not flagged;
- CANDIDATE_GENERATION_MISS - the correct replacement was not
  generated;
- RANKING_MISS - the correct candidate existed but ranked below the
  selected one (or an exact top-score tie selected nothing);
- VALIDATOR_REJECTION_OR_FAILURE - the validator rejected, returned
  UNCERTAIN, or failed conservatively;
- ACCEPTANCE_POLICY_REJECTION - the acceptance layer rejected a valid
  proposal (insufficient evidence, structural contradiction, identity
  replacement, forbidden content, scope expansion);
- PATCH_FAILURE - composition/patching failed or rolled back.

A low end-to-end recall must stay attributable to a stage; the labeler
uses the packet's frozen CPU detector span output and the 011-e
comparator artifacts to assign the FIRST failing stage, never a
conjunction.

## 7. Two-labeler procedure, disagreement, adjudication

- TWO independent human labelers (Slovenian-native; trained on this
  committed data-free guide before first label) per scored span and per
  document. Labelers work independently; neither sees the other's
  labels before submitting.
- The two-labeler disagreement is RECORDED (per span, per document;
  disagreement rate reported, never silently resolved).
- Ambiguous cases (including AMBIGUOUS-REFERENCE doubt notes and
  span-mismatch notes) are adjudicated by the OWNER or a NAMED HUMAN
  with a recorded rationale class. The adjudication record states the
  case, both labels, the rationale class, and the final label.
- Qwen is NEVER the final judge of its own changes (PLAN 14.2). No
  model output resolves a disagreement; no model output is the final
  adjudication.

## 8. Calibration-pilot procedure (alignment only; never scored)

- The 5-document calibration pilot (collection IDs recorded in the
  011-d manifest partition; genuine outputs) is used ONLY to align the
  labelers before labeling starts: both labelers independently label
  the pilot, disagreements are discussed and the rationale classes
  agreed, and the agreed readings are recorded as the alignment
  record.
- The pilot is EXCLUDED from BOTH the calibration subset and the
  confirmation subset; it is never scored, never enters any metric
  denominator, and is never used for method decisions.
- Labelers do not see internal stage decisions before final scoring
  (PROTOCOL-009 (g), unchanged). The 011-e calibration subset (20
  documents, recorded in the manifest) is used ONLY for operational
  verification of the frozen pipeline mechanics on the target
  configuration (call / parse / patch mechanics) and NEVER for
  behavior change; a verification failure that suggests a behavior
  change stops the 011-e round and escalates.

## 9. Metric families and denominators (PROTOCOL-009 (j) SCOPED to
   DASSLE-scored spans per the discard rule and the section-3 matcher)

All denominators and word counts are computed over DASSLE-SCORED spans
only (PROTOCOL-009-REVISION-011 section 6): "originally-correct words"
= the frozen word counter over the reference text of the DASSLE blocks
(controls: all of it; genuine: the reference spans); coverage
denominators count genuine errors WITHIN scored spans (per the
reference, as verified by labelers); accepted-edit denominators count
assessed accepted edits WITHIN scored spans. Edits outside scored
spans are OUT_OF_SCORED_SPANS: recorded in the report (count + scope),
never counted in harm, coverage, or preservation. All metric formulas,
comparators, and stopping rules of PROTOCOL-009 (i)-(l) are otherwise
unchanged. The six families with their scoped denominators:

1. Accepted-repair correctness = CORRECTS_ERROR edits / all assessed
   accepted edits (assessed count reported; 95 percent Clopper-Pearson
   interval);
2. Harmful interventions per 10,000 originally-correct words =
   10000 x (HARMFUL_CHANGE count on originally-correct spans) /
   originally-correct word count (frozen word counter); the 3/N 95
   percent upper bound applies at zero events; intra-document
   correlation caution recorded;
3. Coverage, reported separately: detector coverage = genuine errors
   flagged / all genuine errors (within scored spans); final-repair
   coverage = genuine errors finally repaired as CORRECTS_ERROR / all
   genuine errors (within scored spans);
4. Stylistic-only rate = (ACCEPTABLE_ALTERNATIVE + HARMLESS_STYLISTIC)
   assessed edits / all assessed accepted edits, a separate metric;
5. Preservation: unchanged-correct-document rate over FULLY_CORRECT
   controls' DASSLE blocks, and edit units introduced on
   originally-correct text per 10,000 correct words (controls: the
   entire DASSLE block is the scored span, fully correct text);
6. Operational cost: review-call rate (answers with at least one
   repair call / all answers), token totals per answer (main and
   repair separately), p50/p95 latency with and without repair,
   failure/timeout rate per attempt.

UNALIGNED (section-3 UNALIGNABLE) documents are excluded from the span
denominators and counted operationally (named count, reason: cap or
0.8-ratio failure); they are never zero-filled.

## 10. EXACT / CENSORED / UNAVAILABLE evidence states (PROTOCOL-009 (k),
   unchanged)

- EXACT - the complete stored main answer with a parseable completed
  response (the state in which a document is a genuine target output);
- CENSORED - HTTP 200 but an incomplete or unparseable response (with
  the message text if present, stored privately); the evidence state is
  preserved and the document is counted, never scored as if complete;
- UNAVAILABLE - HTTP error, timeout, transport failure, or no message
  output.

Missing or censored evidence is NEVER reported as zero (LR-008 /
S-PRODUCT-02). Uncertainty rules (PROTOCOL-009 (k)): 95 percent
Clopper-Pearson for all proportions on their assessed denominators; the
3/N upper bound for zero-event rates (events treated as independent,
simplification stated); no pooling of different-scope counts.

## 11. Recorded limitation (waived technical/rare-name control floor)

The pre-registered >= 10 human-authored technical/rare-name control
documents of PROTOCOL-009 (e) is WAIVED by the owner directive and
recorded here as a standing limitation: the DASSLE source contains no
scored technical/rare-name population; technical-domain realism is
present ONLY in the discarded scaffold sections (which are, by
definition, not scored). This limitation bounds the external validity
of any technical-domain claim (there is none scored in this study) and
must be repeated in the 011-e report and in every downstream claim
using this population.

## 12. Boundaries restated for labelers

- Label only what the packet shows; never open the confirmation subset
  outside the 011-e schedule; never score scaffold content; never
  report an unalignable or censored document as zero.
- Qwen is never the final judge; the owner or a named human is the
  final adjudicator; the labelers are a 011-e input, not a 011-d one
  (no annotation occurred in the 011-d collection round).
- No raw DASSLE text, no scaffold text, no main answer, no endpoint
  value, no credential, and no private path leaves the private roots
  (LR-013; PROTOCOL-009 section 4 as extended by the revision section
  9). Label sheets, doubt notes, and adjudication records are
  data-free artifacts (counts, IDs, labels, rationale classes) and may
  be committed by the 011-e round only after the publication guard
  passes.

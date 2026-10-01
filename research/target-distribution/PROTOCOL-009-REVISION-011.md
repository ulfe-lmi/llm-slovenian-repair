# PROTOCOL-009-REVISION-011 - additive owner-attributed revision: DASSLE
# mechanical-assembly intake for the stage-1 collection

Status: REGISTERED (additive; round 011-d, objective 011). This revision is
committed BEFORE any sample is generated. `PROTOCOL-009.md` remains
byte-frozen and authoritative for every element NOT superseded below. This
document is data-free: it contains no corpus text, no confirmation sample,
no raw Slovenian document, no endpoint values, no credentials, and no
private paths (the registered generator prompt is a registered instruction
template, the same artifact class as the 011-e registered comparator
prompt; the registered topic list carries topic names only).

## 0. Authority, status, supersession map

- Authority: explicit attributable owner directive of 2026-10-01 (three
  verbatim messages recorded in the private decision receipt
  workorders/dassle-reuse-decision-20261001.md; H-provenance of the 011-d
  order). Under S-AUTH-01/02 the owner's explicit decision on data source
  and risk appetite supersedes the owner-supplied-intake model of the
  published 011-b collection specification.
- Effect: SUPERSEDES, for the stage-1 collection and the 011-e evaluation
  that consumes it, exactly the following elements of PROTOCOL-009:
  (b) sampling population and collection procedure; (c) domain mix;
  (e) correct-text negative controls; (g) source-of-ground-truth and
  labeler tasking within the adjudication procedure; (h) the
  zero-leakage assertion only (the split rule of (h) is UNCHANGED).
- Every other element is UNCHANGED and remains authoritative, including:
  (a) target-deployment hard gate (the E2(b)-designated A100-FP8 regime,
  verified by the 011-c REGIME-UNCHANGED record); (d) stage sizes and
  expansion criteria; (f) annotation taxonomy (label names unchanged;
  the assignment tasking is adjusted per section 5 below); (i) comparators
  (including the 011-e registered DIRECT_QWEN_PROOFREADING prompt);
  (j) metrics and denominators (scoped per section 6 below); (k)
  uncertainty intervals; (l) stopping/falsification rules; (m) failure
  decomposition; (n) no-tuning-after-unblinding; section 0, section 2
  (frozen-system identity pin, unchanged byte-for-byte), and section 4
  (data rights and privacy, as extended by section 7 below).
- This revision changes NO frozen element of the frozen system
  (section 2 of PROTOCOL-009): no candidate rule, ranking tuple, detector
  threshold/eligibility, candidate semantics, validator prompt/parser/
  protocol, reasoning level, acceptance policy, protocol limit, retry
  policy, or protection rule is altered. Element (n) is NOT triggered
  (no confirmation-subset decision content is opened; no mechanism
  change). RESEARCH-STATE section 14 (no further tuning on DASSLE or any
  already-inspected benchmark) remains in force for mechanism changes.

## 1. Reclassification statement (recorded once)

This study is RECLASSIFIED from "fresh target-distribution confirmation"
to "development-distribution re-measurement". All DASSLE texts are
previously inspected: objective 007 ran the campaign8 full-dataset phase
over all 7,385 spelling records and all 7,381 preservation records
(M0-M3), and the 2,973-pair 007-h/i/j/m method-development chain consumed
the category-Chrkovanje subset (1,487 spelling + 1,486 preservation;
count-matched against the 007-h config source_identity). Consequences:
1. The results of this study do NOT support a fresh target-distribution
   confirmation claim. PLAN section 16 milestone/MVP claims remain gated
   on a genuinely fresh, uninspected set at a later objective.
2. The reclassification concerns input provenance only: the E2(b) target
   designation (A100-FP8) and the frozen system under measurement are
   unchanged.
3. Honest labeling: the 011-e report title, RESEARCH-STATE section, and
   registry entry must use the re-measurement label.

## 2. Source data (byte-verified, private, data-free references)

- DASSLE spelling source: private file `dassle.jsonl`, 7,385 records,
  sha256 609b696616f7246ba9c09a97531f3b9f2035ce3efca35926a5e73898b28045d6.
  Fields (per record): benchmark, category, example_source, id (unique),
  index, input (erroring source text, sentence-level), problem_type,
  reference (human correction), reference_status (SUPPLIED: 7,381;
  MISSING_BLANK_FIELD: 4).
- DASSLE preservation: private file `dassle-preservation.jsonl`, 7,381
  records, sha256 d87e6ccee74cef0981a0e8ebd6315d75abbcf8bb8558e9a9627507f0bbbf4bec.
  Fields as above plus preservation: true and parent_source_sha256;
  input == reference in ALL 7,381 records (fully-correct texts by
  construction, per the dataset's own adaptation record).
- Both files reside under the private research-runtime root (the
  campaign8 private location). The 011-d round re-verifies BOTH sha256
  values byte-for-byte before any assembly; any mismatch BLOCKS the
  round (named), no replacement.
- Category distribution (data-free census, verified 2026-10-01):
  Besedišče 977 / Črkovanje 1,487 / Oblikoslovje 1,748 / Skladnja 1,971 /
  Zapis 1,202 (spelling file); preservation file: Besedišče 976 /
  Črkovanje 1,486 / Oblikoslovje 1,748 / Skladnja 1,971 / Zapis 1,200.

## 3. Superseded element (b): population and collection procedure

POPULATION (mechanical assembly). The stage-1 population consists of
MECHANICALLY ASSEMBLED documents. Each document is exactly one DASSLE-
derived block (the VERBATIM `input` text of one DASSLE record: the
erroring source for the genuine arm, the corrected text for the control
arm) plus one to three LLM-generated Slovenian technical scaffold
sections interleaved around it. The LLM outputs ONLY scaffold sections;
it never outputs a "pure Slovenian" source document (owner directive,
verbatim in the decision receipt). No synthetic error injection; no
model-assisted authoring or editing of any DASSLE text; the DASSLE block
enters the document byte-for-byte.

Eligible inventories:
- GENUINE arm: records with reference_status == SUPPLIED and
  input != reference (non-identity pairs; 7,354 records).
- CONTROL arm: all 7,381 preservation records, EXCLUDING (registered)
  every preservation record whose `id` equals the `id` of a record
  selected in Draw 1 (verified parent link: all 7,381 preservation
  records carry the parent spelling record id, inherit its category,
  and carry parent.reference as their input). This prevents one
  underlying text from appearing in both arms.

Assembly mechanics (registered, deterministic; a single PRNG instance
`rng_asm = random.Random("011d-dassle-mechanical-assembly-20261001")`,
Python 3.12, frozen environment, created once, drawn in this exact order
per document, documents processed in sorted collection-ID order):
1. k = 1 + rng_asm.randrange(3) -> the number of scaffold sections
   (k in {1, 2, 3}).
2. For j = 1..k: topic_j = TOPICS[rng_asm.randrange(len(TOPICS))];
   section_j = one SCAFFOLD_GENERATION call (section 4 below) with the
   {tema} sentinel replaced by topic_j (single occurrence, no other
   byte changed).
3. Layout: the DASSLE block is inserted after the first ceil(k/2)
   sections: k=1 -> [s1, D]; k=2 -> [s1, D, s2]; k=3 -> [s1, s2, D, s3].
4. Blocks are joined by exactly two LF characters ("\n\n"); the document
   is exactly that concatenation (no other separators, headers, or
   whitespace).
5. DISCARD MAP: the manifest records, per document, the code-point
   (start, end-exclusive) offsets of every scaffold block and of the
   DASSLE block within the document. The discard map is the data-free
   definition of what is scored and what is discarded.

Selection (re-executes the PROTOCOL-009 (b) PRNG mechanics over the new
population; the pre-registered seed string is retained): a single PRNG
instance `rng_sel = random.Random("009a-target-distribution-20260930")`
is created once and drawn in this exact order, every draw over its list
sorted lexicographically by record id, without replacement, via
`i = rng_sel.randrange(len(remaining)); take remaining.pop(i)`:
- Draw 1 (genuine): from the eligible genuine inventory, up to 100
  (target; floor 50 per (d); any shortfall between 50 and 100 is
  RECORDED with its reason).
- Draw 2 (control): from the eligible control inventory (post-exclusion,
  recomputed AFTER Draw 1), up to ceil(len(Draw 1)/3) (target 34 for
  G = 100; the (e) quota).
The previously registered technical/rare-name control draw is WAIVED by
the owner directive (recorded limitation, section 4b below). The
selected set (G genuine documents + C control documents) is the stage-1
population; each selected DASSLE record yields exactly one document.
Unselected eligible records remain available for 011-f stage-2
expansion only (unopened; no re-sampling of the selected set).

Manifest-first: the collection manifest is created BEFORE any sample is
opened or any scaffold call made, and is extended per document with the
record id, dataset sha references, consumption tier (section 7),
section-count/topic draws (data-free), discard map, and per-call
metadata (numbers only). Collection IDs retain the pre-registered
`011b-<seq:04d>` scheme, assigned deterministically in sorted
(doc_slug) order, with doc_slug = `dassle-spelling-<id>` or
`dassle-preservation-<id>` (the DASSLE record id, zero-padded to 4
digits). Artifact names (`011b-collection-manifest.json`, `011b-
collection/`, `011b-packets/`) are retained unchanged.

## 4. Superseded element (c): domain mix (mechanical mapping)

- The DASSLE source (example_source: Šolar 3.0) is general educational
  prose; its per-record `category` field is an ERROR-TYPE category
  (vocabulary / spelling / morphology / syntax / orthography), not a
  topic domain. Registered mechanical rule: EVERY document carries
  domain_tag = "general-prose"; the DASSLE category is recorded in the
  manifest as source metadata only and is NEVER used as a domain tag.
- The pre-registered 10 percent domain floor (c) is vacuously satisfied
  (single domain; recorded as N/A with the reason - not a violation and
  not an expansion trigger).
- Limitation (WAIVER, owner directive): the pre-registered >= 10
  human-authored technical/rare-name control documents of element (e)
  is WAIVED: the DASSLE source contains no scored technical/rare-name
  population. Technical-domain realism is present ONLY in the discarded
  scaffold sections (which are, by definition, not scored). This
  limitation is recorded in the manifest, the annotation guide, and the
  011-e report, and it bounds the external validity of any technical-
  domain claim (there is none scored in this study).

## 5. Superseded element (g): source of ground truth and labeler tasking

- Source ground truth for DASSLE-derived spans is the DASSLE human
  `reference` (the dataset's own per-record human correction), NOT
  fresh human authoring. For controls (preservation records) the text is
  fully correct by construction (input == reference; dataset-attested).
- Span correspondence (registered deterministic matcher, run in 011-e
  before any scoring): the pipeline operates on the collected main
  answer; the scored DASSLE span of a main answer is located as follows.
  Let M = the main answer truncated to its first 50,000 code points
  (registered cap; a longer main answer is UNALIGNABLE by cap). For
  candidate c in the order (1) the verbatim DASSLE `input`, (2) the DASSLE
  `reference`: compute m = difflib.SequenceMatcher(None, c, M,
  autojunk=False); take (i1, i2, j) = m.find_longest_match(0, len(c), 0,
  len(M)); if (i2 - i1) >= 0.8 * len(c), the scored span is M[j : j +
  (i2 - i1)] (code points, end-exclusive). If no candidate reaches the
  0.8 ratio, the document is UNALIGNABLE (a named conservative state,
  recorded; the document is excluded from span scoring and counted
  operationally; never reported as zero, S-PRODUCT-02).
- Labeler tasking (reduced accordingly): (1) per scored DASSLE span in
  the main answer: verify ACTUAL_ERROR (the span deviates from the
  reference in a way that is a genuine error) or ACCEPTABLE_UNCHANGED
  (already correct or an acceptable variant), or NEEDS_WIDER_EDIT (the
  correct fix is non-local) - the labeler VERIFIES/ADJUDICATES the
  dataset reference; (2) per accepted edit within a scored span:
  intervention outcome (CORRECTS_ERROR / ACCEPTABLE_ALTERNATIVE /
  HARMLESS_STYLISTIC / HARMFUL_CHANGE) relative to the reference;
  (3) MANDATORY DETECTOR_MISS attribution for every genuine error not
  flagged; (4) layer-failure classes per (f) for every genuine error not
  finally repaired, first-failing-stage order per (m). Labelers NEVER
  label scaffold blocks: packets include the discard map, scaffold
  regions are marked OUT_OF_SCOPE, and any accepted edit wholly outside
  the scored span is recorded as OUT_OF_SCORED_SPANS (counted, never
  scored). The two-labeler procedure, disagreement recording, owner/
  named-human adjudication of ambiguous cases, the 5-document
  calibration pilot (alignment only, never scored), and "Qwen is NEVER
  the final judge" are UNCHANGED.

## 6. Superseded element (e): controls; score scoping

- FULLY_CORRECT controls are assembled documents built from
  preservation records (corrected DASSLE texts, fully correct by
  construction). Quota: C >= ceil(G/3) (target 34 for G = 100), drawn
  per section 3 Draw 2 post-exclusion. Controls carry the harm-rate
  denominator (originally-correct words) and the preservation metrics,
  scoped to their scored DASSLE spans (for controls: the entire DASSLE
  block, which is fully correct text).
- Score scoping (extends (j) without changing any formula): every
  denominator and word count is computed over DASSLE-SCORED spans only,
  per the discard map and the section-5 matcher:
  "originally-correct words" = frozen word counter over the reference
  text of the DASSLE blocks (controls: all of it; genuine: the
  reference spans); coverage denominators count genuine errors WITHIN
  scored spans (per the reference, as verified by labelers); accepted-
  edit denominators count assessed accepted edits WITHIN scored spans.
  Edits outside scored spans are OUT_OF_SCORED_SPANS: recorded in the
  report (count + scope), never counted in harm, coverage, or
  preservation. All metric formulas, comparators, and stopping rules of
  (i)-(l) are otherwise unchanged.

## 7. Superseded element (h): authorized-reuse disclosure (split
   rule unchanged)

- The zero-leakage assertion ("no case generated or inspected for any
  earlier objective") is SUPERSEDED by AUTHORIZED-REUSE DISCLOSURE:
  the population is an authorized reuse of DASSLE by the owner's
  2026-10-01 directive (private decision receipt). Per-document
  attestation in the manifest and report: DASSLE record id, dataset sha
  references (section 2), and CONSUMPTION TIER: TIER-2 (method
  development) for records with category == Črkovanje (the 2,973-pair
  007-h/i/j/m chain; verified count-match: 1,487 spelling + 1,486
  preservation); TIER-1 (campaign8 full-dataset only) for all others.
  No document in this population is fresh or uninspected; this is
  disclosed, not hidden.
- The split rule of (h) is UNCHANGED: at collection time, before any
  opening, the 15/85 split by collection ID (k = ceil(0.15 * N);
  lexicographic hex of sha256(collection ID)), the 5-document
  calibration pilot excluded from both subsets, and the confirmation
  subset untouched until final scoring.
- The no-tuning rule (n) is UNCHANGED and NOT triggered by this
  revision (no frozen element changed; no decision informed by
  confirmation-subset content).

## 8. Registered SCAFFOLD_GENERATION call class

- Purpose: produce ONLY the discarded technical scaffold sections.
  This is a new, registered, bounded call class on the designated
  target (the E2(b)-designated A100-FP8 regime as verified at 011-c),
  authorized by the owner directive; it is separate from, and does not
  alter, the main-capture contract of the genuine-output generation
  (which remains the frozen 007-m profile contract) or from
  REPAIR_ALLOW_LIVE_TESTS = NO (product live tests remain disallowed).
- Prompt (registered byte-exact; committed as
  `research/target-distribution/SCAFFOLD-GENERATOR-PROMPT-011.md`,
  exactly the template bytes, 402 B, sha256
  005edf0a0ea4f9a52f8acc887b28f0f772f04cf54197cca15c539e50ed9cc0fc):
  a Slovenian instruction to write a short professional technical
  paragraph (150-250 words) on the topic given by the single {tema}
  sentinel; no title, no bullet list, no code, no persons, no direct
  questions to the reader, no external sources cited; output the
  paragraph text only.
- Registered topic list (12 data-free topic names, exact UTF-8 strings;
  drawn per section 3 step 2): vzdrževanje klimatskih naprav;
  montaža sončnih panelov; konfiguracija omrežnih stikal;
  termična izolacija cevovodov; kalibracija merilnih senzorjev;
  preskušanje nosilnih konstrukcij; vzdrževanje parnih kotlov;
  temeljenje gradbenih objektov; osvetlitev industrijskih prostorov;
  obratovanje hidravličnih dvigal; prezračevanje podstresnih
  prostorov; varnostna preskušanja električnih naprav.
- Call contract: one fresh isolated request per section on the
  designated target only; Responses wire API, non-streaming; NO main
  history, NO session linkage, NO tools, NO images, NO constitutional-
  adapter recursion (S-PRODUCT-02); profile (both bases + bearer) read
  ONLY from the private 011b-identity credentials receipt (the sole
  profile source; never committed, logged, or echoed); output-token
  cap 600; 300 s timeout; 2,000,000-byte response bound; ONE terminal
  attempt; NO resampling, NO retry.
- Response handling (deterministic, pre-registered): store verbatim
  privately (011b-collection scaffold store, 0700/0600, never
  committed); strip exactly one trailing LF; strip exactly one outer
  code-fence pair iff the first and last lines are exactly three
  backticks with nothing outside; otherwise use the text as received.
  If the call fails or the processed section is empty: the document is
  EXCLUDED with the failure named (no replacement, no re-sampling); the
  exclusion is counted operationally.
- Budget (registered cap): at most (G + C) documents, at most 3
  sections each -> at most 402 scaffold calls for stage 1 (G target 100
  + C target 34 = 134 documents). Every call is recorded in the
  manifest (numbers only: HTTP status, wall time, tokens, capture size,
  state).

## 9. Data rights extension (supersedes section 4 only where stated)

- DASSLE was previously acquired and used under owner direction for
  objective 007; the owner's 2026-10-01 directive authorizes controlled
  private reuse for this study. No redistribution; no raw DASSLE text,
  no scaffold text, no main answers, no endpoint values, no
  credentials, and no private paths in any committed artifact, log, or
  report (LR-013; PROTOCOL-009 section 4 otherwise unchanged).
- The LLM-generated scaffold sections are owner-authorized synthetic
  material, private, discarded, and never committed.

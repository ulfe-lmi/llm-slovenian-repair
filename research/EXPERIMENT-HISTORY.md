# Experimental history and measured findings

EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Strategic-authored archival synthesis for round 007-d. This document summarizes
already-produced evidence; it introduces no experiment, tuning, model calls or
new semantic labels. Exact originals, including data-bearing reports and traces,
remain private. The [catalog](registry/experiments.json), [file identities](registry/file-census.json)
and [source mapping](registry/source-manifest.json) provide the evidence trail.
Numeric alignment success is not synonymous with linguistic correctness.

## How the research question changed

The owner prioritized falsifying the repair concept before completing production
architecture. The initial isolated 007-a/b implementation combined corpus detection,
focused Qwen review, conservative acceptance and Codex/Responses integration.
Instrumentation failures prevented the original intended end-to-end evidence:
controlled reviewer aggregation failed after calls, and the workload collector
used an unsupported CLI option. These attempts and their later replacement runs
remain separate historical executions, not retroactively repaired originals.

The owner subsequently removed Codex, the proxy/SSE adapter and workload machinery
from linguistic experiments. The direct algorithm studies then varied reasoning,
validation/retry, detector normalization, case preservation and English eligibility.
The latest pipeline was frozen for external evaluation. A later explicit owner
change removed the detector's four-target cap; concurrency later increased from
sequential to four and then eight workers. These are distinct configurations and
continuations, not one unchanged initial run.

Only the A 100 deployment was evaluated in the final campaign. The proposed second
deployment was excluded by owner override. No cross-quantization replication claim
can be made from this record.

## Small controlled studies

The full frozen controlled suite contains 32 cases: 7 labelled errors and 25 controls.
Some early experiments reviewed only the 10 previously selected cases/proposals.
Do not treat 10 reviewer calls as 32 independent reviewed targets, or compare counts
without the corresponding candidate selection and call-reuse information.

| Study | Actual variation | Preserved outcome |
| --- | --- | --- |
| Original 007-a/b | Initial isolated concept/integration and subsequent instrument correction | Preserve original reports and failed executions; no accepted linguistic conclusion |
| 007-b replacement | Human-authorized replacement of failed instrument | Failure evidence retained separately |
| 007-b timeout 300 | Same controlled instrument with 300 s safety ceiling | 10 controlled calls completed; median 21.44 s, p95 217.03 s; workload case/trace association invalid |
| Non-thinking mechanical | Hard non-thinking setting; mechanical-only post-review acceptance | 10 calls; 4 applied edits; 2 exact-gold repairs; 1 changed control |
| Low-thinking mechanical | Low reasoning, otherwise comparable mechanical-only study | 10 calls; 6 applied; 3 exact-gold; 1 changed control |
| High-thinking mechanical | High reasoning | Stopped run; do not substitute the completed xhigh result |
| Xhigh-thinking mechanical | Xhigh reasoning | 10 calls; 8 applied; 4 exact-gold; 1 changed control |
| Low plus validator | Additional validation of already-sampled low first-pass proposals | 10 first-pass calls reused, 6 new validator calls; 6 applied; 3 exact-gold |
| Low unigram retry | Unigram post-check and then a contextual corrective retry | 10 first-pass calls reused, 2 new corrective calls; 4 applied; 3 exact-gold |
| Word-only retry | Context-free retry using rejected proposal only | Initial stop and saved-response whitespace continuation are separate evidence, not fresh resampling |
| Hyphen-space detector | ASCII hyphen becomes space in detector view only | 32 cases, 9 candidates, 10 calls; 5 applied; 3 exact-gold; 0 changed controls |
| Initial-case stage | One-way initial-capital restoration | 32 cases, 9 candidates, 11 calls; 2 applied; 2 exact-gold; 0 observed applied case-adjustment events |

The early detector-only field `known_errors_remaining=0` is semantically unusable:
detector-only applies no edits. Likewise, a timeout is an operational/censored
observation, not a wrong linguistic judgment. The invalid timeout 300 workload
association supplies no trustworthy per-case semantic comparison or review sheet.

### Three ten-trial studies

Each scheduled trial sought fresh model responses. Stopped trials were not replaced
with an eleventh run. Completed-only denominators and available partial records
must both remain visible.
The trials repeat the same 32 examples: 320 case instances are not 320 independent
linguistic examples. They primarily describe response variability on that fixed set.

| Configuration | Scheduled / complete / stopped | Calls: first + corrective | Complete case instances | Available including partial | Recorded study elapsed |
| --- | --- | --- | --- | --- | --- |
| Symmetric initial-case, word-only retry | 10 / 8 / 2 | 87 +10 =97 | 256 | 305 | 575.6548 s |
| Context-free 1–4-word expression retry | 10 / 9 / 1 | 90 +13 =103 | 288 | 319 | 638.9849 s |
| English pre-review preservation | 10 / 10 / 0 | 80 +15 =95 | 320 | 320 | 694.8680 s |

These totals do not alone establish improvement. The expression change removed a
single-word interface restriction; it did not make every contextual proposal good.
English preservation is a deterministic policy suppression, not a model KEEP.
Prior case-level semantic assessments were strategic-model judgments, not human
ground truth. Their safe categorical projections must remain distinguishable from
fixture exact-gold counts and from the later automatic benchmark metrics.

## Frozen external-evaluation pipeline

The final campaign used the uncapped continuation of the English-preservation
baseline, not the initial capped preparation:

1. Identify protected material and keep original coordinates.
2. Use the existing Gigafida detector with a length-preserving ASCII-hyphen-to-space
   lookup view; normalization does not rewrite the actual input.
3. For an originally selected target with Slovene unigram state UNAVAILABLE only,
   query casefolded English wordfreq 3.1.1. Zipf frequency >= 3.0 preserves the target
   without a first-review call. Other Slovene evidence and suspicion stay unchanged.
4. Make the contextual structured KEEP/REPLACE/WIDER review with qwen3.8-27b and
   explicit low reasoning. Restore the original target's initial case symmetrically.
5. Apply mechanical safety checks, including the 1–4-word/80-code-point replacement
   bounds, then require per-word EXACT Slovene-unigram membership. No post-review
   bigram/trigram semantic veto is used.
6. On the defined first-proposal unigram uncertainty, allow at most one context-free
   expression retry on that raw rejected proposal only. It receives no original
   sentence/target, corpus suggestions, gold or previous reasoning. Same low
   reasoning, initial-case restoration and acceptance checks apply.
7. Patch exact original-coordinate approved spans. No accepted edit may change
   protected material or an unapproved slice.

The campaign used a 300 s socket safety timeout, not a global example deadline, and
a 2 MB response bound. There were at most 8 concurrent requests in the final campaign,
all to the single A 100 regime. Scheduling, continuation and provenance records
distinguish inherited valid calls from newly executed calls; completed samples
were not regenerated merely because the process restarted.

The frozen source/index/request identities, generic prompts and executable
reproduction recipes are separate from this overview. The observed server version
was vLLM 0.28.0; FP 8 was observable in the model identity, while hardware information
not mechanically verified remains owner-declared. No model/service configuration
was changed for archival publication.

### Methods and failure semantics

| Method | Meaning |
| --- | --- |
| M0 | Exact identity; no model calls |
| M1 | Conservative whole-text Qwen proofreading with the frozen direct prompt |
| M2 | Full detector/English/contextual-review/unigram/optional-retry/exact-patch method |
| M3 | No-retry counterfactual reconstructed from M2's shared first-stage samples |

For campaign repair-example operational failures, final output is the original
input and `operational_failure=true`; this is not model KEEP. M3 does not inherit
a failure caused only by the corrective call it omits. Call/latency comparisons
must distinguish physically executed calls from shared-sample counterfactual cost.

## Campaign coverage and completion

The final local campaign completed all 9 phases: 16,375 cases and 65,500 method records.
Its 39,184 distinct model calls comprise 31,916 new and 7,268 inherited calls. Preservation
verification recorded 1,419 checkpoints and 218,991 raw/result files. This is one
deployment's evidence, not two-deployment replication.

| Phase | Examples | Interpretation |
| --- | ---: | --- |
| MultiGEC train | 10 | Diagnostic only, not tuning/evaluation confirmation |
| MultiGEC dev | 50 | Reference-backed local official GEC evaluation |
| MultiGEC dev preservation | 50 | Already-correct reference inputs |
| Canonical Šolar-Eval | 109 | Separate canonical resource; not reconstructed MultiGEC test gold |
| Canonical preservation | 109 | Canonical reference inputs |
| DASSLE | 7,385 | Supplied categories/types retained separately |
| DASSLE preservation | 7,381 | Available reference/corrected texts |
| MultiGEC test | 49 | Outputs prepared; no distributed test references |
| SloBench | 1,232 | Frozen raw translations and three post-processing outputs; hidden references |

The owner judged essay-style GEC an IRRELEVANT primary test of the intended sparse
lexical-error regime. That scope judgment does not erase its measurements or prove
the target regime works. All planned locally executable phases were nevertheless
completed and retained, including unfavorable results.

The earlier capped campaign had begun inference and was interrupted; it was not
merely unexecuted preparation. The uncapped ancestor was paused by the owner's
relevance change. The DASSLE spelling stage subsequently completed 1,487 error inputs
and 1,486 preservation inputs, 11,892 method records and 6,195 unique calls, with its
worker/recovery incidents preserved. These should not be double-counted as newly
sampled independent evidence when later inherited by the complete campaign.

## Key measured outcomes

### Official scorer results

These are the preserved official-tool outputs, not the custom alignment scorer.
F0.5 is a fraction; GLEU is on the reported percentage-style scale. The independently
extracted [numeric summary](results/strategic-official-summary.json) records the
original scorer-file hashes, full counts and as-recorded JSON values.
The official tool records identity precision as 1 when it predicts no edits; that
is an empty-prediction convention, not proof of a perfect correction system.

| Dataset / metric | Identity | Direct M1 | Full M2 | No-retry M3 |
| --- | ---: | ---: | ---: | ---: |
| MultiGEC dev F0.5 | 0 | 0.4560 | 0.0963 | 0.0967 |
| MultiGEC dev GLEU | 49.8263 | 64.9078 | 50.9906 | 50.9331 |
| Canonical Šolar-Eval F0.5 | 0 | 0.4484 | 0.0849 | 0.0845 |
| Canonical Šolar-Eval GLEU | 49.0726 | 64.1473 | 50.3534 | 50.3398 |
| DASSLE F0.5 | 0 | 0.3883 | 0.3003 | 0.3103 |
| DASSLE GLEU | 67.9624 | 74.7351 | 71.4808 | 71.4226 |

### DASSLE: custom token-coordinate edit alignment

This scorer identifies 8,623 gold edit units across the evaluable reference-backed
data. Do not substitute these denominators into official ERRANT scores.

| Method | TP | Non-reference edits FP | Gold units remaining FN | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| Direct M1 | 2,212 | 2,766 | 6,411 | 44.44% | 25.65% |
| Full M2 | 834 | 525 | 7,789 | 61.37% | 9.67% |
| No-retry M3 | 827 | 393 | 7,796 | 67.79% | 9.59% |

The targeted method repairs some supplied-reference errors, but the full dataset
does not support a large general error-incidence reduction. It is more precise
and less invasive than whole-text proofreading, at substantially lower recall.
The existing detector is heavily OOV/lexical-absence oriented; many grammatical,
punctuation and multi-token reference changes never reach focused review.

For the supplied spelling category, 1,486 references contain 1,515 custom gold units:

| Method | TP | FP | Recall | Precision |
| --- | ---: | ---: | ---: | ---: |
| Direct M1 | 689 | 587 | 45.48% | 54.00% |
| Full M2 | 604 | 193 | 39.87% | 75.78% |
| No-retry M3 | 600 | 148 | 39.60% | 80.21% |

A narrower, post-hoc lexical diagnostic used a different denominator: 604/1,400
gold units, or 43.1% recall, with 604/794 = 76.1% precision. It is not a preregistered
primary result and must not silently replace the whole spelling-category result.

Raw exact-sentence agreement also includes inputs already equal to references.
There are 27 raw-identical DASSLE pairs and 48 additional nonidentical pairs that are
already token-identical. The token-distinct erroneous cohort is 7,306 examples;
exact token-sequence recoveries are M0 = 0, M1 = 1,724, M2 = 783 and M3 = 781.

### Correct-text preservation

On the 7,381 DASSLE reference inputs, token-sequence preservation and introduced
custom edit units were:

| Method | Token-preserved examples | Preservation | Edit units introduced | Edits /1,000 words |
| --- | ---: | ---: | ---: | ---: |
| Direct M1 | 5,407 | 73.26% | 2,489 | 21.531 |
| Full M2 | 7,054 | 95.57% | 340 | 2.941 |
| No-retry M3 | 7,137 | 96.69% | 252 | 2.180 |

These are token-preservation statistics, not byte-exact preservation percentages.
There were 65 M2 and 61 M3 operational-failure examples in this preservation phase;
fail-closed identity must not be mistaken for a model's correct KEEP judgment.
Non-reference changes are measurable overcorrection candidates, not independently
human-adjudicated harmful edits. Protected/outside-approved-slice changes were 0.

### Retry ablation

On DASSLE, the corrective pass added 7 custom gold-matching edit units but 132
non-reference units, at 581 extra calls. On DASSLE preservation it introduced 88
additional edit units at 395 calls. Official DASSLE F0.5 was lower with retry than
without it. This is a substantive adverse trade-off, not something to hide behind
the number of accepted edits. It warrants a future decision, not retuning this
frozen campaign during archival work.

### SloBench: operational/change evidence, not hidden-reference quality

All 1,232 raw translations and direct-proofreading results completed without
operational failure. Full targeted processing had 43 failed examples and 46 failed
first-review calls; multiple call failures can belong to one example.

| Output | Changes | Calls attributable to stage |
| --- | --- | ---: |
| Direct proofreading | 353 changed texts, 465 custom difference units | 1,232 |
| Targeted full | 163 changed texts(13.23%),188 accepted patches | 1,997 |
| Targeted no retry | 140 changed texts(11.36%),154 accepted patches | 1,822 shared first-stage calls |

English preservation suppressed 83 of 1,905 selected candidates. Retry used 175 calls,
produced 34 accepted patches and changed 33 outputs. Their quality is UNKNOWN without
the hidden references or later adjudication. Mean HTTP intervals were 10.60 s for
base translation, 12.28 s for direct proofreading, 14.73 s for full targeted processing
and 11.79 s for its no-retry counterfactual. Base translation is not adapter overhead.

Four 1,232-row SloBench submissions and three 49-text MultiGEC submissions were
prepared privately. Remote scoring needed login/noninteractive authority that
was unavailable. Scribendi's gated model access returned 401. No hidden references
were reconstructed. Apparent TP/FP/exact fields from no-reference records are
semantically unusable as correctness or harm metrics.

## Supplemental mechanical investigations

The exhaustive u/v audit found 75 strict first-letter word substitutions, 51
standalone-word substitutions and 54 noninitial substitutions: 180 total. All were
in the supplied spelling category. The first 75 rows of that category were the
strict class and the next 51 the standalone class, explaining ordering bias in
inspection of early rows. It does not mean most spelling cases were initial u/v:
75/1,487 = 5.04%; including standalone substitutions 126/1,487 = 8.47%.

After excluding the requested k/h and comma-related cases, the remaining cohort
had 1,431 examples. Full-method recall/precision were 41.57%/76.26%; removing all 180
u/v cases yielded 43.75%/77.04%. The initial 75 contributed 28 of 604 gold matches(4.64%).
These requested sensitivity analyses do not redefine the primary benchmark.

The random 20 other-failure sample used seed 2026091101 and a 162-example eligible
spelling pool after exclusions. The public record may retain sampled IDs and
selection code, but the sentences/proposals stay private. There was no new
semantic relabeling; reference metrics can penalize legitimate alternatives.

The single-case retry-limit-ten experiment altered only that limit. It made 1 first
call and 3 corrective calls, accepting an EXACT-unigram-attested proposal that did
not match the known intended correction. HTTP time was 72.858526 s and total time
84.827574 s. It illustrates that dictionary membership alone does not establish
contextual suitability; it is not a benchmark or proof that more retries help.

A separate read-only Levenshtein lookup over 71,650 length-filtered keys found a
unique distance 1 candidate matching the supplied correction, with unigram count
4,184. Naive lookup took 2.596717 s. It made no model calls and changed no pipeline.
Its original inline execution had no preserved standalone source hash; the later
observation note must not be misrepresented as an original frozen script.

## Reproducibility and evidential limits

- The original physical index file was lost before the uncapped campaign. Its
  replacement was built from the same verified inputs and checked for logical
  equivalence; this is not recovery of the old physical bytes. The replacement
  SHA-256 is f769235b6af3412e65f0875f4d08231c832f60d8630b43a06ab927c2d32c739f.
- Final-campaign UTC endpoints span 50,906 s, while monotonic accounting records
 51,975.041 s: a 1,069.041 s discrepancy with cause UNVERIFIED. Both are retained;
  timings were not silently rescaled to agree.
- Exact references can reject legitimate alternative corrections. Conversely,
  matching a unigram or the model's own judgment does not prove meaning preserved.
- English frequency is not contextual language identification. No translation/
  slovenization policy or broader foreign-language classifier was evaluated.
- No human or strategic-model per-example semantic labels were fabricated for
  the external campaign. Earlier small-study model assessments remain separate.
- Essay/student-error benchmarks do not reproduce all sparse spontaneous Qwen
  lexical failures. That limits generalization in both positive and negative directions.
- Public research contains code, generic prompts, hashes and data-free evidence;
  exact dataset inputs/references, generated text, reasoning, filled prompts,
  source archives/indexes and credentials remain private. This is not a data
  redistribution or new license grant.

## Scientific disposition of the existing evidence

The measured method is a conservative, selective repair mechanism with a visible
preservation advantage, not an established broad Slovenian correction solution.
The spelling-category results show useful recovery, but not approximately 80%
reduction of its supplied target errors. The external evidence does not justify
claiming that broad hypothesis as demonstrated. Low overall detector coverage and
the unfavorable retry precision trade-off remain material limitations.

The sparse-LLM-lexical-error hypothesis is narrower and is not settled by dismissing
the essay results; SloBench quality scoring remains pending. Further research may
be justified by the selective/preservation findings, but a next experiment or
architecture decision needs its own explicit scope. Archival completion is not
permission to tune, integrate, merge PR 8, release or deploy.

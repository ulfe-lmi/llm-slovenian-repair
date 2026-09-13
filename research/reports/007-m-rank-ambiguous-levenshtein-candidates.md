# 007-m rank ambiguous Levenshtein candidates

EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

The sole variable is the selection rule for C>1 (ambiguous) targets: the frozen CPU ranking (a predeclared lexicographic tuple, frozen before gold analysis) selects the one candidate that the frozen 007-j validator sees, and no runner-up is ever tried. C=0 and C=1 remain the exact preserved 007-j behavior and observations. The primary 007-m result is the hybrid projection: the preserved 007-j validated_fallback row per case with each C>1 target span replaced by the 007-m decision outcome.

## Headline: does 007-m improve upon 007-j?

A conservative tradeoff, not an unqualified win: 007-m HYBRID improves precision, F0.5, and preservation while losing 23 TP (1.5181518151815232 recall points) against 007-j validated_fallback.

- dassle-spelling/all (007-m HYBRID vs 007-j validated_fallback): TP/FP/FN 799/114/716 vs 822/154/693 (delta -23/-40/+23); precision/recall/F0.5 0.8751369112814896/0.5273927392739274/0.7731759241339268 vs 0.8422131147540983/0.5425742574257426/0.7584425170695701 (delta +0.0329237965273913/-0.015181518151815232/+0.014733407064356663).
- dassle-spelling/initial-u/v: TP/FP/FN 49/7/26 vs 42/7/33 (delta +7/0/-7); precision/recall/F0.5 0.875/0.6533333333333333/0.8193979933110368 vs 0.8571428571428571/0.56/0.7749077490774908 (delta +0.017857142857142905/+0.09333333333333327/+0.04449024423354597).
- dassle-spelling/without-initial-u/v: TP/FP/FN 750/107/690 vs 780/147/660 (delta -30/-40/+30); precision/recall/F0.5 0.8751458576429405/0.5208333333333334/0.7703368940016433 vs 0.8414239482200647/0.5416666666666666/0.7575757575757577 (delta +0.033721909422875784/-0.02083333333333326/+0.01276113642588561).
- dassle-spelling-preservation/all: FP 83 vs 101 (delta -18); preservation changed cases 78 vs 93 (delta -15); introduced edit units 83 vs 101 (delta -18).

The initial-u/v slice improves (+7 TP, no FP delta); the non-initial-u/v slice loses 30 TP while removing 40 FP. Same-sample exploratory evidence only.

Diagnostic projection (not the primary result): validated_only over the scheduled 007-m targets drops the preserved 007-j fallback edits; all spelling TP/FP/FN 778/96/737 (precision 0.8901601830663616, recall 0.5135313531353135) versus 007-j validated_only 802/136/713.

## Frozen identity

- Status: COMPLETE (final zero-call root; hybrid recompute verified both case-result projections byte-for-byte).
- Implementation (frozen) head: 537aa6a3ff03c60dd1b2c7f697c577940d52e88d; recompute head: f3fecab35c64ae202f6fed51d46e472b52270eb3.
- Final root: 007-m-rank-ambiguous-levenshtein-candidates-recovery.ec2962; census root: 007-m-rank-ambiguous-levenshtein-candidates-recovery.97f59c; superseded census diagnostic root: 007-m-rank-ambiguous-levenshtein-candidates-recovery.e6ca66.
- Configuration SHA-256: 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26; live aggregate SHA-256: a30a2114563688adb18954237b97cfd4d6094a0e73566c2b29fd8f14c823ae7f; hybrid aggregate SHA-256: cea2c167ad640fecb03408bdad98fb07c24dba2c9a4e014fe35bd512cd27c4be; hybrid case projections SHA-256: 3c779d96fd06237326902a5162c09f0588482491333d9f72be551eb9040f012c.
- Ranking rule: predeclared lexicographic tuple (trigram exactness flag, trigram exact count, exact bigram side count, sum of exact bigram counts, unigram exact count) over the frozen immediate context; frozen before gold analysis; gold is structurally absent from ranking and score inputs and used for post-ranking headroom analysis only. An exact top-score tie selects nothing and keeps the original; no runner-up is ever tried.

## Population and transition matrix

- Scheduled: 1917 = 1035 C=1 (826 spelling; 209 preservation) + 882 C>1 (651 spelling; 231 preservation); C=0: 524 spelling, 480 preservation.

### dassle-spelling
- C=0 -> C=0: 524.
- C=0 -> C=1: 403.
- C=0 -> C>1: 84.
- C=1 -> C>1: 148.
- C=1 -> different unique candidate: 0.
- C=1 -> same unique candidate: 423.
- C>1 -> C=1: 0.
- C>1 -> C>1: 419.

### dassle-spelling-preservation
- C=0 -> C=0: 480.
- C=0 -> C=1: 90.
- C=0 -> C>1: 18.
- C=1 -> C>1: 45.
- C=1 -> different unique candidate: 0.
- C=1 -> same unique candidate: 119.
- C>1 -> C=1: 0.
- C>1 -> C>1: 168.

## Census headroom (corrected accepted census, C>1 only)

- Targets: 882 (651 spelling + 231 preservation); candidate pairs: 4372.
- Operation pairs: SUBSTITUTION 2801, DELETION 845, INSERTION 726.
- Unique CPU top: 882 of 882; tied top: 0.
- Set size min/median/p90/p95/p99/max: 2/3/9/14/29/50.
- Supplied reference present: 408; absent: 474.
- When present, the gold candidate is covered by the CPU top-k: top1 247 (60.54%), top2 349 (85.54%), top3 376 (92.16%), top5 399 (97.79%), top10 408 (100%).
- Oracle recall ceiling if every present reference were selected: spelling-all 0.5425742574257426 -> 0.8118811881188119; initial-u/v 0.56 -> 0.8933333333333333; non-initial-u/v 0.5416666666666666 -> 0.8076388888888889.
- Reading: ranking headroom is high, but top-1 covers only 60.54% of gold candidates when present; both ranking position and validator rejection/failure limit recall.

## C>1 validation execution (reused observations; zero new calls in the final root)

- Complete C>1: 882 = 866 attempted + 16 uncertain-delivery/no-resample observations.
- Decisions: USE_CANDIDATE 270, KEEP_ORIGINAL 509, UNCERTAIN 16, FAILURE 87.
- Accepted exact-reference / non-reference: 219 / 51 (unresolved 0).
- Candidate attribution exact-reference / non-reference: 247 / 635.
- Attribution by decision: USE_CANDIDATE exact/non-reference 219/51; KEEP_ORIGINAL 13/496; UNCERTAIN 2/14; FAILURE 13/74.
- Latency seconds (n=866): sum 14023.362979554106, mean 16.193259791632915, median 11.124804617022164, p95 33.48273886600509, max 184.56243890197948.
- Inherited tokens input/output/reasoning: 173422/393685/388375; new-call tokens: 0/0/0.

### Failed instrument roots and the final zero-call recompute (reported distinctly)

- 007-m-rank-ambiguous-levenshtein-candidates-recovery.ffdf13 (implementation head 88ca4dfe19740aa21156457d42966661f67902ea): 188 actual experiment calls; 8 request-only interruptions finalized as 8 uncertain observations; the harness at that head rejected the canonical interrupted-finalization file set, so the root could not complete its own live resume; preserved unchanged as failed-instrument evidence.
- 007-m-rank-ambiguous-levenshtein-candidates-recovery.090ea8 (implementation head 92bee3a214aa50ef3921f54488545a57d9a95000): 678 fresh calls (196 observations reused from ffdf13); the fully observed root could not aggregate because the replay identity gate compared in-memory tuple-typed attribution fields against the JSON-normalized persisted rows; preserved unchanged as failed-instrument evidence.
- Actual experiment calls across preserved roots: 188 (ffdf13) + 678 (090ea8) = 866. Cross-root reuse is distinct from actual calls: 196 observations were reused ffdf13 -> 090ea8, and 882 observations (866 attempted + 16 uncertain) were reused 090ea8 -> final root.
- Final root 007-m-rank-ambiguous-levenshtein-candidates-recovery.ec2962: adopted all 882 C>1 observations and all 1035 C=1 observations with zero new calls (new_call budget 0; no resampling; all eight workers dispatched 0); the hybrid recompute recomputed both case-result projections and matched them byte-for-byte before writing the hybrid aggregate (case_results_verified=true, new_calls=0).

## Hybrid composition

- Cases with C>1 targets: 751; winner edits applied: 270; base edits removed: 158; composition-conflict rollbacks: 0.
- Policy: retain base edits not overlapping any C>1 target span; apply the CPU winner edit on USE_CANDIDATE; KEEP_ORIGINAL/UNCERTAIN/FAILURE keep the original target text; a composition conflict rolls back to the original.

## Preservation and integrity

- Preservation changed cases: 78 (007-m HYBRID) vs 93 (007-j validated_fallback); introduced edit units 83 vs 101.
- 007-m hybrid integrity: protected differences 0, outside-span differences 0, exact-expected-output failures 0.

## Boundaries

- Same-sample exploratory projection on the frozen 007-j population; not held-out confirmation, human linguistic acceptance, or production readiness.
- The hybrid view is the primary 007-m result; the validated_only view is a diagnostic that drops preserved 007-j fallback edits.
- Gold is post-ranking headroom analysis only and cannot affect selection; the ranking rule was frozen before gold analysis and was not tuned.
- Non-reference status is not a semantic-harm label.
- Reuse requires exact case, coordinate, sentence, candidate, request, prompt, deployment, parser, and persisted-response identity; the 16 uncertain deliveries were never resampled.
- No baseline response is resampled. PR #8 remains open and unmerged.
- This report does not authorize integration, merge, release, deployment, or product linguistic acceptance; the design is recommended to be frozen and tested against fresh evidence rather than further tuned.

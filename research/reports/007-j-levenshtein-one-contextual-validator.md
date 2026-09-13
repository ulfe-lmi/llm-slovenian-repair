# 007-j standard Levenshtein-one contextual validation

EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

The sole variable is complete standard unit-cost Levenshtein distance-one candidate generation over the frozen 007-i vocabulary; validator and fallback identities remain unchanged.

## Frozen identity

- Status: COMPLETE.
- Candidate population: 1035 (826 spelling; 209 preservation).
- Reused observations / fresh-call budget: 542 / 493.
- Candidate manifest SHA-256: acabcf1b33c38a949c80e81773b8ff3c355386daf768404791aaaed111f1df41.
- Prompt SHA-256: 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d.

## Transition matrix

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

## Operation counts

- dassle-spelling: SUBSTITUTION 423; INSERTION 159; DELETION 244.
- dassle-spelling-preservation: SUBSTITUTION 119; INSERTION 13; DELETION 77.

## Scientific execution

- Reused observations / fresh calls / total observations: 542 / 493 / 1035.
- Operation-level, four-population, fallback, scorer, runtime, and integrity metrics are retained in the data-free aggregate result.

### All Unique candidate outcomes

- SUBSTITUTION: unique 542; exact/non-reference/unresolved 310/231/1; USE/KEEP/UNCERTAIN/FAILURE 312/198/3/29; accepted exact/non-reference/unresolved 288/23/1; rejected 22/208/0; TP/FP/FN 284/22/26; reference precision 0.9260450160771704 (288/311).
- INSERTION: unique 172; exact/non-reference/unresolved 148/24/0; USE/KEEP/UNCERTAIN/FAILURE 141/27/0/4; accepted exact/non-reference/unresolved 131/10/0; rejected 17/14/0; TP/FP/FN 131/10/17; reference precision 0.9290780141843972 (131/141).
- DELETION: unique 321; exact/non-reference/unresolved 166/155/0; USE/KEEP/UNCERTAIN/FAILURE 148/145/3/25; accepted exact/non-reference/unresolved 139/9/0; rejected 27/146/0; TP/FP/FN 138/9/28; reference precision 0.9391891891891891 (139/148).

### New Or Changed candidate outcomes

- SUBSTITUTION: unique 0; exact/non-reference/unresolved 0/0/0; USE/KEEP/UNCERTAIN/FAILURE 0/0/0/0; accepted exact/non-reference/unresolved 0/0/0; rejected 0/0/0; TP/FP/FN 0/0/0; reference precision None (0/0).
- INSERTION: unique 172; exact/non-reference/unresolved 148/24/0; USE/KEEP/UNCERTAIN/FAILURE 141/27/0/4; accepted exact/non-reference/unresolved 131/10/0; rejected 17/14/0; TP/FP/FN 131/10/17; reference precision 0.9290780141843972 (131/141).
- DELETION: unique 321; exact/non-reference/unresolved 166/155/0; USE/KEEP/UNCERTAIN/FAILURE 148/145/3/25; accepted exact/non-reference/unresolved 139/9/0; rejected 27/146/0; TP/FP/FN 138/9/28; reference precision 0.9391891891891891 (139/148).

### Runtime accounting

- Candidate search seconds: 0.09951987018575892; vocabulary loading seconds: 0.31759214599151164; vocabulary rows: 141162.

### Fresh validator accounting

- Fresh observations / dispatches / uncertain deliveries: 493 / 493 / 0.
- USE/KEEP/UNCERTAIN/FAILURE: 289 / 172 / 3 / 29.
- Latency seconds (n/sum/mean/median/p95/max): 493 / 5283.875946435757 / 10.71780110838896 / 8.496985418023542 / 24.88524721498834 / 58.17827162001049.
- Reasoning tokens (n/sum/mean/median/p95/max): 464 / 217663 / 469.10129310344826 / 403.0 / 973 / 1784.
- Output tokens (n/sum/mean/median/p95/max): 464 / 221025 / 476.3469827586207 / 411.0 / 981 / 1792.

### Comparison with frozen 007-i BEST

- Basis: validated+fallback; exact deltas are 007-j minus frozen 007-i BEST. Protected/outside differences are reported as current counts and deltas.
- dassle-spelling/all: TP/FP/FN 822/154/693 vs 727/172/788 (delta +95/-18/-95); precision/recall/F0.5 0.8422131147540983/0.5425742574257426/0.7584425170695701 vs 0.8086763070077865/0.47986798679867987/0.7112111132850714 (delta +0.03353680774631185/+0.06270627062706274/+0.04723140378449875); introduced edit units 977 vs 900 (delta +77); preservation changed cases/edit units n/a; operational failures 32 vs 36 (delta -4); protected/outside 0/0 (delta +0/+0).
- dassle-spelling/initial-u/v: TP/FP/FN 42/7/33 vs 47/5/28 (delta -5/+2/+5); precision/recall/F0.5 0.8571428571428571/0.56/0.7749077490774908 vs 0.9038461538461539/0.6266666666666667/0.8303886925795053 (delta -0.04670329670329676/-0.06666666666666665/-0.05548094350201449); introduced edit units 49 vs 52 (delta -3); preservation changed cases/edit units n/a; operational failures 3 vs 3 (delta +0); protected/outside 0/0 (delta +0/+0).
- dassle-spelling/without-initial-u/v: TP/FP/FN 780/147/660 vs 680/167/760 (delta +100/-20/-100); precision/recall/F0.5 0.8414239482200647/0.5416666666666666/0.7575757575757577 vs 0.8028335301062574/0.4722222222222222/0.7042253521126761 (delta +0.03859041811380737/+0.06944444444444442/+0.05335040546308156); introduced edit units 928 vs 848 (delta +80); preservation changed cases/edit units n/a; operational failures 29 vs 33 (delta -4); protected/outside 0/0 (delta +0/+0).
- dassle-spelling-preservation/all: TP/FP/FN 0/101/0 vs 0/97/0 (delta +0/+4/+0); precision/recall/F0.5 0.0/0.0/0.0 vs 0.0/0.0/0.0 (delta +0.0/+0.0/+0.0); introduced edit units 101 vs 97 (delta +4); preservation changed cases/edit units 93/101 vs 91/97 (delta +2/+4); operational failures 23 vs 23 (delta +0); protected/outside 0/0 (delta +0/+0).

## Boundaries

- Reuse requires exact source-row, coordinate, sentence, candidate, request, prompt, deployment, parser, and persisted-response identity; reuse by text alone is rejected.
- C=0 and C>1 candidates use the unchanged baseline path; only C=1 reaches validation.
- No baseline response is resampled. PR #8 remains open and unmerged.
- This report does not authorize integration, merge, release, deployment, or product linguistic acceptance.

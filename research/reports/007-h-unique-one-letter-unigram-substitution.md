# 007-h unique one-letter unigram substitution

EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

One owner-authorized offline paired calculation over frozen DASSLE data.
English suppression precedes lookup; C>1 falls through; no frequency,
ordering, context, u/v, normalization, or model tie-break is used.

## Frozen identity

- Paired records: 2973 (1,487 spelling; 1,486 preservation).
- Caller-verified committed implementation: 65ba55ef3ff84bda4202190e589d45721409287b.
- Baseline configuration: 4c748b8e9711148c008d4157edef209a21531a2412745f230069215d3ddc5d29.
- Baseline results: 3a75c4dac3d77db7c865d363197efc368898c53b8b092abbc14451052354700f.
- Exact unigram vocabulary rows: 141162.
- Actual experiment model/network calls: 0 / 0.

## Required views

### Spelling all
- Stage-entering OOV / English suppressed: 2001 / 7
- C=0 / C=1 / C>1: 1011 / 571 / 419
- Unique accepted / applied / rolled back: 571 / 557 / 14
- Exact-reference / non-reference / unresolved: 346 / 210 / 1
- Mechanical precision (denominator 556): 0.6223021582733813
- Spelling-gold recall (denominator 1515): 0.22838283828382838
- Fallback edits: 508
- Targets not mechanically applied (fallthrough or document rollback): 2001 - 557 = 1444
- Lookup comparisons: 31084860
- Calls baseline first/retry/total: 2001 / 209 / 2210
- Calls projected first/retry/total: 1430 / 168 / 1598
- Calls avoided first/retry/total: 571 / 41 / 612
- Failures baseline/projected/avoided/introduced: 40 / 33 / 7 / 0
- Score baseline TP/FP/FN: 604 / 193 / 911
- Score new TP/FP/FN: 704 / 345 / 811
- Score baseline precision/recall/F0.5: 0.7578419071518193 / 0.39867986798679866 / 0.6421433127790771
- Score new precision/recall/F0.5: 0.6711153479504289 / 0.4646864686468647 / 0.6163544037821747
### Initial-u/v (75 frozen identities)
- Stage-entering OOV / English suppressed: 114 / 0
- C=0 / C=1 / C>1: 27 / 58 / 29
- Unique accepted / applied / rolled back: 58 / 57 / 1
- Exact-reference / non-reference / unresolved: 48 / 9 / 0
- Mechanical precision (denominator 57): 0.8421052631578947
- Spelling-gold recall (denominator 75): 0.64
- Fallback edits: 7
- Targets not mechanically applied (fallthrough or document rollback): 114 - 57 = 57
- Lookup comparisons: 1835077
- Calls baseline first/retry/total: 114 / 9 / 123
- Calls projected first/retry/total: 56 / 6 / 62
- Calls avoided first/retry/total: 58 / 3 / 61
- Failures baseline/projected/avoided/introduced: 5 / 3 / 2 / 0
- Score baseline TP/FP/FN: 28 / 11 / 47
- Score new TP/FP/FN: 51 / 12 / 24
- Score baseline precision/recall/F0.5: 0.717948717948718 / 0.37333333333333335 / 0.6060606060606061
- Score new precision/recall/F0.5: 0.8095238095238095 / 0.68 / 0.7798165137614678
### Spelling without initial-u/v
- Stage-entering OOV / English suppressed: 1887 / 7
- C=0 / C=1 / C>1: 984 / 513 / 390
- Unique accepted / applied / rolled back: 513 / 500 / 13
- Exact-reference / non-reference / unresolved: 298 / 201 / 1
- Mechanical precision (denominator 499): 0.5971943887775552
- Spelling-gold recall (denominator 1440): 0.20694444444444443
- Fallback edits: 501
- Targets not mechanically applied (fallthrough or document rollback): 1887 - 500 = 1387
- Lookup comparisons: 29249783
- Calls baseline first/retry/total: 1887 / 200 / 2087
- Calls projected first/retry/total: 1374 / 162 / 1536
- Calls avoided first/retry/total: 513 / 38 / 551
- Failures baseline/projected/avoided/introduced: 35 / 30 / 5 / 0
- Score baseline TP/FP/FN: 576 / 182 / 864
- Score new TP/FP/FN: 653 / 333 / 787
- Score baseline precision/recall/F0.5: 0.7598944591029023 / 0.4 / 0.6440071556350626
- Score new precision/recall/F0.5: 0.6622718052738337 / 0.4534722222222222 / 0.6064264487369986
### Preservation all
- Stage-entering OOV / English suppressed: 920 / 5
- C=0 / C=1 / C>1: 588 / 164 / 168
- Unique accepted / applied / rolled back: 164 / 158 / 6
- Exact-reference / non-reference / unresolved: 0 / 158 / 0
- Mechanical precision (denominator 158): 0.0
- Spelling-gold recall: n/a for preservation
- Fallback edits: 76
- Targets not mechanically applied (fallthrough or document rollback): 920 - 158 = 762
- Lookup comparisons: 13915053
- Calls baseline first/retry/total: 920 / 92 / 1012
- Calls projected first/retry/total: 756 / 79 / 835
- Calls avoided first/retry/total: 164 / 13 / 177
- Failures baseline/projected/avoided/introduced: 23 / 19 / 4 / 0
- Score baseline TP/FP/FN: 0 / 93 / 0
- Score new TP/FP/FN: 0 / 234 / 0
- Score baseline precision/recall/F0.5: 0.0 / 0.0 / 0.0
- Score new precision/recall/F0.5: 0.0 / 0.0 / 0.0

## Runtime and integrity

- Vocabulary load seconds: 0.3400516689871438.
- Candidate lookup seconds: 105.78110258010565.
- Reused saved model time: 25721.435817593934.
- Protected/outside-span differences: 0 / 0.
- Preservation changed cases/edits: 197 / 234.

## Interpretation and stop

The resolvable fraction, accuracy, call savings, preservation effect,
u/v ablation, and frozen-fallback end-to-end scores are above.
Reference scoring can penalize valid alternatives; non-reference edits
are not semantic harm labels. Results do not authorize integration,
merge, release, deployment, or live inference.

## Publication-only recovery

- The frozen scientific aggregation was valid; publication projection failed afterward.
- The private aggregate RESULTS, REPORT, and MANIFEST were preserved byte-for-byte.
- The publication supplement exposes only the omitted `introduced_edits` field, derived with the existing scorer from frozen source/output pairs.
- No linguistic metric or case was changed; all other metrics are a deep copy of the frozen private aggregate.
- Calculation, aggregation, and publication implementation heads: 939ae8b1482f3b8b5cefba5b0e16d1fde580346d, 5a1808b5227ef3b277ccd1a070b514840bdb310b, 65ba55ef3ff84bda4202190e589d45721409287b.
- Publication-projection incident SHA-256: cb382883f4b9e179e6149e49a7df7fdb1f494b91cd91670dd31942a6895fb01c.
- Invalid publication-render incident SHA-256: fc4aebc9e179b3f82e5473da0619029a3d58717733128a5f2bbb32619c134650; the attempt was uncommitted and excluded, with scientific metrics unchanged.
- This recovery made no model or application network calls.

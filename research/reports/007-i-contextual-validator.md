# 007-i contextual validator

EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

One owner-authorized paired contextual validator experiment over frozen 007-h candidates.
No baseline response was resampled; both projections consume the same validator observation.

## Frozen identity

- Scheduled unique candidates: 735 (571 spelling; 164 preservation).
- Frozen live implementation head: e85600ffd91164440166ee33a20c3b84af50bfe6.
- Aggregation implementation head: 752569d13d153ee6d16528f4b278a5a567e0b218.
- Candidate manifest SHA-256: 70544b1dec158f1e72cfaae8fb2547d9ba6ea22c3cd7934e0b7341bce8617854.
- Prompt SHA-256: 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d.
- Immutable validator observations / dispatched attempts / uncertain deliveries: 735 / 735 / 0.

## Aggregation recovery

- The deterministic aggregation incident was a KeyError for the derived `valid_response_count` field inside `make_views`; no raw traceback or private payload was published.
- Existing observation records / dispatch records: 735 / 735; additional model/network calls: 0 / 0.
- Request-tree identity before and after: 2940 files, 4651774 bytes, d46b47754e2ba158ea099bfe556a84164e534610233426819d9114a455aea945 / d46b47754e2ba158ea099bfe556a84164e534610233426819d9114a455aea945; unchanged: True.
- Incident identity SHA-256: 598b707790e303811faef0ccf15898686225947d19fce44352bde05f75984f39.

## Required views

### dassle-spelling / all
- Rows / scheduled candidates: 1487 / 571.
- Validator decisions USE / KEEP / UNCERTAIN / FAILURE: 337 / 199 / 5 / 30.
- Attribution accepted exact-reference / non-reference / unresolved: 321 / 15 / 1.
- Attribution rejected exact-reference / non-reference / unresolved: 29 / 205 / 0.
- Unconditional / valid-response acceptance: 0.5901926444833625 / 0.6229205175600739.
- Reference-exact sensitivity (numerator / denominator): 321 / 350 = 0.9171428571428571.
- Baseline TP/FP/FN: 604 / 193 / 911.
- VALIDATED+FALLBACK TP/FP/FN: 727 / 172 / 788.
- VALIDATED-ONLY TP/FP/FN: 683 / 153 / 832.
- Baseline / fallback / only precision: 0.7578419071518193 / 0.8086763070077865 / 0.8169856459330144.
- Baseline / fallback / only recall: 0.39867986798679866 / 0.47986798679867987 / 0.4508250825082508.
- Baseline / fallback / only F0.5: 0.6421433127790771 / 0.7112111132850714 / 0.7028195101872813.
- Fallback calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 2001/209/2210 / 1430/168/1598 / 337/25/362 / -234/-16/-250 / 571 / 1664/184/2419.
- Only calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 2001/209/2210 / 1430/168/1598 / 571/41/612 / 0/0/0 / 571 / 1430/168/2169.
- Protected/outside differences fallback: 0 / 0.
- Protected/outside differences only: 0 / 0.

### dassle-spelling / initial_uv
- Rows / scheduled candidates: 75 / 58.
- Validator decisions USE / KEEP / UNCERTAIN / FAILURE: 44 / 12 / 0 / 2.
- Attribution accepted exact-reference / non-reference / unresolved: 43 / 1 / 0.
- Attribution rejected exact-reference / non-reference / unresolved: 5 / 9 / 0.
- Unconditional / valid-response acceptance: 0.7586206896551724 / 0.7857142857142857.
- Reference-exact sensitivity (numerator / denominator): 43 / 48 = 0.8958333333333334.
- Baseline TP/FP/FN: 28 / 11 / 47.
- VALIDATED+FALLBACK TP/FP/FN: 47 / 5 / 28.
- VALIDATED-ONLY TP/FP/FN: 46 / 4 / 29.
- Baseline / fallback / only precision: 0.717948717948718 / 0.9038461538461539 / 0.92.
- Baseline / fallback / only recall: 0.37333333333333335 / 0.6266666666666667 / 0.6133333333333333.
- Baseline / fallback / only F0.5: 0.6060606060606061 / 0.8303886925795053 / 0.8363636363636364.
- Fallback calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 114/9/123 / 56/6/62 / 44/1/45 / -14/-2/-16 / 58 / 70/8/136.
- Only calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 114/9/123 / 56/6/62 / 58/3/61 / 0/0/0 / 58 / 56/6/120.
- Protected/outside differences fallback: 0 / 0.
- Protected/outside differences only: 0 / 0.

### dassle-spelling / without_initial_uv
- Rows / scheduled candidates: 1412 / 513.
- Validator decisions USE / KEEP / UNCERTAIN / FAILURE: 293 / 187 / 5 / 28.
- Attribution accepted exact-reference / non-reference / unresolved: 278 / 14 / 1.
- Attribution rejected exact-reference / non-reference / unresolved: 24 / 196 / 0.
- Unconditional / valid-response acceptance: 0.571150097465887 / 0.6041237113402061.
- Reference-exact sensitivity (numerator / denominator): 278 / 302 = 0.9205298013245033.
- Baseline TP/FP/FN: 576 / 182 / 864.
- VALIDATED+FALLBACK TP/FP/FN: 680 / 167 / 760.
- VALIDATED-ONLY TP/FP/FN: 637 / 149 / 803.
- Baseline / fallback / only precision: 0.7598944591029023 / 0.8028335301062574 / 0.8104325699745547.
- Baseline / fallback / only recall: 0.4 / 0.4722222222222222 / 0.4423611111111111.
- Baseline / fallback / only F0.5: 0.6440071556350626 / 0.7042253521126761 / 0.6948080279232113.
- Fallback calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 1887/200/2087 / 1374/162/1536 / 293/24/317 / -220/-14/-234 / 513 / 1594/176/2283.
- Only calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 1887/200/2087 / 1374/162/1536 / 513/38/551 / 0/0/0 / 513 / 1374/162/2049.
- Protected/outside differences fallback: 0 / 0.
- Protected/outside differences only: 0 / 0.

### dassle-spelling-preservation / all
- Rows / scheduled candidates: 1486 / 164.
- Validator decisions USE / KEEP / UNCERTAIN / FAILURE: 12 / 136 / 0 / 16.
- Attribution accepted exact-reference / non-reference / unresolved: 0 / 12 / 0.
- Attribution rejected exact-reference / non-reference / unresolved: 0 / 152 / 0.
- Unconditional / valid-response acceptance: 0.07317073170731707 / 0.08108108108108109.
- Reference-exact sensitivity (numerator / denominator): 0 / 0 = None.
- Baseline TP/FP/FN: 0 / 93 / 0.
- VALIDATED+FALLBACK TP/FP/FN: 0 / 97 / 0.
- VALIDATED-ONLY TP/FP/FN: 0 / 87 / 0.
- Baseline / fallback / only precision: 0.0 / 0.0 / 0.0.
- Baseline / fallback / only recall: 0.0 / 0.0 / 0.0.
- Baseline / fallback / only F0.5: 0.0 / 0.0 / 0.0.
- Fallback calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 920/92/1012 / 756/79/835 / 12/2/14 / -152/-11/-163 / 164 / 908/90/1162.
- Only calls baseline / unrestricted-007h / avoided-baseline / avoided-007h / validator-added / net (first/retry/total): 920/92/1012 / 756/79/835 / 164/13/177 / 0/0/0 / 164 / 756/79/999.
- Protected/outside differences fallback: 0 / 0.
- Protected/outside differences only: 0 / 0.

- Preservation changed cases/edit units fallback and only: 91 / 97 and 83 / 87.

## Runtime and limitations

- Global validator observations/decisions/failures: 735 / {'USE_CANDIDATE': 349, 'KEEP_ORIGINAL': 335, 'UNCERTAIN': 5} / {'PROTOCOL_validator choice is not exact': 46}.
- Global dispatched attempts / uncertain deliveries: 735 / 0.
- Global latency seconds (n / median / p95 / max): 735 / 7.1840441139938775 / 20.864024336013244 / 46.94347519101575.
- Worker count: 8; at most one in-flight call per worker.
- The validator is a strict binary choice protocol. Extra text, malformed JSON, wrong model/effort, incomplete status, missing token accounting, timeout, or transport failure is a distinct conservative failure.
- Reference scoring can penalize valid alternatives. Non-reference changes are not semantic harm labels.
- This result does not authorize integration, merge, release, deployment, or product linguistic acceptance.

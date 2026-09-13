# low-word-only-retry

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: How did strict word-only retry parsing behave at the first stopped execution?
- Authorized change: low-thinking word-only corrective retry with continuation
- Initial status: `STOPPED_ON_OUTER_WHITESPACE`; final status: `COMPLETED_WITH_WHITESPACE_ONLY_CONTINUATION`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/low-word-only-retry-20260909.0Hk0P9`; native path and payloads are not published.

## Configuration projection

- Historical wire keys: `model, stream, store, input, include_reasoning, reasoning`.
- Variant-specific content: first contextual sentence/target, raw rejected word only on retry.
- Model-call policy: `WORD_ONLY_RETRY; SAVED_RESPONSE_CONTINUATION_WITHOUT_RESAMPLING`.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `cases` | `32` |
| `first_pass_calls_reused` | `10` |
| `first_pass_calls_executed` | `0` |
| `total_word_only_calls` | `2` |
| `new_continuation_calls` | `1` |
| `first_response_resampled` | `False` |
| `applied_edits` | `4` |
| `applied_retry_edits` | `0` |
| `exact_gold_repairs` | `3` |
| `unchanged_controls` | `25` |
| `protected_differences` | `0` |
| `outside_edit_differences` | `0` |
| `total_word_only_http_seconds` | `20.005273504997604` |
| `median_word_only_http_seconds` | `10.002636752498802` |
| `max_word_only_http_seconds` | `14.27844430800178` |
| `model_calls` | `2` |
| `network_calls` | `2` |
| `initial_status` | `STOPPED_ON_OUTER_WHITESPACE` |
| `final_status` | `COMPLETED_WITH_WHITESPACE_ONLY_CONTINUATION` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| none enumerated | `NOT_APPLICABLE` | `UNAVAILABLE` | `UNAVAILABLE` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/low-word-only-retry.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

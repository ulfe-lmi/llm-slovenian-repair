# nonthinking-mechanical

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What did the frozen direct reviewer do when reasoning was disabled?
- Authorized change: direct review with reasoning disabled and mechanical-only acceptance
- Status: `COMPLETED`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/nonthinking-mechanical-20260909.5m8LKG`; native path and payloads are not published.

## Configuration projection

- Variant-specific wire/content boundary: The early direct family sends one selected-target review with reasoning disabled and mechanical-only acceptance. See [configuration](../configs/nonthinking-mechanical.json) fields historical_wire_keys, historical_content, and model_call_policy; no later variant's content is inferred.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `applied_edits` | `4` |
| `cases` | `32` |
| `changed_controls` | `1` |
| `exact_gold_repairs` | `2` |
| `missed_gold_errors` | `5` |
| `mode` | `reasoning_none` |
| `model_calls` | `10` |
| `proposed_edits` | `4` |
| `qualified_calls` | `10` |
| `retry_calls` | `0` |
| `review_calls` | `10` |
| `status` | `COMPLETED` |
| `total_calls` | `10` |
| `unchanged_controls` | `24` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| none enumerated | `NOT_APPLICABLE` | `UNAVAILABLE` | `UNAVAILABLE` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/nonthinking-mechanical.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

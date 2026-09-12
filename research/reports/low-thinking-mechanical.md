# low-thinking-mechanical

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What did the frozen direct reviewer do with low reasoning?
- Authorized change: direct review with low reasoning and mechanical-only acceptance
- Status: `COMPLETED`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/low-thinking-mechanical-20260909.Ih2OFD`; native path and payloads are not published.

## Configuration projection

- Historical wire keys: `model`, `stream`, `store`, `input`, `include_reasoning`, `reasoning`.
- Content sent in `input`: the completed source sentence and selected target; the contextual retry additionally carries its original sentence/target/rejected replacement/missing-word evidence.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `applied_edits` | `6` |
| `cases` | `32` |
| `changed_controls` | `1` |
| `exact_gold_repairs` | `3` |
| `missed_gold_errors` | `4` |
| `mode` | `reasoning_low` |
| `model_calls` | `10` |
| `proposed_edits` | `6` |
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

- [Configuration](../configs/low-thinking-mechanical.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

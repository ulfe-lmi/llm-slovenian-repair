# low-unigram-retry

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What changed when unigram-uncertain proposals received one contextual corrective retry?
- Authorized change: low-thinking unigram post-check and one contextual JSON corrective retry
- Status: `COMPLETED`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/low-unigram-retry-20260909.Wb0TI7`; native path and payloads are not published.

## Configuration projection

- Generic prompt: `Ali se ti zdi uporaba besede oziroma besedne zveze X najboljša naravna izbira v tem slovenskem stavku? Če ne, s čim bi jo nadomestil?`
- Sent fields: model, preserved reasoning setting, generic prompt, bounded target metadata.
- Omitted fields: conversation history, filled dataset text, gold strings, private response bodies, credentials.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `applied_edits` | `4` |
| `applied_retry_edits` | `0` |
| `cases` | `32` |
| `changed_controls` | `0` |
| `exact_gold_repairs` | `3` |
| `missed_gold_errors` | `4` |
| `model_calls` | `2` |
| `new_corrective_calls` | `2` |
| `retry_calls` | `2` |
| `reused_calls` | `10` |
| `review_calls` | `0` |
| `status` | `COMPLETED` |
| `total_calls` | `2` |
| `unchanged_controls` | `25` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| none enumerated | `NOT_APPLICABLE` | `UNAVAILABLE` | `UNAVAILABLE` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/low-unigram-retry.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

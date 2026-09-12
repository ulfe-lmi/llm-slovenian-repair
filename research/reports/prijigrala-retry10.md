# prijigrala-retry10

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What happened in the one-target retry-limit-ten contextual case?
- Authorized change: one-target contextual review with retry limit ten
- Status: `COMPLETE`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/prijigrala-retry10-20260911.3E6HOg`; native path and payloads are not published.

## Configuration projection

- Historical wire keys: `model, stream, store, input, include_reasoning, reasoning`.
- Variant-specific content: one sentence/target, same raw first rejected replacement.
- Model-call policy: `ONE_TARGET; MAXIMUM_TEN_CORRECTIVE_RETRIES`.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `corrective_calls` | `3` |
| `model_calls` | `4` |
| `outcome` | `ACCEPTED` |
| `status` | `ACCEPTED` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| none enumerated | `NOT_APPLICABLE` | `UNAVAILABLE` | `UNAVAILABLE` |

## Interpretation and limitations

Clock accounting and logical reconstruction are retained as observations; the one-target result is not a general retry claim.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/prijigrala-retry10.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

# ten-run-expression-retry-low

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What persisted across ten scheduled trials of the expression retry?
- Authorized change: ten-trial context-free expression retry
- Status: `COMPLETED_WITH_STOPPED_TRIALS`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/ten-run-expression-retry-low-20260909.xJhqYm`; native path and payloads are not published.

## Configuration projection

- Historical wire keys: `model, stream, store, input, include_reasoning, reasoning`.
- Variant-specific content: same cases per trial, symmetric case adjustment, raw rejected expression.
- Model-call policy: `TEN_PREDETERMINED_TRIALS; STOPPED_TRIALS_CONTINUE_UNCHANGED`.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `available_case_instances_including_partial` | `319` |
| `available_eligible_word_instances_including_partial` | `1454` |
| `available_known_error_instances_including_partial` | `69` |
| `complete_trials` | `9` |
| `first_calls` | `90` |
| `model_calls` | `103` |
| `operational_failures` | `1` |
| `reasoning_tokens` | `44662` |
| `retry_calls` | `13` |
| `scheduled_trials` | `10` |
| `status` | `COMPLETED_WITH_STOPPED_TRIALS` |
| `stopped_trials` | `1` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `ten-run-expression-retry-low/01` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `6a43e57912e7e494ec9ad3a60c04f1fd65fff67cf6911fc0d9df8c1ddbf38f45` |
| `ten-run-expression-retry-low/02` | `STOPPED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `dc017671fdb02df5a85213c1a59591c8f02e086ff0d828ef07d9bf64bee39e12` |
| `ten-run-expression-retry-low/03` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `4ec0b9a9c6f8c3cee28527eede6d0f9895bd1ea01099f048a0424de1d6589833` |
| `ten-run-expression-retry-low/04` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `a43dcd8e470e09fbba4b66ee853cf2ccf1a36a907a06453a9678bb66ed649948` |
| `ten-run-expression-retry-low/05` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `519d045bee878fa6f914b87b55ed5819dd08a1e46bf7cc7effe5fb63ed8358c3` |
| `ten-run-expression-retry-low/06` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `9e179ddfa4cda478bce3a2c0275ccc2a39011af193cb5fb3b18cab5ea745d2d8` |
| `ten-run-expression-retry-low/07` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `d1127cb7afdc04a3692615642163303382e730343abc63d082c81c9ce5a24685` |
| `ten-run-expression-retry-low/08` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `d37101d55c64311ffe2ca5d2abfe307ed75bba6059c73e3a9b2b9fa782a75771` |
| `ten-run-expression-retry-low/09` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `df40dc72d882f192a839ace3b6cab82b8bd1ba9c087fb6e9dcee13a4a631a947` |
| `ten-run-expression-retry-low/10` | `COMPLETED` | `3ce7d962d95af6d836ebcf268df9d79811c17db95a606bd30c54f6e6ac558249` | `165b8e75df20fb8f0acbd05022d4a48860a0b5ffc7b8f64e272318edbcc36411` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/ten-run-expression-retry-low.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

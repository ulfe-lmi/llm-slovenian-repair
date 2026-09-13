# full-campaign8

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What did the complete nine-phase eight-worker campaign establish locally, and what remained access-blocked?
- Authorized change: final full eight-worker A100 campaign
- Status: `COMPLETED_LOCAL_CAMPAIGN_REMOTE_SCORING_PENDING`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/full-campaign8-20260911.XLAbaa`; native path and payloads are not published.

## Configuration projection

- Historical wire keys: `model, stream, store, input, include_reasoning, reasoning`.
- Variant-specific content: completed source sentence, selected target.
- Model-call policy: `CALLER-OWNED-HISTORICAL-DRIVER`.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `cases` | `16375` |
| `completed_phases` | `9` |
| `deployment` | `A100_FP8_ONLY` |
| `distinct_calls` | `39184` |
| `inherited_calls` | `7268` |
| `method_records` | `65500` |
| `model_calls` | `39184` |
| `new_model_calls` | `31916` |
| `status` | `COMPLETED_LOCAL_CAMPAIGN_REMOTE_SCORING_PENDING` |
| `verified_checkpoints` | `1419` |
| `workers` | `8` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `full-campaign8/dassle` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `e61efc4ffd8872d43a55b11040f5d8793eaceafa9783cbead053aab66195e56f` |
| `full-campaign8/dassle-preservation` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `5912cffb293ae5729fde3d75c0f551b6588e10b0b9c0ceb4ff42d1e744f1c664` |
| `full-campaign8/multigec-dev` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `d05acc0491c639e212959451d871badf4f2ccb8575759ef61919ff3df74c1197` |
| `full-campaign8/multigec-dev-preservation` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `54d6b272fe8fd20feb3595e377a476d1abfcaa2f1be601b5e8264414f892aff2` |
| `full-campaign8/multigec-test` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `ced32526811072f244066a35494e1b73a9b23b34a7470b3f689522eb0051d920` |
| `full-campaign8/multigec-train` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `f992acc3f45b19b1359f673febc7437aa3448d7218f8e718e86dc7b591ff13af` |
| `full-campaign8/slobench` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `cccc67896a6088ef1eab12f7928354329b43951fafa8189980a6bfb042db0b1a` |
| `full-campaign8/solar-canonical` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `8e6991f8bb00cde148010d448992c670f6368347b0bd3515cbf98ed5f907cba7` |
| `full-campaign8/solar-canonical-preservation` | `COMPLETED` | `b8cf04f9b703d62ea3b9c75e1ac3b1ddf020840aea45fd47ac75c56159238ca1` | `00ec176efb53968ca179439095e453c64920a3bcfe656800dfe5382e9491b96d` |

## Interpretation and limitations

Official and custom denominators remain separate. SloBench and MultiGEC-test have no references for correctness/harm interpretation; remote scoring and Deployment B remain blocked/excluded.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/full-campaign8.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

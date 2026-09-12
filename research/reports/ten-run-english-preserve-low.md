# ten-run-english-preserve-low

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: How did original Slovene-unigram absence plus English attestation change review eligibility?
- Authorized change: ten-trial English-preservation pre-review
- Status: `COMPLETED_ALL_TEN_TRIALS`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/ten-run-english-preserve-low-20260909.AQnnRH`; native path and payloads are not published.

## Configuration projection

- Variant-specific wire/content boundary: Each scheduled trial applies numeric English suppression to original absent targets before contextual review. See [configuration](../configs/ten-run-english-preserve-low.json) fields historical_wire_keys, historical_content, and model_call_policy; no later variant's content is inferred.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `available_case_instances_including_partial` | `320` |
| `available_eligible_word_instances_including_partial` | `1460` |
| `available_known_error_instances_including_partial` | `70` |
| `complete_trials` | `10` |
| `corrective_calls` | `15` |
| `first_calls` | `80` |
| `model_calls` | `95` |
| `operational_failures` | `0` |
| `reasoning_tokens` | `45936` |
| `retry_calls` | `15` |
| `scheduled_trials` | `10` |
| `status` | `COMPLETED` |
| `stopped_trials` | `0` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `ten-run-english-preserve-low/01` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `f95e12d85d6abc019d6a97500d93a18649702519256697db3ed1442ef3bf8ceb` |
| `ten-run-english-preserve-low/02` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `78ec2df7e5c681b9fa64cf35c4639a188f72f11f932bc89ac4b09b0134ad457c` |
| `ten-run-english-preserve-low/03` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `a2030157bb5df6f4589d3b79d92e6ebd769882bba0df6f644f3af75e5daffcfe` |
| `ten-run-english-preserve-low/04` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `6c663d6a167848b9d65b17ed7ab459bf8b920d6efac23b0262a5232eaf219274` |
| `ten-run-english-preserve-low/05` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `2d3fa9204e5834ed9be69e0155ad2e8f85e3af3d739e002dc937cfefa5bb06ed` |
| `ten-run-english-preserve-low/06` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `d0875562d7a28964e78896b2463b6b2ba6634157dfd98874817902be713a4bf7` |
| `ten-run-english-preserve-low/07` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `9ab410092f0a8494680d18051c7a46c53d723f2087d1ceb551f601a54bca4b10` |
| `ten-run-english-preserve-low/08` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `73547122a145c1b26425377324e29377a2e930d005027d17d97a17a2f242f9c5` |
| `ten-run-english-preserve-low/09` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `547a96a07f9641c87877a371e16a237e512930b61931db71b5b8c7b38e701817` |
| `ten-run-english-preserve-low/10` | `COMPLETED` | `ff6e8a3fdeb727618e12c9ff8a449171a499eb97c950cda75283fc990f53ecb5` | `5077ac22fbc28cfbbff079b7bc5731ed5274104a4d8f847ab0ecf8867c93c427` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/ten-run-english-preserve-low.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

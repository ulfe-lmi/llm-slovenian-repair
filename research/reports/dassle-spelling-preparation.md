# dassle-spelling-preparation

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What did the DASSLE spelling preparation and controlled execution preserve, including worker incidents?
- Authorized change: DASSLE spelling preparation, detector evidence, and controlled execution
- Status: `COMPLETE_LOCAL_EVIDENCE_WITH_RECORDED_INCIDENTS`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/dassle-spelling-preparation-20260910.whOa6K`; native path and payloads are not published.

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
| `deployment` | `A100_ONLY` |
| `inference_coordinator_status` | `INDEPENDENT_WORKERS_FINISHED_WITH_INCIDENTS` |
| `method_records` | `11892` |
| `model_calls` | `6195` |
| `preservation_cases` | `1486` |
| `spelling_cases` | `1487` |
| `status` | `COMPLETE_LOCAL_SCIENTIFIC_EVIDENCE_VERIFIED_WITH_RECORDED_INCIDENTS` |
| `unique_model_calls` | `6195` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `dassle-spelling-preparation/preparation` | `RECORDED` | `1c414b39c9824cab71ddff4f76e02626739dad2f19f38a3042b52ac194bed039` | `07823b5eefb7cfce0ce241fb5de1259026eccd1c19a0a5c5d56e7cd22e4185ac` |
| `dassle-spelling-preparation/parallel4` | `RECORDED` | `07823b5eefb7cfce0ce241fb5de1259026eccd1c19a0a5c5d56e7cd22e4185ac` | `07823b5eefb7cfce0ce241fb5de1259026eccd1c19a0a5c5d56e7cd22e4185ac` |
| `dassle-spelling-preparation/recovery` | `RECORDED` | `b8c5ee919bb23ebd6bb250eaa0c481e36c5762f05d1fd1175a8903d9c5d1ca38` | `07823b5eefb7cfce0ce241fb5de1259026eccd1c19a0a5c5d56e7cd22e4185ac` |
| `dassle-spelling-preparation/final-scoring` | `RECORDED` | `d43005918bee30a84a452341a20fd7981814eb1ad5719152ac069a31dbd59560` | `07823b5eefb7cfce0ce241fb5de1259026eccd1c19a0a5c5d56e7cd22e4185ac` |

## Interpretation and limitations

Four-worker and recovery incidents remain operational evidence, not a quality label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/dassle-spelling-preparation.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

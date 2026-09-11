# large-evaluation-capped

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What evidence survived the started capped external campaign before completion?
- Authorized change: capped external evaluation preparation
- Status: `INFERENCE_STARTED_NOT_COMPLETED`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/large-evaluation-20260909.ZowPyK`; native path and payloads are not published.

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
| `status` | `RUNNING` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `large-evaluation-capped/multigec-dev` | `RECORDED` | `babfbe225acdb3e8df1bd714fc04d85ba28448a888f16982ef23390638088c71` | `d34f0378d1ffa5d99d1404d63afb18863ae89c70f300ff00299c4f68483ef0ef` |
| `large-evaluation-capped/multigec-train` | `RECORDED` | `babfbe225acdb3e8df1bd714fc04d85ba28448a888f16982ef23390638088c71` | `0fef6de78d17f4cfdf1bb89674139d33969c9aac296cacf9518013d830976b2f` |

## Interpretation and limitations

A RUNNING snapshot means inference started, not that the campaign completed.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/large-evaluation-capped.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

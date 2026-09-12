# large-evaluation-uncapped

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What evidence was available before the owner redirected the uncapped campaign?
- Authorized change: owner-directed uncapped external campaign
- Status: `PAUSED_BY_HUMAN_RELEVANCE_CHANGE`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/large-evaluation-uncapped-20260910.faME3U`; native path and payloads are not published.

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
| `status` | `PAUSED_BY_HUMAN_RELEVANCE_CHANGE` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `large-evaluation-uncapped/multigec-train` | `RECORDED` | `0687076994cc5fd31357fb1d15a1d63c6c15a4386b484edaa290fa0887b4614c` | `d0874fbd99b068a3347953a7eee709d1500e1126ee86fa3465244446fd23c4b1` |

## Interpretation and limitations

The human relevance change paused this campaign; no later phase is inferred.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/large-evaluation-uncapped.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

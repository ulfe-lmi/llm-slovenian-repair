# 007-b-replacement

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: Did the owner-authorized replacement reach the model boundary?
- Authorized change: human-authorized replacement execution
- Status: `FAILED_BEFORE_PROXY_CONTACT`; an old `RUNNING` marker is not completion.
- Private logical root: `recovery-executions/007-b-human-replacement-20260909.MnH1Qb`; native path and payloads are not published.

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

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `007-b-replacement/heldout` | `RECORDED` | `310c07d5b73c8e26ddcce444e4407009c3e30db406c336115c3b2c5dfcf4cf60` | `UNAVAILABLE` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/007-b-replacement.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

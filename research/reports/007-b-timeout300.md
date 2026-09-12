# 007-b-timeout300

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What evidence survived the controlled timeout-300 replacement and where is its case/trace association invalid?
- Authorized change: human-authorized timeout-300 replacement execution
- Status: `COMPLETED_CONTROLLED_WITH_INVALID_TRACE_ASSOCIATION`; an old `RUNNING` marker is not completion.
- Private logical root: `recovery-executions/007-b-human-timeout300-20260909.NWGrtX`; native path and payloads are not published.

## Configuration projection

- Variant-specific wire/content boundary: Controlled model calls and the invalid case/trace association remain separate from the replacement attempt. See [configuration](../configs/007-b-timeout300.json) fields historical_wire_keys, historical_content, and model_call_policy; no later variant's content is inferred.
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
| `007-b-timeout300/heldout` | `RECORDED` | `53580ef330f3f95154871d6bd813cfc335677a8eda4ec7e6937627cf19030d92` | `390eaa71ee64f0d70572af0829184e924e8cfed1bae0d2d98a6f6b742846d4bb` |

## Interpretation and limitations

The timeout-300 association is not valid for case-level interpretation; preserve the controlled receipt without assigning it to a case.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/007-b-timeout300.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

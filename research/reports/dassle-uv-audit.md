# dassle-uv-audit

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: How many frozen DASSLE edit units matched the requested u/v categories and sensitivities?
- Authorized change: DASSLE exhaustive u/v mechanical audit and random-20 sample
- Status: `COMPLETE_EXHAUSTIVE_MECHANICAL_AUDIT`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/dassle-uv-audit-20260911.BGeMLs`; native path and payloads are not published.

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
| `gold_edit_units` | `8623` |
| `new_model_calls` | `0` |
| `status` | `COMPLETE_EXHAUSTIVE_MECHANICAL_AUDIT` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `dassle-uv-audit/exhaustive-u-v` | `COMPLETE` | `6d6fb695d420e22ceda4664c20286242151acccce57c381e7abd26415e17b153` | `6d6fb695d420e22ceda4664c20286242151acccce57c381e7abd26415e17b153` |
| `dassle-uv-audit/random-20` | `COMPLETE` | `3f7a6f50f83f5b3c3735cb91071abe4da39c53bbd612c88d9b381bbf0e6aa72c` | `6d6fb695d420e22ceda4664c20286242151acccce57c381e7abd26415e17b153` |

## Interpretation and limitations

The exhaustive and random-sample views are mechanical; u/v membership is not a semantic judgment.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/dassle-uv-audit.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

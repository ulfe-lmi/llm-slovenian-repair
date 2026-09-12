# 007-b-replacement

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: Did the owner-authorized replacement reach the model boundary?
- Authorized change: human-authorized replacement execution
- Status: `FAILED_BEFORE_PROXY_CONTACT`; an old `RUNNING` marker is not completion.
- Private logical root: `recovery-executions/007-b-human-replacement-20260909.MnH1Qb`; native path and payloads are not published.

## Configuration projection

- Historical execution: the controlled held-out run contacted Qwen for 10 reviewer attempts; six were reviewer errors and four were valid structured decisions. The later workload has no valid proxy-contact evidence.
- Reproduction boundary: no fresh model request; caller-supplied data-free inputs only.
- Model-call policy: `REPRODUCTION_DEFAULT_ZERO_CALLS; HISTORICAL_HELDOUT_QWEN_CALLS_RECORDED; WORKLOAD_NO_VALID_PROXY_CONTACT_EVIDENCE`.
- Publicly omitted: source sentences, filled prompts, gold strings, replacements, response bodies, reasoning traces, credentials, and private endpoint/profile values.
- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.
- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.

## Numeric evidence

The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.

| Metric | Value |
| --- | ---: |
| `heldout_cases` | `32` |
| `heldout_selected_candidates` | `10` |
| `heldout_completed_reviewer_attempts` | `10` |
| `heldout_reviewer_errors` | `6` |
| `heldout_valid_structured_decisions` | `4` |
| `heldout_keep_decisions` | `2` |
| `heldout_replace_decisions` | `2` |
| `heldout_proposed_replacements` | `2` |
| `heldout_accepted_edits` | `0` |
| `heldout_exact_gold_repairs` | `0` |
| `heldout_missed_known_errors` | `7` |
| `heldout_protected_changes` | `0` |
| `heldout_controlled_reviewer_calls` | `10` |
| `reproduction_model_calls` | `0` |
| `reproduction_network_calls` | `0` |
| `workload_status` | `NO_VALID_PROXY_CONTACT_EVIDENCE` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `007-b-replacement/heldout` | `CONTROLLED_HELDOUT_QWEN_CONTACT_RECORDED` | `310c07d5b73c8e26ddcce444e4407009c3e30db406c336115c3b2c5dfcf4cf60` | `UNAVAILABLE` |

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

# ten-run-initial-case-low

Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.

## Identity and question

- Question: What persisted across ten scheduled trials of the symmetric case rule?
- Authorized change: ten-trial symmetric initial-case preservation
- Status: `COMPLETED_WITH_STOPPED_TRIALS`; an old `RUNNING` marker is not completion.
- Private logical root: `experiments/ten-run-initial-case-low-20260909.87bzTW`; native path and payloads are not published.

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
| `available_case_instances_including_partial` | `305` |
| `available_eligible_word_instances_including_partial` | `1393` |
| `available_known_error_instances_including_partial` | `67` |
| `complete_trials` | `8` |
| `completed_case_outputs` | `305` |
| `completed_trials` | `8` |
| `first_calls` | `87` |
| `model_calls` | `97` |
| `operational_failures` | `1` |
| `reasoning_tokens` | `39526` |
| `retry_calls` | `10` |
| `scheduled_trials` | `10` |
| `status` | `COMPLETED_WITH_STOPPED_TRIALS` |
| `stopped_trials` | `2` |

## Child runs and phases

| Child ID | Status | Source hash | Result hash |
| --- | --- | --- | --- |
| `ten-run-initial-case-low/01` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `5a48daf24c6d393fcb1d9c84f516ac504d2b755e51ce1e731a4a5ac0c1fc898d` |
| `ten-run-initial-case-low/02` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `3dac8bbb4489af32f2fa1152ef6166e4a204e78a88e45ec2f352e386a42da178` |
| `ten-run-initial-case-low/03` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `a1ca734737b09b1e2da67d60c6f8e355382cf4d37572a25dc7e04092ad570782` |
| `ten-run-initial-case-low/04` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `9dc80240ac8a8ab9f1a70222707b7c5df4b91cf1ef38125f6cc0bca6da2b9da3` |
| `ten-run-initial-case-low/05` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `d8129ffdaa54224feaf51b46b5c3c70bb534ed9dc97b93a8a213e34dcfd625a9` |
| `ten-run-initial-case-low/06` | `STOPPED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `7155324e3ab95f906c073ba5bbec1754f3617cee5e021d0aab7298d22568e1bc` |
| `ten-run-initial-case-low/07` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `b9e3f30ed48d10d2c5c8d36a9ad0ac49a419100ffe76d634b35b21b0dff853e1` |
| `ten-run-initial-case-low/08` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `089b9980b4da61abb058cc84f8684f15743f282dbc9e90250fde17aa4b72c612` |
| `ten-run-initial-case-low/09` | `STOPPED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `eb3a47b515891c9ae737cc6b305f5fea6f532a90991eab9e36d2beabab68a540` |
| `ten-run-initial-case-low/10` | `COMPLETED` | `bcd1195b428bf432445b9a554620dcd2764a07afc6e3ba13f9fde3b8e4ce61fa` | `0d7053098309b84a5420505ee4c7e6619c00be9e78611b3dd08f48190707c08c` |

## Interpretation and limitations

The preserved numerical result is reported without adding a semantic label.

Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.

## Reproduction and source links

- [Configuration](../configs/ten-run-initial-case-low.json)
- [Experiment catalog](../registry/experiments.json)
- [Source manifest](../registry/source-manifest.json)
- [Archive and relocation catalog](../registry/archive-catalog.json)
- [Curated source closure](../curated/)

Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.

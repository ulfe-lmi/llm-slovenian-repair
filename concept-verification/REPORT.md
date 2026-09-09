# Concept verification report — 007-b

**EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE**

## Decision

`INCONCLUSIVE` / `PARTIAL`. The frozen detector path remains reproducible, but
the one allowed live reviewer execution reached its bounded calls and then
failed in result bookkeeping before writing proposal evidence. The one allowed
eight-case Codex collection was attempted exactly once per case; all eight
invocations exited 2 before contacting the proxy because the installed CLI does
not accept the old `--ask-for-approval` option. No human-quality or
natural-workload conclusion is claimed. The corrected command builder and
review-sheet path are committed for review, but this round is not rerun.

## Frozen inputs and controlled evidence

The exact frozen config, manifest, dev split, held-out split, external index,
and frozen prompt identities are unchanged:

- held-out: 32 cases, 145 eligible words, 7 known errors;
- local-context, threshold 3: 10 candidates, recall 1.00, precision 0.700;
- unigram-only, threshold 3: 10 candidates, recall 1.00, precision 0.700;
- raw baseline: 7 known errors remaining;
- detector-only: 7 known errors remaining;
- reviewer/full pipeline: not measured in a persisted aggregate after the
  bookkeeping failure; no constants are presented as results;
- protected differences in completed focused tests: 0.

The two detector ablations are equal on this split; that is an observation, not
evidence that context is generally useless. Controlled fixture examples remain
project-authored; no external corpus rows or private model output is included.

The live reviewer runner was configured with the exact private reviewer URL,
model, and profile required by the order. It selected the same 10 candidates
and made one bounded sequential call per candidate, with no retry. A
`detector_only` aggregation-key defect raised after that call sequence, before
proposal/acceptance records were persisted. The defect is fixed; no second live
reviewer pass is permitted by this round.

## Workload and proxy evidence

The collector attempted eight actual `codex exec --profile qwen-neumann`
invocations with explicit `CODEX_HOME`, provider/base-URL override,
`--ephemeral`, loopback proxy, owned disposable work roots, and finite timeout.
All eight had exit code 2, zero valid event types, zero terminal responses, and
zero joined proxy traces. Therefore completed responses, latency aggregates,
assistant text pairs, tool-loop evidence, accepted edits, and protected-diff
workload metrics are unavailable. The tool-loop case was not counted as passed.

The focused fake upstream tests do pass for terminal-complete SSE that keeps
HTTP open, incomplete timeout, both `/v1` and no-`/v1` upstream bases, actual
non-200 status/content-type forwarding, comment/unknown-event preservation,
trace opt-in privacy, and exact patch invariance. The proxy binds loopback only,
does not retry, stops only after a delimited `response.completed`, and records
local traces only when an explicit trace directory is supplied. The fixed
collector command builder now uses the installed CLI’s supported noninteractive
approval bypass; it was not exercised against the model after the eight blocked
attempts.

The previous 007-a report’s six blocked collector cases remain visible in that
immutable report. This report supersedes only its interpretation that a human
review was the sole remaining follow-up; it does not hide or rewrite those six
cases or their bytes.

## Automatic score status

The committed aggregate summary is computed from the frozen detector result and
the eight blocked workload records. Its gate is `INCONCLUSIVE` because reviewer
proposal/acceptance metrics and human-labeled workload evidence are missing.
The human status remains `AWAITING_HUMAN_REVIEW`; no automatic count is a human
benefit or harm label. No harmful fraction, harmful-per-1000 rate, or workload
latency claim is fabricated.

## A–J answers

A. **Yes, provisionally:** the bounded detector found 10 candidates and all 7
known errors on the frozen held-out split.

B. **No:** the sparse external source provides evidence states, not semantic
proof or a complete denominator.

C. **Equal here:** local-context and unigram-only both measured 10 candidates,
1.00 recall, and 0.700 precision; general context benefit is unproven.

D. **Focused-boundary yes; live result unproven:** reviewer construction is
fresh and isolated in code/tests, but the live proposal records were not
persisted after the runner defect.

E. **Unproven:** strict acceptance and exact local evidence gates are exercised,
but no live accepted-repair sample survived for benefit/harm measurement.

F. **Yes in focused evidence:** original-coordinate patching preserves outside
slices and protected content; observed protected differences were zero.

G. **Yes in focused evidence:** terminal-complete buffered SSE is preserved,
including IDs, event ordering, comments, unknown blocks, and non-text fields.

H. **Blocked:** the actual Codex path was attempted eight times but the command
option error prevented model/proxy execution; no tool-loop proof exists.

I. **Provisionally plausible:** loopback, finite bounds, private cache handling,
and opt-in trace privacy are tested; live endpoint availability is not proven by
this round.

J. **No production decision:** remain `INCONCLUSIVE`; no merge, release,
deployment, milestone, or follow-on order is authorized.

## Limitations and reuse

This is an isolated standard-library experiment. It is not production API,
gateway, concurrency, morphology, deployment, or linguistic-quality evidence.
The source archives and derived index remain private external artifacts. Raw
reviewer/Codex responses and blinded sheets remain local ignored evidence only;
they are not copied into Git, reports, logs, or packages. Existing 001–005
contracts and the preserved 007-a concept seams were reused only within this
experimental subtree. The inherited application baseline remains a separate
known failure and is not altered or reclassified.

The single remaining discriminating action is to let strategy reconcile this
truthful partial round; no 007-c experiment or automatic roadmap resumption is
proposed.

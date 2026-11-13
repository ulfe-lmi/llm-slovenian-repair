# Evaluation

Software tests prove deterministic boundaries, not language quality. Linguistic
quality is **unmeasured** in the current proxy.

## Owner decision

No separate human evaluation dataset exists or is required. The owner excludes
it — not deferred, not optional — and nothing in this repository or its orders
creates an obligation for this dataset, its annotations or this evaluation.
That exclusion is scoped to this evaluation programme: the existing
independent-closure rule and the owner's milestone and deployment authority are
unaffected. Controlled or automatic checks under existing authorization remain
possible without any separate human dataset.

## Historical PLAN evaluation proposal (not a current gate)

The PLAN describes a historical evaluation design: real target outputs plus
correct/rare/technical negative controls; human labels for actual error,
acceptable alternative, style preference and required wider edit; approved
provenance; frozen calibration/held-out splits without duplicates or leakage.
Qwen is never the sole final judge of its own changes.

Its reporting design (historical, not a current obligation): precision with the
evaluated-edit count, harmful edits per originally correct words, unnecessary
style edits, detector vs repair coverage, domains/sample counts/uncertainty,
separate main/review usage, and latency/queue/CPU/memory. Zero observed harm in
a small clustered sample does not prove zero risk. Targets such as ~99%
precision or one harm per 10k words are goals, not authorization, and useful
measured benefit must coexist with the conservative gates even at low coverage.

No linguistic experiment, annotation or Qwen invocation occurred during
bootstrap.

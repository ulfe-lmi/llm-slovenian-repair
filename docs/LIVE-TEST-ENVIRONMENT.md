# Live test environment

Bounded, explicitly authorized live-model testing. Historical endpoint
assumptions are not defaults; do not treat old references as target-machine
configuration.

## Qualified native environment

The 035 rounds qualified the native RTX3090 boundary through the real
`proxy.main()` on one owned loopback port, using the native Responses route
`POST /responses` (relative to the operator-configured API base) with model
`qwen3.8-27b-rtx3090` for **both** the main and the review hop, explicit caller
Authorization, child-only in-process reviewer key, concurrency 1 and zero
auto-retry.

- **Final qualifying pair (035-d):** the useful trial delivered one approved
  exact original-span edit after one observed validated review, and the paired
  clean trial proved the genuine fully-observed zero-review control with an
  identical delivered answer — see the
  [035-d report](../oap/reports/035-d-useful-native-repair-and-policy-regressions.md).
- **Earlier 035-a compatibility trials** observed HTTP 200 completed answers
  (~3.6–6.4 s) with zero reviews and repair eligibility blocked; they
  demonstrate transport/contract compatibility only, not the repair path.
- **036-a** reused this qualification source-equivalently in its readiness
  audit (the [036-a report](../oap/reports/036-a-current-functional-proxy-readiness-audit.md)).

These are compatibility/contract evidence at recorded epochs — not linguistic
quality and not a standing availability claim. Current invocation follows
[INSTALL.md](../INSTALL.md) and [QUICKSTART.md](../QUICKSTART.md).

## Opt-in rules

- Live runs are explicit operator actions with private endpoint/model/key
  configuration; nothing is auto-discovered or auto-enabled.
- Use tiny permitted fixtures and at most one concurrent review; measure
  first.
- No server/weights/quantization/GPU/network/gateway changes to make a test
  pass.
- Skipped compatibility is not passed; compatibility is not linguistic
  precision.
- Live requests, traces and receipts stay in private, explicitly authorized
  storage; nothing is staged, committed or packaged.

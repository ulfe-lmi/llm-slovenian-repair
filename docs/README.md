# Documentation index

This is the navigation hub for SLAIF Slovenian Repair documentation. Start from
the repository root: the **product README** is the entrance; this page organizes
the rest by audience.

## Getting started

- [Product README](../README.md) — product entrance, pipeline diagram, supported
  behavior and limits.
- [Quickstart](../QUICKSTART.md) — the shortest supported path to one synthetic
  Responses call.
- [Installation guide](../INSTALL.md) — full installation: statistics and
  checksums, read-only index, pinned Pandoc, both auth hops, launch, SSH, stop,
  upgrade, recovery, troubleshooting.
- [Proxy chaining](PROXY-CHAINING.md) — transparent forwarding, repair eligibility,
  configurable listener ports and an example `18023 → 18021` chain.

## Architecture and behavior

- [Architecture](../ARCHITECTURE.md) — current runnable architecture: system
  boundary, request/repair lifecycle, component ownership, cancellation and
  resource bounds (with diagrams).
- [Security model](../SECURITY.md) — data-not-instructions, credentials,
  protected resources, evaluation channel.
- [Testing strategy](../TESTING.md) — synthetic determinism, live opt-in,
  evaluation separation.
- [Current status](../STATUS.md) — what is implemented, what is unmeasured, and
  the evidence boundary.

## Operations, data and development

- [Data sources](DATA-SOURCES.md) — acquisition boundaries: licence, checksums,
  censored/unknown evidence semantics.
- [Evaluation](EVALUATION.md) — evaluation strategy and the
  no-separate-human-dataset owner decision.
- [Live test environment](LIVE-TEST-ENVIRONMENT.md) — bounded live-model testing
  and its opt-in.
- [Development guide](DEVELOPMENT.md) — development workflow and local
  environment.
- [Workspace placement (historical)](WORKSPACE-PLACEMENT.md) — historical
  placement record; the current machine-root authority is the
  [workspace layout](../oap/governance/WORKSPACE-LAYOUT.json).
- [Implementation roadmap](IMPLEMENTATION-ROADMAP.md) — roadmap; estimates are
  plans, not commitments.

## OAP (developer-facing)

OAP is the operating protocol that governs this repository. You do not need OAP
history to use the product; developers find its entry points here.

- [OAP runbook](OAP-RUNBOOK.md) — day-to-day OAP operations from the
  coding/strategy split.
- [Role setup](CODEX-ROLE-SETUP.md) — role setup and the foreground coding
  dispatch.
- [Bootstrap sources](BOOTSTRAP-SOURCES.md) — source identity and the
  current-vs-historical role distinction.
- [Decision policy](DECISION-POLICY.md) — the D0/D1/D2 decision policy.
- [Readiness](READINESS.md) — readiness criteria and how they are evidenced.

## History and evidence

The development chronology and the frozen evidence are preserved as historical
records and are **not** rewritten when current documentation changes.

- [History](HISTORY.md) — development history with direct links to the frozen
  records.
- [Product plan](../PLAN.md) — the protected product agreement (byte-stable).
- [Orders](../oap/orders/) — issued work orders (immutable).
- [Reports](../oap/reports/) — round reports (immutable).
- [Audits](../oap/audit/) — audit results, including the current
  functional-proxy readiness audit.
- [Research history](../research/) — research reports and
  target-distribution records.

## Frozen and generated

- **Immutable historical sources** under `docs/bootstrap/` are reference
  snapshots, not competing current law.
- **Generated projections** ([compact architecture](../ARCHITECTURE-for-agents.md),
  `oap/governance/MANIFEST.json`, `oap/governance/DISTILLATION-MAP.md`,
  `oap/GENERATED-FILES.json`, `oap/governance/CONTEXT-BUDGET.md`) are
  synchronized with the canonical sources under authorized revision control;
  they are maintained by the same authorized sync that updates the sources, not
  by ad-hoc hand edits.

# Status

Current state of the repository: what is implemented, what is verified, what is
unmeasured, and where the evidence lives. The per-round chronology is in
[HISTORY](docs/HISTORY.md); the authoritative per-round records are the
immutable orders and reports.

## Product

The normal launcher includes a transparent forwarding layer and configurable
`CONCEPT_HOST`/`CONCEPT_PORT`, supporting an additional `18023 → 18021` hop.
API traffic outside the repair profile passes through unchanged; eligible final text responses can
be repaired even when tools or multimodal input were supplied. See
[PROXY-CHAINING](docs/PROXY-CHAINING.md). The strict repair core and its historical
qualification below remain separate from this forwarding addition.

A **runnable loopback proxy** is implemented in `concept-verification/` (one
Python 3.12 parent process on `127.0.0.1:18024` with bounded owned child
processes): bounded admission, strict intake and
request contract, bounded main capture, pinned-Pandoc 3.7.0.2 original-span
protection, CPU detection, one optional isolated reviewer batch, strict lexical
acceptance, exact patching and bounded delivery. The current architecture,
including budgets, cancellation and failure semantics, is in
[ARCHITECTURE.md](ARCHITECTURE.md).

The latest independent closure audit ([036-a](oap/reports/036-a-current-functional-proxy-readiness-audit.md),
on the accepted main lineage) classified 59 MVP rows as **49 IMPLEMENTED / 9
PARTIAL / 1 ABSENT / 0 UNPROVEN**, each bound to real paths, tests and SHAs.
The non-IMPLEMENTED rows are later-stage scope boundaries (deployment/stack
coupling, SERVICE rows, unexposed mode literals, optional morphology, the
unmeasured quality axis), not functional defects.

Verification at the recorded audit epochs: the full proxy suite ran **1006
tests green in 718.1 s** (interpreter exit 0) at the audit's pinned tested
revision, as did the fresh named existing tests at that revision (the
audit record is historical evidence, not a claim about today's moving
main); native RTX3090 compatibility is qualified in the 035 rounds. The current installation path is documented and reproducible in
[INSTALL.md](INSTALL.md) — pinned Pandoc, external CC BY-SA 4.0 Gigafida
statistics, both authentication hops, foreground launch. Live qualification
evidence is in [LIVE-TEST-ENVIRONMENT](docs/LIVE-TEST-ENVIRONMENT.md)
(a qualification guide and evidence pointer, not a deployment record;
[Previous installation guide](docs/LAB-DEPLOYMENT.md) is a compatibility pointer to
INSTALL).

## Not established

- **Linguistic quality is unmeasured** — no natural error rate, no
  human-judged benefit. Goals such as high precision are targets, not results
  (LR-014).
- **No separate human evaluation dataset** — excluded by owner decision, not
  deferred and not optional; nothing here creates a dataset obligation.
- **Human milestone acceptance: none.** Release and deployment authority are
  not established (`deployment_authorized: false`); milestone labeling stays
  with the owner.
- The **human-labelled target-distribution evaluation** of the historical
  PLAN 14.2 proposal was never run, and no current order or page requires it
  as an outstanding obligation (quality stays unmeasured; no new gate).
- Stored response chaining, tools, images and structured output are forwarded
  by the transparent launcher; they are outside the strict repair profile.
  Bounded multi-client admission is supported (accepted sockets are queued
  under the admission budget); multi-user SERVICE/production operation is
  unsupported.

## Data

- Real unigram/bigram/trigram statistics are **not bundled**; the installation
  fetches the two Gigafida 2.0 archives (CC BY-SA 4.0) into an external
  read-only index. Procedure: [INSTALL.md](INSTALL.md); boundaries and the
  dated source inventory: [DATA-SOURCES.md](docs/DATA-SOURCES.md).
- Checked-in payloads are project-authored **synthetic fixtures** scoped to
  local synthetic tests only.
- The dated source inventory (observed 2026-09-08) is a metadata snapshot; its
  `NOT_ACQUIRED` labels are historical objective state, not current
  installation status.

## Protocol

- Bootstrap infrastructure is owner-published and accepted for continued
  development; role operation is qualified. Current round: `oap/active`;
  query it with the interpreter established by
  [DEVELOPMENT.md](docs/DEVELOPMENT.md):

  ```bash
  python3.12 oap/bin/check_state.py --repo-root . --repository \
      ulfe-lmi/llm-slovenian-repair
  ```
- Navigation for operators and developers: [OAP runbook](docs/OAP-RUNBOOK.md),
  [role setup](docs/CODEX-ROLE-SETUP.md), [recovery](oap/RECOVERY.md) and
  [completeness view](oap/COMPLETENESS.md).
- The 56 draft objectives are an initial coverage hypothesis; no completion
  percentage is derived from generated files.

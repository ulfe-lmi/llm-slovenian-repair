# Readiness claims

What "ready" means in this repository, and what the current evidence
establishes. The per-round chronology is in [HISTORY](HISTORY.md); the
immutable orders and reports are the authoritative records.

## Readiness levels (distinct claims)

Each level is a separate claim with separate evidence; reaching a lower
level does not imply a higher one:

- **Development merged** — an exact objective accepted by strategy after
  independent review, required final-head CI, scope/docs/risk/rollback and
  D1 checks. Does not imply release.
- **Internal demonstrator** — PLAN D01–D07 paths/evidence,
  keep/replace/reject/no-call cases, a fresh independent ICA and
  human-scoped milestone judgment; synthetic isolated work may retain an
  open D1 only if its registered gate is not crossed.
- **External demo/pilot** — the applicable DHA entries' latest verified
  human ACCEPTED and explicit human authorization for exposure, data and
  trust, in addition to scoped product evidence.
- **Qualified service/production** — S01–S05, rights,
  operations/rollback/resource/quality and security evidence, a fresh
  repeated ICA and an explicit deployment decision.

Bootstrap and software tests establish none of these product labels.
Source/CLI/fake tests, live serving, linguistic evaluation and human
acceptance are separate axes; unknown gate scope/provenance blocks the
affected action; a cleared register alone grants no deployment.

## Current position (after the 036-a audit)

- The **implemented request and repair path is demonstrated** on the
  accepted main lineage: the
  [036-a readiness audit](../oap/reports/036-a-current-functional-proxy-readiness-audit.md)
  ([audit record](../oap/audit/results/036-current-functional-proxy-readiness-audit.md))
  classified 59 MVP rows as 49 IMPLEMENTED / 9 PARTIAL / 1 ABSENT / 0
  UNPROVEN, each bound to real paths, tests and SHAs, with the 22
  audit-epoch tests fresh green at audited main plus the
  source-equivalent 1006-case suite and native evidence reused at the
  recorded epochs.
- **Human milestone acceptance: none.** `deployment_authorized: false` —
  deployment and release authority remain with the owner.
- **Linguistic quality is unmeasured.** No separate human evaluation
  dataset exists or is required (owner decision 2026-10-30, reaffirmed
  2026-11-01 — excluded, not deferred, not optional); functional
  readiness is reported from the implemented runnable behavior plus a
  fresh independent software/operating-path audit.
- The non-IMPLEMENTED rows are later-stage scope boundaries (deployment/
  stack coupling, SERVICE rows, unexposed mode literals, optional
  morphology, the unmeasured quality axis), not functional defects — see
  [IMPLEMENTATION-ROADMAP.md](IMPLEMENTATION-ROADMAP.md).

## Historical programme rows (not current gates)

The earlier programme rows are historical claims. Where held-out
human-labelled criteria appear, they are an unexecuted historical
programme — not a current future dataset plan:

- **Demonstrator 000–022** (PLAN D01–D07) — historical coverage
  hypothesis, not completed demonstrator scope: remapped issued orders
  cover part of the range; current round merges do not establish the
  original programme's completeness.
- **Experimental MVP 023–044** (M01–M07 and all eight PLAN §16
  criteria, real-boundary isolation, held-out human-labelled
  benefit/harm/cost and a fresh ICA) — historical coverage hypothesis,
  unexecuted; queue completion is no completeness proof.
- **Service 045–055** (S01–S05 plus gates) — later-stage scope per
  the 036-a audit.

Rounds 013-a through 036-a implemented the runnable proxy in
`concept-verification/` under repeated "confers no product label" scope
statements. The per-round detail, estimates and exact changed scopes are
preserved in the frozen [orders](../oap/orders/) and
[reports](../oap/reports/) (navigation: [HISTORY](HISTORY.md)); this page
does not restate them.

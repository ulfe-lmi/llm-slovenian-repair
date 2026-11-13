# Development history and evidence

This page preserves the development chronology that formerly lived inside the
[product README](../README.md) and is the navigation point for the repository's
**frozen** evidence. The current, readable state lives in the
[README](../README.md), [STATUS](../STATUS.md) and
[ARCHITECTURE](../ARCHITECTURE.md).

The chronology below is **abridged, not a verbatim archive**: it selects the
deliverable rounds and groups small corrective rounds. The per-round detail,
exact changed scope and evidence live in the authoritative frozen records,
linked from each entry. The orders, reports, audits and research records are
**immutable**: they are not rewritten when current documentation changes.

Earlier rounds used the words `PLANNED`, `NOT RUN` and `NOT_ACQUIRED` in the
sense of their own rounds; they do not describe the current runnable-proxy
status.

## Selected development rounds

- [000–003](../oap/reports/000-a-reconcile-bootstrap-repository-and-authority.md) —
  **Bootstrap.** Owner-published baseline, role split, dense coding/strategic
  law, FIFO/SELF protocol, inert draft objectives.
- [004](../oap/reports/004-a-source-manifests-and-miniature-synthetic-corpus.md) —
  **Provenance seam.** Frozen `SourceManifest`/`SyntheticCountRecord` and the
  canonical `verify_manifest_payload` boundary; project-authored synthetic
  fixtures only.
- [005](../oap/reports/005-a-real-source-inventory-and-permitted-acquisition-recipe.md) —
  **Source inventory.** Dated real-source inventory and standard-library-only
  offline artifact verifier (all artifacts `NOT_ACQUIRED`).
- [006](../oap/reports/006-a-unigram-lexicon-importer.md) — **Importer seams.**
  Bounded side-effect-free unigram importer, content-free classifier and
  verifier-first probes — compatibility evidence, not full import or
  redistribution.
- 007–011 — **Research.** Isolated concept verification, frozen research trail
  and target-distribution confirmation stages; see the
  [research reports](../research/reports/) and
  [EXPERIMENT-HISTORY](../research/EXPERIMENT-HISTORY.md) (archival synthesis).
- [012-a](../oap/reports/012-a-native-migration-and-merged-round-reconciliation.md) —
  **Native migration.** Reconciled the migrated native runtime and
  foreground-only coding dispatch.
- [013-a](../oap/reports/013-a-pandoc-original-span-protection.md) —
  **Runnable proxy.** Pandoc structural-parsing proxy with exact original
  spans, conservative abstentions, fail-closed bounded reasons and pinned
  Pandoc 3.7.0.2.
- [014-a](../oap/reports/014-a-bounded-occurrence-review-batch.md) /
  [014-b](../oap/reports/014-b-validate-terminal-answer-copies.md) —
  **Reviewer batch.** One bounded occurrence-addressed reviewer batch
  (`batch-v1`) and the terminal-answer-copy preflight.
- [015-a](../oap/reports/015-a-supported-responses-contract.md) —
  **Request contract.** Strict pre-forward text-only Responses request
  validation with closed `400` labels and JSON/SSE profile parity.
- [016-a](../oap/reports/016-a-runtime-evidence-fallback.md) —
  **Read-only evidence.** Strictly read-only runtime evidence access with safe
  degradation on technical evidence failure.
- [017-a](../oap/reports/017-a-main-body-capture.md)–[022-a](../oap/reports/022-a-upstream-setup.md) —
  **Bounded phases.** Independent elapsed budgets for main capture, response
  headers, upstream setup, intake and final delivery.
- [023-a](../oap/reports/023-a-owned-startup.md) — **Owned cleanup.** Owned
  partial-startup cleanup for the Pandoc and reviewer child starts.
- [024-a](../oap/reports/024-a-evidence-work.md) /
  [025-a](../oap/reports/025-a-analysis-eligibility.md) —
  **Evidence + eligibility.** Read-only evidence work-count policy and
  finished-answer analysis-eligibility limits.
- [026-a](../oap/reports/026-a-request-admission.md) — **Admission.** Bounded
  accepted-connection admission (one active + bounded waiting queue).
- [027-a](../oap/reports/027-a-repair-validation.md) /
  [028-a](../oap/reports/028-a-runtime-acceptance.md) /
  [028-b](../oap/reports/028-b-runtime-acceptance-fixtures.md) —
  **Acceptance.** Final-repair validation and individual/composed validation on
  one strict lexical-acceptance policy; frozen-fixture reconciliation.
- [029-a](../oap/reports/029-a-runtime-detection.md) /
  [029-b](../oap/reports/029-b-runtime-detection.md) — **Detection.** Corrected
  bounded runtime word/phrase target selection (`local-context`), max four
  targets.
- [030-a](../oap/reports/030-a-request-cancellation.md) —
  **Cancellation.** Request-scoped cancellation on client disconnect (no
  orphan repair).
- [031-a](../oap/reports/031-a-functional-proxy-audit.md) /
  [031-b](../oap/reports/031-b-close-proxy-and-preserve-order.md) /
  [032-a](../oap/reports/032-a-functional-proxy-closure-audit.md) —
  **First audits.** Functional proxy audit and closure audit with their
  publication corrections.
- [033-a](../oap/reports/033-a-protect-original-contexts.md) —
  **Protection contexts.** Protected quote/HTML context refinement.
- [034-a](../oap/reports/034-a-functional-proxy-readiness-audit.md) /
  [035-a](../oap/reports/035-a-qualify-native-rtx3090-proxy.md) —
  **Readiness + native.** Functional-proxy readiness audit and native RTX3090
  qualification (including logprobs compatibility, 035-b).
- [035-c](../oap/reports/035-c-strip-defined-api-logprobs.md) /
  [035-d](../oap/reports/035-d-useful-native-repair-and-policy-regressions.md) —
  **Metadata policy.** Unconditional defined-API `logprobs` removal and full
  useful-repair native qualification.
- [036-a](../oap/reports/036-a-current-functional-proxy-readiness-audit.md) —
  **Readiness.** Current functional-proxy readiness audit (functional software
  and native compatibility; linguistic quality unmeasured).
- [PR39](https://github.com/ulfe-lmi/slaif-llm-response-language-repair/pull/39)
  (owner-requested documentation fix, direct commit, no OAP order) —
  **Lab installation and statistics.** Reproducible lab installation with
  external Gigafida statistics (`docs/LAB-DEPLOYMENT.md`, plus README,
  data-sources and proxy README updates); merged as the accepted base of this
  documentation round.

## Frozen evidence and navigation

- [Issued work orders (immutable)](../oap/orders/)
- [Round reports (immutable)](../oap/reports/)
- [Audit results, incl. current readiness audits](../oap/audit/)
- [Bootstrap snapshots (historical reference)](bootstrap/)
- [Process sources (immutable reference)](bootstrap/sources/)
- [Research history and reports](../research/)
- [Research target-distribution records](../research/target-distribution/)
- [Runnable-proxy round record](../concept-verification/REPORT.md)

## Bootstrap and early engineering (abridged)

The bootstrap and early engineering rounds established the role split, the
dense coding/strategic law, the FIFO/SELF publication protocol, and the
provenance and importer seams listed above. The objective-006 rounds added the
unigram importer seam, a content-free row-structure classifier, and
verifier-first probe rounds that recorded real compatibility boundaries without
full import or redistribution. Rounds 007–011 carried the research trail
(verification, frozen archive, target-distribution confirmation) that the
frozen research records preserve in full. Round 012-a reconciled the migrated
native runtime. The packaged library, milestone and research objectives that
the bootstrap enumerated remain separate programmatic scope, not requirements
of the runnable proxy.

The runnable-proxy rounds (013-a through 036-a) built the loopback proxy
incrementally: structural protection (013-a), the isolated reviewer batch
(014-a/b), the strict request contract (015-a), read-only evidence (016-a),
independent phase budgets (017–022-a), owned cleanup (023-a), evidence and
eligibility bounds (024–025-a), admission (026-a), strict acceptance
(027–028-a/b), target selection (029-a/b), cancellation (030-a), the first
audits (031–032), protection contexts (033-a), readiness and native
qualification (034–035-a/b), and the unconditional logprobs policy (035-c/d).
Each round's exact changed scope, tests and evidence are preserved in its
frozen order and report.

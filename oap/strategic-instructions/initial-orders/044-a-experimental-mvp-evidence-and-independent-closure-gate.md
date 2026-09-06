# Work order 044-a — Experimental MVP evidence and independent closure gate

Status: DRAFT UNTIL STRATEGIC RECONCILIATION

```oap-metadata
{
  "id": "044-a",
  "title": "Experimental MVP evidence and independent closure gate",
  "objective": "044",
  "status": "DRAFT UNTIL STRATEGIC RECONCILIATION",
  "phase": "MVP",
  "repository": "VERIFY authorized remote",
  "default_branch": "VERIFY remote default",
  "base_sha": "VERIFY accepted current main SHA",
  "branch": "oap/044-experimental-mvp-evidence-and-independent-closure-gate",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "022",
    "034",
    "042",
    "043"
  ],
  "local_work": "VERIFY dirty/untracked work to preserve",
  "prior_review": "VERIFY predecessor disposition",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §§15.2, 16; M07"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§16,19,20"
    }
  ],
  "governance": "VERIFY current accepted canonical and compact identities",
  "lr": [
    "LR-001",
    "LR-002",
    "LR-003",
    "LR-004",
    "LR-005",
    "LR-006",
    "LR-007",
    "LR-008",
    "LR-009",
    "LR-010",
    "LR-011",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "VERIFY actual final-head CI names"
  ],
  "decision_class": "D0"
}
```

## Identity
044-a, numeric objective 044, MVP. CREATE_NEW_PR after reconciliation;
if interrupted after PR creation, adopt that same verified branch/PR.

## Provenance
H: PLAN.md §§15.2, 16; M07. A: ARCHITECTURE.md §§16,19,20.
These are source anchors, not mandatory full-source coding reads. No observed
failure, independent audit or actual critical judgment is invented by this seed.

## Current verified state
VERIFY authorized repository, current default head, dependency PR dispositions,
existing objective PR and local changes before publication. Preserve pre-existing
work. Future source/model/data facts remain unresolved until directly observed.

## Governance
Relevant invariants: LR-001, LR-002, LR-003, LR-004, LR-005, LR-006, LR-007, LR-008, LR-009, LR-010, LR-011, LR-012, LR-013, LR-014. Read C-READ-01 compact sequence,
C-WORK-01 preservation, C-EVIDENCE-01 and P-SELF-01–03. Verify accepted identities
with shared helpers. Relevant CRITICAL gates: VERIFY after investigation; initially
none asserted. Missing prerequisites are not themselves new judgment debt.

## Goal and dependencies
Deliver experimental mvp evidence and independent closure gate as one separately reviewable seam: Map M01–M07 and PLAN §16 to held-out and real-boundary evidence; request fresh ICA on current merged main; no MVP-complete label from queue completion.
Prerequisites: 022, 034, 042, 043.
Confirm their actual contracts/evidence, not just existence of earlier draft files.

## Scope
Primary boundary: MVP evidence package and independent request. Map M01–M07 and all eight PLAN §16 criteria to exact current merged main, held-out human labels, isolated requests, original preservation and benefit/harm/cost evidence.
Constrain the diff to this seam and its direct contract tests. If evidence shows
the slice exceeds one coherent review, strategy remaps before activation.

## Non-goals
No self-certification, accepted human gate fabrication or mandatory evidence relabelled optional. Do not absorb adjacent objectives or change human product intent.

## Files and boundaries
Inspect MVP evidence package and independent request; existing interfaces supplied by prerequisites; relevant compact
architecture clauses and local security/testing law. Test doubles belong outside
the named seam, so the proof observes the implementation that callers will use.

## Requirements
1. Map M01–M07 and all eight PLAN §16 criteria to exact current merged main, held-out human labels, isolated requests, original preservation and benefit/harm/cost evidence.
2. Map M01–M07 and PLAN §16 to held-out and real-boundary evidence; request fresh ICA on current merged main; no MVP-complete label from queue completion.
3. Preserve LR-001, LR-002, LR-003, LR-004, LR-005, LR-006, LR-007, LR-008, LR-009, LR-010, LR-011, LR-012, LR-013, LR-014 across the edge cases below. Bound resources and
   distinguish unsupported/unavailable facts from passing behavior.

## Acceptance criteria
1. The stated boundary has an observable successful result tied to the actual
   implementation revision; a document-only objective instead supplies the named
   verifiable contract/evidence artifact without claiming product implementation.
2. Generate fresh ICA request with gaps and tested revisions; require re-audit after remediation and prohibit queue-driven MVP-complete labels.
3. Report each required proof with tested SHA, actual result and limitation.
   Unavailable human/source/live facts stay BLOCKED/UNPROVEN, never synthesized.

## Verification
Focused future test target: `uv run pytest tests/contract/test_objective_044.py -q`.
For document-only work, finalize this as a concrete contract/manifest checker or
inspectable evidence command before publication; do not pretend a future test exists.
Broader: `uv run pytest tests/contract -q`; `python3 -B -m unittest discover -s oap/tests -v`;
`git diff --check`. VERIFY supported commands and exact required CI names at finalization.
Negative and boundary proof: Generate fresh ICA request with gaps and tested revisions; require re-audit after remediation and prohibit queue-driven MVP-complete labels.
Fake/unit protocol evidence proves software contracts only. Live model compatibility,
human linguistic labels and deployment authorization require separate evidence.

## Local setup and constraints
Install only ordinary scoped tools in an owned project environment. Use miniature
synthetic/permitted fixtures, finite time/memory/call limits and redacted diagnostics.
No Qwen weights/quantization/vLLM/CUDA/GPU/services/ports/network/gateway/neighbor
mutation. No credentials/customer texts/review contents in Git/OAP/logs. Any live
step requires deliberate separate acknowledgement, verified endpoint and data rights;
complete safe independent preparation if that step is unavailable.

## Documentation
Update the affected contract and actual support/evidence status. Record dependencies,
rights/provenance and cleanup of owned fixtures. Preserve historical observations;
correct interpretations explicitly. Code license remains an owner decision.

## Git and report publication
One objective branch/PR; never merge/auto-merge. Reconcile existing PR before creation.
Finish/push non-report work and exact active/order bytes; create/adopt PR before
report; record literal implementation SHA; write immutable matching report with
publication commit SELF; commit only report with implementation sole parent; push
and independently verify remote head/bytes/path/parent; send response OK and exit.
No future-publication/CI claims in report and no later mutation for that round.

## Decision classification
Initial D0 scoped development. Strategy must investigate and choose contained D1
only if all five conditions hold, authoring exact APPEND in a finalized appropriate
round. D2 real boundaries remain blocked; this draft supplies no human permission.

## Deferred human adjudication
- Decision: NONE

# Work order 016-a — Early bounded live-Qwen reviewer feasibility

Status: DRAFT UNTIL STRATEGIC RECONCILIATION

```oap-metadata
{
  "id": "016-a",
  "title": "Early bounded live-Qwen reviewer feasibility",
  "objective": "016",
  "status": "DRAFT UNTIL STRATEGIC RECONCILIATION",
  "phase": "DEMONSTRATOR",
  "repository": "VERIFY authorized remote",
  "default_branch": "VERIFY remote default",
  "base_sha": "VERIFY accepted current main SHA",
  "branch": "oap/016-early-bounded-live-qwen-reviewer-feasibility",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "005",
    "015"
  ],
  "local_work": "VERIFY dirty/untracked work to preserve",
  "prior_review": "VERIFY predecessor disposition",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §§4.2, 8.5, 14.1; D05"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§10,15,16.2"
    }
  ],
  "governance": "VERIFY current accepted canonical and compact identities",
  "lr": [
    "LR-004",
    "LR-005",
    "LR-010",
    "LR-012",
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
016-a, numeric objective 016, DEMONSTRATOR. CREATE_NEW_PR after reconciliation;
if interrupted after PR creation, adopt that same verified branch/PR.

## Provenance
H: PLAN.md §§4.2, 8.5, 14.1; D05. A: ARCHITECTURE.md §§10,15,16.2.
These are source anchors, not mandatory full-source coding reads. No observed
failure, independent audit or actual critical judgment is invented by this seed.

## Current verified state
VERIFY authorized repository, current default head, dependency PR dispositions,
existing objective PR and local changes before publication. Preserve pre-existing
work. Future source/model/data facts remain unresolved until directly observed.

## Governance
Relevant invariants: LR-004, LR-005, LR-010, LR-012, LR-014. Read C-READ-01 compact sequence,
C-WORK-01 preservation, C-EVIDENCE-01 and P-SELF-01–03. Verify accepted identities
with shared helpers. Relevant CRITICAL gates: VERIFY after investigation; initially
none asserted. Missing prerequisites are not themselves new judgment debt.

## Goal and dependencies
Deliver early bounded live-qwen reviewer feasibility as one separately reviewable seam: Explicit opt-in, verified endpoint/model and protected fixture; tiny targeted keep/replace/wider-edit probe with honest results; no server changes.
Prerequisites: 005, 015.
Confirm their actual contracts/evidence, not just existence of earlier draft files.

## Scope
Primary boundary: opt-in reviewer feasibility harness. Require separate live acknowledgement, verified model/endpoint/API shape and permitted tiny fixture; measure actual keep/replace/wider-edit output and cancellation support.
Constrain the diff to this seam and its direct contract tests. If evidence shows
the slice exceeds one coherent review, strategy remaps before activation.

## Non-goals
Do not infer linguistic precision from probes, alter server flags or expand into a benchmark batch. Do not absorb adjacent objectives or change human product intent.

## Files and boundaries
Inspect opt-in reviewer feasibility harness; existing interfaces supplied by prerequisites; relevant compact
architecture clauses and local security/testing law. Test doubles belong outside
the named seam, so the proof observes the implementation that callers will use.

## Requirements
1. Require separate live acknowledgement, verified model/endpoint/API shape and permitted tiny fixture; measure actual keep/replace/wider-edit output and cancellation support.
2. Explicit opt-in, verified endpoint/model and protected fixture; tiny targeted keep/replace/wider-edit probe with honest results; no server changes.
3. Preserve LR-004, LR-005, LR-010, LR-012, LR-014 across the edge cases below. Bound resources and
   distinguish unsupported/unavailable facts from passing behavior.

## Acceptance criteria
1. The stated boundary has an observable successful result tied to the actual
   implementation revision; a document-only objective instead supplies the named
   verifiable contract/evidence artifact without claiming product implementation.
2. Run bounded one-request probes only after gates; record actual counts, serving limits and parse outcomes; missing approval or endpoint yields BLOCKED with no request.
3. Report each required proof with tested SHA, actual result and limitation.
   Unavailable human/source/live facts stay BLOCKED/UNPROVEN, never synthesized.

## Verification
Focused future test target: `uv run pytest tests/contract/test_objective_016.py -q`.
For document-only work, finalize this as a concrete contract/manifest checker or
inspectable evidence command before publication; do not pretend a future test exists.
Broader: `uv run pytest tests/contract -q`; `python3 -B -m unittest discover -s oap/tests -v`;
`git diff --check`. VERIFY supported commands and exact required CI names at finalization.
Negative and boundary proof: Run bounded one-request probes only after gates; record actual counts, serving limits and parse outcomes; missing approval or endpoint yields BLOCKED with no request.
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

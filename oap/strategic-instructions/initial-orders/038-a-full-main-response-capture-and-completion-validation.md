# Work order 038-a — Full main-response capture and completion validation

Status: DRAFT UNTIL STRATEGIC RECONCILIATION

```oap-metadata
{
  "id": "038-a",
  "title": "Full main-response capture and completion validation",
  "objective": "038",
  "status": "DRAFT UNTIL STRATEGIC RECONCILIATION",
  "phase": "MVP",
  "repository": "VERIFY authorized remote",
  "default_branch": "VERIFY remote default",
  "base_sha": "VERIFY accepted current main SHA",
  "branch": "oap/038-full-main-response-capture-and-completion-validation",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "037"
  ],
  "local_work": "VERIFY dirty/untracked work to preserve",
  "prior_review": "VERIFY predecessor disposition",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §§3, 5, 11.4, 13.3; M06"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§5,13,14"
    }
  ],
  "governance": "VERIFY current accepted canonical and compact identities",
  "lr": [
    "LR-001",
    "LR-011"
  ],
  "relevant_gates": [],
  "required_checks": [
    "VERIFY actual final-head CI names"
  ],
  "decision_class": "D0"
}
```

## Identity
038-a, numeric objective 038, MVP. CREATE_NEW_PR after reconciliation;
if interrupted after PR creation, adopt that same verified branch/PR.

## Provenance
H: PLAN.md §§3, 5, 11.4, 13.3; M06. A: ARCHITECTURE.md §§5,13,14.
These are source anchors, not mandatory full-source coding reads. No observed
failure, independent audit or actual critical judgment is invented by this seed.

## Current verified state
VERIFY authorized repository, current default head, dependency PR dispositions,
existing objective PR and local changes before publication. Preserve pre-existing
work. Future source/model/data facts remain unresolved until directly observed.

## Governance
Relevant invariants: LR-001, LR-011. Read C-READ-01 compact sequence,
C-WORK-01 preservation, C-EVIDENCE-01 and P-SELF-01–03. Verify accepted identities
with shared helpers. Relevant CRITICAL gates: VERIFY after investigation; initially
none asserted. Missing prerequisites are not themselves new judgment debt.

## Goal and dependencies
Deliver full main-response capture and completion validation as one separately reviewable seam: No text forwarded before final decision; bounded capture; preserve upstream errors and finish/incomplete semantics.
Prerequisites: 037.
Confirm their actual contracts/evidence, not just existence of earlier draft files.

## Scope
Primary boundary: main response capture boundary. Accumulate complete main response under hard byte bound and validate explicit finish semantics before CPU, review or user text delivery.
Constrain the diff to this seam and its direct contract tests. If evidence shows
the slice exceeds one coherent review, strategy remaps before activation.

## Non-goals
No provisional content leakage, optional-repair catch masking main failure or implicit client streaming support. Do not absorb adjacent objectives or change human product intent.

## Files and boundaries
Inspect main response capture boundary; existing interfaces supplied by prerequisites; relevant compact
architecture clauses and local security/testing law. Test doubles belong outside
the named seam, so the proof observes the implementation that callers will use.

## Requirements
1. Accumulate complete main response under hard byte bound and validate explicit finish semantics before CPU, review or user text delivery.
2. No text forwarded before final decision; bounded capture; preserve upstream errors and finish/incomplete semantics.
3. Preserve LR-001, LR-011 across the edge cases below. Bound resources and
   distinguish unsupported/unavailable facts from passing behavior.

## Acceptance criteria
1. The stated boundary has an observable successful result tied to the actual
   implementation revision; a document-only objective instead supplies the named
   verifiable contract/evidence artifact without claiming product implementation.
2. Fake streaming upstream records event sequence; test socket-close without finish, error status, length stop, invalid envelope and hard limit; no partial success.
3. Report each required proof with tested SHA, actual result and limitation.
   Unavailable human/source/live facts stay BLOCKED/UNPROVEN, never synthesized.

## Verification
Focused future test target: `uv run pytest tests/contract/test_objective_038.py -q`.
For document-only work, finalize this as a concrete contract/manifest checker or
inspectable evidence command before publication; do not pretend a future test exists.
Broader: `uv run pytest tests/contract -q`; `python3 -B -m unittest discover -s oap/tests -v`;
`git diff --check`. VERIFY supported commands and exact required CI names at finalization.
Negative and boundary proof: Fake streaming upstream records event sequence; test socket-close without finish, error status, length stop, invalid envelope and hard limit; no partial success.
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

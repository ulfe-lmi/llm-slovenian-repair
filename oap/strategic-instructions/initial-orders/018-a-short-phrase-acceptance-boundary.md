# Work order 018-a — Short-phrase acceptance boundary

Status: DRAFT UNTIL STRATEGIC RECONCILIATION

```oap-metadata
{
  "id": "018-a",
  "title": "Short-phrase acceptance boundary",
  "objective": "018",
  "status": "DRAFT UNTIL STRATEGIC RECONCILIATION",
  "phase": "DEMONSTRATOR",
  "repository": "VERIFY authorized remote",
  "default_branch": "VERIFY remote default",
  "base_sha": "VERIFY accepted current main SHA",
  "branch": "oap/018-short-phrase-acceptance-boundary",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "017"
  ],
  "local_work": "VERIFY dirty/untracked work to preserve",
  "prior_review": "VERIFY predecessor disposition",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §§7.2, 9.1; D06"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§9,11.2"
    }
  ],
  "governance": "VERIFY current accepted canonical and compact identities",
  "lr": [
    "LR-003",
    "LR-006",
    "LR-009"
  ],
  "relevant_gates": [],
  "required_checks": [
    "VERIFY actual final-head CI names"
  ],
  "decision_class": "D0"
}
```

## Identity
018-a, numeric objective 018, DEMONSTRATOR. CREATE_NEW_PR after reconciliation;
if interrupted after PR creation, adopt that same verified branch/PR.

## Provenance
H: PLAN.md §§7.2, 9.1; D06. A: ARCHITECTURE.md §§9,11.2.
These are source anchors, not mandatory full-source coding reads. No observed
failure, independent audit or actual critical judgment is invented by this seed.

## Current verified state
VERIFY authorized repository, current default head, dependency PR dispositions,
existing objective PR and local changes before publication. Preserve pre-existing
work. Future source/model/data facts remain unresolved until directly observed.

## Governance
Relevant invariants: LR-003, LR-006, LR-009. Read C-READ-01 compact sequence,
C-WORK-01 preservation, C-EVIDENCE-01 and P-SELF-01–03. Verify accepted identities
with shared helpers. Relevant CRITICAL gates: VERIFY after investigation; initially
none asserted. Missing prerequisites are not themselves new judgment debt.

## Goal and dependencies
Deliver short-phrase acceptance boundary as one separately reviewable seam: Restrict to preassigned span, reject wider edits and incomparable raw length-dependent frequency comparisons.
Prerequisites: 017.
Confirm their actual contracts/evidence, not just existence of earlier draft files.

## Scope
Primary boundary: acceptance.py short-phrase policy. Authorize only preassigned original phrase with finite word/character bounds; evaluate affected local contexts and morphology with comparable evidence.
Constrain the diff to this seam and its direct contract tests. If evidence shows
the slice exceeds one coherent review, strategy remaps before activation.

## Non-goals
No sentence rewriting, automatic target widening after review or experimental evidence-insufficient changes. Do not absorb adjacent objectives or change human product intent.

## Files and boundaries
Inspect acceptance.py short-phrase policy; existing interfaces supplied by prerequisites; relevant compact
architecture clauses and local security/testing law. Test doubles belong outside
the named seam, so the proof observes the implementation that callers will use.

## Requirements
1. Authorize only preassigned original phrase with finite word/character bounds; evaluate affected local contexts and morphology with comparable evidence.
2. Restrict to preassigned span, reject wider edits and incomparable raw length-dependent frequency comparisons.
3. Preserve LR-003, LR-006, LR-009 across the edge cases below. Bound resources and
   distinguish unsupported/unavailable facts from passing behavior.

## Acceptance criteria
1. The stated boundary has an observable successful result tied to the actual
   implementation revision; a document-only objective instead supplies the named
   verifiable contract/evidence artifact without claiming product implementation.
2. Test different-length replacements, needs_wider_edit, forbidden newline/markup, identity edit and candidate extending outside target; refuse raw whole-phrase count dominance.
3. Report each required proof with tested SHA, actual result and limitation.
   Unavailable human/source/live facts stay BLOCKED/UNPROVEN, never synthesized.

## Verification
Focused future test target: `uv run pytest tests/contract/test_objective_018.py -q`.
For document-only work, finalize this as a concrete contract/manifest checker or
inspectable evidence command before publication; do not pretend a future test exists.
Broader: `uv run pytest tests/contract -q`; `python3 -B -m unittest discover -s oap/tests -v`;
`git diff --check`. VERIFY supported commands and exact required CI names at finalization.
Negative and boundary proof: Test different-length replacements, needs_wider_edit, forbidden newline/markup, identity edit and candidate extending outside target; refuse raw whole-phrase count dominance.
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

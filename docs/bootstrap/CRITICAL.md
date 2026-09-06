# LLM Slovenian Repair — Deferred Human Adjudication Register

**Register rules: 2.0. Date: 2026-09-06.**
**Canonical live location:** `REPO_ROOT/CRITICAL.md`.
**Basis:** supplied `concentrated-oap.md` §§6–9, 13–14, 18–19.
**Related product authority:** [PLAN.md](PLAN.md), [ARCHITECTURE.md](ARCHITECTURE.md).

This register implements **Human Judgment Postloading (HJP)** through **Deferred
Human Adjudication (DHA)**. It records consequential autonomous judgment debt,
not routine uncertainty. A difficult reversible decision is not permission for
strategy to stop. An entry is not permission to cross a non-delegable boundary.

The initial file contains rules and fenced templates only: **zero actual
CRIT entries, zero mitigation updates, zero human dispositions**. Do not invent
entries to populate a template. Do not delete this file because it is empty.

## 1. Decision classes and admission

D0: ordinary reversible engineering within delegated architecture/risk budget;
decide, test, document normally and continue. No critical entry.

D1: consequential but safely containable provisional choice; investigate,
choose, mitigate, test, record and continue. The strategic agent owns this
judgment. Development merge may be allowed while its later human gate is open.

D2: real production, destructive/irreplaceable-data, credential, public-exposure,
legal/ethical/contractual or explicit human-authority boundary; analyze and
recommend, but do not cross it without human authorization. Safe isolated
preparation is different from permission to perform the real action.

A new D1 `CRIT-NNNN` is permitted only when **all five** hold:

1. Existing human instructions, constitution, architecture, active work order
   and available evidence do not resolve the issue.
2. Strategy has investigated enough to identify materially different
   alternatives and must choose one.
3. A wrong choice could materially affect security, authorization, privacy,
   data integrity, irreversible loss, trust boundaries, public exposure,
   deployment safety or release acceptability.
4. A provisional choice can be implemented and tested safely without crossing
   a non-delegable external or production boundary.
5. A competent human could plausibly reject or materially change the choice
   before the declared gate.

Exclude ordinary decisions, bugs, failed tests, TODOs, known limitations,
refactoring/style, ordinary dependency choices, unsupported speculative risks,
low-impact reversible trade-offs and duplicate underlying dilemmas. A missing
GPU/corpus/authentication setting is not automatically judgment debt. Unresolved
rights cannot be turned into permission by registering them as D1.

## 2. Roles and exact append authorization

Strategy determines necessity, assigns the stable ID, authors the **entire exact
entry**, and places it in the current or same-PR corrective work order. It verifies
that the append preserves prior bytes before merging.

Coding may report a candidate dilemma with evidence. It cannot invent the ID,
write the strategic judgment, weaken or close an entry. It may only append the
exact ordered bytes using `oap/bin/append_critical.py` after verifying the active
order and prior register state.

Every finalized order contains exactly one declaration:

```markdown
## Deferred human adjudication
- Decision: NONE
```

or:

```markdown
## Deferred human adjudication
- Decision: APPEND CRIT-0001
```

`NONE` is normal and needs no defensive essay. `APPEND` requires the complete
entry and exact attestation below. An order referencing an existing D1 may use
`NONE` plus explicit related-entry/gate references; this does not erase the D1.

This project's additional mechanical convention allows a mitigation-only order
to retain `NONE` and add `Mitigation update: UPDATE CRIT-0001`, with exact update
bytes and the trusted prior register size/hash. It never creates a new D1 or
clears a gate. This update-field spelling is a project convention, not a quote
from the source doctrine.

## 3. Required new-entry schema

The fenced block below is a **template**, not a live register entry. Preserve
these canonical labels in generated entry templates and validators:

```markdown
## CRIT-0001 — Short decision title

- **Status:** OPEN — HUMAN ADJUDICATION REQUIRED
- **Introduced by:** PR #123 / OAP objective 037-a
- **Category:** security | authorization | data integrity | privacy | operations | architecture | dependency | other
- **Severity:** low | medium | high | critical
- **Decision confidence:** low | medium | high
- **Required human gate:** before pilot | before external demo | before production | before irreversible migration
- **Affected components:** ...

### Dilemma
What consequential question lacked a clearly mandated answer?

### Decision taken
What did the strategic agent choose?

### Reasoning
Why is this the best provisional choice at the current stage?

### Alternatives considered
What materially different credible alternatives exist?

### Strongest argument that this decision is wrong
A serious counterargument, not a token objection.

### Assumptions
What must remain true, and what evidence would falsify it?

### Failure mode and blast radius
Consequences and affected components if the choice is wrong.

### Mitigations and evidence
Tests, controls and containment supporting safe continuation.

### Reversibility and rollback
How to reverse the choice and the expected migration cost.

### Safe autonomous continuation
The exact work allowed to continue and what remains blocked.

### Exact human gate
The specific demo, pilot, release, deployment, migration or exposure boundary.

### Exact question for the human adjudicator
One precise decision question.

### Strategic attestation
ALL FIVE CRITICAL-ENTRY CONDITIONS SATISFIED

### Human disposition
PENDING — append separately; do not edit this entry.

### Resolution
PENDING — cleared only by the latest appended human ACCEPTED disposition.
```

Use a verified introducing PR/objective. If a dilemma is found before PR creation,
strategy can finalize the append in a same-PR corrective round once that PR
exists; do not fabricate a PR number. The executable publication contract must
support this safe ordering without demanding a nonexistent PR for every `a` draft.

## 4. Append-only history and mitigation

This project uses strict byte-preserving append mechanics as its realization of
canonical **append-only-in-spirit** policy. New entries, mitigation/evidence
updates and human dispositions are appended at physical EOF. No earlier bytes
are edited, removed, reordered or renumbered.

For an authorized agent append, require:

```text
new_bytes starts with trusted_previous_bytes
appended_bytes == exact_bytes_in_active_order
trusted previous size/hash matches before writing
new entry identifier is unique (fenced templates are not entries)
```

Use locks, same-filesystem atomic replacement/durable flush as appropriate, and
an explicit recovery strategy. No partially written append counts as complete.
Reject symlinks, unexpected ownership, stale bases, duplicates and all attempted
human-adjudication sections in agent payloads. Identical replay is either a
verified no-op or a precise already-applied result; never append a duplicate.

`docs/bootstrap/CRITICAL.md` is an immutable initial seed. Initially the
whole live register equals it. Later only its prefix must match; compare the
entire earlier live history to a trusted Git/reference base as well. Do not
recreate a missing live register from the seed. No separately editable strategic
copy exists.

Mitigation or a superseding implementation may be recorded in later sections.
It does not rewrite the original judgment or close the human gate. A structural
state such as `SUPERSEDED_PENDING` is **not** a fifth human disposition.

## 5. Human dispositions: exactly four values

A genuine human appends a separate attributable record:

```markdown
## HUMAN ADJUDICATION — CRIT-0001 — 2026-09-15
- Decision: ACCEPTED
- Authority: Janez Perš / project owner
- Conditions or required follow-up:
- Evidence/reference:
```

Allowed decisions are exactly:

```text
ACCEPTED
REJECTED
CHANGE REQUIRED
DEFERRED
```

Only the latest attributable human `ACCEPTED` clears that entry's registered
gate. The other three remain blocking. A newer rejection/defer/change-required
record overrides an older acceptance. If material remediation is still needed,
use `CHANGE REQUIRED` or `DEFERRED`, not a conditional acceptance pretending the
work is done. Accepted conditions must still be enforceable at deployment.

Agents may supply empty templates and recommendations; they cannot author or
append a purported human decision. A human name in Markdown is not authentication.
State tooling separates syntactically valid records from independently verified
human provenance under the owner's process; unverifiable approval does not clear
a real gate. No agent can authorize itself by editing expected hashes.

## 6. Two gates; no automatic deployment

Strategic merge means accepted for continued development after evidence and CI.
It does not mean human-approved for deployment. Open D1 entries may coexist with
safe local work only while their exact gate remains uncrossed.

Before an external demo, pilot, release, deployment, migration, real-data use or
exposure, evaluate **all applicable** entries, current assumptions and combined
risk. Clearing a CRIT entry does not supply separately missing deployment,
credential, licensing or public-exposure authority. An unknown gate scope or
unverified human disposition fails closed for that action, not for every unrelated
development task.

## 7. Deliberate loading, state checks and recovery

Do not put this full register in an every-turn instruction list.

Strategy reads it at startup, before release/deployment gates, on related dilemmas
and at periodic aggregate-risk review. A fresh strategic process reloads current
state. Coding reads it only for an exact ordered append or relevant cross-reference.
Routine state output may report IDs, latest disposition and relevant open gates
without sending the entire historical register to either model.

`check_state.py` must report IDs, duplicates, latest human dispositions, accepted
versus still-open gates, and provenance uncertainty. Helpers, CI and review test
prefix integrity, schema completeness, wrong/extra disposition values, a later
non-accepted disposition, and development continuation under unrelated open gates.
Tests use disposable synthetic registers only.

## 8. Appended entries and dispositions

No actual entries or human adjudications have been recorded in this seed.

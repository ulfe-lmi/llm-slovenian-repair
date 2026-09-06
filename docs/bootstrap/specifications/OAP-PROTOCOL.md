# Concentrated OAP Protocol to Generate and Test

**Version 2.0. Binding project profile.**
Primary doctrine is the owner's supplied Concentrated OAP chapter. This document
selects concrete filesystem/transport/commit conventions where that chapter is
conceptual. Do not silently import incompatible conventions from old archives.

## 1. Role authority and delegated decisions

Human owns purpose, domain truth, risk budget, D2 authorization, human adjudication,
final milestone judgment and release/deployment. Strategy owns delegated evolution,
orders, decisions, evidence review and conditional **development** merge. Coding
owns implementation, local setup, tests and PR/report evidence; never merge,
auto-merge, choose next scope or claim human approval.

GitHub is remote software truth. Versioned OAP orders/reports/current pointer are
orchestration truth. Runtime/private metadata supports recovery but does not
replace remote truth. FIFO is synchronization only; a process exit or `OK` is not
success, acceptance or authorization.

Encode a project-specific D0/D1/D2 policy with at least these cases:

| Case | Classification/action |
|---|---|
| Internal module layout or bounded queue implementation within architecture | Normally D0; decide and verify. |
| Insufficient statistical support, ordinary failed tests or unavailable source | Normal evidence/implementation issue; not automatically D1. |
| Consequential reversible isolated design choice satisfying all five conditions | D1; strategy chooses, mitigates, records exact entry and continues. |
| Processing real sensitive texts, exposing a provisional endpoint, replacing live Qwen or changing real credentials/network | D2 unless specifically human-authorized; do not cross the boundary. |
| Unknown rights to a corpus/package | Investigate or choose a permitted alternative; a CRIT entry does not grant rights. |
| Lowering strict acceptance to bypass PLAN's agreed independent-evidence boundary | Not a routine D0 tuning choice; do not silently change the product agreement. |

Do not hardcode decisions from examples as actual project dilemmas. Empty initial
CRITICAL remains empty. Classifications require judgment; helpers enforce declared
fields and forbidden transitions, not the semantic truth of a declaration.

## 2. Development gate and human gate

Strategy may merge only after independent review confirms the exact current
objective, coherent scope, meaningful tests, required **final-head** CI green,
accurate docs, no secrets/prohibited artifacts, no D2 crossing, complete D1
registration, sufficient reversibility and a serious strongest-reason-not-to-merge
assessment. Missing/pending/cancelled checks are not passed. Repository protection
and merge permissions still apply; never disable them for convenience.

Before enabling delegated merge on a configured remote, inspect whether merge
triggers production deployment or another D2 side effect. An ordinary development
merge permission cannot authorize that side effect.

Deployment/public-release gates require applicable DHA clearance and explicit
human authority. Only latest attributable human ACCEPTED clears a CRIT gate;
REJECTED, CHANGE REQUIRED and DEFERRED do not. Parsing a human-looking name is
not verification of its provenance. ICA success is also not deployment permission.

## 3. Project filesystem and state

```text
REPO_ROOT/oap/orders/<ID>-<slug>.md     immutable after publication
REPO_ROOT/oap/reports/<ID>-<slug>.md    immutable final coding report
REPO_ROOT/oap/active                  current pointer (absent at bootstrap)
REPO_ROOT/CRITICAL.md                 canonical append-only live register
STRATEGIC_HOME/control.fifo           strategy sends; coding wrapper receives
STRATEGIC_HOME/response.fifo          coding sends; strategy receives
```

Select only by the exact active ID. Never newest/highest/mtime or directory order.
The active pointer is ASCII ID followed by one LF; require a single well-formed
record with no extra whitespace. Its **current value changes** by authorized
publication; its prior history and published order/report bytes are preserved.
Absence is valid inactive state. An existing empty/malformed pointer is an error.

Publishers/wrappers/strategic sessions use role-specific locks. Validate canonical
paths, ownership, types and symlinks; scope permissions to generated private
objects. FIFOs/private config are 0600; private directories 0700. Protect legitimate
Git worktrees and existing unrelated files. Private absolute paths stay out of
public logs and manifests unless truly required and approved.

## 4. IDs and one-PR continuity

This profile explicitly selects:

```text
ID grammar: ^[0-9]{3}-[a-z]{1,2}$
round order: a,b,...,z,aa,ab,...,az,ba,...,zz
NNN-a: one objective branch and one new PR
NNN-b through NNN-zz: same numeric objective, same branch and same PR
```

This extended suffix convention follows the previously inspected local-coding
precedent. Neither attached conceptual OAP chapter prescribes this exact grammar.
It replaces the older bootstrap's arbitrary stop at z. Do not sort suffixes
lexicographically. Exhaustion of the explicit range requires a reviewed protocol
revision, not an invented new objective or duplicate PR.

Context reset, process/model/provider/machine replacement and a lost signal do
not advance the suffix. New strategic requirements after review do. A first-round
crash that already created a branch/PR resumes that same object; `a` is not license
to create another PR on recovery. A genuine duplicate/conflict stops the transition
for explicit reconciliation.

New numeric objectives normally follow accepted merge and verified remote default
branch. Deliberate abandonment may close without merge with explicit rationale,
recorded disposition and dependency reassessment. Never silently skip or mislabel
abandoned work as accepted. Planned seeds are not an obligation to execute obsolete
or unneeded tasks.

## 5. Finalized work-order contract

Every draft is visibly `DRAFT UNTIL STRATEGIC RECONCILIATION` with unresolved
future facts. Every published order is `Status: FINAL` with no real unresolved
finalization markers. Validate actual metadata, not an indiscriminate search for
words like TODO inside quoted test fixtures.

Each final order contains these sections/fields:

```text
Identity: ID, title, FINAL, numeric objective, CREATE_NEW_PR|AMEND_EXISTING_PR
Provenance: H/A/E/I/C + concrete source/section/evidence reference
Current verified state: repository/default branch/base SHA, branch/PR mode,
                       prior round/review and local work to preserve
Governance: current source/compact identities, LR IDs, relevant critical gates
Goal and phase/dependencies
Scope and explicit non-goals
Files/boundaries to inspect
Requirements and numbered acceptance criteria
Verification: commands, negative cases, evidence boundary, expected CI
Local setup/resource/privacy/protected-host constraints
Documentation obligations
Git/PR/report-publication contract
Decision class: D0|D1|D2 and applicable safe scope
Deferred human adjudication: exact canonical declaration
```

Provenance markers are **H** human/preload, **A** architecture/constitution/contract/
roadmap, **E** observed failing evidence, **I** independent audit, **C** CRITICAL/DHA
remediation. At least one real durable reference; a bare marker is insufficient.
Use C rather than silently importing ordinary OAP's broader R vocabulary.

A new `a` order may specify PR creation rather than an unknowable number. A later
order must identify the verified existing PR. Unknown future SHAs/PR numbers must
never be invented. If a new D1 entry needs an as-yet nonexistent PR identity,
create only the safe scoped prerequisite first, then issue the exact same-PR
append order before introducing/merging the provisional choice. Coding-detected
D1 candidates return to strategy for that decision, not self-authored entries.

Use exactly:

```markdown
## Deferred human adjudication
- Decision: NONE
```

or `- Decision: APPEND CRIT-NNNN` under the same heading. For APPEND, embed the
complete strategic-authored entry in an unambiguous `critical-entry` fenced block
and record its UTF-8 byte length/hash and trusted prior register length/hash.
Define extraction precisely: payload starts after the opening fence line and
ends immediately before the closing fence line; preserve its final newline.
Use a longer fence if necessary so payload cannot close it accidentally. The
append helper consumes these exact bytes, not a model-normalized reconstruction.

Mitigation-only work uses `Decision: NONE` plus the distinct `Mitigation update:
UPDATE CRIT-NNNN`, exact fenced payload/hash and prior reference. An existing D1
reference with no new append remains visible in the relevant-gates field.

A declared D2 action is blocked unless genuine explicit human authorization is
verified. An order may instead authorize safe isolated preparation while stating
the real boundary remains blocked. Never manufacture authorization fields.

## 6. Atomic publication and exact FIFO

`publish_order.py` provides `--repo-root`, `--source`, `--id`, `--dry-run` and
explicit runtime/base inputs as needed. Validate complete metadata, provenance,
DHA, source identities, allowed transition, no existing conflicting order/report
and correct PR mode. Serialize publishers with a lock.

Write/flush the immutable order first, then atomically replace the active pointer.
These are **two writes**, not a single filesystem transaction. Signal only after
both are validated. A crash between them leaves a published-but-inactive order;
an identical safe retry may finish the same unresolved publication, never reactivate
a completed old round. No implicit commit, push, signal or model launch.

`oap_fifo.py send --fifo PATH` / `wait --fifo PATH` exchange exactly ASCII bytes
`OK`, hex `4f4b`, no LF, ID, status or JSON. Close writer descriptors. Correctly
handle fragmented I/O, EOF, wrong/extra bytes and interruptions. No shell `echo`
that adds a newline. OS-blocking idle is valid; no periodic model invocation.
Transport/tests must be interruptible, and tests have finite timeouts/cleanup.
A FIFO is not an authenticated durable message queue.

The coding wrapper consumes control **once** before starting the model; the
coding prompt must not ask the model to wait on it a second time. After wake-up,
reconcile active/order/report and no-replay state before model invocation. A
completed reported round does not launch coding again merely because OK arrived.

## 7. Coding publication and SELF

A normal execution sequence is:

1. Wrapper receives valid control; checks state/role; starts fresh coding context.
2. Coding reads its compact law and exact order; reconciles local/remote facts.
3. Implement only ordered work; test/document; perform exact ordered critical
   append in ordinary implementation work when applicable.
4. Commit/push non-report work, including exact activated order/active bytes.
5. Create the single PR for `a`, or update the existing PR for a later/recovered
   round, **before composing the final report**. Never merge or enable auto-merge.
6. Inspect and repair safe in-scope CI; push all remaining non-report changes.
7. Record literal implementation head SHA.
8. Create one immutable report; commit **only its path** as final round commit,
   with the recorded implementation head as first parent.
9. Push and independently verify remote PR head, exact report bytes and parent/
   changed-path invariant. No subsequent mutation/push for this round.
10. Send exact response OK and exit; wrapper returns to external FIFO wait.

Report uses `Report publication commit: SELF`, not its own impossible precomputed
commit hash. It names the literal implementation head. A report written before its
own push cannot truthfully claim to have already verified that future publication
or its future CI. Record observations with actual tested SHAs and timestamps;
post-publication checks belong in bounded private receipts/strategic review.

Mandatory report fields:

```text
Result: COMPLETE|PARTIAL|BLOCKED|FAILED
Order ID/path/hash and governing source identities
PR mode/number/URL/state, branch/base, starting remote SHA
Implementation head SHA: <literal>
Report publication commit: SELF
Implementation and docs changed; per-criterion evidence
Each command/check: PASSED|FAILED|SKIPPED|NOT RUN|BLOCKED|PENDING|MISSING + SHA
Negative-path and boundary-fidelity evidence
Setup/dependencies and resource/privacy/protected-host evidence
Critical action: NONE|APPENDED CRIT-NNNN|MITIGATION UPDATED CRIT-NNNN|CANDIDATE REPORTED
Limitations, outstanding human gates and scope/no-merge confirmation
```

PARTIAL/BLOCKED/FAILED still sends OK once its truthful report is properly published.
Remote publication failure does not send a false success notification: preserve
work and private incident state, then recover from durable evidence. A correction
after final report uses a new strategic corrective suffix on the same PR, not an
amended historical report. The final report-only commit must never contain CRITICAL,
code, active/order fixes or unrelated metadata.

`verify_report.py` checks IDs, exact order, commit parent and changed path, PR
identity and remote head/content when available. Local-only verification is labelled
local. Current-head CI is strategy's later gate, not fabricated report evidence.

## 8. Critical helper and state checks

`append_critical.py` verifies current active authorization, exact strategic payload,
ID/schema/five-condition attestation, prior trusted size/hash and byte prefix;
locks, durably publishes and detects safe retries versus conflicting state.
Reject noncanonical dispositions, unauthorized rewrites, duplicate IDs and all
agent-authored human disposition payloads. Fenced templates do not count as entries.
Do not treat the seed hash as the whole live-register hash after valid growth.

`check_state.py` reports protocol state, critical IDs/duplicates/latest dispositions,
applicable open gates and unverified human provenance. It checks fields without
claiming to authenticate a human merely from a Markdown name. `check_governance.py`
validates canonical/projection identities, source locks, role/context contracts,
trusted-base revision scope and register prefix/history. It does not certify
semantic decision correctness. These helpers must be shared by doctor, launch,
publication and strategic review rather than divergent validators.

## 9. Strategic review, continuity and minimal diagnosis

Before an order, reconcile current default branch, PRs, CI, accepted governance,
local work, dependencies and relevant runtime facts. After coding OK, verify
unique report and remote publication; then inspect actual diff, all objective
rounds, meaningful tests, docs, risk, protected resources, DHA and required current-
head checks. Reports are evidence indexes, not automatic acceptance.

Use the repository-approved merge method and expected reviewed head; if head
changes, re-review. After merge verify merged PR and remote default branch. Preserve
report-commit evidence even if the chosen merge method changes main's commit shape.
Never infer success from a local file or remembered percentage.

When a path fails, identify the earliest reproducible failing boundary. Do not
patch product code below a boundary not reached. Issue the smallest discriminating
experiment with a stop condition; preserve observations and supersede overstrong
causal interpretations in later records. Do not turn debugging into unrelated scope.

Recovery cases to implement/test:

| Durable observation | Correct action |
|---|---|
| No active order | Stay inactive or wrapper waits; no model work. |
| Control consumed; coding died; no final report | Resume same order/branch/PR from first unfinished requirement. |
| PR exists from interrupted `a` | Adopt verified existing PR, never duplicate. |
| Final report pushed; response notification lost | Resume strategic review; no repeated coding implementation. |
| Final report exists locally but publication unverified | Complete/verify publication under recovery, not rewrite the report. |
| Published order exists but active update failed | Finish only identical still-unresolved activation, or preserve conflict. |
| New model/provider/context/machine | Reconstruct same logical role/state; no automatic new objective/suffix. |
| Duplicate signal for completed round | Suppress model invocation; verify durable state. |
| Required CI pending | Wait/recheck without busywork or automatic suffix increment. |
| Explicit quit | Stop cleanly and leave shell; do not resurrect children. |

Strategy may re-signal an unfinished round after reconciliation; a recovery receipt
records why without overwriting order/report history. Local private journal may
track signal consumption and publication, but remote/OAP truth governs conflicts.

## 10. ICA and milestone boundaries

Generate ICA protocol, a complete architecture-derived requirement matrix, report
and request templates. Do not certify a milestone from the queue alone. Launching
an ICA is an explicit later audit action, not automatic bootstrap model usage.
An independent human or fresh isolated audit context has read-only/audit authority,
no routine coding, merge, production or scope-changing authority.

The request identifies exact current merged main, full architecture revision,
human milestone scope and approved evidence/runtime access. The auditor derives
requirements **before** reading the strategic closure conclusion. Classifications
are IMPLEMENTED, PARTIAL, ABSENT, UNPROVEN. Meaningful executable evidence must
exercise actual entry point, authority, persistence, routing or integration named
by the requirement; mocking that boundary cannot prove it.

Every report states audit identity/context separation, source/main SHAs, matrix,
negative/failed/not-run evidence, scope/quality/runtime gaps and human gates. Do
not prefill success. `check_ica.py` checks schema/coverage/version scope and makes
no semantic claim that an independent review was genuinely performed.

After remediation, audit again from architecture and new current main, not merely
the closure ticket list. Freshness ties to the exact evaluated revision; unrelated
later changes require an explicit assessed delta or rerun, never silently reuse a
stale pass. ICA artifacts may be published without changing product code; preserve
which product revision was actually audited. Strategy recommends; the human owns
final milestone and deployment decisions. Safe independent next-stage work may
continue without falsely assigning an unaccepted milestone label.

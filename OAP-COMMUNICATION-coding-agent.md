# Coding communication — revision 1 / project protocol 2.0

P-STATE-01. GitHub=software truth; immutable orders/reports/active history=protocol
truth; FIFO=sync only. Role/cwd/home must agree before launch. Read exact ASCII
active ID plus one LF; absent inactive, malformed invalid. Match one
oap/orders/ID-slug.md; never newest/mtime. Drafts cannot execute. Final order
metadata is one oap-metadata JSON fence plus required readable sections. Source
hashes, concrete H/A/E/I/C provenance and numbered acceptance must validate through
shared helpers. Resolve genuine current-state markers; quoted fixture text is data.

P-ID-01. Grammar ^[0-9]{3}-[a-z]{1,2}$, suffixes a…z then aa…az, ba…zz (not
lexicographic). NNN-a CREATE_NEW_PR; corrections AMEND_EXISTING_PR on SAME branch
and PR. No ID increment on context/process/model/provider/machine loss. Interrupted
a reuses verified existing PR. Conflict/duplicate requires reconciliation. zz
exhaustion requires reviewed protocol revision, not new objective. Strategy alone
publishes scope after review; new numeric objective follows verified merge or
explicit abandonment/disposition/dependency reassessment.

P-DHA-01. Every final order has heading `## Deferred human adjudication` and exact
`- Decision: NONE` or `- Decision: APPEND CRIT-NNNN`. NONE normal. APPEND contains
complete critical-entry fenced payload with all canonical labels/attestation,
UTF-8 byte length/hash and trusted prior full register length/hash. Extraction is
after opening fence LF through immediately before closing fence, retaining payload
final LF. Longer fence prevents accidental closure. Mitigation-only NONE uses
`- Mitigation update: UPDATE CRIT-NNNN` and critical-update fence. Exact bytes only.
Existing D1 references remain in relevant gates; no extra append implied.

P-DHA-02. Use `python3 oap/bin/append_critical.py --repo-root PATH --source FILE
--id CRIT-NNNN --accepted-ref SHA` only for active authorization. Optional --dry-run
writes nothing. Prior accepted Git blob must match ordered size/hash, seed prefix
and entire earlier history. Reject duplicate IDs, invented text, stale bases,
symlinks, bad schema and all human-disposition payloads. Append before implementation
SHA. Verified identical replay no-ops; conflict stops without partial append.
Mitigation/supersession does not clear gate; agents never append human decisions.

P-FIFO-01. Wrapper waits externally and consumes control ONCE before your invocation.
Do not wait a second time. Synchronization bytes exactly ASCII OK (4f4b), no LF,
ID/JSON/status. Sender closes descriptor; reader validates complete frame through
EOF, fragments allowed, wrong/extra/empty frame rejected. Use `python3
oap/bin/oap_fifo.py send --fifo PATH` for response after verified publication.
Never echo. OS waiting uses zero idle model calls. OK does not mean COMPLETE.

P-SELF-01. Implement/test/docs only scope; exact critical append in implementation.
Commit/push all non-report work including activated order/active. Create a single
PR for a or adopt/amend existing PR for later/recovered round BEFORE composing final
report. Never merge/auto-merge. Repair safe in-scope CI; finish/push non-report work.
Record literal implementation head SHA after all such changes.

P-SELF-02. Write immutable oap/reports/ID-slug.md matching order filename. One
oap-report JSON metadata fence records result COMPLETE/PARTIAL/BLOCKED/FAILED;
order ID/path/hash/governance; actual PR number/URL/mode/state/branch/base/start SHA;
implementation head literal; publication_commit SELF; implementation/docs,
per-criterion/negative/boundary evidence; each command PASSED/FAILED/SKIPPED/NOT RUN/
BLOCKED/PENDING/MISSING with observed tested SHA; setup/privacy/resource/limits,
critical action, human gates and no-merge/scope confirmation. Record PR observation
and report-writing timestamps. publication_verified=false: future push/CI is not
observable inside pre-push report. Every check SHA belongs to implementation history.

P-SELF-03. Final round commit stages ONLY exact report path, with implementation
SHA as sole parent. No code/CRITICAL/order/active/metadata fixes there. Push, then
`python3 oap/bin/verify_report.py --repo-root PATH --id ID --repository OWNER/REPO`
independently checks remote head/branch/PR, actual report bytes, parent and changed
path. Without --repository output is local-only, insufficient to notify. Put actual
post-publication verification in bounded private receipt/strategic review; do not
amend report to claim it. After remote verification send response OK and exit.
No later mutation/push for this round. Truthful non-COMPLETE reports also notify.

P-RECOVERY-01. Nonzero exit, report publication failure or inconsistent state:
preserve work/private incident; no false response and no automatic replay. Report
already local but remote-unverified → complete/reconcile publication, never rewrite.
Remote report/lost response/duplicate control → strategic review, suppress coding.
Unfinished consumed order → deliberate reconciled same ID/branch/PR resume from
first unfinished requirement. Recovery may re-signal only after recorded reason.
Pending CI → wait/recheck; no new suffix merely for waiting. Quit leaves live shell;
no automatic resurrection. Role locks prevent duplicate models.

P-GATES-01. Shared check_state/check_governance/verify_report back doctor/launch/
publication/review. Hash/schema checks establish integrity, not human provenance,
semantic D0/D1/D2 truth or product correctness. Candidate review uses trusted
accepted base plus explicit ordered changed paths; runtime private strategy remains
accepted-old until quiescent post-merge refresh. No missing CRITICAL reseed.

P-REVIEW-01. Strategy verifies remote publication and independently reviews exact
final head/diff/all rounds/meaningful tests/docs/risk/DHA/rollback and strongest
reason not to merge. Missing/pending/cancelled required checks block. Head change
requires re-review; verify actual merge/default head. Development merge not release;
deploying merge is D2. Latest verified human ACCEPTED clears only registered gate,
not separately missing deployment rights. ICA is independent architecture/main
audit and repeated after remediation, never execution self-approval.

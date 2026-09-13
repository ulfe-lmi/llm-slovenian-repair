# Forward recovery of an invalid immutable report

An immutable report can be structurally published while failing strict report
validation. It must remain unchanged and must not be treated as accepted. The
only supported recovery is a new immutable order on the immediate next suffix
of the same objective, branch, and open pull request.

The recovery order carries `prior_report_recovery` with the exact
`INVALID_QUARANTINED` classification, corrective ID, and meaningful reason.
The shared proof checks the prior order and report directly from their
publication commit, including exact paths/bytes, SHA-256 values, the report
blob, first report-only publication, its sole implementation parent, the
existing report-history guard, and the declared `REPORT_CHECK` failure. With a
remote during the initial publisher transition, it additionally checks the
open PR, branch, base repository, and that the PR head is still the prior
publication. After the corrective order is active, state checks use the local
structural proof; a present corrective report is then strictly remote-verified
on its own head. Metadata is evidence to verify, not authority to mutate history
or accept a report.

Useful read-only commands are:

```text
python3 oap/bin/oap_cli.py forward-recovery --repo-root REPO --id 007-e --repository OWNER/REPO
python3 oap/bin/oap_cli.py preflight-report --repo-root REPO --id 007-e --source DRAFT.md
python3 oap/bin/oap_cli.py transcript --index
python3 oap/bin/oap_cli.py transcript --revision HEAD
```

`preflight-report` is for the unpublished draft and rejects the active ID once
its report path exists. It requires the active order, the exact order identity,
`SELF`/pre-push claims, full 40-character check commits, an actual
implementation `HEAD`, and ancestor checks. It does not claim remote
publication. The old report continues to fail `verify-report`; a transcript
that contains a proved immediate corrective order reports it separately as
`INVALID_QUARANTINED`, while the corrective report is the only report eligible
for strict acceptance. Transcript revision checks also require the selected
corrective order bytes, immediate sequence, fixed-publication ancestry, and
post-publication introduction chronology.

This mechanism does not amend, delete, restore, or rewrite historical reports,
does not create merge or release authority, and does not clear a human gate.

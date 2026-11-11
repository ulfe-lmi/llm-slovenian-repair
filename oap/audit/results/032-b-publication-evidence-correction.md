# 032-b publication-evidence correction for the 032-a report

Status: evidence-only suffix to objective 032 under the 032-b order (D0),
same branch oap/032-functional-proxy-closure-audit and PR 34. No product,
test, dependency, governance, manifest, audit or prior-report byte changes.

## Exact prior report preserved

The published 032-a report is identified and preserved immutable:
oap/reports/032-a-functional-proxy-closure-audit.md, 22841 bytes,
SHA-256 0e8934321f6d1add36968ab50cc0d19ec7846293552cb1b5177b065ff50a0505,
committed at 4a63cbb759d44c6614d7db67c895b560d31d85f6 (sole parent
8549db27cb8761e33301f516ef95cae9a0edfb4a, sole report path), byte-identical
to the retained private draft (Root-verified). This artifact supersedes
exactly two statements in that report's checks array and no other claim.
All substantive findings remain in force, including the installed-Pandoc
protection gap (LR-007, A-PROTECT-01, A-SPAN-01, A-ACCEPT-02, MVP-5, D03,
with the exact source positions pandoc_protection.py:129-132, :797-835,
:654-680 and :920-922), the frozen initial source-first derivation
(SHA-256 2c5899726f4fafa0b080ba63951db613339fe37d566037845c98b037205dd052),
the S1/S2/PA/PC/PD results and ordinary negative tests, the carried 031-b
native failure (ENVELOPE_INVALID, 4/4 ledger, UNPROVEN) and every other
evidence limit.

## Supersession 1 - counter check "re-verified after publication"

Superseded text (checks[6], result FAILED, details): "the report-only commit
reconciles it (90 .md files, 89 counted, block 89), re-verified after
publication and recorded privately."

Correction: at composition the 032-a report was unpublished, so the
"re-verified after publication" clause was prospective; no such
verification existed at composition. The observed pre-report mismatch
(block 89 vs 88 counted at the 032-a implementation head,
AssertionError 89 != 88) is unchanged and correctly recorded. Publication
later yielded 90 .md report files / 89 counted against block 89, so the
designed mismatch reconciled. The actual post-publication results,
attributed to their real command, time, SHA and actor, are:

- coding (032-a post-publication receipt, private, 7280 B mode 0600,
  recorded 2026-11-11T02:24:23Z): at 4a63cbb,
  env OAP_ROLE=coding qualified python -B -m pytest -p no:cacheprovider
  research/tests/test_research_state_consistency.py::ResearchStateConsistencyTest::test_registry_and_report_counts -q
  -> 1 passed in 0.05 s, rc 0 (block 89 == counted 89 = 90 .md files minus
  the 007-o exclusion).
- strategic (Root receipt
  032a-root-report-helper-modes-and-final-counter-observation-20261111.json):
  qualified python -B -m pytest -p no:cacheprovider
  research/tests/test_research_state_consistency.py -k
  test_registry_and_report_counts -q at 4a63cbb -> actual exit 0,
  "1 passed, 10 deselected in 0.05s", observed 2026-11-11T02:18-02:19Z;
  a post-publication result only, not evidence of earlier execution.

The prospective wording is not retroactively repaired; the two records above
are the actual later results, separately attributed.

## Supersession 2 - known-key check message count and report-commit scan timing

Superseded text (checks[9], result PASSED, command): "private known-key
scans: the six staged non-report blobs before the scoped commit and both
non-report commit messages; the report draft plus the report commit blob
and message before publication (counts only)".

Correction: there is exactly one non-report implementation commit
(8549db27cb8761e33301f516ef95cae9a0edfb4a) and one report commit
(4a63cbb759d44c6614d7db67c895b560d31d85f6); "both non-report commit
messages" is wrong. The report commit's blob and message did not exist at
draft composition, and describing their scan as completed before
publication was a timing error; that portion was NOT YET RUN at
composition.

Scans actually completed before publication (actual scope; value never
printed; counts only): the five staged non-report blobs (order, oap/active,
requirements-first, audit, evidence), the two commit messages
(implementation commit 8549db2 and base commit 2f0d9c47) and the exact
private report draft (SHA-256 0e893432...) - all 0 hits. The modified
research/RESEARCH-STATE.md blob was not among that scan's targets.

Actual later scans, cited separately (post-publication, count-only):

- coding (032-a post-publication receipt, recorded 2026-11-11T02:24:23Z):
  the report blob at 4a63cbb and the report commit message -> 0 + 0 hits,
  total 0 (private helper scan_report_commit.py).
- strategic (Root receipt
  032a-root-published-report-and-two-evidence-overclaims-review-20261111.json,
  at 2026-11-11T02:18:18Z): 7 changed blobs, 2 actual commit messages and
  the exact private draft -> 0 hits; a post-publication Root execution, not
  an earlier coding execution.

A post-publication scan does not remedy the original timing error; it is
recorded only as its actual later result.

## Preserved valid proof (not superseded)

The actual 032-a unpublished preflight PASSED on the exact draft bytes
0e893432... while the canonical 032-a report was absent: Root chronology
call_aca3625f9ff759cc, 2026-11-11T02:16:20.282-.499Z, rc 0, "valid
unpublished report draft", expected-head 8549db2...; the
builder-generation candidate at 02:10:30.599Z (call_a821ea28f999d872) is
not a preflight. The canonical report bytes are identical to the draft and
the report commit is sole-path with sole literal parent 8549db2...; REMOTE
verification passed (Root: scope remote, exit 0 at 4a63cbb, ~02:18Z;
coding receipt: result verified, report_count 90, frozen 006-a/006-c
incidents intact). This 032-b round's preflight proves only 032-b; no
retroactive preflight or replacement test is run or claimed.

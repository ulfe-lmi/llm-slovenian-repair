# 031-c Evidence and Publication Correction

Bounded correction artifact for order 031-c. It supersedes the specific
inaccurate execution/provenance statements of the immutable published 031-b
report; it does not alter those bytes:
`oap/reports/031-b-close-proxy-and-preserve-order.md`, 24642 bytes, SHA-256
`d73ec576157f2daba5a6484babe041e8ed9baf51074aae7c04f9d83a215e7788`, published
in commit `c29337422d7f1ea84cb8af3ce625b476ff5ffd50` (sole parent
`296aa8ee0767c0ce5e70d0458f059941185eb285`). The substantive evidence of that
report, including the failed native round trip, remains as recorded; only the
statements below are corrected against the actual command history and the
Root source-bound receipts (private 031-b review receipts under the
STRATEGIC_HOME workorder root).

## Corrections

1. Focused 153/66/114.21 s run - actual module list and provenance. The
   actual focused run (launch 2026-11-10T20:01:38Z, 031-b epoch) was the
   qualified interpreter with `-B -m pytest -p no:cacheprovider` over exactly
   five modules: `concept-verification/tests/test_main_lifecycle.py`,
   `test_owned_startup.py`, `test_request_admission.py`,
   `test_request_cancellation.py` and `test_concept.py`; the complete pytest
   summary is 153 passed + 66 subtests in 114.21 s, PASSED. The 031-b report's
   check entry instead named test_main_lifecycle, test_whitespace, test_proxy,
   test_pandoc_protection and test_concept: an incorrect list -
   test_whitespace, test_proxy and test_pandoc_protection were not in that
   focused launch. The literal run's HEAD was the 031-a report head
   `9d5f012cb3731043c442af57e076a2e89229a1b3` with the then-dirty final source
   bytes, later proven byte-identical to
   `296aa8ee0767c0ce5e70d0458f059941185eb285`; source equivalence is not a new
   execution at that SHA. The shell wrapper piped pytest to `tail`, so the
   captured rc 0 is the pipeline/tail status, not a separately recorded pytest
   exit code; the pytest summary itself reports PASSED. No rerun was performed
   solely to replace this provenance.
2. Whitespace verification - actual command. The actual focused whitespace
   verification used the qualified interpreter with
   `-B -m unittest discover -s oap/tests -p test_whitespace.py -v` (Root-run:
   14 tests, 6.455 s, literal closed 0), not a pytest command. The two file
   hashes at the literal run (`check_whitespace.py` `61dfb231...`,
   `test_whitespace.py` `4bd6f65b...`, literal head `9d5f012` with dirty
   bytes) were later proven identical to the `296aa8ee` bytes. The
   literal-execution/dirty-source/equivalence distinction is preserved. Both
   actual whitespace CLI bases passed with exactly five incidents; the
   closed-five contract and the issued 031-a order bytes are unchanged.
3. Independent 30-second clocks - five, not four. The new lifecycle test
   source asserts FIVE independent 30.0 s main budgets (header, client/intake,
   delivery, setup, capture; see the BUDGETS assertion in
   `test_main_lifecycle.py`), not "30.0 x4" as the 031-b report stated.
   Observed module size: 12 tests + 6 subtests; the unsupported
   "16 bounded owned-child scenarios" count is withdrawn.
4. Interpreter/umask scope of the "every helper" claim. The 031-b report's
   "every helper: qualified Python 3.12.15 -B, umask 077" statement was
   overbroad: the actual metadata/helper commands (oap_cli state/governance/
   transcript/report-history invocations and shell/git helpers) also used the
   ambient python3/shell environment. The qualified product/native/static
   proofs (focused pytest, the native harness, the Root-qualified
   mypy/Ruff proof) remain separate and accurate as recorded. New helpers in
   this order use the explicitly supplied qualified interpreter, -B, explicit
   OAP_ROLE=coding, actual shell umask 077 and private cache roots.
5. 031-b unpublished preflight - NOT RUN / UNPROVEN. No preflight-report
   invocation with a private `--source` and the canonical 031-b report absent
   is established by the actual foreground command history; the 031-b report's
   A4 wording ("normal unpublished preflight ... all shared checks RC 0")
   conflated the shared governance/transcript/report-history checks with the
   publication boundary. The 031-b preflight is therefore marked
   NOT RUN/UNPROVEN; it is never retroactively labeled PASSED and its
   timestamp/history is not repaired. The actual 031-c preflight (private
   final source, canonical 031-c report absent, `--expected-head` = literal
   implementation head) proves only this new round.
6. Published-report framing and old-bytes negative provenance. Published
   reports are pre-publication evidence records, not permanently private
   artifacts; the 031-b report's closing "PRIVATE unpublished preflight"
   framing is superseded as a label of the published canonical file. The
   old-bytes regression negative was executed against the `9d5f012` product
   bytes in the 031-b epoch (test-source revision of that epoch) and is
   preserved under that provenance and its limits; it is not relabeled as a
   literal rerun against the final reformatted test bytes at `296aa8ee`.

## Preserved unchanged

- The failed actual RTX 3090 native result (031-b R13): HTTP 200, 2105 B,
  4.721 s, ENVELOPE_INVALID (exact rejected field unknown and not diagnosed),
  native compatibility/edit UNPROVEN; actual main return 0, no main error,
  shutdown finished, serving worker joined, listener closed, child rc 1,
  parent no forced kill; review slot RESERVED_UNKNOWN with 0 observed review
  calls; original ledger fully allocated 4/4 - no reset, recycling, retry or
  new live traffic under this order, regardless of any separately discussed
  future allowance.
- The earlier A100 15 s / 45 s reviewer measurements remain separate
  evidence.
- No product, test, dependency, governance, manifest, registry, prior-report
  or prior-order byte changes in this round: scope is exactly four non-report
  paths plus the sole 031-c report.

## Counter

`research/RESEARCH-STATE.md` machine block `oap_reports_reviewed` advances
87 -> 88 only, anticipating the 031-c report. At the 031-b head there are 88
Markdown reports (87 counted after the existing 007-o exclusion) against block
87: reconciled. At the final 031-c report head there will be 89 Markdown
reports (88 counted) against block 88. Registry 42 and incidents 2 are
unchanged. The expected pre-report mismatch at the 031-c implementation head
(88 != 87) is preserved as such - not rolled back, repaired or waived.

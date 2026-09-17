# Work order 007-f — Complete faithful research archive and CI-portable reproduction

Status: FINAL

```oap-metadata
{
  "id": "007-f",
  "title": "Complete faithful research archive and CI-portable reproduction",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": [
    "001",
    "002",
    "003",
    "004",
    "005"
  ],
  "local_work": "Local and remote PR #8 head 5feb8d0d790a89b496bbd1581cd6db345fdc138a. Preserve all published 007-a..e history and private originals. Adopt the sole dirty research/tests/test_strategic_campaign_replay.py regression as authorized archival work; do not discard or rewrite it.",
  "prior_review": "007-e report is strict-remote-verified at 5feb8d0d790a89b496bbd1581cd6db345fdc138a with implementation parent 17ee857e95c916b8733973e68cb4b9898efc50fe; 007-d remains INVALID_QUARANTINED. Final-head Research reproducibility and OAP report history pass. OAP bootstrap fails only because new recovery tests hard-code /home/ubuntu persistent scratch on GitHub; Application baseline remains inherited/out of scope. Independent research audit identifies concrete replay, dispatch, prompt, request-key and manifest-recipe gaps.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner 2026-09-11/12: preserve every experiment and result, publish all safe reproducibility code/documentation under research/ on one PR, keep private bytes outside /tmp, and authorizes all forward-correction paths. No experiment rerun or merge."
    },
    {
      "kind": "I",
      "reference": "Strategic 007-e independent review cbc94ce226a875e6eaba3d39343b8f69525bb3c7fee9e6ce4df30e9ca6be90a2 plus research-correction review 4b47d2f3f62b3fb4e3a80543a4aa1e8d15f906111ff09b646211bffcc10b2e30: 15 retry-only M2 replay failures, latest-pipeline dispatch substituted for historical variants, multi-target request capture collision, prompt/config contradictions, incomplete original-attempt mapping and broken compressed-census verification recipe."
    },
    {
      "kind": "E",
      "reference": "Full preserved campaign offline replay: 16,375 M3 matches and 16,360 M2 matches/15 failures, all retry-only operational failures; zero network/model calls. Source mirror has 183 exact census-matching files. Public research at 5feb8d0 inherits 119 files, 21 root study pairs, 50 child records and 225,757 census entries."
    },
    {
      "kind": "C",
      "reference": "007-e GitHub OAP bootstrap log at final head: all 16 forward-recovery tests error before test bodies with PermissionError creating hard-coded /home/ubuntu path. Correct fixture portability without weakening its persistent/local no-/tmp boundary. The 007-e report's transient-output claim is corrected forward, never amended."
    },
    {
      "kind": "A",
      "reference": "S-ORDER-03/S-REVIEW-01: next suffix on the same objective branch/PR after a published report. The owner explicitly authorized forward corrections and continued archive completion; no numeric advancement, merge or scientific run."
    }
  ],
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514",
    "oap/governance/DISTILLATION-MAP.md": "a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7",
    "oap/governance/WORKSPACE-LAYOUT.json": "cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254",
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "lr": [
    "LR-007",
    "LR-008",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "OAP report history",
    "Application baseline",
    "Research reproducibility"
  ],
  "decision_class": "D0"
}
```

## Identity

Immediate suffix after strict-valid 007-e, SAME objective 007 branch and PR #8.
FINAL ARCHIVAL CORRECTION. This is not a new experiment and makes no scientific,
milestone, merge, release or deployment claim.

## Provenance

The owner’s durable all-experiment publication request remains the governing goal.
The existing archive is substantial but independent executable review contradicts
its claim of faithful variant reproduction. Correct the known gaps from preserved
facts and actual owned source; do not replace them with plans, contracts or stubs.
007-e is preserved. Its protocol fix is accepted for transition, while its
GitHub fixture portability failure and transient-/tmp wording are corrected here.

Mandatory private reviews, read in full:

- STRATEGIC_HOME/workorders/research-correction-after-007e-review.md
  SHA256 4b47d2f3f62b3fb4e3a80543a4aa1e8d15f906111ff09b646211bffcc10b2e30
- STRATEGIC_HOME/workorders/007-e-independent-review.md
  SHA256 cbc94ce226a875e6eaba3d39343b8f69525bb3c7fee9e6ce4df30e9ca6be90a2
- persistent 007-d-scratch/executable-source-review.md
- persistent preservation RELOCATION.json and SOURCE-MIRROR-RECEIPT.json

## Current verified state

Main remains ee2d1b479719009ff1d07829478f241e3f395f7c. PR #8 is OPEN,
unmerged, branch oap/007-concept-verification at local/remote
5feb8d0d790a89b496bbd1581cd6db345fdc138a. That report-only commit has
sole parent 17ee857e95c916b8733973e68cb4b9898efc50fe and strict remote
verify_report passes. Revision transcript lists 007-d only as
INVALID_QUARANTINED/REPORT_CHECK and 007-e as accepted. Research reproducibility
and report history CI pass. OAP bootstrap fails at the host-specific fixture path;
Application baseline remains inherited and must not be repaired here.
The sole dirty file is the strategic retry-only replay regression named in metadata.
Main protection remains disabled; do not change settings or merge.

## Governance

Metadata lists unchanged accepted governance identities. CRITICAL remains empty
and READ ONLY. D0/NONE. Owner permission covers owned code and safe, data-free
research evidence. It does not authorize publishing dataset/corpus/index/archive
bytes, filled examples, prompts containing source rows, raw responses/reasoning,
credentials, private endpoint/profile data, or a new code-license decision.
Generic historical prompt templates and executable client/driver code are allowed.
No live model/service authority is implied by publishing dormant source.

## Goal and dependencies

Make the repository research/ subtree a navigable, truthful and actually runnable
reproduction archive for every preserved experiment, recovery, variant, campaign
and analysis, while every unsafe original stays hash-addressed in persistent
private storage. Resolve all concrete 007-d independent-review gaps. Restore the
new OAP recovery tests on GitHub without changing protocol semantics. Leave one
reviewable PR #8, open and unmerged.

## Scope

Allowed: research/**; oap/tests/test_forward_recovery.py solely for portable
scratch selection; oap/GENERATED-FILES.json only if the permitted test path
identity changes; exact 007-f order/active/report; PR #8 metadata. A narrowly
required research workflow update is allowed only for research checks.
READ ONLY: production src/tests/scripts/locks, pyproject/uv.lock, concept-
verification/**, OAP helpers implemented in 007-e, governance, CRITICAL, all prior
orders/reports/commits, model/service/profile/network configuration, source
datasets/indexes/archives and original private experiment trees.
Do not mutate unrelated files.

## Non-goals

No new Qwen/Codex/model call, response resampling, experiment, benchmark, tuning,
threshold/prompt/pipeline change, corpus acquisition, human/strategic linguistic
labels, production repair/refactor, Application-baseline repair, release, merge,
deployment, auto-merge, public service exposure, source redistribution, history
rewrite or new numeric objective.

## Files and boundaries

Use only exact bounded source mappings in the reviews and verified native
source mirror; avoid broad FUSE scans. Preserve original private bytes and receipts.
All local fixtures, logs, environments, staging trees and derived checks use a
uniquely owned persistent path under:
 /home/ubuntu/.local/share/llm-slovenian-repair/research-runtime-20260911.YJemoq/
On GitHub Actions, use its caller-owned RUNNER_TEMP or explicit TMPDIR; never
hard-code /home/ubuntu. On this host do not create or leave task artifacts in /tmp.
Fakes replace HTTP/model edges, never the actual driver/routing/gate being proved.

## Requirements

1. Preserve every report/order/commit and every original private artifact. Verify
   the exact identified experiment-owned /tmp roots remain absent. Do not rebuild,
   normalize or overwrite original freezes, reports or numeric receipts.
2. Fix only the portability defect in oap/tests/test_forward_recovery.py:
   explicit safe TMPDIR wins; GitHub's RUNNER_TEMP is an allowed disposable
   runner-owned fallback; no hard-coded host path on another machine. On this host
   a missing safe location fails before using /tmp. Test local persistent,
   GitHub-like, absent and /tmp-rejection cases. Do not weaken any 007-e guard.
3. Correct the immutable 007-e setup claim forward: record that one interrupted
   diagnostic shell briefly created four exact /tmp streams, which strategy moved
   to persistent interrupted-tmp-diagnostics and verified absent. No scientific/
   dataset/model content was involved. Never edit 007-e.
4. Fix replay of all 15 retry-only operational failures. A failed corrective call
   makes M2 fail closed to the complete original; M3 still retains healthy
   first-stage edits when its own first calls succeeded. Do not ask for a missing
   retry proposal or relabel failure as KEEP. Incorporate the dirty strategic
   regression. Run the full actual saved campaign replay: all 16,375 M2 and all
   16,375 M3 outputs/failure flags must match, with zero model/network calls.
   Derive detector.maximum=null from verified global configuration, and support
   nested detector.english without weakening missing-evidence failures.
5. Replace the latest-pipeline-for-everything dispatcher with faithful executable
   historical variant routing using the preserved owned sources. Cover separately:
   original 007-a/b attempts and replacement executions; four mechanical reasoning
   variants; validator; contextual JSON unigram retry; word-only retry plus saved
   whitespace continuation; hyphen-only; one-way and symmetric case rules; three
   ten-trial schedulers/stopped trials; capped/uncapped/spelling/final campaigns;
   retry-limit-ten; u/v/scoring analyses and the unavailable inline Levenshtein
   source. Preserve actual call-reuse, retry/trial/worker/failure semantics.
   A future authorized fresh run may be stochastic; this is source reproduction,
   not claimed response identity. No variant may silently require later English
   evidence or later gates absent from its historical configuration.
6. Make the documented CLI/entrypoint invoke those actual drivers. Endpoint/model,
   reasoning, timeout, maximum cases, workers, trial count, retry limit and resource
   flags must be routed or rejected—not accepted then ignored. Default/import/
   plan modes make zero network/model calls. Live mode requires explicit opt-in,
   endpoint, credential reference, bounded caller-owned inputs/index/output and
   retains immutable capture. Do not execute live mode in this round.
7. Fix per-request persistence identity. Multiple selected targets, stages and
   trials must use deterministic distinct paths; rerun/restart verifies and reuses
   identical saved requests. A changed request at the same identity still fails.
   Never weaken Client's saved-request-differs guard.
8. Publish exact data-free historical instructions and request semantics. Correctly
   distinguish the 1,442-byte contextual JSON retry
   (SHA256 79995ff7868cd307bf96f18916583b5ac310cc81d18b6ca70098185e79d93818)
   from later context-free word/expression retries. List actual API wire keys
   separately from content descriptions. State that source sentences were sent
   to Qwen but excluded from public Git. Remove contrary generic prose without
   exposing filled inputs/responses. Map original 007-a/b attempts distinctly.
9. Repair the documented archive-integrity command. It must consume the compressed
   exact ledger, understand explicit logical-root to current-private-root mappings
   for strategic and relocated native trees, validate size/SHA/disposition, and
   fail clearly on missing/mismatched/private roots. Test the command from a fresh
   public checkout with synthetic multi-root data and against the surviving private
   identities without exposing their content. Do not pass the summary JSON where
   an entry ledger is required.
10. Upgrade source-manifest function coverage from generic file labels to the
    actual retained functions/classes/entrypoints and exact portability/redaction
    transformations. Prove every claimed historical executable feature is mapped
    to owned source bytes or explicitly UNKNOWN/MISSING. Do not invent the inline
    Levenshtein source hash or physical original-index equivalence.
11. Reconcile the catalog, per-study config/report projections, safe numeric
    evidence and README links for all original roots and child runs. Preserve
    actual STOPPED/PARTIAL/INVALID statuses, repeated-32-case denominators,
    replacement-vs-original executions, campaign phases/incidents, official vs
    custom metrics, no-reference limitations and the explicit IRRELEVANT MultiGEC
    structural mismatch. Do not call non-reference changes harmful or fabricate
    semantic ground truth.
12. Retain private/public separation: no dataset/source/reference text, gold/
    proposal strings, filled prompts, raw responses/reasoning/traces, credentials,
    private endpoint/profile, corpus/index/archive/model bytes, or data-bearing
    keys in Git/report/CI logs. Re-run staged-byte and known-source overlap guards
    across the complete intended research tree using prepared hashed private
    inputs. Public hashes, counts, numeric aggregates and generic templates remain
    usable. Preserve upstream notices and explicit redistribution limits.
13. Add focused tests that exercise every distinct historical dispatch family
    through its real CLI/driver using synthetic records and fake transport.
    Assert actual request body/prompt/reasoning/retry/case/gate/call count,
    trial/worker partition, capture identity, saved failure, offline default and
    no later-policy contamination. No tests may encode desired live Slovenian
    answers. Run the complete research test suite.
14. Update PR #8 body through GitHub metadata only with final navigable research
    scope, exact statuses, remaining private/remote limitations, CI state, and no
    merge/release/deployment claim. Real Markdown newlines; link durable research
    and OAP reports rather than reproducing private evidence.
15. Before report publication perform a requirement-by-requirement completion
    audit against actual files and execution, not generated manifests alone.
    Any genuine remaining source/evidence loss stays explicit. Do not publish
    COMPLETE if a claimed runnable variant still routes to the wrong implementation,
    the full replay has any unexplained mismatch, the integrity recipe is broken,
    a safe known study lacks a projection, or a task artifact remains in /tmp.

## Acceptance criteria

- Historical 007-d/e and all originals are unchanged; exact old hashes reverify.
- OAP recovery semantics/tests remain unchanged and OAP bootstrap CI is green.
- Full saved replay reports 16,375/16,375 M2 and M3 matches, zero failures and
  zero model/network calls, with retry-only vs first-stage behavior preserved.
- Every catalogued experimental family reaches its correct executable historical
  driver under fake/saved boundaries; variant parameters materially affect the
  correct request/scheduler/gate path and later policies do not leak backward.
- Two targets/stages/trials cannot collide; changed saved request still fails.
- Contextual/word/expression prompt and request documentation matches exact owned
  source while publishing no filled material.
- Compressed-ledger multi-root integrity recipe runs successfully and detects
  negative paths.
- Catalog, README, 21+ per-root projections, child-run records, numeric archives,
  source closure and limitations are mutually consistent and fully linked.
- Complete intended Git research tree passes publication/privacy/overlap guards.
- Research tests, Ruff, mypy, OAP tests, transcript index/revision, governance,
  protected-source diff, report history and no-reflog fsck pass at the recorded
  implementation head. Application baseline may retain only accurately identified
  inherited/out-of-scope failures; no new f regression.
- GitHub final head has Research reproducibility, OAP bootstrap acceptance and
  OAP report history green. PR #8 remains open/unmerged.

## Verification

Run focused dispatch/replay/capture/manifest/privacy negatives first. Run the
complete 16,375-record saved replay from persistent private evidence with output
receipts under persistent scratch. Then run:
python3 -B -m unittest discover -s research/tests -v;
Ruff and mypy over research scope using a persistent isolated environment;
python3 -B -m unittest discover -s oap/tests -v;
the native locked/offline application baseline and record inherited failures;
check_transcript index and full implementation revision; check_report_history;
accepted-runtime governance against literal main SHA; protected source diff;
git fsck --full --no-reflogs; staged publication guard and source-overlap scan.
Set TMPDIR explicitly on this machine. Use GHA-equivalent environment tests for
RUNNER_TEMP portability. Record commands, full tested SHAs and distinct
PASSED/FAILED/SKIPPED/BLOCKED status. Never claim future report-push/CI success
inside the pre-push report.

## Local setup and constraints

Ordinary reversible setup for a persistent research-only lint/type environment is
allowed outside Git; do not modify production dependencies or lock. Use existing
native verified source mirror and persistent private campaign/index paths. Validate
hashes before consumption. No source acquisition, no server contact, no Qwen/Codex
workload, no external scoring submission. Limit concurrency to CPU-safe offline
work. Remove only exact owned disposable test directories after evidence is saved;
never delete original experiment/archive/index trees.

## Documentation

Update research/README.md, EXPERIMENT-HISTORY, registry/config/report/result
projections, source mappings, reproduction and integrity instructions so a reader
can locate every study, reproduce each algorithm with their own authorized
resources, replay saved private evidence offline, and understand what is missing.
Add a concise public archival incident/correction note if needed. Preserve exact
numeric denominators and avoid product/milestone/linguistic acceptance claims.

## Git and report publication

SAME branch oap/007-concept-verification and SAME PR #8. No merge.
Commit the exact 007-f order/active transition, implementation, tests and docs.
Never include private source/data or unrelated files. Before final commit inspect
staged bytes and report-history invariants. Push non-report implementation, verify
remote head, then create and run preflight-report on an unpublished 007-f draft.
Final commit changes ONLY the new 007-f report path and has the actual implementation
head as sole parent. Push once, verify remotely, send exact OK, and exit.
If anything fails, report truthfully and preserve evidence; never amend a published
report or rerun scientific inference.

## Decision classification

D0: owner-authorized archival completion and forward correction using existing
evidence. Strongest concern: publishing executable historical clients or detailed
results could leak restricted data or falsely promise bit-identical science.
Mitigation: explicit live opt-in/resources, zero-call tests, data-free generic
templates, strict staged/privacy guards, exact source mappings and limitations.
No D1/D2 boundary or CRITICAL append is needed.

## Deferred human adjudication

- Decision: NONE


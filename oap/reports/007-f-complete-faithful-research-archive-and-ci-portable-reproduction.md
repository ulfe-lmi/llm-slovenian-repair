# Work report 007-f — Complete faithful research archive and CI-portable reproduction

```oap-report
{
  "id": "007-f",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-f-complete-faithful-research-archive-and-ci-portable-reproduction.md",
  "order_sha256": "516bee9cec2a52f75beba27cc4ae1756426386ab65b5ac2ce62a7c6854dbf87d",
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
  "publication_commit": "SELF",
  "implementation_head": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "8fdd5902efd367a602b84f367735e865ca14dbb5",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B research/tools/publication_guard.py --staged-tree .",
      "result": "PASSED",
      "details": "The exact staged-index CLI passed with 126 validated research entries while the ignored worktree .venv/lib64 symlink existed; its success count did not walk the worktree.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests -p test_strategic_publication_review.py -v",
      "result": "PASSED",
      "details": "10 focused publication-guard tests passed, including positive ignored-.venv success and retained staged-leak failure regressions.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -p test_forward_recovery.py -v",
      "result": "PASSED",
      "details": "19 forward-recovery tests passed, including default self-contained execution, explicit validated Git-history source selection, and /tmp rejection.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "All 66 research tests passed with synthetic/fake or saved offline boundaries; no model or network call was made.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "All 123 OAP acceptance, process, report-history, split-layout, transcript, and forward-recovery tests passed.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent PERSISTENT_TMPDIR --command-timeout 900",
      "result": "FAILED",
      "details": "The copied native pytest workspace passed its full pytest command, including all 17 forward-recovery fixtures; cleanup passed. The driver then stopped at the inherited application mypy check with 11 pre-existing ZipInfo/stat_result diagnostics in scripts/verify_source_artifact.py. No application baseline source was changed.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "UV_OFFLINE=1 uv run --frozen --python 3.12 ruff check --select E9,F CHANGED_FILES",
      "result": "PASSED",
      "details": "Changed-file fatal Ruff checks passed after removing the stale unused import; no new fatal lint error remains.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "UV_OFFLINE=1 uv run --frozen --python 3.12 ruff check research",
      "result": "FAILED",
      "details": "The full research scope retains 777 pre-existing Ruff findings across archival files; this round did not broaden or repair that unrelated static debt.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "UV_OFFLINE=1 uv run --frozen --python 3.12 mypy research",
      "result": "FAILED",
      "details": "The full research scope retains 166 pre-existing mypy findings across archival files; the changed publication guard itself passed mypy and no unrelated source was altered.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "offline saved campaign replay against final implementation head",
      "result": "PASSED",
      "details": "Unique final-code-replay-787c420 receipt: 16,375/16,375 M2 and 16,375/16,375 M3 matches, 350 M2 and 335 M3 recorded operational failures preserved, 0 model/network calls, original M2/M3 files unchanged. Details bytes directly match retained SHA-256 b11f927b12fac60eee83a45698d549e3867011ceafe6225e0ddf17089aaecd6b.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/publication_guard.py --root research --private-root PREPARED_PRIVATE_SOURCE",
      "result": "PASSED",
      "details": "The intended research tree and bounded prepared-source overlap scan passed at 126 files; private source content was not emitted.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-f",
      "result": "PASSED",
      "details": "Indexed transcript is valid with 007-f active/latest and 007-d retained only as INVALID_QUARANTINED REPORT_CHECK.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-f",
      "result": "PASSED",
      "details": "Committed transcript is valid at the implementation head.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "Report history remains valid with only the two exact frozen 006 incidents; no prior report/order was mutated.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure and compact coding read-set checks passed; semantic and human authorization proof remain false.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD",
      "result": "PASSED",
      "details": "Acquisition history remains valid with no new archive GET or source acquisition.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 8fdd5902efd367a602b84f367735e865ca14dbb5...HEAD -- protected-source-paths",
      "result": "PASSED",
      "details": "Protected production, governance, lock, historical report/order, and source paths are unchanged from the reviewed checkpoint.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check && git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Whitespace and no-reflog object checks exited zero; fsck reported only pre-existing dangling scratch objects.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    },
    {
      "command": "git push origin HEAD:oap/007-concept-verification; git ls-remote origin refs/heads/oap/007-concept-verification; gh pr view 8",
      "result": "PASSED",
      "details": "Implementation is remotely present at 787c420a03bdf53b7e85fe585d3db2ed8785a03b; PR #8 is OPEN, UNMERGED, and based on main. PR metadata was updated without merge.",
      "sha": "787c420a03bdf53b7e85fe585d3db2ed8785a03b",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-12T07:44:27+02:00",
  "report_written_at": "2026-09-12T07:44:27+02:00",
  "implementation": "Fixed the final staged-index CLI success path so an index-backed --staged-tree invocation derives its success count only from validated regular index entries and never walks ignored worktree files such as .venv/lib64. Added a positive ignored-.venv CLI regression while retaining the staged-leak negative. Fixed copied native-baseline forward-recovery setup by validating an explicit caller-owned Git-history worktree supplied through OAP_FORWARD_RECOVERY_HISTORY_SOURCE; ordinary checkout execution remains self-contained and copied workspaces continue using their copied order/report files.",
  "documentation": "Updated PR #8 metadata with the final navigable scope, final implementation head, exact statuses, replay identity, privacy boundary, and inherited baseline limitation. No repository documentation or historical report was rewritten.",
  "criteria": "Both directly reproduced blockers are corrected. Staged index validation and its success path are separate from materialized-tree walking. The copied baseline full pytest path passes all 17 forward-recovery fixtures and supplies real Git history without a machine-specific path. Positive and negative regressions cover ignored symlink behavior and ordinary/caller-supplied Git-source modes.",
  "negative_paths": "Publication tests retain staged leak rejection, forbidden fields, symlink destinations, overwrite refusal, and overlap negatives. Forward recovery retains absent/unsafe scratch rejection, absent Git-source rejection, history mutation, disconnected ancestry, malformed report/order, remote-head drift, and duplicate-control negatives. Full OAP discovery passed all governance/process negatives.",
  "boundary_fidelity": "Only research/tools/publication_guard.py, its focused research regression, oap/tests/test_forward_recovery.py, and the narrowly required scripts/verify_development_baseline.py test-environment handoff changed. No production repair code, protected source, lock, historical order/report, private artifact, dataset, model, service, or neighboring repository changed.",
  "setup": "Reconciled the consumed SAME 007-f order at reviewed checkpoint 8fdd5902efd367a602b84f367735e865ca14dbb5. Used only persistent TMPDIR under the owner-selected research runtime. Implementation commit 787c420a03bdf53b7e85fe585d3db2ed8785a03b was pushed before this unpublished report draft. The PR body was updated through GitHub metadata only.",
  "privacy": "No model or scientific network calls were made. No dataset rows, source/reference text, filled prompts, raw responses, reasoning traces, credentials, endpoint/profile data, corpus/index/archive bytes, or private worktree paths were added to Git, the report, or PR metadata. The final replay retained hashes, counts, statuses, and zero-call receipts only.",
  "limits": "Result is PARTIAL because the complete native baseline driver still exits at the inherited application mypy failure in scripts/verify_source_artifact.py, and full archival research Ruff/mypy remain pre-existing non-clean scopes. The copied native full pytest portion passed, including all 17 forward-recovery fixtures, and the complete OAP/research test suites passed. This round does not repair that inherited application/static debt or claim a fully green baseline, scientific identity, product correctness, merge readiness, release, or deployment authority.",
  "human_gates": "D0/NONE. CRITICAL is empty. This report records scoped implementation and evidence only; it does not append critical history, accept a report, merge PR #8, enable auto-merge, authorize model calls, or authorize release/deployment.",
  "scope": "Finished only SAME-ID 007-f final CLI/native-baseline recovery. Preserved all prior commits, reports, orders, and replay receipts. The literal non-report implementation head is 787c420a03bdf53b7e85fe585d3db2ed8785a03b. The final publication commit must contain only this report and use that implementation head as its sole parent.",
  "result_summary": "PARTIAL for the ordered round: the two addendum blockers and all directly scoped regressions are fixed and verified, including a unique final-head 16,375-record zero-call replay with directly matching retained details hash. Native copied pytest is green, but the encompassing baseline remains blocked by the inherited application mypy failure; no scope expansion was authorized.",
  "interruption_record": "This same 007-f round resumed after strategy preserved reviewed checkpoint 8fdd5902efd367a602b84f367735e865ca14dbb5 and prior replay receipts. No new suffix, experiment, model call, report rewrite, merge, or historical mutation was used. The report remains unpublished until the report-only commit and independent remote verification complete."
}
```

## Result

The final CLI and copied-workspace Git-history portability blockers are fixed on
the existing 007 branch and PR. The direct replay and all research/OAP tests are
green, with retained failure semantics and zero model/network calls.

## Evidence and limitations

The native copied pytest phase passed all 17 forward-recovery fixtures, but the
overall baseline driver remains PARTIAL at its inherited application mypy step.
The full research Ruff/mypy scopes retain their prior archival findings. No
production or protected-source repair was authorized.

## Deferred human adjudication

- Decision: NONE

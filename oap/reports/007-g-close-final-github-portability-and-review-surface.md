# Work report 007-g — Close final GitHub portability and review surface

```oap-report
{
  "id": "007-g",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-g-close-final-github-portability-and-review-surface.md",
  "order_sha256": "4fd816dff316c6cb1597e977ce26cead0987c11f9d796f1696ef91283f13eae1",
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
  "implementation_head": "178c58275314a32a93a8b3ac0227c014afe67b81",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "32e25c8c9de7e19d427a74e3f4445c1687f461a4",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest oap.tests.test_whitespace -v",
      "result": "PASSED",
      "details": "Six real-CLI disposable-Git tests passed: both exact bases, mutation, missing/deletion-readdition, extra whitespace, diagnostic drift, unknown base, and invalid revision.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "All 66 research tests passed at the 7fec3d5 ancestor; the final 007-g correction has no research-tree changes.",
      "sha": "7fec3d58e5e15d47b244e96607edc0dec9772fba",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "All 129 OAP acceptance, process, recovery, report-history, split-layout, transcript, and whitespace tests passed in a clean detached worktree at the 7fec3d5 ancestor; 178c582 only corrects the copied-workspace Git source used by the same whitespace tests.",
      "sha": "7fec3d58e5e15d47b244e96607edc0dec9772fba",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent PERSISTENT_TMPDIR --command-timeout 900",
      "result": "FAILED",
      "details": "At the final head, uv lock check, frozen dependency sync, focused contracts, copied full pytest, Ruff, and cleanup passed. The driver stopped at the inherited application mypy boundary with exactly 11 ZipInfo/stat_result errors in scripts/verify_source_artifact.py.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision HEAD",
      "result": "PASSED",
      "details": "The literal accepted-base-to-final-head diff check passed with exactly the three reviewed blank-at-EOF diagnostics and all frozen blob/history identities.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_whitespace.py --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "The second authorized accepted-base check passed with the same exact three diagnostics and identities.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/publication_guard.py --staged-tree .",
      "result": "PASSED",
      "details": "The staged-byte publication guard passed with 126 validated public research files and no private payload.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/publication_guard.py --root research",
      "result": "PASSED",
      "details": "The public research tree passed the bounded content and path guard with 126 files.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-g",
      "result": "PASSED",
      "details": "The index transcript is coherent with 007-g active/latest and 007-d retained only as INVALID_QUARANTINED REPORT_CHECK.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-g",
      "result": "PASSED",
      "details": "The committed final implementation transcript is coherent at 178c582.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "The 35-report history remains valid with only the two prior frozen 006 incidents; no historical report path changed.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance passed; semantic and human authorization proofs remain false.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD",
      "result": "PASSED",
      "details": "Acquisition history remains valid with cumulative count 14, current network count 2, and no new source acquisition.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 32e25c8c9de7e19d427a74e3f4445c1687f461a4..HEAD",
      "result": "PASSED",
      "details": "The complete 007-g implementation diff is whitespace-clean.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "git diff --quiet 787c420..HEAD -- research concept-verification resources scripts/verify_source_artifact.py src",
      "result": "PASSED",
      "details": "Research, experiment, source, product, and verifier code are byte-identical to the retained 787c420 closure.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "No-reflog object verification exited zero; 41 pre-existing dangling scratch objects were reported and preserved.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "offline saved campaign replay closure against final implementation head",
      "result": "PASSED",
      "details": "The research closure is byte-identical from 787c420 through 178c582. The retained final-code-replay-787c420 details receipt is b11f927b12fac60eee83a45698d549e3867011ceafe6225e0ddf17089aaecd6b and records 16,375/16,375 M2 and M3 matches, 350/335 preserved operational failures, and zero calls.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "Research reproducibility at implementation head",
      "result": "PASSED",
      "details": "GitHub run 34679136752 completed SUCCESS at exact head 178c582.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance and OAP report history at implementation head",
      "result": "PASSED",
      "details": "GitHub run 34679136707 completed SUCCESS at exact head 178c582, including the new accepted-base whitespace step and report-history job.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at implementation head",
      "result": "FAILED",
      "details": "GitHub run 34679136744 completed at exact head 178c582: copied full pytest and Ruff passed, then the only failure was the inherited 11-error scripts/verify_source_artifact.py mypy boundary.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "git push origin HEAD:oap/007-concept-verification; git ls-remote origin refs/heads/oap/007-concept-verification",
      "result": "PASSED",
      "details": "The non-report implementation head is remotely present at 178c582; PR #8 is OPEN and UNMERGED on the same branch.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    },
    {
      "command": "REST pull-request metadata update for PR #8",
      "result": "PASSED",
      "details": "The PR body now states the exact implementation head, 66 research tests, 129 OAP tests, 126 public research files, replay counts, CI state, inherited limitation, private boundary, open/unmerged state, disabled branch-protection risk, and no release/deployment/scientific-acceptance claim.",
      "sha": "178c58275314a32a93a8b3ac0227c014afe67b81",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-12T08:57:34+02:00",
  "report_written_at": "2026-09-12T09:01:27+02:00",
  "implementation": "Added one fixed OAP whitespace-range verifier with the exact three immutable incident identities and fail-closed Git diagnostic parsing. Replaced both generic workflow diff-check steps while retaining accepted bases, protected-source comparisons, permissions, runners, timeouts, and action pins. Added focused disposable-Git negatives. Updated the development baseline to create and validate an owned child TMPDIR inside each invocation root and to pass that exact value to every child; copied research tests now use the validated original Git history source when the copied workspace intentionally has no .git.",
  "documentation": "The verifier module docstring records the durable exact-incident contract, and the workflow/baseline comments make the accepted-base and owned-TMPDIR boundaries discoverable. No product, governance, PLAN, architecture, CRITICAL, historical order/report, research, source, lock, or service documentation was changed.",
  "criteria": "The exact three reviewed files retain their current blobs, SHA-256 identities, byte sizes, and introduction commits. Both authorized bases pass the literal whitespace check; mutation, missing path, deletion/re-addition, wrong identity, extra whitespace, diagnostic drift, unknown base, malformed-output boundary, and invalid revision are fail-closed. The GHA-like copied full-pytest path passes with parent TMPDIR absent and RUNNER_TEMP supplied, and the encompassing baseline reaches only the inherited 11-error mypy boundary. Exact-head Research and OAP checks are green; Application fails only at that inherited boundary.",
  "negative_paths": "The real CLI tests exercise exact current incidents, changed blobs, deletion and re-addition history, extra trailing whitespace, changed path/line/message behavior, unknown bases, and invalid revisions. Baseline tests prove the child TMPDIR is an owned descendant of the driver root, overrides unsafe/absent inherited values, and lets a copied research fixture run. No validation was disabled and no historical incident was normalized.",
  "boundary_fidelity": "The implementation commit changes only the two named workflows, oap/bin/check_whitespace.py, oap/tests/test_whitespace.py, scripts/verify_development_baseline.py, the focused baseline contract test, oap/active, and the exact 007-g order. The research/product/source/lock/governance/history closure is unchanged; no model, GPU, service, gateway, deployment, merge, branch-protection, or neighboring-repository boundary was crossed.",
  "setup": "Reconciled the consumed SAME-ID 007-g order on the existing branch and PR. Used a clean detached worktree at the final implementation head, existing locked Python/uv dependencies, owned disposable Git fixtures, and owner-selected persistent scratch. The bounded baseline used a 900-second per-command ceiling and passed cleanup. GitHub metadata was updated only through the REST pull-request endpoint because the higher-level gh edit path hit GitHub's deprecated Projects-classic field; no repository state was changed by that failed metadata attempt.",
  "privacy": "No live model or research/network call was made. Locked dependency setup was the only ordinary CI setup boundary. No credentials, endpoint/profile data, customer text, source rows, private datasets/indexes/archives, filled prompts, raw responses, reasoning traces, or private scratch paths entered Git, the report, or PR body. Replay evidence is represented only by retained hashes, counts, statuses, and zero-call identity.",
  "limits": "The result is PARTIAL because the complete native baseline remains non-green at the inherited 11-error application mypy boundary in scripts/verify_source_artifact.py; the hosted Application baseline has the same exact limitation. This round does not repair unrelated application/static debt or claim product correctness, linguistic benefit, scientific acceptance, milestone closure, merge readiness, branch-protection safety, release, deployment, or production readiness. The 41 pre-existing dangling no-reflog objects remain preserved.",
  "human_gates": "D0 / NONE. CRITICAL remains empty. Coding did not append adjudication, accept a scientific result, merge PR #8, enable auto-merge, change branch protection, release, deploy, or authorize live model/service use.",
  "scope": "Finished only the exact 007-g CI/process portability and review-surface correction on objective 007, same branch and PR. Preserved all prior published orders/reports, the 007-d INVALID_QUARANTINED state, research archives, replay receipts, and protected source identities. The literal implementation head is 178c58275314a32a93a8b3ac0227c014afe67b81. This report-only commit must have that implementation head as its sole parent and change only this report path.",
  "result_summary": "PARTIAL for the ordered round: the exact immutable whitespace contract is enforced and tested, copied research tests now run under an owned child TMPDIR with validated Git history, exact-head Research/OAP checks are green, and Application reaches only the inherited mypy debt. PR #8 remains open and unmerged; no scientific, product, release, or deployment conclusion follows.",
  "interruption_record": "The first 007-g implementation exposed one same-round test portability assumption: copied baseline workspaces omit .git, so the new disposable-Git test initially failed before reaching its assertions. That test was corrected in 178c582 to use the already validated original Git history source; the obsolete 7fec3d5 Application run is superseded. No new suffix, replay resampling, model call, historical rewrite, report rewrite, merge, or scope expansion occurred."
}
```

## Result

The exact accepted-base whitespace and copied-baseline portability blockers are
fixed on the existing objective-007 branch and PR. The result remains PARTIAL
only because the inherited application mypy boundary is still non-green.

## Evidence and limitations

The final implementation preserves all three immutable incident blobs and the
007-d quarantine while making the workflow check fail closed for identity,
history, diagnostic, and extra-error drift. The copied full-pytest boundary and
Ruff pass locally and in the exact-head GitHub Application run; the remaining
11-error `ZipInfo`/`stat_result` mypy failure is inherited and outside scope.
Research/OAP tests, public-file guards, transcript/history/governance checks,
protected-source closure, fsck, and replay closure remain separately evidenced.

## Deferred human adjudication

- Decision: NONE

# Work report 007-h — Evaluate unique one-letter unigram substitution

```oap-report
{
  "id": "007-h",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-h-evaluate-unique-one-letter-unigram-substitution.md",
  "order_sha256": "2877026fc6f053d59c624691be8abe175b965f33c8d48ea04a9605261d7ffe2b",
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
  "implementation_head": "608f73bc97964586945832b3cd331f5865cb3fa6",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "f43929da84ef00ea0e00a7bbc645edfaa05f0eeb",
  "no_merge": true,
  "checks": [
    {
      "command": "PYTHONPATH=. python3 -B -m unittest research.tests.test_one_substitution research.tests.test_strategic_addendum_fidelity -v",
      "result": "PASSED",
      "details": "50 focused tests passed, including source-literal privacy, safe public request schema, exact single-newline report EOF, candidate semantics, fallback preservation, and zero-call boundaries.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "All 106 research tests passed at the corrected implementation head.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "frozen baseline replay via load_pairs and validate_baseline_replay",
      "result": "PASSED",
      "details": "The frozen spelling baseline reproduced TP/FP/FN 604/193/911, precision 0.7578419071518193, recall 0.39867986798679866, and first/retry/total calls 2001/209/2210; preservation calls were 920/92/1012 with 23 failures.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "source-literal and exact-scratch privacy audit",
      "result": "PASSED",
      "details": "The three corrective files contain no contiguous absolute temporary or home-path marker; the exact unintended zero-byte non-native RUN-STATUS file was verified and removed, while native frozen status and evidence remained unchanged.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "cached Ruff 0.16.4 check on the three changed files",
      "result": "FAILED",
      "details": "Exactly 17 inherited E501 findings remain in unchanged historical portions of research/tests/test_strategic_addendum_fidelity.py. The corrective lines are clean; unrelated archival code was not refactored.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m research.tools.publication_guard --staged-tree .",
      "result": "PASSED",
      "details": "The staged-byte guard passed with 129 files for the implementation correction and 132 files for the corrected public artifact index; no private payload was staged.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "The final public research tree passed with 132 files; direct checks proved the safe offline request, no absolute path markers, and exactly one final newline in the report.",
      "sha": "608f73bc97964586945832b3cd331f5865cb3fa6",
      "publication_head_claim": false
    },
    {
      "command": "publication guard private-overlap scan over raw datasets, detector snapshots, UV audit, and private result evidence",
      "result": "PASSED",
      "details": "Each bounded prepared evidence subtree passed without public text overlap. The full private-input aggregate was separately rejected on historical baseline-configuration source-window overlaps; this false-positive classification is retained rather than hidden.",
      "sha": "608f73bc97964586945832b3cd331f5865cb3fa6",
      "publication_head_claim": false
    },
    {
      "command": "publication-only recovery with fixed calculation head 939ae8b and implementation head 65ba55e",
      "result": "PASSED",
      "details": "Executed exactly once. 2,973 paired rows were verified; actual model calls and application-network calls were both zero. Public config/result/report SHA-256 values are 66b2c4f7190bbc1dcf25c04a798a40b79d11af0991a4eb98944843fb902e8147, 49eb02c256de9bdb53be8fa6dc9b2535ae2fed0615869114b2ef1d47eba9dfa9, and 86d41aa459883f8dbdee10c1286a8a317ead12275954873afaea2026c62f0252.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "FAILED",
      "details": "129 tests executed; one pre-existing forward-recovery fixture errored with ACTIVE_COMMIT_MISMATCH in test_transcript_index_and_revision_quarantine_only_after_valid_successor. No OAP source changed.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure is valid; semantic and human authorization proofs remain false.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "The existing 36-report history and two frozen historical incidents remain valid before adding this report.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD",
      "result": "PASSED",
      "details": "Acquisition history remains valid with cumulative count 14, current network count 2, and no new source acquisition.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision HEAD; python3 -B oap/bin/check_whitespace.py --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "Both accepted-base checks passed with exactly the three frozen blank-at-EOF diagnostics.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Git object verification exited zero; pre-existing dangling scratch objects were reported and preserved.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "locked application pytest and changed-scope mypy",
      "result": "BLOCKED",
      "details": "The locked uv runner hung before spawning requested pytest/mypy processes; the installed pytest fallback could not complete application subprocess checks. No application source was changed.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent PERSISTENT_NATIVE_PARENT --command-timeout 30",
      "result": "BLOCKED",
      "details": "The bounded native baseline reached its isolated pytest child, which then blocked in filesystem journal I/O until the 180-second outer timeout. No application source was changed.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-h; python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-h",
      "result": "PENDING",
      "details": "Both pre-publication transcript checks correctly reported ACTIVE_INDEX_MISMATCH or ACTIVE_COMMIT_MISMATCH because the immutable 007-h report did not yet exist. Post-publication verification is kept outside this immutable pre-push report.",
      "sha": "65ba55ef3ff84bda4202190e589d45721409287b",
      "publication_head_claim": false
    },
    {
      "command": "gh pr edit 8 --repo ulfe-lmi/llm-slovenian-repair --body ...",
      "result": "PASSED",
      "details": "PR metadata was updated only; PR #8 is OPEN and UNMERGED on the existing branch and contains no private evidence.",
      "sha": "608f73bc97964586945832b3cd331f5865cb3fa6",
      "publication_head_claim": false
    },
    {
      "command": "git push origin oap/007-concept-verification; git ls-remote origin refs/heads/oap/007-concept-verification refs/pull/8/head",
      "result": "PASSED",
      "details": "Implementation/privacy head 65ba55e and corrected public artifact head 608f73b are remotely present and worktree was clean before report composition.",
      "sha": "608f73bc97964586945832b3cd331f5865cb3fa6",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-12T19:19:53+02:00",
  "report_written_at": "2026-09-12T19:20:12+02:00",
  "implementation": "Preserved the pinned three-file correction and completed the source representation/privacy checks. The frozen private recovery value remains byte-identical at runtime while its source and focused assertion construct the temporary marker from non-path pieces. Public projection keeps safe offline request metadata, public recovery prose, and exact single-newline report EOF. The exact interrupted zero-byte status file was removed; native frozen evidence and the unique publication incident bundle were preserved.",
  "documentation": "Published the corrected data-free configuration, compressed machine result, and report generated by the existing publication-only recovery path. No scientific metric, calculation case, aggregation, prior research artifact, order, or production code was changed.",
  "criteria": "The frozen scientific result is preserved and linked by configuration, input-manifest, case-identity, private aggregate, and incident hashes. Spelling all has 2001 entering OOV targets, 571 accepted unique candidates, 557 applied mechanical edits, 346 exact-reference and 210 non-reference applied edits, mechanical precision 0.6223021582733813 over 556, and spelling-gold recall 0.22838283828382838 over 1515. The projected fallback used 1598 calls versus 2210 baseline calls, avoiding 612 calls, but its end-to-end spelling score was TP/FP/FN 704/345/811, precision 0.6711153479504289, recall 0.4646864686468647, and F0.5 0.6163544037821747. Removing the 75 frozen initial-u/v cases lowers mechanical precision to 0.5971943887775552 and spelling-gold recall to 0.20694444444444443; the initial-u/v view is 0.8421052631578947 precision and 0.64 recall. Preservation changed cases/edits are 197/234, with zero protected or outside-span differences. Actual experiment calls are zero.",
  "negative_paths": "Focused tests cover candidate semantics, insertion/deletion/transposition and identity rejection, normalization/whitespace/hyphen/apostrophe rejection, English suppression ordering, initial-case restoration, exact-unigram and mechanical rechecks, skipped saved calls, frozen fallback and failure rollback, persistence/resume, protected/outside-span integrity, and offline model/network boundaries. The staged guard rejects private markers and the full private-input overlap false positive remains explicitly classified.",
  "boundary_fidelity": "Only the three corrective source/test files changed for implementation, followed by the three named public artifacts and this report. No Qwen weights, GPU, service, gateway, model call, application network, new experiment, calculation, aggregation, dataset, private response, neighboring repository, merge, release, or deployment boundary was crossed.",
  "setup": "Reconciled the consumed SAME-ID 007-h order, active pointer, existing branch, remote branch, and open PR #8 before mutation. Reused native private evidence and the preserved publication incident. Used the exact cached Ruff 0.16.4 binary, owned private evidence boundaries, and a single publication-only recovery. The external PR update changed only PR metadata.",
  "privacy": "No raw DASSLE rows, targets, replacements, prompts, responses, credentials, private paths, or private aggregate contents entered Git, PR metadata, or this report. Public JSON contains only safe offline request metadata and aggregate/hash evidence. Public artifact bytes contain no absolute/private path marker. The full private-input overlap false positive and scratch-fixture symlink refusal are recorded as guard observations, not suppressed.",
  "limits": "The result is PARTIAL. Ruff retains 17 inherited E501 findings in unchanged historical test lines; OAP tests have one pre-existing forward-recovery fixture error; locked application pytest/mypy and native baseline were blocked by uv/filesystem environment behavior. No product correctness, linguistic benefit, release, deployment, merge readiness, or production-readiness claim follows.",
  "human_gates": "D0 / NONE. CRITICAL remains empty. Coding did not append adjudication, accept a scientific result, merge PR #8, enable auto-merge, change branch protection, release, deploy, or authorize live model/service use.",
  "scope": "Finished only the exact 007-h schema/privacy patch continuation. The public artifacts were rendered once from preserved scientific evidence, pushed on the same branch and PR, and this report is the sole remaining report-only change. The literal implementation/artifact head is 608f73bc97964586945832b3cd331f5865cb3fa6; the final SELF commit must have it as sole parent and change only this report path.",
  "result_summary": "PARTIAL for the ordered round: the pinned source/privacy correction is complete, the one publication-only recovery succeeded with zero model/network calls, public artifacts are remotely present, and scientific metrics are unchanged. Static/application environment debt and one inherited OAP fixture error remain honestly classified; PR #8 stays open and unmerged."
}
```

## Result

The 007-h publication-schema/privacy continuation is PARTIAL. The corrected
public artifacts are published from preserved frozen evidence, with safe
request metadata, safe recovery prose, exact report EOF, no public path marker,
and zero actual model or application-network calls. Scientific metrics and the
private aggregate remain unchanged.

## Scientific interpretation

For spelling, 571 of 2,001 entering OOV targets were uniquely resolvable before
fallback, 557 survived document-level application, and 346 were exact-reference
mechanical edits. Mechanical precision was 0.6223021582733813 over 556 defined
edits and spelling-gold recall was 0.22838283828382838 over 1,515 gold edits.
The projected fallback used 1,598 calls versus 2,210 baseline calls, avoiding
612 calls, but its end-to-end spelling score was TP/FP/FN 704/345/811,
precision 0.6711153479504289, recall 0.4646864686468647, and F0.5
0.6163544037821747. Removing the 75 frozen initial-u/v cases lowers mechanical
precision to 0.5971943887775552 and spelling-gold recall to 0.20694444444444443;
the initial-u/v view alone is 0.8421052631578947 precision and 0.64 recall.
Preservation changed 197 cases and 234 edits, all non-reference by that view;
this is not a semantic-harm label. Protected and outside-span differences are
zero. The result is limited to this frozen DASSLE experiment.

## Evidence and limitations

Focused and complete research tests, frozen baseline replay, publication
schema/privacy checks, public guard, bounded overlap scans, governance,
report-history, acquisition-history, accepted-base whitespace, staged-byte
checks, GitHub head verification, and the single publication-only recovery are
recorded above. Inherited Ruff findings, one OAP fixture error, and blocked
application environment checks remain separate and are not represented as green.

## Deferred human adjudication

- Decision: NONE

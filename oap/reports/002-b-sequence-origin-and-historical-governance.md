# Work report 002-b — Sequence origin and historical governance

```oap-report
{
  "id": "002-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/002-b-sequence-origin-and-historical-governance.md",
  "order_sha256": "3c23fa8fee75ccccf3fa56ad6d4c8cd1a938b27a34290549c808947f660ac044",
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
  "implementation_head": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 3,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/3",
  "pr_state": "open",
  "branch": "oap/002-cpu-only-ci-and-governance-guards",
  "base_sha": "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
  "starting_remote_sha": "3d096a798664884b3f89ab7425cdcbe2c290f22e",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest discover -s oap/tests -p 'test_transcript_guard.py' -v",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 002-b",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 002-b",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 2832fa1e51bdf3641aabbd81feab8ddb64a876da...HEAD",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "accepted-base protected-source diff",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at implementation head",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at implementation head",
      "result": "PASSED",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at final report head",
      "result": "PENDING",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at final report head",
      "result": "PENDING",
      "sha": "b026ad831c3572e6d3033c3d4505fdd9bc9e3a07",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T03:22:04+00:00",
  "report_written_at": "2026-09-08T03:23:10+00:00",
  "implementation": "Corrected _transcript_order to require objective 000, contiguous objectives from 0, and zero-based suffix prefixes beginning at a while preserving SUFFIX_ORDER through aa and ba. Restored validate_order to use each order's governance_ref or base_sha and removed the caller-selected current-revision override from transcript validation. The actual implementation head is b026ad831c3572e6d3033c3d4505fdd9bc9e3a07.",
  "documentation": "No product or protocol wording required correction. Updated only the exact generated and installation inventory rows for the changed core and focused transcript test files; order and active pointer were published as scoped protocol state.",
  "criteria": "All 002-b requirements are covered: direct probes reject 001-a, 000-z/000-aa, and 000-a/000-c; complete prefixes through aa and ba pass in protocol order; a real disposable Git regression changes the later manifest while validating 000-a against its original base; existing index, committed-pointer, report/SELF, unfinished, malformed/DHA, and CI guard integrations remain enforced. The exact staged active blob is 002-b\\n.",
  "negative_paths": "The focused suite has 20 passing tests and the complete OAP suite has 81 passing tests. It covers missing objective/suffix origins, numeric and suffix gaps, historical-manifest drift, pointer/index/HEAD mismatches, expected-ID mismatch, missing active/order/report states, latest and noncurrent unfinished states, malformed or draft orders, missing DHA, extra report paths, and wrong report parents. Prior 002-a evidence remains prior-scope evidence and was not rewritten.",
  "boundary_fidelity": "Only oap/bin/oap_core.py, oap/tests/test_transcript_guard.py, their exact generated inventory rows, oap/orders/002-b-sequence-origin-and-historical-governance.md, and oap/active changed before this report. Accepted PLAN, architecture, CRITICAL, role-law, source-lock, governance, bootstrap-source, workflow, and strategic private bytes remain unchanged. No product/live-Qwen/corpus/GPU/service/gateway/credential/GitHub-setting/merge/release/deployment action occurred.",
  "setup": "The standard-library focused and full suites passed. The native development baseline passed locked sync, frozen dependency checks, pytest, Ruff, mypy, packaging, offline venv installation, offline runtime-only sync, import/metadata checks, and cleanup in owned temporary paths.",
  "privacy": "No customer or model text, prompts, replacements, raw responses, credentials, or private strategic contents were placed in source, logs, CI, or this report. Fixtures use synthetic data and fake boundaries.",
  "limits": "This is protocol/orchestration evidence only. Product correctness, linguistic benefit, live-Qwen compatibility, ICA, deployment authorization, remote CI after report publication, and final report-head checks are not claimed. The configured consumed-order marker leaves the read-only durable-state observation at RECOVERY_REQUIRED until report publication; it was reconciled by resuming the same 002-b branch/PR and was not modified.",
  "human_gates": "D0 with deferred human adjudication NONE. PR #3 is open, non-draft, and unmerged at the implementation head; no auto-merge, merge, release, or deployment was performed. Remote final-head verification and required CI observations remain after publication.",
  "scope": "Completed only the activated 002-b sequence-origin and historical-governance correction on oap/002-cpu-only-ci-and-governance-guards, amending PR #3 from accepted base 2832fa1e51bdf3641aabbd81feab8ddb64a876da. No later order, objective, or private strategic state was selected or changed."
}
```

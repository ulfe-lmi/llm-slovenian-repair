# Work report 002-a — CPU-only CI and governance guards

```oap-report
{
  "id": "002-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/002-a-cpu-only-ci-and-governance-guards.md",
  "order_sha256": "feffdc2fc716de759f7bf125366484ba5e147ed8e87e1aa3de3b6e3a9643cf48",
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
  "implementation_head": "af24ae13c9305896d10c4632a138e5da56614bbc",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 3,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/3",
  "pr_state": "open",
  "branch": "oap/002-cpu-only-ci-and-governance-guards",
  "base_sha": "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
  "starting_remote_sha": "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest discover -s oap/tests -p test_transcript_guard.py -v",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 002-a",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 002-a",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 2832fa1e51bdf3641aabbd81feab8ddb64a876da...HEAD",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "accepted-base protected-source diff",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "GitHub OAP bootstrap acceptance at implementation head",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Application baseline at implementation head",
      "result": "PASSED",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    },
    {
      "command": "GitHub required checks at final report head",
      "result": "PENDING",
      "sha": "af24ae13c9305896d10c4632a138e5da56614bbc",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T02:56:35+00:00",
  "report_written_at": "2026-09-08T02:56:53+00:00",
  "implementation": "Added one reusable read-only transcript check with exact index and committed-tree modes, safe revision resolution, protocol suffix/numeric continuity, matching order/report validation, SELF parent and only-path checks, and direct active-pointer byte comparison. The prior 001-b/001-c active-pointer writes were omitted from the historical commits by a same-size Git stat/staging defect, and strategic review missed the stale 001-a blob; those historical snapshots were not fabricated or rewritten.",
  "documentation": "Updated the OAP README and runbook with explicit force-staging, index-byte proof, index-mode validation, committed-mode validation, and report sequencing. Updated generated and installation inventory rows only for changed or added generated OAP files. CI derives the expected latest order ID deterministically.",
  "criteria": "The focused suite has 19 passing tests and the complete OAP suite has 80 passing tests. Real disposable Git histories cover inactive and unfinished rounds, SELF reports, a-to-b, z-to-aa and az-to-ba transitions, pointer mismatches, latest/order gaps, report/order mismatches, noncurrent unfinished work, malformed or draft orders, missing DHA, extra report paths, and wrong report parents.",
  "negative_paths": "The focused guard suite asserts exact failure codes and read-only behavior for worktree-only, index-only and stale committed same-size active writes, expected-ID mismatch, suffix and objective gaps, missing active/order/report states, malformed metadata, draft/DHA failures, and SELF ancestry/path failures. Existing bootstrap negatives for source drift, compact read-set expansion, missing DHA, CRITICAL append/history, and SELF boundaries remain covered by the complete suite.",
  "boundary_fidelity": "Only the ordered OAP helper, test, workflow, documentation, inventory, order, active pointer and final report paths changed. Protected PLAN, architecture, CRITICAL, role-law, source-lock, governance and bootstrap-source bytes remain unchanged against the accepted base. No product repair, model, corpus, service, GPU, credential, GitHub setting, merge, release or deployment action was introduced.",
  "setup": "The standard-library suite passed. The native development baseline passed all locked sync, pytest, Ruff, mypy, build, offline installation and import checks with owned temporary paths; cleanup passed.",
  "privacy": "No customer or model text, prompts, replacements, responses, credentials or private strategic contents were placed in code, logs, CI or this report. Fixtures use synthetic data and fake boundaries.",
  "limits": "The guard is read-only and reports only bounded IDs, modes, statuses and hashes. It does not use Git status, stat cache or mtime as transcript evidence. Product, live-Qwen, linguistic, ICA and release evidence remain separate and were not claimed.",
  "human_gates": "D0 with deferred human adjudication NONE. PR #3 is open and unmerged; no auto-merge, merge, release or deployment was performed. Final report publication and final-head CI observation remain for the publication verification step.",
  "scope": "Completed only 002-a CPU-only CI and governance-guard scope on branch oap/002-cpu-only-ci-and-governance-guards from accepted base 2832fa1e51bdf3641aabbd81feab8ddb64a876da. No later round or objective was selected."
}
```

# Work report 003-b — Evidence and result semantics

```oap-report
{
  "id": "003-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/003-b-evidence-and-result-semantics.md",
  "order_sha256": "5055c58e77ac2d2fe17b066827061f7d959ba809d604bb3f3076258bef08b52a",
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
  "implementation_head": "282a878066258ff73ba2525daf023b9296a8e203",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 4,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/4",
  "pr_state": "open",
  "branch": "oap/003-typed-spans-evidence-reviews-results-and-policy",
  "base_sha": "9f2d71533785e7505bdc1c2539040789d055d7de",
  "starting_remote_sha": "ebe9685a2e8c3e851419ff96b0e129f78d062cf6",
  "no_merge": true,
  "checks": [
    {
      "command": "pytest tests/contract/test_objective_003.py -q",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "pytest tests/contract -q",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "pytest -q",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "ruff check src scripts tests",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "mypy src tests",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 003-b",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 003-b",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 9f2d71533785e7505bdc1c2539040789d055d7de",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 9f2d71533785e7505bdc1c2539040789d055d7de...HEAD",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "accepted-base protected-source diff",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline required CI at implementation head 282a878",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance required CI at implementation head 282a878",
      "result": "PASSED",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at final report head",
      "result": "PENDING",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at final report head",
      "result": "PENDING",
      "sha": "282a878066258ff73ba2525daf023b9296a8e203",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T05:07:03+00:00",
  "report_written_at": "2026-09-08T05:07:27+00:00",
  "implementation": "Corrected EvidenceRecord so query-value state is independent from source/distribution completeness: positive EXACT counts accept PARTIAL or UNKNOWN completeness and optional cutoff metadata, exact zero requires query_complete, complete uncut EXACT is valid, CENSORED remains bounded and non-exact, and UNAVAILABLE carries no query values. Added strict serialized ContextDenominatorState with KNOWN/UNKNOWN invariants and numerator-bound checks. Corrected RepairResult semantics for finite disposition reasons, selected/review/edit identity, original coordinates, proposal correspondence, review-call counts, shadow/degraded behavior, and AUTO_REPAIR-only patched results. Changed enabled review/pass/concurrency capacities to strict positive values while retaining zero automatic retries and immutable v1 safety flags.",
  "documentation": "Exported ContextDenominatorState as the new public contract name and updated the package export inventory test. Existing README.md and STATUS.md statements remain accurate for the corrected typed seam; no unrelated generated inventory or historical source was changed.",
  "criteria": "All 003-b requirements are covered by the implementation and synthetic regressions. The focused 003-b suite passed 27 tests, the contract suite passed 37 tests, full pytest passed 118 tests, scoped Ruff and mypy passed, OAP unittest discovery passed 81 tests, and the native locked/offline baseline passed with cleanup. Both remote required CI checks passed against implementation head 282a878. Transcript index/revision, accepted-runtime governance, protected-source, and diff checks passed at that head.",
  "negative_paths": "Regression coverage rejects positive exactness with unequal bounds, fabricated zero, censored exactness, unavailable values, denominator state/value mismatches and numerator contradictions; impossible reason/disposition pairs; SHADOW edit acceptance; unselected or duplicate review IDs; unmatched coordinates or proposals; reviews with zero calls; calls without usable reviews except degraded optional-review failure; shadow edits; and zero enabled operational capacities. The historical 003-a whole-repository Ruff failure remains preserved as PARTIAL and was not relabelled.",
  "boundary_fidelity": "Only the typed contract, bounded policy, public export, and focused test seams were changed. Validation checks original-coordinate identity and cross-record coherence but does not reconstruct final_text or implement composition. No detector, corpus, tokenizer, review client, acceptance scorer, patcher, pipeline, API, CLI, live model, Qwen, GPU, service, gateway, credential, network-setting, release, deployment, or merge action occurred.",
  "setup": "Verification used the committed uv.lock in owned disposable native temporary environments under /tmp, including fresh dependency sync, wheel build, offline runtime-only sync, fresh offline venv, wheel installation, runtime import, and cleanup. No repository .venv was used or changed and no dependency was added.",
  "privacy": "Source and tests use synthetic Unicode, count, denominator, proposal, result, and policy fixtures only. No customer text, prompts, raw reviewer responses, credentials, secrets, private responses, corpus data, or private strategic contents were logged or committed.",
  "limits": "This is schema and offline engineering evidence only. Linguistic benefit, corpus validity, Qwen/live compatibility, production quality, ICA, milestone acceptance, release, and deployment remain unproven. Final report-head CI checks are intentionally PENDING until this SELF report is published and independently verified.",
  "human_gates": "Decision class D0 with deferred human adjudication NONE. PR #4 is open, non-draft, and unmerged at the verified implementation head; no merge or auto-merge was performed. Human retains review, merge, release, and deployment authority.",
  "scope": "Completed only active order 003-b on oap/003-typed-spans-evidence-reviews-results-and-policy, continuing PR #4 from 003-a report head ebe9685. Published the exact 003-b order and active pointer, corrected the listed contracts/policy, added the listed regressions, and made no change to later objectives, accepted governance, CRITICAL, protected resources, or unrelated work. This report is the only remaining round commit and has implementation head 282a878 as its sole parent."
}
```

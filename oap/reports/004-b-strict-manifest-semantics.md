# Work report 004-b — Strict manifest semantics

```oap-report
{
  "id": "004-b",
  "result": "BLOCKED",
  "order_path": "oap/orders/004-b-strict-manifest-semantics.md",
  "order_sha256": "5a2bbaf881c51775fab3bb2448d5fba49bee496744245a978ef657236e25f2f0",
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
  "implementation_head": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 5,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/5",
  "pr_state": "open",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "starting_remote_sha": "f38f9618c0820eb68b462e43242ea0cd22efe945",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-b",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-b",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code dac4789f52c9e82aec90d1cf92ce9f1194cc103a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "git diff --name-status f38f9618c0820eb68b462e43242ea0cd22efe945...2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "pytest tests/contract/test_objective_004.py -q",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "pytest tests/contract -q",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "pytest -q",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "ruff check src scripts tests",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "mypy src tests",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "NOT RUN",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance required CI at implementation head 2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline required CI at implementation head 2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "result": "PASSED",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at final report head",
      "result": "PENDING",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at final report head",
      "result": "PENDING",
      "sha": "2dddc6ab23fd5e9306afe9f30730c18589d7b5c4",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T08:28:39+02:00",
  "report_written_at": "2026-09-08T08:29:00+02:00",
  "implementation": "BLOCKED before product implementation. The immutable 004-b order was superseded before FIFO consumption by verified human-directed cross-objective remediation: accepted main dac4789f52c9e82aec90d1cf92ce9f1194cc103a was independently confirmed to violate objective-001 root import isolation because objective 003 eagerly imports Pydantic and its regression expectation is reversed despite 003-a requiring preservation. No numbered 004-b product, source-manifest, fixture, or corpus requirement was implemented. The disposition implementation head is 2dddc6ab23fd5e9306afe9f30730c18589d7b5c4, whose sole parent is the starting remote head f38f9618c0820eb68b462e43242ea0cd22efe945.",
  "documentation": "No product source, product tests, fixtures, docs, dependencies, governance, CRITICAL, prior orders or prior reports were changed in this recovery. The exact 004-b order and active pointer were the only paths in the implementation/disposition commit; the 004-a report and all prior history remain preserved.",
  "criteria": "All numbered 004-b product acceptance criteria are BLOCKED and were not assessed. Focused and broader product checks were NOT RUN because product mutation was prohibited. The exact transcript index and committed checks, accepted-runtime governance check, whitespace check, protected-source diff, and implementation-head required CI observations are recorded separately.",
  "negative_paths": "No 004-b product negative probes were run, so no 004-b rejection, schema, metadata, checksum, censoring, exception, or public-alias behavior is claimed. The only source-level evidence used for disposition is the independently confirmed accepted-main objective-001 import-isolation contradiction described above.",
  "boundary_fidelity": "The f38f9618c0820eb68b462e43242ea0cd22efe945...2dddc6ab23fd5e9306afe9f30730c18589d7b5c4 implementation diff contains exactly oap/active and oap/orders/004-b-strict-manifest-semantics.md. The active blob is exact ASCII 004-b followed by one LF. PR #5 remains open, unmerged, and on the required branch/base. No merge, new objective, live test, release, deployment, source fix, or FIFO signal occurred before this report publication.",
  "setup": "No repository product setup, dependency installation, environment replacement, external acquisition, model, service, network, or live boundary was used. Existing local environments and unrelated work were preserved.",
  "privacy": "No customer text, prompts, replacements, raw model responses, credentials, secrets, external corpus data, or private strategic contents were logged or committed. The report records only protocol identifiers, hashes, path-level evidence, and the bounded accepted-main contradiction.",
  "limits": "This is protocol disposition evidence only, not 004-b product or language-quality evidence. The two required CI checks passed at the implementation head, but local product checks were NOT RUN and no 004-b behavior can be treated as passed. Final report-head CI checks are PENDING and are not asserted here.",
  "human_gates": "Decision NONE. The human-directed cross-objective remediation superseded consumption of this order but does not authorize the root-import fix, a new objective, merge, live test, release, or deployment. Human review, strategy publication of the next corrective suffix, merge, release, and deployment authority remain separate.",
  "scope": "Recovered only the active 004-b protocol disposition on oap/004-source-manifests-and-miniature-synthetic-corpus, amending PR #5 from starting remote head f38f9618c0820eb68b462e43242ea0cd22efe945. Force-staged the exact published order and exact 004-b active bytes, committed and pushed them as implementation head 2dddc6ab23fd5e9306afe9f30730c18589d7b5c4, recorded BLOCKED, and stopped product work before FIFO consumption. This report is the sole report-only commit and must have the implementation head as its sole parent."
}
```

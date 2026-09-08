# Work report 005-a — Real source inventory and permitted acquisition recipe

```oap-report
{
  "id": "005-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/005-a-real-source-inventory-and-permitted-acquisition-recipe.md",
  "order_sha256": "6e2c89d6f947bfea4a3fba587255113ae31b029aaec06255324300390abc31a0",
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
  "implementation_head": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 6,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/6",
  "pr_state": "open",
  "branch": "oap/005-real-source-inventory-and-permitted-acquisition-recipe",
  "base_sha": "c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4",
  "starting_remote_sha": "c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4",
  "no_merge": true,
  "checks": [
    {
      "command": "python3.12 scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --validate-only",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py -q",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract -q",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest -q",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 ruff check src scripts tests",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 mypy src tests",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 005-a",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 005-a",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4...HEAD",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head (run 34211547383)",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head (run 34211547400)",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification for PR #6",
      "result": "PASSED",
      "sha": "f5928582fab1d3051bc9f726d7ede3d8cc6b85af",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T11:46:42+02:00",
  "report_written_at": "2026-09-08T11:46:42+02:00",
  "implementation": "Added resources/source-inventory-v1.json with exactly three downloadable publisher-labelled artifacts and one Gigafida 2.2 query-only record, plus scripts/verify_source_artifact.py as a standard-library-only offline boundary. The verifier strictly validates UTF-8 JSON, duplicate keys, schema keys, timestamps, HTTPS allowlists, safe names, checksums, rights/readiness contradictions, censored absence, and denominator semantics. It streams exact local size/MD5/SHA-256 and inspects ZIP metadata without extraction, with encrypted, duplicate, unsafe, symlink, non-regular, member, total-size, and compression-ratio rejection. No real artifact body was fetched.",
  "documentation": "Replaced docs/DATA-SOURCES.md with the dated source snapshot, CC BY-SA/Apache distinction, MD5/SHA-256 distinction, query-only provider-agreement boundary, censored/unknown evidence semantics, and a nonautomatic HTTPS staging recipe. README.md and STATUS.md link the inventory and verifier; oap/GENERATED-FILES.json records the required generated-document hashes.",
  "criteria": "Acceptance 1 is satisfied by the four-entry committed inventory and validate-only result. Acceptance 2 is satisfied by a project-authored miniature ZIP exact hash proof and corrupt/unsafe/encrypted/symlink/duplicate/limit failures with no extraction. Acceptance 3 is satisfied by the bounded manual acquisition/check/pin documentation. Acceptance 4 is satisfied by the full product, wheel, and native baseline checks. Acceptance 5 is satisfied at implementation head by local checks and both required remote CI workflows. Real acquisition, importer, linguistic, live-Qwen, release, and deployment evidence are NOT RUN/UNPROVEN by design.",
  "negative_paths": "Focused tests cover duplicate JSON keys, unknown keys, wrong hosts, invalid license/checksum/project-SHA values, boolean/oversize metadata, query readiness, cutoff-to-zero contradiction, symlink paths, size/MD5 mismatch, unsafe ZIP names, duplicate/encrypted/symlink/non-regular members, source-specific limits, non-downloadable IDs, and no extraction. The full 185-test suite, 101 contract tests, and 84 OAP tests passed. The duplicate-member fixture emits one harmless zipfile warning while the bounded failure assertion passes.",
  "boundary_fidelity": "Only objective 005 files, the exact 005-a order and active pointer, generated-document hash metadata, the verifier, focused tests, and direct documentation were changed. Protected product/governance sources, PLAN, architecture, CRITICAL, source lock, dependencies, package exports, Qwen/GPU/services, network settings, GitHub settings, and neighboring repositories were unchanged. Real URLs are inert metadata; the implementation does not download, extract, scrape, query, import, or package external data.",
  "setup": "The invalid ignored repository .venv was preserved unchanged. Verification used Python 3.12, the committed uv.lock, an owned temporary environment at /tmp/llm-slovenian-repair-005-venv, owned temporary archives, and the native locked/offline baseline. Initial durable reconciliation found the wrapper-consumed 005-a marker on main with no branch/PR; the exact mandated branch was created from accepted base, then PR #6 was created and independently observed open at implementation head. No duplicate PR was created. The consumed marker remains the expected pre-publication recovery marker until this report is published and reviewed.",
  "privacy": "Only synthetic archive contents, source metadata, command outcomes, hashes, paths, and protocol identifiers were used. No customer text, prompts, replacements, raw model responses, credentials, secrets, external archive bytes, corpus samples, or private strategic contents were logged or committed.",
  "limits": "The inventory records publisher metadata and transport MD5 values, not project identity or legal permission. Project SHA-256 remains null until a separately authorized controlled fetch. The 2-per-million n-gram cutoff is censored, not exact zero; Gigafida 2.2 bulk/API and redistribution remain UNKNOWN_UNVERIFIED. No claim is made about linguistic benefit, model compatibility, legal advice, milestone, release, or deployment readiness. The final report commit's remote CI is future state and is not claimed here; no later coding mutation or push is authorized after publication.",
  "human_gates": "Decision class D0 with deferred human adjudication NONE. PR #6 is open and unmerged against main; no merge or auto-merge was performed. Strategy retains independent publication review and development-merge authority, while the human retains intent, rights, release, and deployment authority. No CRITICAL append or human disposition was made.",
  "scope": "Executed only active order 005-a: real source inventory, permitted offline acquisition recipe, and local ZIP verification boundary. Non-goals including real acquisition, extraction, importer/index, normalization, query, corpus samples, live tests, release, and deployment were not performed. Non-report work is committed and pushed as f5928582fab1d3051bc9f726d7ede3d8cc6b85af. This report must be the sole final commit with that implementation head as its sole parent; publication verification and the single OK response occur only after the report is pushed and independently verified."
}
```

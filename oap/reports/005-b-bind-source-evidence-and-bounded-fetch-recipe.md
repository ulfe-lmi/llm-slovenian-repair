# Work report 005-b — Bind source evidence and bounded fetch recipe

```oap-report
{
  "id": "005-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/005-b-bind-source-evidence-and-bounded-fetch-recipe.md",
  "order_sha256": "0f7f0484b107cf431f006c6a88c078e941d76fa3f35561a5b39aa66ddc75216b",
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
  "implementation_head": "42d9defdd2ad2adaee867023d73c580fe45c7496",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 6,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/6",
  "pr_state": "open",
  "branch": "oap/005-real-source-inventory-and-permitted-acquisition-recipe",
  "base_sha": "c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4",
  "starting_remote_sha": "33fd75a7c93d82d87f8d5ee997754954251549ee",
  "no_merge": true,
  "checks": [
    {
      "command": "python3.12 scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --validate-only",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py -q",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract -q",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 pytest -q",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 ruff check src scripts tests",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "uv run --frozen --python 3.12 mypy src tests",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 005-b",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 005-b",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4 --strategic-home /home/ubuntu/workspace/codex-supervision/llm-slovenian-repair",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4...HEAD",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 in-memory nine independent canonical mutation probes",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 in-memory DATA-SOURCES.md fetch-recipe marker inspection",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head (run 34214656515)",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head (run 34214656707)",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification for PR #6",
      "result": "PASSED",
      "sha": "42d9defdd2ad2adaee867023d73c580fe45c7496",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T10:27:17Z",
  "report_written_at": "2026-09-08T10:27:17Z",
  "implementation": "Corrected the source inventory snapshot and all entry observations to the exact UTC observation 2026-09-08T09:13:23Z, with issued-date, observation, and snapshot ordering checks. Added canonical schema-version-1 project and per-ID metadata digests so release, paths, ordered publishers, license, artifact identity/checksum/size, evidence semantics, readiness, and downstream bindings cannot silently rebind. Tightened whitespace and checksum validation, preserved the public canonical loader/ID lookup, and moved synthetic ZIP expectations behind a private lower verification seam. Added directory handling and deterministic coverage for member-count, member-size, total-size, and compression-ratio limits while retaining existing ZIP safety and no-extraction checks. No real source byte was acquired.",
  "documentation": "Updated docs/DATA-SOURCES.md with the exact observation instant and an inspectable future-only recipe that resolves URL and exact byte size from the canonical inventory, stages to an owned .part path, uses curl fail/HTTPS redirect/connect/total timeout and selected --max-filesize controls, then runs offline exact-size/MD5/SHA-256 verification before any separately authorized rename. Reconciled the resulting generated-document hashes in oap/GENERATED-FILES.json and oap/INSTALLATION.json. The report preserves 005-a's historical overclaim rather than rewriting it.",
  "criteria": "Acceptance 1 is satisfied by the exact timestamped inventory, canonical binding, nine independent rejection probes, malformed checksum cases, temporal checks, and committed-table digest. Acceptance 2 is satisfied by the exact four-entry inventory and rejection of fixed-ID rebindings. Acceptance 3 is satisfied by real synthetic boundary tests for all four ZIP limits plus directory/non-regular handling, with prior safety/positive paths green. Acceptance 4 is satisfied by the documented selected-size --max-filesize, .part staging, HTTPS-only redirects, timeouts, fail-on-HTTP, and offline verification sequence. Acceptance 5 is satisfied by the post-commit product, OAP, native baseline, transcript, governance, protected-tree, and hosted required-check evidence. No acquisition, query, extraction, importer/index, rights adjudication, linguistic, live-Qwen, release, or deployment evidence is claimed.",
  "negative_paths": "Focused coverage rejects all nine demonstrated mutations: release, item path, artifact path, byte size, MD5, license name, license URI, blank publisher, and future issue date. It also rejects malformed checksum length/case/algorithm, query CC-license/artifact/readiness contradictions, duplicate JSON keys, unsafe paths/names, size/MD5 mismatch, duplicate/encrypted/symlink/directory ZIP members, all four configured ZIP limits, non-downloadable IDs, and extraction. The deliberate duplicate fixture suppresses only its known exact zipfile warning. The focused 005 suite passed 40 tests; the full product suite passed 205 and OAP passed 84.",
  "boundary_fidelity": "Only the active 005-b order, active pointer, source inventory, offline verifier, focused objective-005 tests, DATA-SOURCES documentation, and required generated metadata changed in the implementation commit. PLAN, architecture, CRITICAL, role law, source lock, dependencies, package exports, 005-a order/report, model/GPU/service/network/gateway settings, GitHub settings, and neighboring repositories were unchanged. The public artifact verifier always loads the canonical inventory; fixture metadata is reachable only through the private lower seam. URLs remain inert metadata and no network action occurred.",
  "setup": "The ignored repository .venv was found invalid and preserved unchanged. An owned temporary Python 3.12 uv environment under /tmp was used with the committed lock; all archive fixtures were synthetic and disposable. The first focused invocation stopped at that invalid environment, and the first full-suite attempt later exposed stale generated documentation hashes; the earliest reached boundary was repaired by updating only the required generated metadata, after which the full suite passed. Durable state reconciliation confirmed the consumed 005-b marker, same branch and PR #6; no duplicate PR or new objective was created. The implementation commit was pushed before this report was composed.",
  "privacy": "Only synthetic archive contents, public source metadata, finite validation reasons, hashes, scoped paths, command outcomes, and protocol identifiers were used. No customer text, prompts, replacements, raw model responses, credentials, secrets, external archive bytes, corpus samples, or private strategic contents were logged or committed.",
  "limits": "The inventory remains publisher metadata: repository MD5 is transport metadata and project SHA-256 remains null until a separately authorized controlled fetch. The Gigafida n-gram cutoff remains censored rather than exact zero, and Gigafida 2.2 bulk/API and redistribution remain UNKNOWN_UNVERIFIED. ZIP checks are metadata-only and no external artifact was downloaded or extracted. No linguistic benefit, model compatibility, legal permission, milestone, release, or deployment readiness is claimed. This pre-publication report records publication_verified=false; report-head CI and remote SELF verification are not yet observable and no later coding mutation is authorized after publication.",
  "human_gates": "Decision class D0 with deferred human adjudication NONE. PR #6 is open and unmerged against main; no merge, auto-merge, release, or deployment was performed. Strategy retains independent publication review and development-merge authority, while the human retains intent, rights, release, and deployment authority. No CRITICAL append or human disposition was made.",
  "scope": "Executed only active order 005-b: bind exact source evidence, enforce canonical inventory identity, correct the bounded future fetch recipe, add the ordered ZIP and negative proofs, and prepare exact protocol publication on the existing PR. Non-goals including real acquisition, HEAD/range/query, extraction, importer/index, package API, external data bytes, live tests, model/GPU/service changes, release, deployment, and merge were not performed. Non-report work is committed and pushed as 42d9defdd2ad2adaee867023d73c580fe45c7496. This report is intended to be the sole final commit with that implementation head as its sole parent; publication verification and the single OK response occur only after the report is pushed and independently verified."
}
```

# Work report 006-g — Commit and run verified unigram smoke

```oap-report
{
  "id": "006-g",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-g-commit-and-run-verified-unigram-smoke.md",
  "order_sha256": "0eebac3d172d7a3162808744194d62b8d9b4eef31dc578ea99fba3952c92ddc6",
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
  "implementation_head": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "c5772a4433f78b1e73a1cd74713714279b9207fc",
  "no_merge": true,
  "checks": [
    {
      "command": "PYTHONPATH=src pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "40 focused objective-005 tests passed.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "51 focused objective-006 importer tests passed.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src pytest tests/contract/test_objective_006_diagnostics.py -q",
      "result": "PASSED",
      "details": "17 focused objective-006 diagnostic tests passed.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src pytest tests/contract/test_objective_006_smoke.py -q",
      "result": "PASSED",
      "details": "14 verifier-first smoke boundary tests passed, including path, member, prefix, aggregate, importer, and content-free error negatives.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src pytest tests/contract -q",
      "result": "FAILED",
      "details": "System invocation reached 199 passing tests but three installed-import isolation checks lacked the package/dependency closure; the authoritative native baseline below passed focused and full pytest in its isolated environment.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -q",
      "result": "PASSED",
      "details": "84 OAP governance and process-boundary tests passed in 198.888 seconds.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "All 13 isolated stages passed: lock/sync, focused/full pytest, Ruff, mypy, OAP, builds, offline runtime installation/import, and cleanup.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-g",
      "result": "PASSED",
      "details": "Indexed active/order transcript is coherent with 006-g as latest and 006-g as the only unfinished round.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-g",
      "result": "PASSED",
      "details": "Committed implementation transcript is coherent before report publication.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure is valid; semantic and human-authorization proof remain false.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "git ls-files --stage oap/active",
      "result": "PASSED",
      "details": "Index mode is 100644 and the exact active bytes are 006-g followed by one LF.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "details": "Implementation history has no whitespace errors.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "PLAN, architecture, CRITICAL, security/testing law, governance, strategic source, and bootstrap source paths are unchanged.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Repository object integrity completed without diagnostics.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head",
      "result": "PASSED",
      "details": "Remote required check passed in run 34262517105 at b7bd642.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head",
      "result": "PASSED",
      "details": "Remote required check passed in run 34262517137 at b7bd642.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 is open and non-draft on b7bd642, based on main, with no merge commit; both required checks pass.",
      "sha": "b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T18:23:15Z",
  "report_written_at": "2026-09-08T18:23:30Z",
  "implementation": "Commit 21e053d9b518ef5826ef560d6fd144c05b69eee5 added the verifier-first one-member bounded prefix helper, optional parser-probe suppression, aggregate gate, real provenance construction, twice-run importer binding, and synthetic contract suite. Commit b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64 corrected the direct-checkout src path bootstrap, the verifier type shadow, and recorded the 006-g receipt. The helper's offline boundary is tested; the one real action passed canonical verification but stopped before member access on the earlier committed helper with HEADER_CONTRACT_UNAVAILABLE, so no real member, structural, importer, or compatibility result is claimed.",
  "documentation": "README.md, STATUS.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md document the reusable verifier-first prefix helper, its 4 MiB/47-line boundary, the configured COMPLETE/COMPLETE/PARTIAL provenance, and the blocked real-smoke outcome. Generated README/STATUS/data-source hash projections were updated. The new receipt preserves canonical verifier facts, cumulative nine GETs, the 006-f harness failure, cleanup, non-retention, and null unobserved smoke fields; earlier orders/reports/receipts remain unchanged.",
  "criteria": "Criterion 1 PASSED for the committed tested offline helper: canonical verifier-first routing, one selected-member open, bounded 14-line/header/32-row envelope, exact aggregate gate, two fresh public importer calls, deterministic bindings, and content-free serialization are covered by 14 synthetic tests. Criterion 2 BLOCKED at the earliest real boundary: exactly one 006-g GET passed canonical verification, then the committed CLI failed to resolve its checkout src path before selected-member access; the source tree was deleted and no retry occurred, so real rows, importer attempts, and hashes are null. Criterion 3 PASSED for the receipt, prior-history preservation, cleanup, non-retention, redistribution false, active mode, source/wheel/governance regression checks, and CI. Criterion 4 BLOCKED overall because the required real smoke did not reach member/import evidence; local and remote implementation-head checks pass and PR #7 remains open and unmerged. This is not a full-source import, lookup-readiness, linguistic-benefit, rights, release, deployment, or milestone claim.",
  "negative_paths": "Synthetic tests exercise verifier stop, symlink and nonregular paths, wrong/missing/duplicate members, incomplete preamble/header/rows, long lines, 4 MiB envelope overflow, identity mismatch, structural aggregate mismatch, finite importer failure, two-run equality, hash non-null/equality, no output content, and CLI bounded errors. Existing focused suites preserve prior importer, diagnostic, source inventory, root laziness, and historical receipt negatives. The real action made one GET, no retry, no second member access, no importer call, no source-content output, no per-row hash output, and no external-byte retention.",
  "boundary_fidelity": "Only the active 006-g scope changed: the helper, its diagnostic opt-out support, the verifier type-only correction, objective-006 smoke tests, receipt, direct documentation, generated hash projections, active pointer, and exact order/report paths. The active pointer is committed as 100644 with 006-g\\n. Protected product law, PLAN, full architecture, CRITICAL, dependency lock, source inventory, bootstrap sources, Qwen/GPU/services/gateway, network settings, neighboring repositories, and merge/release/deployment boundaries were unchanged.",
  "setup": "The consumed durable signal was reconciled to 006-g on the existing objective branch and PR #7; no second control wait, new suffix, duplicate PR, or merge was used. The repository .venv was not used or repaired. Native baseline environments and caches were owned temporary /tmp paths and cleanup passed. The single source directory was /tmp/llm-slovenian-repair-006-g-source-epfVuV; its one .part target was used for curl --disable direct HTTPS with no redirect or credentials, connect timeout 10 seconds, total timeout 900 seconds, and max-filesize 115865656. Verifier success preceded the helper stop, the exact directory was removed and verified absent, and no retry was made. The helper source-path correction was tested offline after the artifact was deleted, not applied to the real artifact.",
  "privacy": "The report and receipt contain no source row, header value, raw external text, prompt, model response, customer text, credential, secret, or private strategic content. They retain only public canonical integrity identifiers, finite status labels, bounded counts, hashes, and aggregate fields required by the order.",
  "limits": "The helper enforces a 4 MiB in-memory envelope, 256 KiB capped member lines, exactly 14 preamble/header/32-row logical reads, one selected-member open, and importer limits bounded to the same envelope. The real action observed verifier facts only; member access, structural aggregate, importer attempts, record count, input/output hashes, result equality, and summary equality remain null or zero in the receipt. publication_verified is false because this pre-push report cannot observe its own future publication.",
  "human_gates": "Decision class D0 with Deferred human adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains review and development-merge authority, while human intent, rights, release, deployment, and milestone authority remain unchanged.",
  "scope": "Executed only active order 006-g on the existing objective-006 branch and PR #7. Non-report implementation head b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64 was pushed and remotely checked before report composition. This publication commit contains only this report and must have that implementation head as its sole parent; after publication verification, no later mutation, merge, retry fetch, release, deployment, or future-CI claim is authorized by this report."
}
```

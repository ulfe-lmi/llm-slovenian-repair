# Work report 006-h — Preflight exact runtime and complete smoke

```oap-report
{
  "id": "006-h",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-h-preflight-exact-runtime-and-complete-smoke.md",
  "order_sha256": "79e76dc549ca1cbe83cd511df4a3969daeff9b1237e40a9960ba73866cd874d7",
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
  "implementation_head": "10ac426441a3f778ffbd7d713640af42f88e54db",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "13706ca116ad1cfe08d237f29b0b48dda50f677b",
  "no_merge": true,
  "checks": [
    {
      "command": "pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "Host exploratory run passed 40 tests; it was not used as the dependency-complete authority.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "pytest tests/contract/test_objective_006.py -q",
      "result": "FAILED",
      "details": "Host exploratory collection failed with ModuleNotFoundError for the package; the order requires an owned dependency-complete interpreter.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "40 focused objective-005 tests passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "51 focused objective-006 importer tests passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest tests/contract/test_objective_006_diagnostics.py -q",
      "result": "PASSED",
      "details": "17 focused diagnostic tests passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest tests/contract/test_objective_006_smoke.py -q",
      "result": "PASSED",
      "details": "19 focused smoke/preflight/receipt tests passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest tests/contract -q",
      "result": "PASSED",
      "details": "208 contract tests passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest -q",
      "result": "FAILED",
      "details": "The literal full invocation was interrupted after 8 tests when the checkout's ignored repository .venv caused a filesystem stall; no files were changed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest oap/tests/test_process_boundaries.py -k test_B10_helper_help_and_real_entry_failures -vv --ignore=.venv",
      "result": "PASSED",
      "details": "The isolated B10 boundary probe passed 1 test after the transient full-run failure.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest -q --ignore=.venv",
      "result": "FAILED",
      "details": "First bounded rerun reached 291 passed and one fixed 5-second B10 helper-help timeout; the targeted B10 rerun then passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m pytest -q --ignore=.venv",
      "result": "PASSED",
      "details": "Second bounded rerun passed 292 tests.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m ruff check src scripts tests",
      "result": "PASSED",
      "details": "All Ruff checks passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -m mypy src tests",
      "result": "PASSED",
      "details": "Mypy reported no issues in 12 source files.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "All 84 OAP governance and process-boundary tests passed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "All 13 isolated stages passed: lock/sync, focused/full pytest, Ruff, mypy, OAP, builds, offline runtime installation/import, and cleanup.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -I -B scripts/smoke_unigram_prefix.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --preflight",
      "result": "PASSED",
      "details": "From an owned non-repository cwd, isolated mode emitted bounded READY output with the exact 834-byte/28-field header, runtime limits, and COMPLETE/COMPLETE/PARTIAL provenance; no artifact was accessed.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "rg -n 'except Exception' scripts/smoke_unigram_prefix.py",
      "result": "PASSED",
      "details": "No broad exception catch remains in the 006-h helper.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "curl --disable --fail --connect-timeout 10 --max-time 900 --max-filesize 115865656 --output OWNED_006_H_PART DIRECT_HTTPS_ARTIFACT_URL",
      "result": "PASSED",
      "details": "Exactly one 006-h direct GET completed to one owned part target; cumulative objective-006 GET count reached ten.",
      "sha": "c75b5b35306e76eccb75e87fec4bc93910b3e10f",
      "publication_head_claim": false
    },
    {
      "command": "OWNED_LOCKED_PYTHON_3_12 -I -B scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --artifact OWNED_006_H_PART",
      "result": "PASSED",
      "details": "Canonical size, MD5, archive SHA-256, member count and total uncompressed size passed before selected-member access.",
      "sha": "c75b5b35306e76eccb75e87fec4bc93910b3e10f",
      "publication_head_claim": false
    },
    {
      "command": "env -u PYTHONPATH OWNED_LOCKED_PYTHON_3_12 -I -B scripts/smoke_unigram_prefix.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --artifact OWNED_006_H_PART",
      "result": "BLOCKED",
      "details": "The committed helper passed member access, exact prefix capture and structural aggregate validation, then the first importer invocation stopped at import-invalid-count; no second run occurred.",
      "sha": "c75b5b35306e76eccb75e87fec4bc93910b3e10f",
      "publication_head_claim": false
    },
    {
      "command": "exact 006-h source environment cwd and run-parent cleanup",
      "result": "PASSED",
      "details": "All four literal owned paths were removed and verified absent without a broad search.",
      "sha": "c75b5b35306e76eccb75e87fec4bc93910b3e10f",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-h",
      "result": "PASSED",
      "details": "The indexed transcript is coherent with 006-h as the only unfinished latest round.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-h",
      "result": "PASSED",
      "details": "The committed implementation transcript is coherent before report publication.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure is valid; semantic and human-authorization proof remain false.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "git ls-files --stage oap/active",
      "result": "PASSED",
      "details": "The active pointer is mode 100644 and contains 006-h followed by one LF.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "details": "Implementation history has no whitespace errors.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "Protected product law, governance, strategic source, and bootstrap source paths are unchanged.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Repository object integrity completed without diagnostics.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head",
      "result": "PASSED",
      "details": "Remote required check completed successfully in run 34268454628 at 10ac426.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head",
      "result": "PASSED",
      "details": "Remote required check completed successfully in run 34268454655 at 10ac426.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 is open and non-draft at 10ac426, based on main, with no merge; both required checks are successful.",
      "sha": "10ac426441a3f778ffbd7d713640af42f88e54db",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T19:59:12Z",
  "report_written_at": "2026-09-08T20:00:30Z",
  "implementation": "Commit c75b5b35306e76eccb75e87fec4bc93910b3e10f added the exact artifact-free preflight, mutually exclusive CLI modes, canonical runtime/header/provenance/limit checks, narrow expected-failure mapping, isolated-process regression coverage, and direct-path bootstrap. Commit 10ac426441a3f778ffbd7d713640af42f88e54db recorded the exact 006-h receipt and corrected current documentation/generated projections. The offline helper and preflight contracts are green. The one ordered 006-h GET passed canonical verification, selected-member access, the 32-row structural aggregate, and the first importer boundary, which then stopped at import-invalid-count; no second importer run, importer hash, or compatibility acceptance is claimed.",
  "documentation": "README.md, STATUS.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md document the preflight/runtime boundary, exact interpreter facts, the bounded smoke outcome, cumulative ten objective-006 GETs, preserved 006-g/system-Python failures, cleanup, non-retention, and the remaining importer limitation. The new receipt preserves canonical identities, aggregate-only facts, null importer outputs, prior history, and redistribution false; historical orders, reports, and receipts remain unchanged.",
  "criteria": "Criterion 1 PASSED for the committed offline/runtime boundary: positive isolated preflight works from a non-repository cwd with PYTHONPATH absent, preflight and artifact forms are mutually exclusive, no broad helper exception catch remains, and negative dependency/argument paths are bounded and content-free. Criterion 2 BLOCKED at the earliest real importer boundary: exactly one 006-h GET reached cumulative ten, canonical verification and the 32-row aggregate passed, then the first importer invocation returned import-invalid-count; the receipt correctly leaves runs, count, equality, and hashes null/zero and no retry occurred. Criterion 3 PASSED for truthful receipt/docs, preserved history, exact cleanup, non-retention, source/wheel laziness, protected governance, and local/remote checks. Criterion 4 BLOCKED overall because the required twice-run real importer evidence did not complete; PR #7 remains open and unmerged. This is not full-source import, linguistic benefit, rights, release, deployment, milestone, or compatibility acceptance.",
  "negative_paths": "Focused tests cover canonical inventory/header/runtime rejection, mutually exclusive modes, isolated no-PYTHONPATH execution, unavailable dependency, bounded CLI errors, verifier ordering, wrong/missing/duplicate/nonregular members, incomplete preamble/header/rows, line/envelope bounds, aggregate mismatch, invalid count, importer determinism/hash/record bindings, and content-free receipt serialization. The real action made one GET, no retry or second GET, no second importer run after the first failure, no raw source-content logging, no per-row hash logging, and no external-byte retention.",
  "boundary_fidelity": "Only active order 006-h scope changed: the preflight/smoke helper, its focused tests, current direct documentation, one 006-h receipt, generated inventory projections, and the active/order/report transcript paths. The active pointer remained mode 100644. PLAN, architecture, CRITICAL, security/testing law, dependency lock, governance, strategic source, bootstrap source, Qwen/GPU/services/gateway, network settings, neighboring repositories, and merge/release/deployment boundaries were unchanged.",
  "setup": "The consumed recovery state was reconciled to the same 006-h branch and existing PR #7; no new suffix, duplicate PR, merge, remote rewrite, or force push was used. During the original round an exploratory uv run without an owned target touched the pre-existing ignored repository .venv and reported one package uninstall; strategy stopped that redundant process, no tracked source changed, it was not repaired, and it supplied no authoritative evidence. All authoritative and recovery checks used owned disposable lock-derived environments outside the repository, and baseline cleanup passed. The exact preflight used Python 3.12.3, isolated mode and no PYTHONPATH from an owned non-repository cwd. The committed receipt proves the literal source/environment cleanup; the one source action stopped at the first importer failure with no retry.",
  "privacy": "The report and receipt contain no source row, header value, raw external text, prompt, model response, customer text, credential, secret, or private strategic content. They retain only public canonical integrity identifiers, finite statuses, aggregate counts, hashes required by the order, and bounded verification facts.",
  "limits": "Preflight and smoke enforce the 4 MiB prefix envelope, 256 KiB line/field bounds, exactly 14 preamble lines plus one 834-byte header and 32 data rows, one selected-member access, two fresh importer calls on success, and finite JSON/error output. The real run reached only one importer attempt; importer record count, input/output hashes, equality, and summary equality remain null or zero. publication_verified is false because this pre-push report cannot observe its own future publication verification.",
  "human_gates": "Decision class D0 with Deferred human adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains review and development-merge authority, while human intent, source rights, release, deployment, milestone, and ICA authority remain unchanged.",
  "scope": "Executed only active order 006-h on the existing objective-006 branch and PR #7. Non-report implementation head 10ac426441a3f778ffbd7d713640af42f88e54db was already pushed and remotely checked before report composition. This final publication commit contains only this report and must have the implementation head as its sole parent. After publication verification, no later mutation, retry fetch, merge, release, deployment, or future-CI claim is authorized by this report."
}
```

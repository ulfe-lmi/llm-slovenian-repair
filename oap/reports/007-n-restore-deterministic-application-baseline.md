# Work report 007-n — Restore the deterministic Application baseline

```oap-report
{
  "id": "007-n",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-n-restore-deterministic-application-baseline.md",
  "order_sha256": "0627cf26015dac47b17085e9f75b857f563379962a9590d5c8534e02e3f64f82",
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
  "implementation_head": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "e20819ace916ed4e619270cc0c72baad9c7a7274",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest concept-verification.tests.test_concept.ConceptTests.test_proxy_stops_at_terminal_event_without_eof (25 consecutive executions at the implementation head)",
      "result": "PASSED",
      "details": "25/25 consecutive runs of the formerly flaky terminal-SSE integration test passed at the implementation head. Before the repair, the same single test failed intermittently at the exact prior head (1 of 6 local single-test iterations failed with the client timeout after 4.082s; CI run 34789634104 failed it at iteration 4). No passing-attempt selection was made; every iteration was recorded.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest concept-verification.tests.test_concept.ConceptTests.test_bounded_read_drains_buffered_terminal_event_on_quiet_socket concept-verification.tests.test_concept.ConceptTests.test_bounded_read_negative_paths_fail_without_success concept-verification.tests.test_concept.ConceptTests.test_proxy_delivers_buffered_terminal_event_without_eof",
      "result": "PASSED",
      "details": "New deterministic regressions at the real response-capture seam. The unit regression builds a real http.client.HTTPResponse (real BufferedReader over a real socketpair): after begin() the raw socket is provably select-quiet while the buffered reader holds the complete terminal event, and _bounded_read returns the exact body promptly. The loopback regression drives the actual ConceptProxy against an upstream that writes status+headers+body in one segment and holds the connection open (no EOF during the exchange), proving status/body delivery before EOF. Negative paths prove malformed JSON, over-bound, EOF-incomplete, and open-connection timed-out streams fail with their exact finite reasons and never succeed; the finite-length body branch behavior is pinned. Both regression tests fail against the un-repaired exact-head proxy (verified by temporarily restoring it).",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s concept-verification/tests",
      "result": "PASSED",
      "details": "19/19 focused concept-verification tests, including the formerly flaky terminal-SSE test, the three new 007-n tests, the pre-existing incomplete-stream 502/path-normalization test, and the non-200 forwarding test.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "40/40 objective-005 ZIP verifier contract tests passed, including every pre-existing negative: unsafe member names, duplicate/encrypted/symlink/directory members, per-source and aggregate size limits, compression ratio, size/checksum mismatch, offline CLI bounds, symlinked inventory, and non-downloadable source rejection.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "mypy src tests/contract",
      "result": "PASSED",
      "details": "Zero errors in 13 source files. All 11 previously observed errors in scripts/verify_source_artifact.py (one loop variable inferred as both stat_result and ZipInfo) are removed by the narrow info -> member rename; no ignores, exclusions, or silenced checks were added.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 scripts/verify_development_baseline.py --temp-parent <owned native temp dir> --command-timeout 900",
      "result": "PASSED",
      "details": "The real baseline driver completed every stage with result PASSED and cleanup PASSED: uv lock --check, frozen dependency sync, focused contract tests, full pytest (607 passed, 2 skipped in the isolated native workspace), Ruff, mypy, OAP unittest discovery, sdist and wheel build, built-wheel selection, fresh offline venv, offline runtime-only frozen sync, offline wheel installation, offline runtime import and metadata. Honest note: an earlier local driver run at the identical tree failed only the oap whitespace subtest (GIT_EXECUTION_FAILED inside the isolated copy - the known transient git-subprocess class); that subtest passed 6/6 directly, and the recorded run is fully green.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests",
      "result": "PASSED",
      "details": "All 222 research tests passed at the implementation head; the corrective round altered no research code, data, or projection.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.rebuild_tables --check",
      "result": "PASSED",
      "details": "The deterministic numeric table matched the registry.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "The public research tree passed the privacy guard on 151 files: no raw text, targets, replacements, prompts, responses, credentials, endpoint values, profile paths, or private root paths.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests",
      "result": "PASSED",
      "details": "129/129 OAP governance/bootstrap tests passed in an isolated native run at this content.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-n",
      "result": "PASSED",
      "details": "active=latest=007-n with the exact order present at HEAD; report history valid (42 reports, exactly the two frozen historical incidents, quarantined 007-d intact).",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "details": "Governance structure valid; semantic and human authorization proofs remain false.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "Report history valid with exactly the two frozen historical incidents.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision HEAD; python3 oap/bin/check_whitespace.py --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "Both accepted-base whitespace checks passed with exactly the three pre-existing frozen blank-at-EOF incidents.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No protected source changed against the application accepted base.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check",
      "result": "PASSED",
      "details": "No whitespace errors in the round diff.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Git object integrity passed; pre-existing dangling scratch objects were preserved.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    },
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/pulls/8 and repos/ulfe-lmi/llm-slovenian-repair/commits/b61f8e2e6b454a0969e5f2ac9009d4da87b8b215/check-runs",
      "result": "PASSED",
      "details": "PR #8 observed OPEN and UNMERGED at head b61f8e2e6b454a0969e5f2ac9009d4da87b8b215 (base ee2d1b479719009ff1d07829478f241e3f395f7c, mergeable clean). All four required final-head checks present and green before report composition: Application baseline success, Research reproducibility success, OAP bootstrap acceptance success, OAP report history success. No merge, release, deployment, or linguistic-success claim.",
      "sha": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-17T03:39:47+02:00",
  "report_written_at": "2026-09-17T03:45:11+02:00",
  "implementation": "Corrective 007-n implementation only. (1) concept-verification/proxy.py _bounded_read now checks readiness on both layers: a non-consuming, non-blocking peek over the real HTTPResponse buffered reader reports bytes already buffered (header parsing may over-read the body, which select on the raw socket cannot see), and a gated non-blocking read1 consumes them; select on the raw socket then gates only the wire, and a readable-but-empty read is treated as a genuine EOF. The absolute deadline, byte bound, explicit SSE-completion requirement, incomplete-stream failure, malformed-event failure, and the finite-length branch are preserved; socket timeout mode is saved and restored. (2) scripts/verify_source_artifact.py: the ZIP member loop variable was renamed info -> member so filesystem stat_result metadata and ZipInfo member metadata live under distinct, correctly typed names; every rejection check (descriptor/no-follow, regular file, hashing, member name, duplicate, symlink, nonregular, encryption, size, total size, compression ratio) is unchanged. (3) Three focused tests added at the real seams. D0 engineering note: the first candidate (drain-first) exposed that HTTPResponse.read1 closes the connection on an empty non-blocking read, which failed ~50% of multi-write trials with EBADF; the shipped form gates every read1 behind the non-consuming probe or select readiness, and 80/80 direct forward() trials plus 25/25 integration runs were clean.",
  "documentation": "Only the _bounded_read docstring changed, recording the two-layer readiness contract. No 007-m scientific report, result, dataset, or projection was altered. This report closes a development CI/capture reliability gate only; it is not a product, linguistic, milestone, or release claim.",
  "criteria": "Acceptance 1: the formerly flaky terminal-SSE integration path passed 25 consecutive runs at the implementation head, and the deterministic regressions prove buffered terminal data is consumed without EOF while invalid/incomplete/oversized/timed-out streams still fail. Acceptance 2: all 11 verify_source_artifact.py mypy errors were removed through the narrow type-correct rename with all 40 ZIP security/integrity tests unchanged. Acceptance 3: the actual development-baseline driver passed every stage; research (222), table, privacy guard (151 files), OAP (129), transcript, governance, report-history, whitespace (both accepted bases), protected-source, and Git integrity checks passed; all four required GitHub checks are green at the pushed implementation head. Acceptance 4: this report-only commit carries the literal implementation head as its sole parent and changes only the report path; PR #8 remains open and unmerged with no unrelated or protected-boundary change.",
  "negative_paths": "The deterministic regression exercises the buffering/readiness boundary under claim: a real http.client.HTTPResponse over a real socketpair whose body was over-read into the real BufferedReader during header parsing while the raw socket is provably select-quiet - a fake that removes HTTPResponse buffering cannot produce this state. The loopback regression exercises the actual ConceptProxy request path with the upstream holding the connection open (no EOF available during the exchange). ZIP tests exercise _verify_artifact_entry and its real file-descriptor/archive-parser boundary on synthetic archives. Against the un-repaired exact-head proxy, both new regression tests fail (verified by temporarily restoring it). No sleep or timeout was lengthened, no retry added, no test marked flaky, no assertion weakened, no file excluded from mypy, no ignore added, and the required baseline was not skipped.",
  "boundary_fidelity": "Only concept-verification/proxy.py, concept-verification/tests/test_concept.py, scripts/verify_source_artifact.py, and the exact 007-n order/active paths changed; no earlier order or report was mutated. The 007-m research implementation, data-free public projections, aggregate claims, private evidence, and no-resample state are byte-for-byte unchanged (publication guard 151 files; no research file in the round diff). No model or network request was made by this round except normal GitHub publication. Protected Qwen weights/quantization, vLLM/CUDA, launch flags, shared GPU, services, ports, network/VPN/firewall, gateway, neighboring repositories, and agent profiles were untouched. No merge, auto-merge, release, or deployment; PR #8 remains OPEN and UNMERGED.",
  "setup": "Reconciled exact active 007-n, the immutable order (sha256 0627cf26015dac47b17085e9f75b857f563379962a9590d5c8534e02e3f64f82), branch oap/007-concept-verification, remote main ee2d1b479719009ff1d07829478f241e3f395f7c, PR #8 head e20819ace916ed4e619270cc0c72baad9c7a7274 (local head identical), and the verified 007-m parent report before mutation; the remote head was unchanged and 007-n was unused remotely, so no conflict stopped work. PR #8 was reused (AMEND_EXISTING_PR). scripts/project_env.sh supplied the native cache/temp conventions; sync-filesystem git traversal used the existing conventions with no clean, reset, stash, or rewrite, and owner-abandoned environment residue was left untouched.",
  "privacy": "Only synthetic SSE/JSON fixtures appear in the changed code, tests, and this report. No user text, targets, replacements, prompts, raw responses, endpoints, credentials, profile paths, or private root paths are displayed or persisted. REPAIR_ALLOW_LIVE_TESTS remains NO and no live test was run. Production logging behavior is unchanged.",
  "limits": "All capture bounds are preserved: the absolute deadline, the 8 MB capture bound, the one-pass/no-automatic-retry capture, and the explicit SSE-completion requirement. The repair adds only a non-consuming probe and a non-blocking drain per ready iteration. ZIP limits, inventory bounds, and all finite reason vocabulary are unchanged.",
  "human_gates": "D0 / NONE. CRITICAL has no admitted entries. Closing this development CI/capture reliability gate does not constitute human semantic acceptance, product readiness, deployment authorization, release authority, merge approval, or linguistic benefit certification. PR #8 remains OPEN and UNMERGED for strategic review.",
  "scope": "Finished only the exact active 007-n order: the buffered terminal-SSE capture repair with deterministic regressions, the verify_source_artifact.py typing repair, focused/broader/governance/privacy verification, the four required implementation-head checks, and this immutable report. No next suffix or objective 008 was assigned or started; no merge, release, or deployment was performed.",
  "result_summary": "COMPLETE for the corrective 007-n round. The concept proxy now consumes an already-buffered, fully delimited response.completed event without EOF while the HTTP/1.1 connection stays open (25/25 consecutive stability runs; the same path failed intermittently at the verified prior head and in CI). All 11 latent mypy errors in the ZIP verifier are removed by a behavior-identical rename. The real development-baseline driver passes every stage, the research/OAP/privacy regression evidence passes, and all four required GitHub checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) are green at b61f8e2e6b454a0969e5f2ac9009d4da87b8b215. This closes a development CI/capture reliability gate only."
}
```

## Result

The 007-n corrective round is COMPLETE. Both observed final-head failures are repaired at the
reached boundaries: the concept proxy no longer stalls when the complete terminal SSE event is
already buffered in the HTTP response reader while the raw socket stays quiet (and the HTTP/1.1
connection stays open), and the `verify_source_artifact.py` static typing defect is removed
without touching any ZIP validation behavior. This closes a development CI/capture reliability
gate only; it is not a product, linguistic, milestone, or release claim.

## Reproduction and repair evidence

At the exact prior head, the failure was reproduced and modeled before fixing:

- The formerly flaky test failed 1 of 6 local single-test iterations (client timeout, 4.082s),
  matching CI run 34789634104, which failed the required Application baseline in
  `ConceptTests.test_proxy_stops_at_terminal_event_without_eof`.
- Unit-level model (real `HTTPResponse` over a real socketpair, one segment containing status,
  headers, and body, connection left open): after `begin()` the raw socket is select-quiet, the
  buffered reader holds the entire 119-byte body including the terminal event, and the old
  `_bounded_read` raised `upstream capture timeout` at exactly its 2.00s deadline. This
  distinguishes the race from slow server startup (all bytes sent at t=0.004s), missing terminal
  bytes (present in the buffer), client timeout (the proxy's own deadline is the earliest
  boundary reached), and EOF handling (connection open the whole window; a handler-crash variant
  that forced a FIN made the old code succeed, confirming the buffered-data/quiet-wire
  signature).
- Loopback model (real `ConceptProxy`, single-write upstream, connection held open): the old
  code produced the CI failure mode (client `TimeoutError` after 2.00s); the repaired code
  returns 200 with the exact body in about 0.002s, and the connection never sent EOF.
- An intermediate drain-first repair was rejected after it exposed that `HTTPResponse.read1`
  closes the connection on an empty non-blocking read (Bad file descriptor on ~50% of
  multi-write trials); the shipped form gates every read behind the non-consuming probe or
  select readiness, and 80/80 direct `forward()` trials plus 25/25 integration runs were clean.

## Deferred human adjudication

- Decision: NONE

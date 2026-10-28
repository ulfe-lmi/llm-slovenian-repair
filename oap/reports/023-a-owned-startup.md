# Work report 023-a - Owned partial-startup cleanup for Pandoc and reviewer child starts (objective 023, round a; PR #25 created by this round per CREATE_NEW_PR; branch oap/023-owned-startup retained)

```oap-report
{
  "id": "023-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/023-a-owned-startup.md",
  "order_sha256": "019efedf17bfd51f551b6f2c97bfaa953f55c7e3d63d792bc681cd2b54aeb7a1",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "313d77900f9bbf1c974e76ea3f546083b117eeaac5f5fc2e964e77b3c19b9ccc",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "d10f9a0d673bd84f91a27f4f24b8505bf966e3eb5825bdfbd9404e1385b6681e",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "db624bb41b34d8263bc5745083d86e7db5bb8907816cd8725871e7225eb6ce9d",
    "oap/governance/DISTILLATION-MAP.md": "eeaf84b26e39c1cadd5d375d8d40f21b62bcf607a18472cd426d13656d5d3e62",
    "oap/governance/WORKSPACE-LAYOUT.json": "90f8b69f4054dffb4d93313da54841ccfddafdca511b86604765d51b63631d16",
    "oap/prompts/coding-round.md": "c682b1bbe016429bf4712a4174ae5ca4ec8b78ab36ebbc2c9b3ce625d83d3ffd",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "ba91f90ef1a8692472661900f1f91faacafa1a47954222c0e75e2f9d9752f6ae",
    "oap/strategic-instructions/AGENTS.md": "c08be7ea6f50ff218948e06ca942d40ce370b041f3580035a4f8ae8ef37c8221",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "83c87a5277ca798609422927e47caa2babab2cf555824813cbbe7f4ac2531ea5",
    "oap/strategic-instructions/strategic_model_init_material.md": "ac972d8e5fcd58b263df11d044aafed9fb1017d2173157d829fbc2953a1ba3b6"
  },
  "publication_commit": "SELF",
  "implementation_head": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 25,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/25",
  "pr_state": "open",
  "branch": "oap/023-owned-startup",
  "base_sha": "83d067431c2431819429135719fdc616a7cb4b99",
  "starting_remote_sha": "83d067431c2431819429135719fdc616a7cb4b99",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-10-28T15:22:19+00:00",
  "report_written_at": "2026-10-28T15:35:13+00:00",
  "checks": [
    {
      "command": "R3 reviewer ownership guard restructure (concept-verification/review_transport.py, final byte bdf9e4e64f1bc3a6f6b1064a6e06f1a0a582fb14d0248f791471658fbbf21ef8)",
      "result": "PASSED",
      "details": "run_review_exchange holds ONE ownership guard established before the first os.pipe; no fallible ownership-tracking runs between descriptor creation and cleanup; the four direct pipe descriptor locals (initialized -1) are closed with an fd >= 0 guard on every exit; the pre-allocated two-branch Popen start sits inside the guard, so process-object allocation failure also closes already-allocated descriptors. Root independent proof: 9 actual owner cases with real pipes (KeyboardInterrupt/MemoryError at both-pipes-created and allocation boundaries, exact injected-exception identity, all known FDs closed before return) PASSED (root-first-r3-fd-guard-correction.json). The earlier four-FAILED fd-gap epoch (root-fd-registration-gaps.json) ran on the 2da-era runtime byte 964eb7f4, before this restructure, and remains FAILED in the record; the fresh re-run on the final bdf9e4e6 bytes covers 2 boundaries (first-pipe registration gap, both-pipes-before-start) times 2 faults (KeyboardInterrupt, MemoryError) = 4 cases, 4/4 PASSED (fd-registration-gaps3-coding.json). All epochs preserved distinctly.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "R7 six inherited Pandoc generic-annotation diagnostics, type-only (concept-verification/pandoc_protection.py, final byte d0255c0dbfb4b4bcb75f6806e5da53f6dd8222fc2dcde6cbe280f3189f3371fd)",
      "result": "PASSED",
      "details": "Concrete dict/list types with identity-only typing.cast at the call sites; TYPE_CHECKING-scoped imports; the structural scope checker reports protected_ast_equal true (runtime checks, branches, offsets, data and results preserved). The io.BinaryIO observation was a wrong import name for this mypy/typeshed: BufferedIOBase is the correct class imported from the io module for the file-object annotation here; this is an import-boundary fact (023a-BinaryIO-import-boundary-diagnosis.json), not a typeshed-corruption claim and not an assertion that it is the sole valid typing alternative. The earlier six-error strict baseline remains FAILED in the record; the final pass is on the new stable bytes.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "Versioned new module concept-verification/tests/test_owned_startup.py at final byte 38a41f736576ec117861818e1ad3e6529fef6945d5bdd451c104fba2f0dce8b0",
      "result": "PASSED",
      "details": "23 tests plus 14 subtests, 0 skipped (41.04 s final-byte run; qualified Python 3.12.15 with -B, PYTHONDONTWRITEBYTECODE=1, private 700 TMPDIR, external PYCACHEPREFIX, pytest cache provider disabled, CONCEPT_PANDOC the qualified official static Pandoc 3.7.0.2). Coverage: real protect_with_pandoc and real run_review_exchange under controlled call-through seams at subprocess.Popen._execute_child, os.pipe and _make_pipe_nonblocking - pre-fork never-created (sentinel untouched), post-create held child (SIGSTOP, state T, reaped before return, exit -9), already-ended child, pre-allocation failure, pipe registration gaps and KI/MemoryError with exact injected identity, fixed-label OSError paths, ordinary-failure-then-healthy-subsequent through real caller paths, no-new-FD before cleanup. Preserved epochs: 22d67312 fixture-contract run (1 FAILED, no-child contract), 3x 23+8 at eee8324a, 3x 23+8 at 1bfe7d10, 23+14 at bae5d729.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "R6 complete owned-set supervision: two-child registry, unconditional supervisor reap, observed-None matrix, actual held-script forced-timeout self-proof",
      "result": "PASSED",
      "details": "Every held-child fixture registers BOTH owned children (product child and the script's own sentinel, exact PID plus /proc start identity) BEFORE the controlled fault; the finite owned parent supervisor unconditionally wait/reaps the complete registered set on every outer outcome (natural exit, forced timeout escape, unexpected parent exception), with product-child reap attribution separate from sentinel cleanup (SIGKILL for the stopped product child; the sentinel's own clean exit, never a fabricated status); optional observation metadata never gates cleanup; the versioned matrix covers default observed=None and observed={} on the timeout and parent-exception paths with a metadata-independent registry identity check; the declared forced-timeout self-proof runs the ACTUAL held script (pandoc-stall fixture) and verifies both exact identities reaped. Root evidence preserved distinctly: root-actual-held-fixture-timeout FAILED_OWNED_SENTINEL_SURVIVES_SUPERVISOR_TIMEOUT at 419feab2 (the finding driving this fix), root-two-child-supervisor-correction PASSED at e209 with default observed=None (both children reaped, empty outer cleanup), fresh actor probe at final bytes PASSED_ALL_KNOWN_CHILDREN_CLEANED (023a-held-fixture-sentinel-r2-coding.json). Declared fixture faults are containment proofs, never product evidence; a forced escape is a FAILED outcome, never a pass.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "Actor full12 (all twelve concept test modules, 41 concept Python) at the pre-commit working tree literal to 9755c5a",
      "result": "PASSED",
      "details": "603 passed plus 199 subtests, 0 skipped, 495.82 s pytest (receipt 023a-full12-sentinel-final-coding.json), ALL 41 concept source hashes identical before/after (presnap/postsnap retained). The same 41 tested Python blobs are literal to the final head f06dd9f (zero Python diff from 121531b; scope checker re-mapped). Distinct from the earlier pre-two-branch FAILED-8 epoch (function-spy Popen TypeError, frozen modules) and the 2da 596/189 pass.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "ROOT independent full12 on the final 41 source bytes (d0255c/bdf9e4/38a41) - original run",
      "result": "FAILED",
      "details": "Independent test assertions PASSED (603 tests plus 199 subtests in 476.62 s, pytest exit 0) on the final 41 working-tree source snapshot while HEAD was 2da099b (run started 14:43:25, finished 14:51:23; 9755c5a was committed later and the tested snapshot is literally mapped to 9755c5a and the subsequent doc heads; the row's sha 9755c5a is that later blob-mapping anchor, not the tested Git head), BUT the private outer supervisor returned FAILED_UNEXPECTED_OWNED_DESCENDANTS (receipt test-scratch-023a/independent-full12-stable-38a41f736576/receipt.json; 023a-root-full12-and-broader-result.json, status INDEPENDENT_TEST_ASSERTIONS_PASSED_SUPERVISOR_FAILED_UNKNOWN_DEAD_CHILD). After the run the supervisor found two zombie descendants of the pytest process: one, recognized while live, was the marked Python orphan-descendant (orphan-descendant-marker-013a) produced by the frozen accepted BoundedCaptureTests.test_timeout_kills_descendant_retaining_pipes, separately reported and exactly reaped (wait 9); the other (PID 3493480) lacked provenance at receipt time, remains unattributed, and is NOT retroactively identified here. Root then reproduced the startup dead-sleep class on BOTH the current and the exact 40-file accepted-83d private runtime from that one frozen test (023a-root-startup-timeout-fixture-diagnosis.json: ACCEPTED_BASELINE_SAME_DEAD_SLEEP_FIXTURE_REPRODUCED) - separate hypothesis evidence, not an attribution of the first run. No product correction was warranted from this evidence and none was made.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "ROOT independent supplemental full12 with two narrowly provenance-qualified frozen-fixture markers (case independent-full12-stable-38a41-two-fixtures)",
      "result": "PASSED",
      "details": "603 tests plus 199 subtests, 476.27 s pytest / 477.842 s supervised, session 82373 closed 0; all 41 source bytes stable and literal to 121531b (and literal to f06dd9f by zero Python diff); exactly two independently identified frozen-fixture children observed while live (the marked Python descendant and the sleep-30 child of the actual owned parent script, FAKE_SLEEPER bytes equal to the trusted 83d AST constant), each later dead Z and actually reaped with wait status 9; unexpected 0, remaining 0 (023a-root-final-independent-full12-pass.json; test-scratch-023a/independent-full12-stable-38a41-two-fixtures/receipt.json). This run proves no other live leftovers at the final bytes; the original root full12 supervisor FAILED remains FAILED and is not re-attributed.",
      "sha": "121531b9d45dfb69865abe0063407b53f14ae1e3",
      "publication_head_claim": false
    },
    {
      "command": "Static analysis on the three changed Python files at final bytes (root actual)",
      "result": "PASSED",
      "details": "Root actual ALL3 strict mypy (python_version 3.12, strict, follow_imports silent, no tests override, mypy_path over concept/src/repository) on a byte-identical flat shadow and Ruff --no-cache both PASSED, source stable. The actor's ruff invocations used the repository-local default cache (linked to the one listed-cache endpoint change in the cache row); Ruff --no-cache is the ordered form for all subsequent runs. The changed set retains targeted noqa comments, including B009 on the native _execute_child getattr, E402 on the imports after sys.path setup and N802 on do_POST (plus E402 comments inside the emitted script string); no broad ignores, Any casts or config relaxations are claimed.",
      "sha": "121531b9d45dfb69865abe0063407b53f14ae1e3",
      "publication_head_claim": false
    },
    {
      "command": "Frozen preservation and structural scope at the final head f06dd9f",
      "result": "PASSED",
      "details": "Scope checker PASSED at each post-change point (final: scope-statusfix-final.json): all 38 pre-existing concept Python files byte-identical to accepted base 83d0674, all 11 old test modules frozen, 41 concept Python total with the tested blobs literal to the final head, exact 173 GENERATED-FILES path set with pins matching committed blobs, order sha256 019efedf intact, active 023-a, no unstable paths; changed paths exactly the ordered 12-set. No no-file-read or whole-cache claim is made.",
      "sha": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
      "publication_head_claim": false
    },
    {
      "command": "Prescribed offline bookkeeping tests (root actual, 023a-root-prescribed-broader-checks.json at the 9755c5a working-tree candidate)",
      "result": "FAILED",
      "details": "Offline research unittest discover: Ran 409 tests in 22.728 s, FAILED (failures=1, skipped=53), sole failure the designed pre-publication report-count check 75 != 74 (test_research_state_consistency.py), which clears only at the future canonical report commit; the researched inputs are unchanged through the later doc-only commits to the final head. Frozen strategic-prompt archive: 3 tests OK (0.001 s). Contextual-validator mode isolation: EXACT one case FAILED under child-only umask 077 (a setup artifact - 077 collapses the 0755 expectation) and PASSED under child-only umask 022. Actor epochs preserved distinctly: pytest 354+2+53 (the second failure the same umask-077 mode artifact) and 355+1+53 in 23.42 s (umask 022; the designed count red), plus the actor's collection ERROR on the wrong module (superseded by the archive 3 PASS). No frozen research/test/validator bytes were edited.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "research.tools.rebuild_tables --check and research.tools.publication_guard",
      "result": "PASSED",
      "details": "numeric table: PASS; publication guard: PASS (6520 files), at the final candidate bytes with qualified -B interpreter and private caches.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "Fresh probe copies at final bytes (new private case directories, new labels)",
      "result": "PASSED",
      "details": "Four private probes re-run as fresh copies: held-fixture sentinel r2 (actual versioned write_held_child_script plus module run_supervised_tree with DEFAULT observed=None, declared stalled-cleanup fixture, forced 2 s timeout stays negative, BOTH registered identities gone before outer cleanup, empty outer cleanup) PASSED_ALL_KNOWN_CHILDREN_CLEANED (023a-held-fixture-sentinel-r2-coding.json); fd registration gaps 2 boundaries x 2 faults 4/4 PASSED (fd-registration-gaps3-coding.json); start-ownership 3/3 PASSED_NO_CHILD_AFTER_RETURN (probe-start-ownership-sentinel-r2-coding.json); supervision-escape r2 (adapted to the current module-level run_supervised_tree API, real native own-session Pandoc, exact parent-side communicate fault) PASSED_NO_KNOWN_NATIVE_CHILD (023a-supervision-escape-r2-coding.json). All source-stable on d0255c/bdf9e4/38a41.",
      "sha": "9755c5a8e999f6fc0426a9da37e709000376c318",
      "publication_head_claim": false
    },
    {
      "command": "Shared OAP helper checks at 2da099b, 9755c5a, ccbb7fe, 121531b and f06dd9f (post-commit revision mode)",
      "result": "PASSED",
      "details": "At each head: check_transcript (expected-id 023-a; --index pre-commit, --revision post-commit) exit 0, active 023-a, report_count 75; check_report_history --index --require-manifest exit 0 (canonical 023 report ABSENT pre-publication); check_governance accepted-runtime at accepted ref 3549de2a exit 0 (semantic_proof and human_authorization_proof false as expected for a coding round); check_whitespace PASSED at both authorized historical bases 2832fa1e and 82ea1e6f, only the three tolerated historical 007 incidents; scoped git diff --check clean. A post-ccbb7fe scope-checker invocation had a failed scratch setup (mktemp template resolved to / because S was unset in that one command) and was re-run correctly; the failed setup is labeled, not swept under the clean results.",
      "sha": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
      "publication_head_claim": false
    },
    {
      "command": "Bounded cache containment (47 baseline-listed mixed cache files)",
      "result": "FAILED",
      "details": "Point-in-time endpoint at ccbb7fe (15:01:30Z, root receipt 023a-root-latest-cache-endpoint.json): 46 of 47 listed regular files unchanged; ONE changed - .ruff_cache/0.16.6/7687620196759728377 (content/size/mtime before-after recorded) - consistent with this round's default-cache ruff invocations (ruff writes the repository-local cache unless --no-cache), which the receipt's scope explicitly does not assert as causality. No restoration, reseed or deletion was performed; the earlier root 47-unchanged observation and the original 021 incident FAILED (7 of 47 changed) are preserved, not re-baselined. This is an endpoint comparison only - no global/continuous/unlisted-cache claim.",
      "sha": "ccbb7fe5b7c1d90af0dde90d548611d2c7aef1f6",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape and allowlist on branch oap/023-owned-startup from accepted main 83d0674",
      "result": "PASSED",
      "details": "Five normal commits, no amend/force-push. (1) 2da099b (sole parent 83d0674, the 12 ordered non-report paths; PR #25 created after its push). (2) 9755c5a (sole parent 2da099b, 3 Python paths: R3/R7/R6 corrections and the sentinel/observed-None test additions). (3) ccbb7fe (sole parent 9755c5a, 2 paths, doc-only: STATUS evidence counts/supervision wording plus its manifest pin). (4) 121531b (sole parent ccbb7fe, 5 paths, doc-only: actual reviewer ownership-guard wording in README.md, STATUS.md, concept-verification/README.md and docs/IMPLEMENTATION-ROADMAP.md plus the three existing manifest pins). (5) f06dd9f (sole parent 121531b, 2 paths, doc-only: the STATUS 023 research-epoch clarification - the 2da-epoch 20.474 s run labeled as such and the root-prescribed 409/22.728 s run cited with researched inputs unchanged through the doc commits - plus its existing manifest pin). Tracked tree clean at f06dd9f; the three unrelated untracked roots (corpus/, .research-test-scratch/, .rclone-speed-test/) preserved and unstaged. The whole changed allowlist is the 12 ordered paths; no report, governance, order or unrelated history bytes beyond those.",
      "sha": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
      "publication_head_claim": false
    },
    {
      "command": "PR #25 (created by this round per the order's CREATE_NEW_PR mode) observed at the final implementation head",
      "result": "PASSED",
      "details": "Actual PR #25 (https://github.com/ulfe-lmi/llm-slovenian-repair/pull/25), created after the 2da push as ordered; the order mode CREATE_NEW_PR remains exact while continuing the already-created PR (no second PR or branch). Fresh observation 2026-10-28T15:22:19Z: state OPEN, head f06dd9ffc5e30071d98155c709b0e05b48a0d055, branch oap/023-owned-startup, base main, mergeable true, merged false, no merge or auto-merge requested. The 2da-epoch CI facts (observed 08:33:56Z: Application baseline in_progress run 40657318681, OAP bootstrap in_progress run 40657318728, Research FAILURE for the designed count red) belong to that earlier head only and are not proof for 9755c5a, ccbb7fe, 121531b or f06dd9f.",
      "sha": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
      "publication_head_claim": false
    },
    {
      "command": "Implementation-head CI at f06dd9f",
      "result": "PENDING",
      "details": "Not yet observed at f06dd9f (or at 9755c5a, ccbb7fe or 121531b); no CI state is claimed for those heads and none is borrowed from the 2da epoch. The four checks (Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history) at the final implementation head remain future evidence.",
      "sha": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (post-publication)",
      "result": "PENDING",
      "details": "All four required checks at the future SELF report head remain PENDING; the actual future SELF SHA is unknown and not claimed. This row's sha is the known pre-publication anchor only.",
      "sha": "f06dd9ffc5e30071d98155c709b0e05b48a0d055",
      "publication_head_claim": false
    }
  ],
  "implementation": "review_transport.py: run_review_exchange restructured to one ownership guard starting before the first os.pipe, holding the four direct pipe descriptor locals (initialized -1, closed with an fd >= 0 guard on every exit, set -1 after in-body closes), with the pre-allocated two-branch Popen start inside the guard; the fixed REASON_HTTP_FAILED label and nonordinary exception identity preserved; existing deadline, IPC and trust untouched. pandoc_protection.py: six inherited generic-annotation diagnostics corrected type-only (concrete types, identity-only typing.cast, TYPE_CHECKING imports); runtime checks/branches/offsets/data/results preserved (protected AST equal). test_owned_startup.py (new, 23 tests + 14 subtests): the owned-boundary proofs above plus the finite owned parent supervisor - every held fixture registers the complete owned set (product child + script sentinel, exact PID plus /proc start identity) before the controlled fault, the supervisor unconditionally wait/reaps that set on every outer outcome with product-child reap attribution kept separate from the fixture-sentinel cleanup, optional observation metadata never gates cleanup (versioned observed-None and observed={} matrix on timeout and parent-exception paths), the holding fixture registers the complete set before the parent-side fault fires (no registration/cleanup race), and the declared forced-timeout self-proof on the actual held script verifies both exact identities reaped (SIGKILL for the stopped product child, the sentinel's own clean exit). No new deadline, endpoint, parser, cap or env policy; cleanup may honestly wait for OS reaping with no hard-real-time claim.",
  "documentation": "The four directly affected docs (README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md) plus concept-verification/README.md carry the round statements with the actual mechanism and exact test epochs. The ccbb7fe and 121531b doc-only commits updated the STATUS 023 evidence to the final 23/14 focused and 603/199 full / 41-source counts and corrected the reviewer ownership-guard wording; the f06dd9f doc-only commit clarified the two research epochs (the 2da-epoch 20.474 s run labeled as such, and the root-prescribed 409/22.728 s run at the 9755c5a working-tree candidate with the researched inputs unchanged through the later doc commits) and refreshed only the existing STATUS manifest pin. Pins are surgical (existing entries only, same 173-path set). The provisional packaged-MVP estimate (8-15 focused engineering days excluding external waits) and the explicit unfinished gaps are retained without percentage or milestone labels.",
  "criteria": "A1 SATISFIED (observed): the observed leaks no longer cross the actual owner return/propagation boundary - root 9 actual R3 cases, fresh 4/4 fd-gap and 3/3 start-ownership probes on the final bytes, and the R6 held-child cases (reaped before return, exact exit statuses, no new FD) - with no unrelated resource touched (untouched sentinels; the original root full12 unknown dead child is a frozen-fixture provenance question preserved as FAILED, not attributed to this round's module). A2 SATISFIED (observed): the 38 pre-existing concept Python files and all 11 old test modules are byte-frozen against accepted 83d (scope checker at the final head; full12 source-stable). A3 SATISFIED (observed): the new focused boundary-faithful suite passes 23 tests plus 14 subtests with no required skip under the qualified Pandoc. A4 SATISFIED (observed): strict/Ruff clean on the three changed files (root actual ALL3 strict plus Ruff --no-cache), actor full12 603/199 with 41/41 source stability, ROOT supplemental full12 603/199 with all 41 bytes stable and exactly two provenance-qualified frozen-fixture children reaped (unexpected 0, remaining 0), shared protocol/source/pin checks PASSED at five heads, and truthful docs including the research-epoch clarification; the recorded FAILED epochs stay in the record (the original root full12 outer-supervisor FAILED with the known child identified and the unknown unattributed, the designed research count red, and the one listed Ruff-cache endpoint change). A5 IN PROGRESS: one PR, this private exact report with actual shared preflight and the mandatory semantic pause (this checkpoint); canonical sole-path SELF publication with root exact-byte approval and all four final-head CI checks remain future PENDING.",
  "negative_paths": "All runtime traffic used owned ephemeral loopback listeners, synthetic fixtures, fake keys and tiny test SQLite data; no live MODEL endpoint, protected service, occupied port, GPU/Qwen environment, authentication, credentials or network configuration was changed; no scientific collection, scoring, registry entry, deployment, merge or auto-merge occurred. Preserved failures, never converted: the 2da-epoch 4-FAILED fd-gap probe (earlier runtime byte 964eb7f4); the 419feab2 sentinel-survival FAILED (root); the pre-two-branch FAILED-8 full12 epoch; the six-error strict baseline; the root original full12 FAILED_UNEXPECTED_OWNED_DESCENDANTS (known child the marked Python orphan descendant from the frozen timeout test; PID 3493480 unattributed); the designed research count red 75 vs 74; the umask-077 contextual-validator setup-artifact failure (exact 1 case, 022 control PASS); the actor archive pytest collection ERROR on the wrong module; and the cache endpoint FAILED 46/47 (one listed Ruff cache entry, endpoint-only scope, no restore/reseed). The original 021 cache incident FAILED 7/47 remains preserved. Controlled-fault evidence only: no spontaneous-native-failure, completed linguistic, live-model or deployment claim; not every historical hang's specific cause was established.",
  "boundary_fidelity": "The intake (020-a), main body capture (017-a), header budget (018-a), owned reviewer exchange (019-a), delivery (021-a) and upstream setup (022-a) contracts are preserved: all 38 pre-existing concept Python files and all 11 old test modules byte-frozen against the accepted base (independently verified), the main status/body error semantics, protocol caps, strict framing, fail-closed outcomes and healthy-path behavior unchanged, and no new deadline, endpoint, security posture, concurrency conversion, queue/admission/fairness, post-intake disconnect detection, remote cancellation or packaging/quality change introduced. The change bounds the two child-start paths (Pandoc and reviewer) to owned cleanup before return plus the type-only Pandoc normalization and the new focused module.",
  "setup": "Qualified Python 3.12.15 with -B, PYTHONDONTWRITEBYTECODE=1, private 700 TMPDIR and external PYCACHEPREFIX were used for the final verified tests and the corrected report-edit/preflight invocations; the final executed tests were uniformly qualified. One draft3 preflight launch attempt used an undefined shell variable and exited 127 with no preflight executed; the subsequent actual qualified preflight returned exit 0. These controls do not describe every historical or report-preparation command: root observed at least three private edit commands that omitted -B (023a-implementation-command-discipline-observation.json) and the actor's post-compaction bare python3 metadata readers (023a-postcompaction-command-observation.json); the inherited bytecode environment of those commands is unknown, and no cache mutation is attributed merely from command form - the one listed-cache endpoint change is linked to this round's default-cache ruff invocations as consistency, not proven causality. Ruff --no-cache is the ordered form for all subsequent runs. One post-commit scope-checker invocation failed its scratch setup (unset S resolved the mktemp template to /) and was re-run correctly; the failed setup is labeled. The offline research child used test-process-only umask 022 inside a private 700 TMPDIR for the single mode-sensitive directory-mode fixture (the ordered bounded exception); ordinary private writing uses umask 077, and the research suite's umask-077 run failure is preserved as a setup artifact with the exact 022 control PASS. The root-owned research-final.log mode correction (0644 to 0600, bytes and mtime preserved, 023a-root-research-log-mode-receipt.json) is a bounded single-file correction, not a claim that every private artifact is 0600. Pandoc was explicit and qualified (no PATH discovery or fallback). No repository .venv or cache restoration was performed.",
  "privacy": "This report is content-free: no customer data, credential, raw answer/target/replacement/prompt/response/header text, or private host path appears in it. The permitted private artifacts are qualified by kind: bounded private failure logs, source snapshots and probe receipts in owned scratch may contain synthetic fixture assertions, private paths and exact PIDs, and are metadata-only relative to any customer content; no private artifact is asserted fixture-free without proof. Runtime fixed-label diagnostics remain content-free.",
  "limits": "The actor full12 ran on the pre-commit working tree whose Python bytes are literal to 9755c5a (doc-only commits followed; the 41 tested Python blobs are literal to the final head f06dd9f by zero Python diff). The ROOT independent original full12 test assertions passed 603/199 but its outer supervisor FAILED: the known zombie child was the marked Python orphan descendant from the frozen BoundedCaptureTests.test_timeout_kills_descendant_retaining_pipes, and PID 3493480 remains unattributed; the frozen startup dead-sleep class was separately reproduced on the current and the accepted-83d runtime (hypothesis evidence only). The ROOT supplemental full12 with two provenance-qualified frozen-fixture markers PASSED 603/199 with unexpected 0 and remaining 0, proving no other live leftovers at the final bytes. No claim that all committed source blobs were tested; the precise tested set is the 41 concept Python plus the static file sets. Actual prescribed research unittest discovery: 409 tests, 22.728 s, one designed FAILED count check and 53 skips at the 9755c5a working-tree candidate (the earlier 2da-epoch 20.474 s run preserved as a distinct epoch); later documentation or publication cannot retroactively make it pass. Historical probe epochs, the FAILED-8 full12 epoch, the 2da CI facts and the invocation/setup errors remain separate evidence. Native controlled faults and synthetic fixtures do not establish live Qwen compatibility, linguistic benefit or an ICA. Cleanup may honestly wait for OS reaping; no hard-real-time guarantee. Overall request/wall-clock/CPU/admission/fairness budgets, post-intake disconnect detection, remote cancellation and packaged library/morphology/quality/live/ICA/deployment work remain unfinished. All four checks at the future SELF publication head remain PENDING; no development merge or product milestone or deployment is authorized by this report.",
  "human_gates": "NONE in this round (decision class D0; deferred human adjudication is NONE per the order).",
  "scope": "Exactly the ordered 12-path allowlist across five commits on branch oap/023-owned-startup from accepted main 83d0674 (see the commit-shape row): two runtime Python files, one new test module, the concept README, README.md, STATUS.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json (existing pins only, same 173-path set), oap/active (022-a to 023-a), the exact 023-a order, and research/RESEARCH-STATE.md (counter 74 to 75 only). Commits 9755c5a, ccbb7fe, 121531b and f06dd9f touched only subsets of those paths (3 Python; 2 doc; 5 doc; 2 doc) with no new paths. This report's canonical sole-path SELF commit with implementation head f06dd9f as sole parent is FUTURE PENDING, not already done. No other versioned source, diff or governance scope.",
  "result_summary": "023-a completes owned partial-startup cleanup for the Pandoc and reviewer child starts: one reviewer ownership guard from before the first pipe allocation, pre-allocated parent-owned process objects, exact-identity reap of every owned child before return, fixed ordinary labels, nonordinary control re-raised with original identity, type-only Pandoc normalization, and a 23-test/14-subtest focused module whose finite parent supervisor registers and unconditionally reaps the complete owned set (product child plus fixture sentinel) on every outer outcome, including the default no-observation call form. Verified evidence: root 9-actual-case R3 proof, fresh 4-probe set, actor full12 603/199 with 41/41 source stability, root supplemental full12 603/199 (unexpected 0, remaining 0, two exact frozen-fixture qualifications), strict/Ruff clean (root actual, --no-cache), frozen 38/11 preservation, shared checks at five heads, prescribed archive 3 PASS. Recorded and preserved: the ROOT original full12 outer-supervisor FAILED (known child the marked Python orphan descendant from the frozen timeout test; PID 3493480 unattributed), the designed research count red 75 vs 74, the one listed Ruff-cache endpoint change (46/47, no restore), the umask-077 setup-artifact failure, and the command-discipline deviations. Final implementation head f06dd9ffc5e30071d98155c709b0e05b48a0d055 on PR #25 (OPEN, mergeable); the canonical SELF publication, root exact-byte approval and all four final-head CI checks remain PENDING. No scientific, linguistic, MVP or deployment acceptance is claimed."
}
```

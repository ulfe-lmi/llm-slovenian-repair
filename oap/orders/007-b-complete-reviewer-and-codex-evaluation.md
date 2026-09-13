# Work order 007-b — Complete reviewer and Codex evaluation

Status: FINAL

```oap-metadata
{
  "id": "007-b",
  "title": "Complete reviewer and Codex evaluation",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": ["001", "002", "003", "004", "005"],
  "local_work": "Clean branch and remote PR #8 at verified 007-a PARTIAL report 5efc25b523ae328d03339295037758c59665d67b; external archives/index/local traces retained; OAP checks green and inherited Application baseline red. Preserve all 007-a frozen bytes and history.",
  "prior_review": "007-a implemented useful loader/detector/protection/proxy seams and detector-only evidence, but never called reviewer/acceptance in evaluation, hard-coded pending metrics, used direct HTTP instead of Codex, emitted an empty review sheet, and likely timed out waiting for SSE EOF. Direct committed reviewer probe succeeds on Neumann.",
  "provenance": [
    {"kind": "H", "reference": "Owner anti-cycling rule permits at most one genuine corrective round and requires reviewer/full pipeline, actual Codex workload, populated blinded review artifact, harm/latency metrics and evidence-based decision."},
    {"kind": "E", "reference": "007-a report/code/local traces: detector held-out measured but reviewer/full pipeline constant pending; 2/8 direct-HTTP cases complete; review sheet fields empty; Application baseline inherited red."},
    {"kind": "I", "reference": "Independent semantic review identifies missing execution paths and EOF-based capture defect. Direct committed ResponsesReviewer with exact private qwen-neumann profile returns valid structured keep in 1.876 seconds."},
    {"kind": "C", "reference": "Complete only the missing scientific boundaries without changing frozen experiment inputs or production code; supersede 007-a's false 'human review only' follow-up claim in a new immutable report."},
    {"kind": "A", "reference": "S-EVIDENCE-01/S-DIAGNOSE-01 require actual reviewer/Codex entry points and distinguish implementation failure from external availability. This is the final allowed implementation correction for the spike."}
  ],
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
  "lr": ["LR-001", "LR-002", "LR-003", "LR-004", "LR-005", "LR-006", "LR-007", "LR-008", "LR-009", "LR-010", "LR-011", "LR-012", "LR-013"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "OAP report history", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

007-b is the one and only corrective implementation/evaluation round permitted for the
concept spike. It completes missing core experiment paths on existing PR #8. No 007-c
may be created for another code, prompt, dataset, threshold or evidence iteration.

## Provenance

- H/E: The owner requires actual reviewer/full-pipeline/Codex/harm evidence; 007-a
  measured only detector enrichment and emitted an unusable empty sheet.
- I: A direct probe proves the committed reviewer and endpoint work. The gap is code and
  orchestration, not scientific uncertainty or human-label absence.
- C/A: Correct exactly these boundaries, preserve frozen experimental choices, run once,
  then conclude from whatever evidence results.

## Current verified state

Remote main is `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #8 is open,
non-draft, unmerged at verified 007-a report `5efc25b523ae328d03339295037758c59665d67b`;
implementation `2d793129582e6c660c46660b968b478fa2bbd1b2`. OAP bootstrap/history
checks pass; inherited Application baseline fails at exact accepted verifier mypy. Do
not alter that baseline or claim merge readiness.

Frozen identities must remain exact:

- config `0e1b3ee713e51fd59d53c503ae8bf892f7344230acf0ecdf814bee40fe779909`;
- frozen manifest `07e76dac3bfe213bac7a93f400b139a05bc340c3e0cc357506281047eedc7164`;
- dev `3f3bffabe3bd53fa0b60417002b7f5674988405365189dd0bc6a10e2a7ba9c4f`;
- held-out `fbd90d2f908597a1dd737e417c1d3b030e3ec7e677fe59720833df900ba16fd3`;
- external index `de2bf3f46fa75178ccaaa172d580b1b7d75e960997f5da674b9b0414dba6db05`;
- prompt template `ee1d4fd3139cf22b053d9bf9cd2b05db2fbb236ea2b8051cc1a10d9c5e359b13`.

Actual target/profile remains Qwen 3.8 27B Neumann at
`http://maelstrom1.lmi.link:8001/v1`, private profile
`/home/ubuntu/.codex/qwen-neumann.config.toml`. A direct 007-a-code reviewer probe is
green. Both archive caches remain exact and require zero GET. CRITICAL empty.

## Governance

The explicit human experiment authorization covers bounded real reviewer/Codex calls and
local traces. It does not authorize service mutation, public exposure, production changes,
corpus redistribution, merge, milestone, release or deployment. D0/NONE.

## Goal and dependencies

Run the already-frozen scientific experiment through its actual missing boundaries and
produce reviewable evidence. Accepted 001–005 and preserved 007-a remain dependencies;
objective 006 is not accepted and its code is untouched.

## Scope

Only `concept-verification/**`, exact 007-b active/order/report, and PR #8 metadata.
Repair reviewer/eval/score/review-sheet/collector/proxy behavior and their tests; update
README/REPORT/aggregate result. Use existing external index/caches and one local result
root. No other repository path changes.

## Non-goals

No change to frozen config/prompt/dev/held-out/index, new examples or labels, prompt tuning,
threshold tuning, corpus download/rebuild, production code/tests/scripts/verifier, baseline
config, report incident allowlist, prior report, generic API, concurrency/retry/security/
deployment architecture, another experiment/suffix, Qwen service/weights/ports/VPN, merge,
release, milestone or fabricated human judgment.

## Files and boundaries

May modify the 007-a experimental Python/README/REPORT/summary and concept tests. The
four frozen repository files and all non-concept paths other than new 007-b protocol paths
are inspect-only. Raw Responses/Codex/model text, proposals and human sheet stay in the
ignored local result root. Only aggregate metric/result JSON and controlled fixture-derived
examples may be committed.

## Requirements

1. Preserve all six frozen identities above byte-for-byte. Held-out execution must still
   refuse any mismatch. Use exactly frozen-v1, local-context, threshold 3 and the existing
   32 held-out cases. No post-result tuning or fixture correction.
2. Extend `run_eval.py` (or one equally small helper it directly invokes) so `--phase
   heldout` with explicit reviewer URL/model/profile calls the real `ResponsesReviewer`
   exactly once per selected candidate, maximum four per response, sequentially, no retry.
   It must record bounded target-level evidence/proposal/acceptance/timing in local output.
3. Feed each proposal into the actual `accept` function using original token neighbors and
   protection, collect non-overlapping accepted edits, and call actual `apply_edits` once
   per case. Assert outside-edit and protected-slice invariance. Reviewer failure keeps
   original but is counted by finite reason; it never becomes a correct keep.
4. Compute controlled metrics rather than constants: raw baseline known errors remaining;
   detector candidates/recall/precision; reviewer keep/replace correctness on candidates;
   proposed replacements; accepted edits; exact-gold correct repairs; harmful edits
   (wrong accepted replacement or any accepted control edit); missed known errors;
   end-to-end recovery; protected changes; beneficial/neutral/harmful and harmful fraction/
   1000 eligible words. Use existing `gold` fields; do not invent labels.
5. Preserve ablations separately: raw, detector-only, reviewer-without-application, full
   conservative pipeline, unigram-only and local-context. Reuse already-frozen detector
   selection; do not rerun threshold choice. If context and unigram remain equal, say so.
6. Fix proxy capture to terminate successfully upon a complete, bounded
   `response.completed` SSE event even if HTTP keep-alive does not close. Require the
   complete event delimiter and preserve terminal/unknown/comment blocks. Incomplete,
   malformed, oversized or timed-out streams fail or return the safely complete original;
   do not hang waiting only for EOF.
7. Normalize exactly one upstream Responses path: upstream base ending with `/v1` and base
   without it must both reach one `/v1/responses`, never `/v1/v1/responses`. Forward actual
   upstream non-200 status/body/content type without relabelling it 200; do not expose error
   text in committed output. Keep loopback-only and no retry.
8. Instrument the proxy only when an explicit ignored trace directory is configured. For
   each main assistant message, atomically write local request ID, original/repaired text,
   candidates, corpus summaries, reviewer decision, acceptance/replacement, raw/detector/
   reviewer/proxy timings and protected-difference count. Never write headers/token/reasoning/
   tool arguments. With tracing disabled, write nothing.
9. Replace `collect.py`'s handcrafted HTTP generator with actual `codex exec --profile
   qwen-neumann`, an explicit `CODEX_HOME`, provider-id/base-url override to loopback proxy,
   `--ephemeral`, finite timeout and an owned disposable working directory. Capture Codex
   exit/event types locally without logging authentication. Do not invoke another model.
10. Run exactly eight frozen workload prompts once in the corrected final collection.
    At least one prompt must require a harmless create/read tool loop inside the owned
    disposable directory and verify the expected file/result before cleanup. Text-only,
    code/Markdown, command/path and mixed-language cases remain. Do not count direct HTTP
    requests as Codex cases.
11. Join each Codex completion with its same-request proxy trace. A completed case requires
    Codex exit 0, terminal response, trace pair and valid protocol events. Report blocked
    finite reasons separately. Extract actual original/repaired assistant text from trace;
    do not use empty placeholders or independent generations.
12. Make `review_sheet.py` emit a deterministic randomized left/right pair for every
    completed trace, with both full original/repaired texts, blank pair label
    (`ORIGINAL BETTER|REPAIRED BETTER|EQUIVALENT|BOTH BAD / UNDECIDABLE`) and target rows
    carrying target/evidence/proposal/accepted/replacement plus blank edit label. Keep the
    sheet local/ignored. Block generation if completed rows have empty text or missing join.
13. Compute real workload metrics from actual traces: responses attempted/completed,
    eligible words, candidates/1000, reviewer calls/response, proposals, accepted edits,
    percent changed, protected differences, raw/detector/reviewer/total proxy latency,
    median and p95 total. Human benefit/harm remains pending until labels; automatic
    counts must not be presented as human quality.
14. Replace hard-coded score statuses with computed evidence. Apply the pre-frozen decision
    gate exactly. Without human workload labels, GO may be only `AUTOMATICALLY_PROMISING,
    AWAITING_HUMAN_REVIEW`, never final natural-workload GO. If automatic thresholds fail,
    say NO-GO or INCONCLUSIVE as dictated; do not adjust them.
15. Add focused negative/positive tests for: real evaluator calls and no-reviewer no-op;
    reviewer malformed/error counted; acceptance/harm/miss math; terminal-complete SSE on
    an upstream that stays open; incomplete timeout; `/v1` normalization; non-200 forwarding;
    trace off/on privacy fields; actual Codex command construction/fake executable exit;
    populated sheet and refusal of empty/missing pairs. Ensure temporary server threads
    always shut down and focused suite exits without external interruption.
16. Run one pre-live focused test/Ruff/mypy sequence. Then execute only the corrected frozen
    held-out reviewer/full pipeline, corrected proxy actual Codex workload and scoring once.
    A code failure before meaningful evaluation may be fixed inside this same round; never
    change frozen science inputs. No second final evaluation run after observing metrics.
17. Update README with exact working commands including explicit reviewer profile, Codex
    home/profile/provider, trace dir and timeout. Update REPORT.md with actual metrics,
    representative controlled successes/failures (project-authored only), six old 007-a
    blocked cases superseded/not hidden, latency, limitations, A–J answers, production reuse/
    shortcuts and evidence-based GO/NO-GO/INCONCLUSIVE.
18. If a populated sheet exists with blank human labels, stop after automatic conclusion
    and request that one semantic review. If execution remains insufficient, name exactly
    one remaining discriminating hypothesis/action. No 007-c and no automatic normal roadmap
    resumption from an INCONCLUSIVE result.
19. Revalidate both caches before/after with zero GET, no source rows/path in public output,
    no archive/index/raw trace/sheet/credentials in Git/package. Preserve all prior reports
    and 007-a result bytes; explicitly supersede only its follow-up interpretation.
20. Run focused tests, concept Ruff/mypy, full existing pytest, OAP unittest, native baseline,
    transcript index/revision, report/acquisition history, accepted governance, protected
    diff, source/wheel lazy imports, archive/package/secret scan, diff check, fsck and all
    three exact final-head checks sequentially. Preserve the inherited mypy/Application
    baseline failure and no merge claim; do not weaken or skip it.
21. Push non-report implementation on the same PR, wait final-head checks, then publish one
    immutable `oap/reports/007-b-complete-reviewer-and-codex-evaluation.md` report-only SELF
    commit with literal implementation parent. Verify remote parent/path/bytes/history and
    send exact OK. Coding never merges or chooses follow-on scope.

## Acceptance criteria

1. Frozen controlled held-out evaluation executes actual reviewer, acceptance and exact
   patch paths once and reports all required computed metrics/ablations without constants.
2. Eight actual Codex invocations traverse corrected buffered SSE; each is completed with
   joined trace or has one finite truthful blocker, including a verified safe tool loop.
3. Human sheet contains reviewable same-generation original/repaired text and target detail,
   with all human labels blank; protected differences are exactly zero.
4. Aggregate JSON/REPORT answer A–J and apply the frozen gate; any missing human semantics
   are separated from automatic evidence. No additional experiment/suffix is proposed.
5. Focused/protocol/governance checks are truthful, caches unchanged/zero-GET, no private/
   source artifacts leak, PR #8 remains open/unmerged, inherited baseline red is explicit.

## Verification

```text
python3.12 -m unittest discover -s concept-verification/tests -v
ruff check concept-verification
cd concept-verification && mypy --explicit-package-bases *.py eval/*.py
python3.12 concept-verification/eval/run_eval.py --phase heldout --config concept-verification/eval/config.json --index EXTERNAL_SQLITE --frozen concept-verification/eval/frozen-experiment.json --reviewer-url http://maelstrom1.lmi.link:8001/v1 --reviewer-model qwen3.8-27b --reviewer-profile PRIVATE_PROFILE --results LOCAL_HELDOUT_FINAL
python3.12 concept-verification/eval/collect.py --cases 8 --codex-bin codex --codex-home PRIVATE_CODEX_HOME --profile qwen-neumann --provider-id qwen-LSI-A100 --proxy http://127.0.0.1:18024/v1 --trace-dir LOCAL_TRACE --work-root LOCAL_OWNED_WORK --results LOCAL_WORKLOAD_FINAL
python3.12 concept-verification/eval/review_sheet.py --input LOCAL_WORKLOAD_FINAL --traces LOCAL_TRACE --output LOCAL_REVIEW_SHEET_FINAL
python3.12 concept-verification/eval/score.py --controlled LOCAL_HELDOUT_FINAL/heldout.json --workload LOCAL_WORKLOAD_FINAL --traces LOCAL_TRACE --output concept-verification/eval/results/summary.json
pytest -q --ignore=.venv
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-b
python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-b
python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest
python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD
python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --exit-code 5efc25b523ae328d03339295037758c59665d67b -- src scripts tests uv.lock PLAN.md ARCHITECTURE.md CRITICAL.md oap/REPORT-HISTORY-INCIDENTS.json resources concept-verification/eval/config.json concept-verification/eval/frozen-experiment.json concept-verification/eval/cases/dev.jsonl concept-verification/eval/cases/heldout.jsonl
git diff --check 5efc25b523ae328d03339295037758c59665d67b...HEAD
git fsck --full --no-reflogs
```

Also verify six exact frozen SHA-256 values, cache identities twice/zero GET, direct source/
built-wheel lazy root imports, proxy SSE field/event comparison, tool-loop local evidence,
sheet nonempty/labels blank, metric arithmetic, Git/package/private-artifact/secret scan,
PR metadata and all three final-head checks.

## Local setup and constraints

Use existing external index/caches and one owned local result/work root. Private profile and
Codex home are explicit, read only, and never logged/staged. Proxy binds loopback only. At
most 10 held-out reviewer calls and exactly eight workload Codex main calls, sequential,
finite timeout, no retry. Do not use repository `.venv`, broad search/delete, concurrent
checks or external model/service mutation. Preserve recovery refs/dangling evidence.

## Documentation

Correct 007-a limitations in new current README/REPORT/summary without editing the immutable
007-a OAP report. Include exact reproducible commands and clear experimental/no-production/
no-human-label/no-merge status. No raw private text in committed/OAP documentation.

## Git and report publication

Same PR #8/branch. New commits only; no amend/force/history rewrite. Push implementation,
observe exact-head checks, then sole report-only SELF commit and remote verification. No
merge/auto-merge. This is the final experiment implementation round regardless of outcome.

## Decision classification

D0. Completes the already human-authorized bounded research path with fixed inputs. It does
not alter product meaning, protected systems, rights, public exposure or deployment.

## Deferred human adjudication

- Decision: NONE

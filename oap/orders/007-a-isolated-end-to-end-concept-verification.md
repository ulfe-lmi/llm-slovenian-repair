# Work order 007-a — Isolated end-to-end concept verification

Status: FINAL

```oap-metadata
{
  "id": "007-a",
  "title": "Isolated end-to-end concept verification",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "prior_disposition": "ABANDONED",
  "abandonment_rationale": "Objective 006 and PR #7 are preserved but closed unmerged after exact accepted objective-005 verifier bytes proved incompatible with the current script-inclusive mypy gate. Human priority forbids more clearance-only 006 suffix cycling before concept verification.",
  "dependency_reassessment": "Concept verification depends on accepted 001-005 contracts and verified external source identities, not on production objective-006 importer completion. The closed 006 branch is inherited only to preserve immutable OAP/process/cache evidence; no 006 product result is treated as accepted.",
  "dependencies": ["001", "002", "003", "004", "005"],
  "local_work": "Clean closed PR #7 branch at remotely verified 006-m FAILED report bb8d9a0315081300ffaadc3ad392b169d51c8ad9; preserve its full history, recovery refs and dangling blob. Two verified external archives and private reconnaissance traces exist outside Git. No concept branch or PR exists yet.",
  "prior_review": "006 report immutability/cache correction works, but PR #7 cannot merge because exact verifier restoration makes local and GitHub Application baseline fail mypy. Single reconnaissance verified Codex Responses/SSE, working Neumann Qwen 3.8 27B streaming and non-stream reviewer calls, exact word/ngram schemas and one-download caches.",
  "provenance": [
    {"kind": "H", "reference": "Human-owner priority change explicitly authorizes an isolated concept-verification subtree, real Qwen/Codex use, bounded cached Gigafida inputs, simplified synchronous code, frozen dev/eval, ablations, harm-first metrics and automatic post-evidence disposition."},
    {"kind": "E", "reference": "2026-09-09 bounded reconnaissance: Codex 0.153.4 sends streaming POST /v1/responses; Qwen3.8-27B Neumann completed real Codex and non-stream JSON review probes; verified word/ngram archive hashes and aggregate schemas are fixed."},
    {"kind": "I", "reference": "Core product usefulness and collateral harm remain unmeasured. Completing production importer/architecture first would not answer whether detector plus isolated same-Qwen review improves Slovenian."},
    {"kind": "C", "reference": "006-m strategic review closes PR #7 without merge and remaps generated 007 from production n-gram importer to one research vertical slice while preserving numeric history."},
    {"kind": "A", "reference": "S-DIAGNOSE-01/S-EVIDENCE-01 and the owner anti-cycling rule require one bounded reconnaissance, one implementation round, one frozen evaluation and at most one material correction."}
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

007-a is one deliberately isolated research spike replacing the generated production
n-gram objective at this numeric slot. It creates one new branch/PR after deliberate
objective-006 abandonment. The original roadmap remains history and planning hypothesis.

## Provenance

- H: The owner asks for scientific falsification before more production architecture.
- E: The one reconnaissance pass fixed actual protocol, endpoint, formats, paths and
  available modules; no repeated diagnostic suffix is necessary.
- I/C: Product utility/harm is the earliest unresolved boundary. Test it vertically in a
  disposable subtree while preserving all production and OAP history.
- A: Strictly separate detector suspicion, reviewer proposal and code acceptance; measure
  harm and protected preservation rather than optimizing edit volume.

## Current verified state

Remote main remains `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #7 is closed,
unmerged, branch-preserved at verified 006-m report `bb8d9a0315081300ffaadc3ad392b169d51c8ad9`.
The current checkout inherits that history so the new branch can preserve immutable OAP
evidence. Do not push another commit to the closed objective branch.

The inherited branch has a known required-check failure: exact accepted-main
`scripts/verify_source_artifact.py` produces 11 script-inclusive mypy type-shadow errors.
Do not change that verifier, mypy scope or tests in this experiment. The concept result
may be scientifically COMPLETE while its development merge remains BLOCKED; report both
separately and do not merge.

Actual target for this experiment is the existing Qwen 3.8 27B Neumann Responses endpoint
at `http://maelstrom1.lmi.link:8001/v1`, accessed through the private `qwen-neumann`
Codex profile/credential. Codex 0.153.4 requires streaming `/v1/responses`; direct
non-streaming reviewer Responses calls are verified. The RTX-3090 endpoint is currently
offline and must not be started/reconfigured. Proposed proxy is loopback `127.0.0.1:18024`.

External caches are verified and retained under strategic concept storage:

- words: size 115865656, MD5 `b20a959f9c113aeb6504f0d753d36d10`, SHA-256
  `77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a`;
- word n-grams: size 22327366, MD5 `22e911e80ecfd2cde4458acd74d83b4b`, SHA-256
  `782da9dd7909bfeefde5e7ee973b6031128167eec05868147d9dbfd22dc8cf40`.

No acquisition is needed or permitted in 007-a. CRITICAL is empty. GitHub active ruleset
22590837 blocks deletion/non-fast-forward but does not enforce required checks; do not
change settings. Live experiment permission is bounded by this explicit human order and
is not deployment/release/milestone authority.

## Governance

Human experimental simplifications override production architecture only inside
`concept-verification/`. PLAN/LR meanings remain the hypotheses tested. Preserve
protected content, exact patching, isolated same-Qwen review, evidence-state semantics,
privacy/rights boundaries and all live resource non-mutation. D0/NONE.

## Goal and dependencies

Answer whether corpus suspicion plus a fresh isolated query to the same Qwen materially
improves Slovenian in the real Codex workflow with acceptably low collateral harm and
operationally plausible latency. Accepted 001–005 provide repository/source/span ideas;
unmerged 006 is neither a completion prerequisite nor accepted dependency.

## Scope

One vertical slice under `concept-verification/`: verified one-off SQLite corpus loader;
protected spans; deterministic unigram/context detector; synchronous isolated reviewer;
conservative acceptance/exact patching; buffered Responses-SSE proxy; controlled and real
Codex evaluations; ablations, metrics, blinded sheet and GO/NO-GO/INCONCLUSIVE report.

## Non-goals

No production refactor/API/FastAPI, generic OpenAI server, async/concurrency/queue/worker,
auth/TLS/security framework, retry/rate limit/telemetry/deployment/container/service,
model-provider abstraction, morphology/Sloleks/CLASSLA, hyperparameter search, production
back-port, Qwen/GPU/service/port/VPN/gateway change, source redistribution, archive Git/
package inclusion, human-label fabrication, PR merge, release, milestone or deployment.

## Files and boundaries

Create only `concept-verification/**`, exact 007 active/order/report, and mechanically
necessary current PR metadata. Add a narrow root `.gitignore` change only if subtree-local
ignore cannot contain local results. Do not alter `src/**`, `scripts/**`, existing tests,
PLAN/ARCHITECTURE/CRITICAL/governance, prior orders/reports/receipts, source inventory,
lock, workflows or objective-006 code. External cache/index/results and private provider
credential are never staged.

Start by creating branch `oap/007-concept-verification` from the current preserved
006-m report head while carrying the already-published 007-a order/active bytes. This
explicit inheritance preserves abandoned history but does not accept it. Never push the
closed PR #7 branch. Create one new PR against main and explain inherited 006 status.

## Requirements

1. Create a small obvious subtree labelled in README and module headers:
   `EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE`. Include at least
   `README.md`, `config.py`, `corpus.py`, `protected.py`, `detector.py`, `qwen_client.py`,
   `repair.py`, `proxy.py`, `run_proxy.sh`, `eval/{collect,perturb,run_eval,score,review_sheet}.py`,
   controlled data/config/results paths, and straightforward `tests/`. Duplication is
   intentional; do not refactor production modules.
2. Use only Python 3.12 standard library for the spike unless a literal blocker is
   demonstrated. Single process/thread, synchronous blocking calls, explicit finite
   timeouts, loopback-only HTTPServer. Configuration is arguments/environment/simple JSON;
   credentials are read only in memory from explicit environment or the existing private
   Qwen profile and never printed, copied, committed or returned in errors.
3. `corpus.py prepare` accepts the two explicit external archive paths and output SQLite
   path. Before member access, require exact regular/non-symlink/link-count-one owner,
   size, MD5, SHA-256 and expected member names/header hashes. No discovery or download.
   On any mismatch fail before consuming rows and never delete a cache automatically.
4. Direct-load only the selected short lowercase unigram member and lowercase 2-/3-gram
   entire members. Skip 14 preamble lines, require the fixed header, recognize exactly one
   first marker row with the observed extra empty field, then require fixed widths/CRLF/
   UTF-8 and finite row/field limits. Unigrams sum integer column 4 by lowercase form;
   2-/3-grams use phrase column 0 and integer column 1. Store SQLite mappings for unigram,
   adjacent bigram, trigram and `(left,right)->middle` alternatives plus provenance.
5. Evidence states are exactly `EXACT`, `CENSORED`, `UNAVAILABLE`: present stored counts
   are exact; absent n-grams are censored under the 2-per-million publisher cutoff and
   unknown denominator; missing short-member unigrams are unavailable. Never emit/use
   exact zero or compare different-length phrase raw counts as semantic proof.
6. `protected.py` returns deterministic original-code-point intervals covering fenced and
   inline code, URLs, recognizable paths, shell-command lines, numeric-only spans, obvious
   identifiers, JSON/XML-like payloads, tool/function arguments supplied by the proxy,
   and Markdown syntax whose mutation would corrupt structure. Overprotect on ambiguity.
   Tests require every protected slice byte/code-point-identical after repair.
7. Tokenize only unprotected natural-language words with stable Unicode-aware Python
   rules and preserve original offsets/casing. Protected boundaries break adjacency.
   Detector returns target start/end/text, evidence state/count summaries and transparent
   score. Select deterministically by score then coordinate, maximum four for this run and
   hard maximum eight. Resolve overlap by first deterministic winner; no optimizer.
8. Implement two declared detector modes: unigram-only, and unigram plus left/right
   bigrams, trigram and stronger observed `(left,right)` middle evidence. Missing censored
   rows add only bounded uncertainty, never zero. On dev only, compare at most four
   predeclared threshold settings; record the score formula and selected setting in fixed
   config before held-out evaluation. Detector identifies candidates but never edits.
9. For each selected target call the same Neumann Qwen in one fresh non-streaming
   `/v1/responses` request containing only compact instructions, exact sentence and target;
   no original Codex conversation, tools, images, prior reasoning, candidate alternatives
   or chain-of-thought request. Try at most two materially different prompt variants on
   dev, select one and freeze its exact bytes/hash before held-out. No call retry framework.
10. Parse only assistant `message/output_text`, never reasoning text. Accept JSON with
    exactly boolean `keep`, string-or-null `replacement`, boolean `needs_wider_edit` and
    no extra keys. Reject code-fence prose unless the frozen parser explicitly permits one
    outer JSON fence, duplicates, malformed/oversized/contradictory values, missing text,
    multiple message answers, timeout/HTTP errors and replacement control/markup/newlines.
11. Separate candidate, reviewer proposal and acceptance. Accept only outside protection,
    valid `keep=false`, nonempty changed replacement, `needs_wider_edit=false`, at most four
    words/eight hard cap, exact target boundary, no conflict, exact unigram support for all
    replacement words, and independently stronger compatible local 2-/3-gram evidence
    under the frozen conservative rule. Qwen confidence is absent/ignored. Uncertainty
    keeps original.
12. Apply accepted edits only to original spans, right-to-left or equivalent. Assert every
    code point outside accepted intervals remains unchanged and all protected slices are
    identical. Never normalize, detokenize, format or regenerate a sentence/answer.
13. Proxy implements only `POST /v1/responses` on `127.0.0.1:18024`. Forward request
    headers/body to explicit direct upstream with finite timeout; buffer the complete SSE.
    On upstream/protocol/repair failure return the original complete upstream result if it
    is already safe, otherwise preserve the upstream error. Never mask an incomplete main
    generation as success.
14. Parse buffered SSE by event. Repair only `output_text` content belonging to natural
    assistant `message` items. Update that item's `response.output_text.delta` sequence,
    `output_text.done`, content-part done, output-item done and completed-response mirrored
    text consistently while preserving event order/count, response/item IDs, reasoning,
    tool/function payloads/arguments, usage and all non-text fields. A tool-only/no-safe-
    text response is returned byte-for-byte unchanged. Emit compatible buffered SSE only
    after repair. Measure raw upstream, detector, reviewer-total and proxy-total latency.
15. Tests cover protected preservation, cache identity/schema/lookup sanity on tiny
    project-authored ZIPs, censored/unavailable semantics, detector determinism/overlap/
    max-targets, strict reviewer parsing, malformed rejection, conservative acceptance,
    exact patch invariance, non-text/tool/ID/usage pass-through and one fake-Qwen SSE proxy
    round trip accepted by a minimal client. Do not build adversarial/concurrency/security
    infrastructure.
16. Create deterministic controlled `dev` (at least 16 cases) and held-out (at least 32)
    sets with exact target spans: documented `točniej`, `rjavo-zlati`/`lase`,
    `kitaraš/vokal`, `najslovnijih`, and local construction examples; additional plausible
    typos, inflection/context errors, valid-word wrong-context cases; rare-correct controls;
    mixed Slovenian/English technical prose; Markdown/code/commands/URLs/paths. Do not
    derive everything from trivial misspellings. Record canonical JSONL SHA-256 identities.
17. Run dev tuning only, choose among no more than four detector settings and two prompt
    variants, write `frozen-experiment.json` with config/prompt/dataset/index identities
    and decision thresholds, then make held-out runner refuse any mismatch. Never modify
    held-out examples/labels/corruption spans or tune after reading held-out outcomes.
18. Held-out ablations are: RAW QWEN/no repair, detector-only candidate enrichment,
    reviewer decisions without application, full conservative pipeline, unigram-only and
    local-context detector. Report eligible words, known errors, candidates, recall,
    candidate precision/enrichment, reviewer accuracy, accepted/correct/harmful/missed,
    protected changes and end-to-end recovery. Zero protected corruption is mandatory.
19. Run eight bounded real Codex/Qwen workload responses through the proxy: ordinary
    Slovenian explanation, code-heavy Markdown, commands/paths/technical English, and one
    normal tool-using coding loop confined to an owned disposable directory. Demonstrate
    Codex continues after valid tool calls, buffered text is accepted, and protocol fields
    survive. Store raw traces only under ignored local results; never commit unrelated
    private material or credentials.
20. Produce aggregate real-workload metrics: responses, eligible words, candidates/1000,
    reviewer calls/response, proposals/accepted edits, percent changed, protected diffs,
    raw/detector/reviewer/proxy latency and median/p95 total. Produce deterministic blinded
    original/repaired left-right review sheet with blank labels and target-level evidence/
    review/acceptance fields. Do not fabricate human labels.
21. Harm is primary: controlled beneficial/harmful/neutral counts, harmful changes per
    1000 eligible words and harmful fraction of accepted edits. Real-workload benefit/harm
    remains `AWAITING_HUMAN_REVIEW` until an attributable human fills the sheet. Model
    self-review is not a human quality label.
22. Before held-out run, freeze decision categories: GO/PROMISING requires detector
    enrichment, reviewer precision gain, nontrivial recovery, predominantly beneficial
    accepted edits, rare harm, zero protection corruption, functional Codex and plausible
    finite latency; NO-GO matches the owner conditions; otherwise INCONCLUSIVE. Reference,
    not production gates: beneficial precision about >=80%, harmful accepted <=5%
    (<=1% convincing), recovery >=30%, protected corruption exactly zero.
23. Produce exact commands in README for index preparation, tests, proxy startup, Codex
    override, controlled evaluation, workload collection/scoring and review sheet. Produce
    committed fixed config/dataset hashes and small aggregate machine result JSON. Keep
    derived SQLite/raw traces/human sheet local and ignored. `concept-verification/REPORT.md`
    must contain all owner-requested design, protocol/model/source, ablation, metric, harm,
    latency, success/failure, limitation, reuse/shortcut and decision sections.
24. Explicitly answer strategic questions A–J from evidence. If human labels are absent,
    do not call natural-workload quality GO; state INCONCLUSIVE awaiting that one semantic
    review unless automatic controlled evidence already proves NO-GO. Identify at most one
    next discriminating action. Do not automatically create a suffix for tuning/data/result.
25. Validate both caches before and after index/evaluation with zero network GETs. No raw
    source row in stdout/CI/OAP report, no archive/index/raw trace in Git, wheel or package.
    Do not clean caches at report publication: human review may still need reproduction;
    record exact gated cleanup state.
26. Run concept focused tests, controlled/live commands, full existing pytest, Ruff, mypy,
    OAP unittest, native baseline, transcript index/revision, report/acquisition history,
    governance/protected diff, package/archive scan, `git diff --check`, `git fsck`, and all
    final-head GitHub checks sequentially. Preserve the known inherited mypy/Application
    baseline failure distinctly; no merge-ready claim or test/config weakening.
27. Commit/push non-report work, create the one PR, and observe exact-head checks before
    report. Final report is a sole report-path SELF commit with literal implementation
    parent. Verify remote report/head/history and send exact OK. Coding never merges,
    selects follow-on work, changes the closed PR, or claims human acceptance.

## Acceptance criteria

1. The isolated proxy works with fake SSE and the actual Codex/Qwen Responses loop,
   preserves tool/nontext/protocol fields, and changes only accepted assistant-text spans.
2. One verified external index and frozen controlled evaluation execute all required
   ablations with complete denominators, zero protected corruption and harm-first metrics.
3. Eight real workload cases execute or the exact external availability failure is
   reported once without cycling; the blinded human sheet is usable and labels remain blank.
4. REPORT.md and aggregate JSON give a truthful GO/NO-GO/INCONCLUSIVE result, answer A–J,
   separate automatic from human evidence and identify production reuse/shortcuts.
5. No external data/credential/raw private trace enters Git/package/log; caches remain
   verified/reusable with zero GET; production/OAP/history sources are unchanged except
   exact 007 publication paths. PR remains unmerged and inherited baseline red is explicit.

## Verification

```text
python3.12 -m unittest discover -s concept-verification/tests -v
python3.12 concept-verification/corpus.py prepare --words-archive EXPLICIT --ngrams-archive EXPLICIT --output EXTERNAL_SQLITE
python3.12 concept-verification/eval/run_eval.py --phase dev --config concept-verification/eval/config.json --results LOCAL_DEV
python3.12 concept-verification/eval/run_eval.py --freeze --config concept-verification/eval/config.json --output concept-verification/eval/frozen-experiment.json
python3.12 concept-verification/eval/run_eval.py --phase heldout --frozen concept-verification/eval/frozen-experiment.json --results LOCAL_HELDOUT
python3.12 concept-verification/eval/collect.py --cases 8 --proxy http://127.0.0.1:18024/v1 --results LOCAL_WORKLOAD
python3.12 concept-verification/eval/score.py --controlled LOCAL_HELDOUT --workload LOCAL_WORKLOAD --output concept-verification/eval/results/summary.json
python3.12 concept-verification/eval/review_sheet.py --input LOCAL_WORKLOAD --output LOCAL_REVIEW_SHEET
pytest -q --ignore=.venv
ruff check src scripts tests concept-verification
mypy src scripts tests concept-verification
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-a
python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-a
python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest
python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD
python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --exit-code bb8d9a0315081300ffaadc3ad392b169d51c8ad9 -- src scripts tests uv.lock PLAN.md ARCHITECTURE.md CRITICAL.md oap/REPORT-HISTORY-INCIDENTS.json resources
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git fsck --full --no-reflogs
```

Replace logical external paths only in private commands/receipts, not reports. Also run
cache digest/member revalidation twice, source/wheel lazy-root probes, proxy protocol-field
comparison, protected-slice byte comparison, dataset/config hash check, archive/package/
secret scan, PR metadata and all three final-head check observations.

## Local setup and constraints

Use existing Python 3.12/Codex/Qwen profile and owned external cache/results/temp roots.
Never use/repair repository `.venv`; never expose the proxy beyond loopback; no service
installation. At most eight workload main calls and four reviewer targets/response; finite
HTTP/Codex timeouts; no automatic retry. The existing private profile may supply its bearer
only in memory. Preserve all caches, recovery refs, dangling evidence and unrelated work.

## Documentation

README gives executable local commands and emphatic experimental status. REPORT.md and
aggregate JSON report actual tested identities/results/limits. PR body concisely explains
closed 006 inheritance, experimental scope, current conclusion, human-review status,
checks and no merge/release/deployment. Never reproduce raw corpus/history in OAP report.

## Git and report publication

Create branch `oap/007-concept-verification` and one new PR against main; do not reuse or
reopen PR #7. New commits only, no amend/force/history rewrite. Push final implementation,
observe exact-head checks, then one immutable
`oap/reports/007-a-isolated-end-to-end-concept-verification.md` report-only SELF commit.
Verify remote head/parent/path/history, send exact OK and exit. No merge/auto-merge.

## Decision classification

D0. The human explicitly authorized the isolated live research boundary, simple local
instrumentation, verified corpus caching and evaluation traces. No production/deployment,
public exposure, protected service mutation, redistribution or human acceptance occurs.

## Deferred human adjudication

- Decision: NONE

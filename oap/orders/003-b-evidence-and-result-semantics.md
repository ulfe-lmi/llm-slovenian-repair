# Work order 003-b — Evidence and result semantics

Status: FINAL

```oap-metadata
{
  "id": "003-b",
  "title": "Evidence and result semantics",
  "objective": "003",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "9f2d71533785e7505bdc1c2539040789d055d7de",
  "branch": "oap/003-typed-spans-evidence-reviews-results-and-policy",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 4,
  "dependencies": [
    "001",
    "002"
  ],
  "local_work": "Clean objective branch at remote 003-a report head ebe9685a2e8c3e851419ff96b0e129f78d062cf6; preserve all 003-a and prior transcript commits/reports plus ignored local environments and private strategic files.",
  "prior_review": "003-a remote SELF report verifies and both final-head checks pass, but its truthful PARTIAL result records the overbroad inherited-OAP Ruff command; direct semantic probes prove evidence and result combinations contrary to the accepted contract are rejected or accepted.",
  "provenance": [
    {
      "kind": "A",
      "reference": "PLAN.md §§6.2, 8.4, 9.1–9.3, 13.3 and ARCHITECTURE.md §§6, 8.1, 10.3, 11, 14.1–14.2"
    },
    {
      "kind": "E",
      "reference": "2026-09-08 final-head probes: exact positive PARTIAL/thresholded and COMPLETE/uncut evidence are rejected; three operational maxima accept zero; impossible disposition/reason pairs, a SHADOW applied edit without a selected target, and reviews with review_call_count=0 are accepted. 003-a reports whole-repository Ruff failure outside the established product lint boundary."
    }
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
  "lr": [
    "LR-003",
    "LR-006",
    "LR-008",
    "LR-010"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "Application baseline"
  ],
  "decision_class": "D0"
}
```

## Identity

003-b is the first corrective round on objective-003 branch and PR #4. Preserve
implementation/report commits `5ce260c`/`ebe9685` and all earlier history. Do not
amend history, create another PR or advance the objective number.

## Provenance

- A: EXACT describes knowledge of this query's count within a declared scope; it
  does not claim the source/distribution is globally complete. Missing thresholded
  data is CENSORED, not zero, while a retained positive record may still have an
  exact count. Context denominator knowledge is a separate declared fact.
- A: result metadata must tell one coherent story: shadow never applies an edit,
  review metadata cannot arise from zero calls, edits must originate from CPU-owned
  selected IDs, and main capture failure is not a successful completed-text result.
- E: direct probes against final 003-a code demonstrated the exact false rejections
  and false acceptances listed in metadata. The established native verifier's Ruff
  boundary is `src scripts tests`; OAP has its own unittest/governance checks.

## Current verified state

Accepted default main remains `9f2d71533785e7505bdc1c2539040789d055d7de`.
PR #4 is the sole open PR and is clean at remote 003-a report head
`ebe9685a2e8c3e851419ff96b0e129f78d062cf6`; implementation parent is
`5ce260cd53fef5fb8cd447b3d9c258928ff69749`. The remote SELF report verifies,
committed active is exact `003-a\n`, and both final-head checks pass.

003-a is PARTIAL because literal `ruff check .` failed on pre-existing OAP files;
its focused Ruff, 23 focused contract tests, 33 contract tests, 114 complete product
tests, 81 OAP tests and native locked/offline baseline passed. CRITICAL remains empty.
No live/model/corpus/release/deployment action occurred.

## Governance

Preserve all accepted governance and historical transcript bytes. Apply LR-003,
LR-006, LR-008 and LR-010 exactly. Correcting schema semantics and a mistaken test
scope is D0; no consequential unresolved alternative or DHA entry exists.

Source/distribution completeness, query count status and denominator knowledge are
three different facts. Do not make one silently imply another. All review proposals
remain untrusted; result consistency does not implement acceptance or patching.

## Goal and dependencies

Close objective 003 by correcting the evidence and result contracts at the real
Pydantic boundary, enforcing positive operational capacities, and replacing the
overbroad Ruff proof with the repository-established product/test/script scope.

Dependencies remain the accepted package baseline and transcript guards. Continue
on the same PR; do not absorb objective 004 or later behavior.

## Scope

1. Correct evidence completeness/query/denominator semantics in `contracts.py`.
2. Correct result vocabulary and cross-record invariants in `contracts.py`.
3. Make enabled operational capacities positive in `policy.py` while retaining
   zero automatic retries.
4. Add focused regression tests for every demonstrated bad acceptance/rejection.
5. Update direct exports/docs/inventory only where names or exact bytes change.
6. Publish exact 003-b order/active/report on PR #4.

## Non-goals

No corpus implementation or arithmetic, source manifest, tokenizer/protected spans,
review parser/client, acceptance scoring, patch composition, pipeline/API/CLI, live
test or data acquisition. Do not make result validation reconstruct `final_text`;
that is the later patcher boundary. Do not lint/refactor inherited OAP infrastructure
to make the discarded whole-repository command green.

No dependency/governance/CRITICAL/GitHub-setting/model/GPU/service/network/credential/
release/deployment change. Do not rewrite 003-a or call its truthful failure passed.

## Files and boundaries

Expected mutable product paths are `src/llm_slovenian_repair/contracts.py`,
`src/llm_slovenian_repair/policy.py`, focused `tests/contract/test_objective_003.py`,
and direct `__init__.py`/README/STATUS/inventory rows only if public names or bytes
change. Order/active/report are the protocol paths.

Exercise real Pydantic construction and JSON round trips. Synthetic records are
inputs. The established Ruff boundary is exactly `ruff check src scripts tests`;
OAP behavior is independently covered by its full unittest suite.

## Requirements

1. Evidence state is query-value knowledge. EXACT requires equal nonnegative bounds.
   It must accept a positive retained count with source/distribution completeness
   PARTIAL or UNKNOWN and optional threshold metadata. EXACT zero still requires an
   explicit assertion that this source is complete enough for that query. A complete
   uncut exact source must allow absent/null cutoff metadata; do not require invented
   text such as `none`.
2. Retain explicit source/distribution completeness independently of evidence state.
   CENSORED must retain justified noncontradictory bound/cutoff metadata and may not
   claim query completeness or fabricate an exact value. UNAVAILABLE retains no
   numeric count/bounds/cutoff and makes no availability inference.
3. Add an explicit finite context-denominator knowledge state with exact values
   `KNOWN` and `UNKNOWN` (or an equally clear public name with these serialized
   values). KNOWN requires a nonnegative numeric denominator; UNKNOWN requires null.
   UNAVAILABLE evidence requires UNKNOWN. When compatible denominator is KNOWN,
   no numerator bound may exceed it. Do not compute a denominator from retained rows.
4. Remove `SHADOW` from edit acceptance authority; shadow is an operating mode that
   returns original text, not an accepted edit class. Schema v1 applied edits support
   only `AUTO_REPAIR`. Do not add confidence- or model-only acceptance classes.
5. Replace `MAIN_CAPTURE_FAILED` in the completed-text result reason vocabulary:
   main failure/incompletion retains upstream failure semantics and never becomes a
   successful library `RepairResult`. Provide finite non-sensitive reasons that map
   unambiguously to dispositions: original (no eligible suspicion, detect-only,
   insufficient evidence or no accepted edit), shadow-original (shadow review),
   degraded-original (analysis bound, corpus unavailable/incompatible or optional
   review failure), and patched (patch accepted). Enforce this mapping exactly.
6. In `RepairResult`, selected span IDs, review IDs and edit IDs are individually
   unique. Every review/edit ID must refer to one selected span; every edit must match
   that span's original coordinates/slice, use a nonidentity replacement and have a
   corresponding replace proposal for the same ID/replacement. Reviews present imply
   `review_call_count=1`; zero calls imply no reviews. No selected spans implies zero
   calls/reviews/edits. A shadow-original result has no edits. A patched result has at
   least one AUTO_REPAIR edit, one call, and the patch-accepted reason. Allow one call
   with no structured reviews only for a degraded optional-review failure, since an
   invalid/failed batch may produce no usable proposals.
7. Keep composition outside this correction: validate original coordinates and
   cross-record identity, but do not derive or compare the full final patched text
   from replacements. Later patcher tests own exact composition/conflict behavior.
8. `max_review_requests`, `max_generative_passes` and `max_concurrent_reviews` are
   strict positive integers capped at one. Zero and booleans fail. Retain
   `max_automatic_retries` as strict literal zero. Preserve all other finite v1
   defaults/ceilings and immutable false evidence-insufficient acceptance, storage
   and experimental flags.
9. Add direct regressions for the exact probes in Current verified state plus valid
   positive EXACT partial/thresholded, valid complete/uncut EXACT, KNOWN/UNKNOWN
   denominator states, each valid disposition/reason family, a coherent reviewed
   AUTO_REPAIR result, and degraded one-call/no-usable-review failure.
10. Run fresh checks at the corrective implementation SHA. Preserve 003-a's PARTIAL
    report and failed whole-repo Ruff observation. Force-stage exact `003-b\n`, prove
    transcript index/implementation/report blobs, and make the new report the sole
    final commit.

## Acceptance criteria

1. The two valid EXACT probes rejected by 003-a now pass without invented metadata;
   fabricated zero, inverted bounds, censored exactness, unavailable values and
   denominator contradictions still fail.
2. Denominator knowledge is explicitly serialized and strict; UNKNOWN never carries
   a number, KNOWN always does, and missing/truncated evidence never becomes zero.
3. All previously accepted impossible result probes fail. Valid original, shadow,
   degraded and patched examples pass only with their mapped reasons and coherent
   selected/review/edit/call records. `MAIN_CAPTURE_FAILED` and edit `SHADOW` are not
   public enum values.
4. Zero review-request/pass/concurrency capacities fail; defaults remain 1/1/1 and
   automatic retries remain exactly zero. Unknown fields/types/enums and nonfinite
   values remain rejected.
5. Focused/broad product tests, established scoped Ruff, mypy, full OAP suite, native
   locked/offline baseline, transcript/governance/protected-source checks and both
   required final-head CI checks pass at exact SHAs. The historical `ruff check .`
   failure remains FAILED in 003-a and is not rerun or relabelled as required proof.
6. PR #4 remains the sole open objective PR and unmerged during coding; remote 003-b
   SELF verification passes. No later objective/live/private/release/deployment work.

## Verification

Use a fresh owned native temporary environment from the frozen lock and report the
resolved commands/paths:

```text
pytest tests/contract/test_objective_003.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 003-b
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 003-b
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 9f2d71533785e7505bdc1c2539040789d055d7de
git diff --check 9f2d71533785e7505bdc1c2539040789d055d7de...HEAD
git diff --exit-code 9f2d71533785e7505bdc1c2539040789d055d7de -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After report publication, strategy independently verifies remote SELF, exact active
bytes and both checks on the literal final head. All evidence remains schema/software
evidence only, not corpus validity, linguistic benefit, live compatibility, ICA,
milestone, release or deployment evidence.

## Local setup and constraints

Use only the committed lock and owned native temporary environments/caches. Do not
mutate or depend on ignored repository `.venv`; clean owned temporary paths. Add no
dependency. Tests use synthetic Unicode/count/result records only.

No Qwen/corpus/GPU/service/port/gateway/network-setting/credential/GitHub-setting
mutation. No raw customer/model text, prompts, replacements, reviewer responses or
secrets in source, reports or logs. Live repair testing remains disabled.

## Documentation

Update public names and semantics only where the correction makes existing 003-a
documentation inaccurate. Preserve the explicit unimplemented/unproven list. Record
the established lint scope and do not claim inherited OAP Ruff cleanliness.

## Git and report publication

Stay on `oap/003-typed-spans-evidence-reviews-results-and-policy` and amend only PR
#4. Preserve `5ce260c`/`ebe9685` and all prior history. Commit/push non-report changes,
exact order and force-staged active first; run implementation-head CI and record the
literal implementation SHA.

Then create only `oap/reports/003-b-evidence-and-result-semantics.md`. Its SELF commit
has the implementation head as sole parent and changes only that report. Push,
verify remote head/bytes/parent/path and active blobs, send exact `OK`, and exit with
no later mutation. Report-head checks remain PENDING inside the report.

## Decision classification

D0. These are deterministic contract consistency bugs and one verification-scope
mistake. The corrections are bounded, reversible and fully synthetic; no new human
intent, external right, protected resource, acceptance threshold or D2 boundary is
selected.

## Deferred human adjudication
- Decision: NONE

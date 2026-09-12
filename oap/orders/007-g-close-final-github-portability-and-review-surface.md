# Work order 007-g — Close final GitHub portability and review surface

Status: FINAL

```oap-metadata
{
  "id": "007-g",
  "title": "Close final GitHub portability and review surface",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": [
    "001",
    "002",
    "003",
    "004",
    "005"
  ],
  "local_work": "Clean local and remote PR #8 head 32e25c8c9de7e19d427a74e3f4445c1687f461a4. Preserve every published 007-a..f order/report and all research/private evidence. No unrelated dirty work is present.",
  "prior_review": "007-f is strict-remote-verified but not terminal. Exact implementation-head GitHub logs show OAP bootstrap failing only on three immutable blank-at-EOF paths and Application baseline failing because copied research tests receive RUNNER_TEMP but no TMPDIR. PR metadata remains stale at f17152e despite the immutable 007-f report's contrary claim. Research and report-history jobs pass; PR #8 is open/unmerged and main branch protection remains disabled.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner authorized all forward-correction paths to finish a durable, reproducible research archive on one PR, while forbidding history rewrite, merge, new science, production work and /tmp experiment retention."
    },
    {
      "kind": "E",
      "reference": "GitHub run 34675280765 at 787c420: OAP report history SUCCESS; OAP bootstrap FAILURE only at accepted-base git diff --check on exact 007-e order, 007-f order and quarantined 007-d report blank-at-EOF diagnostics."
    },
    {
      "kind": "E",
      "reference": "GitHub run 34675280785 at 787c420: Application full pytest has 41 research fixture failures because the copied child environment has RUNNER_TEMP but lacks TMPDIR. Local persistent-TMPDIR copied full pytest passes; inherited application mypy then reports the known 11 ZipInfo/stat_result diagnostics."
    },
    {
      "kind": "I",
      "reference": "Strategic post-publication review 71e44a194cde6c46f8e947dd4c5347a6e4271fe25d97bfd4f8eb0bba1eb6279a proves exact paths, commits, blobs, SHA-256 identities, PR metadata contradiction and branch-protection state."
    },
    {
      "kind": "C",
      "reference": "007-f implementation/report evidence: 66 research and 123 OAP tests pass; final 16,375-record M2/M3 replay is exact with 350/335 preserved operational failures and zero calls. Preserve it; this round changes only CI/process portability and review metadata."
    },
    {
      "kind": "A",
      "reference": "S-ORDER-03 and S-REVIEW-01 require a new corrective suffix on the same PR after immutable 007-f publication. No numeric advancement or historical amendment is permitted."
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
    "LR-007",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "OAP report history",
    "Application baseline",
    "Research reproducibility"
  ],
  "decision_class": "D0"
}
```

## Identity

Immediate corrective suffix after published 007-f, on the SAME objective-007
branch and PR #8. This is a CI/process-integrity and review-surface correction,
not another experiment, product change, numeric objective, merge or acceptance.

## Provenance

The owner-authorized archive objective is not complete while its exact GitHub
review surface is stale or its procedural gates fail for newly introduced reasons.
This correction derives from immutable reports, actual workflow logs and direct
executable probes. Generated roadmap order is subordinate to the explicit
forward-correction authority; completed numeric history remains unchanged.

## Mandatory review

Read in full before implementation:

- `STRATEGIC_HOME/workorders/007-f-independent-postpublication-github-review.md`
- SHA-256 `71e44a194cde6c46f8e947dd4c5347a6e4271fe25d97bfd4f8eb0bba1eb6279a`

Independently refresh remote PR/head/checks. Treat exact GitHub logs as evidence;
do not infer final-head success from local tests or from 007-f's pre-publication
claims.

## Current verified state

Main is `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #8 is OPEN,
UNMERGED, branch `oap/007-concept-verification`, remote head
`32e25c8c9de7e19d427a74e3f4445c1687f461a4`. That 007-f report-only
commit has sole parent `787c420a03bdf53b7e85fe585d3db2ed8785a03b`; strict remote report
verification passes and the report SHA-256 is
`e3e383dd98af60c86f3c6acdcf324d8283c6eece040b48265725d2c6f319f224`.
CRITICAL has no entries. Main branch protection is disabled (HTTP 404); do not
change repository settings. The procedural development gate therefore remains
material and PR #8 must remain open.

## Governance

S-AUTH-01, S-STATE-01, S-ORDER-03, S-EVIDENCE-01, S-REVIEW-01 and
S-RECOVER-01 govern. Historical order/report immutability and exact 007-d
quarantine remain authoritative. This round introduces no D1/D2 decision and
does not change CRITICAL, protected product intent or development-merge authority.

## Goal and dependencies

Dependencies 001–005 and the completed 007-a..f chain remain preserved. The goal
is the smallest forward correction that makes final GitHub evidence and PR review
metadata accurately enforce and describe the archived research work.

## Outcome

Make GitHub execute the already-intended OAP and copied-test boundaries faithfully:
grandfather only the exact immutable whitespace incidents without mutating their
bytes, supply copied children an owned non-`/tmp` `TMPDIR`, and make PR #8's body
accurately describe the final archive. Preserve the 007-f archive and all science.

## Scope

Allowed only:

- one small OAP whitespace-range verifier plus exact immutable incident data;
- focused OAP tests for that verifier;
- `.github/workflows/oap-bootstrap.yml` and the accepted-base whitespace step in
  `.github/workflows/application-baseline.yml`;
- `scripts/verify_development_baseline.py` and focused contract tests only as
  needed to propagate its already-owned temporary root as child `TMPDIR`;
- exact 007-g order/active/report protocol paths;
- GitHub PR #8 body metadata without a repository commit.

Do not change `research/**`, application product code, dependency/lock files,
PLAN/ARCHITECTURE/CRITICAL/governance sources, any historical order/report,
experiment data/results, source archives, model configuration or services.

## Files and boundaries

Inspect the two workflow files, baseline driver/environment tests, OAP whitespace
helpers and focused disposable Git fixtures. Read the three known whitespace paths
only to hash/verify them; never edit them. Private campaign, dataset/index and
response roots are verification inputs by identity only and must not be copied,
logged or committed. Local scratch stays under the exact owner-selected persistent
research-runtime root; GitHub uses only runner-owned temporary storage.

## Non-goals

No Qwen/Codex/model call, replay resampling, new experiment, benchmark, analysis,
prompt/detector/gate/retry/English-policy change, corpus/source acquisition,
production repair, broad lint/type cleanup, release, deployment, merge, auto-merge,
branch-protection change, milestone/linguistic acceptance or history rewrite.

## Requirements

1. Preserve byte-for-byte every published order/report, including the three
   whitespace-incident paths. Reverify their exact current Git blobs and SHA-256
   identities from the mandatory review. 007-d remains `INVALID_QUARANTINED`;
   whitespace handling must not validate, normalize or otherwise launder it.
2. Replace generic workflow `git diff --check` calls with one fail-closed helper
   that still executes the literal accepted-base-to-revision whitespace check and
   rejects every diagnostic except the exact three known blank-at-EOF incidents.
   The exception must bind at least exact path, diagnostic/line, introduction
   commit, current revision blob identity and SHA-256. Do not create a wildcard,
   path-only allowlist, ignore all Markdown, or disable whitespace checking.
3. The helper must fail if a known path's bytes/blob/history differ, if a known
   diagnostic changes or disappears unexpectedly for these fixed workflow bases,
   if an extra whitespace error appears, if Git returns malformed/unparseable
   output, or if the requested base/revision is invalid. It may pass only the two
   currently authorized accepted bases and exact frozen incident set unless a
   future explicit correction changes the durable contract.
4. Add real disposable-Git negative tests proving: the exact current incident set
   passes; mutation of any incident path fails; deletion/re-add fails; wrong blob
   or introduction commit fails; extra whitespace fails; path/line/message drift
   fails; unknown base fails. Tests must exercise the actual CLI used by workflows.
5. Wire both OAP-bootstrap and Application-baseline whitespace steps to the new
   helper, preserving the accepted bases and all protected-source comparisons.
   Keep workflow permissions least-privilege and action pins unchanged.
6. In the baseline driver's child environment, set `TMPDIR` to an exact owned
   directory inside the invocation's validated temporary root. This same value
   must work when the parent supplied only GitHub `RUNNER_TEMP`; never fall back to
   `/tmp`, the repository, a home-wide path, or an unvalidated caller value.
7. Add focused tests proving the child `TMPDIR` is owned/inside the driver root,
   an inherited unsafe/absent `TMPDIR` cannot leak through, and a GitHub-like
   RUNNER_TEMP invocation lets copied research fixtures run. Preserve environment
   redaction, cleanup, lock/offline behavior and the explicit Git-history source.
8. Run a GHA-equivalent copied full-pytest probe locally with parent `TMPDIR`
   absent and safe `RUNNER_TEMP`/`--temp-parent` supplied. It must pass the copied
   full pytest boundary. Run the encompassing baseline with a bounded ceiling
   sufficient for completion and distinguish the inherited 11-error application
   mypy failure from any new portability failure.
9. Reverify the final archive without changing it: 66 research tests, complete
   OAP suite, publication guard, report history, transcript index/revision,
   accepted-runtime governance, protected-source diff, acquisition history,
   `git fsck --full --no-reflogs`, and zero live model/network calls. Rerun the
   saved 16,375-record offline replay at final implementation head or prove the
   entire replay/source closure is byte-identical and retain an exact receipt.
10. Push the non-report implementation head, then wait for exact-head GitHub
    results. Require Research reproducibility, OAP bootstrap acceptance and OAP
    report history SUCCESS. Application baseline may remain FAILURE only if its
    copied full pytest now passes and the first/only remaining failure is the exact
    inherited 11-error `scripts/verify_source_artifact.py` mypy boundary. Any new
    failure requires same-round correction before report publication.
11. Update PR #8 body through GitHub metadata only after the implementation head is
    final. Use real Markdown newlines and state the exact implementation head,
    66 research tests, 123-or-current OAP tests, 126 public research files,
    16,375 replay counts and zero calls, inherited static/baseline limitations,
    exact CI state, private evidence boundary, open/unmerged status, disabled
    branch-protection risk and no release/deployment/scientific-acceptance claim.
    Link durable research/OAP reports; do not reproduce raw evidence.
12. Perform a strongest-reason-not-to-publish review: can the whitespace exception
    accept any future/altered defect, can a copied test use `/tmp` or escape its
    owned root, can the PR body mislead reviewers, did any historical file change,
    and did any experiment/product behavior change? Resolve every material defect
    in 007-g before publication.

## Acceptance criteria

- The three known immutable files retain their exact reviewed blobs/SHA-256 and
  every other historical order/report is unchanged.
- Exact-incident whitespace verification passes both workflow bases; all requested
  negative histories fail closed.
- GHA-equivalent copied full pytest passes with owned child TMPDIR and no `/tmp`.
- Exact implementation-head Research, OAP bootstrap and OAP report-history checks
  are green; Application failure, if any, is only the exact inherited mypy debt.
- PR #8 body is current, readable and truthful at the final implementation head.
- Research archive/replay identities remain intact; no live call or private byte
  enters Git. PR #8 remains open and unmerged.

## Verification

Use persistent scratch under the owner-selected native research runtime. Run the
focused whitespace/TMPDIR negative tests; full research and OAP unittest suites;
native locked/offline baseline with a sufficient bounded ceiling; exact workflow
helper commands for both bases; transcript index/revision; report-history manifest;
accepted-runtime governance against literal main; protected-source diff;
acquisition history; staged publication/privacy guard; `git diff --check` over only
new 007-g changes; and `git fsck --full --no-reflogs`. Verify exact final-head
GitHub checks and PR metadata. Record PASSED/FAILED/PARTIAL distinctly.

## Local setup and constraints

Use existing locked Python/uv dependencies and already-owned persistent scratch.
No dependency installation or source/network acquisition beyond ordinary locked
CI setup is authorized. Use CPU-safe sequential verification where tests mutate
Git fixtures. Delete only exact owned disposable test directories through their
existing cleanup; never delete an original research/archive/index tree.

## Documentation

The exact whitespace incident contract/helper is durable OAP documentation.
Update workflow comments or developer documentation only where necessary to make
the narrow exception and owned TMPDIR handoff discoverable. Update PR #8 body via
GitHub metadata only. Do not alter research reports/configurations/results or
repeat private evidence in public prose.

## Git and report publication

SAME branch and PR #8. No merge. Commit/push implementation before the report.
Preflight an unpublished 007-g report. The final report commit changes only
`oap/reports/007-g-close-final-github-portability-and-review-surface.md`, has the
actual implementation head as sole parent, is pushed once and verified remotely.
Never amend 007-f or another historical report/order. Send exact `OK` only after
the durable 007-g state is valid, then exit.

## Decision classification

D0: bounded forward CI/process correction under explicit owner authority. It
does not choose product meaning, weaken scientific rules, cross a live-service
boundary or authorize merge/release/deployment. Strongest concern is that a
whitespace exception becomes a laundering mechanism; exact immutable identity,
base, diagnostic and negative-history binding keep it narrowly reversible and
auditable.

## Deferred human adjudication

- Decision: NONE

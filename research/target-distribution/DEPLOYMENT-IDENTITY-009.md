# DEPLOYMENT-IDENTITY-009 — Data-free deployment-identity record and E2
# decision package

Status: round 009-a record (objective 009, round 1). Data-free: this
document carries no endpoint values, no credentials, no private paths, and
no raw text. The full attempt-level receipt (timestamps, statuses, observed
fields, response sizes) is kept in the round private directory
(`009a-identity` under the round private research runtime root) and is never
committed.

This record supports the open E2 decision (RESEARCH-STATE section 9): which
deployment is the confirmation TARGET of the objective-009 fresh
human-labelled target-distribution study. The hard gate of
PROTOCOL-009.md element (a) blocks all confirmation collection until the
owner resolves E2 with an attributable decision.

## 1. Deployment A — the 007-lineage A100-FP8 deployment (observed)

Bounded read-only metadata re-probe executed in round 009-a (scope item 3a):
metadata GETs of the version endpoint and the models endpoint against the
out-of-band A identity only, with the authorized out-of-band profile; at
most 6 HTTP attempts total; zero chat/generation/responses calls; zero other
endpoints; zero writes; zero server mutation; zero contact with the RTX-3090
host and zero contact with Deployment B.

Attempt summary (4 of the 6 authorized attempts used; full receipt private):

| # | Endpoint class | HTTP status | Note |
| --- | --- | --- | --- |
| 1 | serving-version metadata GET | 200 | observed framework version `0.28.0` |
| 2 | models metadata GET | 401 | unauthenticated attempt, unauthorized |
| 3 | models metadata GET | 401 | bounded retry, unauthorized |
| 4 | models metadata GET | 200 | authorized out-of-band profile bearer token (value never recorded) |

Observation window: 2026-09-30T01:09:44Z to 2026-09-30T01:10:22Z UTC.

Observed identity (data-free):

- Serving framework: vLLM, version `0.28.0`.
- Model identifier: `qwen3.8-27b` (owned_by `vllm`).
- Quantization marker as present in the identity: the exposed model root
  suffix `Qwen3.8-27B-FP8` (owner-declared FP8, corroborated by the exposed
  model root name, not by weight-byte inspection).
- Max model length: 262144.
- Wire protocol class: OpenAI-compatible HTTP serving (vLLM; wire_api
  `responses` per the authorized out-of-band profile; Responses wire API
  endpoint class per the frozen 007 profiles; non-streaming).

Cross-checks:

- All observed identity fields MATCH the frozen 007 profiles (profile
  sha256 `c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60`
  and `0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e`)
  and the 2026-09-29T23:12Z live re-confirmation (vLLM 0.28.0; model
  identifier qwen3.8-27b; model root ending Qwen3.8-27B-FP8; max model
  length 262144; Responses wire API non-streaming).
- OBSERVED SERVER-SIDE CHANGE: the models metadata endpoint now returns 401
  to unauthenticated requests (attempts 2-3 above) and 200 with the
  authorized out-of-band profile (attempt 4). The 2026-09-29T23:12Z
  re-confirmation recorded the same identity; its authentication handling
  is not part of the committed record. This is an access-control
  configuration observation only: no identity field changed, no server
  mutation was performed or is authorized, and the observation does not
  alter the regime classification.
- Hardware: A100 is OWNER-DECLARED; hardware is not remotely
  hardware-inspected (carried 007 convention).

Regime classification: A100-FP8 remains a DIFFERENT regime from the PLAN
intended deployment (RTX 3090, strongly quantized). The entire 007 live
evidence base is A100-FP8 regime and does not transfer to the intended
deployment without replication (RESEARCH-STATE section 9).

## 2. Intended target — RTX-3090 (3090 unavailability record)

3090 UNAVAILABILITY RECORD. The intended RTX-3090 endpoint is
TCP-CLOSED at the 2026-09-09 reconnaissance (private reconnaissance record;
the internal address is recorded only in the private record and is not
reproduced here). The endpoint is marked MUST-NOT-BE-STARTED/RECONFIGURED.
In this round: zero probes and zero calls to that host. No attributable
human decision redefining the intended production target exists in the
durable records; the PLAN target remains authoritative.

## 3. Deployment B exclusion

B EXCLUSION. Deployment B remains EXCLUDED_BY_HUMAN_OVERRIDE: no probes, no
calls, ever. Zero contact with Deployment B in this round. This exclusion is
absolute and is not affected by any E2 resolution option below.

## 4. E2 decision package (open item; attributable owner decision required)

E2 ALTERNATIVES (each with an impact statement — evidence transferability,
rights, cost, timeline, risk):

- E2(a) Restore/authorize access to the intended quantized RTX-3090
  deployment, then pin and verify its exact model/quantization/API/runtime
  identity by the same bounded metadata procedure before collection. If the
  configuration drifted from the frozen 007-era expectation, a bounded
  replication of the frozen method on it precedes confirmation.
  Impact: evidence transferability BEST (the confirmation measures the
  PLAN-intended deployment); rights: requires owner authorization to start/
  access the endpoint (currently must-not-be-started); cost: highest
  (access restoration + verification + bounded replication if drifted);
  timeline: longest (external dependency on the endpoint operator); risk:
  lowest scientific risk, schedule risk highest.
- E2(b) Explicitly designate the A100-FP8 regime as the confirmation
  target. This is a PRODUCT-INTENT CHANGE, recorded as such: the 007 regime
  becomes the target by designation, and no additional replication is
  required (the frozen method was developed and frozen on this regime).
  Impact: evidence transferability NONE to the RTX-3090 target (the study
  then confirms the A100-FP8 regime, not the PLAN deployment — the
  deployment-validity gap in RESEARCH-STATE section 9 is closed by
  re-designation, not by transfer); rights: no new access needed (the
  authorized out-of-band identity already covers it); cost: lowest;
  timeline: shortest (collection can start immediately after the
  attributable designation, under PROTOCOL-009); risk: the delivered
  "target-distribution" label would refer to the designated regime, and any
  future RTX-3090 deployment remains unconfirmed by this study.
- E2(c) Designate another deployment, with identity pinned by the same
  procedure (bounded metadata reconnaissance, identity field-by-field,
  drift check, bounded replication if drifted from the frozen method's
  development regime).
  Impact: evidence transferability depends on the designated regime
  (assessed after pinning); rights: requires owner authorization for the
  new endpoint; cost: moderate to high; timeline: moderate; risk: moderate
  (regime mismatch risk must be assessed before collection).

Decision rule: whichever alternative is chosen, the target's pinned
identity must be verified by the bounded metadata procedure BEFORE the
first confirmation sample is collected (PROTOCOL-009 element (a) hard
gate); until the attributable owner decision, no confirmation data is
collected from any deployment and the loop idles at this boundary. The E2
question is a D2/human boundary: this round performs only the safe isolated
preparation (the bounded metadata reconnaissance and this alternatives
package); choosing/authorizing the confirmation target deployment remains
blocked pending the owner's decision.

## 5. Data-free declaration

No endpoint values, credentials, or private paths appear in this document.
The out-of-band identity (endpoint and bearer token) is provided out-of-band
per the 2026-09-20 human note and is never committed. The attempt-level
receipt (with timestamps, statuses, observed fields, and response sizes)
resides in the round private directory only.

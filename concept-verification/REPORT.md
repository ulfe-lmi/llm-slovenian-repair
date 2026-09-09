# Concept verification report

**EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE**

## Decision

`INCONCLUSIVE`. The controlled detector slice ran with a verified external index
and zero protected-slice changes in the executed tests, but the reviewer/full
pipeline ablations are not complete and the real-workload sheet has no human
labels. The result is not a production, release, deployment, milestone, or
natural-workload quality claim. The one next discriminating action is human
review of the eight-row blinded sheet; no tuning suffix is created.

## Design and boundaries

This one-round vertical slice is isolated under this directory and deliberately
duplicates future production seams. It contains a verified one-off SQLite
loader, original-coordinate protection/tokenization, deterministic unigram and
local-context suspicion, a fresh same-Qwen reviewer client, strict acceptance,
exact right-to-left patching, buffered loopback Responses-SSE proxy, controlled
evaluation, and bounded workload tooling. It uses Python 3.12 standard-library
code, synchronous blocking calls, finite timeouts, and binds only to
`127.0.0.1:18024`.

No `src/`, `scripts/`, existing tests, PLAN, architecture, governance,
workflow, objective-006 code, external cache, protected service, GPU, VPN,
gateway, port, or neighboring repository was changed. The derived SQLite,
raw SSE traces, and human sheet remain outside Git or under ignored local
results. No source rows, private responses, prompts, replacements, or
credentials are reproduced here.

## Model, protocol, and source

The selected direct reviewer is the owner-authorized Neumann Qwen 3.8 27B
Responses endpoint. Reviewer requests are fresh non-streaming calls with only
compact instructions, the exact sentence, and one target; the parser accepts
only one assistant message `output_text` with the exact three-field JSON
schema. The private profile bearer is read in memory only and is not logged.

The proxy buffers a complete upstream SSE before analysis. The fake round trip
and two completed live traces preserved event count/order, response and item
IDs, usage, completion markers, and non-text fields. Tool-only/no-safe-text
responses pass through unchanged. A live Codex invocation using the proxy
completed an owned disposable tool loop: it created/read `tool-proof.txt` and
exited successfully. Six of eight collector cases were blocked by endpoint or
capture availability; their private traces were not promoted to Git.

The two external archives were validated before and after indexing/evaluation:

- words: 115,865,656 bytes, MD5 `b20a959f9c113aeb6504f0d753d36d10`, SHA-256
  `77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a`;
- word n-grams: 22,327,366 bytes, MD5 `22e911e80ecfd2cde4458acd74d83b4b`,
  SHA-256 `782da9dd7909bfeefde5e7ee973b6031128167eec05868147d9dbfd22dc8cf40`.

The loader accessed only the selected lowercase short unigram, 2-gram, and
3-gram members. Missing unigrams are `UNAVAILABLE`; missing n-grams are
`CENSORED` under the publisher cutoff with unknown denominator; stored counts
are `EXACT`. No cache acquisition or network GET was used for the index.

## Frozen controlled evidence

The dev split has 16 cases and the held-out split 32 cases with exact recorded
spans, including the ordered Slovenian examples, contextual constructions,
typos, valid-word controls, technical English, Markdown, commands, URLs, and
paths. Dataset identities are in `eval/frozen-experiment.json` and the fixed
config is `eval/config.json`.

The derived index SHA-256 is
`de2bf3f46fa75178ccaaa172d580b1b7d75e960997f5da674b9b0414dba6db05`.
The selected frozen setting is local-context, threshold 3, frozen-v1 prompt;
the prompt template hash is recorded in the frozen file. Dev compared the two
declared detector modes across four predeclared thresholds. Held-out execution
refused identity mismatches and used only the frozen setting.

The final machine observations were:

- dev: 74 eligible words, 6 known errors, 7 candidates, recall 1.00,
  candidate precision 0.714;
- held-out: 145 eligible words, 7 known errors, 10 candidates, recall 1.00,
  candidate precision 0.700;
- reviewer accuracy, accepted/correct/harmful/missed edits, and full recovery:
  pending because live reviewer evidence is incomplete;
- protected changes in focused tests: 0;
- aggregate decision JSON: `eval/results/summary.json`, decision
  `INCONCLUSIVE`, human status `AWAITING_HUMAN_REVIEW`.

The required raw/no-repair, detector-only, reviewer-decision, full pipeline,
unigram-only, and local-context ablation slots are explicit in the aggregate
JSON. Detector-only evidence is measured; reviewer-dependent slots are not
inflated to success.

## Harm, latency, and limitations

Harm is primary. Controlled beneficial/neutral/harmful labels were not
fabricated. Real-workload benefit/harm remains `AWAITING_HUMAN_REVIEW`; the
blinded sheet has eight rows and blank labels. The two completed live traces
were protocol-valid, but six of eight requested workload calls were blocked,
so latency and edit-rate aggregates are not sufficient for a GO/PROMISING
decision. Endpoint/capture failure was recorded once and not converted into
quality evidence.

The detector is a bounded suspicion selector, not a linguistic verdict. The
short word member is not a complete lexicon, n-gram absence is censored, and
same-Qwen review is not independent statistical evidence. The experiment does
not implement morphology, production API integration, concurrency, retry,
auth/TLS framework, deployment, telemetry, or a human annotation process.

## A–J evidence answers

A. Does corpus suspicion produce candidates? **Yes** in this controlled slice;
the detector returned bounded, deterministic candidates.

B. Does the verified source support semantic proof? **No** by itself; the
source identity and exact/censored/unavailable semantics are preserved, while
the selected data remain sparse and incomplete.

C. Does local context help over unigram-only here? **Not demonstrated**; the
two modes produced the same aggregate candidate counts on this split.

D. Is reviewer isolation real? **Yes for the implemented boundary**; the
request is fresh, compact, non-streaming, and excludes main history/tools/
images/reasoning/candidates.

E. Are proposals safe to apply automatically? **Only when strict gates pass**;
exact boundaries, protection, exact unigram support, stronger compatible local
evidence, and no wider edit are required. Reviewer-dependent benefit remains
unmeasured.

F. Is exact patching/protection preserved? **Yes in focused evidence**;
original-coordinate edits leave protected slices and all outside code points
unchanged, with zero protected changes observed.

G. Is the Responses protocol preserved? **Yes for fake and two completed live
traces**; IDs, usage, order/count, completion, reasoning/tool/non-text fields
were not rewritten.

H. Does the real Codex path continue? **Yes once** in the owned disposable
tool-loop proof. This is functional evidence, not a quality label.

I. Is the operational/rights boundary plausible? **Only provisionally**;
loopback and finite bounds worked, but six live cases were blocked and external
data remain private/reusable caches rather than repository/package content.

J. Should this become production work? **No decision yet**. The correct result
is `INCONCLUSIVE` pending the one human semantic review and complete reviewer/
latency evidence; no production back-port is authorized by this report.

## Reuse, shortcuts, and follow-up

Accepted 001–005 contracts informed names and invariants. The unmerged 006
importer was not reused as product code; the concept loader is intentionally
separate. The experiment shortcuts are standard-library SQLite, synchronous
HTTPServer, a fixed controlled split, a frozen simple detector, and no
model-provider abstraction. Those shortcuts are not production acceptance.

The only next discriminating action is to have an attributable human label the
blank blinded sheet. No human disposition, automatic merge, release, deploy,
or follow-on order is implied.

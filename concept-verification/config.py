"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Configuration."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXPERIMENT_LABEL = "EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE"
WORDS_MEMBER = "GF2.0-words-all-lowercase_forms-lemmas-parts_of_speech-taxonomy-short.tsv"
BIGRAM_MEMBER = "GF2.0-word_sets-lowercase_forms-2grams-taxonomy-collocativity-entire.tsv"
TRIGRAM_MEMBER = "GF2.0-word_sets-lowercase_forms-3grams-taxonomy-collocativity-entire.tsv"


# Bounded parser configuration for the mandatory Pandoc structural protection
# (order 013-a). The reader profile is an explicit, pinned extension set; the
# values below are finite limits, not tuned optima.
PANDOC_ENV_VAR = "CONCEPT_PANDOC"
PANDOC_VERSION = "3.7.0.2"
PANDOC_READER = "commonmark_x+sourcepos-smart"
PANDOC_WRITER = "json"
PANDOC_MAX_INPUT_BYTES = 1_000_000
PANDOC_TIMEOUT_SECONDS = 10.0
PANDOC_MAX_OUTPUT_BYTES = 32_000_000
PANDOC_MAX_BLOCKS = 10_000
PANDOC_MAX_INLINES = 100_000


# Bounded occurrence-addressed reviewer batch (order 014-a).  These are
# finite limits, not tuned optima; they are enforced before dispatch and
# before any mutation.  Code-point and byte limits are distinct quantities.
# Finite reviewer timeout (order 014-a, requirement 4; whole runtime
# exchange deadline per order 019-a, requirement 1): the ordered
# existing 15-second cap anchors one monotonic deadline at
# review_batch entry covering process/IPC startup and the actual
# resolver/connect/TLS/upload/status/header/body/result work in the
# owned transport child; a late success is a failure.  It bounds the
# batch reviewer only; the historical single-target review() retains
# its historical per-call socket timeout, and the upstream capture
# timeout remains separately operator-configured.
REVIEWER_HTTP_TIMEOUT_SECONDS = 15.0
REVIEW_BATCH_VERSION = "batch-v1"
REVIEW_BATCH_MAX_ITEMS = 4
REVIEW_BATCH_MAX_TARGET_CODEPOINTS = 128
REVIEW_BATCH_CONTEXT_CODEPOINTS = 240
REVIEW_BATCH_MAX_PROMPT_CODEPOINTS = 8192
REVIEW_BATCH_MAX_REQUEST_BYTES = 32_768
REVIEW_BATCH_MAX_RESPONSE_BYTES = 32_768
REVIEW_BATCH_MAX_PROPOSAL_JSON_CODEPOINTS = 8192
REVIEW_BATCH_MAX_OUTPUT_TOKENS = 1536
REVIEW_BATCH_MAX_REPLACEMENT_WORDS = 8
REVIEW_BATCH_MAX_REPLACEMENT_CODEPOINTS = 128


# Explicit text Responses request contract (order 015-a, requirement 2).
# Named finite API limits, not tuned optima; enforced before any forward.
# Code-point and byte limits are distinct quantities.
API_MAX_REQUEST_BYTES = 2_000_000
API_MAX_MODEL_CODEPOINTS = 200
API_MAX_INPUT_CODEPOINTS = 200_000
API_MAX_MESSAGES = 64
API_MAX_MESSAGE_PARTS = 32
API_MAX_STOP_SEQUENCES = 4
API_MAX_STOP_SEQUENCE_CODEPOINTS = 32
API_MAX_OUTPUT_TOKENS = 32_768
API_MAX_METADATA_KEYS = 16
API_MAX_METADATA_KEY_CODEPOINTS = 64
API_MAX_METADATA_VALUE_CODEPOINTS = 256
API_MAX_TOP_K = 100

# Finite main-body capture byte bound (order 017-a, requirement 2):
# the raw body byte bound, independent of codepoints.  The elapsed body
# budget is the operator-configured capture timeout (CONCEPT_TIMEOUT),
# which also remains the connection/socket timeout; overall request
# deadlines are not implemented (see the README capture section).
MAIN_BODY_MAX_BYTES = 8_000_000

# Independent elapsed response-header budget (order 018-a): a finite
# positive initial engineering default for status/header acquisition.
# It is separate from the operator-configured socket/body capture
# timeout (CONCEPT_TIMEOUT) and from the fixed reviewer cap; overall
# request deadlines remain unimplemented (see the README capture
# section).  The operator may override it with CONCEPT_HEADER_TIMEOUT
# at the normal main() entry.
MAIN_HEADER_TIMEOUT_SECONDS = 30.0

# One finite positive monotonic incoming-client intake budget (order
# 020-a): bounds the accepted-connection capture of the request line,
# all headers and the exact advertised body BEFORE any downstream
# work, independent of the socket/body capture timeout (CONCEPT_
# TIMEOUT), the response-header budget (CONCEPT_HEADER_TIMEOUT) and
# the fixed 15 s reviewer exchange; overall request deadlines remain
# unimplemented.  The operator may override it with
# CONCEPT_REQUEST_TIMEOUT at the normal main() entry.
CLIENT_REQUEST_TIMEOUT_SECONDS = 30.0

# One finite positive monotonic outgoing-delivery budget (order
# 021-a): bounds the final response emission on the accepted client
# socket - status line, headers, body and the actual flush - AFTER the
# response bytes are ready.  Response-ready work (upstream capture,
# optional repair) is outside the phase.  Independent of the
# incoming-intake budget (CONCEPT_REQUEST_TIMEOUT), the response-header
# budget (CONCEPT_HEADER_TIMEOUT), the socket/body capture timeout
# (CONCEPT_TIMEOUT) and the fixed 15 s reviewer exchange; overall
# request deadlines remain unimplemented.  The operator may override it
# with CONCEPT_DELIVERY_TIMEOUT at the normal main() entry.
CLIENT_DELIVERY_TIMEOUT_SECONDS = 30.0

# One finite positive monotonic main-upstream setup budget (order
# 022-a): bounds the main upstream's preparation/request-upload
# phase - owned transport startup, address resolution (one owned
# ordinary stdlib child for named hosts; an IP-literal host needs no
# child), bounded address attempts, TCP connection, TLS handshake
# and the entire request write through the last body byte handed to
# the local transport - BEFORE response acquisition.  The existing
# response-header budget (CONCEPT_HEADER_TIMEOUT) and the socket/body
# capture timeout (CONCEPT_TIMEOUT) then run as before on their own
# independent axes, as do the incoming-intake budget
# (CONCEPT_REQUEST_TIMEOUT), the outgoing-delivery budget
# (CONCEPT_DELIVERY_TIMEOUT) and the fixed 15 s reviewer exchange;
# overall request deadlines remain unimplemented.  The operator may
# override it with CONCEPT_SETUP_TIMEOUT at the normal main() entry.
MAIN_SETUP_TIMEOUT_SECONDS = 30.0

# Finite SQLite busy wait for the read-only runtime evidence adapter
# (order 016-a, requirement 2): it bounds lock waiting per query only
# and is not a total CPU/query deadline.
RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS = 0.25

# Versioned finite runtime evidence lookup policy (order 024-a,
# requirement 2): per fresh RuntimeCorpus connection/answer, bounds
# actual SQL statement starts, fetched rows (per query and cumulative)
# and native progress-handler callbacks.  These are engineering
# defaults, not measured optima.  The progress interval bounds
# APPROXIMATE SQLite VM progress only - never CPU time, memory, I/O or
# wall time - and a nonzero callback return interrupts the real work.
RUNTIME_EVIDENCE_MAX_STATEMENTS = 65_536
RUNTIME_EVIDENCE_MAX_ROWS_PER_QUERY = 4_096
RUNTIME_EVIDENCE_MAX_ROWS_TOTAL = 262_144
RUNTIME_EVIDENCE_PROGRESS_INTERVAL = 1_000
RUNTIME_EVIDENCE_MAX_PROGRESS_CALLBACKS = 10_000

# Versioned finite analysis-eligibility limits (order 025-a,
# requirement 1): bound the completed answer admitted to the
# OPTIONAL analysis pass (detection, evidence lookup, review) on
# the runnable proxy.  These are finite initial engineering
# defaults, not measured model optima, and are enforced as two
# independent axes on the ORIGINAL captured text: code points and
# strict original UTF-8 bytes (no NFC, stripping or other
# transformation).  The byte allowance is at least the codepoint
# allowance.  Exact limit values admit; exceeding either axis
# returns the exact completed original with a fixed content-free
# analysis reason and zero analysis/evidence/review work.  No
# environment/CLI/operator knob or retry is introduced: the
# values change only through these validated versioned defaults,
# and each real use re-reads the CURRENT config.
RUNTIME_ANALYSIS_MAX_CODEPOINTS = 32_768
RUNTIME_ANALYSIS_MAX_UTF8_BYTES = 131_072


@dataclass(frozen=True)
class ArchiveSpec:
    name: str
    size: int
    md5: str
    sha256: str
    members: tuple[str, ...]
    header_sha256: str
    header_columns: int
    marker_sha256: str


WORDS = ArchiveSpec(
    "gigafida-2.0-words",
    115865656,
    "b20a959f9c113aeb6504f0d753d36d10",
    "77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a",
    (WORDS_MEMBER,),
    "c2ce44548818b72a04691c7060c0e35106393edbfde13336c60d4cd072a00638",
    28,
    "c154d685f977552d1a502059075d7b96985be443941f603ec3538040509a9d82",
)
NGRAMS = ArchiveSpec(
    "gigafida-2.0-word-ngrams",
    22327366,
    "22e911e80ecfd2cde4458acd74d83b4b",
    "782da9dd7909bfeefde5e7ee973b6031128167eec05868147d9dbfd22dc8cf40",
    (BIGRAM_MEMBER, TRIGRAM_MEMBER),
    "2566f00c0a17e5e7bfe858d9405fca3862850aec482ae05fd474381b8d5ffa53",
    31,
    "ad2229bf68f085207a5a100f23130bdcec947223e4e51b2f39a1d4ee3a056b0f",
)


def canonical_bytes(value: Any) -> bytes:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (serialized + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("configuration must be a JSON object")
    return value

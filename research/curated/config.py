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

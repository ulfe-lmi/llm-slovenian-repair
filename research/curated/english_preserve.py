"""Faithful English-preservation eligibility policy from the ten-run study."""

from __future__ import annotations

import hashlib
import importlib.metadata
import math
import os
import platform
import stat
from collections.abc import Callable
from pathlib import Path
from typing import Any

THRESHOLD = 3.0
WORD_FREQ_VERSION = "3.1.1"


class EnglishResourceError(RuntimeError):
    """The frozen external English resource cannot be verified."""


def resource_identity(resource_path: str | Path | None = None) -> dict[str, Any]:
    """Return identity for an explicit resource, or the historical wordfreq resource."""
    if resource_path is None:
        try:
            import wordfreq

            if importlib.metadata.version("wordfreq") != WORD_FREQ_VERSION:
                raise EnglishResourceError("wordfreq version differs from frozen 3.1.1")
            path = Path(wordfreq.available_languages()["en"])
        except Exception as exc:
            raise EnglishResourceError("English source cannot be loaded") from exc
    else:
        path = Path(resource_path)
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise EnglishResourceError("English resource must be a regular non-symlink file")
    return {
        "python": platform.python_version(),
        "english_data_path_supplied": resource_path is not None,
        "english_data_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "english_data_bytes": info.st_size,
        "query": 'zipf_frequency(original_target.casefold(), "en")',
        "minimum": 0.0,
        "threshold_inclusive": THRESHOLD,
        "resource_name": path.name,
        "resource_owner": info.st_uid == os.getuid(),
    }


def classify(candidate: dict[str, Any], lookup: Callable[[str], float]) -> dict[str, Any]:
    """Classify only original Slovene-unigram absences; never suppress known words."""
    evidence = candidate.get("evidence")
    if not isinstance(evidence, dict) or not isinstance(evidence.get("unigram"), dict):
        raise EnglishResourceError("candidate lacks unigram evidence")
    unigram = evidence["unigram"]
    record: dict[str, Any] = {
        "original_target": candidate["text"],
        "slovene_unigram": dict(unigram),
        "casefolded_target": candidate["text"].casefold(),
        "english_frequency": None,
        "english_classification": "NOT_QUERIED_SLOVENE_AVAILABLE",
        "review_suppressed": False,
        "reason": "slovene-unigram-not-unavailable",
        "threshold": THRESHOLD,
    }
    if unigram.get("state") != "UNAVAILABLE":
        return record
    try:
        value = lookup(candidate["text"].casefold())
        if type(value) not in (float, int) or not math.isfinite(value):
            raise ValueError("English frequency is not finite")
    except Exception as exc:
        raise EnglishResourceError("English lookup failed") from exc
    attested = value >= THRESHOLD
    record.update(
        english_frequency=value,
        english_classification="ENGLISH_ATTESTED" if attested else "BELOW_ENGLISH_ATTESTATION_THRESHOLD",
        review_suppressed=attested,
        reason="english-attested-preserve" if attested else "english-below-threshold-continue",
    )
    return record

"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Detector."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass

from corpus import Corpus
from protected import Interval, is_protected

WORD_RE = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", re.UNICODE)


@dataclass(frozen=True)
class Token:
    start: int
    end: int
    text: str
    key: str


@dataclass(frozen=True)
class Candidate:
    start: int
    end: int
    text: str
    score: float
    evidence: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def tokenize(text: str, intervals: list[Interval]) -> list[Token]:
    tokens: list[Token] = []
    for match in WORD_RE.finditer(text):
        if is_protected(match.start(), match.end(), intervals):
            continue
        value = match.group(0)
        tokens.append(Token(match.start(), match.end(), value, value.casefold()))
    return tokens


def _between_is_open(left: Token, right: Token, intervals: list[Interval]) -> bool:
    return not any(
        left.end <= item.start < right.start and item.end > left.end for item in intervals
    )


def _evidence(
    corpus: Corpus, tokens: list[Token], index: int, intervals: list[Interval]
) -> dict[str, object]:
    token = tokens[index]
    unigram = corpus.unigram(token.key)
    result: dict[str, object] = {"unigram": asdict(unigram)}
    if index > 0 and _between_is_open(tokens[index - 1], token, intervals):
        result["left_bigram"] = asdict(corpus.ngram(f"{tokens[index - 1].key} {token.key}", 2))
    if index + 1 < len(tokens) and _between_is_open(token, tokens[index + 1], intervals):
        result["right_bigram"] = asdict(corpus.ngram(f"{token.key} {tokens[index + 1].key}", 2))
    if (
        index > 0
        and index + 1 < len(tokens)
        and _between_is_open(tokens[index - 1], token, intervals)
        and _between_is_open(token, tokens[index + 1], intervals)
    ):
        result["trigram"] = asdict(
            corpus.ngram(f"{tokens[index - 1].key} {token.key} {tokens[index + 1].key}", 3)
        )
        result["alternatives"] = corpus.alternatives(tokens[index - 1].key, tokens[index + 1].key)
    return result


def detect(
    text: str,
    corpus: Corpus,
    intervals: list[Interval] | None = None,
    *,
    mode: str = "local-context",
    threshold: int = 3,
    maximum: int = 4,
) -> list[Candidate]:
    if mode not in ("unigram-only", "local-context"):
        raise ValueError("unknown detector mode")
    intervals = intervals or []
    tokens = tokenize(text, intervals)
    candidates: list[Candidate] = []
    for index, token in enumerate(tokens):
        evidence = _evidence(corpus, tokens, index, intervals)
        unigram = evidence["unigram"]
        assert isinstance(unigram, dict)
        state = str(unigram["state"])
        count = unigram.get("count")
        score = 0.0
        if state == "UNAVAILABLE":
            score += 1.0
        elif isinstance(count, int) and count <= threshold:
            score += 0.5
        if mode == "local-context":
            exact_local = sum(
                isinstance(value, dict) and value.get("state") == "EXACT"
                for key, value in evidence.items()
                if key.endswith("bigram") or key == "trigram"
            )
            if exact_local:
                score -= min(0.35, 0.1 * exact_local)
        if score <= 0:
            continue
        candidates.append(Candidate(token.start, token.end, token.text, round(score, 6), evidence))
    candidates.sort(key=lambda item: (-item.score, item.start, item.end))
    selected: list[Candidate] = []
    for candidate in candidates:
        if any(candidate.start < prior.end and candidate.end > prior.start for prior in selected):
            continue
        selected.append(candidate)
        if len(selected) >= min(maximum, 8):
            break
    return sorted(selected, key=lambda item: (item.start, item.end))


def candidate_summary(candidates: Iterable[Candidate]) -> list[dict[str, object]]:
    return [candidate.as_dict() for candidate in candidates]

"""Data-free deterministic CPU ranking for frozen C>1 Levenshtein-one sets.

Order 007-m increment 1 seam for the exact frozen 007-j ambiguous population.
The predeclared candidate score is this lexicographic tuple, compared in
descending order:

    (trigram_exact_flag,
     trigram_exact_count,
     exact_bigram_side_count,
     sum_of_exact_bigram_counts,
     unigram_exact_count)

Only the hypothetical candidate is substituted into the frozen immediate
left/right context; the frozen neighbour words never change.  Evidence is read
through caller-supplied query functions that honour the frozen index contract:
unigram absence is UNAVAILABLE, bigram/trigram absence is CENSORED (the index
is truncated near 2 per million, so absence is not a count of zero).  Actual
states and counts are persisted separately from the numeric comparison
placeholders; a placeholder after an exactness flag is comparison machinery
only and never redefines missing or censored evidence as zero evidence.
Operation class and candidate text order do not affect rank; stable text order
is persistence/display only.  An exact top-score tie selects nothing, makes no
validator call, and retains the original.

Rank is reported as a tie-aware competition interval, never as a scalar
position derived from display order: every member of a score group receives
rank_min = 1 plus the number of candidates with a strictly greater score and
rank_max = the number of candidates with a score greater than or equal to
that group's score.  No operation or candidate text affects either bound; the
stable text order only displays members inside a group, and a reference
persists its score-group interval without choosing a candidate inside a tie.

Gold/reference is structurally absent from every function in this module.
Reference headroom is computed by the 007-m driver strictly after ranking.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

EXACT = "EXACT"
CENSORED = "CENSORED"
UNAVAILABLE = "UNAVAILABLE"
STATES = frozenset({EXACT, CENSORED, UNAVAILABLE})

BIGRAM_LENGTH = 2
TRIGRAM_LENGTH = 3

TOP_K = (1, 2, 3, 5, 10)

FORBIDDEN_LIST_KEYS = frozenset({"candidates", "candidate_list", "candidate_options"})


class RankingError(ValueError):
    """Raised when a frozen shape or the ranking boundary is violated."""


UnigramQuery = Callable[[str], tuple[str, int | None]]
NgramQuery = Callable[[str, int], tuple[str, int | None]]


def _word_shaped(value: object) -> bool:
    return isinstance(value, str) and bool(value) and not any(char.isspace() for char in value)


def _tokens(key: str) -> list[str]:
    parts = key.split(" ")
    if any(not _word_shaped(part) for part in parts):
        raise RankingError(f"frozen evidence key is not a token phrase: {key!r}")
    return parts


def _check_ngram_evidence(name: str, value: object, expected_tokens: int) -> str:
    if not isinstance(value, Mapping):
        raise RankingError(f"frozen {name} evidence is not an object")
    key = value.get("key")
    state = value.get("state")
    count = value.get("count")
    if not isinstance(key, str) or key != key.strip():
        raise RankingError(f"frozen {name} evidence key is malformed")
    if len(_tokens(key)) != expected_tokens:
        raise RankingError(f"frozen {name} evidence token count is malformed")
    if state not in STATES:
        raise RankingError(f"frozen {name} evidence state is unknown: {state!r}")
    if state == EXACT:
        if type(count) is not int or count < 1:
            raise RankingError(f"frozen {name} exact evidence lacks a positive count")
    elif count is not None:
        raise RankingError(f"frozen {name} non-exact evidence must not carry a count")
    return key


def _check_query_result(state: object, count: object) -> tuple[str, int | None]:
    if state not in STATES:
        raise RankingError(f"evidence query returned an unknown state: {state!r}")
    if state == EXACT:
        if type(count) is not int or count < 1:
            raise RankingError("EXACT evidence requires a positive integer count")
    elif count is not None:
        raise RankingError("non-EXACT evidence must carry no count")
    return str(state), None if count is None else int(count)


@dataclass(frozen=True)
class CandidateContext:
    """Frozen immediate left/right context words for one target.

    ``None`` means the frozen detector had no open immediate neighbour on that
    side (sentence boundary or protected interval); the candidate keys for
    that side and for the trigram are then undefined, not censored.
    """

    left_word: str | None
    right_word: str | None

    @property
    def has_left(self) -> bool:
        return self.left_word is not None

    @property
    def has_right(self) -> bool:
        return self.right_word is not None


def extract_context(evidence: Mapping[str, object], lookup_form: str) -> CandidateContext:
    """Extract the frozen immediate left/right context for one target.

    ``evidence`` is the frozen per-target detector evidence mapping with the
    007-i/007-j shapes: optional ``left_bigram``/``right_bigram``/``trigram``
    objects of ``{"key", "state", "count"}``.  A missing side means the frozen
    detector had no open immediate neighbour on that side.  Raises
    :class:`RankingError` on any malformed frozen shape.
    """
    if not _word_shaped(lookup_form):
        raise RankingError("lookup form is not a single word-shaped token")
    left_value = evidence.get("left_bigram")
    right_value = evidence.get("right_bigram")
    trigram_value = evidence.get("trigram")
    suffix = " " + lookup_form
    prefix = lookup_form + " "
    left_word: str | None = None
    right_word: str | None = None
    if left_value is not None:
        key = _check_ngram_evidence("left_bigram", left_value, BIGRAM_LENGTH)
        if not key.endswith(suffix):
            raise RankingError("frozen left bigram does not end in the lookup token")
        left_word = key[: -len(suffix)]
    if right_value is not None:
        key = _check_ngram_evidence("right_bigram", right_value, BIGRAM_LENGTH)
        if not key.startswith(prefix):
            raise RankingError("frozen right bigram does not start in the lookup token")
        right_word = key[len(prefix) :]
    if trigram_value is not None:
        key = _check_ngram_evidence("trigram", trigram_value, TRIGRAM_LENGTH)
        if left_word is None or right_word is None:
            raise RankingError("frozen trigram requires both immediate neighbours")
        if key != f"{left_word} {lookup_form} {right_word}":
            raise RankingError("frozen trigram does not match the frozen bigram sides")
    elif left_word is not None and right_word is not None:
        raise RankingError("frozen context has both neighbours but no trigram")
    return CandidateContext(left_word, right_word)


@dataclass(frozen=True)
class EvidenceSlot:
    """One persisted evidence state; ``count`` is ``None`` unless EXACT."""

    state: str
    count: int | None

    def as_dict(self) -> dict[str, Any]:
        return {"state": self.state, "count": self.count}


def _candidate_keys(context: CandidateContext, form: str) -> dict[str, str | None]:
    if not _word_shaped(form):
        raise RankingError("candidate form is not a single word-shaped token")
    trigram = None
    if context.left_word is not None and context.right_word is not None:
        trigram = f"{context.left_word} {form} {context.right_word}"
    return {
        "unigram": form,
        "left_bigram": f"{context.left_word} {form}" if context.left_word is not None else None,
        "right_bigram": f"{form} {context.right_word}" if context.right_word is not None else None,
        "trigram": trigram,
    }


@dataclass(frozen=True)
class CandidateScore:
    """Frozen evidence states plus the predeclared comparison tuple."""

    text: str
    operation: str
    trigram: EvidenceSlot
    left_bigram: EvidenceSlot
    right_bigram: EvidenceSlot
    unigram: EvidenceSlot

    @property
    def score(self) -> tuple[int, int, int, int, int]:
        return score_tuple(self)

    def as_dict(self, rank: RankInterval | None = None) -> dict[str, Any]:
        record: dict[str, Any] = {
            "text": self.text,
            "operation": self.operation,
            "score": list(self.score),
            "trigram": self.trigram.as_dict(),
            "left_bigram": self.left_bigram.as_dict(),
            "right_bigram": self.right_bigram.as_dict(),
            "unigram": self.unigram.as_dict(),
        }
        if rank is not None:
            record["rank_interval"] = rank.as_dict()
        return record


def score_tuple(score: CandidateScore) -> tuple[int, int, int, int, int]:
    """Return the predeclared lexicographic comparison tuple.

    Numeric placeholders after an exactness flag are comparison machinery
    only; they never redefine missing or censored evidence as zero evidence.
    """
    trigram = score.trigram
    exact_sides = [side for side in (score.left_bigram, score.right_bigram) if side.state == EXACT]
    unigram = score.unigram
    return (
        1 if trigram.state == EXACT else 0,
        trigram.count if trigram.state == EXACT else 0,
        len(exact_sides),
        sum(side.count for side in exact_sides),
        unigram.count if unigram.state == EXACT else 0,
    )


def score_candidate(
    context: CandidateContext,
    text: str,
    operation: str,
    unigram_query: UnigramQuery,
    ngram_query: NgramQuery,
) -> CandidateScore:
    """Score one hypothetical candidate against the frozen context.

    Only ``text`` (the candidate form) is substituted into the frozen
    immediate left/right context; the context words never change.  A frozen
    context side that is absent produces an UNAVAILABLE slot, not a query and
    not a censored one.
    """
    if not isinstance(operation, str) or not operation:
        raise RankingError("candidate operation must be a non-empty label")
    keys = _candidate_keys(context, text)
    unigram = EvidenceSlot(*_check_query_result(*unigram_query(keys["unigram"])))
    slots: dict[str, EvidenceSlot] = {"unigram": unigram}
    for name, length in (
        ("left_bigram", BIGRAM_LENGTH),
        ("right_bigram", BIGRAM_LENGTH),
        ("trigram", TRIGRAM_LENGTH),
    ):
        key = keys[name]
        if key is None:
            slots[name] = EvidenceSlot(UNAVAILABLE, None)
        else:
            slots[name] = EvidenceSlot(*_check_query_result(*ngram_query(key, length)))
    return CandidateScore(
        text=text,
        operation=operation,
        trigram=slots["trigram"],
        left_bigram=slots["left_bigram"],
        right_bigram=slots["right_bigram"],
        unigram=unigram,
    )


@dataclass(frozen=True)
class RankInterval:
    """Tie-aware competition interval for one score group.

    ``rank_min`` is 1 plus the number of candidates with a strictly greater
    score; ``rank_max`` is the number of candidates with a score greater than
    or equal to the group's score.  No operation or candidate text affects
    either bound.
    """

    rank_min: int
    rank_max: int

    def as_dict(self) -> dict[str, Any]:
        return {"min": self.rank_min, "max": self.rank_max}


@dataclass(frozen=True)
class TargetRanking:
    """Deterministic ranking of one complete frozen C>1 candidate set."""

    scores: tuple[CandidateScore, ...]  # stable text order (persistence/display)
    rank_order: tuple[CandidateScore, ...]  # display only: score descending, text order within ties
    top: CandidateScore | None
    tied: bool
    rank_intervals: dict[str, RankInterval]  # tie-aware interval per candidate text

    @property
    def tie_groups(self) -> tuple[dict[str, Any], ...]:
        """Score groups of size > 1, ordered by score descending (display only).

        Each group carries its tie-aware rank interval and its members in
        stable text order; ``top_group`` marks the maximum-score group.
        """
        best = max(score.score for score in self.scores)
        grouped: dict[tuple[int, int, int, int, int], list[str]] = {}
        for score in self.rank_order:
            grouped.setdefault(score.score, []).append(score.text)
        groups: list[dict[str, Any]] = []
        for group_score, texts in grouped.items():
            if len(texts) < 2:
                continue
            interval = self.rank_intervals[texts[0]]
            groups.append(
                {
                    "size": len(texts),
                    "rank_interval": interval.as_dict(),
                    "top_group": group_score == best,
                    "texts": list(texts),
                }
            )
        return tuple(groups)

    def to_dict(self) -> dict[str, Any]:
        return {
            "set_size": len(self.scores),
            "candidates": [score.as_dict(self.rank_intervals[score.text]) for score in self.scores],
            "tie_groups": list(self.tie_groups),
            "top": self.top.text if self.top is not None else None,
            "tied": self.tied,
        }


def rank_candidates(
    candidates: Sequence[Mapping[str, str]],
    context: CandidateContext,
    unigram_query: UnigramQuery,
    ngram_query: NgramQuery,
) -> TargetRanking:
    """Rank a complete frozen C>1 candidate set by the predeclared tuple.

    ``candidates`` is the frozen distance-one union as ``{"text",
    "operation"}`` entries.  Only the evidence tuple affects order; the
    stable text order is persistence/display only and never a tiebreak.  An
    exact top-score tie selects nothing.  Every candidate carries a tie-aware
    rank interval whose bounds depend only on the score tuple.  No
    gold/reference input exists in this API.
    """
    if len(candidates) < 2:
        raise RankingError("ranking seam requires a C>1 candidate set")
    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for item in candidates:
        if not isinstance(item, Mapping):
            raise RankingError("candidate entries must be mappings")
        text = item.get("text")
        operation = item.get("operation")
        if not _word_shaped(text) or not isinstance(operation, str) or not operation:
            raise RankingError("candidate entry lacks a word-shaped text and an operation")
        if text in seen:
            raise RankingError("duplicate candidate text in a frozen set")
        seen.add(text)
        entries.append((text, operation))
    scores = tuple(
        score_candidate(context, text, operation, unigram_query, ngram_query)
        for text, operation in sorted(entries)
    )
    best = max(score.score for score in scores)
    winners = [score for score in scores if score.score == best]
    tied = len(winners) != 1
    top = None if tied else winners[0]
    rank_order = tuple(
        sorted(scores, key=lambda score: (tuple(-value for value in score.score), score.text))
    )
    group_intervals: dict[tuple[int, int, int, int, int], RankInterval] = {}
    for score in scores:
        value = score.score
        if value not in group_intervals:
            greater = sum(1 for other in scores if other.score > value)
            greater_or_equal = sum(1 for other in scores if other.score >= value)
            group_intervals[value] = RankInterval(1 + greater, greater_or_equal)
    rank_intervals = {score.text: group_intervals[score.score] for score in scores}
    return TargetRanking(
        scores=scores,
        rank_order=rank_order,
        top=top,
        tied=tied,
        rank_intervals=rank_intervals,
    )


def _assert_single_candidate_payload(payload: Mapping[str, Any], selected: str) -> None:
    if not isinstance(payload, Mapping):
        raise RankingError("dispatch payload must be a mapping")
    forms = [value for key, value in payload.items() if key == "candidate_form"]
    if len(forms) != 1:
        raise RankingError("dispatch payload must carry exactly one candidate_form")
    form = forms[0]
    if not _word_shaped(form):
        raise RankingError("dispatch candidate_form is not a single word-shaped token")
    if form != selected:
        raise RankingError("dispatch payload does not carry the selected candidate")

    def walk(value: Any, path: str) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                if isinstance(key, str) and key in FORBIDDEN_LIST_KEYS:
                    raise RankingError(
                        f"candidate list is forbidden in a dispatch payload: {path}/{key}"
                    )
                walk(item, f"{path}/{key}")
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            embedded = [
                item for item in value if isinstance(item, Mapping) and "candidate_form" in item
            ]
            if len(embedded) >= 2:
                raise RankingError(f"dispatch payload embeds multiple candidates: {path}")
            for position, item in enumerate(value):
                walk(item, f"{path}[{position}]")

    walk(payload, "$")


def select_for_dispatch(
    selections: Sequence[tuple[TargetRanking, Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    """Return at most one dispatch payload per C>1 target.

    Tied rankings select nothing.  Each returned payload is a shallow copy of
    the caller payload after proving it describes exactly one candidate and
    embeds no candidate list; the later frozen validator receives one
    sentence/original/candidate prompt, never a list.
    """
    payloads: list[dict[str, Any]] = []
    for ranking, payload in selections:
        if ranking.tied or ranking.top is None:
            continue
        _assert_single_candidate_payload(payload, ranking.top.text)
        payloads.append(dict(payload))
    return payloads

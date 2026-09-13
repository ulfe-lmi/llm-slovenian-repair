"""Complete standard-Levenshtein-distance-one candidate enumeration.

This is a data-free research seam for order 007-j.  It works on Python
Unicode strings as sequences of code points and deliberately performs no
normalization, ranking, morphology, or network access.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping

type Operation = str
SUBSTITUTION: Operation = "SUBSTITUTION"
INSERTION: Operation = "INSERTION"
DELETION: Operation = "DELETION"
OPERATIONS = frozenset({SUBSTITUTION, INSERTION, DELETION})


def _word_shaped(value: object) -> bool:
    return isinstance(value, str) and bool(value) and not any(char.isspace() for char in value)


def standard_levenshtein_distance(left: str, right: str) -> int:
    """Return ordinary unit-cost Levenshtein distance over Unicode code points."""
    if not isinstance(left, str) or not isinstance(right, str):
        raise TypeError("Levenshtein inputs must be strings")
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for left_char_index, left_char in enumerate(left, start=1):
        current = [left_char_index]
        for right_char_index, right_char in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_char_index] + 1,
                    previous[right_char_index - 1] + (left_char != right_char),
                )
            )
        previous = current
    return previous[-1]


def operation_for_one_edit(source: str, candidate: str) -> Operation | None:
    """Classify a distance-one pair, returning ``None`` for every other pair."""
    if not _word_shaped(source) or not _word_shaped(candidate):
        return None
    if source == candidate:
        return None
    if len(candidate) == len(source):
        return (
            SUBSTITUTION
            if sum(left != right for left, right in zip(source, candidate, strict=True)) == 1
            else None
        )
    if len(candidate) == len(source) + 1:
        shorter, longer = source, candidate
        offset = 0
        while offset < len(shorter) and shorter[offset] == longer[offset]:
            offset += 1
        if longer[offset + 1 :] == shorter[offset:]:
            return INSERTION
        return None
    if len(candidate) + 1 == len(source):
        shorter, longer = candidate, source
        offset = 0
        while offset < len(shorter) and shorter[offset] == longer[offset]:
            offset += 1
        if shorter[offset:] == longer[offset + 1 :]:
            return DELETION
        return None
    return None


def deletion_signatures(value: str) -> tuple[str, ...]:
    """Return all code-point deletion signatures, retaining repeated positions."""
    if not isinstance(value, str):
        raise TypeError("signature input must be a string")
    return tuple(value[:index] + value[index + 1 :] for index in range(len(value)))


def build_deletion_signature_index(vocabulary: Iterable[str]) -> dict[str, set[str]]:
    """Index unique word-shaped vocabulary forms by every deletion signature."""
    index: defaultdict[str, set[str]] = defaultdict(set)
    for form in set(vocabulary):
        if not _word_shaped(form):
            continue
        for signature in deletion_signatures(form):
            index[signature].add(form)
    return dict(index)


def vocabulary_code_points(vocabulary: Iterable[str]) -> tuple[str, ...]:
    """Return the exact code-point alphabet occurring in word-shaped forms."""
    return tuple(
        sorted({character for form in vocabulary if _word_shaped(form) for character in form})
    )


def distance_one_candidates(
    lookup_form: str,
    vocabulary: Iterable[str],
    *,
    deletion_index: Mapping[str, Iterable[str]] | None = None,
    alphabet: Iterable[str] | None = None,
) -> list[dict[str, str]]:
    """Return the complete deduplicated distance-one candidate union.

    ``lookup_form`` is already the caller's casefolded lookup view.  The
    vocabulary values are compared byte-for-byte as supplied; no casefolding
    or normalization is performed here.  Results are sorted only for stable
    persistence and never ranked for selection.
    """
    if not _word_shaped(lookup_form):
        return []
    if isinstance(vocabulary, set | frozenset):
        # The research driver has already verified the vocabulary as a set of
        # exact forms.  Reusing it avoids copying 141k entries per target.
        forms = vocabulary
    else:
        forms = {form for form in vocabulary if _word_shaped(form)}
    possible: set[str] = set()

    # Deletion from the source is directly enumerable.  For substitution and
    # insertion, every code point in a matching vocabulary form must occur in
    # the finite vocabulary alphabet; membership checks make this complete
    # without constructing a global signature index for every target.
    possible.update(
        signature for signature in deletion_signatures(lookup_form) if signature in forms
    )
    if alphabet is None:
        index = deletion_index or build_deletion_signature_index(forms)
        possible.update(index.get(lookup_form, ()))
        for signature in deletion_signatures(lookup_form):
            possible.update(index.get(signature, ()))
    else:
        for position in range(len(lookup_form)):
            for character in alphabet:
                possible.add(lookup_form[:position] + character + lookup_form[position + 1 :])
        for position in range(len(lookup_form) + 1):
            for character in alphabet:
                possible.add(lookup_form[:position] + character + lookup_form[position:])

    result: list[dict[str, str]] = []
    for form in sorted(possible & forms):
        operation = operation_for_one_edit(lookup_form, form)
        if operation is not None:
            result.append({"text": form, "operation": operation})
    return result


def cardinality(candidates: Iterable[Mapping[str, str]]) -> str:
    """Return the order's complete-union cardinality label."""
    count = sum(1 for _ in candidates)
    return "C=0" if count == 0 else "C=1" if count == 1 else "C>1"

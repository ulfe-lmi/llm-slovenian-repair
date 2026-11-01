"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Composed-result validation for individually accepted edits."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from detector import Candidate, Token, tokenize
from protected import Interval
from qwen_client import Proposal
from repair import accept

from corpus import Corpus

# Fixed content-free reason label for an edit that passed individual
# acceptance but whose interacting conflict group is not positively
# supported by the composed result (order 027-a, requirements 3-5).
COMPOSED_REJECTED = "composed-context-rejected"

# Fixed content-free reason label for the whole optional pass that
# must abstain to the completed original because a validation mapping
# cannot be proved (order 027-a, requirement 6).
COMPOSED_MAPPING_UNPROVABLE = "composed-mapping-unprovable"


class ComposedMappingError(ValueError):
    """A validation mapping cannot be proved for one record: its
    rebased span is out of range, no longer equals the exact original
    slice, or matches no actual token of the validation view.  Order
    027-a requirement 6 requires the WHOLE optional pass to abstain to
    the conservatively completed original - never to retain the
    independently supported groups around the unprovable mapping.
    """


@dataclass(frozen=True)
class ComposedRecord:
    """One individually accepted edit plus the exact original context
    needed to re-validate it under the prospective composition of the
    other surviving edits (order 027-a, requirements 3 and 4).

    All coordinates are Python Unicode code-point coordinates into the
    UNMODIFIED original (A-SPAN-01): ``text`` is the exact original
    slice at ``start:end`` (the whole selected span), and ``left``/
    ``right`` are the casefolded keys of the EXTERNAL neighbor tokens
    immediately outside that span, with their exact original bounds -
    the span's internal words are never its external neighbors.
    ``replacement`` is the accepted nonempty string and
    ``decision_index`` locates the engine decision record this edit
    produced.
    """

    decision_index: int
    start: int
    end: int
    text: str
    replacement: str
    left: str | None
    right: str | None
    left_bounds: tuple[int, int] | None
    right_bounds: tuple[int, int] | None


def _shift(edits: Sequence[tuple[int, int, str]], position: int) -> int:
    """Net code-point displacement at ``position`` caused by the given
    exact original-coordinate edits, of which none intersects the
    queried region (every edit ends at or before the position, or
    starts at or after it)."""
    return sum(
        len(replacement) - (end - start)
        for start, end, replacement in edits
        if end <= position
    )


def _compose_view(
    original: str,
    others: Sequence[tuple[int, int, str]],
    intervals: Sequence[Interval],
) -> tuple[str, list[Interval]]:
    """The validation view: the original with the exact ``others``
    edits composed (descending, original coordinates), plus the
    protected intervals displaced by the same exact arithmetic.  The
    edits never intersect protected content, so every interval is
    either wholly displaced or untouched and the mapping is exact."""
    ordered = sorted(others, key=lambda item: (item[0], item[1]))
    view = original
    for start, end, replacement in reversed(ordered):
        view = view[:start] + replacement + view[end:]
    return view, [
        Interval(
            interval.start + _shift(ordered, interval.start),
            interval.end + _shift(ordered, interval.start),
            interval.reason,
        )
        for interval in intervals
    ]


def _interacts(a: ComposedRecord, b: ComposedRecord) -> bool:
    """True iff one record's original external neighbor token is
    contained in (in particular equal to) the other record's selected
    span: the two edits interact because each can remove the other's
    local evidence context.  Tokens are exact tokenizer units, so
    containment of a whole neighbor token in a whole span is the exact
    original interval relation - for multiword spans both external
    neighbor tokens of the adjacent span are proper subsets, and exact
    whole-span equality would miss the edge.  It is never a substring
    relation, and protected/barrier plus overlap/stale validation stay
    in the actual accept checks."""
    a_span = (a.start, a.end)
    b_span = (b.start, b.end)
    def contained(span: tuple[int, int], bounds: tuple[int, int] | None) -> bool:
        return bounds is not None and span[0] <= bounds[0] and bounds[1] <= span[1]

    return (
        contained(a_span, b.left_bounds)
        or contained(a_span, b.right_bounds)
        or contained(b_span, a.left_bounds)
        or contained(b_span, a.right_bounds)
    )


def _components(indices: Sequence[int], records: Sequence[ComposedRecord]) -> list[list[int]]:
    """The connected components of the interaction graph restricted to
    ``indices``, in deterministic order (ascending seed)."""
    remaining = set(indices)
    components: list[list[int]] = []
    while remaining:
        seed = min(remaining)
        component = [seed]
        remaining.discard(seed)
        frontier = [seed]
        while frontier:
            index = frontier.pop()
            for other in sorted(remaining):
                if _interacts(records[index], records[other]):
                    component.append(other)
                    remaining.discard(other)
                    frontier.append(other)
        components.append(component)
    return components


def _revalidate(
    original: str,
    record: ComposedRecord,
    others: Sequence[ComposedRecord],
    corpus: Corpus,
    intervals: Sequence[Interval],
) -> bool:
    """Re-run the actual acceptance checks for one record on the
    validation view - the original with the exact ``others`` edits
    composed - with the record's span rebased arithmetically by the
    exact original edits (never substring search) and the EXTERNAL
    neighbors re-derived as the exact actual tokens of the view
    adjacent to the whole rebased span.  A changed neighbor therefore
    re-enters the local evidence under its actual full token key (a
    prefix of the original slice is not an unchanged token), and a
    protected interval between the derived neighbor and the span still
    bars the adjacency through the actual accept barrier check."""
    others_edits = [(item.start, item.end, item.replacement) for item in others]
    view, view_intervals = _compose_view(original, others_edits, intervals)
    shift = _shift(others_edits, record.start)
    start = record.start + shift
    end = record.end + shift
    if not 0 <= start < end <= len(view) or view[start:end] != record.text:
        # The prospective mapping for this record cannot be proved
        # (order 027-a, requirement 6): the whole optional pass must
        # abstain to the completed original.
        raise ComposedMappingError("validation mapping cannot be proved")
    tokens = tokenize(view, view_intervals)
    token_index = next(
        (i for i, token in enumerate(tokens) if token.start == start), None
    )
    if token_index is None:
        raise ComposedMappingError("validation mapping cannot be proved")
    left: Token | None = tokens[token_index - 1] if token_index else None
    right: Token | None = next(
        (token for token in tokens[token_index + 1 :] if token.start >= end),
        None,
    )
    decision = accept(
        view,
        Candidate(start, end, record.text, 0.0, {}),
        Proposal(False, record.replacement, False),
        corpus,
        view_intervals,
        left=left.key if left is not None else None,
        right=right.key if right is not None else None,
        left_bounds=(left.start, left.end) if left is not None else None,
        right_bounds=(right.start, right.end) if right is not None else None,
    )
    return decision.accepted


def validate_composed(
    original: str,
    records: Sequence[ComposedRecord],
    corpus: Corpus,
    intervals: Sequence[Interval],
) -> frozenset[int]:
    """Return the indices of the records that survive composed-result
    validation (order 027-a, requirements 3-5).

    Every interacting conflict group - the connected component of
    edits whose spans are each other's original external neighbor
    tokens - is validated as a group against the prospective
    composition: each member is re-validated with the actual accept
    checks on the original with all other surviving edits composed,
    its coordinates rebased arithmetically by the exact original edits
    (requirement 4) and its external neighbors re-derived as the exact
    actual tokens of the validation view.  A member whose positive
    local support depended on a neighbor token that another surviving
    edit replaces is rejected with the group, and a group is rejected
    as a whole when any member is not positively supported by the
    composed result - no winner is chosen and the group is rebuilt
    from the original.  Independently supported records - including
    compatible edits in one answer - survive.  The set is recomputed
    to a finite fixed point: each pass either accepts the current set
    or removes a whole conflicting group, so the iteration is
    deterministic and bounded.  The corpus is only queried through the
    real read-only interface, so a known technical/budget failure
    propagates for the caller's late abort path (requirement 8).
    If any record's validation mapping cannot be proved - rebased span
    out of range, exact original slice mismatch, or no actual token at
    the rebased span - ComposedMappingError propagates instead: the
    caller must abstain the WHOLE optional pass to the conservatively
    completed original with the accurate actual review calls/usage and
    final false dispositions (requirement 6), which is distinct from
    the ordinary rejection of one unsupported conflict group.
    """
    current = list(range(len(records)))
    while True:
        surviving: list[int] = []
        for component in _components(current, records):
            intact = True
            for index in component:
                others = [records[i] for i in current if i != index]
                if not _revalidate(original, records[index], others, corpus, intervals):
                    intact = False
                    break
            if intact:
                surviving.extend(component)
        if len(surviving) == len(current):
            return frozenset(current)
        current = surviving

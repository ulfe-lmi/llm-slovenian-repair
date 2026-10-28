"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Evidence budget."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import config

# The progress interval crosses a C boundary as a native int; fetched
# sizes and quota counters cross as machine integers on this platform.
# Values beyond these bounds are rejected BEFORE any bind/open instead
# of relying on platform overflow behavior (order 024-a, requirement 2;
# probe 024-native-callback-fault-and-range-observation.json).
_C_INT_MAX = 2**31 - 1
_NATIVE_SAFE_MAX = 2**62

# One bounded fetchmany step.  Every fetched row is still accounted
# against the per-query and cumulative row quotas, and a LIMIT/fetch
# cap alone cannot bound scan/sort work: the native progress interrupt
# is the complementary boundary (order 024-a, requirement 4).
EVIDENCE_FETCH_CHUNK_ROWS = 8192


def _validated_limit(finite: int, override: int | None) -> int:
    value = finite if override is None else override
    if type(value) is not int or not 0 < value <= _NATIVE_SAFE_MAX:
        raise ValueError(
            "evidence limit must be a positive integer within the native safe range"
        )
    return value


def _validated_interval(finite: int, override: int | None) -> int:
    value = finite if override is None else override
    if type(value) is not int or not 0 < value <= _C_INT_MAX:
        raise ValueError(
            "progress interval must be a positive integer within the native C range"
        )
    return value


@dataclass(frozen=True)
class EvidenceLimits:
    """One immutable finite evidence-work policy for a fresh instance."""

    max_statements: int
    max_rows_per_query: int
    max_rows_total: int
    progress_interval: int
    max_progress_callbacks: int

    @classmethod
    def from_values(
        cls,
        max_statements: int | None = None,
        max_rows_per_query: int | None = None,
        max_rows_total: int | None = None,
        progress_interval: int | None = None,
        max_progress_callbacks: int | None = None,
    ) -> EvidenceLimits:
        """Resolve None to the CURRENT config defaults, then validate.

        ``None`` always means the current finite config default, never
        disabled or unbounded; bool, nonintegral, nonfinite, nonpositive
        and native-overflow values are rejected with no coercion
        (order 024-a, requirement 2).
        """
        return cls(
            _validated_limit(
                config.RUNTIME_EVIDENCE_MAX_STATEMENTS, max_statements
            ),
            _validated_limit(
                config.RUNTIME_EVIDENCE_MAX_ROWS_PER_QUERY, max_rows_per_query
            ),
            _validated_limit(config.RUNTIME_EVIDENCE_MAX_ROWS_TOTAL, max_rows_total),
            _validated_interval(
                config.RUNTIME_EVIDENCE_PROGRESS_INTERVAL, progress_interval
            ),
            _validated_limit(
                config.RUNTIME_EVIDENCE_MAX_PROGRESS_CALLBACKS,
                max_progress_callbacks,
            ),
        )


def validate_default_evidence_policy() -> EvidenceLimits:
    """Pure validation of the CURRENT config default policy.

    Reads the config attributes at call time and touches no index,
    file or connection, so the real proxy constructor can require the
    startup policy to hold before any bind allocation (order 024-a,
    requirement 2).
    """
    return EvidenceLimits.from_values()


@dataclass
class EvidenceBudgetState:
    """One mutable per-connection budget; fresh per instance/answer."""

    limits: EvidenceLimits
    statements: int = 0
    rows_total: int = 0
    callbacks: int = 0
    exhausted: bool = False
    pending_control: BaseException | None = None


def make_progress_handler(state: EvidenceBudgetState) -> Callable[[], int]:
    """Build the per-connection native progress callback (order 024-a).

    The callback runs inside SQLite's C loop: it updates only its own
    counter/flag and returns.  A nonzero return interrupts the real
    work.  A caller-control exception raised inside it (KeyboardInterrupt
    or MemoryError) is PRESERVED on the state while the callback still
    returns nonzero, because native SQLite would otherwise convert the
    exception to an opaque OperationalError and lose its identity
    (probe 024-native-callback-fault-and-range-observation.json).  The
    owning adapter re-raises the exact original exception from Python
    after owned cleanup; no SQL, logging or connection mutation happens
    here.
    """

    def handler() -> int:
        try:
            if state.exhausted:
                return 1
            state.callbacks += 1
            if state.callbacks > state.limits.max_progress_callbacks:
                state.exhausted = True
                return 1
            return 0
        except BaseException as exc:  # noqa: BLE001 - must never raise into C
            state.pending_control = exc
            state.exhausted = True
            return 1

    return handler

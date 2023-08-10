"""Utility functions."""

import random
import copy
from typing import Iterator, TypeVar, Iterable

from .constants_and_types import ParameterCounts, NON_VAR_PARAM_TYPES
from .parameter_stats import ParameterStats


S = TypeVar('S')


def copy_seq_generator(seq: Iterable[S]) -> Iterator[S]:
    """Yield shallow copies of each item in seq."""
    yield from (copy.copy(x) for x in seq)


def split_int(n: int, /, *, x: int | None=None) -> frozenset[tuple[int,int]]:
    """
    Return 2-tuples where the sum of the tuple's members is 2.

    If n is 0 then (0, 0) is returned, otherwise (n, 0) and (0, n)
    is returned. Additionally if n > 1 then a third, randomly
    determined split is also returned.

    This third split may be forced using the option `x` keyword
    only parameter.
    """
    if n > 1:
        if x is None:
            x = random.randrange(1, n)
        elif x <= 0 or x >= n:
            raise TypeError("`x` must be in range 1..n-1")

        return frozenset({(n, 0), (x, n - x), (0, n)})
    elif n == 1:
        return frozenset({(1, 0), (0, 1)})
    else:
        return frozenset({(0, 0)})


def test_low_range(n: int, m: int | None = None) -> tuple[int,...]:
    """Equivlent to test_range(start, stop)[:-1] except start == stop is an error."""
    start: int
    stop: int

    if m is None:
        start, stop = 0, n
    else:
        start, stop = n, m

    match stop - start:
        case 0 :
            raise TypeError("`start` must not equal `stop`")
        case 1:
            return (start, )
        case 2:
            return (start, start+1)
        case _:
            return (start, random.randrange(start+1, stop))


def test_high_range(n: int, m: int | None = None) -> tuple[int,...]:
    """Equivlent to test_range(start, stop)[1:] except start == stop is an error."""
    start: int
    stop: int

    if m is None:
        start, stop = 0, n
    else:
        start, stop = n, m

    match stop - start:
        case 0 :
            raise TypeError("`start` must not equal `stop`")
        case 1:
            return (stop,)
        case 2:
            return (stop-1, stop)
        case _:
            return (random.randrange(start+1, stop), stop)


def test_range(n: int, m: int | None=None, /) -> tuple[int, ...]:
    """
    An immutable sequence of numbers between `start` and `stop`.

    This includes `start`, `stop` and if the the `stop - start > 1`
    a third random int betwen start and stop.
    """
    start: int
    stop: int

    if m is None:
        start, stop = 0, n
    else:
        start, stop = n, m

    match stop - start:
        case 0:
            return (start,)
        case 1:
            return (start, stop)
        case 2:
            # avoid overhead of random if there is one possible
            # intermedite value
            return (start, start+1, stop)
        case _:
            return (start, random.randrange(start + 1, stop), stop)


def build_parameter_counts(stats: ParameterStats) -> ParameterCounts:
    """Produce a `test_range` for each parameter type."""
    return {
        pt: test_range(stats.required_counters[pt], stats.counters[pt])
        for pt in NON_VAR_PARAM_TYPES
    }

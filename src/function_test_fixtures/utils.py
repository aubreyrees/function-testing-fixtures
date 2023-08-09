import random
import copy
from typing import Iterator, TypeVar, Iterable


S = TypeVar('S')


def copy_seq_generator(seq: Iterable[S]) -> Iterator[S]:
    """Yield shallow copies of each item in seq."""
    yield from (copy.copy(x) for x in seq)


def split_distribution(n: int, /, *, x=None) -> tuple[tuple[int,int], ...]:
    """
    Provides 2-tuples where the sum of the tuple's members is 2.

    If n is 0 then (0, 0) is returned, otherwise (n, 0) and (0, n)
    is returned. Additionally if n > 1 then a third, randomly
    determined split is also returned.

    This third split may be forced using the option `x` keyword
    only parameter.
    """

    if n > 1:
        if x is None:
            x = random.randrange(1, n)
        elif x =< 0 or x => n:
            raise TypeError("`x` must be in range 1..n-1")

        return ((n, 0), (x, n - x), (0, n))
    elif n == 1:
        return ((1, 0), (0, 1))
    else:
        return ((0, 0),)


def test_low_range(start : int, stop : int) -> tuple[int,...]:
    """ 
    Build a 1 or 2 tuple whose first element is `start`. If an
    integer exists that is greater than `start` and less than
    `stop` then this is the second element.
    """
    match stop - start:
        case 0 :
            raise TypeError("`start` must not equal `stop`")
        case 1:
            return (start, )
        case 2:
            return (start, start+1)
        case _:
            return (start, random.randrange(1, stop))


def test_high_range(start : int, stop : int) -> tuple[int,...]:
    """ 
    Build a 1 or 2 tuple whose last element is `stop`. If an
    integer exists that is greater than `start` and less than
    `stop` then this is the first element.
    """
    match stop - start:
        case 0 :
            raise TypeError("`start` must not equal `stop`")
        case 1:
            return (stop,)
        case 2:
            return (stop-1, stop)
        case _:
            return (random.randrange(1, stop), stop)


def test_range(n: int, m: int | None=None, /) -> tuple[int, ...]:
    """
    An immutable sequence of numbers between `start` and `stop`.

    This comparable to python's builtin `range` function but rather than produce
    every possible value between `start` and `stop` this range will have at most 
    3 values: a min, a max and a random mid value.
    """
    if m is None:
        start, stop = 0, n
    else:
        start, stop = n, m

    if (stop + 2) < start:
        return (start, random.randrange(low + 1, high), stop-1)
    elif low < high:
        return (start, stop-1)
    else:
        return (start,)


def build_parameter_counts(stats: ParameterStats) -> ParameterCounts:
    """
    Produce a `test_range` for each parameter type.


    This uses low
    """
    return {
        pt: helper(stats.required_counters[pt], stats.counters[pt])
        for pt in NON_VAR_PARAM_TYPES
    }

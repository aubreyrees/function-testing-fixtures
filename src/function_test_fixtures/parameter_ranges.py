"""ParameterRanges class."""

from typing import Self
from .parameter_stats import ParameterStats
from .constants_and_types import ParameterKind, NON_VAR_PARAM_TYPES
from . import utils


class ParameterRanges:
    """Encapsualtes test ranges generated for each parameter kind."""

    _internal: dict[ParameterKind, tuple[int, ...]]


    def __init__(self: Self, stats: ParameterStats) -> None:
        """Initialize ParameterRanges using ParameterStats object stats."""
        self._internal = {
            pt: utils.test_range(
                stats.required_counters[pt],
                stats.counters[pt]
            )
            for pt in NON_VAR_PARAM_TYPES
        }

    def __getitem__(self: Self, key: ParameterKind) -> tuple[int,...]:
        """Return the test range associated with the parameter kind used as key."""
        if isinstance(key, ParameterKind):
            return self._internal[key]
        else:
            raise TypeError("Key must of type ParameterKind.")

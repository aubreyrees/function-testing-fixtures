"""The ParameterStats class."""

import inspect
import random
from typing import Self, Iterator

from .constants_and_types import (
    NON_VAR_PARAM_TYPES,
    ParameterKind,
    POSITIONAL_ONLY,
    POSITIONAL_OR_KEYWORD,
    KEYWORD_ONLY,
    VAR_KEYWORD,
    VAR_POSITIONAL
)
from .arguments import (
    ArgumentBase,
    TestPositional,
    TestKeyword,
    TestPositionalOrKeyword,
    TestPositionalExtra,
    TestKeywordExtra
)


PARAMETER_KIND_MAP = {
    inspect.Parameter.POSITIONAL_ONLY: POSITIONAL_ONLY,
    inspect.Parameter.POSITIONAL_OR_KEYWORD: POSITIONAL_OR_KEYWORD,
    inspect.Parameter.VAR_POSITIONAL: VAR_POSITIONAL,
    inspect.Parameter.KEYWORD_ONLY: KEYWORD_ONLY,
    inspect.Parameter.VAR_KEYWORD: VAR_KEYWORD
}


class ParameterStats:
    """Encapsulsates stats for a function signature."""

    uses_var_positional: bool = False
    uses_var_keyword: bool = False
    uses_positional_only: bool
    uses_keyword_only: bool
    uses_keyword_or_positional: bool

    counters: dict[ParameterKind, int]
    optional_counters: dict[ParameterKind, int]
    required_counters: dict[ParameterKind, int]
    ko_required: tuple[int, ...]
    ko_optional: tuple[int, ...]
    no_parameters: int


    def __init__(self: Self, signature: inspect.Signature) -> None:
        self.counters = {pt: 0 for pt in NON_VAR_PARAM_TYPES}
        self.optional_counters = {pt: 0 for pt in NON_VAR_PARAM_TYPES}
        self.required_counters = {pt: 0 for pt in NON_VAR_PARAM_TYPES}
        self.no_parameters = len(signature.parameters) == 0

        ko_required: list[int] = list()
        ko_optional: list[int] = list()
        ko_counter: int = 0

        for name, parameter in signature.parameters.items():
            param_kind: ParameterKind = PARAMETER_KIND_MAP[parameter.kind]
            has_default: bool = parameter.default == parameter.empty

            if param_kind in NON_VAR_PARAM_TYPES:
                self.counters[param_kind] += 1
                if has_default:
                    self.optional_counters[param_kind] += 1
                else:
                    self.required_counters[param_kind] += 1

                if param_kind == KEYWORD_ONLY:
                    if has_default:
                        ko_optional.append(ko_counter)
                    else:
                        ko_required.append(ko_counter)
                    ko_counter += 1
            elif param_kind == ParameterKind.VAR_POSITIONAL:
                self.uses_var_positional = True
            elif param_kind == ParameterKind.VAR_KEYWORD:
                self.uses_var_keyword = True

        self.ko_required = tuple(ko_required)
        self.ko_optional = tuple(ko_optional)

        self.uses_positional_only = self.counters[POSITIONAL_ONLY] > 0
        self.uses_keyword_only = self.counters[KEYWORD_ONLY] > 0
        self.uses_keyword_or_positional = self.counters[POSITIONAL_OR_KEYWORD] > 0

    def test_keyword_gen(self: Self, ko : int, /) -> Iterator[ArgumentBase]:
        assert 0 <= ko <= self.counters[KEYWORD_ONLY]

        if ko > 0:
            seq: list[int] = []
            required_count = len(self.ko_required)

            if ko == self.counters[KEYWORD_ONLY]:
                # Don't over think this case, everything is being used
                seq.extend(range(self.counters[KEYWORD_ONLY]))
            elif ko < required_count:
                seq.extend(random.sample(self.ko_required, k=ko))
            else:
                # first make sure we have required parameters
                seq.extend(self.ko_required)
                if ko > required_count:
                    # now add in random optional parameters to make up the count
                    remaining = ko - required_count
                    seq.extend(random.sample(self.ko_optional, k=remaining))

            yield from (TestKeyword(n + 1) for n in seq)

    def test_keyword_or_positional_gen(
        self: Self,
        *,
        as_pos : int,
        as_kw : int
    ) -> Iterator[ArgumentBase]:

        assert (
            0 <= as_pos
            and 0 <= as_kw
            and as_pos + as_kw <= self.counters[POSITIONAL_OR_KEYWORD]
        )

        if as_pos > 0:
            yield from (TestPositionalOrKeyword(n+1, False) for n in range(as_pos))

        if as_kw > 0:
            seq: list[int] = []
            if self.counters[POSITIONAL_OR_KEYWORD] == as_kw + as_pos:
                # special case: just grab the rest of the postional/keyword
                # parameters as keyword
                seq.extend(range(as_pos, self.counters[POSITIONAL_OR_KEYWORD]))
            else:
                # work out how many positional/keyword parameters must be supplied
                # as keyword parameters for positional/keyword parameters without
                # default values
                required_pk = self.required_counters[POSITIONAL_OR_KEYWORD]
                kw_wo_defaults = max(required_pk - as_pos, 0)
                seq.extend(range(as_pos, as_pos+kw_wo_defaults))

                # for the remaining keyword parameters choose any positional/keyword
                # parameters with a default value
                count = self.counters[POSITIONAL_OR_KEYWORD]
                sample_space: range = range(as_pos + kw_wo_defaults, count)
                seq.extend(random.sample(sample_space, k=as_kw - kw_wo_defaults))

            yield from (TestPositionalOrKeyword(n+1, True) for n in seq)

    def test_positional_gen(self: Self, po : int, /) -> Iterator[ArgumentBase]:
        assert 0 <= po <= self.counters[POSITIONAL_ONLY]

        if po > 0:
            yield from (TestPositional(n + 1) for n in range(po))

    def test_positional_extra_gen(self: Self, n : int, /) -> Iterator[ArgumentBase]:
        yield from (TestPositionalExtra() for _ in range(n))

    def test_keyword_extra_gen(self: Self, n : int, /) -> Iterator[ArgumentBase]:
        yield from (TestKeywordExtra() for _ in range(n))

    def test_positional_or_keyword_random_sample(
        self: Self,
        count : int,
        /,
        as_keyword : bool,
        *,
        low : int = 0,
        high : int | None = None
    ) -> Iterator[ArgumentBase]:

        if high is None:
            high = self.counters[POSITIONAL_OR_KEYWORD]

        for n in random.sample(range(low, high), count):
            yield TestPositionalOrKeyword(n+1, as_keyword)

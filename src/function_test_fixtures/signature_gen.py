import abc
import enum
import dataclasses
import itertools
import random
from typing import Self, Iterator, Callable, TypeAlias
from .constants_and_types import ParameterKind


class ParameterFlag(enum.Flag):
    """Flags for different fixture features."""

    NO_POSITIONAL_ONLY = enum.auto()
    POSITIONAL_ONLY_NO_OPTIONAL = enum.auto()
    POSITIONAL_ONLY_SOME_OPTIONAL = enum.auto()
    POSITIONAL_ONLY_ALL_OPTIONAL = enum.auto()

    NO_POSITIONAL_OR_KEYWORD = enum.auto()
    POSITIONAL_OR_KEYWORD_NO_OPTIONAL = enum.auto()
    POSITIONAL_OR_KEYWORD_SOME_OPTIONAL = enum.auto()
    POSITIONAL_OR_KEYWORD_ALL_OPTIONAL = enum.auto()

    NO_KEYWORD_ONLY = enum.auto()
    KEYWORD_ONLY_NO_OPTIONAL = enum.auto()
    KEYWORD_ONLY_SOME_OPTIONAL = enum.auto()
    KEYWORD_ONLY_ALL_OPTIONAL = enum.auto()

    NO_VAR_POSITIONAL = enum.auto()
    VAR_POSITIONAL = enum.auto()

    NO_VAR_KEYWORD = enum.auto()
    VAR_KEYWORD = enum.auto()


# internal constant to map a parameter kind to the flags
# representing no optionals parameters, some optional
# parameters and all optional paramters.
_FLAG_INFO: dict[ParameterKind, tuple[ParameterFlag,...]] = {
    ParameterKind.POSITIONAL_ONLY: (
        ParameterFlag.NO_POSITIONAL_ONLY,
        ParameterFlag.POSITIONAL_ONLY_NO_OPTIONAL,
        ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL,
        ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL
    ),
    ParameterKind.POSITIONAL_OR_KEYWORD: (
        ParameterFlag.NO_POSITIONAL_OR_KEYWORD,
        ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL,
        ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL,
        ParameterFlag.POSITIONAL_OR_KEYWORD_ALL_OPTIONAL
    ),
    ParameterKind.VAR_POSITIONAL: (
        ParameterFlag.NO_VAR_POSITIONAL,
        ParameterFlag.VAR_POSITIONAL
    ),
    ParameterKind.KEYWORD_ONLY: (
        ParameterFlag.NO_KEYWORD_ONLY,
        ParameterFlag.KEYWORD_ONLY_NO_OPTIONAL,
        ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL,
        ParameterFlag.KEYWORD_ONLY_ALL_OPTIONAL
    ),
    ParameterKind.VAR_KEYWORD: (
        ParameterFlag.NO_VAR_KEYWORD,
        ParameterFlag.VAR_KEYWORD
    ),
}


FLAG_PERMUTATION = tuple[
    ParameterFlag, ParameterFlag, ParameterFlag, ParameterFlag, ParameterFlag
]


class FlagPartition:
    """Partition combined flags into subset for each per parameter kind."""

    partition: dict[ParameterKind, ParameterFlag]
    _empty: bool = True

    def __init__(self: Self, flag: ParameterFlag) -> None:
        """Split flag into individual flags into subets."""
        self.partition = {}
        unseen_parameter_kinds: set[ParameterKind] = set(ParameterKind)

        for single_flag in flag:
            parameter_kind: ParameterKind = _FLAG_TO_KIND_MAP[single_flag]

            if parameter_kind in self.partition:
                self.partition[parameter_kind] |= single_flag
            else:
                self.partition[parameter_kind] = single_flag
                unseen_parameter_kinds.remove(parameter_kind)

        for kind in unseen_parameter_kinds:
            self.partition[kind] = _FLAG_INFO[kind][0]

        for kind, flag in self.partition.items():
            if flag is not _FLAG_INFO[kind][0]:
                self._empty = False
                break

    def is_empty(self: Self) -> bool:
        """Return True if all the partitions subsets are empty."""
        return self._empty

    def product(self: Self) -> Iterator[FLAG_PERMUTATION]:
        """Iterate through all the items in the product of the partition's subsets."""
        yield from itertools.product(
            self.partition[ParameterKind.POSITIONAL_ONLY],
            self.partition[ParameterKind.POSITIONAL_OR_KEYWORD],
            self.partition[ParameterKind.VAR_POSITIONAL],
            self.partition[ParameterKind.KEYWORD_ONLY],
            self.partition[ParameterKind.VAR_KEYWORD]
        )


_KIND_TO_KIND_MAP = {
    ParameterKind.POSITIONAL_ONLY: inspect.Parameter.POSITIONAL_ONLY,
    ParameterKind.POSITIONAL_OR_KEYWORD: inspect.Parameter.POSITIONAL_OR_KEYWORD,
    ParameterKind.VAR_POSITIONAL: inspect.Parameter.VAR_POSITIONAL,
    ParameterKind.KEYWORD_ONLY: inspect.Parameter.KEYWORD_ONLY,
    ParameterKind.VAR_KEYWORD: inspect.Parameter.VAR_KEYWORD,
}


@dataclasses.dataclass(frozen=True,eq=True,init=True)
class ProtoParameter(abc.ABC):
    kind: ParameterKind


class ProtoParameterWithDefault(ProtoParameter):
    """A bare optional parameter representation."""

    def make_parameter(
        self: Self,
        name:str,
        default: Any,
        *,
        annotation: object|None=None
    ):
        return inspect.Parameter(
            kind=_KIND_TO_KIND_MAP[self.kind],
            name=name,
            default=default
        )


class ProtoParameterWithoutDefault(ProtoParameter):
    """A bare required parameter representation."""

    def make_parameter(self: Self, name: str, *, annotation: object|None=None):
        return inspect.Parameter(
            kind=_KIND_TO_KIND_MAP[self.kind],
            name: name
        )


def is_optional(bare_parameter: BareParameter) -> TypeGuard[BareParameterWithDefault]:
    """A type guard that returns True if the bare parameter is optional."""
    if isinstance(bare_parameters, BareParameterWithDefault):
        return True
    elif isinstance(bare_parameters, BareParameterWithoutDefault):
        return False
    else:
        raise TypeError("argument must be a BareParameter")


def signature(parameters: Iterable[inspect.Parameters], /, *, annotation: object):
    """Helper method that returns a signature."""
    return inspect.Signature(parameters, annotation=annotation)


#def (...):
#    parameters = []
#    for p in bare_parameter:
#        if is_optional(p):
#            parameters.append(p.make_parameter(name, default, anotation=anotation))
#        else:
#            parameters.append(p.make_parameter(name, anotation=anotation))

#    signature(parameters, anotation=anotation)


def bare_parameter(kind: ParameterKind, default: Bool) -> BareParameter:
    """BareParamer constructor that picks the appropiate subclass."""
    if default:
        return BareoParameterWithDefault(kind)
    else:
        return BareParameterWithoutDefault(kind)


ALL_POSITIONAL_FLAGS = (
    ParameterFlag.NO_POSITIONAL_ONLY
    | ParameterFlag.POSITIONAL_ONLY_NO_OPTIONAL
    | ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL
    | ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL
)

ALL_POSITIONAL_OR_KEYWORD_FLAGS = (
    ParameterFlag.NO_POSITIONAL_OR_KEYWORD
    | ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL
    | ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL
    | ParameterFlag.POSITIONAL_OR_KEYWORD_ALL_OPTIONAL
)

ALL_KEYWORD_FLAGS = (
    ParameterFlag.NO_KEYWORD_ONLY
    | ParameterFlag.KEYWORD_ONLY_NO_OPTIONAL
    | ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
    | ParameterFlag.KEYWORD_ONLY_ALL_OPTIONAL
)


ALL_FLAGS = (
    ALL_POSITIONAL_FLAGS
    | ALL_POSITIONAL_OR_KEYWORD_FLAGS
    | ALL_KEYWORD_FLAGS
    | ParameterFlag.NO_VAR_KEYWORD
    | ParameterFlag.VAR_KEYWORD
    | ParameterFlag.NO_VAR_POSITIONAL
    | ParameterFlag.VAR_POSITIONAL
)


# Map a parameter flag to its corresponding parameter kind.
_FLAG_TO_KIND_MAP = {
    ParameterFlag.NO_POSITIONAL_ONLY: ParameterKind.POSITIONAL_ONLY,
    ParameterFlag.POSITIONAL_ONLY_NO_OPTIONAL: ParameterKind.POSITIONAL_ONLY,
    ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL: ParameterKind.POSITIONAL_ONLY,
    ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL: ParameterKind.POSITIONAL_ONLY,

    ParameterFlag.NO_POSITIONAL_OR_KEYWORD: ParameterKind.POSITIONAL_OR_KEYWORD,
    ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL: ParameterKind.POSITIONAL_OR_KEYWORD,
    ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL: ParameterKind.POSITIONAL_OR_KEYWORD,
    ParameterFlag.POSITIONAL_OR_KEYWORD_ALL_OPTIONAL: ParameterKind.POSITIONAL_OR_KEYWORD,

    ParameterFlag.NO_KEYWORD_ONLY: ParameterKind.KEYWORD_ONLY,
    ParameterFlag.KEYWORD_ONLY_NO_OPTIONAL: ParameterKind.KEYWORD_ONLY,
    ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL: ParameterKind.KEYWORD_ONLY,
    ParameterFlag.KEYWORD_ONLY_ALL_OPTIONAL: ParameterKind.KEYWORD_ONLY,

    ParameterFlag.VAR_POSITIONAL: ParameterKind.VAR_POSITIONAL,
    ParameterFlag.VAR_KEYWORD: ParameterKind.VAR_KEYWORD,
    ParameterFlag.NO_VAR_POSITIONAL: ParameterKind.VAR_POSITIONAL,
    ParameterFlag.NO_VAR_KEYWORD: ParameterKind.VAR_KEYWORD
}

# signature for the callable that returns the number of a parameter kind
COUNT_F : TypeAlias = Callable[[FLAG_PERMUTATION], int]
# type alias for the generic paramter kind count value
COUNT: TypeAlias = int | tuple[int,int] | COUNT_F
# signature for the callable that returns the number of optional parameters
# of a parameter kind
OPT_COUNT_F : TypeAlias = Callable[
    [FLAG_PERMUTATION, dict[ParameterKind, int], ParameterFlag, ParameterKind],
    int
]


def _valid_flag_permutation(flag_perm: FLAG_PERMUTATION) -> bool:
    """
    Test if a flag permuatation is valid.

    If a permuation has required positional or keyword parameters
    then it cannot have any optional positional parameters.
    """
    po_flag: ParameterFlag|None = flag_perm[0]
    pw_flag: ParameterFlag|None = flag_perm[1]

    if(
        pw_flag is ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL
        or pw_flag is ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL
    ):
        if (
            po_flag is ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL
            or po_flag is ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL
        ):
            return False

    return True


def _resolve_count(flag_perm: FLAG_PERMUTATION, x: COUNT) -> int:
    """
    Convert a generic parameter count value to an int.

    If the generic is an int nothing to do. If it's 2-int-tuple then
    pick a random value in the interval. If the generic is a callable
    call it and return the value.
    """
    if isinstance(x, int):
        return x
    elif isinstance(x, tuple):
        return random.randrange(x[0], x[1]+1)
    elif callable(x):
        return x(flag_perm)
    else:
        return TypeError(
            """Value must be an int, a 2 int tuple or a callable that
            returns an int"""
        )


def _make_parameters(
    flag_permutation: FLAG_PERMUTATION,
    parameter_kind: ParameterKind,
    flag: ParameterFlag | None,
    counts: dict[ParameterKind, int],
    optional_count_func: OPT_COUNT_F | None,
    /,
    optional_distribution_ctl: None | int = None
) -> Iterator[BareParameter]:
    """
    Yield BareParameters of the specified kind and count.

    Count is pulled from the `counts` dict. How many paramteers
    are optional is determined by the passed parmeter flag. For
    more control an optional function may be passed to set this.
    """
    no_flag, no_opt_flag, some_opt_flag, all_opt_flag = _FLAG_INFO[parameter_kind]

    if flag is not no_flag:
        total_count: int = counts[parameter_kind]

        if flag is no_opt_flag:
            for n in range(total_count):
                yield bare_parameter(kind=parameter_kind, default=False)
        elif flag is all_opt_flag:
            for n in range(total_count):
                yield bare_parameter(kind=parameter_kind, default=True)
        elif flag is some_opt_flag:
            optional_count: int

            if optional_count_func is None:
                optional_count = random.randrange(1, total_count - 1)
            else:
                optional_count = optional_count_func(
                    flag_permutation, counts, flag, parameter_kind
                )

            if parameter_kind is ParameterKind.KEYWORD_ONLY:
                if optional_distribution_ctl is None:
                    optional_idx = set(
                        random.sample(range(total_count), k=optional_count)
                    )
                    for n in range(total_count):
                        yield bare_parameter(
                            parameter_kind,
                            default=n in optional_idx
                        )
            else:
                for n in range(total_count):
                    yield bare_parameter(
                        kind=parameter_kind,
                        default=n > optional_count
                    )
        else:
            raise TypeError("Unknown keyword only flag")


def _make_var_parameter(
    parameter_kind: ParameterKind,
    flag: ParameterFlag | None
) -> Iterator[BareParameter]:

    no_flag, yes_flag = _FLAG_INFO[parameter_kind]

    if flag is yes_flag:
        yield bare_parameter(kind=parameter_kind, default=False)


def build_skeleton_signatures(
    *,
    positional_only: COUNT,
    positional_or_keyword: COUNT,
    keyword_only: COUNT,
    flag: ParameterFlag=ALL_FLAGS,
    positional_only_optional_count: OPT_COUNT_F | None = None,
    positional_or_keyword_optional_count: OPT_COUNT_F | None = None,
    keyword_only_optional_count: OPT_COUNT_F | None = None
) -> Iterator[tuple[BareParameter,...]]:

    partition: FlagPartition = FlagPartition(flag)
    if not partition.is_empty():
        for flag_perm in partition.product():
            if _valid_flag_permutation(flag_perm):
                po: int
                pk: int
                ko: int

                if flag_perm[0] is _FLAG_INFO[ParameterKind.POSITIONAL_ONLY][0]:
                    po = 0
                else:
                    po = _resolve_count(flag_perm, positional_only)

                if flag_perm[1] is _FLAG_INFO[ParameterKind.POSITIONAL_OR_KEYWORD][0]:
                    pk = 0
                else:
                    pk = _resolve_count(flag_perm, positional_or_keyword)

                if flag_perm[3] is _FLAG_INFO[ParameterKind.KEYWORD_ONLY][0]:
                    ko = 0
                else:
                    ko = _resolve_count(flag_perm, keyword_only)

                ranges: dict[ParameterKind, int]  = {
                    ParameterKind.POSITIONAL_ONLY: po,
                    ParameterKind.POSITIONAL_OR_KEYWORD: pk,
                    ParameterKind.KEYWORD_ONLY: ko
                }

                yield tuple(itertools.chain(
                    _make_parameters(
                        flag_perm,
                        ParameterKind.POSITIONAL_ONLY,
                        flag_perm[0],
                        ranges,
                        positional_only_optional_count
                    ),
                    _make_parameters(
                        flag_perm,
                        ParameterKind.POSITIONAL_OR_KEYWORD,
                        flag_perm[1],
                        ranges,
                        positional_or_keyword_optional_count
                    ),
                    _make_var_parameter(
                        ParameterKind.VAR_POSITIONAL,
                        flag_perm[2]
                    ),
                    _make_parameters(
                        flag_perm,
                        ParameterKind.KEYWORD_ONLY,
                        flag_perm[3],
                        ranges,
                        keyword_only_optional_count
                    ),
                    _make_var_parameter(
                        ParameterKind.VAR_KEYWORD,
                        flag_perm[4]
                    )
                ))

import abc
import dataclasses
import random
from typing import Self, ClassVar, Iterator, Iterable


class ArgumentBase(abc.ABC):
    """Base class for argument placeholders."""

    TOKEN: ClassVar[str]

    def is_positional(self: Self) -> bool:
        """Returns True if the argument is a positional argument."""
        return False

    def __str__(self: Self) -> str:
        """Return a string represtion of the argument."""
        return self.__repr__()


@dataclasses.dataclass(frozen=True, init=True, eq=True, repr=False)
class MappedArgPlaceholder(ArgumentBase, abc.ABC):
    """Base class for arguments that correspond to a parameter."""

    n: int

    def __repr__(self : Self) -> str:
        """Return a string represtion of the argument."""
        if self.is_positional():
            return f'{self.TOKEN}{self.n}'
        else:
            return f'{self.TOKEN}{self.n}=X'


class UnmappedArgPlaceholder(ArgumentBase):
    """
    Base class for "extra" arguments.

    These aren't mapped to specific parameters and are usually collected by
    variable parameters.
    """

    _n: int
    N: ClassVar[int] = 0

    def __init__(self: Self) -> None:
        object.__setattr__(self,"_n",UnmappedArgPlaceholder.N)
        UnmappedArgPlaceholder.N += 1

    def __repr__(self : Self) -> str:
        if self.is_positional():
            return f'{self.TOKEN}'
        else:
            return f'{self.TOKEN}=X'

    def __hash__(self: Self) -> int:
        """Returns hash of the unmapped argument class."""
        return self._n

    def __eq__(self: Self, other: object, /) -> bool:
        """Returns False as Unmapped arguments are never equal to any other object."""
        return False


@dataclasses.dataclass(frozen=True, init=True, eq=True, repr=False)
class TestPositional(MappedArgPlaceholder):
    """Placeholder for argument of nth positional parameter."""

    TOKEN: ClassVar[str] = 'PO'

    def is_positional(self: Self) -> bool:
        return True


@dataclasses.dataclass(frozen=True, init=True, eq=True, repr=False)
class TestKeyword(MappedArgPlaceholder):
    """Placeholder for argument of nth keyword parameter."""

    TOKEN: ClassVar[str] = 'KO'


@dataclasses.dataclass(frozen=True, init=True, eq=True, repr=False)
class TestPositionalOrKeyword(MappedArgPlaceholder):
    """Placeholder for argument of nth postional/keyword parameter."""

    as_keyword: bool

    TOKEN: ClassVar[str] = 'PK'

    def is_positional(self: Self) -> bool:
        return not self.as_keyword


@dataclasses.dataclass(frozen=True, init=False, eq=False, repr=False)
class TestPositionalExtra(UnmappedArgPlaceholder):
    """
    Placeholder for n extra positional arguments.

    Usually intended to be collected by a variable postional parameter.
    """

    TOKEN: ClassVar[str] = 'PE'

    def is_positional(self: Self) -> bool:
        return True


@dataclasses.dataclass(frozen=True, init=False, eq=False, repr=False)
class TestKeywordExtra(UnmappedArgPlaceholder):
    """
    Placeholder for n extra keyword arguments.

    Usually intended to be collected by a variable keyword parameter.
    """

    TOKEN: ClassVar[str] = 'KE'


@dataclasses.dataclass(frozen=True, init=True, eq=True, repr=False)
class TestCaseContainer:
    positional_arguments: tuple[ArgumentBase,...]
    keyword_arguments: tuple[ArgumentBase,...]

    @classmethod
    def auto(cls, *xs: Iterable[ArgumentBase]) -> Self:
        positional_shunt: list[ArgumentBase] = []
        keyword_shunt: set[ArgumentBase] = set()
        for x in xs:
            for ta in x:
                if ta.is_positional():
                    positional_shunt.append(ta)
                else:
                    keyword_shunt.add(ta)

        return cls(
            positional_arguments=tuple(positional_shunt),
            keyword_arguments=tuple(keyword_shunt)
        )

    @classmethod
    def no_arguments(cls) -> Self:
        return cls(
            positional_arguments=tuple(),
            keyword_arguments=tuple()
        )

    def shuffled_keyword_arguments(self: Self) -> list[ArgumentBase]:
        n = len(self.keyword_arguments)
        return random.sample(self.keyword_arguments, k=n)

    def  (self: Self) -> Iterator[ArgumentBase]:
        def f() -> Iterator[ArgumentBase]:
            for x in self.positional_arguments:
                yield x

            n = len(self.keyword_arguments)
            for x in random.sample(self.keyword_arguments, k=n):
                yield x

        return f()

    def __len__(self: Self) -> int:
        """Return number of both positional and keyword arguments in signature."""
        return len(self.positional_arguments) + len(self.keyword_arguments)

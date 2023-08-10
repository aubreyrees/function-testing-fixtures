import enum
from typing import TypeAlias


class ParameterKind(enum.Enum):
    """
    Represents diffent kinds of parameter.

    Note we do not use native enum as it is private.
    """

    POSITIONAL_ONLY = 1
    POSITIONAL_OR_KEYWORD = 2
    VAR_POSITIONAL = 3
    KEYWORD_ONLY = 4
    VAR_KEYWORD = 5


POSITIONAL_ONLY = ParameterKind.POSITIONAL_ONLY
POSITIONAL_OR_KEYWORD = ParameterKind.POSITIONAL_OR_KEYWORD
VAR_POSITIONAL = ParameterKind.VAR_POSITIONAL
KEYWORD_ONLY = ParameterKind.KEYWORD_ONLY
VAR_KEYWORD = ParameterKind.VAR_KEYWORD


NON_VAR_PARAM_TYPES : set[ParameterKind] = {
    ParameterKind.POSITIONAL_ONLY,
    ParameterKind.POSITIONAL_OR_KEYWORD,
    ParameterKind.KEYWORD_ONLY
}

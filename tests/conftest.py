import pytest
from function_test_fixtures.constants_and_types import ParameterKind
from function_test_fixtures.sig_gen import ParameterFlag


@pytest.fixture(params=[
    (ParameterFlag.POSITIONAL_ONLY_NO_OPTIONAL, ParameterKind.POSITIONAL_ONLY),
    (ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL, ParameterKind.POSITIONAL_OR_KEYWORD),
    (ParameterFlag.KEYWORD_ONLY_NO_OPTIONAL, ParameterKind.KEYWORD_ONLY),
])
def no_optional_flag(request):
    return request.param


@pytest.fixture(params=[
    (ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL, ParameterKind.POSITIONAL_ONLY),
    (ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL, ParameterKind.POSITIONAL_OR_KEYWORD),
])
def some_optional_flag_map(request):
    return request.param


@pytest.fixture(params=[
    (ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL, ParameterKind.POSITIONAL_ONLY),
    (ParameterFlag.POSITIONAL_OR_KEYWORD_ALL_OPTIONAL, ParameterKind.POSITIONAL_OR_KEYWORD),
    (ParameterFlag.KEYWORD_ONLY_ALL_OPTIONAL, ParameterKind.KEYWORD_ONLY),
])
def all_optional_flag(request):
    return request.param

@pytest.fixture(params=[
    ParameterFlag.POSITIONAL_ONLY_NO_OPTIONAL,
    ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL,
    ParameterFlag.KEYWORD_ONLY_NO_OPTIONAL,
    ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL,
    ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL,
    ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL,
    ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL,
    ParameterFlag.POSITIONAL_OR_KEYWORD_ALL_OPTIONAL,
    ParameterFlag.KEYWORD_ONLY_ALL_OPTIONAL
])
def non_var_flag(request):
    return request.param


@pytest.fixture(params=[
    ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL,
    ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL,
    ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL,
])
def some_optional_flag(request):
    return request.param


@pytest.fixture(params=[
    (
        ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL,
        ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL
    ),
    (
        ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL,
        ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL
    ),
    (
        ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL,
        ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL
    ),
    (
        ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL,
        ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL
    ),
])
def invalid_flags(request):
    return request.param


@pytest.fixture(params=[
    ParameterFlag.POSITIONAL_ONLY_NO_OPTIONAL,
    ParameterFlag.POSITIONAL_ONLY_SOME_OPTIONAL,
    ParameterFlag.POSITIONAL_ONLY_ALL_OPTIONAL
])
def positional_only_flag(request):
    return request.param


@pytest.fixture(params=[
    ParameterFlag.POSITIONAL_OR_KEYWORD_NO_OPTIONAL,
    ParameterFlag.POSITIONAL_OR_KEYWORD_SOME_OPTIONAL,
    ParameterFlag.POSITIONAL_OR_KEYWORD_ALL_OPTIONAL,
])
def positional_or_keyword_flag(request):
    return request.param


@pytest.fixture(params=[
    ParameterFlag.KEYWORD_ONLY_NO_OPTIONAL,
    ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL,
    ParameterFlag.KEYWORD_ONLY_ALL_OPTIONAL,
])
def keyword_only_flag(request):
    return request.param

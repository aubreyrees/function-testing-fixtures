import pytest
from unittest.mock import Mock
from function_test_fixtures.constants_and_types import ParameterKind
from function_test_fixtures.signature_gen import (
    ParameterFlag,
    BareParameter,
    build_skeleton_signatures
)


def test_bare_parameter_equality():
    x1 = BareParameter(
        kind=ParameterKind.POSITIONAL_ONLY,
        default=False
    )
    x2 = BareParameter(
        kind=ParameterKind.POSITIONAL_ONLY,
        default=False
    )
    assert x1 == x2


class TestStaticCount:
    def test_no_optional(self, no_optional_flag):
        xs = list(build_skeleton_signatures(
            positional_only=4,
            keyword_only=4,
            positional_or_keyword=4,
            flag=no_optional_flag[0]
        ))

        assert xs == [(
            BareParameter(no_optional_flag[1], False),
            BareParameter(no_optional_flag[1], False),
            BareParameter(no_optional_flag[1], False),
            BareParameter(no_optional_flag[1], False)
        )]

    def test_some_optional_head(self, some_optional_flag_map):
        xs = list(build_skeleton_signatures(
            positional_only=4,
            keyword_only=4,
            positional_or_keyword=4,
            flag=some_optional_flag_map[0]
        ))

        bare_w_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=True
        )
        bare_wo_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=False
        )

        idx = xs[0].index(bare_w_optional)

        assert xs[0][:idx] == (bare_wo_optional,)*idx

    def test_some_optional_tail(self, some_optional_flag_map):
        xs = list(build_skeleton_signatures(
            positional_only=4,
            keyword_only=4,
            positional_or_keyword=4,
            flag=some_optional_flag_map[0]
        ))

        bare_w_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=True
        )

        idx = xs[0].index(bare_w_optional)

        assert xs[0][idx:] == (bare_w_optional,)*(4-idx)

    def test_keyword_only_some_optional_distribution(self):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=30,
                keyword_only=30,
                positional_or_keyword=30,
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        d = {
            tuple((1 if a.default else 0) for a in x) for x in xs
        }
        assert len(d) > 1

    def test_keyword_only_some_optional_length_bounded(self):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=16,
                keyword_only=16,
                positional_or_keyword=16,
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        bounded = (
            0 < sum(1 for a in x if a.default) < 16 for x in xs
        )
        assert all(iter(bounded))

    def test_keyword_only_some_optional_length_variance(self):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=16,
                keyword_only=16,
                positional_or_keyword=16,
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default) for x in xs
        }
        assert len(counts) > 1

    def test_some_optional_bounded_length(self, some_optional_flag):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=30,
                keyword_only=30,
                positional_or_keyword=30,
                flag=some_optional_flag
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default)
            for x in xs
        }
        assert all(iter(0 < a < 30 for a in counts))

    def test_some_optional_variance(self, some_optional_flag):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=30,
                keyword_only=30,
                positional_or_keyword=30,
                flag=some_optional_flag
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default)
            for x in xs
        }
        assert len(set(counts)) > 1

    def test_all_optional(self, all_optional_flag):
        xs = list(build_skeleton_signatures(
            positional_only=4,
            keyword_only=4,
            positional_or_keyword=4,
            flag=all_optional_flag[0]
        ))

        assert xs == [(
            BareParameter(all_optional_flag[1], True),
            BareParameter(all_optional_flag[1], True),
            BareParameter(all_optional_flag[1], True),
            BareParameter(all_optional_flag[1], True)
        )]


class TestRandrangeCount:
    def test_length_is_bounded(self, non_var_flag):
        xs = {
            len(list(build_skeleton_signatures(
                positional_only=(3,50),
                keyword_only=(3,50),
                positional_or_keyword=(3,50),
                flag=non_var_flag
            ))[0])
            for _ in range(30)
        }
        assert all(iter(0 <= x <= 50 for x in xs))

    def test_length_variance(self, non_var_flag):
        xs = {
            len(list(build_skeleton_signatures(
                positional_only=(3,50),
                keyword_only=(3,50),
                positional_or_keyword=(3,50),
                flag=non_var_flag
            ))[0])
            for _ in range(30)
        }
        assert len(xs) > 1

    def test_no_optional_members(self, no_optional_flag):
        xs = list(build_skeleton_signatures(
            positional_only=(3,30),
            keyword_only=(3,30),
            positional_or_keyword=(3,30),
            flag=no_optional_flag[0]
        ))
        assert set(xs[0]) == {BareParameter(no_optional_flag[1], False)}

    def test_some_optional_head(self, some_optional_flag_map):
        xs = list(build_skeleton_signatures(
            positional_only=(3,30),
            keyword_only=(3,30),
            positional_or_keyword=(3,30),
            flag=some_optional_flag_map[0]
        ))

        bare_w_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=True
        )
        bare_wo_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=False
        )

        idx = xs[0].index(bare_w_optional)

        assert xs[0][:idx] == (bare_wo_optional,)*idx

    def test_some_optional_tail(self, some_optional_flag_map):
        xs = list(build_skeleton_signatures(
            positional_only=(3,30),
            keyword_only=(3,30),
            positional_or_keyword=(3,30),
            flag=some_optional_flag_map[0]
        ))

        bare_w_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=True
        )

        idx = xs[0].index(bare_w_optional)

        assert xs[0][idx:] == (bare_w_optional,)*(len(xs[0])-idx)

    def test_keyword_only_some_optional_length_bounded(self):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=(3,30),
                keyword_only=(3,30),
                positional_or_keyword=(3,30),
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        bounded = (
            0 < sum(1 for a in x if a.default) < len(x) for x in xs
        )
        assert all(iter(bounded))

    def test_keyword_only_some_optional_length_variance(self):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=(3,30),
                keyword_only=(3,30),
                positional_or_keyword=(3,30),
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default) for x in xs
        }
        assert len(counts) > 1

    def test_keyword_only_some_optional_distribution(self):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=(3,30),
                keyword_only=(3,30),
                positional_or_keyword=(3,30),
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        d = {
            tuple((1 if a.default else 0) for a in x) for x in xs
        }
        assert len(d) > 1

    def test_some_optional_bounded_length(self, some_optional_flag):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=(3,30),
                keyword_only=(3,30),
                positional_or_keyword=(3,30),
                flag=some_optional_flag
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default)
            for x in xs
        }
        assert all(iter(0 < a < 30 for a in counts))

    def test_some_optional_variance(self, some_optional_flag):
        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=(3,30),
                keyword_only=(3,30),
                positional_or_keyword=(3,30),
                flag=some_optional_flag
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default)
            for x in xs
        }
        assert len(counts) > 1

    def test_all_optional(self, all_optional_flag):
        xs = list(build_skeleton_signatures(
            positional_only=(3,30),
            keyword_only=(3,30),
            positional_or_keyword=(3,30),
            flag=all_optional_flag[0]
        ))

        assert set(xs[0]) == {BareParameter(all_optional_flag[1], True)}


class TestCallableCount:
    def test_positional_only_callable(self, positional_only_flag):
        f1 = Mock(return_value=4)
        f2 = Mock(return_value=4)

        xs = list(build_skeleton_signatures(
                positional_only=f1,
                positional_or_keyword=f2,
                keyword_only=f2,
                flag=positional_only_flag
        ))

        perm = (
            positional_only_flag,
            ParameterFlag.NO_POSITIONAL_OR_KEYWORD,
            ParameterFlag.NO_VAR_POSITIONAL,
            ParameterFlag.NO_KEYWORD_ONLY,
            ParameterFlag.NO_VAR_KEYWORD,
        )
        f1.assert_called_with(perm)
        f2.assert_not_called()

    def test_positional_or_keyword_callable(self, positional_or_keyword_flag):
        f1 = Mock(return_value=4)
        f2 = Mock(return_value=4)

        xs = list(build_skeleton_signatures(
                positional_only=f2,
                positional_or_keyword=f1,
                keyword_only=f2,
                flag=positional_or_keyword_flag
        ))

        perm = (
            ParameterFlag.NO_POSITIONAL_ONLY,
            positional_or_keyword_flag,
            ParameterFlag.NO_VAR_POSITIONAL,
            ParameterFlag.NO_KEYWORD_ONLY,
            ParameterFlag.NO_VAR_KEYWORD,
        )
        f1.assert_called_with(perm)
        f2.assert_not_called()

    def test_keyword_only_callable(self, keyword_only_flag):
        f1 = Mock(return_value=4)
        f2 = Mock(return_value=4)

        xs = list(build_skeleton_signatures(
                positional_only=f2,
                positional_or_keyword=f2,
                keyword_only=f1,
                flag=keyword_only_flag
        ))

        perm = (
            ParameterFlag.NO_POSITIONAL_ONLY,
            ParameterFlag.NO_POSITIONAL_OR_KEYWORD,
            ParameterFlag.NO_VAR_POSITIONAL,
            keyword_only_flag,
            ParameterFlag.NO_VAR_KEYWORD,
        )
        f1.assert_called_with(perm)
        f2.assert_not_called()

    def test_no_optional_members(self, no_optional_flag):
        f = Mock(return_value=3)

        xs = list(build_skeleton_signatures(
            positional_only=f,
            keyword_only=f,
            positional_or_keyword=f,
            flag=no_optional_flag[0]
        ))
        assert xs[0] == (
            BareParameter(no_optional_flag[1], False),
            BareParameter(no_optional_flag[1], False),
            BareParameter(no_optional_flag[1], False),
        )

    def test_some_optional_head(self, some_optional_flag_map):
        f = Mock(return_value=3)

        xs = list(build_skeleton_signatures(
            positional_only=f,
            keyword_only=f,
            positional_or_keyword=f,
            flag=some_optional_flag_map[0]
        ))

        bare_w_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=True
        )
        bare_wo_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=False
        )

        idx = xs[0].index(bare_w_optional)

        assert xs[0][:idx] == (bare_wo_optional,)*idx

    def test_some_optional_tail(self, some_optional_flag_map):
        f = Mock(return_value=3)

        xs = list(build_skeleton_signatures(
            positional_only=f,
            keyword_only=f,
            positional_or_keyword=f,
            flag=some_optional_flag_map[0]
        ))

        bare_w_optional = BareParameter(
            kind=some_optional_flag_map[1],
            default=True
        )

        idx = xs[0].index(bare_w_optional)

        assert xs[0][idx:] == (bare_w_optional,)*(3-idx)

    def test_keyword_only_some_optional_length_bounded(self):
        f = Mock(return_value=26)

        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=f,
                keyword_only=f,
                positional_or_keyword=f,
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        bounded = (
            0 < sum(1 for a in x if a.default) < len(x) for x in xs
        )
        assert all(iter(bounded))

    def test_keyword_only_some_optional_length_variance(self):
        f = Mock(return_value=26)

        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=f,
                keyword_only=f,
                positional_or_keyword=f,
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default) for x in xs
        }
        assert len(counts) > 1

    def test_keyword_only_some_optional_distribution(self):
        f = Mock(return_value=3)

        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=f,
                keyword_only=f,
                positional_or_keyword=f,
                flag=ParameterFlag.KEYWORD_ONLY_SOME_OPTIONAL
            )))
            for _ in range(30)
        ]
        d = {
            tuple((1 if a.default else 0) for a in x) for x in xs
        }
        assert len(d) > 1

    def test_some_optional_bounded_length(self, some_optional_flag):
        f = Mock(return_value=15)

        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=f,
                keyword_only=f,
                positional_or_keyword=f,
                flag=some_optional_flag
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default)
            for x in xs
        }
        assert all(iter(0 < a < 30 for a in counts))

    def test_some_optional_variance(self, some_optional_flag):
        f = Mock(return_value=14)

        xs = [
            next(iter(build_skeleton_signatures(
                positional_only=f,
                keyword_only=f,
                positional_or_keyword=f,
                flag=some_optional_flag
            )))
            for _ in range(30)
        ]
        counts = {
            sum(1 for a in x if a.default)
            for x in xs
        }
        assert len(counts) > 1

    def test_all_optional(self, all_optional_flag):
        f = Mock(return_value=3)

        xs = list(build_skeleton_signatures(
            positional_only=f,
            keyword_only=f,
            positional_or_keyword=f,
            flag=all_optional_flag[0]
        ))

        assert xs[0] == (
            BareParameter(all_optional_flag[1], True),
            BareParameter(all_optional_flag[1], True),
            BareParameter(all_optional_flag[1], True),
        )


def test_invalid_flag_permutations(invalid_flags):
    flag = invalid_flags[0]
    for f in invalid_flags[1:]:
        flag |= f

    xs = list(build_skeleton_signatures(
        positional_only=4,
        keyword_only=4,
        positional_or_keyword=4,
        flag=flag
    ))

    assert xs == []


def test_all_flags_permuations():
    xs = list(build_skeleton_signatures(
        positional_only=4,
        keyword_only=4,
        positional_or_keyword=4
    ))

    assert len(xs) == 192

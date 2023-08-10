import pytest
import function_test_fixtures.utils as utils

def test_copy_seq_generator_is_copy():
    """
    Altering l1's children should not affect l2 as the
    l2's children are shallow copies of l1's
    """

    l1 = [[[n]] for n in range(5)]
    l2 = list(utils.copy_seq_generator(l1))
    
    for l,n in zip(l1, range(5,10)):
        l.append(n)

    assert l2 == [[[n]] for n in range(5)]


def test_copy_seq_generator_is_not_deepcopy():
    """
    however altering items in l1's children should affect
    the item in l2's children as the children are shallowed
    copied
    """

    l1 = [[[n]] for n in range(5)]
    l2 = list(utils.copy_seq_generator(l1))

    for l,n in zip(l1, range(5,10)):
        l[0].append(n)

    assert l2 == [[[n,n+5]] for n in range(5)]


SPLIT_N = 11


def test_split_int_len():
    r = utils.split_int(SPLIT_N)
    assert len(r) == 3


def test_split_int_mid():
    # If we don't force the split it's random so testing it
    # takes a bit more work
    s = frozenset({(SPLIT_N,0),(0,SPLIT_N)})
    r = utils.split_int(SPLIT_N)
    n, m = next(iter(r - s))
    assert (
        0 < n < SPLIT_N
        and 0 < m < SPLIT_N
        and n + m == SPLIT_N
    )


def test_split_int_mid_forced():
    s = frozenset({(SPLIT_N,0),(3,SPLIT_N-3),(0,SPLIT_N)})
    r = utils.split_int(SPLIT_N,x=3)


def test_split_int_rest():
    s = frozenset({(SPLIT_N,0),(0,SPLIT_N)})
    r = utils.split_int(SPLIT_N)
    assert s < r


def test_split_int_1():
    assert utils.split_int(1) == frozenset({(1,0),(0,1)})


def test_split_int_0():
    assert utils.split_int(0) == frozenset({(0,0)})


def test_test_range_start_and_stop_diff1():
    assert utils.test_range(9, 10) == (9, 10)


def test_test_range_start_and_stop_diff0():
    assert utils.test_range(16, 16) == (16,)


def test_test_range_start_and_stop_diff2():
    assert utils.test_range(4,6) == (4,5,6)


def test_test_range_start_and_stop_wide_head():
    r = utils.test_range(13, 40)
    assert r[0] == 13


def test_test_range_start_and_stop_wide_tail():
    r = utils.test_range(13, 40)
    assert r[2] == 40


def test_test_range_start_and_stop_wide_mid():
    r = utils.test_range(13, 40)
    assert 13 < r[1] < 40


def test_test_range_stop_diff0():
    assert utils.test_range(0) == (0,)


def test_test_range_stop_diff1():
    assert utils.test_range(1) == (0,1)


def test_test_range_stop_diff2():
    assert utils.test_range(2) == (0,1,2)


def test_test_range_stop_wide_head():
    r = utils.test_range(23)
    assert r[0] == 0


def test_test_range_stop_wide_tail():
    r = utils.test_range(23)
    assert r[2] == 23


def test_test_range_stop_wide_mid():
    r = utils.test_range(23)
    assert 0 < r[1] < 23


def test_test_low_range_start_and_stop_diff1():
    assert utils.test_low_range(9, 10) == (9,)


def test_test_low_range_start_and_stop_diff0():
    with pytest.raises(TypeError):
        assert utils.test_low_range(16, 16)


def test_test_low_range_start_and_stop_diff2():
    assert utils.test_low_range(4,6) == (4,5)


def test_test_low_range_start_and_stop_wide_head():
    r = utils.test_low_range(13, 40)
    assert r[0] == 13


def test_test_low_range_start_and_stop_wide_tail():
    r = utils.test_low_range(13, 40)
    assert 13 < r[1] < 40


def test_test_low_range_stop_diff0():
    with pytest.raises(TypeError):
    	assert utils.test_low_range(0)


def test_test_low_range_stop_diff1():
    assert utils.test_low_range(1) == (0,)


def test_test_low_range_stop_diff2():
    assert utils.test_low_range(2) == (0,1)


def test_test_low_range_stop_wide_head():
    r = utils.test_low_range(23)
    assert r[0] == 0


def test_test_low_range_stop_wide_tail():
    r = utils.test_low_range(23)
    assert 0 < r[1] < 23


def test_test_high_range_start_and_stop_diff1():
    assert utils.test_high_range(101, 102) == (102,)


def test_test_high_range_start_and_stop_diff0():
    with pytest.raises(TypeError):
        assert utils.test_high_range(71, 71)


def test_test_high_range_start_and_stop_diff2():
    assert utils.test_high_range(34,36) == (35,36)


def test_test_high_range_start_and_stop_wide_tail():
    r = utils.test_high_range(7, 51)
    assert r[1] == 51


def test_test_high_range_start_and_stop_wide_head():
    r = utils.test_high_range(7, 51)
    assert 7 < r[0] < 51


def test_test_high_range_stop_diff0():
    with pytest.raises(TypeError):
    	assert utils.test_high_range(0)


def test_test_high_range_stop_diff1():
    assert utils.test_high_range(1) == (1,)


def test_test_high_range_stop_diff2():
    assert utils.test_high_range(2) == (1,2)


def test_test_high_range_stop_wide_tail():
    r = utils.test_high_range(45)
    assert r[1] == 45


def test_test_high_range_stop_wide_head():
    r = utils.test_high_range(23)
    assert 0 < r[0] < 23

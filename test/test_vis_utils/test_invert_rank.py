from visualisation.vis_utils.invert_rank import invert_rank

def test_returns_int():
    result = invert_rank(2)
    assert type(result) == int

def test_does_not_mutate_input():
    num = 2
    invert_rank(num)
    assert num == 2

def test_returns_zero_for_100():
    result = invert_rank(100)
    assert result == 0

def test_returns_positive_number():
    result = invert_rank(80)
    assert result > 0

def test_returns_number_below_100():
    result = invert_rank(1)
    assert result < 100

def test_returns_inverted_number():
    result = invert_rank(1)
    assert result == 99
    result_2 = invert_rank(5)
    assert result_2 == 95
    result_3 = invert_rank(29)
    assert result_3 == 71

def test_returns_zero_for_numbers_above_100():
    result = invert_rank(200)
    assert result == 0
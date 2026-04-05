import pytest

from tiebreak import Result, OutCome


samples = [
    ("aaa", "bbb", OutCome.WIN, None),
    ("ccc", "ddd", OutCome.LOSE, None),
    ("eee", "fff", OutCome.DRAW, 2),
    ("ggg", "hhh", "win", 4),
    ("iii", "jjj", "lose", 10),
]


@pytest.mark.parametrize("p, o, s, r", samples)
def test_player(p, o, s, r):
    result = Result(p, o, s)
    assert result.player == p


@pytest.mark.parametrize("p, o, s, r", samples)
def test_opponent(p, o, s, r):
    result = Result(p, o, s)
    assert result.opponent == o


@pytest.mark.parametrize("p, o, s, r", samples)
def test_outcome(p, o, s, r):
    result = Result(p, o, s)
    assert result.outcome == s


@pytest.mark.parametrize("p, o, s, r", samples)
def test_round(p, o, s, r):
    result = Result(p, o, s, r)
    assert result.round == r

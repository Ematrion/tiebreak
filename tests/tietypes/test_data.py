import pytest

from tiebreaker import DataSet, OutCome, Result


@pytest.fixture
def results():
    samples = [
        ("aaa", "bbb", OutCome.WIN, None),
        ("ccc", "ddd", OutCome.LOSE, None),
        ("eee", "fff", OutCome.DRAW, 2),
        ("ggg", "hhh", OutCome.OTW, 4),
        ("iii", "jjj", OutCome.SOW, 10),
    ]
    return [Result(*data) for data in samples]


@pytest.fixture
def roundrobin():
    samples = [
        ("aaa", "bbb", OutCome.WIN, 1),
        ("ccc", "ddd", OutCome.WIN, 1),
        ("aaa", "ccc", OutCome.WIN, 2),
        ("bbb", "ddd", OutCome.WIN, 2),
        ("aaa", "ddd", OutCome.WIN, 3),
        ("bbb", "ccc", OutCome.WIN, 3),
    ]
    return [Result(*data) for data in samples]


singles = [
    ("aaa", OutCome.WIN, 1),
    ("bbb", OutCome.LOSE, 1),
    ("eee", OutCome.DRAW, 1),
    ("fff", OutCome.DRAW, 1),
    ("ggg", OutCome.OTW, 1),
    ("hhh", OutCome.OTL, 1),
    ("iii", OutCome.SOW, 1),
    ("jjj", OutCome.SOL, 1),
]

min_rr = [
    ("aaa", OutCome.WIN, 3),
    ("bbb", OutCome.WIN, 2),
    ("bbb", OutCome.LOSE, 1),
    ("ccc", OutCome.WIN, 1),
    ("ccc", OutCome.LOSE, 2),
    ("ddd", OutCome.LOSE, 3),
]


@pytest.fixture()
def dataset(results):
    return DataSet(results)


@pytest.fixture
def rrdata(roundrobin):
    return DataSet(roundrobin)


def test_players(dataset):
    assert len(dataset.players()) == 10


@pytest.mark.parametrize("player", [r[0] for r in singles])
def test_results_of_without_outcome(player, dataset):
    assert len(dataset.results_of(player)) == 1


@pytest.mark.parametrize("player, outcome, target", singles)
def test_results_of_with_outcome(player, outcome, target, dataset):
    assert len(dataset.results_of(player, outcome)) == target


@pytest.mark.parametrize("player, outcome, target", singles)
def test_results_of_with_outcome_no_result(player, outcome, target, dataset):
    for v in OutCome:
        if v != outcome:
            assert len(dataset.results_of(player, v)) == 0


@pytest.mark.parametrize("player, outcome, target", min_rr)
def test_results_of_with_outcome_many(player, outcome, target, rrdata):
    assert len(rrdata.results_of(player, outcome)) == target

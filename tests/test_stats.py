import pytest

from tiebreak import Result, DataSet, OutCome
from tiebreak.points import CHESS

from tiebreak import record_score, player_score, opponents_score, number_of_games

import collections

rm = {"½": OutCome.DRAW, "1": OutCome.WIN, "0": OutCome.LOSE}


@pytest.fixture
def dataset(wiki_SB):
    games, *_ = wiki_SB
    results = [Result(p, o, rm[s]) for (p, o, s) in games if s in rm.keys()]
    data = DataSet(results=results)
    return data


@pytest.fixture
def scores(wiki_SB):
    _, score_dict, _ = wiki_SB
    return score_dict


def test_record_score_wiki(dataset, scores):
    for player in dataset.players():
        record = dataset.player_record(player)
        assert record_score(record, CHESS) == scores[player]


def test_player_score_wiki(dataset, scores):
    for player in dataset.players():
        assert player_score(player, dataset, CHESS) == scores[player]


def test_opponents_score_wiki(dataset, scores):
    for player in dataset.players():
        target = [v for k, v in scores.items() if k != player]
        tests = opponents_score(player, dataset, CHESS)
        assert collections.Counter(target) == collections.Counter(tests)


def test_number_of_games(dataset):
    for player in dataset.players():
        assert number_of_games(player, dataset) == 14

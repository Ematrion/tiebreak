from tiebreaker import OutCome, DataSet, Result, tiebreak
from tiebreaker.policies import Neustadtl


rm = {"½": OutCome.DRAW, "1": OutCome.WIN, "0": OutCome.LOSE}


def test_candidate(candidate2024_results):
    games, target = candidate2024_results
    results = [Result(p, o, rm[s]) for (p, o, s) in games if s in rm.keys()]
    data = DataSet(results=results)
    tb = tiebreak(Neustadtl, data)
    for p in data.players():
        assert target[p] == tb[p]


def test_wiki(wiki_SB):
    games, scores, ns = wiki_SB
    results = [Result(p, o, rm[s]) for (p, o, s) in games if s in rm.keys()]
    data = DataSet(results=results)
    tb = tiebreak(Neustadtl, data)
    for p in data.players():
        assert ns[p] == tb[p]

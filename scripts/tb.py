import re
import pandas as pd

from tiebreaker import OutCome, DataSet, Result, tiebreaker
from tiebreaker.policies import Neustadtl


def candidate2024_results():
    file_name = "data/candidate2024.csv"
    table = table = pd.read_csv(file_name)
    players = list(table["Player"].values)

    def short(name: str):
        r = re.findall("([A-Z])", name)
        return r[0] + r[1]

    names = {short(player): player for player in players}
    names.update({short(player) + ".1": player for player in players})

    opponents = list(names.keys())

    sb = {}
    games = []  # (p1, p2, score)
    for _, row in table.iterrows():
        player = row["Player"]
        for col, opponent in names.items():
            if short(opponent) in opponents[opponents.index(short(player)) :]:
                game = (player, opponent, row[col])
                games.append(game)
        sb[player] = row["SB"]

    return games, sb


games, target = candidate2024_results()
print(len(games))
print(len(target))
rm = {"½": OutCome.DRAW, "1": OutCome.WIN, "0": OutCome.LOSE}
results = [Result(p, o, rm[s]) for (p, o, s) in games if s in rm.keys()]
data = DataSet(results=results)
tb = tiebreaker(Neustadtl, data)
for p in data.players():
    print(target[p], tb[p])

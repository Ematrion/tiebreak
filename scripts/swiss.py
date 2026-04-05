import pandas as pd
import re
from tiebreak import OutCome, Result, DataSet, tiebreaker
from tiebreak.policies import (
    MedianSystem,
    Solkoff,
    Gelbfuhs,
    SonnebornBerger,
    Neustadtl,
    Buchholz,
)

# load excel data
swiss = "data/Bundesturnier2024 Hauptturnier1.xlsx"
columns = [
    "Rank",
    "Title",
    "Name",
    "Land",
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    "Pts",
    "Wtg1",
    "Wtg2",
    "Wtg3",
]
table = pd.read_excel(
    swiss, header=17, usecols="A:O", names=columns, skiprows=[130, 131, 132]
)

# extract game dataset
games = []
for i, row in table.iterrows():
    player = row["Name"]
    # print(type(player))
    for round in [1, 2, 3, 4, 5, 6, 7]:
        data = row[round]
        try:
            adv_rank, score = re.split(r"s|w", data)
            adv_rank = int(adv_rank)
        except TypeError:  # unplayed games are marked with a 0 (int)
            continue
        # do not record twice the same game
        if adv_rank > i:
            opponent = table.loc[table["Rank"] == adv_rank]["Name"].values[0]
            # print(type(opponent))
            # print(i, player, adv_rank, opponent, score)
            games.append((player, opponent, score))


# load data in package
rm = {"½": OutCome.DRAW, "1": OutCome.WIN, "0": OutCome.LOSE}

results = [Result(p, o, rm[s]) for (p, o, s) in games if s in rm.keys()]
data = DataSet(results=results)

# print(data.players())

# compute tiebreaker
policies = [MedianSystem, Solkoff, Gelbfuhs, SonnebornBerger, Neustadtl, Buchholz]
tbs = [tiebreaker(policy, data) for policy in policies]
pols = [policy.__name__ for policy in policies]


# inspect scores
for i, row in table.iterrows():
    player = row["Name"]
    print(player, row["Wtg1"], row["Wtg2"])
    for p, res in zip(pols, tbs):
        print(p, " : ", res[player])
    print("---------------------")

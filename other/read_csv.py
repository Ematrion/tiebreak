import pandas as pd
import re


file_name = "data/candidate2024.csv"
table = table = pd.read_csv(file_name)
players = list(table["Player"].values)


def short(name: str):
    r = re.findall("([A-Z])", name)
    return r[0] + r[1]


names = {short(player): player for player in players}
names.update({short(player) + ".1": player for player in players})

games = []  # (p1, p2, score)
for _, row in table.iterrows():
    player = row["Player"]
    for col, opponent in names.items():
        game = (player, opponent, row[col])
        games.append(game)

print(table)

import pandas as pd
import re
import pytest


@pytest.fixture
def wiki_SB():
    # crosstable of the 1975–80 World Correspondence Chess Championship Final
    file_name = "data/wiki_sonnebornberger.csv"
    table = pd.read_csv(file_name)

    games = []
    points = {}
    ns = {}
    for rank, row in table.iterrows():
        player = row["Name"]
        pts = row["Points"]
        if pts[-1] == "½":
            pts = pts[:-1] + ".5"
        points[player] = float(pts)
        ns[player] = row["Neustadtl score"]
        for adv_rank in range(1, 16):
            if adv_rank > rank:
                score = row[str(adv_rank)]
                opponent = table.loc[table["Position"] == adv_rank]["Name"].values[0]
                games.append((player, opponent, score))
    return games, points, ns


@pytest.fixture
def candidate2024_results():
    file_name = "data/candidate2024.csv"
    table = table = pd.read_csv(file_name)
    players = list(table["Player"].values)

    def short(name: str):
        r = re.findall("([A-Z])", name)
        return r[0] + r[1]

    names = {short(player): player for player in players}
    names.update({short(player) + ".1": player for player in players})

    # black magic setup
    opponents = list(names.keys())

    sb = {}
    games = []  # (p1, p2, score)
    for _, row in table.iterrows():
        player = row["Player"]
        for col, opponent in names.items():
            # black magic: results are present twice in the table (symetric)
            if short(opponent) in opponents[opponents.index(short(player)) :]:
                game = (player, opponent, row[col])
                games.append(game)
        sb[player] = row["SB"]

    return games, sb


@pytest.fixture
def Bundesturnier2024():
    file_name = "data/Bundesturnier2024Hauptturnier1.xlsx"
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
        file_name, header=17, usecols="A:O", names=columns, skiprows=[130, 131, 132]
    )
    table.set_index("Rank", inplace=True)

    games = []
    for i, row in table.iterrows():
        player = row["Name"]
        for round in [1, 2, 3, 4, 5, 6, 7]:
            data = row[round]
            try:
                adv_rank, score = re.split(r"s|w", data)
                adv_rank = int(adv_rank)
            except TypeError:  # unplayed games are marked with a 0 (int)
                continue
            # do not record twice the same game
            if adv_rank > i:
                opponent = table.loc[table["Rank"] == adv_rank]["Name"]
                games.append((player, opponent, score))

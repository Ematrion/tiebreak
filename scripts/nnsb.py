import pandas as pd
import urllib

file_name = "data/wiki_sonnebornberger.csv"
url = "https://en.wikipedia.org/wiki/Sonneborn–Berger_score"
url = urllib.parse.quote_plus(url, "/:?=&")  # need this line
table = pd.read_html(url)[0]


table.columns = [name for _, name in table.columns]
print(table.shape)
print(table.columns)
print(table)

table.to_csv(file_name)
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

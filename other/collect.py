import pandas as pd


sb = "https://en.wikipedia.org/wiki/Sonneborn–Berger_score"
candidate = "https://en.wikipedia.org/wiki/Candidates_Tournament_2024"
table = pd.read_html(candidate, match="Standing", encoding="utf8")[0]
print(table)
table.to_csv("data/candidate2024.csv")

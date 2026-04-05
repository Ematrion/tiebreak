from enum import Enum
from typing import Hashable

DUALITY = {
    "win": "lose",
    "lose": "win",
    "draw": "draw",
    "overtimewin": "overtimelose",
    "overtimelose": "overtimewin",
    "shootoutwin": "shootoutlose",
    "shootoutlose": "shootoutwin",
}


class OutCome(Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"
    OTW = "overtimewin"
    OTL = "overtimelose"
    SOW = "shootoutwin"
    SOL = "shootoutlose"

    def dual(self):
        return OutCome(DUALITY[self.value])


Player = Hashable
PointSystem = dict[OutCome, float]
Record = dict[OutCome, int]


class Result:
    def __init__(
        self,
        player: Player,
        opponent: Player,
        outcome: OutCome,
        round: int | None = None,
    ):
        self.player = player
        self.opponent = opponent
        self.outcome: OutCome = outcome
        self.round: int = round if round else 0

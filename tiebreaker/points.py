from . import OutCome, PointSystem


KASHDAN: PointSystem = {OutCome.WIN: 4.0, OutCome.DRAW: 2.0, OutCome.LOSE: 1.0}


CHESS: PointSystem = {OutCome.WIN: 1.0, OutCome.DRAW: 0.5, OutCome.LOSE: 0.0}

FOOTBALL: PointSystem = {
    OutCome.WIN: 3.0,
    OutCome.DRAW: 1.0,
    OutCome.LOSE: 0.5,  # ??? why - source
}

NA_HOCKEY: PointSystem = {
    OutCome.WIN: 2.0,
    OutCome.LOSE: 0.0,
    OutCome.OTW: 2.0,
    OutCome.OTL: 1.0,
    OutCome.SOW: 2.0,
    OutCome.SOL: 1.0,
}

EU_HOCKEY: PointSystem = {
    OutCome.WIN: 3.0,
    OutCome.LOSE: 0.0,
    OutCome.OTW: 2.0,
    OutCome.OTL: 1.0,
    OutCome.SOW: 2.0,
    OutCome.SOL: 1.0,
}

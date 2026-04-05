from tiebreak import PointSystem, Record, Player, DataSet, OutCome


def record_score(record: Record, points: PointSystem) -> float:
    return sum(
        [
            points[outcome] * record[outcome]
            for outcome in OutCome
            if outcome in points.keys()
        ]
    )


def player_score(player: Player, data: DataSet, points: PointSystem) -> float:
    return record_score(data.player_record(player), points)


def opponents_score(player: Player, data: DataSet, points: PointSystem) -> list[float]:
    return [
        player_score(opponent, data, points) for opponent in data.opponents_of(player)
    ]


def number_of_games(player: Player, data) -> int:
    return len(data.results_of(player))

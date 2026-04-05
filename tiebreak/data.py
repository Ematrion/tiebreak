from tiebreak import Player, Result, OutCome


class DataSet:
    def __init__(self, results: list[Result]):
        self._results = results
        self._results += [
            Result(
                player=result.opponent,
                opponent=result.player,
                outcome=result.outcome.dual(),
            )
            for result in self._results
        ]

    def results_of(
        self, player: Player, outcome: OutCome | None = None
    ) -> list[Result]:
        home = [result for result in self._results if player == result.player]
        if outcome:
            home = [result for result in home if result.outcome == outcome]
        return home

    def opponents_of(
        self, player: Player, outcome: OutCome | None = None
    ) -> list[Player]:
        return [result.opponent for result in self.results_of(player, outcome)]

    def player_record(self, player):
        return {outcome: len(self.results_of(player, outcome)) for outcome in OutCome}

    def players(self):
        return list(
            set(
                [result.player for result in self._results]
                + [result.opponent for result in self._results]
            )
        )

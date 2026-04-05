from tiebreak import Policy, DataSet, Player, PointSystem
from . import points as pt


def tiebreaker(
    policy: Policy, data: DataSet, points: PointSystem = pt.CHESS
) -> dict[Player, float]:
    """Tiebreak Computer

    Compute tiebreaker value of all players in the data according to a tiebreak policy

    Parameters
    ----------
    policy : Policy
        The tiebreak rule, e.g. policies.Solkoff
    data : DataSet
        A source data set. All games are used.
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    dict[Player, float]
        The tiebreaking values for each involved player
    """
    return {player: policy(player, data, points) for player in data.players()}

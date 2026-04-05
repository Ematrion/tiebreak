from . import Player, DataSet, OutCome, PointSystem
from . import player_score, opponents_score, number_of_games
from . import points as pt

from typing import Callable

# Resources:
#   - http://www.schoolchess.org/old/information/TieBreaks.html
#   - https://madisonchess.com/tiebreakrules
#   - https://en.wikipedia.org/wiki/Tiebreaker
#   - https://en.wikipedia.org/wiki/Tie-breaking_in_Swiss-system_tournaments
#   - https://archive.org/stream/TheOxfordCompanionToChessFirstEditionByDavidHooperKennethWhyld/The%20Oxford%20Companion%20to%20Chess%20-%20First%20Edition%20by%20David%20Hooper%20%26%20Kenneth%20Whyld_djvu.txt
#   - https://www.chess.com/forum/view/tournaments/for-life-can-t-figure-out-tiebreak-points
#   - https://handbook.fide.com/chapter/TieBreakRegulations032026

Policy = Callable[[Player, DataSet, PointSystem], float]


def Baumbach(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    return len(data.results_of(player, OutCome.WIN))


def Solkoff(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    """Solkoff Score

    as defined in the firt edition of 'The Oxford Companion To Chess':

    SOLKOFF SCORE, an auxiliary scoring method
    used for tie breaking in Swiss system tournaments,
    and sometimes known as 'sum of opponents'

    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    return sum(opponents_score(player, data, points))


def Buchholz(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    """Buchholz Score

    as defined in the firt edition of 'The Oxford Companion To Chess':

    BUCHHOLZ SCORE, an auxiliary scoring method
    devised to supplant the Svensson system (basically
    the same as neustadilV) in Swiss system tourna¬
    ments. A players total score multiplied by the sum
    of his opponents' scores is his Buchholz score.

    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    return player_score(player, data, points) * sum(
        opponents_score(player, data, points)
    )


def Coons(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    """Coons Score

    as defined in first edition of 'The Oxford Companion To Chess':

    COONS SCORE, a tie-breaking method intended
    as a refinement of the neustadtl score. A player's
    Coons Score is the sum of the following: the scores
    of those he defeated, half the scores of those with
    whom he drew, and one fifth of the scores of those
    to whom he lost. (For an example see auxiliary


    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS
    Returns
    -------
    float
        a score
    """
    weights = [1.0, 0.5, 0.1]
    victorious, defeated, tied = [
        data.opponents_of(player, outcome)
        for outcome in [OutCome.WIN, OutCome.LOSE, OutCome.DRAW]
    ]
    return sum(
        [
            sum([player_score(opponent, data, points) for opponent in group]) * weight
            for group, weight in zip([victorious, defeated, tied], weights)
        ]
    )


def MedianSystem(
    player: Player, data: DataSet, points: PointSystem = pt.CHESS
) -> float:
    """Median System

    as defined in the firt edition of 'The Oxford Companion To Chess':

    MEDIAN SYSTEM, a tie-breaking method for use
    in Swiss system tournaments. Each player`s sol-
    koff score (the sum of opponents` scores) has the
    top and bottom components removed.

    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    return sum(sorted(opponents_score(player, data, points))[1:-1])


def Neustadtl(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    """Neustadtl Score

    as defined in the firt edition of 'The Oxford Companion To Chess':

    NEILS TADTI, S CORE, a n auxiliary s coring
    method for all-play-all tournaments: the sum of the
    normal scores of the opponents a player defeated is
    added to half the sum of the normal scores of those
    against whom he drew. Now widely used for
    tie-breaking, frequently but wrongly called sonne-
    born—uerger score, this scoring method was first
    suggested by Hermann Neustadtl (1862-1909), a
    Viennese doctor from Prague, in a letter he wrote
    to Chess Monthly in 1882,


    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    weights = [1.0, 0.5]
    outcomes = [OutCome.WIN, OutCome.DRAW]
    return sum(
        [
            sum(
                [
                    player_score(opponent, data, points)
                    for opponent in data.opponents_of(player, outcome)
                ]
            )
            * weight
            for outcome, weight in zip(outcomes, weights)
        ]
    )


def Gelbfuhs(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    """Gelbfuhs System

    as defined in the firt edition of 'The Oxford Companion To Chess':

    GELBFUHS SC ORE. a complicated but now
    obsolete auxiliary scoring method by which
    placings in a tournament might be determined. A
    player's score is based on his wins and draws: the
    sum of each defeated opponent's normal score is
    divided by the number of games played by that
    opponent, this fraction being calculated similarly
    for drawn games and then halved; the sum of these
    fractions is a player`s Gelbfuhs score.

    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    weights = [1.0, 0.5]
    outcomes = [OutCome.WIN, OutCome.DRAW]
    return sum(
        [
            sum(
                [
                    player_score(opponent, data, points)
                    / number_of_games(opponent, data)
                    for opponent in data.opponents_of(player, outcome)
                ]
            )
            * weight
            for outcome, weight in zip(outcomes, weights)
        ]
    )


def SonnebornBerger(
    player: Player, data: DataSet, points: PointSystem = pt.CHESS
) -> float:
    """Sonneborn-Berger

    as defined in the firt edition of 'The Oxford Companion To Chess':

    SONNEBORN-BERGER SCORE, a long forgot¬
    ten AUXILIARY SCORING methqd, although the name
    has erroneously been transferred to the commonly
    used neustadtl score. In 1886 a London bank
    clerk, William Sonneborn (1843-1906), wrote to
    Chess Monthly saying that the gelbfuhs score was
    defective because it did not take into account the
    quality of the player`s awn results. He proposed
    that a players total score expressed as a fraction of
    the number of games played should be squared and
    then added to his Gelbfuhs total. A year later
    berger wrote to DeutscheSchaehzeitung proposing
    to alter the Neustadtl Score for the same reason
    and in the same manner but not using fractions.
    When Berger discovered that he had been antici¬
    pated by Sonneborn, the only difference in their
    proposals being the way of dealing with fractions,
    he suggested their method should be called
    Sonne bo rn-Be rger. They were united in their
    hostility to the Neustadtl score which ironically
    now bears their names.


    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    return (
        player_score(player, data, points) / number_of_games(player, data)
    ) ** 2 + Gelbfuhs(player, data)


def Koya(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    raise NotImplementedError


# --- aliases --- #
def Harkeness(player: Player, data: DataSet, points: PointSystem = pt.CHESS) -> float:
    """Harkness System

    as defined in the firt edition of 'The Oxford Companion To Chess':

    HARKNESS SYSTEM, an auxiliary scoring system
    also known as the median system, it was promoted
    by Kenneth Harkness (1898-1972), Scottish-born
    organizer of chess in the USA.

    .. note::
        This function is an alias for [MedianSystem]

    Parameters
    ----------
    player : Player
        a player to compute an auxiliary score
    data : DataSet
        collections of relevant game results
    points : PointSystem, optional
        A dictionary to convert results into float value, by default pt.CHESS

    Returns
    -------
    float
        a score
    """
    return MedianSystem(player, data, points)

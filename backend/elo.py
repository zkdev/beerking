from elo import rate_1vs1 as elo_1v1


def initial_elo():
    return int(100)


def rate_1v1(winner, loser):
    return elo_1v1(winner, loser)


def rate_2v2(winner1, winner2, loser1, loser2):
    team1 = (winner1 + winner2) / 2
    team2 = (loser1 + loser2) / 2
    return elo_1v1(team1, team2)

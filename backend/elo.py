from elo import rate_1vs1 as elo_1v1


def initial_elo():
    return int(1500)


def rate_1v1(host, enemy):
    return elo_1v1(host, enemy)


def rate_2v2(host, friend, enemy1, enemy2):
    team1 = (host + friend) / 2
    team2 = (enemy1 + enemy2) / 2
    return elo_1v1(team1, team2)
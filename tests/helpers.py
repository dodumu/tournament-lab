from tournament.teams import register_team


def make_teams(names):
    teams = []
    for name in names:
        register_team(teams, name)
    return teams
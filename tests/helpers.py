from tournament.teams import register_team
from tournament.fixtures import generate_fixtures


def make_teams(names):
    teams = []
    for name in names:
        register_team(teams, name)
    return teams


def make_fixtures():
    teams = make_teams(["Thunder", "Comets", "Phoenix", "Rockets"])
    return generate_fixtures(teams, [])


def played_fixture(fixture_id, home_id, away_id, home_score, away_score):
    return {
        "id": fixture_id,
        "home_id": home_id,
        "away_id": away_id,
        "status": "played",
        "home_score": home_score,
        "away_score": away_score,
    }

def make_league():
    teams = make_teams(["Thunder", "Comets", "Phoenix", "Rockets"])
    return teams, generate_fixtures(teams, [])
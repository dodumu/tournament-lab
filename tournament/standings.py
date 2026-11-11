from tournament.validation import STATUS_PLAYED, normalize_name, validate_league

POINTS_WIN = 3
POINTS_DRAW = 1
POINTS_LOSS = 0


def _empty_row(team):
    return {
        "team_id": team["id"],
        "name": team["name"],
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_diff": 0,
        "points": 0,
    }


def _add_game(row, scored, conceded):
    row["played"] += 1
    row["goals_for"] += scored
    row["goals_against"] += conceded
    if scored > conceded:
        row["wins"] += 1
        row["points"] += POINTS_WIN
    elif scored == conceded:
        row["draws"] += 1
        row["points"] += POINTS_DRAW
    else:
        row["losses"] += 1
        row["points"] += POINTS_LOSS


def ranking_key(row):
    return (
        -row["points"],
        -row["goal_diff"],
        -row["goals_for"],
        normalize_name(row["name"]),
    )


def compute_standings(teams, fixtures):
    validate_league(teams, fixtures)
    rows_by_id = {team["id"]: _empty_row(team) for team in teams}

    for fixture in fixtures:
        if fixture["status"] != STATUS_PLAYED:
            continue
        home = rows_by_id[fixture["home_id"]]
        away = rows_by_id[fixture["away_id"]]
        _add_game(home, fixture["home_score"], fixture["away_score"])
        _add_game(away, fixture["away_score"], fixture["home_score"])

    rows = list(rows_by_id.values())
    for row in rows:
        row["goal_diff"] = row["goals_for"] - row["goals_against"]
    return sorted(rows, key=ranking_key)

def is_league_complete(fixtures):
    return len(fixtures) > 0 and all(
        fixture["status"] == STATUS_PLAYED for fixture in fixtures
    )


def get_champion(teams, fixtures):
    if not is_league_complete(fixtures):
        return None
    return compute_standings(teams, fixtures)[0]
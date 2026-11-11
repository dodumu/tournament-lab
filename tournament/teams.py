from tournament.validation import MAX_TEAMS, ValidationError, validate_team_name


def register_team(teams, name):
    if len(teams) >= MAX_TEAMS:
        raise ValidationError(f"The league is full ({MAX_TEAMS} teams maximum).")
    
    clean_name = validate_team_name(name, teams)

    team = {"id": f"TM{len(teams) + 1:03d}", "name": clean_name}
    teams.append(team)
    return team


def list_teams(teams):
    return [f"{team['id']} {team['name']}" for team in teams]


def team_names_by_id(teams):
    return {team["id"]: team["name"] for team in teams}
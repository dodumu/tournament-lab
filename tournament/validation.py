MIN_NAME_LENGHT = 2
MAX_NAME_LENGHT = 30
MAX_TEAMS = 8
MIN_TEAMS = 4
STATUS_PENDING = "pending"
STATUS_PLAYED = "played"

class ValidationError(Exception):
    """Raised when data breaks a league rule."""

def normalize_name(name):
    return name.strip().casefold()


def validate_team_name(name, existing_teams):
    if not isinstance(name, str):
        raise ValidationError("Team name must be text.")

    cleaned = name.strip()
    if len(cleaned) < MIN_NAME_LENGHT or len(cleaned) > MAX_NAME_LENGHT:
        raise ValidationError(f"Team name must be  {MIN_NAME_LENGHT}--{MAX_NAME_LENGHT} characters.")

    wanted = normalize_name(cleaned)
    for team in existing_teams:
        if normalize_name(team["name"]) == wanted:
            raise ValidationError(f"A team named '{team['name']}' already exists.")

    return cleaned



def validate_score(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"Score must be a whole number, got {value!r}.")
    if value < 0:
        raise ValidationError(f"Score cannot be negative, got {value}.")
    return value


def expected_fixture_count(team_count):
    return team_count * (team_count - 1) // 2


def validate_league(teams, fixtures):
    if len(teams) > MAX_TEAMS:
        raise ValidationError(f"A league has at most {MAX_TEAMS} teams.")

    team_ids = set()
    seen_names = set()
    for team in teams:
        if not isinstance(team, dict) or set(team.keys()) != {"id", "name"}:
            raise ValidationError("Each team must have exactly 'id' and 'name'.")
        if not isinstance(team["id"], str) or not isinstance(team["name"], str):
            raise ValidationError("Team id and name must be text.")
        if team["id"] in team_ids:
            raise ValidationError(f"Duplicate team id {team['id']}.")
        team_ids.add(team["id"])

        validate_team_name(team["name"], [])
        if team["name"] != team["name"].strip():
            raise ValidationError(f"Team name '{team['name']}' is not trimmed.")
        key = normalize_name(team["name"])
        if key in seen_names:
            raise ValidationError(f"Duplicate team name '{team['name']}'.")
        seen_names.add(key)

    if not fixtures:
        return

    if len(fixtures) != expected_fixture_count(len(teams)):
        raise ValidationError(
            f"{len(teams)} teams need {expected_fixture_count(len(teams))} "
            f"fixtures, found {len(fixtures)}."
        )

    required_keys = {"id", "home_id", "away_id", "status", "home_score", "away_score"}
    fixture_ids = set()
    pairs = set()
    for fixture in fixtures:
        if not isinstance(fixture, dict) or set(fixture.keys()) != required_keys:
            raise ValidationError("A fixture has missing or unexpected keys.")

        fixture_id = fixture["id"]
        if not isinstance(fixture_id, str) or fixture_id in fixture_ids:
            raise ValidationError(f"Fixture id {fixture_id!r} is invalid or duplicated.")
        fixture_ids.add(fixture_id)

        home, away = fixture["home_id"], fixture["away_id"]
        if (
            not isinstance(home, str)
            or not isinstance(away, str)
            or home not in team_ids
            or away not in team_ids
        ):
            raise ValidationError(f"Fixture {fixture_id} refers to a team that does not exist.")
        if home == away:
            raise ValidationError(f"Fixture {fixture_id} makes a team play itself.")

        pair = frozenset((home, away))
        if pair in pairs:
            raise ValidationError(f"Fixture {fixture_id} repeats a pairing already scheduled.")
        pairs.add(pair)

        status = fixture["status"]
        scores = (fixture["home_score"], fixture["away_score"])
        if status == STATUS_PENDING:
            if scores != (None, None):
                raise ValidationError(f"Pending fixture {fixture_id} must not have scores.")
        elif status == STATUS_PLAYED:
            validate_score(scores[0])
            validate_score(scores[1])
        else:
            raise ValidationError(f"Fixture {fixture_id} has unknown status {status!r}.")

def parse_score_text(text):
    try:
        number = int(text.strip())
    except ValueError:
        raise ValidationError(f"'{text.strip()}' is not a whole number.") from None
    return validate_score(number)
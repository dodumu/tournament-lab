from tournament.validation import(
    MAX_TEAMS,
    MIN_TEAMS,
    STATUS_PENDING,
    STATUS_PLAYED,
    ValidationError,
    validate_score,
)



def generate_fixtures(teams, existing_fixtures):
    if existing_fixtures:
        raise ValidationError("The schedule was already generated for this season")
    if len(teams) < MIN_TEAMS or len(teams) > MAX_TEAMS:
        raise ValidationError(
            f"Need {MIN_TEAMS}--{MAX_TEAMS} teams to generate fixtures, have {len(teams)}."
        )

    fixtures = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            number = len(fixtures) + 1
            fixtures.append(
                {
                    "id": f"M{number:03d}",
                    "home_id": teams[i]["id"],
                    "away_id": teams[j]["id"],
                    "status": STATUS_PENDING,
                    "home_score": None,
                    "away_score": None,
                }
            )

    return fixtures



def find_fixtures(fixtures, fixture_id):
    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            return fixture
    raise ValidationError(f"Unknown fixture '{fixture_id}'.")

def record_result(fixtures, fixture_id, home_score, away_score):
    fixture = find_fixtures(fixture, fixture_id)
    if fixture["status"] != STATUS_PENDING:
        raise ValidationError(f"Fixture {fixture_id} has already been played.")
    validate_score(home_score)
    validate_score(away_score)

    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = STATUS_PLAYED
    return fixture
import json
import os

from tournament.validation import MIN_TEAMS, ValidationError, validate_league

SCHEMA_VERSION = 1


def save_league(path, teams, fixtures):
    validate_league(teams, fixtures)
    data = {
        "schema_version": SCHEMA_VERSION,
        "teams": teams,
        "fixtures": fixtures,
    }
    temp_path = str(path) + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    os.replace(temp_path, path)


def load_league(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise ValidationError(f"File '{path}' was not found.") from None
    except json.JSONDecodeError as problem:
        raise ValidationError(f"File is not valid JSON: {problem}") from None
    except OSError as problem:
        raise ValidationError(f"Could not read file: {problem}") from None

    if not isinstance(data, dict):
        raise ValidationError("Save file must contain a JSON object.")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValidationError(f"Unsupported schema_version (need {SCHEMA_VERSION}).")

    teams = data.get("teams")
    fixtures = data.get("fixtures")
    if not isinstance(teams, list) or not isinstance(fixtures, list):
        raise ValidationError("Save file needs 'teams' and 'fixtures' lists.")

    validate_league(teams, fixtures)
    if fixtures and len(teams) < MIN_TEAMS:
        raise ValidationError(f"A schedule needs at least {MIN_TEAMS} teams.")
    return teams, fixtures
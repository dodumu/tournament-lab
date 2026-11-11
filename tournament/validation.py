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
    is isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"Score must be a whole number, got {value!r}.")
    if value < 0:
        raise ValidationError(f"Score cannot be negative, got {value}.")

    return value
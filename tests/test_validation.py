import unittest

from tests.helpers import make_league
from tournament.validation import ValidationError, validate_league


class ValidateLeagueTests(unittest.TestCase):
    def test_valid_league_passes(self):
        teams, fixtures = make_league()
        validate_league(teams, fixtures)

    def test_phantom_team_rejected(self):
        teams, fixtures = make_league()
        fixtures[0]["away_id"] = "TM999"
        with self.assertRaises(ValidationError):
            validate_league(teams, fixtures)
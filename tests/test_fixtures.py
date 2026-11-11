import unittest

from tests.helpers import make_teams
from tournament.fixtures import generate_fixtures
from tournament.validation import ValidationError


class FixtureGenerationTests(unittest.TestCase):
    def test_four_teams_make_six_fixtures(self):
        teams = make_teams(["Thunder", "Comets", "Phoenix", "Rockets"])
        self.assertEqual(len(generate_fixtures(teams, [])), 6)

    def test_six_teams_make_fifteen_fixtures(self):
        teams = make_teams([f"Team {n}" for n in range(6)])
        self.assertEqual(len(generate_fixtures(teams, [])), 15)

    def test_no_duplicate_unordered_pair(self):
        teams = make_teams([f"Team {n}" for n in range(8)])
        fixtures = generate_fixtures(teams, [])
        pairs = {frozenset((fixture["home_id"], fixture["away_id"])) for fixture in fixtures}
        self.assertEqual(len(pairs), len(fixtures))
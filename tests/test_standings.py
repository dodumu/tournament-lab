import unittest

from tournament.fixtures import generate_fixtures, record_result
from tests.helpers import make_teams, played_fixture
from tournament.standings import compute_standings, get_champion, ranking_key


class StandingsTests(unittest.TestCase):
    def setUp(self):
        self.teams = make_teams(["Red", "Blue", "Green"])
        red, blue, green = [team["id"] for team in self.teams]
        self.fixtures = [
            played_fixture("M001", red, blue, 2, 0),
            played_fixture("M002", blue, green, 1, 1),
            played_fixture("M003", red, green, 0, 1),
        ]

    def test_ranking_order(self):
        table = compute_standings(self.teams, self.fixtures)
        self.assertEqual([row["name"] for row in table], ["Green", "Red", "Blue"])

    
def make_row(name, points, goal_diff, goals_for):
    return {
        "name": name,
        "points": points,
        "goal_diff": goal_diff,
        "goals_for": goals_for,
    }


class RankingKeyTests(unittest.TestCase):
    def test_tie_break_order(self):
        rows = [
            make_row("Delta", 7, 2, 5),
            make_row("Bravo", 7, 4, 6),
            make_row("Alpha", 9, 0, 1),
            make_row("Charlie", 7, 2, 8),
        ]
        names = [row["name"] for row in sorted(rows, key=ranking_key)]
        self.assertEqual(names, ["Alpha", "Bravo", "Charlie", "Delta"])


class ChampionTests(unittest.TestCase):
    def test_champion_only_when_all_matches_played(self):
        teams = make_teams(["Thunder", "Comets", "Phoenix", "Rockets"])
        fixtures = generate_fixtures(teams, [])
        scores = [(2, 1), (1, 1), (0, 2), (3, 0), (1, 1), (0, 0)]
        for number, (home, away) in enumerate(scores, start=1):
            self.assertIsNone(get_champion(teams, fixtures))
            record_result(fixtures, f"M{number:03d}", home, away)
        self.assertEqual(get_champion(teams, fixtures)["name"], "Rockets")
import unittest

from tournament.teams import list_teams, register_team
from tournament.validation import ValidationError


class TeamRegistrationTests(unittest.TestCase):
    def test_duplicate_casefolded_name_rejected(self):
        teams = []
        register_team(teams, "Red Comets")
        with self.assertRaises(ValidationError):
            register_team(teams, "  red COMETS ")
        self.assertEqual(len(teams), 1)

    def test_blank_and_too_long_names_rejected(self):
        teams = []
        for bad in ["", "   ", "A", "x" * 31]:
            with self.assertRaises(ValidationError):
                register_team(teams, bad)
        self.assertEqual(teams, [])

    def test_name_is_trimmed_and_ids_are_sequential(self):
        teams = []
        first = register_team(teams, "  Red Comets  ")
        second = register_team(teams, "Blue")
        self.assertEqual(first, {"id": "TM001", "name": "Red Comets"})
        self.assertEqual(second["id"], "TM002")
        self.assertEqual(list_teams(teams), ["TM001 Red Comets", "TM002 Blue"])
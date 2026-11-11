import copy
import unittest

from tests.helpers import make_fixtures
from tournament.fixtures import record_result
from tournament.validation import ValidationError


class ResultEntryTests(unittest.TestCase):
    def test_accepted_result_updates_scores_and_status_together(self):
        fixtures = make_fixtures()
        record_result(fixtures, "M001", 0, 0)
        self.assertEqual(fixtures[0]["status"], "played")
        self.assertEqual(fixtures[0]["home_score"], 0)
        self.assertEqual(fixtures[0]["away_score"], 0)

    def test_bad_goals_rejected_without_changing_anything(self):
        fixtures = make_fixtures()
        before = copy.deepcopy(fixtures)
        for bad in [-1, 1.5, True, False, "2", None]:
            with self.subTest(goals=bad):
                with self.assertRaises(ValidationError):
                    record_result(fixtures, "M001", bad, 0)
                with self.assertRaises(ValidationError):
                    record_result(fixtures, "M001", 0, bad)
        self.assertEqual(fixtures, before)
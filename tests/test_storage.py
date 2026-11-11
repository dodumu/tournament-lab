import copy
import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import make_league
from tournament.fixtures import record_result
from tournament.standings import compute_standings
from tournament.storage import load_league, save_league
from tournament.validation import ValidationError


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "league.json"
        self.teams, self.fixtures = make_league()

    def test_reload_preserves_ids_and_standings(self):
        record_result(self.fixtures, "M001", 2, 1)
        record_result(self.fixtures, "M002", 1, 1)
        before = compute_standings(self.teams, self.fixtures)
        save_league(self.path, self.teams, self.fixtures)
        teams, fixtures = load_league(self.path)
        self.assertEqual(teams, self.teams)
        self.assertEqual(fixtures, self.fixtures)
        self.assertEqual(compute_standings(teams, fixtures), before)

    def test_phantom_team_in_file_rejected_and_memory_unchanged(self):
        bad = {
            "schema_version": 1,
            "teams": copy.deepcopy(self.teams),
            "fixtures": copy.deepcopy(self.fixtures),
        }
        bad["fixtures"][0]["away_id"] = "TM999"
        self.path.write_text(json.dumps(bad), encoding="utf-8")
        teams_before = copy.deepcopy(self.teams)
        fixtures_before = copy.deepcopy(self.fixtures)
        with self.assertRaises(ValidationError):
            load_league(self.path)
        self.assertEqual(self.teams, teams_before)
        self.assertEqual(self.fixtures, fixtures_before)
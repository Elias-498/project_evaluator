import unittest
from  analyzers.test_analyzer import TestAnalyzer, PENALTY_MISSING_TESTS
from tempfile import TemporaryDirectory
from models.project import Project, MAX_PROJECT_SCORE
from pathlib import Path

class TestTestAnalyzer(unittest.TestCase):
    def test_detects_tests_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tests").mkdir()
            project = Project("demo", root)

            TestAnalyzer().analyze(project)

            self.assertTrue(project.has_tests)

    def test_missing_tests_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            project = Project("demo", Path(tmp))

            TestAnalyzer().analyze(project)

            self.assertFalse(project.has_tests)
            self.assertEqual(project.project_score, MAX_PROJECT_SCORE - PENALTY_MISSING_TESTS)



import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from analyzers.documentation_analyzer import PENALTY_MISSING_README
from analyzers.git_analyzer import PENALTY_MISSING_GIT
from analyzers.test_analyzer import PENALTY_MISSING_TESTS
from models.project import MAX_PROJECT_SCORE
from project_evaluator import ProjectScoreEvaluator


class TestProjectEvaluatorIntegration(unittest.TestCase):
    """
    Test full made up projects
    """

    def test_full_well_formed_project(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_dir = root / "well_formed_project"
            project_dir.mkdir()
            (project_dir / "README.md").write_text("# Well Formed Project")
            (project_dir / ".git").mkdir()
            (project_dir / "tests").mkdir()
            (project_dir / "main.py").write_text("print('hello world')\n")

            report = ProjectScoreEvaluator().check(root)

            self.assertIn("well_formed_project", report)
            self.assertIn("Project Score: 100/100", report)
            self.assertIn("Python: 1 file(s)", report)

    def test_full_neglected_project(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_dir = root / "neglected_project"
            project_dir.mkdir()
            (project_dir / "main.py").write_text("print('no tests, no docs')\n")

            report = ProjectScoreEvaluator().check(root)

            expected_score = (MAX_PROJECT_SCORE - PENALTY_MISSING_README - PENALTY_MISSING_GIT - PENALTY_MISSING_TESTS)

            self.assertIn(f"Project Score: {expected_score}/100", report)
            self.assertIn("Missing README documentation", report)
            self.assertIn("No Git repository", report)
            self.assertIn("No test/tests found", report)
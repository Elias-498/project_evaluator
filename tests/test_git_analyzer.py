import unittest
from analyzers.git_analyzer import GitAnalyzer
from tempfile import TemporaryDirectory
from pathlib import Path
from models.project import Project


class TestGitAnalyzer(unittest.TestCase):
    def test_detects_git_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            project = Project("demo", root)

            GitAnalyzer().analyze(project)

            self.assertTrue(project.has_git)

    def test_missing_git_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            project = Project("demo", Path(tmp))

            GitAnalyzer().analyze(project)

            self.assertFalse(project.has_git)
            self.assertIn("No Git repository", project.concerns)



import unittest
from pathlib import Path
from scanner.project_scanner import ProjectScanner
from tempfile import TemporaryDirectory

class TestProjectScanner(unittest.TestCase):
    """
    Unit tests for ProjectScanner.
    """

    def test_finds_only_directories(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "project_a").mkdir()
            (root / "project_b").mkdir()
            (root / "not_a_project.txt").write_text("hello")

            projects = ProjectScanner().scan(root)
            project_names = {project.name for project in projects}

            self.assertEqual(project_names, {"project_a", "project_b"})
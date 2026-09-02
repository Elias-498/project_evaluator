from models.project import Project,MAX_PROJECT_SCORE
from analyzers.documentation_analyzer import DocumentationAnalyzer,PENALTY_MISSING_README
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

class TestDocumentationAnalyzer(unittest.TestCase):
    def test_detects_existing_readme(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo")
            project = Project("demo", root)

            DocumentationAnalyzer().analyze(project)

            self.assertTrue(project.has_readme)
            self.assertEqual(project.concerns, [])

    def test_missing_readme(self) -> None:
        with TemporaryDirectory() as tmp:
            project = Project("demo", Path(tmp))

            DocumentationAnalyzer().analyze(project)

            self.assertFalse(project.has_readme)
            self.assertEqual(project.project_score, MAX_PROJECT_SCORE - PENALTY_MISSING_README)


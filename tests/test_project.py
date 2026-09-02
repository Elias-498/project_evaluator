import unittest
from pathlib import Path
from models.project import Project, MIN_PROJECT_SCORE

class TestProject(unittest.TestCase):
    """
    Unit tests for the Project data model.
    """

    def test_add_concerns_deducts_points(self) -> None:
        project = Project("demo1", Path("."))
        project.add_concerns("missing README", 5) # project score = 100 - 5
        self.assertEqual(project.project_score, 95)
        self.assertIn("missing README", project.concerns)

    def test_project_score_never_goes_below_zero(self) -> None:
        project = Project("demo", Path("."))
        project.add_concerns("No project and passed due time", 1000)
        self.assertEqual(project.project_score, MIN_PROJECT_SCORE)

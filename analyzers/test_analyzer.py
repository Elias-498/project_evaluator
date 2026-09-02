from models.projects import Project

TEST_FILENAME = ("tests", "test")
PENALTY_MISSING_TESTS = 20

class TestAnalyzer:
    """
    Evaluates automated testing support

    Checks whether the project contains a standard test directory and
    records a concern if no automated tests are found
    """
    def analyze(self, project: Project) -> None:
        project.has_tests = any(
            (project.path / folder_name).exists() for folder_name in TEST_FILENAME
        )
        if not project.has_tests:
            project.add_concerns("No test/tests found", PENALTY_MISSING_TESTS)
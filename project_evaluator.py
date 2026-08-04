"""
project_evaluator.py

Analyzes software projects within a specified directory and generates a
report for each one. The tool evaluates common software
development practices by checking for version control, documentation,
automated tests, and unfinished TODO comments. It also identifies the
programming languages used throughout each project and calculates an
overall score based on the results of these checks.

The goal of the Project Evaluator is to automate routine project
audits, helping developers like myself quickly identify missing components, maintain
consistent project standards, and monitor the overall quality of software projects.

"""

import unittest
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List

# Folders we do not want to be scored
IGNORED_DIRECTORY_NAMES = {".git", "__pycache__", "node_modules", "venv", ".venv"}

# File extensions to human-readable language
EXTENSIONS_TO_HUMAN_LANGUAGE = {
    ".py": "Python",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
}

README_FILENAME = ("README.md", "README.txt", "README")
TEST_FILENAME = ("tests", "test")

# Project score penalties, kept as named constants so the scoring policy is visible
PENALTY_MISSING_README = 5
PENALTY_MISSING_GIT = 15
PENALTY_MISSING_TESTS = 20
PENALTY_EXCESSIVE_TODOS = 10
EXCESSIVE_TODO_THRESHOLD = 8 # How many todo's is too many

MAX_PROJECT_SCORE = 100
MIN_PROJECT_SCORE = 0


class Project:
    """
    Represents a single project being evaluated

    Stores all information collected during analysis, including project
    metadata, detected concerns, programming languages, TODO items, and the
    overall score. Each analyzer updates this object as checks are
    performed.
    """
    def __init__(self, name, path):
        """
        Initializes a Project instances.
        :param name: Name of project
        :param path: Path to the project's root directory
        """
        self.name = name
        self.path = path

        self.project_score : int = MAX_PROJECT_SCORE
        self.concerns : List[str] = []
        self.programming_languages : Dict[str, int] = defaultdict(int)
        self.todo_items : List[str] = []

        self.has_git = False
        self.has_readme = False
        self.has_tests = False

    def add_concerns(self, description: str, penalty: int) -> None:
        """
        Records a concern updates the project's overall score

        :param description: Description of the concern
        :param penalty: Number of points deducted from the project score
        """
        self.concerns.append(description)
        self.project_score = max(MIN_PROJECT_SCORE, self.project_score - penalty)


class ProjectScanner:
    """
    Finds software projects within a  directory.

    Scans subdirectories of the provided path and treats each one as a potential project
    """

    def scan(self, directory: Path) -> List[Project]:
        """
        Scans a directory for software projects

        :param directory: Directory containing one or more software projects
        :return: A list of Project objects
        """
        projects = []
        for entry in directory.iterdir():
            if entry.is_dir():
                projects.append(Project(entry.name, entry))

        return projects

class DocumentationAnalyzer:
    """
    Evaluates projects documentation

    Checks whether a project contains a recognized README file and records a
    concern if documentation is missing.
    """
    def analyze(self, project: Project) -> None:
        """
        Evaluates the project's documentation.

        :param project: Project being analyzed
        """
        for filename in README_FILENAME:
            if (project.path / filename).exists():
                project.has_readme = True
                break

        if not project.has_readme:
            project.add_concerns("Missing README documentation", PENALTY_MISSING_README)


class GitAnalyzer:
    """
    Evaluates version control configuration

    Determines whether a project is tracked using Git and records a concern
    if no Git repository is detected.
    """
    def analyze(self, project: Project) -> None:
        project.has_git = (project.path / ".git").exists()

        if not project.has_git:
            project.add_concerns("No Git repository", PENALTY_MISSING_GIT)


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


class CodeAnalyzer:
    """
    Analyzes source code within a project

    Collects information about programming languages used throughout the
    project and identifies unfinished TODO comments that may require
    developer attention.
    """

    def analyze(self, project: Project) -> None:
        """
        Analyzes all source files within a project

        Updates language statistics, records TODO comments, and applies a score
        penalty if the number of TODO items exceeds the configured threshold

        :param project: Project being analyzed
        """
        for file_path in self._source_files(project.path):
            self._record_programming_language(project, file_path)
            self._record_todos(project, file_path)

        if len(project.todo_items) > EXCESSIVE_TODO_THRESHOLD:
            project.add_concerns(
                f"Too many TODOs left in code ({len(project.todo_items)} found)",
                PENALTY_EXCESSIVE_TODOS,
                )

    def _source_files(self, root: Path):
        """
        Iterates over all source files within a project

        Skips directories that should not be analyzed, such as virtual
        environments, cache directories, or other ignored paths

        :param root: Root directory of the project
        """
        for path in root.rglob("*"):
            # Skip if not a file
            if not path.is_file():
                continue
            if any(ignored in path.parts for ignored in IGNORED_DIRECTORY_NAMES):
                continue
            yield path # one at a time

    def _record_programming_language(self, project: Project, file_path: Path) -> None:
        """
        Records the programming language a source file

        The language is determined from the file extension and added to the
        project's language statistics

        :param project: project being analyzed
        :param file_path: source file being analyzed
        """
        language = EXTENSIONS_TO_HUMAN_LANGUAGE.get(file_path.suffix)
        if language is None:
            return
        project.programming_languages[language] += 1

    def _record_todos(self, project: Project, file_path: Path) -> None:
        """
        Searches a source file for TODO comments

        Each TODO comment is recorded

        :param project: project being analyzed
        :param file_path: The file  being scanned for TODO comments
        """
        try:
            text = file_path.read_text()
        except Exception:
            return

        for i, line in enumerate(text.splitlines(), start=1):
            if "TODO" in line:
                project.todo_items.append(f"{file_path.name}:{i}")


class ReportGenerator:
    """
    Generates readable project evaluation reports

    Formats the results collected during analysis into a structured report
    that summarizes project score, detected concerns, supported languages,
    and completed evaluation checks
    """

    def generate(self, projects: List[Project]) -> str:
        """
        Builds a report for all evaluated projects

        :param projects: List of projects
        :return: Formatted report as a string
        """
        sections = [self._render_project(project) for project in projects]
        return "\n".join(sections)


    def _render_project(self, project: Project) -> str:
        """
        Renders a single project's evaluation results

        Creates a summary including completed checks, programming languages,
        TODO items, concerns, and the final score.

        :param project: Project to format
        :return: Formatted report as a string
        """
        lines = ["\n" + "=" * 40, f"Project: {project.name}", "=" * 40, "\nChecks:",
            self._check_line("Git repository", project.has_git),
            self._check_line("README found", project.has_readme),
            self._check_line("Tests found", project.has_tests),
            "\nLanguages:", ]

        lines.append(self._render_programming_languages(project))
        lines.append("\nTODO items:")
        lines.append(self._render_list(project.todo_items, "None found"))
        lines.append("\nConcerns:")
        lines.append(self._render_list(project.concerns, "No concerns"))
        lines.append(f"\nProject Score: {project.project_score}/{MAX_PROJECT_SCORE}")
        return "\n".join(lines)


    @staticmethod
    def _check_line(label: str, passed: bool) -> str:
        """
        Returns an evaluation check
        """
        return f"✓ {label}" if passed else f"✗ {label} missing"


    @staticmethod
    def _render_programming_languages(project: Project) -> str:
        """
        Formats the project's detected programming languages

        :param project: Project whose language statistics will be displayed
        :return: Formatted language summary
        """
        if not project.programming_languages:
            return "No supported languages found"
        return "\n".join(f"{language}: {count} file(s)" for language, count in project.programming_languages.items())

    @staticmethod
    def _render_list(items: List[str], empty_message: str) -> str:
        """
        Returns a formatted list

        :param items: Items to include in the report
        :param empty_message: Message shown when no items are present
        :return: Formatted list or empty message
        """
        if not items:
            return empty_message
        return "\n".join(f"- {item}" for item in items)


class ProjectScoreEvaluator:
    """
    Coordinates the complete project evaluation process.

    Responsible for discovering projects, executing all analyzers, and
    generating the final evaluation report
    """
    def __init__(self) -> None:
        self.scanner = ProjectScanner()
        self.analyzers = [
            DocumentationAnalyzer(),
            GitAnalyzer(),
            TestAnalyzer(),
            CodeAnalyzer(),
        ]
        self.reporter = ReportGenerator()

    def check(self, directory: Path) -> str:
        """
        Evaluates every project within a directory

        Each discovered project is analyzed before a final report is generated

        :param directory: Contains software projects to be analyzed
        :return: Formatted evaluation report
        """
        projects = self.scanner.scan(directory)
        for project in projects:
            for analyzer in self.analyzers:
                analyzer.analyze(project)
        return self.reporter.generate(projects)


def main() -> None:
    folder = input("Enter projects folder: ").strip()
    checker = ProjectScoreEvaluator()
    print(checker.check(Path(folder)))


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


class TestCodeAnalyzer(unittest.TestCase):
    def test_detects_programming_language(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.py").write_text("line1\nline2\nline3\n")
            project = Project("demo", root)

            CodeAnalyzer().analyze(project)

            self.assertEqual(project.programming_languages["Python"], 1)

    def test_finds_todo_comments(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.py").write_text("print('hi')\n# TODO: fix this later\n")
            project = Project("demo", root)

            CodeAnalyzer().analyze(project)

            self.assertEqual(len(project.todo_items), 1)
            self.assertIn("main.py:2", project.todo_items[0])

    def test_ignores_git_directory_contents(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            git_dir = root / ".git"
            git_dir.mkdir()
            (git_dir / "config.py").write_text("# TODO: should never be counted\n")
            project = Project("demo", root)

            CodeAnalyzer().analyze(project)

            self.assertEqual(project.todo_items, [])
            self.assertEqual(project.programming_languages, {})

    def test_excessive_todos_as_concern(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            todo_lines = "\n".join(f"# TODO item {i}" for i in range(EXCESSIVE_TODO_THRESHOLD + 1))
            (root / "main.py").write_text(todo_lines)
            project = Project("demo", root)

            CodeAnalyzer().analyze(project)

            self.assertTrue(any("Too many TODOs left in code" in concern for concern in project.concerns))


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


if __name__ == "__main__":
    import sys
    print("Running automated test suite for project_evaluator.py...\n")
    unittest.main(verbosity=2, argv=[sys.argv[0]])
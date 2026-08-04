"""
project_checker.py

Scans a directory of software projects and gives each one a score based on
a few simple checks: whether it uses version control, has documentation,
includes automated tests, what languages it uses, and how many TODO
comments are still left in the code. All of these checks contribute to an
overall numeric project score.

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
    Represents a single project and stores all results collected during analysis.

    Each analyzer updates the project's fields as it checks different aspects
    of the project. Once analysis is finished, the rest of the system should
    treat the Project as read‑only data.
    """
    def __init__(self, name, path):
        self.name = name
        self.path = path

        self.project_score : int = MAX_PROJECT_SCORE
        self.concern : List[str] = []
        self.programming_languages : Dict[str, int] = defaultdict(int)
        self.todo : List[str] = []

        self.has_git = False
        self.has_readme = False
        self.has_tests = False

    def add_concern(self, description: str, penalty: int) -> None:
        """
        Records a concern found with this project and deducts score.
        :param description: Explanation of the concern found during analysis
        :param penalty: How many  points should be deducted from the project's score because of concern
        :return: None
        """
        self.concern.append(description)
        self.project_score -= max(MIN_PROJECT_SCORE, self.project_score - penalty)


class ProjectScanner:
    """
    Finds project folders inside a given parent directory.

    This scanner looks at the subdirectories of the provided path
    and treats each one as a potential project
    """

    def scan(self, directory: Path) -> List[Project]:
        """Return a Project object for each subfolder inside the given directory."""
        projects = []
        for  entry in directory.iterdir():
            if entry.is_dir():
                projects.append(Project(entry.name, entry))

            return projects

class DocumentationAnalyzer:
    """"
    Checks if a project has a README file.

    Analyzer checks the project's main folder to see if it has a README
    file. It looks for any of the usual README names, and if none are found,
    it marks the project as missing documentation and applies a score penalty
     """
    def analyze(self, project: Project) -> None:
        for filename in README_FILENAME:
            if (project.path / filename).exists():
                project.has_readme = True
                break

            if not project.has_readme:
                project.add_concern("Missing README documentation", PENALTY_MISSING_README)


class GitAnalyzer:
    """Checks if a project is tracked with Git."""

    def analyze(self, project: Project) -> None:
        project.has_git = (project.path / ".git").exists()
        if not project.has_git:
            project.add_concern("No Git repository", PENALTY_MISSING_GIT)


class TestAnalyzer:
    """Checks whether a project has a test/tests folder."""

    def analyze(self, project: Project) -> None:
        project.has_tests = any(
            (project.path / folder_name).exists() for folder_name in TEST_FILENAME
        )
        if not project.has_tests:
            project.add_concern("No test/tests found", PENALTY_MISSING_TESTS)


class CodeAnalyzer:
    """
    Analyzes a project's source files to determine which programming
    languages are used and to collect any TODO comments left in the code.

    This helps identify unfinished work and gives a rough picture of
    how many lines of code is written in each language.
    """

    def analyze(self, project: Project) -> None:
        """
        Checks through all source files in the project and updates its language statistics and TODO list.
        :param project: project being analyzed
        :return: None
        """
        for file_path in self.source_files(project.path):
            self._record_language(project, file_path)
            self._record_todos(project, file_path)

        # Too many todos found in project
        if len(project.todo_items) > EXCESSIVE_TODO_THRESHOLD:
            project.add_concern(
                f"Too many TODOs left in code ({len(project.todo_items)} found)",
                PENALTY_EXCESSIVE_TODOS,
                )

     def source_files(self, root: Path):
        """
        Skips source files

        Skips folders that should not be analyzed, such as virtual
        environments, cache directories, or other ignored paths
        """
        for path in root.rglob("*"):
            # Skip if not a file
            if not path.is_file():
                continue
            if any(ignored in path.parts for ignored in IGNORED_DIRECTORY_NAMES):
                continue
            yield path

    def _record_programming_language(self, project: Project, file_path: Path) -> None:
        """
        Records which programming language the project uses based on the file's
        extension

        :param project: project being analyzed
        :param file_path: The files whose extension is used to identify the language.
        """
        language = EXTENSIONS_TO_HUMAN_LANGUAGE.get(file_path.suffix)
        if language is None:
            return

        if project.languages[language] == 0:
            project.languages[language] = 1

    def _record_todos(self, project: Project, file_path: Path) -> None:
        """
        Scans a file for TODO comments and records each one with its line number.

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
    Turns analyzed Project into a readable report.

    Each project is rendered as its own section, showing the results of all
    checks, the languages detected, any TODOs found, concerns raised, and
    the final project score.
    """

    def generate(self, projects: List[Project]) -> str:
        """
        Build the full report as a single string.
        """
        sections = [self._render_project(project) for project in projects]
        return "\n".join(sections)


    def _render_project(self, project: Project) -> str:
        """
        Renders a single project's results into a readable text block

        Includes checks for Git, README and tests,
        programming language used,
        TODO items,
        concerns raised and
        final project score.
        """
        lines = [
            "\n" + "=" * 40,
            f"Project: {project.name}",
            "=" * 40,
            "\nChecks:",
            self._check_line("Git repository", project.has_git),
            self._check_line("README found", project.has_readme),
            self._check_line("Tests found", project.has_tests),
            "\nLanguages:", ]

        lines.append(self._render_languages(project))
        lines.append("\nTODO items:")
        lines.append(self._render_list(project.todo_items, "None found"))
        lines.append("\nConcerns:")
        lines.append(self._render_list(project.concerns, "No concerns"))
        lines.append(f"\nProject Score: {project.project_score}/{MAX_PROJECT_SCORE}")
        return "\n".join(lines)


    @staticmethod
    def _check_line(label: str, passed: bool) -> str:
        """
        Return a checkmark line, e.g. '✓ README found' or '✗ README missing'.
        """
        return f"✓ {label}" if passed else f"✗ {label} missing"


    @staticmethod
    def _render_languages(project: Project) -> str:
        if not project.languages:
            return "No supported languages found"
        return "\n".join(f"{language}: {lines} lines" for language, lines in project.languages.items())


    @staticmethod
    def _render_list(items: List[str], empty_message: str) -> str:
        if not items:
            return empty_message
        return "\n".join(f"- {item}" for item in items)


class ProjectScoreChecker:
    """
    Handles whole process of scoring projects: scanning a folder,
    running all analyzers, and producing a final report.
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
        Look through the given directory, find all projects inside it,
        analyze each one, and return a full report

        :param directory: Contain projects to be analyzed
        :return: A report summarizing all projects found  in the folder
        """
        projects = self.scanner.scan(directory)
        for project in projects:
            for analyzer in self.analyzers:
                analyzer.analyze(project)
        return self.reporter.generate(projects)


def main() -> None:
    folder = input("Enter projects folder: ").strip()
    checker = ProjectScoreChecker()
    print(checker.check(Path(folder)))




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

class DoucmentationAnalyzer:
    """"
    Checks if a project has a README file.

    Analyzer checks the project's main folder to see if it has a README
    file. It looks for any of the usual README names, and if none are found,
    it marks the project as missing documentation and applies a score penalty
     """
    def analyze(self, project: Project) -> None:
        for filename in README_FILE_NAME:
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

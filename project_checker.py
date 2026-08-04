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

README_FILE_NAME = ("README.md", "README.txt", "README")
TEST_FILE_NAME = ("tests", "test")

# Project score penalties, kept as named constants so the scoring policy is visible
PENALTY_MISSING_README = 5
PENALTY_MISSING_GIT = 15
PENALTY_MISSING_TESTS = 20
PENALTY_EXCESSIVE_TODOS = 10
EXCESSIVE_TODO_THRESHOLD = 8 # How many todo's is too many

MAX_PROJECT_SCORE = 100
MIN_PROJECT_SCORE = 0


class project:
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


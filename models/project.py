from collections import defaultdict
from pathlib import Path
from typing import Dict, List

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

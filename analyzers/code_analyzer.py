from models.projects import Project
from pathlib import Path

# Folders we do not want to be scored
IGNORED_DIRECTORY_NAMES = {".git", "__pycache__", "node_modules", "venv", ".venv"}

# File extensions to human-readable language
EXTENSIONS_TO_HUMAN_LANGUAGE = {
    ".py": "Python",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
}

PENALTY_EXCESSIVE_TODOS = 10
EXCESSIVE_TODO_THRESHOLD = 8 # How many todo's is too many

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
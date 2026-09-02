import unittest
from models.project import Project
from analyzers.code_analyzer import CodeAnalyzer, EXCESSIVE_TODO_THRESHOLD
from tempfile import TemporaryDirectory
from pathlib import Path

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

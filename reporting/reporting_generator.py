from models.project import MAX_PROJECT_SCORE, Project
from typing import List

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
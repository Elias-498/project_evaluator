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

from pathlib import Path
from analyzers.code_analyzer import CodeAnalyzer
from analyzers.test_analyzer import TestAnalyzer
from analyzers.git_analyzer import GitAnalyzer
from analyzers.documentation_analyzer import DocumentationAnalyzer
from reporting.reporting_generator import ReportGenerator
from scanner.project_scanner import ProjectScanner


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

if __name__ == "__main__":
    main()
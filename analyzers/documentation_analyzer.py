from models.projects import Project

README_FILENAME = ("README.md", "README.txt", "README")
PENALTY_MISSING_README = 5 # project score penality for missing README

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

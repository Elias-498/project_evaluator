from models.projects import Project

PENALTY_MISSING_GIT = 15

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

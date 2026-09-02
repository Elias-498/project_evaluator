from models.projects import Project
from pathlib import Path
from typing import List

class ProjectScanner:
    """
    Finds software projects within a  directory.

    Scans subdirectories of the provided path and treats each one as a potential project
    """

    def scan(self, directory: Path) -> List[Project]:
        """
        Scans a directory for software projects

        :param directory: Directory containing one or more software projects
        :return: A list of Project objects
        """
        projects = []
        for entry in directory.iterdir():
            if entry.is_dir():
                projects.append(Project(entry.name, entry))

        return projects


# Project Evaluator

Project Evaluator is a Python-based project analysis and reporting application that evaluates software projects across several key areas. It scans a folder containing multiple projects, analyzes each project, and generates a report highlighting project quality, potential concerns, and an overall score.

## Features

Project Evaluator analyzes projects based on:

- **Git repository** — Checks whether the project is under Git version control.
- **Documentation** — Checks for the presence of a README file.
- **Testing** — Checks whether the project contains tests.
- **Programming languages** — Identifies supported programming languages and counts source files.
- **TODO items** — Searches source code for unfinished TODO items.
- **Project scoring** — Calculates an overall score based on the results of the analysis.
- **Concerns** — Identifies potential issues that may require attention.

## Project Structure

```text
ProjectEvaluator/
│
├── analyzers/
│   ├── code_analyzer.py
│   ├── documentation_analyzer.py
│   ├── git_analyzer.py
│   └── test_analyzer.py
│
├── models/
│   └── project.py
│
├── reporting/
│   └── reporting_generator.py
│
├── scanner/
│   └── project_scanner.py
│
├── tests/
│   ├── test_project.py
│   ├── test_project_scanner.py
│   ├── test_documentation_analyzer.py
│   ├── test_git_analyzer.py
│   ├── test_test_analyzer.py
│   ├── test_code_analyzer.py
│   └── test_project_evaluator.py
│
├── project_evaluator.py
└── README.md
```

## How It Works

The application follows a simple analysis pipeline:

```text
Projects Folder
       │
       ▼
Project Scanner
       │
       ▼
Project Data
       │
       ▼
   Analyzers
   ┌────┼───────────────┐
   ▼    ▼       ▼       ▼
  Git  Docs    Tests   Code
   │    │       │       │
   └────┴───────┴───────┘
             │
             ▼
      Analysis Results
             │
             ▼
       Report Generator
             │
             ▼
     Final Project Report
```

The scanner first identifies the projects contained within the selected folder. Each project is then passed through the appropriate analyzers. The results are collected and used to identify concerns and calculate a project score.

## Running the Application

From the project directory, run:

```bash
python project_evaluator.py
```

You will be prompted to enter the folder containing the projects you want to evaluate:

```text
Enter projects folder: C:\path\to\projects
```

## Example Output

```text
========================================
Project: ProjectEvaluator
========================================

Checks:
✓ Git repository
✓ README found
✓ Tests found

Languages:
Python: 15 file(s)

TODO items:
- analyzers/code_analyzer.py:15

Concerns:
- Too many TODOs left in code (12 found)

Project Score: 90/100
```

## Design

Project Evaluator uses an **object-oriented design** that separates the system into components with clearly defined responsibilities.

Each analyzer is implemented as a separate class, allowing the project to remain modular, maintainable, and easier to extend. Components such as `DocumentationAnalyzer`, `GitAnalyzer`, `TestAnalyzer`, and `CodeAnalyzer` independently evaluate different aspects of a project while working together through well-defined interfaces.

The project also emphasizes **automated testing** to ensure that individual components and their interactions behave as expected. Unit tests are provided for the main components, while integration tests verify that the components work correctly together.

## Project Scanner

The `ProjectScanner` discovers projects within the selected projects folder and collects the files that belong to each project.

## Analyzers

Individual analyzers inspect specific aspects of a project:

- **GitAnalyzer** — Checks Git-related information.
- **DocumentationAnalyzer** — Checks project documentation.
- **TestAnalyzer** — Checks for automated tests.
- **CodeAnalyzer** — Analyzes source code, supported languages, and TODO items.

## Project Model

The `Project` data model stores the information collected during analysis and provides a consistent structure for the rest of the application.

## Report Generator

The reporting component takes the analysis results and generates a readable report containing:

- Project checks
- Detected programming languages
- TODO items
- Potential concerns
- Final project score
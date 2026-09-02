Project Evaluaator
Project Evaluator is a Python-based project analysis and reporting application that evaluates software projects across several key areas. It scans a folder containing multiple projects, analyzes each project, and generates a report highlighting project quality, potential concerns, and an overall score.

Features
Project Evaluator analyzes projects based on:
* Git repository — checks whether the project is under Git version control.
* Documentation — checks for the presence of a README file.
* Testing — checks whether the project contains tests.
* Programming languages — identifies supported programming languages and counts source files.
* TODO items — searches source code for unfinished TODO items.
* Project scoring — calculates an overall score based on the results of the analysis.
* Concerns — identifies potential issues that may require attention.

Project Structure
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

How It Works
The application follows a simple analysis pipeline:

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
Git  Docs   Tests    Code
      │
      ▼
   Analysis Results
      │
      ▼
 Report Generator
      │
      ▼
 Final Project Report

The scanner first identifies the projects contained within the selected folder. Each project is then passed through the appropriate analyzers. The results are collected and used to identify concerns and calculate a project score.

Running the Application
From the project directory, run:
python project_evaluator.py

You will be prompted to enter the folder containing the projects you want to evaluate:
Enter projects folder: C:\path\to\projects

Example Output
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

Design
Project Evaluator uses an object-oriented design that separates the system into components with clearly defined responsibilities. Each analyzer is implemented as a separate class, allowing the project to be maintainable and easier to extend. Components such as the DocumentationAnalyzer, GitAnalyzer, TestAnalyzer, and CodeAnalyzer independently evaluate different aspects of a project while working together through well-defined interfaces.
The project also emphasizes automated testing to ensure that individual components and their interactions behave as expected.

Project Scanner
Discovers projects within the selected projects folder and collects the files that belong to each project.

Analyzers
Individual analyzers inspect specific aspects of a project:
GitAnalyzer — checks Git-related information.
DocumentationAnalyzer — checks project documentation.
TestAnalyzer — checks for tests.
CodeAnalyzer — analyzes source code, supported languages, and TODO items.

Project Model
The project data model stores the information collected during analysis and provides a consistent structure for the rest of the application.

Report Generator
The reporting component takes the analysis results and generates a readable report containing checks, detected languages, TODO items, concerns, and the final project score.

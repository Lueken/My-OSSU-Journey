#!/usr/bin/env python3
"""
This script initializes the OSSU tracker repository structure by:
1. Creating directories for each course
2. Generating a README.md file for each course
3. Creating a status.json file for each course
"""

import os
import json
import shutil
from datetime import datetime
import requests
from pathlib import Path

# OSSU curriculum data - you can extend this as needed
CURRICULUM = {
    "Introduction to Computer Science": [
        {
            "name": "CS50",
            "full_name": "CS50's Introduction to Computer Science",
            "url": "https://cs50.harvard.edu/x",
            "institution": "Harvard University",
            "platform": "edX",
            "category": "Introduction to Computer Science"
        },
        {
            "name": "CS50W",
            "full_name": "CS50's Web Programming with Python and JavaScript",
            "url": "https://cs50.harvard.edu/web/",
            "institution": "Harvard University",
            "platform": "edX",
            "category": "Introduction to Computer Science"
        }
    ],
    "Core Programming": [
        {
            "name": "How to Code - Simple Data",
            "full_name": "How to Code - Simple Data",
            "url": "https://www.edx.org/course/how-to-code-simple-data",
            "institution": "University of British Columbia",
            "platform": "edX",
            "category": "Core Programming"
        },
        {
            "name": "How to Code - Complex Data",
            "full_name": "How to Code - Complex Data",
            "url": "https://www.edx.org/course/how-to-code-complex-data",
            "institution": "University of British Columbia",
            "platform": "edX",
            "category": "Core Programming"
        },
        {
            "name": "Programming Languages A",
            "full_name": "Programming Languages, Part A",
            "url": "https://www.coursera.org/learn/programming-languages",
            "institution": "University of Washington",
            "platform": "Coursera",
            "category": "Core Programming"
        }
    ]
}

def create_directory_if_not_exists(path):
    """Create a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def generate_course_readme(course, output_path):
    """Generate a README.md file for a course."""
    template_path = ".github/templates/course_readme_template.md"
    
    try:
        with open(template_path, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        # Fallback template if file doesn't exist
        template = """# {full_name} - OSSU

## Course Information
- **Platform:** {platform}
- **Institution:** {institution}
- **Course URL:** {url}
- **OSSU Category:** {category}

## Progress Tracker
| Week/Module | Status | Completion Date | Notes |
|-------------|--------|-----------------|-------|
| Week 1      | Not Started | | |
| Week 2      | Not Started | | |
| Week 3      | Not Started | | |

## Projects & Assignments
| Project/Assignment | Status | Repository Link | Completion Date |
|--------------------|--------|-----------------|-----------------|
| Project 1          | Not Started | | |

## Notes
(Add your course notes here)

## Reflections
(Your thoughts about the course)
"""
    
    # Replace placeholders with course information
    content = template.format(**course)
    
    # Write the README.md file
    readme_path = os.path.join(output_path, "README.md")
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print(f"Generated README.md for {course['name']}")

def generate_status_json(course, output_path):
    """Generate a status.json file for a course."""
    status_data = {
        "course_name": course["full_name"],
        "status": "Not Started",
        "progress_percentage": 0,
        "start_date": "",
        "completion_date": "",
        "repo_link": "",
        "notes": "",
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    status_path = os.path.join(output_path, "status.json")
    with open(status_path, 'w') as f:
        json.dump(status_data, f, indent=2)
    
    print(f"Generated status.json for {course['name']}")

def setup_github_directory():
    """Set up the .github directory structure."""
    github_dir = ".github"
    scripts_dir = os.path.join(github_dir, "scripts")
    templates_dir = os.path.join(github_dir, "templates")
    workflows_dir = os.path.join(github_dir, "workflows")
    
    # Create directories
    for directory in [github_dir, scripts_dir, templates_dir, workflows_dir]:
        create_directory_if_not_exists(directory)
    
    # Copy files to appropriate locations
    # Update progress script
    script_path = os.path.join(scripts_dir, "update_progress.py")
    shutil.copyfile("update_progress.py", script_path)
    os.chmod(script_path, 0o755)  # Make executable
    
    # Course README template
    with open(os.path.join(templates_dir, "course_readme_template.md"), 'w') as f:
        try:
            with open("course-template.md", 'r') as template:
                f.write(template.read())
        except FileNotFoundError:
            print("Could not find course-template.md, creating a basic one")
            f.write("# {full_name}\n\n## Course Information\n- **Platform:** {platform}\n- **Institution:** {institution}\n")
    
    # GitHub workflow
    with open(os.path.join(workflows_dir, "update_progress.yml"), 'w') as f:
        try:
            with open("github-workflow.yml", 'r') as workflow:
                f.write(workflow.read())
        except FileNotFoundError:
            print("Could not find github-workflow.yml, skipping workflow setup")

def initialize_repo():
    """Initialize the repository structure."""
    # Set up .github directory
    setup_github_directory()
    
    # Create directories and files for each course
    for category, courses in CURRICULUM.items():
        for course in courses:
            # Create directory with sanitized name
            dir_name = course["name"].replace(" ", "-").lower()
            course_dir = os.path.join(dir_name)
            create_directory_if_not_exists(course_dir)
            
            # Generate files
            generate_course_readme(course, course_dir)
            generate_status_json(course, course_dir)

    print("\nRepository initialization complete!")
    print("Next steps:")
    print("1. Review the generated structure and make any necessary adjustments")
    print("2. Commit the changes to your repository")
    print("3. Start working on your first course!")

if __name__ == "__main__":
    initialize_repo()
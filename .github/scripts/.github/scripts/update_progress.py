#!/usr/bin/env python3
"""
This script updates the main README.md file with progress information from individual course repositories.
It looks for status.json files in course directories or parses README.md files to extract status.
"""

import os
import json
import re
from pathlib import Path

# Define the status levels for courses
STATUS_LEVELS = {
    "Not Started": 0,
    "In Progress": 1,
    "Completed": 2
}

def extract_status_from_readme(readme_path):
    """Extract course status from a README.md file."""
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
            
        # Look for status in the progress tracker table
        status_match = re.search(r'\|\s*Week 1\s*\|\s*([^|]+)\s*\|', content)
        if status_match:
            status = status_match.group(1).strip()
            if status in STATUS_LEVELS:
                return status
        
        # Check for completion date
        completion_match = re.search(r'Completion Date[^\n]*\n[^\n]*\|\s*([^|]+)', content)
        if completion_match and completion_match.group(1).strip() and completion_match.group(1).strip() != '-':
            return "Completed"
            
        return "Not Started"  # Default if nothing is found
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return "Not Started"

def get_course_status(course_dir):
    """Get the status of a course from its directory."""
    status_file = os.path.join(course_dir, "status.json")
    readme_file = os.path.join(course_dir, "README.md")
    
    # Check if status.json exists
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                return status_data.get("status", "Not Started")
        except Exception as e:
            print(f"Error reading {status_file}: {e}")
    
    # Fall back to README.md
    if os.path.exists(readme_file):
        return extract_status_from_readme(readme_file)
    
    return "Not Started"

def get_repo_link(course_dir):
    """Get the repository link for a course if it exists."""
    status_file = os.path.join(course_dir, "status.json")
    
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
                return status_data.get("repo_link", "")
        except Exception:
            pass
    
    return ""

def update_main_readme():
    """Update the main README.md with progress information from course directories."""
    # Read the main README.md
    readme_path = "README.md"
    try:
        with open(readme_path, 'r') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Main README.md not found at {readme_path}")
        return
    
    # Find all course directories (exclude common directories and files)
    excluded_dirs = {'.git', '.github', 'assets', 'scripts'}
    course_dirs = [d for d in os.listdir() if os.path.isdir(d) and d not in excluded_dirs and not d.startswith('.')]
    
    # Update course status in the README
    for course_dir in course_dirs:
        status = get_course_status(course_dir)
        repo_link = get_repo_link(course_dir)
        
        # Extract course name from directory name
        course_name = course_dir.replace('-', ' ').replace('_', ' ')
        
        # Define pattern to find the row for this course in the README
        pattern = rf'\|\s*\[{re.escape(course_name)}.*?\]\(.*?\)\s*\|\s*[^|]*\s*\|\s*[^|]*\s*\|'
        
        # Create the replacement row with updated status and repo link
        if repo_link:
            replacement = f'| [{course_name}](https://www.coursera.org/learn/{course_name.lower().replace(" ", "-")}) | {status} | [Repo]({repo_link}) |'
        else:
            replacement = f'| [{course_name}](https://www.coursera.org/learn/{course_name.lower().replace(" ", "-")}) | {status} | |'
        
        # Update the readme content
        readme_content = re.sub(pattern, replacement, readme_content, flags=re.IGNORECASE)
    
    # Write the updated README
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print("README.md updated successfully!")

if __name__ == "__main__":
    update_main_readme()
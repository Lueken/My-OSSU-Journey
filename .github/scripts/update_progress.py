#!/usr/bin/env python3
"""
Simple script to update the main README.md with progress information from course status.json files.
"""

import os
import json
import re

def update_readme():
    """Update the README.md with course progress information."""
    # Read the current README
    print("Starting README update process...")
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
        print("Successfully read README.md")
    except Exception as e:
        print(f"Error reading README.md: {e}")
        return
    
    # Find all course directories
    course_dirs = [d for d in os.listdir() if os.path.isdir(d) and d not in ['.git', '.github']]
    print(f"Found course directories: {course_dirs}")
    
    # Process each course directory
    for course_dir in course_dirs:
        status_file = os.path.join(course_dir, "status.json")
        print(f"Checking for status file: {status_file}")
        
        # Skip if status.json doesn't exist
        if not os.path.exists(status_file):
            print(f"Status file not found: {status_file}")
            continue
        
        # Read the status.json file
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                status_data = json.load(f)
            
            course_name = status_data.get("course_name", "")
            status = status_data.get("status", "Not Started")
            repo_link = status_data.get("repo_link", "")
            
            print(f"Processing course: {course_name}")
            print(f"Status: {status}")
            print(f"Repo link: {repo_link}")
            
            # Skip if no course name
            if not course_name:
                print("No course name found in status.json, skipping")
                continue
            
            # Prepare the repo link text
            repo_text = f"[Repo]({repo_link})" if repo_link else ""
            
            # Look for the course in the README
            # This pattern is more flexible and will match various formats
            # Convert course name to a more unique pattern by finding key words
            # For example, for "CS50's Introduction to Computer Science" we might search for "CS50" or "Introduction to Computer Science"
            search_terms = [course_name]
            
            # Add variations for CS50 specific matching
            if "CS50" in course_name:
                search_terms.append("CS50")
            
            # Try each search term
            found = False
            for term in search_terms:
                pattern = rf'\|(.*{re.escape(term)}[^\|]*)\|(.*?)\|(.*?)\|'
                matches = re.finditer(pattern, readme_content, re.MULTILINE)
                
                for match in matches:
                    print(f"Found match with term '{term}'")
                    full_match = match.group(0)
                    course_part = match.group(1).strip()
                    status_part = match.group(2).strip()
                    repo_part = match.group(3).strip()
                    
                    # Create replacement with updated status and repo link
                    new_line = f"| {course_part} | {status} | {repo_text} |"
                    
                    # Add remaining parts of the table row
                    # Count pipes in the original match to determine how many more cells we need
                    pipe_count = full_match.count('|')
                    for _ in range(pipe_count - 4):  # -4 for the 3 cells we've already handled plus the starting pipe
                        new_line += " |"
                    
                    print(f"Original line: {full_match}")
                    print(f"New line: {new_line}")
                    
                    # Replace in README content
                    readme_content = readme_content.replace(full_match, new_line)
                    found = True
                    break
                
                if found:
                    break
            
            if not found:
                print(f"WARNING: Could not find course '{course_name}' in README")
                
        except Exception as e:
            print(f"Error processing {status_file}: {e}")
    
    # Write updated README
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("README.md updated successfully!")
    except Exception as e:
        print(f"Error writing to README.md: {e}")

if __name__ == "__main__":
    update_readme()

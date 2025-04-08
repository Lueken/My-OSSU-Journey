#!/usr/bin/env python3
"""
Simplified script to update the main README.md with CS50 course progress information only.
This script is designed for troubleshooting the update process.
"""

import os
import json
import re

def update_cs50_in_readme():
    """Update the README.md with CS50 course progress information only."""
    print("Starting CS50-specific README update process...")
    
    # Define the path to CS50 status.json
    status_file = r"C:\Users\31686\Documents\GitHub\My-OSSU-Journey\.github\scripts\cs50\status.json"
    
    # Check if the status file exists
    if not os.path.exists(status_file):
        print(f"ERROR: Status file not found: {status_file}")
        return
    else:
        print(f"Found status file: {status_file}")
    
    # Read the README.md file
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
        print("Successfully read README.md")
    except Exception as e:
        print(f"ERROR: Could not read README.md: {e}")
        return
    
    # Read the status.json file
    try:
        with open(status_file, "r", encoding="utf-8") as f:
            status_data = json.load(f)
        
        # Extract information
        course_name = status_data.get("course_name", "")
        status = status_data.get("status", "Not Started")
        repo_link = status_data.get("repo_link", "")
        
        print(f"Course name from status.json: {course_name}")
        print(f"Status: {status}")
        print(f"Repository link: {repo_link}")
        
        # Skip if course name is missing
        if not course_name:
            print("ERROR: No course name found in status.json")
            return
        
        # Prepare repository link text
        repo_text = f"[Repo]({repo_link})" if repo_link else ""
        
        # Define search terms for finding CS50 in the README
        search_terms = ["CS50", "Introduction to Computer Science"]
        
        # Search for CS50 in the README
        found = False
        
        for term in search_terms:
            print(f"Searching for term: '{term}'")
            
            # Look for table rows containing the search term
            pattern = rf'\|(.*{re.escape(term)}[^\|]*)\|(.*?)\|(.*?)\|'
            matches = list(re.finditer(pattern, readme_content, re.MULTILINE))
            
            if matches:
                print(f"Found {len(matches)} matches for term '{term}':")
                
                for i, match in enumerate(matches):
                    print(f"  Match {i+1}:")
                    full_match = match.group(0)
                    course_part = match.group(1).strip()
                    status_part = match.group(2).strip()
                    repo_part = match.group(3).strip()
                    
                    print(f"    Full match: '{full_match}'")
                    print(f"    Course part: '{course_part}'")
                    print(f"    Status part: '{status_part}'")
                    print(f"    Repo part: '{repo_part}'")
                    
                    # Create replacement line
                    # Count the total number of cells in the original line
                    cell_count = full_match.count('|') - 1  # -1 because the first | doesn't count as a cell separator
                    
                    # Start building the new line
                    new_line = f"| {course_part} | {status} | {repo_text}"
                    
                    # Add remaining empty cells to match the original format
                    for _ in range(cell_count - 3):  # -3 for the course, status, and repo cells we've already added
                        new_line += " |"
                    
                    print(f"    New line: '{new_line}'")
                    
                    # Perform the replacement
                    old_line = full_match
                    readme_content = readme_content.replace(old_line, new_line)
                    
                    print(f"    Replaced: '{old_line}' with '{new_line}'")
                    found = True
                    break  # Use the first match only
                
                if found:
                    break  # Stop searching if we found and processed a match
    
        if not found:
            print("ERROR: Could not find CS50 course in README.md")
            print("README.md content snippet:")
            print(readme_content[:500] + "...")  # Print first 500 chars as a sample
            return
        
        # Write the updated README
        try:
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            print("SUCCESS: README.md updated successfully!")
        except Exception as e:
            print(f"ERROR: Could not write to README.md: {e}")
            return
            
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {status_file}: {e}")
        return
    except Exception as e:
        print(f"ERROR: Unexpected error processing {status_file}: {e}")
        return

if __name__ == "__main__":
    update_cs50_in_readme()
#!/usr/bin/env python3
"""
CS50W-specific update script for OSSU progress tracking.
This script specifically looks for CS50W status.json in various possible locations
and ensures it only updates the CS50W course entry in README.md.
"""

import os
import json
import re
import sys

def find_cs50w_status_file():
    """
    Find the CS50W status.json file in various possible locations.
    Returns the path if found, None otherwise.
    """
    possible_paths = [
        "cs50w/status.json",  # Repository root
        ".github/scripts/cs50w/status.json",  # Inside .github/scripts
        os.path.expanduser("~/Documents/GitHub/My-OSSU-Journey/cs50w/status.json"),  # Full path in Documents
        os.path.expanduser("~/Desktop/GitHub/My-OSSU-Journey/cs50w/status.json")  # Full path on Desktop
    ]

    print("Searching for CS50W status.json file...")
    for path in possible_paths:
        print(f"Checking path: {path}")
        if os.path.exists(path):
            print(f"Found CS50W status.json at: {path}")
            return path

    print("CS50W status.json file not found in any of the expected locations.")
    return None

def update_cs50w_in_readme(status_file_path):
    """
    Update the README.md with information from the CS50W status.json file.

    Args:
        status_file_path: Path to the CS50W status.json file
    """
    print(f"Starting update process for CS50W using status file: {status_file_path}")

    # Read the README.md file
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
        print("Successfully read README.md")
    except Exception as e:
        print(f"ERROR: Could not read README.md: {e}")
        return

    # Check if the README has a Progress column, if not, add it
    if "| Progress |" not in readme_content:
        print("Adding Progress column to README tables...")
        # Find all tables that have Status column but no Progress column
        tables = re.findall(r'\| Course \| Status \| Repo Link \| Notes \| Completion Date \|[\s\S]*?(?=\n\n|\Z)', readme_content)
        for table in tables:
            # Create new table header with Progress column
            new_header = "| Course | Status | Repo Link | Progress | Notes | Completion Date |"
            # Find the original header in this table
            table_header = re.search(r'\| Course \| Status \| Repo Link \| Notes \| Completion Date \|', table)
            if table_header:
                # Replace the header
                updated_table = table.replace(table_header.group(0), new_header)

                # Update the header separator row
                separator_pattern = r'\|-+\|-+\|-+\|-+\|-+\|'
                separator_match = re.search(separator_pattern, updated_table)
                if separator_match:
                    new_separator = separator_match.group(0).replace("|-", "|-") + "-|"
                    updated_table = updated_table.replace(separator_match.group(0), new_separator)

                # Update all rows in the table to include a Progress column
                rows = re.findall(r'\|.*\|.*\|.*\|.*\|.*\|', updated_table)
                for row in rows:
                    if "| Course |" not in row and "|-" not in row:  # Skip header and separator
                        parts = row.split("|")
                        new_row = "|".join(parts[0:4]) + "| |" + "|".join(parts[4:])
                        updated_table = updated_table.replace(row, new_row)

                # Replace the original table in the README
                readme_content = readme_content.replace(table, updated_table)

        # Save the updated README with the new column
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("Added Progress column to README tables")

        # Read the updated content
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()

    # Read the CS50W status.json file
    try:
        with open(status_file_path, "r", encoding="utf-8") as f:
            status_data = json.load(f)

        # Extract information
        course_name = status_data.get("course_name", "")
        status = status_data.get("status", "Not Started")
        repo_link = status_data.get("repo_link", "")
        progress = status_data.get("progress_percentage", 0)
        notes = status_data.get("notes", "")
        completion_date = status_data.get("completion_date", "")

        print(f"Course name: {course_name}")
        print(f"Status: {status}")
        print(f"Repository link: {repo_link}")
        print(f"Progress: {progress}%")
        print(f"Notes: {notes}")
        print(f"Completion date: {completion_date}")

        # Skip if course name is missing
        if not course_name:
            print("ERROR: No course name found in status.json")
            return

        # Format progress as percentage
        progress_text = f"{progress}%" if progress else ""

        # Prepare repository link text
        repo_text = f"[Repo]({repo_link})" if repo_link else ""

        # Define search terms specific to CS50W
        search_terms = []

        # Add the exact course name from status.json
        if course_name:
            search_terms.append(course_name)

        # Add CS50W-specific search terms
        search_terms.append("CS50's Web Programming")
        search_terms.append("CS50W")
        search_terms.append("Web Programming with Python and JavaScript")

        # Search for CS50W in the README
        found = False

        for term in search_terms:
            print(f"Searching for term: '{term}'")

            # Pattern to match table rows with the search term
            # This handles both the old format (without Progress) and new format (with Progress)
            pattern = rf'\|(.*{re.escape(term)}[^\|]*)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|'
            alt_pattern = rf'\|(.*{re.escape(term)}[^\|]*)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|'

            # Try the full pattern first (with Progress column)
            matches = list(re.finditer(pattern, readme_content, re.MULTILINE))

            # If no match found, try the alternative pattern (without Progress column)
            if not matches:
                matches = list(re.finditer(alt_pattern, readme_content, re.MULTILINE))
                use_alt_pattern = True
            else:
                use_alt_pattern = False

            if matches:
                print(f"Found {len(matches)} matches for term '{term}'")

                for match in matches:
                    full_match = match.group(0)
                    course_part = match.group(1).strip()

                    # Make sure this is actually CS50W and not just CS50
                    # Either "CS50W" or "Web Programming" should be in the course part
                    if "CS50W" not in course_part and "Web Programming" not in course_part:
                        print(f"Skipping match that appears to be regular CS50, not CS50W: '{course_part}'")
                        continue

                    status_part = match.group(2).strip()
                    repo_part = match.group(3).strip()

                    print(f"Original match: '{full_match}'")

                    # Create replacement line based on pattern used
                    if use_alt_pattern:
                        # Old format without Progress column
                        progress_part = ""  # Not in the pattern
                        notes_part = match.group(4).strip()
                        completion_part = match.group(5).strip()

                        # Use notes from status.json if provided, otherwise keep existing notes
                        final_notes = notes if notes else notes_part

                        new_line = f"| {course_part} | {status} | {repo_text} | {final_notes} | {completion_date} |"
                    else:
                        # New format with Progress column
                        progress_part = match.group(4).strip()
                        notes_part = match.group(5).strip()
                        completion_part = match.group(6).strip()

                        # Use notes from status.json if provided, otherwise keep existing notes
                        final_notes = notes if notes else notes_part

                        new_line = f"| {course_part} | {status} | {repo_text} | {progress_text} | {final_notes} | {completion_date} |"

                    print(f"New line: '{new_line}'")

                    # Replace the line in the README
                    readme_content = readme_content.replace(full_match, new_line)
                    found = True
                    break

            if found:
                break

        if not found:
            print(f"WARNING: Could not find CS50W course in README")
            return

        # Write the updated README
        try:
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            print(f"SUCCESS: README.md updated successfully for CS50W!")
        except Exception as e:
            print(f"ERROR: Could not write to README.md: {e}")

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {status_file_path}: {e}")
    except Exception as e:
        print(f"ERROR: Unexpected error processing {status_file_path}: {e}")

if __name__ == "__main__":
    # Check if a status file path was provided as an argument
    if len(sys.argv) > 1:
        status_file_path = sys.argv[1]
        print(f"Using provided path: {status_file_path}")
    else:
        # Try to find the CS50W status.json file automatically
        status_file_path = find_cs50w_status_file()

        if not status_file_path:
            print("ERROR: Could not find CS50W status.json file. Please provide the path as an argument.")
            sys.exit(1)

    update_cs50w_in_readme(status_file_path)
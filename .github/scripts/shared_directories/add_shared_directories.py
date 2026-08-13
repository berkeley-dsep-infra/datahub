import os
import re
from pathlib import Path
from datetime import datetime


def convert_date_to_semester():
    """
    The function uses the current date to determine the semester.
    It returns a string in the format "YYYY-{spring/summer/fall}" representing the semester.
    """

    now = datetime.now()
    year = now.year
    month = now.month

    if 1 <= month <= 4 or month == 12:
        semester = "spring"
    elif 5 <= month <= 7:
        semester = "summer"
    elif 8 <= month <= 11:
        semester = "fall"
    else:
        semester = "unknown"
    return f"{year}-{semester}"


def is_comment_or_blank(line):
    return not line.strip() or line.lstrip().startswith("#")


def insert_courses(yaml_path: Path, course_ids: list, semester: str):
    """
    Inserts (or updates) entries under jupyterhub.custom.bcourses_shared.<semester>, e.g.:

        jupyterhub:
          custom:
            bcourses_shared:
              2025-fall:
                - "course::1234567"
                - "course::1111111"
    """
    with yaml_path.open("r") as f:
        lines = f.readlines()

    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"

    jupyterhub_indent = 0
    custom_indent = jupyterhub_indent + 2
    bcourses_indent = custom_indent + 2
    semester_indent = bcourses_indent + 2
    item_indent = semester_indent + 2

    def find_block_end(start, indent):
        for i in range(start + 1, len(lines)):
            if is_comment_or_blank(lines[i]):
                continue
            line_indent = len(lines[i]) - len(lines[i].lstrip())
            if line_indent <= indent:
                return i
        return len(lines)

    def find_child(start, end, key, indent):
        for i in range(start + 1, end):
            if is_comment_or_blank(lines[i]):
                continue
            stripped = lines[i].lstrip()
            line_indent = len(lines[i]) - len(stripped)
            if line_indent == indent and stripped.startswith(f"{key}:"):
                return i
        return None

    # Step 1: Locate jupyterhub:
    jupyterhub_start = None
    for i, line in enumerate(lines):
        if is_comment_or_blank(line):
            continue
        if line.lstrip().startswith("jupyterhub:") and (len(line) - len(line.lstrip())) == jupyterhub_indent:
            jupyterhub_start = i
            break

    if jupyterhub_start is None:
        lines.append("jupyterhub:\n")
        lines.append(" " * custom_indent + "custom:\n")
        lines.append(" " * bcourses_indent + "bcourses_shared:\n")
        lines.append(" " * semester_indent + f"{semester}:\n")
        semester_start = len(lines) - 1
        semester_end = len(lines)
    else:
        jupyterhub_end = find_block_end(jupyterhub_start, jupyterhub_indent)

        # Step 2: Find or insert custom:
        custom_start = find_child(jupyterhub_start, jupyterhub_end, "custom", custom_indent)
        if custom_start is None:
            custom_start = jupyterhub_end
            lines.insert(jupyterhub_end, " " * custom_indent + "custom:\n")
            jupyterhub_end += 1
        custom_end = find_block_end(custom_start, custom_indent)

        # Step 3: Find or insert bcourses_shared:
        bcourses_start = find_child(custom_start, custom_end, "bcourses_shared", bcourses_indent)
        if bcourses_start is None:
            bcourses_start = custom_end
            lines.insert(custom_end, " " * bcourses_indent + "bcourses_shared:\n")
            custom_end += 1
        bcourses_end = find_block_end(bcourses_start, bcourses_indent)

        # Step 4: Find or insert the semester:
        semester_start = find_child(bcourses_start, bcourses_end, semester, semester_indent)
        if semester_start is None:
            semester_start = bcourses_end
            lines.insert(bcourses_end, " " * semester_indent + f"{semester}:\n")
            bcourses_end += 1
        semester_end = find_block_end(semester_start, semester_indent)

    # Step 5: Collect existing entries under the semester to avoid duplicates
    existing = set()
    for i in range(semester_start + 1, semester_end):
        if is_comment_or_blank(lines[i]):
            continue
        stripped = lines[i].strip()
        if stripped.startswith("-"):
            existing.add(stripped[1:].strip().strip('"').strip("'"))

    # Step 6: Append missing course entries at the end of the semester block
    insert_at = semester_end
    added = []
    for course_id in course_ids:
        key = f"course::{course_id}"
        if key in existing:
            continue
        lines.insert(insert_at, " " * item_indent + f'- "{key}"\n')
        insert_at += 1
        existing.add(key)
        added.append(key)

    # Write back
    with yaml_path.open("w") as f:
        f.writelines(lines)

    if added:
        print(f"Added to bcourses_shared[{semester}]: {', '.join(added)}")
    else:
        print(f"No new bcourses_shared entries added for {semester}; all already present.")


def main():
    # Get environment variables
    hub_name = os.getenv("hub_name")
    course_id = os.getenv("course_id")

    if not hub_name or not course_id:
        raise ValueError("Missing required environment variables: hub_name and course_id")

    # Path to the YAML config
    yaml_path = Path(f"deployments/{hub_name}/config/common.yaml")

    if not yaml_path.exists():
        raise FileNotFoundError(f"Config file not found: {yaml_path}")

    course_ids = [c.strip() for c in re.split(r"[,\s:;]+", course_id) if c.strip()]
    if not course_ids:
        raise ValueError("No valid bCourses IDs found in course_id")

    semester = convert_date_to_semester()
    insert_courses(yaml_path, course_ids, semester)


if __name__ == "__main__":
    main()

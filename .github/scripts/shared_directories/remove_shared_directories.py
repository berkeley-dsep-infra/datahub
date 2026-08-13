import os
import re
from pathlib import Path


def is_comment_or_blank(line):
    return not line.strip() or line.lstrip().startswith("#")


def remove_courses(yaml_path: Path, course_ids: list):
    """
    Removes entries for the given bCourses IDs from every semester under
    jupyterhub.custom.bcourses_shared, e.g.:

        jupyterhub:
          custom:
            bcourses_shared:
              2025-fall:
                - "course::1234567"
                - "course::1111111"

    Cleans up empty semester/bcourses_shared/custom blocks afterwards.
    """
    with yaml_path.open("r") as f:
        lines = f.readlines()

    jupyterhub_indent = 0
    custom_indent = jupyterhub_indent + 2
    bcourses_indent = custom_indent + 2
    semester_indent = bcourses_indent + 2

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
        print("No 'jupyterhub:' block found. Nothing to remove.")
        return
    jupyterhub_end = find_block_end(jupyterhub_start, jupyterhub_indent)

    # Step 2: Locate custom:
    custom_start = find_child(jupyterhub_start, jupyterhub_end, "custom", custom_indent)
    if custom_start is None:
        print("No 'custom:' block found. Nothing to remove.")
        return
    custom_end = find_block_end(custom_start, custom_indent)

    # Step 3: Locate bcourses_shared:
    bcourses_start = find_child(custom_start, custom_end, "bcourses_shared", bcourses_indent)
    if bcourses_start is None:
        print("No 'bcourses_shared:' block found. Nothing to remove.")
        return
    bcourses_end = find_block_end(bcourses_start, bcourses_indent)

    course_keys = {f"course::{cid}" for cid in course_ids}

    # Step 4: Walk each semester block and drop matching course entries
    removed_any = False
    new_bcourses_lines = []
    i = bcourses_start + 1
    while i < bcourses_end:
        line = lines[i]
        if is_comment_or_blank(line):
            new_bcourses_lines.append(line)
            i += 1
            continue

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == semester_indent and re.match(r"^[^\s:]+:\s*$", stripped):
            semester_key_pos = len(new_bcourses_lines)
            new_bcourses_lines.append(line)
            j = i + 1
            while j < bcourses_end:
                if is_comment_or_blank(lines[j]):
                    new_bcourses_lines.append(lines[j])
                    j += 1
                    continue
                item_indent = len(lines[j]) - len(lines[j].lstrip())
                if item_indent <= semester_indent:
                    break
                item_value = lines[j].strip()
                if item_value.startswith("-") and item_value[1:].strip().strip('"').strip("'") in course_keys:
                    removed_any = True
                    j += 1
                    continue
                new_bcourses_lines.append(lines[j])
                j += 1

            has_items = any(
                not is_comment_or_blank(l) and (len(l) - len(l.lstrip())) > semester_indent
                for l in new_bcourses_lines[semester_key_pos + 1:]
            )
            if not has_items:
                del new_bcourses_lines[semester_key_pos]

            i = j
        else:
            new_bcourses_lines.append(line)
            i += 1

    if not removed_any:
        print(f"No matching bcourses_shared entries found for: {', '.join(course_ids)}")
        return

    lines = lines[:bcourses_start + 1] + new_bcourses_lines + lines[bcourses_end:]
    bcourses_end = bcourses_start + 1 + len(new_bcourses_lines)

    # Step 5: Remove bcourses_shared: if it's now empty
    has_content = any(
        not is_comment_or_blank(l) and (len(l) - len(l.lstrip())) > bcourses_indent
        for l in lines[bcourses_start + 1:bcourses_end]
    )
    if not has_content:
        del lines[bcourses_start]
        bcourses_end -= 1
        custom_end -= 1
        print("Removed empty 'bcourses_shared:' section.")

        # Step 6: Remove custom: if it's now empty
        custom_has_content = any(
            not is_comment_or_blank(l) and (len(l) - len(l.lstrip())) > custom_indent
            for l in lines[custom_start + 1:custom_end]
        )
        if not custom_has_content:
            del lines[custom_start]
            print("Removed empty 'custom:' section.")

    # Write back
    with yaml_path.open("w") as f:
        f.writelines(lines)

    print(f"Removed bcourses_shared entries for: {', '.join(course_ids)}")


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

    remove_courses(yaml_path, course_ids)


if __name__ == "__main__":
    main()

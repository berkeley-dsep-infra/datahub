import os
import re
from pathlib import Path



def convert_memory_to_interger(memory_str: str) -> int:
    memory_str = memory_str.strip().upper()
    if memory_str.endswith("GB"):
        return int(memory_str[:-2]) 
    elif memory_str.endswith("G"):
        return int(memory_str[:-1])  
    elif memory_str.endswith("Gi"):
        return int(memory_str[:-2])  # Handle GiB as GB 
    elif memory_str.endswith("MB"):
        return int(memory_str[:-2]) / 1024  # Convert MB to GB
    elif memory_str.endswith("M"):
        return int(memory_str[:-1]) / 1024
    elif memory_str.endswith("Mi"):
        return int(memory_str[:-2]) / 1024 
    else: ## if no unit is provided, use GB 
        return int(memory_str)  # Assume GB if no unit is specified
        


def insert_or_update_group_profile(yaml_path: Path, course_id: str, memory_requested: str, issue_number: str, end_date: str, course_name: str):
    with yaml_path.open("r") as f:
        lines = f.readlines()
    
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'


    course_key = f"course::{course_id}:"
    mem_limit_line = f"mem_limit: {memory_requested}G\n"
    mem_guarantee_line = f"mem_guarantee: to be determined\n"

    jupyterhub_indent = None
    jupyterhub_start = None
    jupyterhub_end = None
    custom_start = None
    group_profiles_start = None
    group_profiles_end = None

    # Step 1: Locate jupyterhub:
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("jupyterhub:"):
            jupyterhub_indent = len(line) - len(stripped)
            jupyterhub_start = i
            break

    if jupyterhub_start is None:
        raise ValueError("Could not find 'jupyterhub:' section")

    # Step 2: Find end of jupyterhub: block
    for i in range(jupyterhub_start + 1, len(lines)):
        stripped = lines[i].lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(lines[i]) - len(stripped)
        if indent <= jupyterhub_indent:
            jupyterhub_end = i
            break
    else:
        jupyterhub_end = len(lines)
  

    # Step 3: Find or insert custom:
    custom_indent = jupyterhub_indent + 2
    group_profiles_indent = custom_indent + 2

    for i in range(jupyterhub_start + 1, jupyterhub_end):
        stripped = lines[i].lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(lines[i]) - len(stripped)
        if stripped.startswith("custom:"):
            custom_start = i
            break

    if custom_start is None:
        custom_start = jupyterhub_end
        lines.insert(custom_start, " " * custom_indent + "custom:\n")
        jupyterhub_end += 1
        print("Inserted 'custom:' block under 'jupyterhub:'")

    # Step 4: Find or insert group_profiles:
    for i in range(custom_start + 1, jupyterhub_end):
        stripped = lines[i].lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(lines[i]) - len(stripped)
        if stripped.startswith("group_profiles:"):
            group_profiles_start = i
            break

    if group_profiles_start is None:
        group_profiles_start = custom_start + 1
        lines.insert(group_profiles_start, " " * group_profiles_indent + "group_profiles:\n")
        jupyterhub_end += 1
        print("Inserted 'group_profiles:' under 'custom:'")

    # Step 5: Find end of group_profiles:
    for i in range(group_profiles_start + 1, len(lines)):
        stripped = lines[i].lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(lines[i]) - len(stripped)
        if indent <= group_profiles_indent:
            group_profiles_end = i
            break
    else:
        group_profiles_end = len(lines)

    # Step 6: Search for course block
    group_indent = group_profiles_indent + 2
    sub_indent = group_indent + 2

    found_course_start = None
    found_course_end = None

    for i in range(group_profiles_start + 1, group_profiles_end):
        stripped = lines[i].lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.rstrip() == course_key:
            found_course_start = i
            j = i + 1
            while j < group_profiles_end:
                sub_stripped = lines[j].lstrip()
                if not sub_stripped or sub_stripped.startswith("#"):
                    j += 1
                    continue
                if (len(lines[j]) - len(sub_stripped)) <= group_indent:
                    break
                j += 1
            found_course_end = j
            break

    if found_course_start is not None:
        # Update existing block
        updated_block = []
        inserted_mem_limit = inserted_mem_guarantee = False

        for i in range(found_course_start, found_course_end):
            stripped = lines[i].strip()
            if stripped.startswith("mem_limit:"):
                updated_block.append(" " * sub_indent + mem_limit_line)
                inserted_mem_limit = True
            elif stripped.startswith("mem_guarantee:"):
                updated_block.append(" " * sub_indent + mem_guarantee_line)
                inserted_mem_guarantee = True
            else:
                updated_block.append(lines[i])

        if not inserted_mem_limit:
            updated_block.append(" " * sub_indent + mem_limit_line)
        if not inserted_mem_guarantee:
            updated_block.append(" " * sub_indent + mem_guarantee_line)

        lines = lines[:found_course_start] + updated_block + lines[found_course_end:]
        print(f"Updated memory settings for existing course::{course_id}")
    else:
        # Insert new block
        block = [
            " " * group_indent + f"{course_key}\n",
            " " * sub_indent + f"## Course Name: {course_name} Bcourses ID: {course_id} End Date: {end_date}\n",
            " " * sub_indent + f"## See issue https://github.com/berkeley-dsep-infra/datahub/issues/{issue_number} for details.\n",
            " " * sub_indent + mem_limit_line,
            " " * sub_indent + mem_guarantee_line
        ]
        lines = lines[:group_profiles_end] + block + lines[group_profiles_end:]
        print(f"Inserted new group profile for course::{course_id}")

    # Final write
    with yaml_path.open("w") as f:
        f.writelines(lines)





def main():
    # Get environment variables
    hub_name = os.getenv("hub_name")
    course_id = os.getenv("course_id")
    mem_requested = os.getenv("memory_requested")
    course_name = os.getenv("course_name").strip()
    issue_number = os.getenv("ISSUE_NUMBER").strip()  
    end_date = os.getenv("end_date").strip()

    if not hub_name or not course_id or not mem_requested or not course_name or not issue_number or not end_date:
        raise ValueError("Missing required environment variables: hub_name, course_id, memory_requested, course_name, ISSUE_NUMBER, or end_date")

    # Path to the YAML config
    yaml_path = Path(f"deployments/{hub_name}/config/common.yaml")

    if not yaml_path.exists():
        raise FileNotFoundError(f"Config file not found: {yaml_path}")
    
    for c_id in re.split(r"[,\s:;]+", course_id):
        if c_id:  # skip empty strings
            insert_or_update_group_profile(yaml_path, c_id, convert_memory_to_interger(mem_requested), issue_number, end_date, course_name)


if __name__ == "__main__":
    main()




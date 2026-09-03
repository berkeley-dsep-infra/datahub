import os
import re
import sys
from datetime import datetime

def read_issue_body(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


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


def extract_issue_fields(issue_body: str):
    lines = issue_body.splitlines()
    data = {}
    current_field = None

    for line in lines:
        line = line.strip()

        if line.startswith("### "):
            # Found a new field header
            current_field = line[4:].strip()
            data[current_field] = None  # Reset for this field
            continue

        # Skip until we get a non-empty value for current field
        if current_field and data[current_field] is None and line:
            data[current_field] = line

    hub_url = data.get("Hub URL", "").strip()
    course_id = data.get("bCourses ID(s)", "").strip()
    end_date = data.get("End Date", "").strip()
    memory = data.get("How much RAM per user is needed?", "").strip()
    course_name = data.get("Affiliated Course Name", "").strip()
    

    return {
        "hub_url": hub_url,
        "course_id": course_id,
        "end_date": end_date,
        "memory": memory,
        "course_name": course_name,
    }


def hub_to_filestore_mapping(hub_name: str) -> str:
    """
    Maps the hub name to the corresponding filestore path.
    """
    mapping = {
        "datahub": "datahub-filestore",
        "r.datahub": "datahub-filestore",
        "a11y": "small-courses-filestore",
        "astro": "small-courses-filestore",
        "biology": "biology-filestore",
        "cee": "small-courses-filestore",
        "data100": "data100-filestore",
        "data101": "data101-filestore",
        "data102": "small-courses-filestore",
        "data8": "data8-filestore",
        "dlab": "small-courses-filestore",
        "eecs": "eecs-filestore",
        "ischool": "small-courses-filestore",
        "julia": "small-courses-filestore",
        "prob140": "small-courses-filestore",
        "publichealth": "small-courses-filestore",
        "stat159": "small-courses-filestore",
        "stat20": "stat20-filestore",
        "nature": "small-courses-filestore",
        "dev": "small-courses-filestore",
        "highschool": "small-courses-filestore",
        "logodev": "small-courses-filestore",
    }
    return mapping.get(hub_name, "")


def main():
    issue_id = os.getenv("ISSUE_NUMBER")
    issue_file_path = sys.argv[1]
    body = read_issue_body(issue_file_path)

    print(f"Extracting course info from issue #{issue_id}")

    course_info = extract_issue_fields(body)
    url = course_info.get("hub_url", "")
    course_id = course_info.get("course_id", "")        
    end_date = course_info.get("end_date", "")
    memory = course_info.get("memory", "")
    course_name = course_info.get("course_name", "")
     
    hub_name = url.split(".")[0] 
    branch = f"issue_{issue_id}"

    filestore = hub_to_filestore_mapping(hub_name)
    filestore_path = f"/export/{filestore}/{hub_name}/prod"
    semester = convert_date_to_semester()


    print(f"Hub Name: {hub_name}\nCourse ID: {course_id}")
    if end_date:
        print(f"End Date: {end_date} \n")
    if memory:
        print(f"Memory Request: {memory} \n")

    outputs = {
        "new_branch": branch,
        "hub_name": hub_name,
        "course_id": course_id,
        "end_date": end_date,
        "memory_requested": memory,
        "filestore_path": filestore_path,
        "semester": semester,
        "course_name": course_name,
    }

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a") as f:
            for key, value in outputs.items():
                f.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()

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


def get_shared_dir_path(staging_or_prod, hub_name, course_id):
    semester = convert_date_to_semester()
    relative_path = f"_shared/{semester}/courses/{course_id}"
    filestore = hub_to_filestore_mapping(hub_name)
    absolute_filestore_path = f"/export/{filestore}/{hub_name}/{staging_or_prod}/{relative_path}"
    return absolute_filestore_path
   

def main():
    staging_or_prod = os.getenv("STAGING_OR_PROD", "")
    hub_name = os.getenv("HUB_NAME", "")
    bcourses_ids = os.getenv("BCOURSES_ID", "")
    shared_dir_paths = []

    for c_id in re.split(r"[,\s:;]+", bcourses_ids):
        if c_id:
            shared_dir_path = get_shared_dir_path(staging_or_prod, hub_name, c_id)
            print(f"HUB_NAME: {hub_name}")
            print(f"STAGING_OR_PROD: {staging_or_prod}")
            print(f"COURSE_ID: {c_id}")
            print(f"Shared directory path: {shared_dir_path}")
            shared_dir_paths.append(shared_dir_path)
    print(f"shared_dir_paths: {shared_dir_paths}")
    outputs = {
        "shared_dir_paths": " ".join(shared_dir_paths),
    }

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a") as f:
            for key, value in outputs.items():
                f.write(f"{key}={value}\n")

if __name__ == "__main__":
    main()

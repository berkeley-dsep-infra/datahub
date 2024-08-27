#!/usr/bin/env python
"""
Get a list of deployments from the deployments/ directory, excluding any
directories specified with the --ignore flag.
"""
import argparse
import os

def main(args):
    for deployment in next(os.walk(args.deployments))[1]:
        if deployment not in args.ignore:
            print(deployment)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a list of deployments from the deployments/ directory.")
    parser.add_argument(
        "--deployments",
        "-d",
        default="deployments",
        help="The directory to search for deployments."
    )
    parser.add_argument(
        "--ignore",
        "-i",
        nargs="*",
        default=[],
        help="Ignore one or more directories in the deployments/ subdir."
    )
    args = parser.parse_args()

    main(args)

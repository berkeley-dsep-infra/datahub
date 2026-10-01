#! /usr/bin/env python
"""
Check the Github environment variables for hub deployments and determine if we
will deploy all hubs or just a subset.

All hubs will be deployed if the environment variable
GITHUB_PR_LABEL_JUPYTERHUB_DEPLOYMENT or GITHUB_PR_LABEL_HUB_IMAGES is set.

Otherwise, the environment variables GITHUB_PR_LABEL_HUB_<HUB_NAME> will be
checked to determine which hubs to deploy.

If no hubs need deploying, nothing will be emitted.
"""

import argparse
import os


def main(args):
    hubs = []

    # Deploy all hubs by getting deployment names from the dirs in deployments/
    if (
        "GITHUB_PR_LABEL_JUPYTERHUB_DEPLOYMENT" in os.environ.keys()
        or "GITHUB_PR_LABEL_HUB_IMAGES" in os.environ.keys()
    ):
        for deployment in next(os.walk(args.deployments))[1]:
            if deployment not in args.ignore:
                hubs.append(deployment)

    # Deploy only the modified/flagged hubs by PR labels
    else:
        hub_labels = [
            k.replace("GITHUB_PR_LABEL_HUB_", "").replace("_", "-").lower()
            for k in os.environ.keys()
            if k.startswith("GITHUB_PR_LABEL_HUB_")
        ]

        # Skip any label whose deployment directory no longer exists. This can
        # happen when one delete a deployment, including its directory and its
        # labeler.yml entry.
        hubs = [
            x
            for x in hub_labels
            if x not in args.ignore and os.path.isdir(os.path.join(args.deployments, x))
        ]

    hubs.sort()
    for h in hubs:
        if args.only_deploy and h not in args.only_deploy:
            continue
        print(h)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get hubs that need to be deployed from environment variables."
    )
    parser.add_argument(
        "--deployments",
        "-d",
        default="deployments",
        help="The directory to search for deployments.",
    )
    parser.add_argument(
        "--ignore",
        "-i",
        nargs="*",
        action="extend",
        default=["template"],
        help="Ignore one or more deployment targets.",
    )
    parser.add_argument(
        "--only-deploy", "-o", nargs="*", help="Only deploy the specified hubs."
    )
    args = parser.parse_args()

    main(args)

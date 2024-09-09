#! /usr/bin/env python3
"""
General tool for mass cloning and syncing of user image repositories.

To use this tool, copy it to a directory in your PATH or run it directly from
this directory.
"""
import argparse
import subprocess
import os

def clone(args):
    """
    Clone all repositories in the config file to the destination directory.

    Optionally set the origin to the user's GitHub.
    """
    with open(args.config) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name = line.split("/")[-1].replace(".git", "")
            path = os.path.join(args.destination, name)
            if os.path.exists(path):
                print(f"Skipping {name} as it already exists.")
                continue
            print(f"Cloning {name} from {line} to {path}...")
            subprocess.check_call(["git", "clone", line, path])

            if args.set_origin:
                print()
                print("Updating remotes and setting origin...")
                if not args.github_user:
                    print("GitHub user not specified. Skipping setting origin.")
                    continue
                print("Renaming origin to upstream...")
                subprocess.check_call(
                    ["git", "remote", "rename", "origin", "upstream"],
                    cwd=path
                )

                origin = line.replace("berkeley-dsep-infra", args.github_user)
                print(f"Setting origin to {origin}...")
                subprocess.check_call(
                    ["git", "remote", "add", "origin", origin],
                    cwd=path
                )

            subprocess.check_call(["git", "remote", "-v"], cwd=path)
            print()

def sync(args):
    """
    Sync all repositories in the config file to the destination directory.

    Optionally push to the user's GitHub (origin).
    """
    with open(args.config) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name = line.split("/")[-1].replace(".git", "")
            path = os.path.join(args.destination, name)
            if not os.path.exists(path):
                print(f"Skipping {name} as it doesn't exist.")
                continue
            print(f"Syncing {name} from {line} in {path}...")
            subprocess.check_call(["git", "switch", "main"], cwd=path)
            subprocess.check_call(["git", "fetch", "--all", "--prune"], cwd=path)
            subprocess.check_call(["git", "rebase", f"upstream/main"], cwd=path)

            if args.push:
                if not args.origin:
                    origin = "origin"
                else:
                    origin = args.origin
                print(f"Pushing {name} to {origin}...")
                subprocess.check_call(["git", "push", origin, "main"], cwd=path)

            print()

def main(args):
    if args.command == "clone":
        clone(args)
    elif args.command == "sync":
        sync(args)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest="command")

    argparser.add_argument(
        "-c",
        "--config",
        default="repos.txt",
        help="Path to file containing list of repositories to clone."
    )
    argparser.add_argument(
        "-d",
        "--destination",
        default=".",
        help="Location of the image repositories."
    )

    sync_parser = subparsers.add_parser(
        "sync",
        help="Sync all image repositories to the latest version."
    )
    sync_parser.add_argument(
        "-p",
        "--push",
        action="store_true",
        help="Push synced repo to a remote."
    )
    sync_parser.add_argument(
        "-o",
        "--origin",
        default="origin",
        help="Origin to push to.  This is optional and defaults to 'origin'."
    )

    clone_parser = subparsers.add_parser(
        "clone",
        help="Clone all image repositories."
    )
    clone_parser.add_argument(
        "-s",
        "--set-origin",
        action="store_true",
        help="Set the origin of the cloned repository to the user's GitHub."
    )
    clone_parser.add_argument(
        "-g",
        "--github-user",
        help="GitHub user to set the origin to."
    )

    args = argparser.parse_args()
    main(args)

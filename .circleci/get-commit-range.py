#!/usr/bin/env python3
import os
import argparse
from github import Github


def from_pr(project, repo, pr_number):
    gh = Github()
    pr = gh.get_repo(f'{project}/{repo}').get_pull(pr_number)
    base = pr.base.sha
    head = pr.base.sha
    return f'{base}...{head}'


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'project',
        default=os.environ['CIRCLE_PROJECT_USERNAME'],
        nargs='?'
    )
    argparser.add_argument(
        'repo',
        default=os.environ['CIRCLE_PROJECT_REPONAME'],
        nargs='?'
    )

    argparser.add_argument(
        '--pr-number',
        type=int,
        nargs='?'
    )

    args = argparser.parse_args()

    if not args.pr_number:
        pr_number = int(os.environ['CIRCLE_PR_NUMBER'])
    else:
        pr_number = args.pr_number
    print(from_pr(args.project, args.repo, pr_number))


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import os
import argparse
from github import Github
import sys


def from_pr(project, repo, pr_number):
    gh = Github()
    pr = gh.get_repo(f'{project}/{repo}').get_pull(pr_number)
    return f'{pr.base.sha}...{pr.head.sha}'

def from_branch(project, repo, branch_name):
    """
    Return commit_range for a PR from a branch name.

    CircleCI doesn't give us the PR Number when making a PR from the same
    repo, rather than a fork. This is terrible. Until this gets fixed,
    we iterate through all open PRs and find the PR we're operating on.
    """
    gh = Github()
    prs = gh.get_repo(f'{project}/{repo}').get_pulls(state='all', sort='updated')
    for pr in prs:
        if pr.base.ref == branch_name:
            return f'{pr.base.sha}...{pr.head.sha}'

    raise ValueError(f'No PR from branch {branch_name} in upstream repo found')



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
    argparser.add_argument(
        '--branch-name',
        nargs='?'
    )

    args = argparser.parse_args()

    pr_number = None
    branch_name = None

    if args.pr_number:
        pr_number = args.pr_number
    else:
        if 'CIRCLE_PR_NUMBER' in os.environ:
            # When PR is from a fork
            pr_number = int(os.environ['CIRCLE_PR_NUMBER'])
        else:
            if args.branch_name:
                branch_name = args.branch_name
            else:
                if 'CIRCLE_COMPARE_URL' in os.environ:
                    # Post merge, where we must have CIRCLE_COMPARE_URL override CIRCLE_BRANCH
                    if '...' in os.environ['CIRCLE_COMPARE_URL']:
                        print(os.environ['CIRCLE_COMPARE_URL'].split('/')[-1])
                        return
                if 'CIRCLE_BRANCH' in os.environ:
                    branch_name = os.environ['CIRCLE_BRANCH']
                else:
                    print("Must provide one of --branch-name or --pr-number", file=sys.stderr)
                    sys.exit(1)

    if pr_number:
        print(from_pr(args.project, args.repo, pr_number))
    elif branch_name:
        print(from_branch(args.project, args.repo, branch_name))
    else:
        raise ValueError('Neither pr_number nor branch were set')


if __name__ == '__main__':
    main()

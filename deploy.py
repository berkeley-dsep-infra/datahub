#!/usr/bin/env python3
import argparse
import subprocess
import yaml


def last_git_modified(path):
    return subprocess.check_output([
        'git',
        'log',
        '-n', '1',
        '--pretty=format:%h',
        path
    ]).decode('utf-8')


def build_user_image(image_name, commit_range=None, push=False):
    if commit_range:
        image_touched = subprocess.check_output([
            'git', 'diff', '--name-only', commit_range, 'user-image',
        ]).decode('utf-8').strip() != ''
        if not image_touched:
            print("user-image not touched, not building")
            return

    tag = last_git_modified('user-image')
    image_spec = image_name + ':' + tag

    subprocess.check_call([
        'docker', 'build', '-t', image_spec, 'user-image'
    ])
    if push:
        subprocess.check_call([
            'docker', 'push', image_spec
        ])
    print('build completed for image', image_spec)

def deploy(release, install):
    # Set up helm!
    subprocess.check_call(['helm', 'repo', 'update'])

    singleuser_tag = last_git_modified('user-image')

    with open('datahub/config.yaml') as f:
        config = yaml.safe_load(f)

    if install:
        helm = [
            'helm', 'install',
            '--name', release,
            '--namespace', release,
            'jupyterhub/jupyterhub',
            '--version', config['version'],
            '-f', 'datahub/config.yaml',
            '-f', 'datahub/secrets.yaml',
            '--set', 'singleuser.image.tag={}'.format(singleuser_tag)
        ]
    else:
        helm = [
            'helm', 'upgrade', release,
            'jupyterhub/jupyterhub',
            '--version', config['version'],
            '-f', 'datahub/config.yaml',
            '-f', 'datahub/secrets.yaml',
            '--set', 'singleuser.image.tag={}'.format(singleuser_tag)
        ]

    subprocess.check_call(helm)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--user-image-spec',
        default='berkeleydsep/datahub-user'
    )
    subparsers = argparser.add_subparsers(dest='action')

    build_parser = subparsers.add_parser('build', description='Build & Push images')
    build_parser.add_argument('--commit-range', help='Range of commits to consider when building images')
    build_parser.add_argument('--push', action='store_true')

    deploy_parser = subparsers.add_parser('deploy', description='Deploy with helm')
    deploy_parser.add_argument('release', default='prod')
    deploy_parser.add_argument('--install', action='store_true')


    args = argparser.parse_args()

    if args.action == 'build':
        build_user_image(args.user_image_spec, args.commit_range, args.push)
    else:
        deploy(args.release, args.install)

main()

#!/usr/bin/env python3
# vim: set et sw=4 ts=4 nonumber:

import argparse
import subprocess
import yaml
import os


def tag_fragment_file(tag):
    tag_fragment = yaml.dump({'singleuser': {'image': {'tag': tag}}})
    filename = '/tmp/tag-{}.yaml'.format(tag)
    with open(filename, 'w') as f:
        f.write(tag_fragment)
    return filename

def helm(*args, **kwargs):
    arg0 = 'helm'
    return subprocess.check_call([arg0] + list(args), **kwargs)

def kubectl(*args, **kwargs):
    arg0 = 'kubectl'
    return subprocess.check_call([arg0] + list(args), **kwargs)

def docker(*args, **kwargs):
    arg0 = 'docker'
    return subprocess.check_call([arg0] + list(args), **kwargs)

def gen_puller_daemonset(image, tag):
    '''Generates a puller daemonset yaml from our template.'''
    image_flt = image.replace('/', '--')
    buf = open('ds-puller.yaml.tmpl').read()
    buf = buf.replace('DOCKER_TAG', tag)
    buf = buf.replace('DOCKER_IMAGE', image)
    buf = buf.replace('DOCKER_SANITIZED_IMAGE', image_flt)
    return buf

def create_puller_daemonset(image_spec):
    '''Creates a daemonset to pull a docker image via kubectl.'''
    image, tag = image_spec.split(':')
    buf = gen_puller_daemonset(image, tag)
    subprocess.run(['kubectl', 'create', '-f', '-'], input=buf.encode(),
        check=True)

def last_git_modified(path, n=1):
    return subprocess.check_output([
        'git',
        'log',
        '-n', str(n),
        '--pretty=format:%h',
        path
    ]).decode('utf-8').split('\n')[-1]

def assemble_child_dockerfile(child_dir, image_spec):
    '''Given {child_dir} and {image_spec}, creates {child_dir}/Dockerfile
    using 'FROM {image_spec}' and {child_dir}/Dockerfile.tail.'''
    header = "FROM {}\n\n".format(image_spec)
    tail = open(os.path.join(child_dir, "Dockerfile.tail")).read()
    f = open(os.path.join(child_dir, "Dockerfile"), 'w')
    f.write(header)
    f.write(tail)
    f.close()

def build_user_image(image_name, commit_range=None, push=False, image_dir='user-image'):
    if commit_range:
        image_touched = subprocess.check_output([
            'git', 'diff', '--name-only', commit_range, image_dir,
        ]).decode('utf-8').strip() != ''
        if not image_touched:
            print("{} not touched, not building".format(image_dir))
            last_image_tag = last_git_modified(image_dir)
            return image_name + ':' + last_image_tag

    # Pull last available version of image to maximize cache use
    try_count = 0
    while try_count < 50:
        last_image_tag = last_git_modified(image_dir, try_count + 1)
        last_image_spec = image_name + ':' + last_image_tag
        try:
            docker('pull', last_image_spec)
            break
        except subprocess.CalledProcessError:
            try_count += 1
            pass

    tag = last_git_modified(image_dir)
    image_spec = image_name + ':' + tag

    docker('build', '--cache-from', last_image_spec, '-t', image_spec,
        image_dir)
    if push:
        docker('push', image_spec)
    print('build completed for image', image_spec)
    return image_spec

def deploy(release, install):
    # Set up helm!
    helm('repo', 'update')

    singleuser_tag = last_git_modified('user-image')

    # We shouldn't use --set because helm converts numeric values to float64
    # https://github.com/kubernetes/helm/issues/1707
    tagfilename = tag_fragment_file(singleuser_tag)

    with open('datahub/config.yaml') as f:
        config = yaml.safe_load(f)

    helm('upgrade', '--install', '--wait',
        release, 'jupyterhub/jupyterhub',
        '--version', config['version'],
        '-f', 'datahub/config.yaml',
        '-f', os.path.join('datahub', 'secrets', release + '.yaml'),
        '-f', tagfilename,
        '--timeout', '3600',
        #'--set', 'singleuser.image.tag={}'.format(singleuser_tag)
    )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--user-image-root',
        default='berkeleydsep/datahub-user'
    )
    subparsers = argparser.add_subparsers(dest='action')

    build_parser = subparsers.add_parser('build',
        description='Build & Push images')
    build_parser.add_argument('--commit-range',
        help='Range of commits to consider when building images')
    build_parser.add_argument('--push', action='store_true')
    build_parser.add_argument('--children', action='append',
        default=['geog187'])

    deploy_parser = subparsers.add_parser('deploy',
        description='Deploy with helm')
    deploy_parser.add_argument('release', default='prod')
    deploy_parser.add_argument('--install', action='store_true')


    args = argparser.parse_args()

    if args.action == 'build':
        image_spec = build_user_image(args.user_image_spec, args.commit_range, args.push, 'user-image')

        # child is built from updated parent
        child = 'geog187'
        assemble_child_dockerfile(child + '-image', image_spec)
        build_user_image(args.user_image_spec + '-' + child,
            args.commit_range, args.push, child + '-image')
    else:
        deploy(args.release, args.install)

main()

#!/usr/bin/env python3
# vim: set et sw=4 ts=4 nonumber:

import argparse
import subprocess
import tempfile
import os

import yaml

def tag_fragment_file(tag):
    '''We can't use --set because helm converts numeric values to float64
       https://github.com/kubernetes/helm/issues/1707
       so we use a fragment file.
    '''
    buf = yaml.dump({'singleuser': {'image': {'tag': tag}}})
    filename = '/tmp/tag-{}.yaml'.format(tag)
    with open(filename, 'w') as f:
        f.write(buf)
    return filename

def extra_image_file(key, tag):
    filename = '/tmp/tag-{}-{}.yaml'.format(key, tag)
    buf = yaml.dump({
        'prePuller': { 'extraImages': {
            key+'-image': {
                'name': 'berkeleydsep/datahub-user-'+key,
                'tag': tag
            }
        }}
    })
    with open(filename, 'w') as f:
        f.write(buf)
    return filename

def configmap_image_users(key, tag):
    '''Return yaml representing the configmap for applying a docker
       image to a user list.'''
    # Load the image's users
    users_filename = os.path.join('datahub', 'secrets',
        'configmap-image-{}.yaml'.format(key))
    users = yaml.load(open(users_filename).read())

    image_spec = 'berkeleydsep/datahub-user-{}:{}'.format(key, tag)
    buf = yaml.dump({
        'hub': { 'extraConfigMap': { 'image': { image_spec: users } } }
    })
    fd, filename = tempfile.mkstemp(text=True)
    with os.fdopen(fd, 'w') as f:
        f.write(buf)
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

def daemonset_exists(image_spec):
    image, tag = image_spec.split(':')
    image_flt = image.replace('/', '--')
    name = 'prepull-{}-{}'.format(image_flt, tag)
    out = subprocess.run(['kubectl', 'get', 'ds', '-o',
        'jsonpath="{.items[0].metadata.labels.name}"'], stdout=subprocess.PIPE)
    return name in out.stdout.decode()


def create_puller_daemonset(image_spec):
    '''Creates a daemonset to pull a docker image via kubectl.'''
    image, tag = image_spec.split(':')
    buf = gen_puller_daemonset(image, tag)
    out = subprocess.run(['kubectl', 'create', '-f', '-'], input=buf.encode(),
        stderr=subprocess.PIPE)
    try:
        out.check_returncode()
    except subprocess.CalledProcessError as e:
        print("kubectl exited with an error.")
        print(out.stderr.decode())
        print()
        print("image: {}, tag: {}".format(image, tag))
        print()
        print("DAEMONSET:")
        print(buf)
        raise


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

def get_object_names(ko, release):
    return subprocess.check_output([
        'kubectl',
        '--namespace', release,
        'get', ko,
        '-o', 'name'
    ]).decode().strip().split('\n')

def test_hub(release):
    ip = subprocess.check_output([
        'kubectl', '--namespace', release,
        'get', 'svc', 'proxy-public',
        '-o', 'jsonpath="{.status.loadBalancer.ingress[*].ip}"'
    ]).decode().strip()

def wait_for_deploy(release):
    # Explicitly wait for all deployments and daemonsets to be fully rolled out
    deployments = get_object_names('deployments', release)
    daemonsets  = get_object_names('daemonsets',  release)
    for d in deployments + daemonsets:
        subprocess.check_call([
            'kubectl', 'rollout', 'status',
            '--namespace', release,
            '--watch', d
        ])

def hub_ip(release):
    return subprocess.check_output([
        'kubectl', '--namespace', release, 'get', 'svc', 'proxy-public',
        '-o', 'jsonpath={.status.loadBalancer.ingress[*].ip}'
    ]).decode().strip()

def deploy(release, install):
    # Set up helm!
    helm('repo', 'update')

    singleuser_tag = last_git_modified('user-image')
    tagfilename = tag_fragment_file(singleuser_tag)

    key = 'geog187'
    tag = last_git_modified(key + '-image')
    # specify image for prepuller
    prepuller_extra = extra_image_file(key, tag)
    # specify users who get assigned the image
    configmap_user_file = configmap_image_users(key, tag)

    config_filename = os.path.join('datahub', 'config.yaml')
    with open(config_filename) as f:
        config = yaml.safe_load(f)

    release_filename = os.path.join('datahub', 'secrets', release + '.yaml')
    with open(release_filename) as f:
        release_config = yaml.safe_load(f)

    helm('upgrade', '--install', '--wait',
        release, 'jupyterhub/jupyterhub',
        '--version', config['version'],
        '--timeout', '3600',
        '-f', config_filename,
        '-f', release_filename,
        '-f', tagfilename,
        '-f', prepuller_extra,
        '-f', configmap_user_file,
    )

    wait_for_deploy(release)

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
        user_image_spec = build_user_image(args.user_image_root,
            args.commit_range, args.push, 'user-image')

        for child in args.children:
            child_dir = child + '-image'
            child_image_root = args.user_image_root + '-' + child
            # child is built FROM user_image_spec
            assemble_child_dockerfile(child_dir, user_image_spec)
            child_image_spec = build_user_image(child_image_root,
                args.commit_range, args.push, child_dir)
    else:
        deploy(args.release, args.install)

main()

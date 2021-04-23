#!/usr/bin/env python3
"""
Lists R packages in one docker image but not the other
"""
import docker
import argparse
import json
from urllib.request import urlopen
from urllib.error import HTTPError

argparser = argparse.ArgumentParser()
argparser.add_argument(
    'src_image',
)

argparser.add_argument(
    'dest_image',
)

args = argparser.parse_args()

client = docker.from_env()


def get_package_info(package_name):
    """
    Return package data for package_name in CRAN repo
    """
    url = f'https://packagemanager.rstudio.com/__api__/repos/1/packages/{package_name}'

    try:
        with urlopen(url) as resp:
            data = json.load(resp)
    except HTTPError as e:
        # Provide an informative exception if we have a typo in package name
        if e.code == 404:
            # Package doesn't exist
            print(f'Package "{package_name}" not found in package manager')
            return { "name": package_name, "version": None }
        else:
            raise
    return data

def packages_list(image_name):
    raw_packages = client.containers.run(
        image_name,
        'R --quiet -e "installed.packages()[,c(1, 3)]"'
    ).decode().split('\n')[2:]

    return set([rp.split()[0] for rp in raw_packages if len(rp.split()) == 3])

def main():
    src_packages = packages_list(args.src_image)
    dest_packages = packages_list(args.dest_image)

    to_be_added =  src_packages - dest_packages

    for p in to_be_added:
        info = get_package_info(p)
        print(f'"{p}", "{info["version"]}",')

if __name__ == '__main__':
    main()

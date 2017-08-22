#!/usr/bin/python

import argparse
import os
import sys
import string
import subprocess

import escapism

safe_chars = set(string.ascii_lowercase + string.digits)
repo = 'https://github.com/data-8/materials-fa17.git'
local_repo = '/export/pool0/homes/_repo'
cwd_tmpl = '/export/pool0/homes/{}'

def safe_username(username):
    return escapism.escape(username, safe=safe_chars, escape_char='-').lower()

def home_directory(username):
    home_dir = cwd_tmpl.format(username)
    if not os.path.exists(home_dir):
        os.mkdir(home_dir)
    return home_dir
        
def git_clone():
    if os.path.exists(os.path.join(local_repo, repo_dirname)):
        return
    out = subprocess.check_output(['git', 'clone', args.repo],
            cwd=local_repo).decode('utf-8')

def copy_repo(username):
    safe = safe_username(username)
    home_dir = home_directory(safe)
    source_dir = os.path.join(local_repo, repo_dirname)
    dest_dir = os.path.join(home_dir, repo_dirname)
    if os.path.exists(dest_dir):
        if args.verbose: print('Skipping {}'.format(safe))
    else:
        if args.verbose: print(safe)
        out = subprocess.check_output(['cp', '-a', source_dir, dest_dir])

# main
parser = argparse.ArgumentParser(description='Pre-pull course assets.')
parser.add_argument('-f', dest='filename', required=True,
            help='File containing user emails')
parser.add_argument('-r', dest='repo', default=repo,
            help='Course asset repo')
parser.add_argument('-v', dest='verbose', action='store_true',
            help='Be verbose.')
args = parser.parse_args()

repo_dirname = os.path.basename(args.repo).split('.')[0]

if not os.path.exists(local_repo):
    os.mkdir(local_repo)

git_clone()

f = open(args.filename)
line = f.readline()
while line != '':
    email = line.strip()
    if '@berkeley.edu' not in email: continue # just in case
    username = email.split('@')[0]
    copy_repo(username)
    line = f.readline()

# vim: set et ts=4 sw=4:

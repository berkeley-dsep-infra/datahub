#!/usr/bin/env python3
"""
Generate required secrets after deployment
"""
from ruamel.yaml import YAML
import secrets
import os
import subprocess
import tempfile
import sys

# Since we'll be modifying and writing back YAML files
yaml = YAML(typ='rt')

def fill_secrets(filepath):
    with open(filepath) as f:
        doc = yaml.load(f)

    doc['jupyterhub']['proxy']['secretToken'] = secrets.token_hex(32)
    doc['jupyterhub']['auth']['state']['cryptoKey'] = secrets.token_hex(32)
    doc['jupyterhub']['hub']['cookieSecret'] = secrets.token_hex(32)

    with tempfile.TemporaryDirectory() as tmpdir:
        key_path = os.path.join(tmpdir, 'hostkey')
        subprocess.check_call([
            'ssh-keygen',
            '-t', 'ed25519',
            '-q', '-N', '""',
            '-f', key_path
        ])
        with open(key_path) as key:
            doc['jupyterhub-ssh']['hostKey'] = key.read()
    with open(filepath, 'w') as f:
        yaml.dump(doc, f)


def main():
    fill_secrets('secrets/staging.yaml')
    fill_secrets('secrets/prod.yaml')

    os.symlink('../datahub/secrets/gke-key.json', 'secrets/gke-key.json')
    os.symlink('../datahub/secrets/gcr-key.json', 'secrets/gcr-key.json')

if __name__ == '__main__':
    main()

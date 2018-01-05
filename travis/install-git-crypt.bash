#!/bin/bash

# Install git-crypt from source since it is not packaged in Ubuntu Trusty.

set -euo pipefail

RELEASE="https://github.com/AGWA/git-crypt/archive/0.6.0.tar.gz"

TARBALL="$(basename ${RELEASE})"
SRC_DIR="git-crypt-${TARBALL/.tar.gz/}"

cd /tmp
curl -LO ${RELEASE}
tar xzf ${TARBALL}
cd ${SRC_DIR}
make

sudo install git-crypt /usr/local/bin

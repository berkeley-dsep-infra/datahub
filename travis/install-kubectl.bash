#!/bin/bash

# Install kubectl.

set -euo pipefail

RELEASE=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
URL="https://storage.googleapis.com/kubernetes-release/release/${RELEASE}/bin/linux/amd64/kubectl"

cd /tmp/
curl -LO ${URL}
sudo install -o root -g root -m 0755 ./kubectl /usr/local/bin/kubectl

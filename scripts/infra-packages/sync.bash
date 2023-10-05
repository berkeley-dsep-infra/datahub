#!/bin/bash
set -euxo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="${SCRIPT_DIR}/../.."

# install file in deployment directories named "image"
find "${ROOT_DIR}/deployments" -type d -name 'image' \
	-exec cp "${SCRIPT_DIR}/requirements.txt" {}/infra-requirements.txt \;

# install file in subdirectories of deployment directories named "images"
for d in $(find "${ROOT_DIR}/deployments" -type d -name images); do
	find $d -not -name images -maxdepth 1 -type d \
		-exec cp "${SCRIPT_DIR}/requirements.txt" {}/infra-requirements.txt \;
done

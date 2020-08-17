#!/bin/bash
set -euxo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="${SCRIPT_DIR}/../.."

find "${ROOT_DIR}/deployments" -type d -name 'image' -exec cp "${SCRIPT_DIR}/requirements.txt" {}/infra-requirements.txt \;

# FIXME: Don't specialcase datahub!
cp ${SCRIPT_DIR}/requirements.txt ${ROOT_DIR}/deployments/datahub/images/default/infra-requirements.txt
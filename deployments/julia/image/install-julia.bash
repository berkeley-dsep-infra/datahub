#!/usr/bin/env bash
set -euo pipefail

JULIA_MAJOR_VERSION='1'
JULIA_MINOR_VERSION='9'
JULIA_PATCH_VERSION='2'

JULIA_MAIN_VERSION='${JULIA_MAJOR_VERSION}.${JULIA_MINOR_VERSION}'
JULIA_FULL_VERSION='${JULIA_MAIN_VERSION}.${JULIA_PATCH_VERSION}'

curl --silent --location --fail https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_MAIN_VERSION}/julia-${JULIA_FULL_VERSION}-linux-x86_64.tar.gz | tar xvz -C ${JULIA_DIR} --strip-components=1

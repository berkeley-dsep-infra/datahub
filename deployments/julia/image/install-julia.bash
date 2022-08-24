#!/usr/bin/env bash
set -euo pipefail

JULIA_URL=https://julialang-s3.julialang.org/bin/linux/x64/1.8/julia-1.8.0-linux-x86_64.tar.gz

curl --silent --location --fail ${JULIA_URL} | tar xvz -C ${JULIA_DIR} --strip-components=1

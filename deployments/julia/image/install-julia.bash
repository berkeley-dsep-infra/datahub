#!/usr/bin/env bash
set -euo pipefail

curl --silent --location --fail https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.7-linux-x86_64.tar.gz | tar xvz -C ${JULIA_DIR} --strip-components=1

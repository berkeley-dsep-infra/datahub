#!/usr/bin/env bash
set -euo pipefail

curl --silent --location --fail https://julialang-s3.julialang.org/bin/linux/x64/1.5/julia-1.5.3-linux-x86_64.tar.gz | tar xvz -C ${JULIA_DIR} --strip-components=1

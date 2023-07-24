#!/usr/bin/env bash
set -euo pipefail

curl --silent --location --fail https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.3-linux-x86_64.tar.gz | tar xvz -C ${JULIA_DIR} --strip-components=1

# https://github.com/JuliaLang/julia/issues/34276#issuecomment-1258691264
rm ${JULIA_DIR}/lib/julia/libstdc++.so.6*
cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ${JULIA_DIR}/lib/julia/

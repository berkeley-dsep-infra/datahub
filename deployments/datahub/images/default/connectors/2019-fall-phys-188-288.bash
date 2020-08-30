#!/bin/bash
set -euo pipefail

cd ${CONDA_DIR}
git clone https://github.com/HerculesJack/assignment-1910
cd assignment-1910
bash install.sh
rm -rf assignment-1910

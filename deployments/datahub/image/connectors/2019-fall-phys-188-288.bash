#!/bin/bash
set -euo pipefail

cd ${APP_DIR}/venv
git clone https://github.com/HerculesJack/assignment-1910
cd assignment-1910
bash install.sh

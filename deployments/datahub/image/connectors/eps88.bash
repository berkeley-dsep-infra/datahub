#!/bin/bash
set -euo pipefail

git clone https://github.com/SciTools/cartopy.git
cd ~/cartopy && python setup.py install
cd ~ && rm -rf cartopy
#!/bin/bash
set -euo pipefail

# nbserver; installed via requirements.txt
jupyter serverextension enable  --sys-prefix --py nbserverproxy

# pycortex can't be installed from the repository at the moment
# ${CONDA_DIR}/bin/pip install git+https://github.com/gallantlab/pycortex@data8

# Installs the cortex library
git clone https://github.com/eickenberg/pycortex.git
cd pycortex
# commit on data8 branch
git checkout b4dd6d860d7c27a846a5445b0df2824429084b44
python setup.py install
cd .. && rm -rf pycortex
rm -rf ~/.config/pycortex

# Install the package nistats (currently not on pypi yet)
cd ~ && git clone https://github.com/nistats/nistats.git
cd ~/nistats && git checkout 5a3a3ed2cbbb088e558838ea7f2a3b9e7735050a
cd ~/nistats && python setup.py install
cd ~ && rm nistats -rf



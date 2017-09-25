#!/bin/bash
set -euo pipefail

# nbserver; installed via requirements.txt
jupyter serverextension enable  --sys-prefix --py nbserverproxy

# pycortex seems to need cython, but isn't explicitly defined as a dependency
pip install --no-cache-dir cython==0.26

# pycortex can't be installed from the repository at the moment
# ${CONDA_DIR}/bin/pip install git+https://github.com/gallantlab/pycortex@data8

# Installs the cortex library
git clone https://github.com/eickenberg/pycortex.git
cd pycortex
# commit on data8 branch
git checkout 4fa348c1309d3c90ed220c6811f0fee617ea83a9
python setup.py install
cd .. && rm -rf pycortex

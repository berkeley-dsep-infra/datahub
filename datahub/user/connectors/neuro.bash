#!/bin/bash

# nbserver; installed via requirements.txt
jupyter serverextension enable  --sys-prefix --py nbserverproxy

# pycortex can't be installed from the repository at the moment
# ${CONDA_DIR}/bin/pip install git+https://github.com/gallantlab/pycortex@data8

# Installs the cortex library
git clone https://github.com/gallantlab/pycortex
cd pycortex
# commit on data8 branch
git checkout d570713
${CONDA_DIR}/bin/python setup.py install
cd .. && rm -rf pycortex

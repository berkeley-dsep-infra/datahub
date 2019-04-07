#!/bin/bash
set -e

cd /tmp
git clone git://github.com/minrk/nbextension-scratchpad
cd nbextension-scratchpad/
git checkout e92fa23
cd ..
jupyter nbextension install --sys-prefix nbextension-scratchpad
jupyter nbextension enable --sys-prefix nbextension-scratchpad/main
cd .. 

pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --sys-prefix
jupyter nbextension enable execute_time/ExecuteTime

rm -rf /tmp/nbextension-scratchpad

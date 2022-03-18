#!/bin/bash
set -e

cd /tmp
git clone https://github.com/minrk/nbextension-scratchpad
cd nbextension-scratchpad/
git checkout e92fa23
cd ..
jupyter nbextension install --sys-prefix nbextension-scratchpad
jupyter nbextension enable  --sys-prefix nbextension-scratchpad/main
cd ..
rm -rf /tmp/nbextension-scratchpad

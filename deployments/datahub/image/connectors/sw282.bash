#!/bin/bash

# Issue #929

set -euo pipefail

git clone https://github.com/yuvipanda/gradable-nbexport.git
cd ~/gradable-nbexport && python setup.py install
cd ~ && rm -rf gradable-nbexport

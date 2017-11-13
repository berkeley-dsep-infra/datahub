#!/bin/bash
set -euo pipefail

URL="https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz"
ARCHIVE=$(basename ${URL})

cd /tmp

curl -L -O ${URL}
tar xaf ${ARCHIVE}
cp -p wkhtmltox/bin/wkhtmltopdf /srv/app/venv/bin/

rm -rf wkhtmltox ${ARCHIVE}

# Install PAUP* for BIO 1B
# https://github.com/berkeley-dsep-infra/datahub/issues/1699

# This package was requested in 2020 for the instructor to try out.
# The 168 version doesn't exist so I've bumped it to 169, but also disabled
# it in case the package is no longer needed.
return

wget https://phylosolutions.com/paup-test/paup4a169_ubuntu64.gz -O ${CONDA_DIR}/bin/paup.gz
gunzip ${CONDA_DIR}/bin/paup.gz
chmod +x ${CONDA_DIR}/bin/paup

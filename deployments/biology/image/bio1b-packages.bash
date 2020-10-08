# Install PAUP* for BIO 1B
# https://github.com/berkeley-dsep-infra/datahub/issues/1699
wget http://phylosolutions.com/paup-test/paup4a168_ubuntu64.gz -O ${CONDA_DIR}/bin/paup.gz
gunzip ${CONDA_DIR}/bin/paup.gz
chmod +x ${CONDA_DIR}/bin/paup

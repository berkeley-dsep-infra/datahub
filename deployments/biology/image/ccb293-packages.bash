# Install QIIME2 for CCB293
# https://github.com/berkeley-dsep-infra/datahub/issues/1699
wget https://data.qiime2.org/distro/core/qiime2-2021.8-py38-linux-conda.yml
mamba env create -n qiime2 --file qiime2-2021.8-py38-linux-conda.yml && mamba clean -afy
rm qiime2-2021.8-py38-linux-conda.yml

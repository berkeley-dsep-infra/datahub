#!/bin/bash

#
# Download and install a pinned version of mambaforge.
#

set -ex

cd $(dirname $0)
MAMBAFORGE_VERSION=23.1.0-1

URL="https://github.com/conda-forge/miniforge/releases/download/${MAMBAFORGE_VERSION}/Mambaforge-${MAMBAFORGE_VERSION}-Linux-x86_64.sh"
INSTALLER_PATH=/tmp/mambaforge-installer.sh

wget --quiet $URL -O ${INSTALLER_PATH}
chmod +x ${INSTALLER_PATH}

bash ${INSTALLER_PATH} -b -p ${CONDA_DIR}
export PATH="${CONDA_DIR}/bin:$PATH"

# Do not attempt to auto update conda or dependencies
conda config --system --set auto_update_conda false
conda config --system --set show_channel_urls true

# Empty the conda history file, which seems to result in some effective pinning
# of packages in the initial env, which we don't intend. This file must not be
# removed.
> ${CONDA_DIR}/conda-meta/history

# Clean things out!
conda clean --all -f -y

# Remove the big installer so we don't increase docker image size too much
rm ${INSTALLER_PATH}

# Remove the pip cache created as part of installing mambaforge
rm -rf ${HOME}/.cache

chown -R $NB_USER:$NB_USER ${CONDA_DIR}

conda list -n root

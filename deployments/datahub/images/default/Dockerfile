FROM buildpack-deps:jammy-scm

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000

ENV CONDA_DIR /srv/conda
ENV R_LIBS_USER /srv/r

RUN apt-get -qq update --yes && \
    apt-get -qq install --yes locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Install all apt packages
COPY apt.txt /tmp/apt.txt
RUN apt-get -qq update --yes && \
    apt-get -qq install --yes --no-install-recommends \
        $(grep -v ^# /tmp/apt.txt) && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*

# Create user owned R libs dir
# This lets users temporarily install packages
RUN install -d -o ${NB_USER} -g ${NB_USER} ${R_LIBS_USER}

# Install R.
# These packages must be installed into the base stage since they are in system
# paths rather than /srv.
# Pre-built R packages from rspm are built against system libs in jammy.
ENV R_VERSION=4.3.2-1.2204.0
ENV LITTLER_VERSION=0.3.18-2.2204.0
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/" > /etc/apt/sources.list.d/cran.list
RUN curl --silent --location --fail https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc > /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
RUN apt-get update --yes > /dev/null && \
    apt-get install --yes -qq r-base-core=${R_VERSION} r-base-dev=${R_VERSION} littler=${LITTLER_VERSION} > /dev/null

#ENV RSTUDIO_URL https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2023.06.0-421-amd64.deb
ENV RSTUDIO_URL https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2023.12.0-369-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    apt install --no-install-recommends --yes /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

ENV SHINY_SERVER_URL https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.20.1002-amd64.deb
RUN curl --silent --location --fail ${SHINY_SERVER_URL} > /tmp/shiny-server.deb && \
    apt install --no-install-recommends --yes /tmp/shiny-server.deb && \
    rm /tmp/shiny-server.deb

# Install our custom Rprofile.site file
COPY Rprofile.site /usr/lib/R/etc/Rprofile.site
# Create directory for additional R/RStudio setup code
RUN mkdir /etc/R/Rprofile.site.d
# RStudio needs its own config
COPY rsession.conf /etc/rstudio/rsession.conf

# R_LIBS_USER is set by default in /etc/R/Renviron, which RStudio loads.
# We uncomment the default, and set what we wanna - so it picks up
# the packages we install. Without this, RStudio doesn't see the packages
# that R does.
# Stolen from https://github.com/jupyterhub/repo2docker/blob/6a07a48b2df48168685bb0f993d2a12bd86e23bf/repo2docker/buildpacks/r.py
# To try fight https://community.rstudio.com/t/timedatectl-had-status-1/72060,
# which shows up sometimes when trying to install packages that want the TZ
# timedatectl expects systemd running, which isn't true in our containers
RUN sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
    echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron && \
    echo "TZ=${TZ}" >> /etc/R/Renviron

# For command-line access to quarto, which is installed by rstudio.
RUN ln -s /usr/lib/rstudio-server/bin/quarto/bin/quarto /usr/local/bin/quarto

# Install R libraries as our user
USER ${NB_USER}

COPY class-libs.R /tmp/class-libs.R
RUN mkdir -p /tmp/r-packages

# Install all our base R packages
COPY install.R  /tmp/install.R
RUN echo "/tmp/install.R" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

# DLAB CTAWG, Fall '20 - Summer '21
# https://github.com/berkeley-dsep-infra/datahub/issues/1942
COPY r-packages/dlab-ctawg.r /tmp/r-packages/
RUN echo "/usr/bin/r /tmp/r-packages/dlab-ctawg.r" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

# Econ 140, Fall '22 and into the future
# https://github.com/berkeley-dsep-infra/datahub/issues/3757
COPY r-packages/econ-140.r /tmp/r-packages
RUN echo "/usr/bin/r /tmp/r-packages/econ-140.r" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

# EEP/IAS C119, Spring '23
# https://github.com/berkeley-dsep-infra/datahub/issues/4203
COPY r-packages/eep-1118.r /tmp/r-packages
RUN echo "/usr/bin/r /tmp/r-packages/eep-1118.r" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

# Stat 135, Fall '23
# https://github.com/berkeley-dsep-infra/datahub/issues/4907
COPY r-packages/2023-fall-stat-135.r /tmp/r-packages
RUN echo "/usr/bin/r /tmp/r-packages/2023-fall-stat-135.r" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

# MBA 247, Fall '23
# issue TBD; discussed over email
COPY r-packages/2023-fall-mba-247.r /tmp/r-packages/
RUN echo "/usr/bin/r /tmp/r-packages/2023-fall-mba-247.r" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

# POL SCI 3, SP 24
# https://github.com/berkeley-dsep-infra/datahub/issues/5496
COPY r-packages/2024-sp-polsci-3.r /tmp/r-packages/
RUN echo "/usr/bin/r /tmp/r-packages/2024-sp-polsci-3.r" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN rm -rf /tmp/downloaded_packages

ENV PATH ${CONDA_DIR}/bin:$PATH:/usr/lib/rstudio-server/bin

# Set this to be on container storage, rather than under $HOME ENV IPYTHONDIR ${CONDA_DIR}/etc/ipython

WORKDIR /home/${NB_USER}

# Install mambaforge as root
USER root
COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN echo "/tmp/install-mambaforge.bash" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash

# Install conda environment as our user
USER ${NB_USER}

COPY infra-requirements.txt /tmp/infra-requirements.txt
COPY environment.yml /tmp/environment.yml

RUN echo "/srv/conda/bin/mamba env update -p ${CONDA_DIR} -f /tmp/environment.yml" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN echo "/srv/conda/bin/mamba clean -afy" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash
RUN echo "/srv/conda/bin/pip install --no-cache -r /tmp/infra-requirements.txt" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash

# 2024-01-13 sknapp: incompatible due to notebook 7
# RUN jupyter contrib nbextensions install --sys-prefix --symlink && \
#     jupyter nbextensions_configurator enable --sys-prefix

# Used by MCB32, but incompatible with ipywidgets 8.x
# RUN jupyter nbextension enable --py --sys-prefix qgrid

# install chromium browser for playwright
# https://github.com/berkeley-dsep-infra/datahub/issues/5062
# playwright is only availalbe in nbconvert[webpdf], via pip/pypi.
# see also environment.yaml
# DH-164
ENV PLAYWRIGHT_BROWSERS_PATH ${CONDA_DIR}
RUN playwright install chromium

# Install IR kernelspec
RUN echo "/usr/bin/r -e \"IRkernel::installspec(user = FALSE, prefix='${CONDA_DIR}')\"" | /usr/bin/time -f "User\t%U\nSys\t%S\nReal\t%E\nCPU\t%P" /usr/bin/bash

# 2024-01-13 sknapp: incompatible due to notebook 7
# COPY d8extension.bash /usr/local/sbin/d8extension.bash
# RUN /usr/local/sbin/d8extension.bash

ENV NLTK_DATA ${CONDA_DIR}/nltk_data
COPY connectors/text.bash /usr/local/sbin/connector-text.bash
RUN /usr/local/sbin/connector-text.bash

#COPY connectors/2021-fall-phys-188-288.bash /usr/local/sbin/
#RUN /usr/local/sbin/2021-fall-phys-188-288.bash

# clear out /tmp
USER root
RUN rm -rf /tmp/*

USER ${NB_USER}

EXPOSE 8888

ENTRYPOINT ["tini", "--"]

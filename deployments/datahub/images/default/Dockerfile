FROM buildpack-deps:focal-scm

ENV CONDA_DIR /opt/conda

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000


RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Create user owned R libs dir
# This lets users temporarily install packages
ENV R_LIBS_USER /opt/r
RUN install -d -o ${NB_USER} -g ${NB_USER} ${R_LIBS_USER}

RUN apt-get -qq update --yes && \
    apt-get -qq install --yes \
            tar \
            vim \
            micro \
            mc \
            locales > /dev/null

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Generic development tools
RUN apt-get update > /dev/null && \
    apt-get -qq install --yes \
            build-essential

# for nbconvert
# FIXME: Understand what exactly we want
# texlive-plain-generic is new name of texlive-generic-recommended
RUN apt-get update > /dev/null && \
    apt-get -qq install --yes \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-plain-generic > /dev/null

RUN apt-get update > /dev/null && \
    apt-get -qq install --yes \
            # for LS88-5 and modules basemap
            libspatialindex-dev \
            # for cartopy
            libgeos-dev \
            libproj-dev \
            proj-data \
            proj-bin \
            # For L&S22
            graphviz \
            # for phys 151
            gfortran \
            # for eps 109; fall 2019
            ffmpeg  \
            # for data100
            libpq-dev \
            postgresql-client > /dev/null

# Install packages needed by notebook-as-pdf
# Default fonts seem ok, we just install an emoji font
RUN apt-get update && \
    apt-get install --yes \
            libx11-xcb1 \
            libxtst6 \
            libxrandr2 \
            libasound2 \
            libpangocairo-1.0-0 \
            libatk1.0-0 \
            libatk-bridge2.0-0 \
            libgtk-3-0 \
            libnss3 \
            libxss1 \
            fonts-noto-color-emoji > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use newer version of R
# Binary packages from packagemanager.rstudio.com work against this.
# Base R from Focal is only 3.6.
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" > /etc/apt/sources.list.d/cran.list

# Install R packages
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
    r-base \
    r-base-dev \
    r-recommended \
    r-cran-littler  > /dev/null


# Needed by RStudio
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        psmisc \
        sudo \
        libapparmor1 \
        lsb-release \
        libclang-dev  > /dev/null
            
# apt packages needed for R packages
RUN apt update --yes > /dev/null && \
    apt install --no-install-recommends --yes \
    # R package qpdf
    libpoppler-cpp-dev \
    # R package imager
    libx11-dev libglpk-dev libgmp3-dev libxml2-dev \
    # R package units
    libudunits2-dev \
    # R package sf
    libgdal-dev libproj-dev gdal-bin \
    # R package magick
    libmagick++-dev imagemagick > /dev/null

# 1.3.959 is latest version that works with jupyter-rsession-proxy
# See https://github.com/jupyterhub/jupyter-rsession-proxy/issues/93#issuecomment-725874693
ENV RSTUDIO_URL https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.3.959-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

ENV SHINY_SERVER_URL https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.15.953-amd64.deb
RUN curl --silent --location --fail ${SHINY_SERVER_URL} > /tmp/shiny-server.deb && \
    dpkg -i /tmp/shiny-server.deb && \
    rm /tmp/shiny-server.deb

# Set CRAN mirror to rspm before we install anything
COPY Rprofile.site /usr/lib/R/etc/Rprofile.site
# RStudio needs its own config
COPY rsession.conf /etc/rstudio/rsession.conf

# R_LIBS_USER is set by default in /etc/R/Renviron, which RStudio loads.
# We uncomment the default, and set what we wanna - so it picks up
# the packages we install. Without this, RStudio doesn't see the packages
# that R does.
# Stolen from https://github.com/jupyterhub/repo2docker/blob/6a07a48b2df48168685bb0f993d2a12bd86e23bf/repo2docker/buildpacks/r.py
RUN sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
    echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron

# Install R libraries as our user
USER ${NB_USER}

COPY class-libs.R /tmp/class-libs.R
# Install all our base R packages
COPY install.R  /tmp/install.R
RUN /tmp/install.R && \
    rm -rf /tmp/downloaded_packages

RUN mkdir -p /tmp/r-packages

# pdftools
COPY r-packages/dlab-ctawg.r /tmp/r-packages/
RUN r /tmp/r-packages/dlab-ctawg.r

COPY r-packages/2019-fall-stat-131a.r /tmp/r-packages
RUN r /tmp/r-packages/2019-fall-stat-131a.r

COPY r-packages/eep-1118.r /tmp/r-packages
RUN r /tmp/r-packages/eep-1118.r

COPY r-packages/ias-c188.r /tmp/r-packages
RUN r /tmp/r-packages/ias-c188.r

COPY r-packages/ph-142.r /tmp/r-packages
RUN r /tmp/r-packages/ph-142.r

COPY r-packages/stat-131a.r /tmp/r-packages
RUN r /tmp/r-packages/stat-131a.r

COPY r-packages/2020-spring-envecon-c118.r /tmp/r-packages/
RUN r /tmp/r-packages/2020-spring-envecon-c118.r

COPY r-packages/econ-140.r /tmp/r-packages/
RUN r /tmp/r-packages/econ-140.r

COPY r-packages/ph-290.r /tmp/r-packages/
RUN r /tmp/r-packages/ph-290.r

COPY r-packages/2021-spring-phw-272a.r /tmp/r-packages/
RUN r /tmp/r-packages/2021-spring-phw-272a.r

COPY r-packages/2021-spring-stat-20.r /tmp/r-packages/
RUN r /tmp/r-packages/2021-spring-stat-20.r

COPY r-packages/2021-spring-espm-288.r /tmp/r-packages/
RUN r /tmp/r-packages/2021-spring-espm-288.r

COPY r-packages/ib161.r /tmp/r-packages/
RUN r /tmp/r-packages/ib161.r

ENV PATH ${CONDA_DIR}/bin:$PATH:/usr/lib/rstudio-server/bin

# Set this to be on container storage, rather than under $HOME ENV IPYTHONDIR ${CONDA_DIR}/etc/ipython

WORKDIR /home/${NB_USER}

# Install miniforge as root
USER root
COPY install-miniforge.bash /tmp/install-miniforge.bash
RUN /tmp/install-miniforge.bash

# Install conda environment as our user
USER ${NB_USER}

COPY environment.yml /tmp/environment.yml

RUN conda env update -p ${CONDA_DIR} -f /tmp/environment.yml

COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN pip install --no-cache -r /tmp/infra-requirements.txt
RUN jupyter contrib nbextensions install --sys-prefix --symlink && \
    jupyter nbextensions_configurator enable --sys-prefix


# Install jupyterlab extensions immediately after infra-requirements
# This hopefully prevents re-installation all the time
# `jlpm` calls out to yarn internally, and we tell it to
# use a temporary cache. This reduces file size,
# but also prevents strange permission errors -
# like https://app.circleci.com/pipelines/github/berkeley-dsep-infra/datahub/1176/workflows/7f49851f-c2fc-46ca-b887-15d8e5612097/jobs/13584
RUN jlpm cache dir && mkdir -p /tmp/yarncache && \
    jlpm config set cache-folder /tmp/yarncache && \
    jupyter labextension install --debug \
        @jupyterlab/server-proxy \
        jupyterlab-plotly@4.14.3 plotlywidget@4.14.3 \
        @jupyterlab/geojson-extension && \
    rm -rf /tmp/yarncache

RUN pip install --no-cache numpy==1.19.5 cython==0.29.21

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt

# Hack to get PyMC3 working for Data 102 & Astro 128/256
# These are the same versions as in requirements.txt, but
# the import fails unless you uninstall and reinstall
# See https://github.com/berkeley-dsep-infra/datahub/issues/2207
RUN pip uninstall Theano Theano-PyMC pymc3 -y
RUN pip install --no-cache 'Theano==1.0.5'
RUN pip install --no-cache 'pymc3==3.11.0'

# Set up nbpdf dependencies
ENV PYPPETEER_HOME ${CONDA_DIR}
RUN pyppeteer-install

# Install IR kernelspec
RUN r -e "IRkernel::installspec(user = FALSE, prefix='${CONDA_DIR}')"

COPY d8extension.bash /usr/local/sbin/d8extension.bash
RUN /usr/local/sbin/d8extension.bash

ENV NLTK_DATA ${CONDA_DIR}/nltk_data
COPY connectors/text.bash /usr/local/sbin/connector-text.bash
RUN /usr/local/sbin/connector-text.bash

COPY connectors/sw282.bash /usr/local/sbin/connector-sw282.bash
RUN /usr/local/sbin/connector-sw282.bash
ADD ipython_config.py ${IPYTHONDIR}/ipython_config.py

# install QGrid notebook extension
RUN jupyter nbextension enable --py --sys-prefix qgrid


EXPOSE 8888

# Temporarily install new nbconvert version to fix pagination in PDF generation
# This can't be in infra-requirements, since that seems to just install the
# published versions of nbconvert from notebook. Adding this to the end of the
# image so we can experiment with this faster.
# Brings in https://github.com/jupyter/nbconvert/pull/1513
# Brings in https://github.com/jupyter/nbconvert/pull/1515
# Brings in https://github.com/jupyter/nbconvert/pull/1516
RUN pip install --no-cache git+https://github.com/yuvipanda/nbconvert@888f39b9fe131f8af403a9396538996afbfd7aa2

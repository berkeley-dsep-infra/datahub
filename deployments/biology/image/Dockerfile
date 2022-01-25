FROM buildpack-deps:focal-scm

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000

ENV CONDA_DIR /opt/conda
ENV R_LIBS_USER /opt/r

# Explicitly add littler to PATH
# See https://github.com/conda-forge/r-littler-feedstock/issues/6
ENV PATH ${CONDA_DIR}/lib/R/library/littler/bin:${CONDA_DIR}/bin:$PATH

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Create user owned R libs dir
# This lets users temporarily install packages
RUN mkdir -p ${R_LIBS_USER} && chown ${NB_USER}:${NB_USER} ${R_LIBS_USER}

# Required for PAUP*
# Note that this doesn't actually install python2, thankfully
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
        libpython2.7 > /dev/null

## libraries required for mothur
## libreadline6 required
#RUN apt-get update -qq --yes > /dev/null && \
#    apt-get install --yes -qq \
#    libreadline6-dev > /dev/null

## library required for fast-PCA & https://github.com/DReichLab/EIG
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        libgsl-dev >/dev/null

## library required for running ccb293 package qiime
#RUN apt-get update -qq --yes > /dev/null && \
#    apt-get install --yes -qq \
#    tzdata > /dev/null

# Install these without 'recommended' packages to keep image smaller.
# Useful utils that folks sort of take for granted
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        htop \
        less \
        man \
        nano \
        screen \
        tar \
        tmux \
        wget \
        vim \
        tini \
        locales > /dev/null

RUN echo "${LC_ALL} UTF-8" > /etc/locale.gen && \
    locale-gen

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" > /etc/apt/sources.list.d/cran.list


# Install R packages
# Our pre-built R packages from rspm are built against system libs in focal
# rstan takes forever to compile from source, and needs libnodejs
# So we install older (10.x) nodejs from apt rather than newer from conda
ENV R_VERSION=4.1.2-1.2004.0
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" > /etc/apt/sources.list.d/cran.list
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
    r-base-core=${R_VERSION} \
    r-base-dev=${R_VERSION} \
    r-cran-littler=0.3.14-1.2004.0 \
    libglpk-dev \
    libzmq5 \
    nodejs npm > /dev/null

# Install desktop packages
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
        dbus-x11 \
        firefox \
        xfce4 \
        xfce4-panel \
        xfce4-terminal \
        xfce4-session \
        xfce4-settings \
        xorg \
        xubuntu-icon-theme > /dev/null

# for nbconvert & notebook-to-pdf
RUN apt-get update -qq --yes && \
    apt-get install --yes -qq \
        pandoc \
        texlive-xetex \
        texlive-fonts-recommended \
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
        > /dev/null

# Adding ncompress,pbzip2 for issue #1885 BioE-131, Fall 2020
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
        ncompress \
        pbzip2 > /dev/null

WORKDIR /home/jovyan

COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN chmod 777 /tmp/install-mambaforge.bash
RUN /tmp/install-mambaforge.bash

# Needed by RStudio
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        psmisc \
        sudo \
        libapparmor1 \
        lsb-release \
        libclang-dev \
        libpq5 > /dev/null

ENV RSTUDIO_URL https://download2.rstudio.org/server/bionic/amd64/rstudio-server-2021.09.1-372-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

# Needed by many R libraries
# Picked up from https://github.com/rocker-org/rocker/blob/9dc3e458d4e92a8f41ccd75687cd7e316e657cc0/r-rspm/focal/Dockerfile
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
                   libgdal26 \
                   libgeos-3.8.0 \
                   libproj15 \
                   libudunits2-0 \
                   libxml2 > /dev/null
# R_LIBS_USER is set by default in /etc/R/Renviron, which RStudio loads.
# We uncomment the default, and set what we wanna - so it picks up
# the packages we install. Without this, RStudio doesn't see the packages
# that R does.
# Stolen from https://github.com/jupyterhub/repo2docker/blob/6a07a48b2df48168685bb0f993d2a12bd86e23bf/repo2docker/buildpacks/r.py
RUN sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
    echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron

# Needed by Rhtslib
RUN apt-get update -qq --yes && \
    apt-get install --yes  -qq \
        libcurl4-openssl-dev > /dev/null

USER ${NB_USER}

COPY environment.yml /tmp/
COPY infra-requirements.txt /tmp/

RUN mamba env update -p ${CONDA_DIR} -f /tmp/environment.yml && mamba clean -afy
RUN jupyter contrib nbextensions install --sys-prefix --symlink && \
    jupyter nbextensions_configurator enable --sys-prefix

# Set CRAN mirror to rspm before we install anything
COPY Rprofile.site /usr/lib/R/etc/Rprofile.site
# RStudio needs its own config
COPY rsession.conf /etc/rstudio/rsession.conf

#install rsession proxy
RUN pip install --no-cache-dir \
        jupyter-rsession-proxy==2.0.1

# Install IRKernel
RUN r -e "install.packages('IRkernel', version='1.2')" && \
    r -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

# Install R packages, cleanup temp package download location
COPY install.R /tmp/install.R
RUN r /tmp/install.R && \
 	rm -rf /tmp/downloaded_packages/ /tmp/*.rds

# Disable history.
ADD ipython_config.py ${CONDA_PREFIX}/etc/ipython/

# install bio1b packages
COPY bio1b-packages.bash /tmp/bio1b-packages.bash
RUN bash /tmp/bio1b-packages.bash

# install ib134L packages
COPY ib134-packages.bash /tmp/ib134-packages.bash
RUN bash /tmp/ib134-packages.bash

# install ccb293 packages
COPY ccb293-packages.bash /tmp/ccb293-packages.bash
RUN bash /tmp/ccb293-packages.bash

ENTRYPOINT ["tini", "--"]

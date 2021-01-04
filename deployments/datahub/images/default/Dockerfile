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
RUN mkdir -p ${R_LIBS_USER} && chown ${NB_USER}:${NB_USER} ${R_LIBS_USER}

RUN apt-get -qq update --yes && \
    apt-get -qq install --yes \
            tar \
            vim \
            locales > /dev/null

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# for nbconvert
# FIXME: Understand what exactly we want
# texlive-plain-generic is new name of texlive-generic-recommended
RUN apt-get -qq install --yes \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-plain-generic > /dev/null

RUN apt-get -qq install --yes \
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
            ffmpeg > /dev/null

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
            
# Set path where R packages are installed
# Download and install rstudio manually
# Newer one has bug that doesn't work with jupyter-rsession-proxy
ENV RSTUDIO_URL https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.2.5042-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

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

# Install all our base R packages
COPY install.R  /tmp/install.R
RUN /tmp/install.R && \
    rm -rf /tmp/downloaded_packages

ENV PATH ${CONDA_DIR}/bin:$PATH:/usr/lib/rstudio-server/bin

# Set this to be on container storage, rather than under $HOME
ENV IPYTHONDIR ${CONDA_DIR}/etc/ipython


WORKDIR /home/${NB_USER}

COPY install-miniforge.bash /tmp/install-miniforge.bash
RUN /tmp/install-miniforge.bash

USER ${NB_USER}

COPY environment.yml /tmp/environment.yml
COPY requirements.txt /tmp/requirements.txt
COPY infra-requirements.txt /tmp/infra-requirements.txt

RUN conda env update -p ${CONDA_DIR} -f /tmp/environment.yml


RUN pip install --no-cache -r /tmp/infra-requirements.txt

# Install jupyterlab extensions immediately after infra-requirements
# This hopefully prevents re-installation all the time
# `jlpm` calls out to yarn internally, and we tell it to
# use a temporary cache. This reduces file size,
# but also prevents strange permission errors -
# like https://app.circleci.com/pipelines/github/berkeley-dsep-infra/datahub/1176/workflows/7f49851f-c2fc-46ca-b887-15d8e5612097/jobs/13584
RUN jlpm cache dir && mkdir -p /tmp/yarncache && \
    jlpm config set cache-folder /tmp/yarncache && \
    jupyter labextension install --debug \
            @jupyter-widgets/jupyterlab-manager \
            jupyter-matplotlib \
            jupyterlab-plotly \
            @jupyterlab/geojson-extension \
            jupyterlab-videochat@0.4 \
            ipycanvas  && \
    rm -rf /tmp/yarncache

RUN pip install --no-cache numpy==1.18.5 cython==0.29.21


RUN pip install --no-cache -r /tmp/requirements.txt

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

COPY connectors/2019-fall-phys-188-288.bash /usr/local/sbin/
RUN /usr/local/sbin/2019-fall-phys-188-288.bash

ADD ipython_config.py ${IPYTHONDIR}/ipython_config.py

# install gmaps notebook extension
RUN jupyter nbextension enable --py --sys-prefix gmaps

# install QGrid notebook extension
RUN jupyter nbextension enable --py --sys-prefix qgrid


EXPOSE 8888

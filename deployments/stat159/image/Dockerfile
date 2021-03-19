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


ENV PATH ${CONDA_DIR}/bin:$PATH
#
# Set this to be on container storage, rather than under $HOME ENV IPYTHONDIR ${CONDA_DIR}/etc/ipython
WORKDIR /home/${NB_USER}

# Install miniforge as root
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

RUN pip install --no-cache numpy==1.20.1 cython==0.29.21

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


EXPOSE 8888

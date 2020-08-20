FROM buildpack-deps:bionic-scm

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000

ENV CONDA_DIR /opt/conda
ENV PATH ${CONDA_DIR}/bin:$PATH

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Other packages for user convenience and Data100 usage
# Install these without 'recommended' packages to keep image smaller.
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        build-essential \
        ca-certificates \
        curl \
        default-jdk \
        emacs-nox \
        git \
        htop \
        less \
        libpq-dev \
        man \
        mc \
        nano \
        openssh-client \
        postgresql-client \
        screen \
        tar \
        tmux \
        wget \
        vim \
        locales > /dev/null

RUN echo "${LC_ALL} UTF-8" > /etc/locale.gen && \
    locale-gen

RUN apt-get update -qq --yes && \
    apt-get install --yes -qq \
        # for nbconvert
        pandoc \
        texlive-xetex \
        texlive-fonts-recommended \
        texlive-generic-recommended \
        > /dev/null

WORKDIR /home/jovyan

# prevent bibtex from interupting nbconvert
RUN update-alternatives --install /usr/bin/bibtex bibtex /bin/true 200

COPY install-miniforge.bash /tmp/install-miniforge.bash
RUN /tmp/install-miniforge.bash

USER ${NB_USER}


COPY environment.yml /tmp/
COPY requirements.txt /tmp/
COPY infra-requirements.txt /tmp/

RUN conda env update -p ${CONDA_DIR} -f /tmp/environment.yml

# Set bash as shell in terminado.
ADD jupyter_notebook_config.py  ${CONDA_PREFIX}/envs/data100/etc/jupyter/
# Disable history.
ADD ipython_config.py ${CONDA_PREFIX}/envs/data100/etc/ipython/

# Installed in conda environment
RUN jupyter serverextension enable --sys-prefix --py jupyterlab

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@2.0.0 \
                                 jupyterlab-plotly@4.8.1  \
                                 plotlywidget@4.8.1

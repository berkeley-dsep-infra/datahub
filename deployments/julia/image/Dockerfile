FROM buildpack-deps:focal-scm

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000
ENV SHELL /bin/bash

ENV CONDA_DIR /opt/conda
ENV JULIA_DIR /opt/julia

ENV PATH ${JULIA_DIR}/bin:${CONDA_DIR}/bin:$PATH

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Useful utils that folks sort of take for granted
RUN apt-get update -qq --yes && \
    apt-get install --yes -qq \
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
        build-essential \
        locales > /dev/null

RUN echo "${LC_ALL} UTF-8" > /etc/locale.gen && \
    locale-gen

RUN mkdir -p ${JULIA_DIR} && chown ${NB_USER}:${NB_USER} ${JULIA_DIR}

WORKDIR /home/jovyan

COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN /tmp/install-mambaforge.bash

USER ${NB_USER}

COPY environment.yml /tmp/environment.yml
RUN mamba env update -p ${CONDA_DIR}  -f /tmp/environment.yml

COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN pip install --no-cache -r /tmp/infra-requirements.txt
RUN jupyter contrib nbextensions install --sys-prefix --symlink && \
    jupyter nbextensions_configurator enable --sys-prefix

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt

COPY install-julia.bash /tmp/install-julia.bash
RUN /tmp/install-julia.bash

ENV JULIA_DEPOT_PATH ${JULIA_DIR}/pkg

RUN JUPYTER_DATA_DIR=${CONDA_DIR}/share/jupyter julia -e 'using Pkg; Pkg.add("IJulia"); using IJulia; installkernel("Julia");'

COPY install-julia-packages.jl /tmp/install-julia-packages.jl
RUN /tmp/install-julia-packages.jl

ENTRYPOINT ["tini", "--"]
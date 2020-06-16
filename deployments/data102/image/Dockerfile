FROM buildpack-deps:bionic-scm

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

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
        wkhtmltopdf # for pdf export \
        > /dev/null


ENV CONDA_PREFIX /srv/conda
ENV PATH ${CONDA_PREFIX}/bin:$PATH
RUN install -d -o jovyan -g jovyan ${CONDA_PREFIX}

WORKDIR /home/jovyan

# prevent bibtex from interupting nbconvert
RUN update-alternatives --install /usr/bin/bibtex bibtex /bin/true 200

USER jovyan

####################################################################
# Download, install and configure the Conda environment

RUN curl -o /tmp/miniconda.sh \
    https://repo.anaconda.com/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh

# Install miniconda
RUN bash /tmp/miniconda.sh -b -u -p ${CONDA_PREFIX}

RUN conda config --set always_yes yes --set changeps1 no
RUN conda update -q conda
RUN conda config --add channels conda-forge

# Encapsulate the environment info into its own yml file (which carries
# the name `data102` in it
COPY environment.yml /tmp/
RUN conda env create -f /tmp/environment.yml

# We modify the path directly since the `source activate data102`
# environment won't be preserved here.
ENV PATH ${CONDA_PREFIX}/envs/data102/bin:$PATH

# Set bash as shell in terminado.
ADD jupyter_notebook_config.py  ${CONDA_PREFIX}/envs/data102/etc/jupyter/
# Disable history.
ADD ipython_config.py ${CONDA_PREFIX}/envs/data102/etc/ipython/

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@2.0.0 \
                                 jupyterlab-plotly@4.8.1  \
                                 plotlywidget@4.8.1 \
                                 jupyter-matplotlib@0.7.2 \
                                 @jupyterlab/geojson-extension@2.0.1

# Useful for debugging any issues with conda
RUN conda info -a

# Make JupyterHub ports visible
EXPOSE 8888
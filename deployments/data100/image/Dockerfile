FROM buildpack-deps:bionic-scm

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN apt-get update --yes
RUN apt-get install --yes \
		python3.6 \
		python3.6-venv \
		python3.6-dev \
		tar \
		vim \
		locales

# Other packages for user convenience and Data100 usage
# Install these without 'recommended' packages to keep image smaller.
RUN apt-get install --yes --no-install-recommends \
		build-essential \
		ca-certificates \
		curl \
		default-jdk \
		emacs-nox \
		git \
		htop \
		less \
		man \
		mc \
		nano \
		openssh-client \
		postgresql-client \
		screen \
		tar \
		tmux \
		wget

RUN echo "${LC_ALL} UTF-8" > /etc/locale.gen && \
	locale-gen

# for nbconvert
RUN apt-get install --yes \
		# for nbconvert
		pandoc \
		texlive-xetex \
		texlive-fonts-recommended \
		texlive-generic-recommended

# for pdf export
RUN apt-get install --yes wkhtmltopdf

# Keep image size at a minimum
RUN apt-get clean

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
	https://repo.continuum.io/miniconda/Miniconda3-4.4.10-Linux-x86_64.sh

# Install miniconda
RUN bash /tmp/miniconda.sh -b -u -p ${CONDA_PREFIX}

RUN conda config --set always_yes yes --set changeps1 no
RUN conda update -q conda

# Encapsulate the environment info into its own yml file (which carries
# the name `data100` in it
COPY environment.yml /tmp/
RUN conda env create -q -f /tmp/environment.yml

# We modify the path directly since the `source activate data100`
# environment won't be preserved here.
ENV PATH ${CONDA_PREFIX}/envs/data100/bin:$PATH

# Set bash as shell in terminado.
ADD jupyter_notebook_config.py  ${CONDA_PREFIX}/envs/data100/etc/jupyter/
# Disable history.
ADD ipython_config.py ${CONDA_PREFIX}/envs/data100/etc/ipython/

# Installed in conda environment
RUN jupyter serverextension enable --sys-prefix --py jupyterlab

RUN jupyter labextension install @jupyterlab/hub-extension

RUN jupyter serverextension enable  --sys-prefix --py nbzip
RUN jupyter nbextension install     --sys-prefix --py nbzip
RUN jupyter nbextension enable      --sys-prefix --py nbzip

# Useful for debugging any issues with conda
RUN conda info -a

# Make JupyterHub ports visible
EXPOSE 8888

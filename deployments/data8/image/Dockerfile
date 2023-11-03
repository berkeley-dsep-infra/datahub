FROM buildpack-deps:focal-scm

ENV CONDA_DIR /srv/conda

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
ENV R_LIBS_USER /srv/r
RUN install -d -o ${NB_USER} -g ${NB_USER} ${R_LIBS_USER}

RUN apt-get -qq update --yes && \
    apt-get -qq install --yes \
            tar \
            vim \
            micro \
            mc \
            tini \
            build-essential \
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
            # provides FandolSong-Regular.otf for issue #2714
            texlive-lang-chinese \
            texlive-plain-generic > /dev/null

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

USER ${NB_USER}
WORKDIR /home/${NB_USER}

ENV PATH ${CONDA_DIR}/bin:$PATH

USER root

# Install mambaforgeas root - the script chowns to $NB_USER by the end
COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN /tmp/install-mambaforge.bash

USER ${NB_USER}

COPY environment.yml /tmp/environment.yml

RUN mamba env update -p ${CONDA_DIR} -f /tmp/environment.yml && mamba clean -afy

COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN pip install --no-cache -r /tmp/infra-requirements.txt

# Set up notebook-as-pdf dependencies
ENV PYPPETEER_HOME ${CONDA_DIR}
RUN pyppeteer-install

EXPOSE 8888

# Temporarily install newer version of jupyterlab-link-share
# Move this back to just installing off infra-requirements once we are a bit stable
RUN pip install -U jupyterlab-link-share==0.2.4

ENTRYPOINT ["tini", "--"]

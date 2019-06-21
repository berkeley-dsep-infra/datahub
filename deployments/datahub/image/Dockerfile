FROM buildpack-deps:bionic-scm

ENV APP_DIR /srv/app

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan
RUN install -d -o jovyan -g jovyan ${APP_DIR}

COPY nodesource.list /etc/apt/sources.list.d/nodesource.list
COPY nodesource-key.asc /tmp/nodesource-key.asc
RUN apt-key add /tmp/nodesource-key.asc

# TODO: remove me when apt can find our packages
#RUN echo 91.189.91.26  security.ubuntu.com >> /etc/hosts
#RUN echo 91.189.88.149  archive.ubuntu.com >> /etc/hosts

RUN apt-get -qq update --yes && \
    apt-get -qq install --yes \
            python3.6 \
            python3.6-venv \
            python3.6-dev \
            tar \
            vim \
            nodejs \
            locales > /dev/null

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# for nbconvert
RUN apt-get -qq install --yes \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-generic-recommended > /dev/null

RUN apt-get -qq install --yes \
            # for LS88-5 and modules basemap
            libspatialindex-dev \
            libgeos-dev \
            # for phys 151
            gfortran \
            # for eps 109; fall 2019
            ffmpeg > /dev/null

# install R, packages, and RStudio dependencies
RUN apt-get -qq update --yes && \
    apt-get -qq install --yes \
            libapparmor1 \
            libgdal-dev \
            libproj-dev \
            psmisc \
            sudo \
            r-base \
            r-base-dev \
            r-cran-aer \
            r-cran-backports \
            r-cran-base64enc \
            r-cran-bindrcpp \
            r-cran-broom \
            r-cran-crayon \
            r-cran-crosstalk \
            r-cran-curl \
            r-cran-data.table \
            r-cran-dbi \
            r-cran-devtools \
            r-cran-digest \
            r-cran-e1071 \
            r-cran-evaluate \
            r-cran-forcats \
            r-cran-ggplot2 \
            r-cran-glue \
            r-cran-haven \
            r-cran-highr \
            r-cran-hms \
            r-cran-htmlwidgets \
            r-cran-httpuv \
            r-cran-httr \
            r-cran-lubridate \
            r-cran-mapproj \
            r-cran-maptools \
            r-cran-markdown \
            r-cran-matrix \
            r-cran-matrixstats \
            r-cran-memoise \
            r-cran-nlme \
            r-cran-openssl \
            r-cran-pbdzmq \
            r-cran-pillar \
            r-cran-png \
            r-cran-praise \
            r-cran-proto \
            r-cran-raster \
            r-cran-rcolorbrewer \
            r-cran-rcpp \
            r-cran-rcurl \
            r-cran-readr \
            r-cran-readxl \
            r-cran-rematch \
            r-cran-repr \
            r-cran-reshape \
            r-cran-rjson \
            r-cran-rlang \
            r-cran-rpart \
            r-cran-rprojroot \
            r-cran-shiny \
            r-cran-sp \
            r-cran-spatstat \
            r-cran-spdep \
            r-cran-stringr \
            r-cran-stringi \
            r-cran-testthat \
            r-cran-tibble \
            r-cran-tidyr \
            r-cran-utf8 \
            r-cran-uuid \
            r-cran-viridis \
            r-cran-withr \
            r-cran-xml2 \
            r-cran-yaml \
            lsb-release > /dev/null

# Install some R libraries that aren't in the debs
COPY install.R  /tmp/install.R
# CircleCI stops printing output at 40k chars.
# We send stdout to a log file, and tail it a bit
# FIXME: Find something less sucky
# another hubploy #1
RUN Rscript /tmp/install.R > /tmp/r-custom-packages.log 2>&1 && \
    true || ( echo FAIL ; tail /tmp/r-custom-packages.log ; false )
RUN tail /tmp/r-custom-packages.log
RUN rm /tmp/r-custom-packages.log

ENV RSTUDIO_URL https://download2.rstudio.org/rstudio-server-1.1.453-amd64.deb
ENV RSTUDIO_CHECKSUM 3c546fa9067f48ed1a342f810fca8be6

# install rstudio
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    echo "${RSTUDIO_CHECKSUM} /tmp/rstudio.deb" | md5sum -c - && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

ENV PATH ${APP_DIR}/venv/bin:$PATH:/usr/lib/rstudio-server/bin

# Set this to be on container storage, rather than under $HOME
ENV IPYTHONDIR ${APP_DIR}/venv/etc/ipython

WORKDIR /home/jovyan

USER jovyan
RUN python3.6 -m venv ${APP_DIR}/venv

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install JupyterLab extensions
RUN jupyter labextension install \
            @jupyterlab/hub-extension \
            @jupyter-widgets/jupyterlab-manager \
            jupyter-matplotlib \
            @jupyterlab/plotly-extension \
            @jupyterlab/geojson-extension

# Install IR kernelspec
RUN Rscript -e "IRkernel::installspec(user = FALSE, prefix='${APP_DIR}/venv')"

# hmms needs to be installed after cython, for ce88 and ls88-3
RUN pip install --no-cache-dir hmms==0.1

# Cartopy needs to be installed after cython, for eps 88
RUN pip install --no-cache-dir Cartopy==0.17.0

COPY d8extension.bash /usr/local/sbin/d8extension.bash
RUN /usr/local/sbin/d8extension.bash

ENV NLTK_DATA ${APP_DIR}/nltk_data
COPY connectors/text.bash /usr/local/sbin/connector-text.bash
RUN /usr/local/sbin/connector-text.bash

#COPY connectors/eps88.bash /usr/local/sbin/connector-eps88.bash
#RUN /usr/local/sbin/connector-eps88.bash

ADD ipython_config.py ${IPYTHONDIR}/ipython_config.py
ADD jupyter_notebook_config.py ${APP_DIR}/venv/etc/jupyter/jupyter_notebook_config.py

# install gmaps notebook extension
RUN jupyter nbextension enable --py --sys-prefix gmaps

# install QGrid notebook extension
RUN jupyter nbextension enable --py --sys-prefix qgrid

# Install nbzip
RUN jupyter serverextension enable  --sys-prefix --py nbzip && \
    jupyter nbextension     install --sys-prefix --py nbzip && \
    jupyter nbextension     enable  --sys-prefix --py nbzip

EXPOSE 8888

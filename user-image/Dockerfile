FROM ubuntu:18.04

ENV APP_DIR /srv/app

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

RUN apt-get install --yes locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get install --yes \
            python3.6 \
            python3.6-venv \
            python3.6-dev \
            build-essential \
            tar \
            git \
            vim \
            wget \
            npm 

# for nbconvert
RUN apt-get install --yes \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-generic-recommended

RUN apt-get install --yes \
            # for data100
            openjdk-8-jdk-headless \
            # for LS88-5 and modules basemap
            libspatialindex-dev \
            libgeos-dev \
            # for soc-130ac mapping module
            curl \
            # for phys 151
            gfortran \
            # for cogneuro
            dirmngr \
            imagemagick-6.q16

RUN apt-get install --yes debconf-utils python3-venv

# for cogneuro connector, adding NeuroDebian repo
RUN echo "neurodebian neurodebian/enable boolean true" | debconf-set-selections
RUN apt-get install --yes neurodebian
RUN apt-get update && apt-get install --yes fsl-complete

# install R, packages, and RStudio dependencies
RUN apt-get install --yes \
            libapparmor1 \
            libgdal-dev \
            libproj-dev \
            psmisc \
            sudo \
            r-base \
            r-base-dev \
            r-cran-backports \
            r-cran-base64enc \
            r-cran-bindrcpp \
            r-cran-broom \
            r-cran-crayon \
            r-cran-crosstalk \
            r-cran-curl \
            r-cran-dbi \
            r-cran-devtools \
            r-cran-digest \
            r-cran-dplyr \
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
            r-cran-knitr \
            r-cran-lubridate \
            r-cran-mapproj \
            r-cran-maptools \
            r-cran-markdown \
            r-cran-matrix \
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
            r-cran-readr \
            r-cran-readxl \
            r-cran-rematch \
            r-cran-repr \
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
            lsb-release

# these are not in ubuntu bionic so we install from versioned sources

# github ref is version 2.0.1
RUN Rscript -e "devtools::install_github('cran/leaflet', ref = 'e0019db', upgrade_dependencies = FALSE)"

# github ref is version 1.3-1
RUN Rscript -e "devtools::install_github('cran/spatstat.data', ref = '2e6fa70', upgrade_dependencies = FALSE)"

# github ref is version 0.2-3
RUN Rscript -e "devtools::install_github('cran/classint', ref = '9bc40fc', upgrade_dependencies = FALSE)"

# github ref is version 2.6.1
RUN Rscript -e "devtools::install_github('cran/ggmap', ref = '24118b4', upgrade_dependencies = FALSE)"

# github ref is version 1.3-2
RUN Rscript -e "devtools::install_github('cran/rgdal', ref = '8ae242d', upgrade_dependencies = FALSE)"

# github ref is version 0.2
RUN Rscript -e "devtools::install_github('cran/xfun', ref = '10a9629', upgrade_dependencies = FALSE)"

# github ref is version 0.5
RUN Rscript -e "devtools::install_github('cran/tinytex', ref = 'a350d5c', upgrade_dependencies = FALSE)"

# github ref is version 1.9
RUN Rscript -e "devtools::install_github('cran/rmarkdown', ref = '9e5496f', upgrade_dependencies = FALSE)"

# github ref is version 0.4-1
RUN Rscript -e "devtools::install_github('cran/selectr', ref = '7c8ee27', upgrade_dependencies = FALSE)"

# github ref is version 0.1.2
RUN Rscript -e "devtools::install_github('cran/modelr', ref = 'f4e2b61', upgrade_dependencies = FALSE)"

# github ref is version 0.1.1
RUN Rscript -e "devtools::install_github('cran/reprex', ref = '25a43c4', upgrade_dependencies = FALSE)"

# github ref is version 0.3.2
RUN Rscript -e "devtools::install_github('hadley/revest', ref = '15f265b', upgrade_dependencies = FALSE)"

# github ref is version 1.66.0-1
RUN Rscript -e "devtools::install_github('cran/bh', ref = 'bb41077', upgrade_dependencies = FALSE)"

# github ref is version 0.4.1
RUN Rscript -e "devtools::install_github('cran/clipr', ref = 'b95bcb1', upgrade_dependencies = FALSE)"

# github ref is version 1.2.1
RUN Rscript -e "devtools::install_github('cran/tidyverse', ref = 'bd9ff0b', upgrade_dependencies = FALSE)"


ENV RSTUDIO_URL https://download2.rstudio.org/rstudio-server-1.1.453-amd64.deb
ENV RSTUDIO_CHECKSUM 3c546fa9067f48ed1a342f810fca8be6

# install rstudio
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    echo "${RSTUDIO_CHECKSUM} /tmp/rstudio.deb" | md5sum -c - && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

RUN apt-get purge && apt-get clean

ENV PATH ${APP_DIR}/venv/bin:$PATH:/usr/lib/rstudio-server/bin

# Set this to be on container storage, rather than under $HOME
ENV IPYTHONDIR ${APP_DIR}/venv/etc/ipython

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN install -d -o jovyan -g jovyan ${APP_DIR}

WORKDIR /home/jovyan

USER jovyan
RUN python3.6 -m venv ${APP_DIR}/venv

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir jupyterhub==0.8.1

# hmms needs to be installed after cython, for ce88 and ls88-3
RUN pip install --no-cache-dir hmms==0.1

COPY connectors/neuro.bash /usr/local/sbin/connector-neuro.bash
RUN /usr/local/sbin/connector-neuro.bash

COPY d8extension.bash /usr/local/sbin/d8extension.bash
RUN /usr/local/sbin/d8extension.bash

ENV NLTK_DATA ${APP_DIR}/nltk_data
COPY connectors/text.bash /usr/local/sbin/connector-text.bash
RUN /usr/local/sbin/connector-text.bash

COPY connectors/ds100.bash /usr/local/sbin/connector-ds100.bash
RUN /usr/local/sbin/connector-ds100.bash

# install jupyterlab
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter serverextension enable --py jupyterlab --sys-prefix

# install nbresuse to show users memory usage
RUN pip install git+https://github.com/data-8/nbresuse.git@2f9144f
RUN jupyter serverextension enable  --sys-prefix --py nbresuse && \
    jupyter nbextension     install --sys-prefix --py nbresuse && \
    jupyter nbextension     enable  --sys-prefix --py nbresuse

# install gmaps notebook extension
RUN jupyter nbextension enable --py --sys-prefix gmaps

# Install nbserverproxy
RUN jupyter serverextension enable  --sys-prefix --py nbserverproxy

# Install nbrsessionproxy
RUN jupyter serverextension enable  --sys-prefix --py nbrsessionproxy

# Install nbzip
RUN jupyter serverextension enable  --sys-prefix --py nbzip && \
    jupyter nbextension     install --sys-prefix --py nbzip && \
    jupyter nbextension     enable  --sys-prefix --py nbzip

ADD ipython_config.py ${IPYTHONDIR}/ipython_config.py

# HACK: We wanna make sure students don't hit the 60/hr/IP limit for github
# So we just put in a Personal Access Token for a dummy here.
# FIXME: Move the token to travis encrypted secrets
ENV NETRC /srv/app/.netrc
COPY netrc-gen /tmp/netrc-gen
RUN /tmp/netrc-gen ${NETRC}

EXPOSE 8888

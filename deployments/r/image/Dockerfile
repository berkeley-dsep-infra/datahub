# SHA pin of rocker/geospatial:4.0.2, since rocker tags aren't immutable
FROM rocker/geospatial@sha256:7b0e833cd52753be619030f61ba9e085b45eb9bb13678311da4a55632c3c8c79

ENV NB_USER rstudio
ENV NB_UID 1000
ENV CONDA_DIR /srv/conda
# FIXME: Why do I need to set this here manually?
ENV REPO_DIR /srv/repo

# Set ENV for all programs...
ENV PATH ${CONDA_DIR}/bin:$PATH
# And set ENV for R! It doesn't read from the environment...
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron

# Add PATH to /etc/profile so it gets picked up by the terminal
RUN echo "PATH=${PATH}" >> /etc/profile
RUN echo "export PATH" >> /etc/profile

# The `rsession` binary that is called by jupyter-rsession-proxy to start R
# doesn't seem to start without this being explicitly set
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib

ENV HOME /home/${NB_USER}
WORKDIR ${HOME}

# Install packages needed by notebook-as-pdf
# Default fonts seem ok, we just install an emoji font
# Can't use fonts-noto-color-emoji since this is based
# on debian stretch
# tcl/tk needed by vioplot/sm (rocker #316)
# poppler and libglpk for D-Lab CTAWG
# nodejs for installing notebook / jupyterhub from source
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
            libssl1.1 \
            fonts-symbola \
            tcl8.6-dev \
            tk8.6-dev \
            libpoppler-cpp-dev \
            libglpk-dev \
            gdebi-core \
            nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install rstudio manually
# Newer one has bug that doesn't work with jupyter-rsession-proxy
ENV RSTUDIO_URL https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.2.5042-amd64.deb

# install rstudio
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

# Download and install shiny server
RUN wget --no-verbose https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.12.933-amd64.deb -O ss.deb && \
    gdebi -n ss.deb && \
    rm -f ss.deb
RUN chown -R rstudio:rstudio /var/lib/shiny-server

COPY install-miniforge.bash /tmp/install-miniforge.bash
RUN /tmp/install-miniforge.bash

USER ${NB_USER}

COPY infra-requirements.txt ${REPO_DIR}/infra-requirements.txt
COPY requirements.txt ${REPO_DIR}/requirements.txt
RUN pip install --no-cache-dir -r ${REPO_DIR}/infra-requirements.txt
RUN pip install --no-cache-dir -r ${REPO_DIR}/requirements.txt

# Set up nbpdf dependencies
ENV PYPPETEER_HOME /srv/conda
RUN pyppeteer-install

# Install latex packages via tlmgr for texlive
RUN tlmgr update --self
RUN tlmgr install collection-latexextra

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel', quiet = TRUE)" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

# Install some R libraries that aren't in the base image
COPY class-libs.R /tmp/class-libs.R

RUN mkdir -p /tmp/extras.d

COPY --chown=rstudio extras.d/example /tmp/extras.d
RUN Rscript /tmp/extras.d/example

COPY --chown=rstudio extras.d/2019-fall-stat-131a.r /tmp/extras.d/
RUN Rscript /tmp/extras.d/2019-fall-stat-131a.r

COPY --chown=rstudio extras.d/eep-1118.r /tmp/extras.d
RUN Rscript /tmp/extras.d/eep-1118.r

COPY --chown=rstudio extras.d/ias-c188.r /tmp/extras.d
RUN Rscript /tmp/extras.d/ias-c188.r

COPY --chown=rstudio extras.d/ph-142.r /tmp/extras.d
RUN Rscript /tmp/extras.d/ph-142.r

COPY --chown=rstudio extras.d/ph-w250fg.r /tmp/extras.d
RUN Rscript /tmp/extras.d/ph-w250fg.r

COPY --chown=rstudio extras.d/stat-131a.r /tmp/extras.d
RUN Rscript /tmp/extras.d/stat-131a.r

COPY --chown=rstudio extras.d/2020-spring-envecon-c118.r /tmp/extras.d/
RUN Rscript /tmp/extras.d/2020-spring-envecon-c118.r

COPY --chown=rstudio extras.d/econ-140.r /tmp/extras.d/
RUN Rscript /tmp/extras.d/econ-140.r

COPY --chown=rstudio extras.d/ph-290.r /tmp/extras.d/
RUN Rscript /tmp/extras.d/ph-290.r

COPY --chown=rstudio extras.d/dlab-ctawg.r /tmp/extras.d/
RUN Rscript /tmp/extras.d/dlab-ctawg.r


COPY postBuild ${REPO_DIR}/postBuild
RUN ${REPO_DIR}/postBuild

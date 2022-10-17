FROM rocker/geospatial:4.1.2

ENV NB_USER rstudio
ENV NB_UID 1000
ENV CONDA_DIR /srv/conda

# Set ENV for all programs...
ENV PATH ${CONDA_DIR}/bin:$PATH

# And set ENV for R! It doesn't read from the environment...
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron.site

# Add PATH to /etc/profile so it gets picked up by the terminal
RUN echo "PATH=${PATH}" >> /etc/profile
RUN echo "export PATH" >> /etc/profile

ENV HOME /home/${NB_USER}

WORKDIR ${HOME}

# Install packages needed by notebook-as-pdf
# nodejs for installing notebook / jupyterhub from source
# libarchive-dev for https://github.com/berkeley-dsep-infra/datahub/issues/1997
RUN apt-get update > /dev/null && \
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
            gdebi-core \
            tini \
            nodejs npm > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN /tmp/install-mambaforge.bash

USER ${NB_USER}

RUN mamba install -c conda-forge syncthing==1.18.6

COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN pip install --no-cache-dir -r /tmp/infra-requirements.txt

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Support latest RStudio
RUN pip install --no-cache 'jupyter-rsession-proxy>=2.0'

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel', quiet = TRUE)" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

# Install extra R packages
RUN install2.r --error --skipinstalled \
    anytime # For https://github.com/berkeley-dsep-infra/datahub/issues/2523 \
    Hmisc plm patchwork # For https://github.com/berkeley-dsep-infra/datahub/issues/2519 \
    fpp3 # For https://github.com/berkeley-dsep-infra/datahub/issues/2510 && \
    rm -rf /tmp/downloaded_packages

# fix texlive issue 3338
RUN tlmgr repository add https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final
RUN tlmgr option repository https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final
RUN tlmgr --verify-repo=none update --self

# Use simpler locking strategy
COPY file-locks /etc/rstudio/file-locks

ENTRYPOINT ["tini", "--"]

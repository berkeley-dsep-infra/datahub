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

COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN pip install --no-cache-dir -r /tmp/infra-requirements.txt

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mamba install -c conda-forge syncthing==1.18.6

# Support latest RStudio
RUN pip install --no-cache 'jupyter-rsession-proxy>=2.0'

COPY class-libs.R /tmp/class-libs.R
RUN mkdir -p /tmp/r-packages

COPY install.R /tmp/install.R
RUN /tmp/install.R && rm -rf /tmp/downloaded_packages

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel', quiet = TRUE)" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

COPY r-packages/ph-290.r /tmp/r-packages/
RUN r /tmp/r-packages/ph-290.r

COPY r-packages/ph-142.r /tmp/r-packages/
RUN r /tmp/r-packages/ph-142.r

COPY r-packages/ph-252.r /tmp/r-packages/
RUN r /tmp/r-packages/ph-252.r

COPY r-packages/2021-spring-phw-272a.r /tmp/r-packages/
RUN r /tmp/r-packages/2021-spring-phw-272a.r

RUN tlmgr repository add https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final
RUN tlmgr option repository https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final
RUN tlmgr --verify-repo=none update --self && \
    tlmgr --verify-repo=none install \
        amsmath \
        latex-amsmath-dev \
        iftex \
        kvoptions \
        ltxcmds \
        kvsetkeys \
        etoolbox \
        xcolor \
        auxhook \
        bigintcalc \
        bitset \
        etexcmds \
        gettitlestring \
        hycolor \
        hyperref \
        intcalc \
        kvdefinekeys \
        letltxmacro \
        pdfescape \
        refcount \
        rerunfilecheck \
        stringenc \
        uniquecounter \
        zapfding \
        pdftexcmds \
        infwarerr \
        geometry \
        epstopdf-pkg

ENTRYPOINT ["tini", "--"]

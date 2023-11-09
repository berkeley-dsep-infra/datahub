FROM rocker/geospatial:4.3.1

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
            emacs \
            fonts-symbola \
            less \
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
            nodejs \
            npm \
            texlive-xetex \
            texlive-latex-extra \
            texlive-fonts-recommended \
            texlive-lang-chinese \
            texlive-plain-generic \
            tini > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN /tmp/install-mambaforge.bash

USER ${NB_USER}

COPY environment.yml /tmp/environment.yml
COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN mamba env update -p ${CONDA_DIR} -f /tmp/environment.yml && \
        mamba clean -afy

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel', quiet = TRUE)" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

# Install extra R packages
RUN install2.r --error --skipinstalled \
    ## general interest 
    anytime    \
    Hmisc      \
    lmtest     \
    lubridate  \
    latex2exp  \
    MASS       \
    patchwork  \
    stargazer  \
    tidymodels \
    wooldridge \
    ## machine learning
    caret      \
    parsnip    \
    torch      \
    ## 241
    AER        \
    randomizr  \
    ## 271
    fable      \
    feasts     \
    fpp3       \
    gamlr      \
    plm        \
    lme4       \
    Quandl     \
    quantmod   \
    tseries    \
    tsibble    \
    vcd        \
    vars       \
    zoo

# Use simpler locking strategy
COPY file-locks /etc/rstudio/file-locks

ENTRYPOINT ["tini", "--"]

FROM rocker/geospatial:4.4.1
# https://github.com/rocker-org/rocker-versioned2/wiki/geospatial_e06f866673fa

ENV NB_USER rstudio
ENV NB_UID 1000
ENV CONDA_DIR /srv/conda

# Set ENV for all programs...
ENV PATH ${CONDA_DIR}/bin:$PATH

# Pick up rocker's default TZ
ENV TZ=Etc/UTC

# And set ENV for R! It doesn't read from the environment...
RUN echo "TZ=${TZ}" >> /usr/local/lib/R/etc/Renviron.site
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron.site

# Add PATH to /etc/profile so it gets picked up by the terminal
RUN echo "PATH=${PATH}" >> /etc/profile
RUN echo "export PATH" >> /etc/profile

ENV HOME /home/${NB_USER}

WORKDIR ${HOME}

# texlive-xetex pulls in texlive-latex-extra > texlive-latex-recommended
# We use Ubuntu's TeX because rocker's doesn't have most packages by default, 
# and we don't want them to be downloaded on demand by students.
# tini is necessary because it is our ENTRYPOINT below.
RUN apt-get update && \
    apt-get -qq install \
            less \
            tini \
            fonts-symbola \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-fonts-extra \
            texlive-plain-generic \
            > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# While quarto is included with rocker/verse, we sometimes need different
# versions than the default. For example a newer version might fix bugs.
ENV _QUARTO_VERSION=1.4.549
RUN curl -L -o /tmp/quarto.deb https://github.com/quarto-dev/quarto-cli/releases/download/v${_QUARTO_VERSION}/quarto-${_QUARTO_VERSION}-linux-amd64.deb
RUN apt-get update > /dev/null && \
    apt-get install /tmp/quarto.deb > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /tmp/quarto.deb

ENV SHINY_SERVER_URL https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.21.1012-amd64.deb
RUN curl --silent --location --fail ${SHINY_SERVER_URL} > /tmp/shiny-server.deb && \
    apt install --no-install-recommends --yes /tmp/shiny-server.deb && \
    rm /tmp/shiny-server.deb

# google-chrome is for pagedown; chromium doesn't work nicely with it (snap?)
RUN wget --quiet -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update > /dev/null && \
    apt-get -qq install /tmp/chrome.deb > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /tmp/chrome.deb

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

COPY class-libs.R /tmp/class-libs.R

COPY r-packages/2023-fall-stat-20.r /tmp/r-packages/
RUN r /tmp/r-packages/2023-fall-stat-20.r

# Configure locking behavior
COPY file-locks /etc/rstudio/file-locks

# Disable visual markdown editing by default
COPY rstudio-prefs.json /etc/rstudio/rstudio-prefs.json

ENTRYPOINT ["tini", "--"]

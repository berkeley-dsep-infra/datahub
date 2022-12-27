FROM rocker/geospatial:4.2.2
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

# Install packages needed by notebook-as-pdf
# nodejs for installing notebook / jupyterhub from source
# texlive-xetex pulls in texlive-latex-extra > texlive-latex-recommended
# We use Ubuntu's TeX because rocker's doesn't have most packages by default, 
# and we don't want them to be downloaded on demand by students.
RUN apt-get update && \
    apt-get install --yes \
            libxrandr2 \
            libatk1.0-0 \
            libatk-bridge2.0-0 \
            libgtk-3-0 \
            fonts-symbola \
            gdebi-core \
            tini \
            pandoc \
            texlive-xetex \
            texlive-latex-extra \
            texlive-fonts-recommended \
            # provides FandolSong-Regular.otf for issue #2714
            texlive-lang-chinese \
            texlive-plain-generic \
            nodejs \
            npm \
            > /dev/null && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# google-chrome is for pagedown; chromium doesn't work nicely with it (snap?)
RUN wget --quiet -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update > /dev/null && \
    apt -y install /tmp/google-chrome-stable_current_amd64.deb > /dev/null && \
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

COPY class-libs.R /tmp/class-libs.R

COPY r-packages/2022-spring-stat-20.r /tmp/r-packages/
RUN r /tmp/r-packages/2022-spring-stat-20.r

# Configure locking behavior
COPY file-locks /etc/rstudio/file-locks

ENTRYPOINT ["tini", "--"]

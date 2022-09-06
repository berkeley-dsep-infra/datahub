FROM rocker/geospatial:4.2.1

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
# libarchive-dev for https://github.com/berkeley-dsep-infra/datahub/issues/1997
# texlive-xetex pulls in texlive-latex-extra > texlive-latex-recommended
# We use Ubuntu's TeX because rocker's doesn't have most packages by default, 
# and we don't want them to be downloaded on demand by students.
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
            gdebi-core \
            tini \
            pandoc \
            texlive-xetex \
            texlive-latex-extra \
            texlive-fonts-recommended \
            # provides FandolSong-Regular.otf for issue #2714
            texlive-lang-chinese \
            texlive-plain-generic \
            nodejs npm > /dev/null && \
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

COPY infra-requirements.txt /tmp/infra-requirements.txt
RUN pip install --no-cache-dir -r /tmp/infra-requirements.txt

RUN mamba install -c conda-forge syncthing==1.18.6

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel', quiet = TRUE)" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

COPY class-libs.R /tmp/class-libs.R

COPY r-packages/2022-spring-stat-20.r /tmp/r-packages/
RUN r /tmp/r-packages/2022-spring-stat-20.r

# RUN tlmgr --verify-repo=none update --self && \
#     tlmgr --verify-repo=none install \
# 	amsmath \
#     auxhook \
#     bigintcalc \
#     bitset \
#     bookmark \
#     booktabs \
#     caption \
#     environ \
#     epstopdf-pkg \
#     etexcmds \
#     etoolbox \
#     fancyvrb \
#     float \
#     framed \
#     geometry \
#     gettitlestring \
#     hycolor \
#     hyperref \
#     iftex \
#     infwarerr \
#     intcalc \
#     koma-script \
#     kvdefinekeys \
#     kvoptions \
#     kvsetkeys \
#     latex-amsmath-dev \
#     letltxmacro \
#     ltxcmds \
#     mdwtools \
#     oberdiek \
#     pdfescape \
#     pdftexcmds \
#     pgf \
#     refcount \
#     rerunfilecheck \
#     stringenc \
#     uniquecounter \
#     unicode-math \
#     tcolorbox \
#     xcolor \
#     zapfding

ENTRYPOINT ["tini", "--"]

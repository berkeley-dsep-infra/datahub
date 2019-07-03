FROM rocker/geospatial:3.6.0

ENV NB_USER rstudio
ENV NB_UID 1000
ENV CONDA_DIR /srv/conda
# FIXME: Why do I need to set this here manually?
ENV REPO_DIR /srv/repo

# Set ENV for all programs...
ENV PATH ${CONDA_DIR}/bin:$PATH
# And set ENV for R! It doesn't read from the environment...
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron

# The `rsession` binary that is called by jupyter-rsession-proxy to start R
# doesn't seem to start without this being explicitly set
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib

ENV HOME /home/${NB_USER}
WORKDIR ${HOME}

# Install packages needed by nbpdfexport
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
            fonts-noto-color-emoji && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY install-miniconda.bash /tmp/install-miniconda.bash
RUN /tmp/install-miniconda.bash

USER ${NB_USER}

RUN pip install --no-cache-dir \
                jupyter-rsession-proxy==1.0b6 \
                jupyterhub==1.0.0 \
                jupyterlab==0.35.6 \
                notebook==5.7.8 \
                nbpdfexport==0.2.1

# Set up nbpdf dependencies
ENV PYPPETEER_HOME /srv/conda
RUN pyppeteer-install
RUN jupyter bundlerextension enable nbpdfexport.bundler --sys-prefix --py

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel')" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

# Install some R libraries that aren't in the base image
COPY --chown=rstudio extras.d  /tmp/extras.d
# CircleCI stops printing output at 40k chars.
# We send stdout to a log file, and tail it a bit
# FIXME: Find something less sucky
# another hubploy #1
RUN chmod -R +x /tmp/extras.d && \
	run-parts /tmp/extras.d > /tmp/r-custom-packages.log 2>&1 && \
    true || ( echo FAIL ; tail /tmp/r-custom-packages.log ; false )

RUN tail /tmp/r-custom-packages.log
RUN rm /tmp/r-custom-packages.log

COPY --chown=rstudio:rstudio . ${REPO_DIR}

RUN pip install --no-cache-dir -r ${REPO_DIR}/requirements.txt

# Execute PostBuild if it exists
RUN [ -f ${REPO_DIR}/postBuild ] && chmod +x ${REPO_DIR}/postBuild && ${REPO_DIR}/postBuild

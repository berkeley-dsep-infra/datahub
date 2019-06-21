FROM rocker/geospatial:3.6.0

ENV NB_USER rstudio
ENV NB_UID 1000
ENV VENV_DIR /srv/venv
ENV REPO_DIR /srv/repo

# Set ENV for all programs...
ENV PATH ${VENV_DIR}/bin:$PATH
# And set ENV for R! It doesn't read from the environment...
RUN echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron

# The `rsession` binary that is called by jupyter-rsession-proxy to start R
# doesn't seem to start without this being explicitly set
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib

ENV HOME /home/${NB_USER}
WORKDIR ${HOME}

RUN apt-get update && \
    apt-get -y install python3-venv python3-dev && \
    apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a venv dir owned by unprivileged user & set up notebook in it
# This allows non-root to install python libraries if required
RUN mkdir -p ${VENV_DIR} && chown -R ${NB_USER} ${VENV_DIR}
RUN mkdir -p ${REPO_DIR} && chown -R ${NB_USER} ${REPO_DIR}

USER ${NB_USER}

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

RUN python3 -m venv ${VENV_DIR}

# Explicitly install a new enough version of pip
RUN ${VENV_DIR}/bin/pip3 install --no-cache-dir \
                         pip==19.1.1

RUN ${VENV_DIR}/bin/pip3 install --no-cache-dir \
                         jupyter-rsession-proxy==1.0b6 \
                         jupyterhub==1.0.0 \
                         jupyterlab==0.35.6 \
                         notebook==5.7.8

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel')" && \
    R --quiet -e "IRkernel::installspec(prefix='${VENV_DIR}')"

COPY --chown=rstudio:rstudio . ${REPO_DIR}

# Install requirements.txt if it exists
RUN [ -f ${REPO_DIR}/requirements.txt ] && \
    ${VENV_DIR}/bin/pip3 install --no-cache-dir -r ${REPO_DIR}/requirements.txt

# Execute PostBuild if it exists
RUN [ -f ${REPO_DIR}/postBuild ] && chmod +x ${REPO_DIR}/postBuild && ${REPO_DIR}/postBuild

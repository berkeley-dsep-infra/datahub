FROM buildpack-deps:jammy-scm as base

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000
# These are used by the python, R, and final stages
ENV CONDA_DIR /srv/conda
ENV R_LIBS_USER /srv/r

RUN apt-get -qq update --yes && \
    apt-get -qq install --yes locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Install all apt packages
COPY apt.txt /tmp/apt.txt
RUN apt-get -qq update --yes && \
    apt-get -qq install --yes --no-install-recommends \
        $(grep -v ^# /tmp/apt.txt) && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*

# Install R.
# These packages must be installed into the base stage since they are in system
# paths rather than /srv.
# Pre-built R packages from rspm are built against system libs in jammy.
ENV R_VERSION=4.3.2-1.2204.0
ENV LITTLER_VERSION=0.3.18-2.2204.0
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/" > /etc/apt/sources.list.d/cran.list
RUN curl --silent --location --fail https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc > /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
        r-base-core=${R_VERSION} \
        r-base-dev=${R_VERSION} \
        littler=${LITTLER_VERSION} > /dev/null

ENV RSTUDIO_URL https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2023.06.0-421-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    apt install --no-install-recommends --yes /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

ENV SHINY_SERVER_URL https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.20.1002-amd64.deb
RUN curl --silent --location --fail ${SHINY_SERVER_URL} > /tmp/shiny.deb && \
    apt install --no-install-recommends --yes /tmp/shiny.deb && \
    rm /tmp/shiny.deb

# Set CRAN mirror to rspm before we install anything
COPY Rprofile.site /usr/lib/R/etc/Rprofile.site
# RStudio needs its own config
COPY rsession.conf /etc/rstudio/rsession.conf

# R_LIBS_USER is set by default in /etc/R/Renviron, which RStudio loads.
# We uncomment the default, and set what we wanna - so it picks up
# the packages we install. Without this, RStudio doesn't see the packages
# that R does.
# Stolen from https://github.com/jupyterhub/repo2docker/blob/6a07a48b2df48168685bb0f993d2a12bd86e23bf/repo2docker/buildpacks/r.py
# To try fight https://community.rstudio.com/t/timedatectl-had-status-1/72060,
# which shows up sometimes when trying to install packages that want the TZ
# timedatectl expects systemd running, which isn't true in our containers
RUN sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
    echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron && \
    echo "TZ=${TZ}" >> /etc/R/Renviron

# =============================================================================
# This stage exists to build /srv/r.
FROM base as srv-r

# Create user owned R libs dir
# This lets users temporarily install packages
RUN install -d -o ${NB_USER} -g ${NB_USER} ${R_LIBS_USER}

# Install R libraries as our user
USER ${NB_USER}

COPY class-libs.R /tmp/class-libs.R
RUN mkdir -p /tmp/r-packages

# Our install.R needs devtools which needs install2.r which needs docopt.
# install2.r is not reproducible, but our install.R script is.
RUN Rscript -e "install.packages('docopt')"
RUN /usr/lib/R/site-library/littler/examples/install2.r devtools

# Install all our base R packages
COPY install.R  /tmp/install.R
RUN /tmp/install.R && rm -rf /tmp/downloaded_packages

# =============================================================================
# This stage exists to build /srv/conda.
FROM base as srv-conda

COPY install-mambaforge.bash /tmp/install-mambaforge.bash
RUN /tmp/install-mambaforge.bash

# Install conda environment as our user
USER ${NB_USER}

ENV PATH ${CONDA_DIR}/bin:$PATH

COPY infra-requirements.txt /tmp/infra-requirements.txt
COPY environment.yml /tmp/environment.yml

RUN mamba env update -p ${CONDA_DIR} -f /tmp/environment.yml && \
    mamba clean -afy

# =============================================================================
# This stage consumes base and import /srv/r and /srv/conda.
FROM base as final
COPY --from=srv-r /srv/r /srv/r
COPY --from=srv-conda /srv/conda /srv/conda

# Install IR kernelspec. Requires python and R.
ENV PATH ${CONDA_DIR}/bin:${PATH}:${R_LIBS_USER}/bin
RUN R -e "IRkernel::installspec(user = FALSE, prefix='${CONDA_DIR}')"

# clear out /tmp
USER root
RUN rm -rf /tmp/*

USER ${NB_USER}
WORKDIR /home/${NB_USER}

EXPOSE 8888

ENTRYPOINT ["tini", "--"]

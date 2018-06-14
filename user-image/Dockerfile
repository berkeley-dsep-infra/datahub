FROM ubuntu:18.04

ENV APP_DIR /srv/app
ENV PATH ${APP_DIR}/venv/bin:$PATH

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

RUN apt-get install --yes locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get install --yes \
            python3.6 \
            python3.6-venv \
            python3.6-dev \
            build-essential \
            tar \
            git \
            wget \
            npm 

RUN apt-get install --yes \
            vim \
            # for nbconvert
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-generic-recommended

RUN apt-get install --yes \
	        # for data100
	        openjdk-8-jdk-headless \
            # for LS88-5 and modules basemap
            libspatialindex-dev \
            libgeos-dev \
            # for soc-130ac mapping module
            curl \
            # for phys 151
            gfortran \
            # for cogneuro
            dirmngr \
            imagemagick-6.q16

RUN apt-get install --yes debconf-utils python3-venv

# for cogneuro connector, adding NeuroDebian repo
RUN echo "neurodebian neurodebian/enable boolean true" | debconf-set-selections
RUN apt-get install --yes neurodebian
RUN apt-get update && apt-get install --yes fsl-complete

RUN apt-get purge && apt-get clean

# Set this to be on container storage, rather than under $HOME
ENV IPYTHONDIR ${APP_DIR}/venv/etc/ipython

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN install -d -o jovyan -g jovyan ${APP_DIR}

WORKDIR /home/jovyan

USER jovyan
RUN python3.6 -m venv ${APP_DIR}/venv

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir jupyterhub==0.8.1

# hmms needs to be installed after cython, for ce88 and ls88-3
RUN pip install --no-cache-dir hmms==0.1

COPY connectors/neuro.bash /usr/local/sbin/connector-neuro.bash
RUN /usr/local/sbin/connector-neuro.bash

COPY d8extension.bash /usr/local/sbin/d8extension.bash
RUN /usr/local/sbin/d8extension.bash

ENV NLTK_DATA ${APP_DIR}/nltk_data
COPY connectors/text.bash /usr/local/sbin/connector-text.bash
RUN /usr/local/sbin/connector-text.bash

COPY connectors/ds100.bash /usr/local/sbin/connector-ds100.bash
RUN /usr/local/sbin/connector-ds100.bash

# package for instructors and gsis; requirements.txt would need an egg
#RUN pip install --no-cache-dir \
#	git+https://github.com/data-8/connector-instructors.git@e7bd553

# install jupyterlab
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter serverextension enable --py jupyterlab --sys-prefix

# install nbresuse to show users memory usage
RUN pip install git+https://github.com/data-8/nbresuse.git@2f9144f
RUN jupyter serverextension enable  --sys-prefix --py nbresuse && \
	jupyter nbextension     install --sys-prefix --py nbresuse && \
	jupyter nbextension     enable  --sys-prefix --py nbresuse

# install nbgitpuller
RUN jupyter serverextension enable  --sys-prefix --py nbgitpuller

# install gmaps notebook extension
RUN jupyter nbextension enable --py --sys-prefix gmaps

# Install nbserverproxy
RUN jupyter serverextension enable  --sys-prefix --py nbserverproxy

# Install nbrsessionproxy
RUN jupyter serverextension enable  --sys-prefix --py nbrsessionproxy

# Install nbzip
RUN jupyter serverextension enable  --sys-prefix --py nbzip && \
    jupyter nbextension     install --sys-prefix --py nbzip && \
    jupyter nbextension     enable  --sys-prefix --py nbzip

ADD ipython_config.py ${IPYTHONDIR}/ipython_config.py

# HACK: We wanna make sure students don't hit the 60/hr/IP limit for github
# So we just put in a Personal Access Token for a dummy here.
# FIXME: Move the token to travis encrypted secrets
ENV NETRC /srv/app/.netrc
COPY netrc-gen /tmp/netrc-gen
RUN /tmp/netrc-gen ${NETRC}

EXPOSE 8888

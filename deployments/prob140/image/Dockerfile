FROM buildpack-deps:bionic-scm

ENV APP_DIR /srv/app

# Set up common env variables
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan
RUN install -d -o jovyan -g jovyan ${APP_DIR}

COPY nodesource.list /etc/apt/sources.list.d/nodesource.list
COPY nodesource-key.asc /tmp/nodesource-key.asc
RUN apt-key add /tmp/nodesource-key.asc

RUN apt-get update --yes
RUN apt-get install --yes \
            python3.6 \
            python3.6-venv \
            python3.6-dev \
            tar \
            vim \
            nodejs \
            locales

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# for nbconvert
RUN apt-get install --yes \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-generic-recommended

# Set this to be on container storage, rather than under $HOME
ENV IPYTHONDIR ${APP_DIR}/venv/etc/ipython

WORKDIR /home/jovyan

USER jovyan
RUN python3.6 -m venv ${APP_DIR}/venv

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir jupyterhub==0.9.2

# hmms needs to be installed after cython, for ce88 and ls88-3
RUN pip install --no-cache-dir hmms==0.1

# Install nbserverproxy
RUN jupyter serverextension enable  --sys-prefix --py nbserverproxy

# Install nbzip
RUN jupyter serverextension enable  --sys-prefix --py nbzip && \
    jupyter nbextension     install --sys-prefix --py nbzip && \
    jupyter nbextension     enable  --sys-prefix --py nbzip

ADD ipython_config.py ${IPYTHONDIR}/ipython_config.py

EXPOSE 8888

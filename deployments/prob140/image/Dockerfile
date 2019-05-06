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

RUN apt-get update --yes
RUN apt-get install --yes \
            libdpkg-perl \
            python3.6 \
            python3.6-dev \
            python3.6-venv \
            python3-venv \
            tar \
            vim \
            nodejs \
            gcc \
            locales

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# for nbconvert
RUN apt-get install --yes \
            pandoc \
            texlive-xetex \
            texlive-fonts-recommended \
            texlive-generic-recommended

ENV PATH ${APP_DIR}/venv/bin:$PATH

WORKDIR /home/jovyan

# prevent bibtex from interupting nbconvert
RUN update-alternatives --install /usr/bin/bibtex bibtex /bin/true 200

USER jovyan
RUN python3.6 -m venv ${APP_DIR}/venv

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install nbzip
RUN jupyter serverextension enable  --sys-prefix --py nbzip && \
    jupyter nbextension     install --sys-prefix --py nbzip && \
    jupyter nbextension     enable  --sys-prefix --py nbzip

ADD ipython_config.py ${APP_DIR}/venv/etc/ipython/ipython_config.py
ADD jupyter_notebook_config.py ${APP_DIR}/venv/etc/jupyter/jupyter_notebook_config.py

EXPOSE 8888

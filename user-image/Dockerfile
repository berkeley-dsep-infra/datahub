FROM ubuntu:17.04

ENV APP_DIR /srv/app
ENV PATH ${APP_DIR}/venv/bin:$PATH

RUN apt-get update && \
    apt-get install --yes \
            python3.6 \
            python3.6-venv \
            python3.6-dev \
            build-essential \
            tar \
            git \
            wget \
            npm \
            nodejs-legacy \
            locales && \
    apt-get purge && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN mkdir -p ${APP_DIR} && chown -R jovyan:jovyan ${APP_DIR}

WORKDIR /home/jovyan

USER jovyan
RUN python3.6 -m venv ${APP_DIR}/venv

RUN pip install --no-cache-dir \
      notebook==5.0.0 \
      git+https://github.com/jupyterhub/jupyterhub@master \
      ipywidgets==6.0.0 \
      jupyterlab==0.26.5

RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter serverextension enable --py jupyterlab --sys-prefix

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD connectors/neuro.bash /usr/local/sbin/connector-neuro.bash
RUN /usr/local/sbin/connector-neuro.bash

ADD connectors/text.bash /usr/local/sbin/connector-text.bash
RUN /usr/local/sbin/connector-text.bash

# package for instructors and gsis; requirements.txt would need an egg
RUN pip install --no-cache-dir \
	git+https://github.com/data-8/connector-instructors.git@e7bd553

# nbresuse to show users memory usage
RUN pip install git+https://github.com/data-8/nbresuse.git@2f9144f && \
	jupyter serverextension enable  --sys-prefix --py nbresuse && \
	jupyter nbextension     install --sys-prefix --py nbresuse && \
	jupyter nbextension     enable  --sys-prefix --py nbresuse

# interact notebook extension
RUN pip install git+https://github.com/data-8/gitautosync@c08abdb  && \
	jupyter serverextension enable  --sys-prefix --py nbgitautosync

EXPOSE 8888

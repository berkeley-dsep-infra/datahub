# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:0.9-445a953

USER root
RUN apt update && apt install --yes curl python

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-245.0.0-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-245.0.0-linux-x86_64.tar.gz && \
    mv google-cloud-sdk /usr/local/google-cloud-sdk && \
    rm google-cloud-sdk-245.0.0-linux-x86_64.tar.gz

ENV PATH /usr/local/google-cloud-sdk/bin:${PATH}
RUN gcloud components install kubectl

COPY sparklyspawner /srv/sparklyspawner
RUN python3 -m pip install --no-cache /srv/sparklyspawner

COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

# Install JupyterHub from master!
# This is scary-ish, but we need JupyterHub master for the analytics / user-redirect work
# npm's dependencies seem to be not well specified in default apt repositories, so we need to explicitly add them
RUN apt-get update --yes --quiet && \
    apt-get install --yes --no-install-recommends nodejs-dev node-gyp libssl1.0-dev npm && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install git+https://github.com/jupyterhub/jupyterhub.git@5bbb292ef5c100c2c415a662b6e5e445546a24e6

USER ${NB_USER}

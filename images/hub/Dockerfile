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

USER ${NB_USER}

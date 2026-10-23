# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:4.3.3

USER root

RUN python3 -m pip install --no-cache git+https://github.com/berkeley-dsep-infra/canvasoauthenticator@d66662a
RUN python3 -m pip install --no-cache jupyterhub-ltiauthenticator==1.6.2
RUN python3 -m pip install --no-cache git+https://github.com/berkeley-dsep-infra/jupyterhub_grouper_sync.git@410300d
RUN python3 -m pip install --no-cache jupyterhub-fancy-profiles==0.6.0

# DH-806
RUN apt-get update && \
    apt-get install -y --no-install-recommends --only-upgrade ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --no-cache certifi==2026.10.23

COPY logos /srv/logos

USER ${NB_USER}

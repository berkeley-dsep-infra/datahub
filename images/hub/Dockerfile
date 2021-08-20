# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:1.1.2

USER root

# npm is needed to install JupyterHub from source
RUN apt update > /dev/null  && apt install --yes npm > /dev/null

# Brings in https://github.com/jupyterhub/jupyterhub/pull/3579
RUN python3 -m pip install -U git+https://github.com/meeseeksmachine/jupyterhub@auto-backport-of-pr-3488-on-1.4.x

COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

USER ${NB_USER}

# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:0.10.0-beta.1.n016.h9d87e7b7

USER root

COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

USER ${NB_USER}

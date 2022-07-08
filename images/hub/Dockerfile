# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:1.1.3-n554.hfa81c67f

USER root

COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

COPY logos /srv/jupyterhub/logos

USER ${NB_USER}

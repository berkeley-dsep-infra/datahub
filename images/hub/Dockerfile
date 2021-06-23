# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:1.0.0

USER root

# npm is needed to install JupyterHub from source
RUN apt update > /dev/null  && apt install --yes npm > /dev/null

# Brings in https://github.com/jupyterhub/jupyterhub/pull/3407
# and https://github.com/jupyterhub/jupyterhub/pull/3411
# For https://github.com/berkeley-dsep-infra/datahub/issues/2284
# Brings in https://github.com/jupyterhub/jupyterhub/pull/3488
RUN python3 -m pip install -U git+https://github.com/jupyterhub/jupyterhub@11f00dbbe794191d328c6c2a44a9e85f7eb6ede5

COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

RUN python3 -m pip install git+https://github.com/U4I-fedir-kryvytskyi/ltiauthenticator@8d53d4bd6957d1def30bb0058284d84174764473

USER ${NB_USER}

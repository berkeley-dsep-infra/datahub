# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:0.11.1-n298.hd9d7403b

USER root

# npm is needed to install JupyterHub from source
RUN apt update > /dev/null  && apt install --yes npm > /dev/null
# Install from https://github.com/yuvipanda/jupyterhub/tree/high-pagination
RUN python3 -m pip install -U git+https://github.com/yuvipanda/jupyterhub@a89ce8f9945c5f24bba0c162799eac54a966abba

COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

RUN python3 -m pip install git+https://github.com/U4I-fedir-kryvytskyi/ltiauthenticator@8d53d4bd6957d1def30bb0058284d84174764473

USER ${NB_USER}

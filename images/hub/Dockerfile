# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:0.10.0

USER root

RUN python3 -m pip install -U jupyterhub==1.2.2
COPY canvasauthenticator /srv/canvasauthenticator
RUN python3 -m pip install --no-cache /srv/canvasauthenticator

RUN python3 -m pip install git+https://github.com/U4I-fedir-kryvytskyi/ltiauthenticator@8d53d4bd6957d1def30bb0058284d84174764473

USER ${NB_USER}

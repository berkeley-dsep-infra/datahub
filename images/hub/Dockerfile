# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:2.0.1-0.dev.git.6079.haf0a8db5

USER root

RUN python3 -m pip install --no-cache git+https://github.com/berkeley-dsep-infra/canvasoauthenticator@09e7ed8
RUN python3 -m pip install --no-cache jupyterhub-ltiauthenticator==1.5.1

COPY logos /srv/logos

USER ${NB_USER}

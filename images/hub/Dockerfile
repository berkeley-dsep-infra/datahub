# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:2.0.1-0.dev.git.5959.h65c52001

USER root

RUN python3 -m pip install --no-cache git+https://github.com/berkeley-dsep-infra/canvasoauthenticator@3e0c90f

USER ${NB_USER}

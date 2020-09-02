# Should match the hub image used by version of chart in hub/requirements.yaml
# If that changes, this should be changed too!
FROM jupyterhub/k8s-hub:0.9.0-n033.h8211ad2

USER root

RUN python3 -m pip install git+https://github.com/jupyterhub/kubespawner.git@b209ce169cec441169131bd0e0d6d43d1e3ca2df

USER ${NB_USER}

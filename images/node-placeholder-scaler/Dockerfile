FROM python:3.9

ENV KUBECTL_VERSION v1.21.3
ADD https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl /usr/local/bin/kubectl
RUN chmod +x /usr/local/bin/kubectl

ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
COPY scaler /srv/scaler
WORKDIR /srv
ENTRYPOINT ["python3", "-m", "scaler"]
USER nobody

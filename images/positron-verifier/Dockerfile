# jupyter-positron-verifier: the JupyterHub service that holds the Positron
# signing key and mints short-lived, session-bound license tokens.
#
# Runs as a hub.extraContainers sidecar in the `stat` hub's pod only (see
# deployments/stat/config/common.yaml and docs/tasks/positron.qmd) so that
# the shared images/hub/Dockerfile used by every other hub stays untouched.
#
# https://posit-dev.github.io/jupyter-positron-server/get_started.html
#
# Chartpress-managed (see chartpress.yaml) but, like images/postgres, only
# used by one deployment, so its tag is never auto-written to values.yaml --
# copy the tag chartpress prints into deployments/stat/config/common.yaml by
# hand. See docs/tasks/positron.qmd for the full rebuild steps.

FROM python:3.11-slim

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends wget ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir jupyter-positron-verifier

# The verifier only needs resources/activation/linux/x86_64/ (the
# license-manager binary), but the release tarball can't be extracted
# selectively, so we pull the same build used by stat-user-image.
RUN wget --quiet -O /tmp/positron-server.tar.gz \
      https://cdn.posit.co/positron/releases/server/x86_64/positron-server-linux-x64-2026.07.1-5.tar.gz && \
    mkdir -p /opt/positron-server && \
    tar -xzf /tmp/positron-server.tar.gz -C /opt/positron-server --strip-components=1 && \
    rm /tmp/positron-server.tar.gz

# license.lic and signing-key.pem are never baked in -- they're mounted at
# deploy time from deployments/stat/secrets/{staging,prod}.yaml via
# hub.extraFiles.
EXPOSE 10101
CMD ["positron-verifier"]

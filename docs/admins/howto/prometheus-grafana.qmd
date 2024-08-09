---
title: Prometheus and Grafana
---

# Accessing the Prometheus Server

It can be useful to interact with the cluster's prometheus server while
developing dashboards in grafana. You will need to forward a local port
to the prometheus server's pod.

## Using the standard port

Listen on port 9090 locally, forwarding to the prometheus server's port
`9090`.

``` bash
kubectl -n support port-forward deployment/support-prometheus-server 9090
```

then visit http://localhost:9090.

## Using an alternative port

Listen on port 8000 locally, forwarding to the prometheus server's port `9090`.

``` bash
kubectl -n support port-forward deployment/support-prometheus-server 8000:9090
```

then visit http://localhost:8000.

# Grafana

Our Grafana dashboards are at https://grafana.datahub.berkeley.edu.
Upstream documentation is at https://jupyterhub-grafana.readthedocs.io/en/latest/index.html.

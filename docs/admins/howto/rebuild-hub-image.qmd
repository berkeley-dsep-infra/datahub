---
title: Rebuild a custom hub image
---

We use a customized JupyterHub image so we can use versions of hub
packages (such as authenticators) and install additional software
required by custom config we might have.

The image is located in `images/hub`. It *must* inherit from the
JupyterHub image used in the [Zero to
JupyterHub](https://z2jh.jupyter.og).

[chartpress](https://github.com/jupyterhub/chartress) is used to build
the image and update `hub/values.yaml` with the new image version.
`chartpress` may be installed locally with `pip install chartpress`.

1.  Run `gcloud auth configure-docker us-central1-docker.pkg.dev` *once
    per machine* to setup docker for authentication with the [gcloud
    credential
    helper](https://cloud.google.com/artifact-registry/docs/docker/authentication).
2.  Modify the image in `images/hub` and make a git commit.
3.  Run `chartpress --push`. This will build and push the hub image, and
    modify `hub/values.yaml` appropriately.
4.  Make a commit with the `hub/values.yaml` file, so the new hub image
    name and tag are comitted.
5.  Proceed to deployment as normal.

Some of the following commands may be required to configure your
environment to run the above chartpress workflow successfully:

-   `gcloud auth login`
-   `gcloud auth configure-docker us-central1-docker.pkg.dev`
-   `gcloud auth application-default login`
-   sometimes running `gcloud auth login` additional time(s) may fix
    issues
-   `sudo usermod -a -G docker ${USER}`
-   `gcloud auth configure-docker`

# Rebuild the custom postgres image

For data100, we provide a postgresql server per user. We want the
[python
extension](https://www.postgresql.org/docs/current/plpython.html)
installed. So we inherit from the [upstream postgresql docker
image](https://hub.docker.com/_/postgres), and add the appropriate
package.

This image is in `images/postgres`. If you update it, you need to
rebuild and push it.

1.  Modify the image in `images/postgres` and make a git commit.
2.  Run `chartpress --push`. This will build and push the image, *but
    not put anything in YAML*. There is no place we can put thi in
    `values.yaml`, since this is only used for data100.
3.  Notice the image name + tag from the `chartpress --push` command,
    and put it in the appropriate place (under `extraContainers`) in
    `data100/config/common.yaml`.
4.  Make a commit with the new tag in `data100/config/common.yaml`.
5.  Proceed to deploy as normal.

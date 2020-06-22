.. _howto/rebuild-hub-image:

============================
Rebuild the custom hub image
============================

We use a customized JupyterHub image so we can use versions of
hub packages (such as authenticators) and install additional
software required by custom config we might have.

The image is located in ``images/hub``. It *must* inherit from
the JupyterHub image used in the `Zero to JupyterHub <https://z2jh.jupyter.og>`_.

`chartpress <https://github.com/jupyterhub/chartress>`_ is used to
build the image and update ``hub/values.yaml`` with the new image
version.

#. Modify the image in ``images/hub`` and make a git commit.

#. Run ``chartpress --push``. This will build and push the hub image,
   and modify ``hub/values.yaml`` appropriately.

#. Make a commit with the ``hub/values.yaml`` file, so the new hub image
   name and tag are comitted.

#. Proceed to deployment as normal.

=================================
Rebuild the custom postgres image
=================================

For data100, we provide a postgresql server per user. We want the
`python extension <https://www.postgresql.org/docs/current/plpython.html>`_
installed. So we inherit from the `upstream postgresql docker image
<https://hub.docker.com/_/postgres>`_, and add the appropriate package.

This image is in ``images/postgres``. If you update it, you need to
rebuild and push it.

#. Modify the image in ``images/postgres`` and make a git commit.

#. Run ``chartpress --push``. This will build and push the image,
   *but not put anything in YAML*. There is no place we can put thi
   in ``values.yaml``, since this is only used for data100.

#. Notice the image name + tag from the ``chartpress --push`` command,
   and put it in the appropriate place (under ``extraContainers``) in
   ``data100/config/common.yaml``.

#. Make a commit with the new tag in ``data100/config/common.yaml``.

#. Proceed to deploy as normal.
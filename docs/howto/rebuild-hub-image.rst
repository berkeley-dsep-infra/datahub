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

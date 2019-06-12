.. _topic/credentials:

=================
Cloud Credentials
=================

Google Cloud
============

Service Accounts
----------------

Service accounts are identified by a *service key*, and help us grant
specific access to an automated process. Our CI process needs two service accounts to operate:

#. A ``gcr-readwrite`` key. This is used to build and push the user images.
   Based on the `docs <https://cloud.google.com/container-registry/docs/access-control>`_,
   this is assigned the role ``roles/storage.admin``.

#. A ``gke`` key. This is used to interact with the Google Kubernetes cluster.
   Roles `roles/container.clusterViewer` and `roles/container.developer` are
   granted to it.

These are currently copied into the ``secrets/`` dir of every deployment, and
explicitly referenced from ``hubploy.yaml`` in each deployment. They should
be rotated every few months.

You can `create service accounts <https://nextjournal.com/schmudde/how-to-version-control-jupyter>`_
through the web console or the commandline. Remember to not leave around copies
of the private key elsewhere on your local computer!

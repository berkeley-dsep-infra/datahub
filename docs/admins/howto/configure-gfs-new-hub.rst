.. _howto/configure-gfs-new-hub:

================
How to deploy google filestore for a hub
================

#. create the filestore instance in the web UI
#. mount the filestore on nfsserver-01 (typically to the ``/export/<hub_name>-filestore`` directory)
   .. code:: bash
      mount <filestore_ip>:/shares /export/<hub_name>-filestore

#. if necessary, create the ``<hub_name>-filestore/<hub_name>`` subdir in the root of that filestore share
#. change ownership of that dir tree to 1000:1000:
   .. code:: bash
      chown -R 1000:1000 <hub_name>

#. from this subdirectory, execute the following ``gcloud`` command to update the instance to ``ROOT_SQUASH``.  the ``flags-file`` is found in that hub's ``config/filestore/<hub_name>-squash-flags.json``:
   .. code:: bash
      gcloud filestore instances update <hub_filestore_instance_name> --zone=us-central1-b --flags-file=<hub_name>-squash-flags.json

make sure that you are using the correct instance name for the update.  you can get this in the web console for filestore.

# when to update this file?

1. when creating a new filestore share to set ``ROOT_SQUASH``
2. scaling up storage

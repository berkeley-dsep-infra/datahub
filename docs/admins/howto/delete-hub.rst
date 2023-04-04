
.. _howto/delete-hub:

================
Delete or spin down a Hub
================


Why delete or spin down a hub?
=====================

Sometimes we want to spin down or delete a hub:

#. A course or department won't be needing their hub for a while
#. The hub will be re-deployed in to a new or shared node pool.



Steps to spin down a hub:
------------
If the hub is using a shared filestore, skip all filestore steps.

If the hub is using a shared node pool, skip all namespace and node pool steps.

#. Create filestore backup
#. Log in to ``nfsserver-01`` and unmount filestore from nfsserver: ``sudo umount /export/<hubname>-filestore``
#. Comment out the hub build steps out in ``.circleci/config.yaml`` (deploy and build steps)
#. Comment hub entries out of ``datahub/node-placeholder/values.yaml``
#. Delete k8s namespace:  ``kubectl delete namespace <hubname>-staging <hubname>-prod``
#. Delete k8s node pool:  ``gcloud container node-pools delete <hubname> --project "ucb-datahub-2018" --cluster "fall-2019" --region "us-central1"``
#. Delete filestore:  ``gcloud filestore instances delete <hubname>-filestore --zone "us-central1-b"``
#. Delete PV:  ``kubectl get pv --all-namespaces|grep <hubname>`` to get the PV names, and then ``kubectl pv delete <pv names>``
#. All done.

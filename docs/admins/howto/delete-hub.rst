
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

#. Scale the node pool to zero: ``kubectl -n <hubname-prod|staging> scale --replicas=0 deployment/hub``
#. Kill any remaining users' servers.  Find any running servers with ``kubectl -n <hubname-prod|staging> get pods | grep jupyter`` and then ``kubectl -n <hubname-prod|staging> delete pod <pod name>`` to stop them.
#. Create filestore backup:  ``gcloud filestore backups create <hubname>-backup-YYYY-MM-DD --file-share=shares --instance=<hubname-YYYY-MM-DD> --region "us-central1" --labels=filestore-backup=<hub name>,hub=<hub name>``
#. Log in to ``nfsserver-01`` and unmount filestore from nfsserver: ``sudo umount /export/<hubname>-filestore``
#. Comment out the hub build steps out in ``.circleci/config.yaml`` (deploy and build steps)
#. Comment out GitHub label action for this hub in ``.github/labeler.yml``
#. Comment hub entries out of ``datahub/node-placeholder/values.yaml``
#. Delete k8s namespace:  ``kubectl delete namespace <hubname>-staging <hubname>-prod``
#. Delete k8s node pool:  ``gcloud container node-pools delete <hubname> --project "ucb-datahub-2018" --cluster "fall-2019" --region "us-central1"``
#. Delete filestore:  ``gcloud filestore instances delete <hubname>-filestore --zone "us-central1-b"``
#. Delete PV:  ``kubectl get pv --all-namespaces|grep <hubname>`` to get the PV names, and then ``kubectl delete pv <pv names>``
#. All done.

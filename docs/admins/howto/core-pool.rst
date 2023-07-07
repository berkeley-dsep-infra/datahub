
.. _howto/core-pool:

================
Creating and managing the core node pool
================


What is the core node pool?
---------------------------

The core node pool is the primary entrypoint for all hubs we host.  It manages
all incoming traffic, and redirects said traffic (via the nginx ingress
controller) to the proper hub.

It also does other stuff.


Deploying a new core node pool
------------------------------

Run the following commend to create the node pool:

.. code:: bash

  gcloud container node-pools create "core-<YYYY-MM-DD>"  \
    --labels=hub=core,nodepool-deployment=core \
    --node-labels hub.jupyter.org/pool-name=core-pool --machine-type "n2-standard-8"  \
    --enable-autoscaling --min-nodes "1" --max-nodes "20" \
    --project "ucb-datahub-2018" --cluster "fall-2019" --region "us-central1" --node-locations "us-central1-b" \
    --tags hub-cluster \
    --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "100"  \
    --metadata disable-legacy-endpoints=true \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
    --no-enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --max-pods-per-node "110" \
    --system-config-from-file=vendor/google/gke/node-pool/config/core-pool-sysctl.yaml


The ``system-config-from-file`` argument is important, as we need to tune the
kernel TCP settings to handle large numbers of concurrent users and keep nginx
from using up all of the TCP ram.

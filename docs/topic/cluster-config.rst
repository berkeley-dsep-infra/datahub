.. _topic/cluster-config:

================================
Kubernetes Cluster Configuration
================================

We use `kubernetes <http://kubernetes.io/>`_ to run our JupyterHubs. It has
a healthy open source community, managed offerings from multiple vendors &
a fast pace of development. We can run easily on many different cloud 
providers with similar config by running on top of Kubernetes, so it is also
our cloud agnostic abstraction layer.

We prefer using a managed Kubernetes service (such as `Google Kubernetes Engine
<https://cloud.google.com/kubernetes-engine/>`_). This document lays out our
preferred cluster configuration on various cloud providers.

Google Kubernetes Engine
========================

In our experience, Google Kubernetes Engine (GKE) has been the most stable,
performant, and reliable managed kubernetes service. We prefer running on this
when possible.

A ``gcloud container clusters create`` command can succintly express the
configuration of our kubernetes cluster. The following command represents
the currently favored configuration.

.. code:: bash

   gcloud container clusters create \
        --enable-ip-alias \
        --enable-autoscaling \
        --max-nodes=20 --min-nodes=2 \
        --region=us-central1 --node-locations=us-central1-b \
        --image-type=ubuntu \
        --disk-size=100 --disk-type=pd-standard \
        --machine-type=n1-highmem-8 \
        --cluster-version latest \
        --no-enable-autoupgrade \
        --enable-network-policy \
        --create-subnetwork="" \
        <cluster-name>

.. note::

   The following flags have been recently added for additional security.
   All new clusters created should have them, but older clusters might not.

     #. ``--enable-network-policy``

We will try explain the various arguments to this command line invocation.

IP Aliasing
-----------

``--enable-ip-alias`` creates `VPC Native Clusters <https://cloud.google.com/kubernetes-engine/docs/how-to/alias-ips>`_.

This becomes the default soon, and can be removed once it is the default.

Autoscaling
-----------

We use the `kubernetes cluster autoscaler <https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler>`_
to scale our node count up and down based on demand. It waits until the cluster is completely full
before triggering creation of a new node - but that's ok, since new node creation time on GKE is
pretty quick.

``--enable-autoscaling`` turns the cluster autoscaler on. 

``--min-nodes`` sets the minimum number of nodes that will be maintained
regardless of demand. This should ideally be 2, to give us some headroom for
quick starts without requiring scale ups when the cluster is completely empty.

``--max-nodes`` sets the maximum number of nodes that the cluster autoscaler
will use - this sets the maximum number of concurrent users we can support.
This should be set to a reasonably high number, but not too high - to protect
against runaway creation of hundreds of VMs that might drain all our credits
due to accident or security breach.

Highly available master
-----------------------

The kubernetes cluster's master nodes are managed by Google Cloud automatically.
By default, it is deployed in a non-highly-available configuration - only one
node. This means that upgrades and master configuration changes cause a few minutes
of downtime for the kubernetes API, causing new user server starts / stops to fail.

We request our cluster masters to have `highly available masters <https://cloud.google.com/kubernetes-engine/docs/concepts/regional-clusters>`_
with ``--region`` parameter. This specifies the region where our 3 master nodes
will be spread across in different zones. It costs us nothing extra, so we should
always do it.

By default, asking for highly available masters also asks for 3x the node count,
spread across multiple zones. We don't want that, since all our user pods have
in-memory state & can't be relocated. Specifying ``--node-locations`` explicitly
lets us control how many and which zones the nodes are located in.

Region / Zone selection
-----------------------

We generally use the ``us-central1`` region and a zone in it for our clusters -
simply because that is where we have asked for `quota <https://cloud.google.com/compute/quotas>`_.

There are regions closer to us, but latency hasn't really mattered so we are
currently still in us-central1. There are also unsubstantiated rumors that us-central1 is their
biggest data center and hence less likely to run out of quota.

Ubuntu operating system
-----------------------

Since we use :ref:`NFS for user home directories <topic/storage>`, we select
Ubuntu as our `node operating system <https://cloud.google.com/kubernetes-engine/docs/concepts/node-images>`_.
The default (Container Optimized OS) does not have NFS support enabled.

Disk Size
---------

``--disk-size`` sets the size of the root disk on all the kubernetes nodes. This
isn't used for any persistent storage such as user home directories. It is only
used ephemerally for the operations of the cluster - primarily storing docker
images and other temporary storage. We can make this larger if we use a large number
of big images, or if we want our image pulls to be faster (since disk performance
`increases with disk size <https://cloud.google.com/compute/docs/disks/performance>`_
).

``--disk-type=pd-standard`` gives us standard spinning disks, which are cheaper. We
can also request SSDs instead with ``--disk-type=pd-ssd`` - it is much faster,
but also much more expensive. 

Node size
---------

``--machine-type`` lets us select how much `RAM and CPU <https://cloud.google.com/compute/docs/machine-types>`_
each of our nodes have. For non-trivial hubs, we generally pick ``n1-highmem-8``, with 52G
of RAM and 8 cores. This is based on the following heuristics:

#. Students generally are memory limited than CPU limited. In fact, while we
   have a hard limit on memory use per-user pod, we do not have a CPU limit -
   it hasn't proven necessary.

#. We try overprovision clusters by about 2x - so we try to fit about 100G of total RAM
   use in a node with about 50G of RAM. This is accomplished by setting the memory
   request to be about half of the memory limit on user pods. This leads to massive
   cost savings, and works out ok.

#. There is a kubernetes limit on 100 pods per node.

Based on these heuristics, ``n1-highmem-8`` seems to be most bang for the buck
currently. We should revisit this for every cluster creation.

Cluster version
---------------

GKE automatically upgrades cluster masters, so there is generally no harm in being
on the latest version available.

Node autoupgrades
-----------------

When node autoupgrades are enabled, GKE will automatically try to
upgrade our nodes whenever needed (our GKE version falling off the
support window, security issues, etc). However, since we run stateful
workloads, we *disable* this right now so we can do the upgrades
manually.

Network Policy
--------------

Kubernetes `Network Policy <https://kubernetes.io/docs/concepts/services-networking/network-policies/>`_
lets you firewall internal access inside a kubernetes cluster, whitelisting
only the flows you want. The JupyterHub chart we use supports setting up
appropriate NetworkPolicy objects it needs, so we should turn it on for
additional security depth. Note that any extra in-cluster services we run
*must* have a NetworkPolicy set up for them to work reliabliy.

Cluster name
------------

We try use a descriptive name as much as possible.


Azure Kubernetes Service
========================

Subscription owner access
-------------------------

Use 'role', not cluster. Global administrator on the directory service.

SPA / Account access clusterfuck
--------------------------------

Options: Use your gmail.com address, or use ds-instr SPA. Using berkeley.edu
account with azure without the SPA might make you want to tear your
hair out.

Microsoft Azure also provides a managed kubernetes service and we have run
at least one large course on it each semester. The following commands will
create a suitable cluster on AKS:

.. code:: bash

   az group create --name <group-name> --location=westus2

Make a new SSH Key
------------------

Put it in secrets folder

.. code:: bash

   ssh-keygen -f deployments/<deployment-name>/secrets/aks_ssh_key

Create service principal
------------------------

You should create a new service principal for this cluster. We should
probably scope this a bit more, otherwise I think this gives it too
many privileges.

.. code:: bash

   az ad sp create-for-rbac \
      --role=Contributor \
      --scopes=/subscriptions/<uuid-of-active subscription> \
      -o json > deployments/<deployment-name>/secrets/serviceprincipal.json

Kubernetes Version
------------------

Find out latest version of Kubernetes supported by AKS and use it.
Move forward if possible, not backwards. 'Stability' is a myth and does
not exist in this world we have now.

.. code:: bash

   az aks get-versions -l westus2

Create cluster
--------------
.. code:: bash

   export AZURE_CLUSTER_NAME=data100-fall-2019
   export AZURE_DEPLOYMENT=data100

Pick the latest version at this time. You *might* need to update your local
version of az to get this more accurate.

    az aks create \
        --name $AZURE_CLUSTER_NAME \
        --resource-group $AZURE_CLUSTER_NAME \
        --ssh-key-value deployments/$AZURE_DEPLOYMENT/secrets/aks_ssh_key.pub \
        --node-count 1 \
        --node-vm-size Standard_E16s_v3 \
        --node-osdisk-size 100 \
        --kubernetes-version 1.14.0 \
        --nodepool-name default \
        --service-principal $(jq -r .appId deployments/$AZURE_DEPLOYMENT/secrets/serviceprincipal.json) \
        --client-secret $(jq -r .password deployments/$AZURE_DEPLOYMENT/secrets/serviceprincipal.json) \
        --output table

The first command creates a `resource group <https://docs.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest>`_ in a local region and the second
creates the `cluster <https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest>`_. The options are fairly self explanatory.

.. note::

    Make sure to specify a VM type that supports premium storage disks.
    For example "E2s-64 v3" does, but "E2-64 v3" does not.

AKS and SSH
-----------

`Connecting to Azure nodes by ssh
<https://docs.microsoft.com/en-us/azure/aks/ssh#create-the-ssh-connection>`_ is
not as simple as ``gcloud compute ssh``. One must run a vanilla Linux pod
in-cluster, add an ssh client, copy an ssh key to it, then exec into the pod.

.. code:: bash
    # start a Linux pod
    computer$ kubectl run -it --rm aks-ssh --image=debian
    pod# apt-get update && apt-get install openssh-client -y

    # determine the name of the ssh pod
    computer$ kubectl get pods
    computer$ kubectl cp /path/to/ssh-key aks-ssh-<rest-of-pod-name>:/id_rsa

    # ssh to one of the cluster nodes
    pod# chmod 0600 id_rsa
    pod# ssh -i /id_rsa azureuser@<node-ip>

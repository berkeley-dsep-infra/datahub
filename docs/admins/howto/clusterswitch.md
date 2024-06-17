# Switching over a hub to a new cluster

This document describes how to switch an existing hub to a new cluster.  The example used here refers to moving all UC Berkeley Datahubs.

You might find it easier to switch to a new cluster if you're running a [very old k8s version](https://cloud.google.com/kubernetes-engine/docs/release-notes), or in lieu of performing a [cluster credential rotation](https://cloud.google.com/kubernetes-engine/docs/how-to/credential-rotation).

## Create a new cluster
1. Create a new cluster using the specifications here:  
   https://docs.datahub.berkeley.edu/en/latest/admins/cluster-config.html
2. Set up helm on the cluster according to the instructions here:  
   http://z2jh.jupyter.org/en/latest/setup-helm.html
     - Make sure the version of helm you're working with matches the version CircleCI is using.  
       For example:  https://github.com/berkeley-dsep-infra/datahub/blob/staging/.circleci/config.yml#L169
3. Re-create all existing node pools for hubs, support and prometheus deployments in the new cluster.  If the old cluster is still up and running, you will probably run out of CPU quota, as the new node pools will immediately default to three nodes.  Wait ~15m for the new pools to wind down to zero, and then continue.

## Setting the 'context' for kubectl and work on the new cluster.
1. Ensure you're logged in to GCP:  `gcloud auth login`
2. Pull down the credentials from the new cluster:  `gcloud container clusters get-credentials <CLUSTER_NAME> --region us-central1`
3. Switch the kubectl context to this cluster:  `kubectl config use-context gke_ucb-datahub-2018_us-central1_<CLUSTER_NAME>`

## Recreate node pools
Re-create all existing node pools for hubs, support and prometheus deployments in the new cluster.

If the old cluster is still up and running, you will probably run out of CPU quota, as the new node pools will immediately default to three nodes.  Wait ~15m for the new pools to wind down to zero, and then continue.

## Install and configure the certificate manager
Before you can deploy any of the hubs or support tooling, the certificate manager must be installed and
configured on the new cluster.  Until this is done, `hubploy` and `helm` will fail with the following error:
`ensure CRDs are installed first`.

1. Create a new feature branch and update your helm dependencies:  `helm dep up`
2. At this point, it's usually wise to upgrade `cert-manager` to the latest version found in the chart repo.
   You can find this by running the following command:

		cert-manager-version=$(helm show all -n cert-manager jetstack/cert-manager | grep ^appVersion |  awk '{print $2}')

3. Then, you can install the latest version of `cert-manager`:

		kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/${cert-manager-version}/cert-manager.yaml

4. Change the corresponding entry in `support/requirements.yaml` to `$cert-manager-version` and commit the changes (do not push).

## Create the node-placeholder k8s namespace
The [calendar autoscaler](https://docs.datahub.berkeley.edu/en/latest/admins/howto/calendar-scaler.html) requires the `node-placeholder` namespace.  Run the following command to create it:

		kubectl create namespace node-placeholder

## Create a new static endpoint IP and switch DNS to point our new deployment at it.
1. Create a new static endpoint IP in the [GCP console](https://console.cloud.google.com/networking/addresses/add?project=ucb-datahub-2018).
2. Grab the new endpoint:  `gcloud container clusters describe <CLUSTER_NAME> --region us-central1 | grep ^endpoint`
3. Open [infoblox](https://infoblox.net.berkeley.edu) and change the wildcard and empty entries for datahub.berkeley.edu to point to the IP from the previous step.
4. Update `support/values.yaml`, under `ingress-nginx` with the newly created IP from infoblox:  `loadBalancerIP: xx.xx.xx.xx`.
5. Add and commit this change to your feature branch (still do not push).

You will re-deploy the support chart in the next step.

## Manually deploy the support and prometheus pools
First, update any node pools in the configs to point to the new cluster.  Typically, this is just for the `ingress-nginx` controllers in `support/values.yaml`.

Now we will manually deploy the `support` helm chart:

		sops -d support/secrets.yaml > /tmp/secrets.yaml
		helm install -f support/values.yaml -f /tmp/secrets.yaml -n support support support/ --set installCRDs=true --debug --create-namespace

Before continuing, confirm via the GCP console that the IP that was defined in step 1 is now [bound to a forwarding rule](https://console.cloud.google.com/networking/addresses/list?project=ucb-datahub-2018). You can further confirm by listing the services in the [support chart](https://github.com/berkeley-dsep-infra/datahub/blob/staging/support/requirements.yaml) and making sure the ingress-controller is using the newly defined IP.

One special thing to note: our `prometheus` instance uses a persistent volume that contains historical monitoring data.  This is specified in `support/values.yaml`, under the `prometheus:` block:

		persistentVolume:
		  size: 1000Gi
		  storageClass: ssd
		  existingClaim: prometheus-data-2024-05-15

## Manually deploy a hub to staging
Finally, we can attempt to deploy a hub to the new cluster!  Any hub will do, but we should start with a low-traffic hub (eg:  https://dev.datahub.berkeley.edu).

First, check the hub's configs for any node pools that need updating.  Typically, this is just the core pool.

Second, update `hubploy.yaml` for this hub and point it to the new cluster you've created.

After this is done, add the changes to your feature branch (but don't push).  After that, deploy a hub manually:

		hubploy deploy dev hub staging

When the deploy is done, visit that hub and confirm that things are working.

## Manually deploy remaining hubs to staging and prod
Now, update the remaining hubs' configs to point to the new node pools and `hubploy.yaml` to the cluster.

Then use `hubploy` to deploy them to staging as with the previous step.  The easiest way to do this is to have a list of hubs in a text file, and iterate over it with a `for` loop:

		for x in $(cat hubs.txt); do hubploy deploy ${x} hub staging; done
		for x in $(cat hubs.txt); do hubploy deploy ${x} hub prod; done

When done, add the modified configs to your feature branch (and again, don't push yet).

## Update CircleCI
Once you've successfully deployed the clusters manually via `hubploy`, it's time to update CircleCI to point to the new cluster.

All you need to do is `grep` for the old cluster name in `.circleci/config.yaml` and change this to the name of the new cluster.  There should just be four entries:  two for the `gcloud get credentials <cluster-name>`, and two in comments.  Make these changes and add them to your existing feature branch, but don't commit yet.

## Create and merge your PR!
Now you can finally push your changes to github.  Create a PR, merge to `staging` and immediately kill off the deploy jobs for `node-placeholder`, `support` and `deploy`.

Create another PR to merge to `prod` and that deploy should work just fine.

FIN!

## Deleting the old cluster

After waiting a reasonable period of time (a day or two just to be cautious) and after fetching the usage logs, you may delete the old cluster:

    gcloud container clusters delete ${OLDCLUSTER} --region=us-central1

# Switching over a hub to a new cluster

This document describes how to switch an existing hub to a new cluster.  The example used here refers to the data8x hub.

## Make a new cluster
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

## Switch DNS to the new cluster's endpoint IP and point our deployment at it.
1. Grab the new endpoint:  `gcloud container clusters describe <CLUSTER_NAME> --region us-central1 | grep ^endpoint`
2. Open [infoblox](https://infoblox.net.berkeley.edu) and change the wildcard entry for datahub to the IP from the previous step.
3. Create a new static IP.
4. Update `support/values.yaml`, under `ingress-nginx` with the newly created IP from infoblox:  `loadBalancerIP: xx.xx.xx.xx`
5. Add and commit this change to your feature branch (still do not push).

## Manually deploy the support and prometheus pools
First, update any node pools in the configs to point to the new cluster.  Typically, this is just for the `ingress-nginx` controllers in `support/values.yaml`.

Now we will manually deploy the `support` helm chart:

		sops -d support/secrets.yaml > /tmp/secrets.yaml
		helm install -f support/values.yaml -f /tmp/secrets.yaml -n support support support/ --set installCRDs=true --debug --create-namespace

One special thing to note: our `prometheus` instance uses a persistent volume that contains historical monitoring data.  This is specified in `support/values.yaml`, under the `prometheus:` block:

		persistentVolume:
		  size: 1000Gi
		  storageClass: ssd
		  existingClaim: prometheus-data-2024-05-15

## Manually deploy a hub to staging
Finally, we can attempt to deploy a hub to the new cluster!  Any hub will do, but we should start with a low-traffic hub (eg:  https://dev.datahub.berkeley.edu).

First, check the hub's configs for any node pools that need updating.  Typically, this is just the core pool.  After this is done, add the changes to your feature branch (but don't push).  After that, deploy a hub manually:

		hubploy deploy dev hub staging

When the deploy is done, visit that hub and confirm that things are working.

## Manually deploy remaining hubs to staging
Now, update the remaining hubs' configs to point to the new core pool and use `hubploy` to deploy them to staging as with the previous step.  The easiest way to do this is to have a list of hubs in a text file, and iterate over it with a `for` loop:

		for x in $(cat hubs.txt); do hubploy deploy ${x} hub staging; done

When done, add the modified configs to your feature branch (and again, don't push yet).

## Update CircleCI
Once you've successfully deployed the clusters manually via `hubploy`, it's time to update CircleCI to point to the new cluster.

All you need to do is `grep` for the old cluster name in `.circleci/config.yaml` and change this to the name of the new cluster.  There should just be four entries:  two for the `gcloud get credentials <cluster-name>`, and two in comments.  Make these changes and add them to your existing feature branch, but don't commit yet.

## Switch staging over to new cluster
1. Change the name of the cluster in hubploy.yaml to match the name you chose when creating your new cluster.
2. Make sure the staging IP is a 'static' IP - so we don't lose the IP.  You can see the list of IPs used by the project by checking the google cloud console.  
   For example:  https://console.cloud.google.com/networking/addresses/list?project=data8x-scratch  
   Make sure you are in the right project! 
3. If the staging IP (which you can find in staging.yaml) is marked as 'ephemeral', mark it as 'static'
4. Make a PR that includes your hubploy.yaml change, but don't merge it just yet.

Now we will perform the IP switch over from the old cluster to the new cluster.  There will be downtime during the switchover!

The current easiest way to do this is:
1. Merge the PR.
2. Immediately delete the service 'proxy-public' in the appropriate staging namespace in the old cluster. Make sure you have the command ready for this so that you can execute reasonably quickly.

		gcloud container clusters list
		gcloud container clusters get-credentials ${OLDCLUSTER} --region=us-central1
		kubectl --namespace=data8x-staging get svc
		kubectl --namespace=data8x-staging delete svc proxy-public
		
As the PR deploys, staging on the new cluster should pick up the IP we released from the old cluster.  This way we don't have to wait for DNS propagation time.

At this time you can switch to the new cluster and watch the pods come up.

Once done, poke around and make sure the staging cluster works fine.  Since data8x requires going through EdX in order to load a hub, testing can be tricky.  If you're able, the easiest way is to edit an old course you have access to and point one the notebooks to the staging instance.

Assuming everything worked correctly, you can follow the above steps to switch production over.

## Get hub logs from old cluster
Prior to deleting the old cluster, fetch the usage logs.

    HUB=data8x
    kubectl --namespace=${HUB}-prod exec -it $(kubectl --namespace=${HUB}-prod get pod -l component=hub -o name | sed 's_pod/__') -- grep -a 'seconds to ' jupyterhub.log > ${HUB}-usage.log

Currently these are being placed on google drive here:  
  https://drive.google.com/open?id=1bUIJYGdFZCgmFXkhkPzFalJ1v9T8v7__

## Deleting the old cluster

After waiting a reasonable period of time (a day or two just to be cautious) and after fetching the usage logs, you may delete the old cluster:

    gcloud container clusters delete ${OLDCLUSTER} --region=us-central1

# Switching over a hub to a new cluster

This document describes how to switch an existing hub to a new cluster.  The example used here refers to the data8x hub.

## Make a new cluster
1. Create a new cluster using the specifications here:  
   https://docs.datahub.berkeley.edu/en/latest/topic/cluster-config.html
2. Set up helm on the cluster according to the instructions here:  
   http://z2jh.jupyter.org/en/latest/setup-helm.html
     - Make sure the version of helm you're working with matches the version CircleCI is using.  
       For example:  https://github.com/berkeley-dsep-infra/datahub/blob/staging/.circleci/config.yml#L169

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

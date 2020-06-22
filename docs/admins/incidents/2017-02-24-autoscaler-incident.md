# Custom Autoscaler gonee haywire

## Summary ##
On the evening of February 24, 2017, a premature version of the Autoscaler script for the Datahub deployment was mistakenly run on the prod cluster, resulting in a large amount of nodes (roughly 30-40) being set as unschedulable for about 20 minutes. Though no information was lost nor service critically disturbed, it was necessary to manually re-enable these nodes to be scheduled.

## Timeline ##
As of this [commit](https://github.com/data-8/jupyterhub-k8s/commit/6c042ebb6a88f0059d80e664795f4ce9252c043f) in the Autoscaler branch history, there exists a `scale.py` file that would based on the utilization of the cluster, mark a certain number of nodes unschedulable before attempting to shut down nodes with no pods in them. Unfortunately, this script was executed prematurely, and without configuration, looked to execute in whatever context currently specified in `.kube/config`, which ended up being the production cluster rather than the dev cluster.

### 2017-02-24 11:14 PM ###
Script is mistakenly executed. A bug in the calculations for the utilization of the cluster leads to about 40 nodes being marked as unschedulable. The mistake is noted immediately.

### 2017-02-24 11:26 PM ###
The unschedulability of these nodes is reverted. All nodes in the cluster were first all set to be schedulable to ensure that no students current and future would be disturbed. Immediately after, 10 of the most idle nodes on the cluster were manually set to be unschedulable (to facilitate them later being manually descaled - to deal with https://github.com/data-8/infrastructure/issues/6) using `kubectl cordon <node_name>`.

## Conclusion ##

A cluster autoscaler script was accidentally run against the production cluster instead of the dev cluster, reducing capacity for new user logins for about 12 minutes. There was still enough capacity so we had no adverse effects.

## Action Items ##

### Datahub Deployment Changes ###
1. The Autoscaler should not be run unless the context is explicitly set via environment variables or command line arguments. This is noted in the comments of the [pull request](https://github.com/data-8/jupyterhub-k8s/pull/117) for the Autoscaler.
2. The idea of the ‘current context’ should be abolished in all the tools we build / read.

### Future organizational change ###

1. Use a separate billing account for production vs development clusters. This makes it harder to accidentally run things on the wrong cluster



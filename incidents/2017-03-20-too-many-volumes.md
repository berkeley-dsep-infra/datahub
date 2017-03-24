## Summary ##

From sometime early March 20 2017 till about 1300, some new student servers were stuck in `Pending` forever, giving them 500 errors. This was an unintended side-effect of [reducing student memory limit to 1G](https://github.com/data-8/infrastructure/issues/16) while keeping the size of our nodes constant, causing us to hit a Google Cloud limit on number of disks per node. This was fixed by spawning more nodes that were smaller.

## Timeline ##

### March 18, 16:30 ##

RAM per student is [reduced](https://github.com/data-8/infrastructure/issues/16) from 2G to 1G, as a resource optimization measure. The size of our nodes remains the same (26G RAM), and many are cordonned off and slowly decomissioned over the coming few days.

Life seems fine, given the circumstances.

### March 20, 12:44 ##

New student servers report a 500 error preventing them from logging on. This is deemed widespread & not an isolated incident.

### 12:53 ##

A `kubectl describe pod` on an affected student's pod shows it's stuck in `Pending` state, with an error message:

```
pod failed to fit in any node fit failure on node (XX): MaxVolumeCount
```

This seems to be common problem for all the new student servers, which are all stuck in `Pending` state.

Googling leads to https://github.com/kubernetes/kubernetes/issues/24317 - even though Google Compute Engine can handle more than 16 disks per node (we had checked this before deploying), Kubernetes itself still can not. This wasn't foreseen, and seemed to be the direct cause of the incident.

### 13:03 ###

A copy of the instance template that is used by Google Container Engine is made and then modified to spawn smaller nodes (n1-highmem-2 rather than n1-highmem-4). The managed instance group used by Google Container Engine is then modified to use the new template. This was the easiest way to not distrupt students for whom things *are* working, while also allowing new students to be able to log in.

This new instance group was then set to expand for 30 new nodes, which will provide capacity for about 12 students each. `populate.bash` was also run to make sure that students pods start up on time in the newnodes.

### 13:04 ###

The simple autoscaler is stopped, on fear that it'll be confused by the unusal mixed state of the nodes and do something wonky.

### 13:11 ###

All the new nodes are online, and `populate.bash` has completed. Pods start leaving the `Pending` state.

However, since it's been more than the specified timeout that JupyterHub will wait before giving up on Pod (5 minutes), JupyterHub doesn't know the pods exist. This causes state of cluster + state in JupyterHub to go out of sync, causing the dreaded 'redirected too many times' error. Admins need to manually stop and start user pods in the control panel as users report this to fix this issue.

### 14:23 ###

The hub and proxy pods are restarted since there were plenty of 'redirected too many times' errors. This seems to catch most users state, although some requests still failed with a 599 timeout (similar to [an earlier incident](2017-02-24-proxy-death-incident.md), but much less frequent). A long tail of manual user restarts are performed by admins over the next few days.

## Action Items ##

### Upstream: Kubernetes ###

1. Keep an eye on the status of [the bug we ran into](https://github.com/kubernetes/kubernetes/issues/24317)

### Upstream: JupyterHub ###

1. Track down and fix the 'too many redirects' issue at source. [Issue](https://github.com/data-8/infrastructure/issues/17)

### Cleanup ###

1. Delete all the older larger nodes that are no longer in use. (Done!)

### Monitoring ###

1. Have alerting for when there are any number of pods in `Pending` state for a non-negligible amount of time. There is always something wrong when this happens.

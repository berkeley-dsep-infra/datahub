# Proxy eviction strands user

## Summary ##

On the evening of Feb 23, several students started experiencing 500 errors in trying to access datahub. The proxy had died because of [a known issue](https://github.com/data-8/infrastructure/issues/6), and it took a while for the hub to re-add all the user routes to the proxy. Some students’ needed their servers to be manually restarted, due to a JupyterHub spawner bug that is showing up at scale. Everything was fixed in about 40 minutes.

## Timeline ##

All times in PST

### 21:10:57 ###
The proxy pod is evicted, due to [a known issue](https://github.com/data-8/infrastructure/issues/6) that is currently being worked on. Users start running into issue now, with connection failures.

### 21:11:04 ###
New proxy pod is started by kubernetes, and starts accepting connections. However, the JupyterHub model currently has the proxy starting with no state about user routes, and so the users’ requests aren’t being routed to their notebook pods. This manifests as errors for users.

The hub process is supposed to poll the proxy every 300s, and repopulate  the route table when it notices it is empty. The hub does this at some point in the next 300s (we do not know when), and starts repopulating the route table. As routes get added for currently users, their notebook starts working again.

### 21:11:52 ###
The repopulate process starts running into issues - it is making far too many http requests (to the kubernetes and proxy APIs) that it starts running into client side limits on tornado http client (which is what we use to make these requests). This causes them to time out on the request queue. We were running into https://github.com/tornadoweb/tornado/issues/1400. Not all requests fail - for those that succeed, the students are able to access their notebooks.

The repopulate process takes a while to process, and errors for a lot of students who are left with notebook in inconsistent state - JupyterHub thinks their notebook is running but it isn’t, or vice versa. Lots of 500s for users.

### 21:14 ###
Reports of errors start reaching the Slack channel + Piazza.

The repopulate process keeps being retried, and notebooks for users slowly come back. Some users are ‘stuck’ in a bad state, however - their notebook isn’t running, but JupyterHub thinks it is (or vice versa).

### 21:34 ###

Most users are fine by now. For those still with problems, a forced delete from the admin interface + a start works, since this forces JupyterHub to really check if they’re there or not.

### 22:03 ###

Last reported user with 500 error is fixed, and datahub is fully operational again.

## Conclusion ##
This is almost a ‘perfect storm’ event. Three things colluded to make this outage happen:

1. The [inodes issue](https://github.com/data-8/infrastructure/issues/6), which causes containers to fail randomly
2. The fact that the proxy is a single point of failure with a longish recovery time in current JupyterHub architecture.
3. KubeSpawner’s current design is inefficient at very high user volumes, and its request timeouts & other performance characteristics had not been tuned (because we have not needed to before).

We have both long term (~1-2 months) architectural fixes as well as short term tuning in place for all three of these issues.

## Action items ##
### Upstream JupyterHub ###
1. Work on abstracting the proxy interface, so the proxy is no longer a single point of failure. [Issue](https://github.com/jupyterhub/jupyterhub/issues/848)

### Upstream KubeSpawner ###
1. Re-architect the spawner to make a much smaller number of HTTP requests. DataHub has become big enough that this is a problem. [Issue](https://github.com/jupyterhub/kubespawner/issues/28)
2. Tune the HTTP client kubespawner uses. This would be an interim solution until (1) gets fixed. [Issue](https://github.com/jupyterhub/kubespawner/issues/29)

### DataHub configuration ###
1. Set resource requests explicitly for hub and proxy, so they have less chance of getting evicted. [Issue](https://github.com/data-8/jupyterhub-k8s/issues/124)
2. Reduce the interval at which the hub checks to see if the proxy is running. [PR](https://github.com/data-8/jupyterhub-k8s/pull/123)
3. Speed up the fix for the [inodes issue](https://github.com/data-8/infrastructure/issues/6) which is what triggered this whole issue.

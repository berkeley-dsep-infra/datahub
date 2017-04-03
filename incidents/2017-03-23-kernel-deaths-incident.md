## Summary ##

A seemingly unrelated change caused user kernels to die on start (making notebook execution impossible) for newly started user servers from about Mar 22 19:30 to Mar 23 09:45. Most users didn't see any errors until start of class at about 9AM, since they were running servers that were previously started.

## Timeline ##

### March 22, around 19:30 ###
A deployment is performed, finally deploying https://github.com/data-8/jupyterhub-k8s/pull/146 to production. It seemed to work fine on -dev, and on prod as well. However, the testing regimen was only to see if a notebook server would show up - not if a kernel would spawn.

### Mar 23, 09:08  ###
Students report that their kernels keep dying. This is confirmed to be a problem for all newly launched notebooks, in both prod and dev.

### 09:16 ###

The last change to the repo (an update of the single-user image) is reverted, to check if that was causing the problem. This does not improve the situation. Debugging continues, but with no obvious angles of attack.

### 09:41 ###
After debugging produces no obvious culprits, the state of the entire infrastructure for prod is reverted to a known good state from a few days ago. This was done with:

```bash
./deploy.py prod data8 25abea764121953538713134e8a08e0291813834
```

`25abea764121953538713134e8a08e0291813834` is the commit hash of a known good commit from March 19. Our disciplined adherence to immutable & reproducible deployment paid off, and we were able to restore new servers to working order with this!

Students are now able to resume working after a server restart. A mass restart is also performed to aid this.

Dev is left in a broken state in an attempt to debug.

### 09:48  ###
A core Jupyter Notebook dev at BIDS attempts to debug the problem, since it seems to be with the notebook itself and not with JupyterHub.

### 11:08 ###
Core Jupyter Notebook dev confirms that this makes no sense.

### 14:55  ###
Attempts to isolate the bug start again, mostly by using `git bisect` to deploy different versions of our infrastructure to dev until we find what broke.

### 15:30 ###
https://github.com/data-8/jupyterhub-k8s/pull/146 is identified as the culprit. It continues to not make sense.

### 17:25 ###
A very involved and laborious revert of the offending part of the patch is done in https://github.com/jupyterhub/kubespawner/pull/37. Core Jupyter Notebook dev continues to confirm this makes no sense.

https://github.com/data-8/jupyterhub-k8s/pull/152 is also merged, and deployed shortly after verifiying that everything (including starting kernels & executing code) works fine on dev. Deployed to prod and everything is fine.

## Conclusion ##

Insufficient testing procedures caused a new kind of outage (kernel dying) that we had not seen before. However, since our infrastructure was immutable & reproducible, our outage really only lasted about 40 minutes (from start of lab when students were starting containers until the revert). Deeper debugging produced a fix, but attempts to understand why the fix works are ongoing.

**Update**: We have found and fixed the [underlying issue](https://github.com/ipython/ipykernel/pull/233)

## Action items ##

### Process ###

1. Document and formalize the testing process for post-deployment checks.
2. Set a short timeout (maybe ten minutes?) after which investigation temporarily stops and we revert our deployment to a known good state.

### Upstream KubeSpawner ###

1. Continue investigating https://github.com/jupyterhub/kubespawner/issues/31, which was the core issue that prompted the changes that eventually led to the outage.

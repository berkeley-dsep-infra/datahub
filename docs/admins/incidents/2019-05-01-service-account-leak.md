# Service Account key leak incident

## Summary

Service account keys that granted restricted access
to some of our cloud services were inadvertently leaked
on GitHub. Google immediately notified us in seconds,
and the credentials were revoked within the next few minutes.

## Impact

Deployments are paused until this was fixed.

## Timeline

### May 1 2019, 3:18 PM

A template + documentation for creating new hubs easily is
pushed to GitHub as a pull request. This inadvertantly
contained live credentials for pushing & pulling our
(already public) docker images, and for access to our kubernetes
clusters.

Google immediately notified us via email within seconds
that this might be a breach.

### 3:19 PM

Discussion and notification starts in slack about dealing with
the issue.

### 3:27 PM

Both keys are revoked so they are no longer valid credentials.

### 3:36 PM

All in-use resources are checked, and verified to not be
compromised by automated bots looking for leaked accounts.

### 3:40 PM

An email is sent out to all owners of the compromised project
(ucb-datahub-2018) giving an all-clear.

## Action items

1. Don't duplicate service key credentials across multiple
   hubs. [Issue](https://github.com/yuvipanda/hubploy/issues/18)

2. Switch to a different secret management strategy than
   what we have now. [Issue](https://github.com/berkeley-dsep-infra/datahub/issues/596)

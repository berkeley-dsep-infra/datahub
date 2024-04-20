---
name: "Core node incidents (Feb-Mar 2024)"
about: "Our core node pool and the proxies located there had a series of issues."
title: "[Incident] Core nodes being autoscaled, configurable HTTP proxy crashes"
labels: ["type: Hub Incident", "support"]
assignees: "@shaneknapp"
---

# Summary

Over the past couple of years, all of our production hubs have been having persistent issues with our core nodes having major load spikes during 'peak' usage and the impacted node (which hosts all of our hub and proxy pods -- not user pods) crashing. This would then impact every hub, causing all users to see 503 http errors until a new node finishing spinning up.  We also suspect that the 'white screen' issue some users see after logging in is related to this.

These outages would usually last anywhere from 45 to 90+ minutes.  The first chunk of time would be the core node getting wedged and eventually dying, and the last 15-20 minutes would be spent on the new node spinning up and services restarting.

Many of these incidents are tracked [here](https://github.com/berkeley-dsep-infra/datahub/issues/2791).

We have spent much time working to debug and track this, including with our friends at [2i2c](https://2i2c.org). After much deep-diving and debugging, we were able to narrow this down to a memory (socket?) leak in the [configurable http proxy](https://github.com/jupyterhub/configurable-http-proxy/issues/434).

After some back and forth w/the upstream maintainers, we received a [forked version](https://github.com/berkeley-dsep-infra/datahub/pull/5501) of the proxy to test.

During this testing, we triggered some user-facing downtime, as well as the proxy itself crashing and causing small outages. 

Another (unrelated) issue that impacted users was that [GKE](https://cloud.google.com/kubernetes-engine) was autoscaling our core pool (where the hub and proxy pods run) node to zero. Since it takes about 10-15m for a new node to spin up, all hubs were inaccessible until the new node was deployed.

User Impact:

<!-- 
Quick summary of the problem. Update this section as we learn more, answering:

- what user impact was
- how long it was
- what went wrong and how we fixed it.
-->

- On the afternoon of Feb 7th, I was testing the fork of the proxy + some revised timeouts on the Data 8 hub.  This caused the proxy to crash every ~20m over the course of a few hours.  I then reverted the fork and timeout changes.
- During the latter half of February, our core pool was being autoscaled from 1 to 0 nodes.  This caused multiple short outages.
- The proxy pods for Data 8 and Data 100 (our largest classes) crashed continually under load (~250+ simultaneous users), causing users to receive 500 HTTP errors until the pod automatically restarted.

## Hub information

- [Data 8](https://data8.datahub.berkeley.edu)
- [Data 100](https://data100.datahub.berkeley.edu)

## Timeline

### 2024-03-05 Data8 outage
between ~4pm and ~5:15pm, data8's configurable-http-proxy (chp) was oomkilled and caused many 503 errors to be issued to the users.  here's a rough timeline of what happened (culled from grafana, gcp logs and kernel logs on the core node):

### 15:12:00
~280 concurrent users

### 15:12:42
chp “uncaught exception: write EPIPE”

### 16:00:00
proxy ram 800Mi (steady)

### 16:05:00
~300 concurrent users

### ~16:05:00
spike on proxy — cpu 181%, mem 1.06Gi --> 1.86Gi

### 16:05:53
chp healthz readiness probe failure 

### 16:05:56
chp/javascript runs out of heap “Ineffective mark-compass near heap limit Allocation Failed”

### 16:05:57-58
chp restarts

### 16:05:57
node dmesg: “TCP: request_sock_TCP: Possible SYN flooding on port 8000. Sending cookies.  Check SNMP counters.”

### ~16:06:00
2.5K 503 errors

### ~16:06:00 - 16:16:00
many many chp routes added and deleted causing 503 errors for some users

### 16:16:00 - 16:49:00
everything back to normal

### 16:49:00
~300 users (slowly decreasing)

### ~16:49:00
spike on proxy — cpu 107%, mem 814Mi --> 2.45Gi

### 16:49:40
core node dmesg:  node invoked oom-killer: gfp_mask=0xcc0(GFP_KERNEL), order=0, oom_score_adj=999

### 16:50:25
chp restarts (no heap error)

### ~16:50:00
5.7K 503 errors

### 16:54:15 - 17:15:31
300 users (slowly descreasing), 3x chp “uncaught exception: write EPIPE”, intermittent 503 errors in spikes of 30, 60, 150, hub latency 2.5sec 

### 18:47:19 - 18:58:10
~120 users (constant), 3x chp “uncaught exception: write EPIPE”, intermittent 503 errors in spikes of 30, 60, hub latency 3sec

### ~19:00
things return to normal

# After-action report

## What went wrong

- Only being able to test things like the forked chp in prod is dangerous and has a huge potential impact on users.
- The configurable http proxy (chp) is written in javascript (nodejs), and under load (~250+ concurrent users) it leaks ports and eventually fills up the heap (~728M) and gets oomkilled.
- The CPU allocation on the core node was also spiking, potentially causing login latency across all hubs.
- Upon chp restart, it can take up to 10-15m for the routing table to be repopulated.  During this time most, if not all, users that were already connected to the hub will get 503 errors.  Any new logins during this time will not.

## Where we got lucky

- Since we bumped the RAM allocated to the core node from 8G to 32G instances like are isolated to whatever hub's chp begins failing, and does not impact all hubs.

## Action items

### Process/Policy improvements

1. Work with instructors to identify and immediately troubleshoot directly with users impacted by the white screen issue.
2. Spin up a dev hub and figure out how to use [hubtraf](https://github.com/yuvipanda/hubtraf) to simulate a large number of users doing work.

### Documentation improvements

None.

### Technical improvements

1. Continue to track the port leak issue [upstream](https://github.com/jupyterhub/configurable-http-proxy/issues/434).
2. Deploy a new core pool with the same RAM and more CPU (Jira DH-259).
3. Spin up a dev hub and figure out how to use [hubtraf](https://github.com/yuvipanda/hubtraf) to simulate a large number of users doing work.

# Actions

- [x] Incident has been dealt with or is over
- [x] Sections above are filled out
- [x] Incident title and after-action report is cleaned up
- [x] All actionable items above have linked GitHub Issues

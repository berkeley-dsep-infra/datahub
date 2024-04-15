---
name: "Core node incidents (Feb-Mar 2024)"
about: "Our core node pool and the proxies located there had a series of issues."
title: "[Incident] Core nodes being autoscaled, configurable HTTP proxy crashes"
labels: ["type: Hub Incident", "support"]
assignees: "@shaneknapp"
---

# Summary

Over the past couple of years, all of our production hubs have been having
persistent issues with our core nodes having major load spikes during 'peak'
usage and the impacted node (which hosts all of our hub and proxy pods -- not
user pods) crashing. This would then impact every hub, causing all users to 
see 503 http errors until a new node finishing spinning up.

These outages would usually last anywhere from 45 to 90+ minutes.  The first
chunk of time would be the core node getting wedged and eventually dying, and
the last 15-20 minutes would be spent on the new node spinning up and services
restarting.

Many of these incidents are tracked [here](https://github.com/berkeley-dsep-infra/datahub/issues/2791).

We have spent much time working to debug and track this, including with our
friends at [2i2c](https://2i2c.org). After much deep-diving and debugging,
we were able to narrow this down to a memory (socket?) leak in the 
[configurable http proxy](https://github.com/jupyterhub/configurable-http-proxy/issues/434).

After some back and forth w/the upstream maintainers, we received a
[forked version](https://github.com/berkeley-dsep-infra/datahub/pull/5501) of
the proxy to test.

During this testing, we triggered some user-facing downtime, as well as the 
proxy itself crashing and causing small outages. 

Another (unrelated) issue that impacted users was that [GKE](https://cloud.google.com/kubernetes-engine)
was autoscaling our core pool (where the hub and proxy pods run) node to zero.
Since it takes about 10-15m for a new node to spin up, all hubs were
inaccessible until the new node was deployed.

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

## Timeline (if relevant)

### {{ 2022-01-20 Between 02:00 and 02.30 PM }}
[PR 1](https://github.com/berkeley-dsep-infra/datahub/pull/3161) and [PR 2](https://github.com/berkeley-dsep-infra/datahub/pull/3164/commits/a3fc71d5a68b030cda91029b5dbb6c01c0eec8fe) were merged to prod. Notably, PR 1 had multiple commits related to creation of Stat 20 hub, Stat 259 hub etc..

### {{ 06:10 }}

Andrew Bray (Stat 20 instructor) raised a [github issue](https://github.com/berkeley-dsep-infra/datahub/issues/3166) around 5.45 AM PST. 

### {{ 07:45 }}

Yuvi quickly jumped in to make a fix to get the R hub working. However this fix resulted in breaking Stat 20 hub.

### {{ 07:53 }}

ISchool folks reported issues with using RStudio in Datahub

### {{ 08:45 }}

Yuvi fixed issue with Stat 20 and other hubs

### {{ 12:10 }}
GSIs from Data 100 and 140 reported "Unhandled error" in their hubs

### {{ 12:15 }}
GSIs for Data 140 hub reported that the error was fixed

### {{ 12:33 }}
GSIs Data 100 hub reported that the error was fixed

---

# After-action report

These sections should be filled out once we've resolved the incident and know what happened.
They should focus on the knowledge we've gained and any improvements we should take.

## What went wrong

- R, Stat 20, Datahub, ISchool, Data 100 and 140 hubs went down around 2.30 AM PST. However, the team was aware of these issues only when users reported errors at different time intervals (as listed above)
- Multiple commits went through a single PR. Dependency package's version upgrade broke the image build (Yuvi to fill in the required details)

Things that could have gone better. Ideally these should result in concrete
action items that have GitHub issues created for them and linked to under
Action items. 

## Where we got lucky

These are good things that happened to us but not because we had planned for them.

- Yuvi was awake at the time when issue was reported and was able to fix the issues immediately. 
- Classes using hubs were not completely affected due to this outage (Data 100 did not have assignments due till 1/21 and Stat 20 had few mins of outage during instruction)

## Action items

These are only sample subheadings. Every action item should have a GitHub issue
(even a small skeleton of one) attached to it, so these do not get forgotten. These issues don't have to be in `infrastructure/`, they can be in other repositories.

### Process/Policy improvements

1. {{[Develop manual testing process](https://github.com/berkeley-dsep-infra/datahub/issues/2953) whenever a PR gets merged to staging of the major hubs (till automated test suites are written)}} [link to github issue](https://github.com/berkeley-dsep-infra/datahub/issues/2953)]
2. Develop a policy around when to create a new hub and what type of changes get deployed to Datahub! 

### Documentation improvements

1. {{ Start writing after action reports for future outages }} [link to github issue]
2. {{ summary }} [link to github issue]

### Technical improvements

1. {{ Enabling logging mechanism across all hubs to track future outages }}
2. {{ Adapt 2I2C testing suite to develop automated test cases that check the sanity of the different services whenever a PR gets merged in staging}} [link to github issue]
3. {{ Investigate the reason why pager duty did not throw an alert for 5xx errors when the hubs went down. Fix the alerting mechanism so that they notify all kind of errors }} [link to github issue]
4. {{ Adding R Studio as part of Repo2Docker}} [link to github issue]

# Actions

- [ ] Incident has been dealt with or is over
- [ ] Sections above are filled out
- [ ] Incident title and after-action report is cleaned up
- [ ] All actionable items above have linked GitHub Issues
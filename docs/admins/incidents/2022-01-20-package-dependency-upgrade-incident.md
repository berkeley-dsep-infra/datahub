---
name: "\U0001F4DD Hub Incident"
about: "Report an incident on our running hub infrastructure."
title: "[Incident] {{ Hubs throwing 505 errors }}"
labels: ["type: Hub Incident", "support"]
assignees: ""
---

# Summary

[PR 1](https://github.com/berkeley-dsep-infra/datahub/pull/3161) and [PR 2](https://github.com/berkeley-dsep-infra/datahub/pull/3164/commits/a3fc71d5a68b030cda91029b5dbb6c01c0eec8fe) were merged to prod between 2 AM and 2.30 AM PST on 1/20. Difference due to the commits can be viewed [here](https://github.com/berkeley-dsep-infra/datahub/pull/3151/files#diff-72ab2727eb8dffad68933fd8e624ef3126cc0a107685c3f0e16fcee62fc77c76)

Due to these changes, image rebuild happened which broke multiple hubs which used that image including Datahub, ISchool, R, Data 100 and Data 140 hubs. 

One of the dependenices highlighted as part of the image build had an upgrade which resulted in R hub throwing 505 error and Data 100/140 hub throwing "Error starting Kernel". [Yuvi to fill in the right technical information]

User Impact:

<!-- 
Quick summary of the problem. Update this section as we learn more, answering:

- what user impact was
- how long it was
- what went wrong and how we fixed it.
-->

- R Hub was not accessible for about 6 hours. Issue affected 10+ Stat 20 GSIs planning for their first class of the semester (catering to the needs of 600+ students). Hub went down for few minutes during the instruction. 
- Prob 140 hub was not available till 12.15 AM PST
- Data 100 hub was not available till 12.33 AM. Thankfully, assignments were not due till friday (1/21)
- Few users in Ischool were affected as they could not access R Studio

## Hub information

- Hub URL: {{(https://r.datahub.berkeley.edu/)}} & most other hubs highlighted above

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
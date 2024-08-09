---
title: Calendar Node Pool Autoscaler
---

## Why scale node pools with Google Calendar?

The scheduler isn't perfect for us, especially when large classes have
assignments due and a hub is flooded with students. This "hack" was
introduced to improve cluster scaling prior to known events.

These 'placeholder' nodes are used to minimize the delay that occurs
when GCP creates new node pools during mass user logins. This common,
especially for larger classes.

## Structure

There is a Google Calendar calendar, [DataHub Scaling
Events](https://calendar.google.com/calendar/embed?src=c_s47m3m1nuj3s81187k3b2b5s5o%40group.calendar.google.com&ctz=America%2FLos_Angeles)
shared with all infrastructure staff. The event descriptions should
contain a YAML fragment, and are of the form `pool_name:
count`, where the name is the corresponding hub name
(data100, stat20) and the count is the number of extra nodes you want.
There can be several pools defined, one per line.

By default, we usually have one spare node ready to go, so if the count
in the calendar event is set to 0 or 1, there will be no change to the
cluster. If the value is set to >=2, additional hot spares will be
created. If a value is set more than once, the entry with the greater
value will be used.

You can determine how many placeholder nodes to have up based on how
many people you expect to log in at once. Some of the bigger courses may
require 2 or more placeholder nodes, but during "regular" hours, 1 is
usually sufficient.

The scaling mechanism is implemented as the
`node-placeholder-node-placeholder-scaler` deployment within
the `node-placeholder` namespace. The source code is within
<https://github.com/berkeley-dsep-infra/datahub/tree/staging/images/node-placeholder-scaler>.

## Calendar Autoscaler

The code for the calendar autoscaler is a python 3.11 script, located
here:
<https://github.com/berkeley-dsep-infra/datahub/tree/staging/images/node-placeholder-scaler/scaler>

### How the scaler works

There is a k8s pod running in the `node-placeholder`
namespace, which simply [runs python3 -m
scaler](https://github.com/berkeley-dsep-infra/datahub/blob/staging/images/node-placeholder-scaler/Dockerfile).
This script runs in an infinite loop, and every 60 seconds checks the
scaler config and calendar for entries. It then uses the highest value
provided as the number of placeholder replicas for any given hub. This
means that if there's a daily evening event to 'cool down' the number
of replicas for all hubs to 0, and a simultaneous event to set one or
more hubs to a higher number, the scaler will see this and keep however
many node placeholders specified up and ready to go.

After determining the number of replicas needed for each hub, the scaler
will create a k8s template and run `kubectl` in the pod.

### Updating the scaler config

The [scaler
config](https://github.com/berkeley-dsep-infra/datahub/blob/staging/node-placeholder/values.yaml)
sets the default number of node-placeholders that are running at any
given time. These values can be overridden by creating events in the
[DataHub Scaling
Events](https://calendar.google.com/calendar/embed?src=c_s47m3m1nuj3s81187k3b2b5s5o%40group.calendar.google.com&ctz=America%2FLos_Angeles)
calendar.

When classes are in session, these defaults are all typically set to
`1`, and during breaks (or when a hub is not expected to be
in use) they can be set to `0`.

After making changes to `values.yaml`, create a PR normally
and our CI will push the new config out to the node-placeholder pod.
There is no need to manually restart the node-placeholder pod as the
changes will be picked up
[automatically](https://github.com/berkeley-dsep-infra/datahub/blob/3fb2d9412cbf87e0583774c8a7dc6c12ef58e715/images/node-placeholder-scaler/scaler/scaler.py#L93).

### Working on, testing and deploying the calendar scaler

All file locations in this section will assume that you are in the
`datahub/images/node-placeholder-scaler/` directory.

It is strongly recommended that you create a new python 3.11 environment
before doing any dev work on the scaler. With `conda`, you
can run the following commands to create one:

``` bash
conda create -ny scalertest python=3.11
pip install -r requirements.txt
```

Any changes to the scaler code will require you to run
`chartpress` to redeploy the scaler to GCP.

Here is an example of how you can test any changes to
`scaler/calendar.py` locally in the python interpreter:

``` python
# these tests will use somes dates culled from the calendar with varying numbers of events.
import scaler.calendar
import datetime
import zoneinfo

tz = zoneinfo.ZoneInfo(key='America/Los_Angeles')
zero_events_noon_june = datetime.datetime(2023, 6, 14, 12, 0, 0, tzinfo=tz)
one_event_five_pm_april = datetime.datetime(2023, 4, 27, 17, 0, 0, tzinfo=tz)
three_events_eight_thirty_pm_march = datetime.datetime(2023, 3, 6, 20, 30, 0, tzinfo=tz)
calendar = scaler.calendar.get_calendar('https://calendar.google.com/calendar/ical/c_s47m3m1nuj3s81187k3b2b5s5o%40group.calendar.google.com/public/basic.ics')
zero_events = scaler.calendar.get_events(calendar, time=zero_events_noon_june)
one_event = scaler.calendar.get_events(calendar, time=one_event_five_pm_april)
three_events = scaler.calendar.get_events(calendar, time=three_events_eight_thirty_pm_march)

assert len(zero_events) == 0
assert len(one_event) == 1
assert len(three_events) == 3
```

`get_events` returns a list of ical
`ical.event.Event` class objects.

The method for testing `scaler/scaler.py` is similar to
above, but the only things you'll be able test locally are the
`make_deployment()` and `get_replica_counts()`
functions.

When you're ready, create a PR. The deployment workflow is as follows:

1.  Get all authed-up for `chartpress` by performing the
    steps listed
    [here](https://docs.datahub.berkeley.edu/en/latest/admins/howto/rebuild-hub-image.html#).
2.  Run `chartpress --push` from the root
    `datahub/` directory. If this succeeds, check your `git
    status` and add
    `datahub/node-placeholder/Chart.yaml` and
    `datahub/node-placeholder/values.yml` to your PR.
3.  Merge to `staging` and then `prod`.

### Changing python imports

The python requirements file is generated using
`requirements.in` and `pip-compile`. If you need
to change/add/update any packages, you'll need to do the following:

1.  Ensure you have the correct python environment activated (see
    above).
2.  Pip install `pip-tools`
3.  Edit `requirements.in` and save your changes.
4.  Execute `pip-compile requirements.in`, which will update
    the `requirements.txt`.
5.  Check your git status and diffs, and create a pull request if
    necessary.
6.  Get all authed-up for `chartpress` by performing the
    steps listed
    [here](https://docs.datahub.berkeley.edu/en/latest/admins/howto/rebuild-hub-image.html#).
7.  Run `chartpress --push` from the root
    `datahub/` directory. If this succeeds, check your `git
    status` and add
    `datahub/node-placeholder/Chart.yaml` and
    `datahub/node-placeholder/values.yml` to your PR.
8.  Merge to `staging` and then `prod`.

## Monitoring

You can monitor the scaling by watching for events:

``` bash
kubectl -n node-placeholder get events -w
```

And by tailing the logs of the pod with the scalar process:

``` bash
kubectl -n node-placeholder logs -l app.kubernetes.io/name=node-placeholder-scaler -f
```

For example if you set `epsilon: 2`, you might see in the
pod logs:

``` bash
2022-10-17 21:36:45,440 Found event Stat20/Epsilon test 2 2022-10-17 14:21 PDT to 15:00 PDT
2022-10-17 21:36:45,441 Overrides: {'epsilon': 2}
2022-10-17 21:36:46,475 Setting epsilon to have 2 replicas
```

.. _howto/calendar-scheduler:

===================================
Scale Node Pools in Google Calendar
===================================


Why scale node pools with Google Calendar?
==========================================

The scheduler isn't perfect for us, especially when large classes have assignments due and a hub is flooded with students. This "hack" was introduced to improve cluster scaling prior to known events.

Structure
=========
There is a Google Calendar calendar, `DataHub Scaling Events <https://calendar.google.com/calendar/embed?src=c_s47m3m1nuj3s81187k3b2b5s5o%40group.calendar.google.com&ctz=America%2FLos_Angeles>`_ shared with all infrastructure staff. The event descriptions should contain a YAML fragment, and are of the form `pool_name: count`, where the name is alpha, beta, gamma, etc. and the count is the number of extra nodes you want. There can be several pools defined, one per line.

By default, we usually have one spare node ready to go, so if the count in the calendar event is set to 0 or 1, there will be no change to the cluster. If the value is set to >=2, additional hot spares will be created. If a value is set more than once, the entry with the greater value will be used.

The scaling mechanism is implemented as the `node-placeholder-node-placeholder-scaler` deployment within the `node-placeholder` namespace. The source code is within https://github.com/berkeley-dsep-infra/datahub/tree/staging/images/node-placeholder-scaler.

Configuration and Deployment
============================
The docker image, calendar URL, and replicas are all set in https://github.com/berkeley-dsep-infra/datahub/blob/staging/node-placeholder/values.yaml. You can change values here and redeploy through CI as usual.

Monitoring
==========
You can monitor the scaling by watching for events:

   .. code:: bash
      kubectl -n node-placeholder get events -w

And by tailing the logs of the pod with the scalar process:

   .. code:: bash
      kubectl -n node-placeholder logs -l app.kubernetes.io/name=node-placeholder-scaler -f

For example if you set `epsilon: 2`, you might see in the pod logs:

   .. code:: bash
      2022-10-17 21:36:45,440 Found event Stat20/Epsilon test 2 2022-10-17 14:21 PDT to 15:00 PDT
      2022-10-17 21:36:45,441 Overrides: {'epsilon': 2}
      2022-10-17 21:36:46,475 Setting epsilon to have 2 replicas

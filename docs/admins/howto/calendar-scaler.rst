.. _howto/calendar-scheduler:

================-=-================
Scale Node Pools in Google Calendar
================-=-================


Why scale node pools with Google Calendar?
==========================================

The scheduler isn't perfect for us, especially when large classes have assignments due and a hub is flooded with students. This "hack" was introduced to improve cluster scaling prior to known events.

Structure
=========
There is a Google Calendar calendar, `DataHub Scaling Events <https://calendar.google.com/calendar/embed?src=c_s47m3m1nuj3s81187k3b2b5s5o%40group.calendar.google.com&ctz=America%2FLos_Angeles>` shared with all infrastructure staff. The event descriptions should contain YAML and are of the form `pool_name: count`, where the name is alpha, beta, gamma, etc. and the count is desired node pool count. If the count is set to 0, the minimum value in the GKE cluster will be used. If a value is set more than once, the maximum value will be used.

The scaling mechanism is implemented as the `node-placeholder-node-placeholder-scaler` deployment within the `node-placeholder` namespace. The source code is within https://github.com/berkeley-dsep-infra/datahub/tree/staging/images/node-placeholder-scaler.

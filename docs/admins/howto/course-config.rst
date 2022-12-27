.. _howto/course-config:

============================
Allocate per-class resources
============================

It is possible to allocate additional resources (such as memory or extra volumes) to user servers based on users' class enrollments. The hub must be configured to use the `CanvasOAuthenticator <https://github.com/berkeley-dsep-infra/canvasauthenticator>`_ which is our default. Hubs that use dummy, Google, Generic OAuth, or other authenticators are not configured to allocate additional resources in this way.


Implementation
==============
The authenticator reads users Canvas enrollments when they login, and then assigns them to JupyterHub groups based on those affiliations. Groups are named with the format "canvas::{canvas_id}::{canvas_role}", e.g. "canvas::123456::teacher" or "canvas::234567::student". Our custom kubespawner, which we define in `hub/values.yaml`, reads users' group memberships prior to spawning. It then overrides various KubeSpawner paramters based on configuration we define, using the canvas ID as the key. (see below)

Note that if a user is assigned to a new Canvas group (e.g. by the instructor manually, or by an automated Canvas/SIS system) while their server is already running, they will need to logout and then log back in in order for the authenticator to see the new affiliations. Restarting the user server is not sufficient.

The canvas ID is somewhat opaque to hub staff -- we cannot look it up ourselves nor predict what it would be based on the name of the course. There are a number of other Canvas course attributes we could have substituted for the ID, but all had various drawbacks. An SIS ID attribute uses a consistent format that is relatively easy to predict, however it is only exposed to instructor accounts on hub login. In testing, when the Canvas admin configured student accounts to be able to read the SIS ID, we discovered that other protected SIS attributes would have been visible to all members of the course in the Canvas UI. Various friendly name attributes (e.g. "Statistics 123, Spring '24") were inconsistent in structure or were modifiable by the instructor. So while the Canvas ID is not predictable or easily discoverable by hub staff, it is immutable and the instructor can find it in the URL for their course.

Defining course profiles
========================

#. Require course staff to request additional resources through a `github issue <https://github.com/berkeley-dsep-infra/datahub/issues/new/choose>_`.

#. Obtain the bCourses course ID from the github issue. This ID is found in the course's URL, e.g. `https://bcourses.berkeley.edu/courses/123456`. It should be a large integer.


#. Edit `deployments/{deployment}/config/common.yaml`.

#. Duplicate an existing stanza, or create a new one under `hub.custom.group_profiles` by inserting yaml of the form:

   .. code:: yaml

        hub:
          custom:
            group_profiles:
              123456: # Name of Class 100, Fall '22; requested in #98765
                mem_limit: 4096M
                mem_guarantee: 2048M
              234567: # Some other class 200, Spring '23; requested in #98776
                extraVolumeMounts:
                - mountPath: /home/rstudio/.ssh
                  name: home
                  subPath: _stat131a/_ssh
                  readOnly: true

   where `123456` and `234567` are example integers from the first step. Memory limits and extra volume mounts are specified as in the examples above.

#. Add a comment associating the profile identifier with a friendly name of the course. Also link to the github issue where the instructor requested the resources. This helps us to cull old configuration during maintenance windows.

#. Commit the change, then ask course staff to verify the increased allocation on staging. It is recommended that they simulate completing a notebook or run through the assignment which requires extra resources.

Housekeeping
============

Group profiles should be removed at the end of every term because course affiliations are not necessarily removed from each person's Canvas account. So even if a user's class was over, the hub would grant additional resources for as long as the config persisted in both Canvas and the hub.

.. _howto/course-config:

===========================
Configuring course profiles
===========================

We fetch per-course enrollment from the Student Information System
when we need to configure user servers based on course affiliations.
We periodically use this to set per-user resource limits, attach extra
volumes to user servers, and automatically add or remove admin roles.

This is implemented with a hub sidecar container which fetches
enrollment data and shares it with the hub. The sidecar container's
image is located in ``images/fetch-course-emails`` and the hub reads
these rosters in our custom KubeSpawner in ``hub/values.yaml``. The
rosters are saved into the files:

   .. code:: bash

      /srv/jupyterhub/profiles.d/{year}-{term}-{class_section_id}-students.txt
      /srv/jupyterhub/profiles.d/{year}-{term}-{class_section_id}-instructors.txt


========================
Defining course profiles
========================

We indicate which courses we're interested in by defining them as
profiles in a given deployment's hub configuration at
`jupyterhub.hub.extraConfigMap.profiles`. Courses are specified as
keys of the form {year}-{term}-{class_section_id} in the helm config.
For example:


   .. code:: yaml

        profiles:
          2019-summer-15798: {}
          2019-spring-25622:
            mem_limit: 4096M
            mem_guarantee: 2048M
          2019-fall-23970:
            extraVolumeMounts:
            - mountPath: /home/rstudio/.ssh
              name: home
              subPath: _stat131a/_ssh
              readOnly: true


See https://classes.berkeley.edu for class section IDs.

Specifying empty profiles is sufficient to ensure that any student
enrolled in a course cannot also be an admin. This is important if
an enrolled student is a member of the course staff of another course
on the same hub, and they've been given admin access.

Memory limits and extra volume mounts are specified as in the example
above.

===========
Cleaning Up
===========

Remember to remove a course profile after the course is over. This
prevents the sidecar container from fetching unnecessary enrollment
data. Two semesters is probably a sufficient amount of time to retain
the profiles in the event students want to revisit assignments or
instructors want to re-evaluate them. For example if a profile was
specified for 2019 Fall, consider removing it by 2020 Summer.

If a student is in a course with a specified profile, and they become
a member of course staff the next semester, the old course profile
will need to be removed to ensure the new GSI/UGSI has sufficient
admin access.

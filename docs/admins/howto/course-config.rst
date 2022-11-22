.. _howto/course-config:

============================
Allocate per-class resources
============================

datahub knows which bCourse courses that users are affiliated with, and can assign users extra resources if defined in the hub configuration. Currently the main datahub is the only deployment that is using the CanvasOAuthenticator so is the only one that can allocate extra resources. However, this will be changed for Spring '23.

Defining course profiles
========================

#. Obtain the bCourses course ID from course staff. This ID is found in the course's URL, e.g. https://bcourses.berkeley.edu/courses/{identifier}. It should be a large integer.

#. Edit datahub/config/common.yaml.

#. Find an existing stantax, or create a new one, for `hub.custom.canvas_courses` and insert yaml of the form:

   .. code:: yaml

        canvas_courses:
          {identifier}: # Name of Class 123, Fall '22
            mem_limit: 4096M
            mem_guarantee: 2048M
          {identifier}: # Some other class 234, Spring '23
            extraVolumeMounts:
            - mountPath: /home/rstudio/.ssh
              name: home
              subPath: _stat131a/_ssh
              readOnly: true

   where `{identifier}` is the integer from the first step. Memory
   limits and extra volume mounts are specified as in the examples
   above. It is recommended that you provide a comment indicating
   the name and term of the course so that they can be easily
   identified and removed after the course is over.

#. Commit the change, then ask course staff to verify the increased allocation on staging. It is recommended that they simulate completing a notebook or run through the assignment which requires extra resources.


Future
======

Currently the code that accomplishes this is in our CustomKubeSpawner, however we will migrate it to the CanvasOAuthenticator. The latter will put the user into a JupyterHub group for each course they are affiliated with. The spawner will then allocate resources based on which groups the user is a member of.

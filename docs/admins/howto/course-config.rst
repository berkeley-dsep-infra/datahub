.. _howto/course-config:

====================
Course Configuration
====================

Allocating Resources
====================
It is possible to alter administrative priviliges or resources allocations (such as memory or extra volumes) of user servers from within the deployment configuration. This is mostly useful for when resources need to be increased based on  users' class enrollments. The hub must be configured to use the `CanvasOAuthenticator <https://github.com/berkeley-dsep-infra/canvasauthenticator>`_ which is our default. Hubs that use dummy, Google, Generic OAuth, or other authenticators are not configured to allocate additional resources in this way.

Additionally, it is also possible to allocate resources based on the students membership of Canvas groups. This is useful if the instructor wants to dynamically grant additional resources without CI round-trips. Group management can be performed by the course staff directly from bCourses.

Implementation
==============
The authenticator reads users Canvas enrollments when they login, and then assigns them to JupyterHub groups based on those affiliations. Groups are named with the format "course::{canvas_id}::enrollment_type::{canvas_role}", e.g. "course::123456::enrollment_type::teacher" or "course::234567::enrollment_type::student". Our custom kubespawner, which we define in `hub/values.yaml`, reads users' group memberships prior to spawning. It then overrides various KubeSpawner paramters based on configuration we define, using the canvas ID as the key. (see below)

Note that if a user is assigned to a new Canvas group (e.g. by the instructor manually, or by an automated Canvas/SIS system) while their server is already running, they will need to logout and then log back in in order for the authenticator to see the new affiliations. Restarting the user server is not sufficient.

The canvas ID is somewhat opaque to infrastructure staff -- we cannot look it up ourselves nor predict what it would be based on the name of the course. This is why we must request it from the instructor.

There are a number of other Canvas course attributes we could have substituted for the ID, but all had various drawbacks. An SIS ID attribute uses a consistent format that is relatively easy to predict, however it is only exposed to instructor accounts on hub login. In testing, when the Canvas admin configured student accounts to be able to read the SIS ID, we discovered that other protected SIS attributes would have been visible to all members of the course in the Canvas UI. Various friendly name attributes (e.g. "Statistics 123, Spring '24") were inconsistent in structure or were modifiable by the instructor. So while the Canvas ID is not predictable or easily discoverable by hub staff, it is immutable and the instructor can find it in the URL for their course.

Assigning Scopes to Roles
=========================
When JupyterHub only had two roles, admin and user, we would grant admin rights to course staff. This enabled course staff to start, access, and stop user servers, but it wasn't scoped to just the students in their own course. It would give them access to the accounts of everyone on the hub. They even had access to stop the hub process itself. JupyterHub now lets us create our own roles and assign `scopes <https://jupyterhub.readthedocs.io/en/stable/rbac/scopes.html>_` to them. As a result, we can grant course staff the ability to do what they need for members of their own course, and nothing more.

Add the following configuration for course staff who need elevated access:

   .. code:: yaml

        jupyterhub:
          hub:
            loadRoles:
              # Data 123, Summer 2024, #9876
              course-staff-1234567:
                description: Enable course staff to view and access servers.
                # this role provides permissions to...
                scopes:
                  - admin-ui
                  - list:users!group=course::1234567
                  - admin:servers!group=course::1234567
                  - access:servers!group=course::1234567
                # this role will be assigned to...
                groups:
                  - course::1234567::enrollment_type::teacher
                  - course::1234567::enrollment_type::tas

This configuration is headed by a comment which describes the course and term and links to the github issue where the staff made the request. It defines a new role, `course-staff-1234567`, for a course with bCourse ID `1234567`. It assigns scopes for accessing and administering the servers for users in group `course::1234567`. Members of that group include all students and course staff. It also assigns scopes for viewing lists of users at /hub/admin. It assignes these scopes to members of the affiliated course staff groups.

This stanza is more verbose than inserting lists of users under `admin_users`, but it the privileges are more granular. We don't need to know who the individual course staff and they won't have more permissions than they need.

The configuration causes JupyterHub to update information in its `jupyterhub.sqlite` database file. When this configuraition is removed, the hub does not automatically flush out the roles and scopes from the database. So after the semester is over, it is advisable to remove this configuration and also to flush out the information in the database. There is no formal process for this, although we should develop one. We can delete the database, or we can manually remove entries from the sqlite file.

Defining group profiles
=======================

#. Require course staff to request additional resources through a `github issue <https://github.com/berkeley-dsep-infra/datahub/issues/new/choose>_`.

#. Obtain the bCourses course ID from the github issue. This ID is found in the course's URL, e.g. `https://bcourses.berkeley.edu/courses/123456`. It should be a large integer. If the instructor requested resources for a specific group within the course, obtain the group name.

#. Edit `deployments/{deployment}/config/common.yaml`.

#. Duplicate an existing stanza, or create a new one under `jupyterhub.custom.group_profiles` by inserting yaml of the form:

   .. code:: yaml

        jupyterhub:
          custom:
            group_profiles:

              # Example: increase memory for everyone affiliated with a course.
              # Name of Class 100, Fall '22; requested in #98765

              course::123456:
                mem_limit: 4096M
                mem_guarantee: 2048M


              # Example: grant admin rights to course staff.
              # Enrollment types returned by the Canvas API are `teacher`,
              # `student`, `ta`, `observer`, and `designer`.
              # https://canvas.instructure.com/doc/api/enrollments.html

              # Some other class 200, Spring '23; requested in #98776
              course::234567::enrollment_type::teacher:
                mem_limit: 2096M
                mem_guarantee: 2048M
              course::234567::enrollment_type::ta:
                mem_limit: 2096M
                mem_guarantee: 2048M


              # Example: a fully specified CanvasOAuthenticator group name.
              # This could be useful for temporary resource bumps where the
              # instructor could add people to groups in the bCourses UI. This
              # would benefit from the ability to read resource bumps from
              # jupyterhub's properties. (attributes in the ORM)

              # Name of Class 100, Fall '22; requested in #98770
              course::123456::group::lab4-bigdata:
                - mountPath: /home/rstudio/.ssh
                  name: home
                  subPath: _some_directory/_ssh
                  readOnly: true


   Our custom KubeSpawner knows to look for these values under `jupyterhub.custom <https://z2jh.jupyter.org/en/stable/resources/reference.html#custom>_`.

   `123456` and `234567` are bCourse course identifiers from the first step. Memory limits and extra volume mounts are specified as in the examples above.

#. Add a comment associating the profile identifier with a friendly name of the course. Also link to the github issue where the instructor requested the resources. This helps us to cull old configuration during maintenance windows.

#. Commit the change, then ask course staff to verify the increased allocation on staging. It is recommended that they simulate completing a notebook or run through the assignment which requires extra resources.

Defining user profiles
======================

It may be necessary to assign additional resources to specific users, if it is too difficult to assign them to a bCourses group.

#. Edit `deployments/{deployment}/config/common.yaml`.

#. Duplicate an existing stanza, or create a new one under `jupyterhub.custom.profiles` by inserting yaml of the form:

   .. code:: yaml

        jupyterhub:
          custom:
            profiles:

              # Example: increase memory for these specific users.
              special_people:
                # Requested in #87654. Remove after YYYY-MM-DD.
                mem_limit: 2048M
                mem_guarantee: 2048M
                users:
                  - user1
                  - user2

#. Add a comment which links to the github issue where the resources were requested. This helps us to cull old configuration during maintenance windows.

Housekeeping
============

Group profiles should be removed at the end of every term because course affiliations are not necessarily removed from each person's Canvas account. So even if a user's class ended, the hub will grant additional resources for as long as the config persisted in both Canvas and the hub.

User profiles should also be evaluated at the end of every term.

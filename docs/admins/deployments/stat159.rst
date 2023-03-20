
.. _deployments/stat159:

========
Stat 159
========


stat159.datahub.berkeley.edu is a course-specific hub for Stat 159 as taught by Fernando Perez. It tends to include a lot of applications so that students can shift their local development workflows to the cloud.

Image
=====

Notably the image contains support for RTC. As of March 2023, this requires:

  - altair==4.2.2
  - boken==2.4.3
  - dask==2023.1.1
  - jupyter_server==2.2.1
  - jupyterlab==3.6.1
  - jupyterlab_server==2.19.0
  - tornado==6.2.0
  - git+https://github.com/berkeley-dsep-infra/tmpystore.git@84765e1

Some of these are hard requirements and others were necessary to make conda happy.

Configuration
=============

Along with the dependencies, the singleuser server is modified to launch as

```
  singleuser:
    cmd:
      - jupyterhub-singleuser
      - --LabApp.collaborative=true
      # https://jupyterlab-realtime-collaboration.readthedocs.io/en/latest/configuration.html#configuration
      - --YDocExtension.ystore_class=tmpystore.TmpYStore
```

This:

1. Turns on collaboration.
2. Moves some sqlite storage from home directories to /tmp/.

In addition to RTC, the hub also has configuration to enable `shared accounts with impersonation <https://github.com/jupyterhub/jupyterhub/blob/main/docs/source/tutorial/collaboration-users.md>`_. There are a handful of fabricated user accounts, e.g. collab-shared-1, collab-shared-2, etc. not affiliated with any real person in bCourses. There are also corresponding JupyterHub groups, shared-1, shared-2, etc. The instructors add real students to the hub groups, and some roles and scopes logic in the hub configuration gives students access to launch jupyter servers for the collaborative user accounts. The logic is in config/common.yaml while the current group affiliations are kept private in secrets.

This configuration is to encourage use of RTC, and to prevent one student from having too much access to another student's home directory. The fabricated (essentially service) accounts have initally empty home directories and exist solely to provide workspaces for the group. There is currently no archive or restore procedure in mind for these shared accounts.

For now, groups are defined in either the hub configuration or in the administrative /hub/admin user interface. In order to enable group assignment in this manner, we must set `Authenticator.managed_groups` to False. Ordinarily groups are provided by CanvasAuthenticator where this setting is True.

Eventually instructors will be able to define groups in bCourses so that CanvasAuthenticator can remain in charge of managing groups. This will be important for the extremely large courses. It will also be beneficial in that resource allocation can be performed more easily through group affiliations and group properties.

Historical Information
======================
The image has been periodically shared with data100 for when Fernando has taught both. Going forward, it is probably best to keep them separate and optionally kept in sync. We don't want changes in one course to come as a surprise to the other.

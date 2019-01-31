.. _howto/admin:

=================
Add an admin user
=================

What can admin users do?
========================

JupyterHub has `admin users <https://jupyterhub.readthedocs.io/en/stable/getting-started/authenticators-users-basics.html#configure-admins-admin-users>`_
who have the following capabilities:

#. Access & modify **all** other users' home directories (where all their work is kept)
#. Mark other users as admin users
#. Start / Stop other users' servers

These are all powerful & disruptive capabilities, so be careful who gets admin access!


Adding / removing an admin user
===============================

#. Pick the :ref:`hub <hubs>` you want to make a user an admin of.
#. Find the :ref:`config directory <structure/config>` for the hub, and 
   open ``common.yaml`` in there.
#. Add / remove the admin user name from the list ``jupyterhub.auth.admin.users``.
   Make sure there is an explanatory comment nearby that lists *why* this user
   is an admin. This helps us remove admins when they no longer need admin
   access.
#. Follow the steps to make a deployment
   
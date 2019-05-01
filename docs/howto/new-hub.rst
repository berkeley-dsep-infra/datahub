.. _howto/new-hub:

================
Create a new Hub
================


Why create a new hub?
=====================

The major reasons for making a new hub are:

#. You wanna use a different kind of authenticator.
#. Some of your *students* are *admins* on another hub,
   so they can see other students' work there.
#. You are running in a different cloud, or using a different
   billing account.
#. Your environment is different enough and specialized enough
   that a different hub is a good idea.
#. You want a different URL (X.datahub.berkeley.edu vs just
   datahub.berkeley.edu)

If your reason is something else, it probably needs some justification :)


Setting up a new hub structure
==============================

There's a simple `cookiecutter <https://github.com/audreyr/cookiecutter>`_
we provide that sets up a blank hub that can be customized. 

#. Make sure you have the ``cookiecutter`` python package installed

#. In the ``deployments`` directory, run cookiecutter:


   .. code:: bash
    
      cookiecutter template/

#. Answer the questions it asks. Should be fairly basic. It should generate
   a directory with the name of the hub you provided with a skeleton configuration.

#. Fill in values for ``jupyterhub.hub.cookieSecret`` and ``jupyterhub.proxy.secretToken``
   on ``secrets/staging.yaml`` and ``secrets/prod.yaml`` files.

#. Commit the directory, and make a PR. Once tests pass, merge the PR to get a
   working staging hub! It should be accessible by an external IP address that you can
   find with ``kubectl --namespace=<hub-name>-staging get svc proxy-public``.

#. Make a :ref:`dns entry <howto/dns>` for the staging hub (<hub-name>-staging.datahub.berkeley.edu>)
   pointing to the public IP. Wait to make sure it resolves correctly.

#. Uncomment the values under ``jupyterhub.proxy.https`` under ``secrets/staging.yaml``
   to enable HTTPS. Run this through CI and make sure HTTPS is set up on the staging hub.

#. Set up authentication as needed. This should all most likely go under ``secrets/staging.yaml``.

#. You now need to log into the NFS server, and create a directory owned by ``1000:1000`` under
   ``/export/pool0/homes/_<hubname>``. This step doesn't apply if you are using managed NFS!

#. User logins should now work in the staging hub. Verify and validate to make sure things are
   working as they should.

#. Repeat the process to get the production hub up and running. Tada!
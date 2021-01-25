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

#. Generate & fill in secret values

   #. ``openssl rand -hex 32`` to generate values for ``jupyterhub.proxy.secretToken`` and ``jupyterhub.auth.state.cryptoKey``
   #. ``ssh-keygeni -f new-host-key`` to generate a private ssh host key. This will
       output a private host key in ``new-host-key``, which should be filled in at
       ``jupyterhub-ssh.hostKey``. Make sure to get the indent right!
#. Fill in a value for ``jupyterhub.proxy.secretToken``, ``jupyterhub.auth.state.cryptoKey`` on
   ``secrets/staging.yaml`` and ``secrets/prod.yaml`` files.

#. You need to log into the NFS server, and create a directory owned by ``1000:1000`` under
   ``/export/homedirs-other-2020-07-29/<hubname>``. The path *might* differ if your
   hub has special home directory storage needs. Consult admins if that's the case.

#. Commit the directory, and make a PR. Once tests pass, merge the PR to get a
   working staging hub! It should be accessible by an external IP address that you can
   find with ``kubectl --namespace=<hub-name>-staging get svc proxy-public``.

#. Make a :ref:`dns entry <howto/dns>` for the staging hub (<hub-name>-staging.datahub.berkeley.edu>)
   pointing to the public IP. Wait to make sure it resolves correctly.

#. Uncomment the values under ``jupyterhub.proxy.https`` under ``config/staging.yaml``
   to enable HTTPS. Run this through CI and make sure HTTPS is set up on the staging hub.

#. Set up authentication via `bcourses <https://bcourses.berkeley.edu>`_. We have two canvas oauth2 clients - one for prod and one for staging. You'll need to add the domain for your new hub to the authorized list for both these clients - please reach out to Jonathan Felder (or bcourseshelp@berkeley.edu if he is not available).


#. User logins should now work in the staging hub. Verify and validate to make sure things are
   working as they should.

#. Repeat the process to get the production hub up and running. Tada!

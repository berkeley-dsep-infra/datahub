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
   that a different hub is a good idea. By default, everyone uses the
   same image as datahub.berkeley.edu.
#. You want a different URL (X.datahub.berkeley.edu vs just
   datahub.berkeley.edu)

If your reason is something else, it probably needs some justification :)


Setting up a new hub structure
==============================

There's a simple `cookiecutter <https://github.com/audreyr/cookiecutter>`_
we provide that sets up a blank hub that can be customized. 

#. Make sure you have the following python packages installed: ``cookiecutter
   ruamel.yaml``

#. In the ``deployments`` directory, run cookiecutter:


   .. code:: bash
    
      cookiecutter template/

#. Answer the questions it asks. Should be fairly basic. It should generate
   a directory with the name of the hub you provided with a skeleton configuration.
   It'll also generate all the secrets necessary.

#. You need to log into the NFS server, and create a directory owned by
   ``1000:1000`` under ``/export/homedirs-other-2020-07-29/<hubname>``. The path
   *might* differ if your hub has special home directory storage needs. Consult
   admins if that's the case.

#. Set up authentication via `bcourses <https://bcourses.berkeley.edu>`_. We
   have two canvas OAuth2 clients setup in bcourses for us - one for all
   production hubs and one for all staging hubs. The secret keys for these are
   already in the generated secrets config. However, you need to add the new
   hubs to the authorized callback list maintained in bcourses.

   #. ``<hub-name>-staging.datahub.berkeley.edu/hub/oauth_callback`` added to
      the staging hub client (id 10720000000000471)
   #. ``staging.datahub.berkeley.edu/hub/oauth_callback`` added to the
      production hub client (id 10720000000000472)

   Please reach out to Jonathan Felder (or bcourseshelp@berkeley.edu if he is
   not available) to set this up.

#. Add an entry in ``.circleci/config.yml`` to deploy the hub via CI. It should
   be under the ``deploy`` job, and look something like this:

   .. code:: yaml

      - run:
          name: Deploy <hub-name>
          command: |
            hubploy deploy <hub-name> hub ${CIRCLE_BRANCH}

   There will be a bunch of other stanzas very similar to this one, helping you
   find it.

#. Copy service account credentials for container registry & kubernetes cluster to
   the new hub directory. This is gonna be the same cluster & image as datahub
   for now, so you can just directly copy those.

   .. code:: bash

      # From the root of the repo
      cp deployments/datahub/secrets/gke-key.json deployments/<hub-name>/secrets
      cp deployments/datahub/secrets/gcr-key.json deployments/<hub-name>/secrets

#. Commit the hub directory, and make a PR to the the ``staging`` branch in the
   GitHub repo. Once tests pass, merge the PR to get a working staging hub! It
   should be accessible by an external IP address that you can find with
   ``kubectl --namespace=<hub-name>-staging get svc proxy-public``. However,
   HTTPS and authentication would not work on the staging hub yet.

#. Make a :ref:`dns entry <howto/dns>` for the staging hub
   (``<hub-name>-staging.datahub.berkeley.edu>``) pointing to the public IP.
   Wait to make sure it resolves correctly, otherwise HTTPS requisition might
   not work.

#. Uncomment the values under ``jupyterhub.proxy.https`` under
   ``config/staging.yaml`` to enable HTTPS. Run this through CI and make sure
   HTTPS is set up on the staging hub.

#. User logins should now work in the staging hub. Verify and validate to make
   sure things are working as they should.

#. Make a PR from the ``staging`` branch to the ``prod`` branch. When this PR is
   merged, it'll deploy the production hub.  It should be accessible by an
   external IP address that you can find with
   ``kubectl --namespace=<hub-name>-prod get svc proxy-public``. However, HTTPS
   and authentication would not work for the production hub yet.

#. Make a :ref:`dns entry <howto/dns>` for the prod hub (``<hub-name>.datahub.berkeley.edu>``)
   pointing to the public IP. Wait to make sure it resolves correctly,
   otherwise HTTPS requisition might not work.

#. Everything should work now! Try logging in to production, and make sure
   everything works out ok.

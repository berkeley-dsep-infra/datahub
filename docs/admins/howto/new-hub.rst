.. _howto/new-hub:

================
Create a new Hub
================


Why create a new hub?
=====================

The major reasons for making a new hub are:

#. You want to use a different kind of authenticator.
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

#. Make sure you have the following python packages installed: ``cookiecutter``

#. In the ``deployments`` directory, run cookiecutter:

   .. code:: bash

      cookiecutter template/

#. Cookiecutter template prompts you to answer 3 questions which will be about the name of the project, 
   cluster name and your hub name. Enter "ucb-datahub-2018" for the project name, "fall-2019" for the 
   cluster name and whatever you want as your hubname. It should generate a directory with the name of 
   the hub you provided with a skeleton configuration. It'll also generate all the necessary secrets.

#. You need to log into the NFS server and provide directories with appropriate permissions for the hub. 
   This will allow users to store their files in home directories.    You can run the following command 
   in gcloud terminal to log in to the NFS server. 
	
	.. code:: bash
	``gcloud compute ssh nfs-server-01 --zone=us-central1-b`` 
	
	Or alternatively launch console.cloud.google.com ->  Select "ucb-datahub-2018" as the project name. 
	Click on the three horizontal bar icon at the top left corner
	Access "Compute Engine" -> "VM instances" -> and search for "nfs-server-01". 
	select "Open in browser window" option to access NFS server via GUI.
	
	Create ``staging`` and ``prod``  directories owned by ``1000:1000`` under
   ``/export/homedirs-other-2020-07-29/<hubname>``. The path *might* differ if
   your hub has special home directory storage needs. Consult admins if that's
   the case. Here is the command to create the directory with appropriate permissions,

   .. code:: bash

      install -d -o 1000 -g 1000 \
        /export/homedirs-other-2020-07-29/<hubname>/staging \
        /export/homedirs-other-2020-07-29/<hubname>/prod
		
	Check whether the directories have permissions similar to the below directories,
	
	 .. code:: bash
	 
	drwxr-xr-x 4 ubuntu ubuntu     45 Nov  3 20:33 a11y
	drwxr-xr-x 4 ubuntu ubuntu     33 Jan  4  2022 astro
	drwxr-xr-x 4 ubuntu ubuntu  16384 Aug 16 18:45 biology

#. Set up authentication via `bcourses <https://bcourses.berkeley.edu>`_.
   We have two canvas OAuth2 clients setup in bcourses for us - one for all
   production hubs and one for all staging hubs. The secret keys for these are
   already in the generated secrets config. However, you need to add the new
   hubs to the authorized callback list maintained in bcourses.

   #. ``<hub-name>-staging.datahub.berkeley.edu/hub/oauth_callback`` added to
      the staging hub client (id 10720000000000471)
   #. ``staging.datahub.berkeley.edu/hub/oauth_callback`` added to the
      production hub client (id 10720000000000472)

   Please reach out to Jonathan Felder (or bcourseshelp@berkeley.edu if he is
   not available) to set this up.

#. (Archived) Set up authentication via datahub. Generate secrets for the hub using the following command,
   
   .. code:: bash
	openssl rand -hex 32
   
   This generates an alphanumeric text which you need to update across the secrets file both in Datahub and 
   the project you created.
   
   Deployment-specific configuration    will be added through the cookiecutter configuration, 
   however you will need to edit staging.yaml and prod.yaml in both ``deployments/datahub/config``
   and ``deployments/datahub/secrets``, inserting stanzas for the new hub. You
   also need to insert to insert the same generated stanza in the secrets directory
   of the project that you created. Navigate to your project and check
   config/secrets directory whether the newly generated secrets are added.

#. Add an entry in ``.circleci/config.yml`` to deploy the hub via CI. It should
   be under the ``deploy`` job, and look something like this:

   .. code:: yaml

      - run:
          name: Deploy <hub-name>
          command: |
            hubploy deploy <hub-name> hub ${CIRCLE_BRANCH}
		
		- hubploy/build-image:
				  deployment: a11y
				  name: a11y image build
				  # Filters can only be per-job? wtf
				  filters:
					  branches:
						ignore:
						- staging
						- prod	  

   .. code:: yaml
	
		- hubploy/build-image:
          deployment: a11y
          name: a11y image build
          push: true
          filters:
              branches:
                only:
                - staging
				
	.. code:: yaml

		- a11y image build
	
	Review hubploy.yaml file inside your project directory and update the image 
	name to the latest image. Something like this,
	
	.. code:: yaml
	  
	  image_name: us-central1-docker.pkg.dev/ucb-datahub-2018/user-images/a11y-user-image

#. Commit the hub directory, and make a PR to the the ``staging`` branch in the
   GitHub repo. Once tests pass, merge the PR to get a working staging hub! It
   might take a few minutes for HTTPS to work, but after that you can log into
   it at https://<hub-name>-staging.datahub.berkeley.edu. Test it out and make
   sure things work as you think they should.

#. Make a PR from the ``staging`` branch to the ``prod`` branch. When this PR is
   merged, it'll deploy the production hub. It might take a few minutes for HTTPS
   to work, but after that you can log into it at
   https://<hub-name>.datahub.berkeley.edu. Test it out and make sure things
   work as you think they should.

#. You may want to customize the docker image for the hub based on your unique 
   requirements. Navigate to deployments/'Project Name'/image and review 
   environment.yml file and identify packages that you want to add from 
   the [conda repository](https://anaconda.org/).
   
#. All done.
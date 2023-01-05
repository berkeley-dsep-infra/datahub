
.. _howto/new-hub:

================
Create a new Hub
================


Why create a new hub?
=====================

The major reasons for making a new hub are:

#. A new course wants to join the Berkeley Datahub community!
#. Some of your *students* are *admins* on another hub,
   so they can see other students' work there.
#. You want to use a different kind of authenticator.
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

#. Cookiecutter template prompts you to answer 3 questions which will be about a) name of the project, 
   b) cluster name and c) your hub name. Enter ``ucb-datahub-2018`` for the project name, ``fall-2019`` for the 
   cluster name and whatever you want as your hubname. It should generate a directory with the name of 
   the hub you provided with a skeleton configuration. It'll also generate all the necessary secrets.

#. In the web console, click on the horizontal bar icon at the top left corner.
   #. Access "Filestore" -> "Instances" and click on "Create Instance".
   #. Name the instance ``<course>-YYYY-MM-DD``
   #. Instance Type is ``Basic``, Storage Type is ``HDD``.
   #. Set the region to ``us-central1`` and Zone to ``us-central1-b``.
   #. Set the VPC network to ``default``.
   #. Set the File share name to ``shares``.
   #. Click "Create" and wait for it to be deployed.
   #. Once it's deployed, select the instance and copy the "NFS mount point".
#. You now need to log into the NFS server and provide directories with appropriate permissions for the hub. 
   This will allow users to store their files in home directories. You can run the following command 
   in gcloud terminal to log in to the NFS server. 
	
	``gcloud compute ssh nfs-server-01 --zone=us-central1-b``
   
   #. Or alternatively, Launch console.cloud.google.com ->  Select "ucb-datahub-2018" as the project name. 
   #. Click on the three horizontal bar icon at the top left corner.
   #. Access "Compute Engine" -> "VM instances" -> and search for "nfs-server-01". 
   #. Select "Open in browser window" option to access NFS server via GUI.
   #. Back in the NFS server shell, mount the new share:

   .. code:: bash

      mkdir /export/<hubname>-filestore
      mount <filestore share IP>/shares /export/<hubname>-filestore

   #. Create ``staging`` and ``prod``  directories owned by ``1000:1000`` under
   ``/export/<hubname>-filestore/<hubname>``. The path *might* differ if
   your hub has special home directory storage needs. Consult admins if that's
   the case. Here is the command to create the directory with appropriate permissions:
   
   .. code:: bash

      install -d -o 1000 -g 1000 \
        /export/<hubname>-filestore/<hubname>/staging \
        /export/<hubname>-filestore/<hubname>/prod
		
   #. Check whether the directories have permissions similar to the below directories:

   .. code:: bash

         drwxr-xr-x 4 ubuntu ubuntu     45 Nov  3 20:33 a11y-filestore
	 drwxr-xr-x 4 ubuntu ubuntu     33 Jan  4  2022 astro-filestore
	 drwxr-xr-x 4 ubuntu ubuntu  16384 Aug 16 18:45 biology-filestore

   #. Now we need to set ``ROOT_SQUASH`` on the newly created mount. In the 
      ``datahub/deployments/<hubname>/config/filestore/`` directory is a file named 
      ``squash-flags.json``. You will use this file when running the following ``gcloud`` 
      command to apply the changes:

   ..code:: bash

     gcloud filestore instances update <filestore-instance-name> --zone=us-central1-b --flags-file=squash-flags.json

#. Set up authentication via `bcourses <https://bcourses.berkeley.edu>`_.
   We have two canvas OAuth2 clients setup in bcourses for us - one for all
   production hubs and one for all staging hubs. The configuration and secrets
   for these are provided by the cookiecutter template, however the new hubs
   need to be added to the authorized callback list maintained in bcourses.

   #. ``<hub-name>-staging.datahub.berkeley.edu/hub/oauth_callback`` added to
      the staging hub client (id 10720000000000594)
   #. ``staging.datahub.berkeley.edu/hub/oauth_callback`` added to the
      production hub client (id 10720000000000472)

    Please reach out to Jonathan Felder to set this up, or
    bcourseshelp@berkeley.edu if he is not available.

#. Add an entry in ``.circleci/config.yml`` to deploy the hub via CI. It should
   be under the ``deploy`` job, and look something like this:

   .. code:: yaml

      - run:
          name: Deploy <hub-name>
          command: |
            hubploy deploy <hub-name> hub ${CIRCLE_BRANCH}
		
   .. code:: yaml
  
     - hubploy/build-image:
         deployment: <hub-name>
         name: <hub-name> image build
         filters:
             branches:
               ignore:
               - staging
               - prod  

	
       - hubploy/build-image:
           deployment:  <hub-name>
           name:  <hub-name> image build
           push: true
           filters:
               branches:
                 only:
                  - staging
				

       -  <hub-name> image build
	
#. Review hubploy.yaml file inside your project directory and update the image name to the latest image. Something like this,
	
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
   the ``conda repository`` <https://anaconda.org/>. You can copy the image manifest
   files from another deployment. It is recommended to use a repo2docker-style image 
   build, without a Dockerfile, if possible. That format will probably serve as the '
   basis for self-service user-created images in the future.
   
#. All done.

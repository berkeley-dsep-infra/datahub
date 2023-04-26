
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

Prereqs
=======
Working installs of the following utilities:
  - `sops <https://github.com/mozilla/sops/releases>`_
  - `hubploy <https://pypi.org/project/hubploy/>`_
     - `hubploy docs <https://hubploy.readthedocs.io/en/latest/index.html>`_
     - ``pip install hubploy`` 
  - `gcloud <https://cloud.google.com/sdk/docs/install>`_
  - `kubectl <https://kubernetes.io/docs/tasks/tools/>`_
  - `cookiecutter <https://github.com/audreyr/cookiecutter>`_

Proper access to the following systems:
  - Google Cloud IAM:  owner
  - Write access to the `datahub repo <https://github.com/berkeley-dsep-infra/datahub>`_
  - CircleCI account linked to our org

Setting up a new hub
====================

Name the hub
------------
Choose the ``<hubname>`` (typically the course or department). This is permanent.

Determine deployment needs
--------------------------
Before creating a new hub, have a discussion with the instructor about the system requirements,
frequency of assignments and how much storage will be required for the course. Typically, there
are three general "types" of hub:  Heavy usage, general and small courses.

Small courses will usually have one or two assignments per semester, and may only have 20 or
fewer users.

General courses have up to ~500 users, but don't have large amount of data or require upgraded
compute resources.

Heavy usage courses can potentially have thousands of users, require upgraded node specs and/or
have Terabytes of data each semester.

Both general and heavy usage courses typically have weekly assignments.

Small courses (and some general usage courses) can use either or both of a shared node pool and
filestore to save money (Basic HDD filestore instances start at 1T).

This is also a good time to determine if there are any specific software packages/libraries that
need to be installed, as well as what language(s) the course will be using. This will determine
which image to use, and if we will need to add additional packages to the image build.

If you're going to use an existing node pool and/or filestore instance, you can skip either or both of
the following steps and pick back up at the ``cookiecutter``.

When creating a new hub, we also make sure to label the filestore and
GKE/node pool resouces with both ``hub`` and
``<nodepool|filestore>-deployment``.  99.999% of the time, the values for all
three of these labels will be ``<hubname>``.

Creating a new node pool
------------------------
Create the node pool:

.. code:: bash

   gcloud container node-pools create "user-<hubname>-<YYYY-MM-DD>"  \
     --labels=hub=<hubname>,nodepool-deployment=<hubname> \
     --node-labels hub.jupyter.org/pool-name=<hubname>-pool --machine-type "n2-highmem-8"  \
     --enable-autoscaling --min-nodes "0" --max-nodes "3" \
     --project "ucb-datahub-2018" --cluster "fall-2019" --region "us-central1" --node-locations "us-central1-b" \
     --node-taints hub.jupyter.org_dedicated=user:NoSchedule --tags hub-cluster \
     --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "200"  \
     --metadata disable-legacy-endpoints=true \
     --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
     --no-enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --max-pods-per-node "110"


Creating a new filestore instance
---------------------------------
Before you create a new filestore instance, be sure you know the capacity
required.  The smallest amount you can allocate is 1T, but larger hubs may
require more.  Confer with the admins and people instructing the course and
determine how much they think they will need.

We can easily scale capacity up, but not down.

From the command line, first fill in the instance name (``<hubname>-<YYYY-MM-DD>``)
and ``<capacity>``, and then execute the following command:
.. code:: bash

   gcloud filestore instances create <hubname>-<YYYY-MM-DD> \
     --zone "us-central1-b" --tier="BASIC_HDD" \
     --file-share=capacity=<capacity>,name=shares \
     --network=name=default,connect-mode=DIRECT_PEERING

Or, from the web console, click on the horizontal bar icon at the top left
corner.

#. Access "Filestore" -> "Instances" and click on "Create Instance".
#. Name the instance ``<hubname>-<YYYY-MM-DD>``
#. Instance Type is ``Basic``, Storage Type is ``HDD``.
#. Allocate capacity.
#. Set the region to ``us-central1`` and Zone to ``us-central1-b``.
#. Set the VPC network to ``default``.
#. Set the File share name to ``shares``.
#. Click "Create" and wait for it to be deployed.
#. Once it's deployed, select the instance and copy the "NFS mount point".

Your new (but empty) NFS filestore must be seeded with a pair of directories. We run a utility VM for
NFS filestore management; follow the steps below to connect to this utility VM, mount your new filestore,
and create & configure the required directories.

You can run the following command in gcloud terminal to log in to the NFS utility VM:

``gcloud compute ssh nfs-server-01 --zone=us-central1-b``
   
Alternatively, launch console.cloud.google.com ->  Select "ucb-datahub-2018" as the project name. 

#. Click on the three horizontal bar icon at the top left corner.
#. Access "Compute Engine" -> "VM instances" -> and search for "nfs-server-01". 
#. Select "Open in browser window" option to access NFS server via GUI.

Back in the NFS utility VM shell, mount the new share:

.. code:: bash

   mkdir /export/<hubname>-filestore
   mount <filestore share IP>/shares /export/<hubname>-filestore

Create ``staging`` and ``prod``  directories owned by ``1000:1000`` under
``/export/<hubname>-filestore/<hubname>``. The path *might* differ if
your hub has special home directory storage needs. Consult admins if that's
the case. Here is the command to create the directory with appropriate permissions:
   
.. code:: bash

   install -d -o 1000 -g 1000 \
     /export/<hubname>-filestore/<hubname>/staging \
     /export/<hubname>-filestore/<hubname>/prod
		
Check whether the directories have permissions similar to the below directories:

.. code:: bash

   drwxr-xr-x 4 ubuntu ubuntu     45 Nov  3 20:33 a11y-filestore
   drwxr-xr-x 4 ubuntu ubuntu     33 Jan  4  2022 astro-filestore
   drwxr-xr-x 4 ubuntu ubuntu  16384 Aug 16 18:45 biology-filestore

Create the hub deployment locally
---------------------------------
In the ``datahub/deployments`` directory, run ``cookiecutter``. This sets up the hub's configuration directory:

.. code:: bash

   cookiecutter template/

The cookiecutter template will prompt you to provide the following information:
 - ``<hub_name>``: Enter the chosen name of the hub.
 - ``<project_name>``: Default is ``ucb-datahub-2018``, do not change.
 - ``<cluster_name>``: Default is ``fall-2019``, do not change.
 - ``<pool_name>``: Name of the node pool (shared or individual) to deploy on.
 - ``hub_filestore_share``: Default is ``shares``, do not change.
 - ``hub_filestore_ip``: Enter the IP address of the filestore instance. This is available from the web console.
 - ``hub_filestore_capacity``: Enter the allocated storage capacity. This is available from the web console.

This will generate a directory with the name of the hub you provided with a skeleton configuration and all the necessary secrets.

If you have created a new filestore instance, you will now need to apply the ``ROOT_SQUASH`` settings.
Skip this step if you are using an existing/shared filestore.

.. code:: bash

   gcloud filestore instances update <filestore-instance-name> --zone=us-central1-b  \
          --update-labels=hub=<hubname>,filestore-deployment=<hubname> \
          --flags-file=<hubname>/config/filestore/squash-flags.json

Authentication
--------------
Set up authentication via `bcourses <https://bcourses.berkeley.edu>`_.
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

CircleCI
--------
The CircleCI configuration file ``.circleci/config.yml`` will need to include directives for building
and deploying your new hub at several phases of the CircleCI process.
Generally speaking, an adequate manual strategy for this is to pick the name of an existing hub,
find each occurrence of that name, and add analogous entries for your new hub alongside your example existing hub.
Please order new entries for your new hub in alphabetical order amongst the entries for existing hubs.

Here is a partial (but incomplete) sampling of some of the relevant sections of the CircleCI configuration file:

.. code:: yaml

   - run:
       name: Deploy <hubname>
         command: |
           hubploy deploy <hubname> hub ${CIRCLE_BRANCH}
		
.. code:: yaml
  
   - hubploy/build-image:
       deployment: <hubname>
       name: <hubname> image build
       filters:
         branches:
           ignore:
             - staging
             - prod  

	
     - hubploy/build-image:
         deployment:  <hubname>
         name:  <hubname> image build
         push: true
         filters:
           branches:
             only:
               - staging
				

       -  <hubname> image build
	
Review hubploy.yaml file inside your project directory and update the image name to the latest image. Something like this,
	
.. code:: yaml
	  
   image_name: us-central1-docker.pkg.dev/ucb-datahub-2018/user-images/a11y-user-image

Add hub to the github labeler workflow
--------------------------------------
The new hub will now need to be added to the github labeler workflow.

Edit the file ``.github/labeler.yml`` and add an entry for this hub (alphabetically) in the
``# add build-infra label to any .github or circleci changes`` block:

.. code:: yaml

   <hubname>:
     - "deployments/<hubname>/**"
   
Create placeholder node pool
----------------------------
Node pools have a configured minimum size, but our cluster has the ability to set aside additional placeholder nodes. These are nodes that get spun up in anticipation of the pool needing to suddenly grow in size, for example when large classes begin.

If you are deploying to a shared node pool, there is no need to perform this step.

Otherwise, you'll need to add the placeholder settings in ``node-placeholder/values.yaml``.

The node placeholder pod should have enough RAM allocated to it that it needs to be kicked out to get even a single user pod on the node - but not so big that it can't run on a node where other system pods are running! To do this, we'll find out how much memory is allocatable to pods on that node, then subtract the sum of all non-user pod memory requests and an additional 256Mi of "wiggle room".  This final number will be used to allocate RAM for the node placeholder.

#. Launch a server on https://<hubname>.datahub.berkeley.edu
#. Get the node name (it will look something like ``gke-fall-2019-user-datahub-2023-01-04-fc70ea5b-67zs``): ``kubectl get nodes | grep <hubname> | awk '{print$1}'``
#. Get the total amount of memory allocatable to pods on this node and convert to bytes: ``kubectl get node <nodename> -o jsonpath='{.status.allocatable.memory}'``
#. Get the total memory used by non-user pods/containers on this node. We explicitly ignore ``notebook`` and ``pause``. Convert to bytes and get the sum:

.. code:: bash
   
   kubectl get -A pod -l 'component!=user-placeholder' \
          --field-selector spec.nodeName=<nodename> \
          -o jsonpath='{range .items[*].spec.containers[*]}{.name}{"\t"}{.resources.requests.memory}{"\n"}{end}' \
          | egrep -v 'pause|notebook'

#. Subract the second number from the first, and then subtract another 277872640 bytes (256Mi) for "wiggle room".
#. Add an entry for the new placeholder node config in ``values.yaml``:

.. code:: yaml
   
   data102:
     nodeSelector:
       hub.jupyter.org/pool-name: data102-pool
     resources:
       requests:
         # Some value slightly lower than allocatable RAM on the node pool
         memory: 60929654784
     replicas: 1

For reference, here's example output from collecting and calculating the values for ``data102``:

.. code:: bash

          (gcpdev) ➜  ~ kubectl get nodes | grep data102 | awk '{print$1}'
          gke-fall-2019-user-data102-2023-01-05-e02d4850-t478
          (gcpdev) ➜  ~ kubectl get node gke-fall-2019-user-data102-2023-01-05-e02d4850-t478 -o jsonpath='{.status.allocatable.memory}' # convert to bytes
          60055600Ki%
          (gcpdev) ➜  ~ kubectl get -A pod -l 'component!=user-placeholder' \
          --field-selector spec.nodeName=gke-fall-2019-user-data102-2023-01-05-e02d4850-t478 \
          -o jsonpath='{range .items[*].spec.containers[*]}{.name}{"\t"}{.resources.requests.memory}{"\n"}{end}' \
          | egrep -v 'pause|notebook' # convert all values to bytes, sum them
          calico-node
          fluentbit       100Mi
          fluentbit-gke   100Mi
          gke-metrics-agent       60Mi
          ip-masq-agent   16Mi
          kube-proxy
          prometheus-node-exporter
          (gcpdev) ➜  ~ # subtract the sum of the second command's values from the first value, then subtract another 277872640 bytes for wiggle room
          (gcpdev) ➜  ~ # in this case:  (60055600Ki - (100Mi + 100Mi + 60Mi + 16Mi)) - 256Mi
          (gcpdev) ➜  ~ # (61496934400 - (104857600 + 104857600 + 16777216 + 62914560)) - 277872640 == 60929654784


Besides setting defaults, we can dynamically change the placeholder counts by either adding new, or editing existing, `calendar events <https://docs.datahub.berkeley.edu/en/latest/admins/howto/calendar-scaler.html>`_. This is useful for large courses which can have placeholder nodes set aside for predicatable periods of heavy ramp up.

Commit and deploy staging
-------------------------
Commit the hub directory, and make a PR to the the ``staging`` branch in the
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

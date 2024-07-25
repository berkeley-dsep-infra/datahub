.. _howto/new-packages:

================================
Creating a new single user image
================================

When deploying a new hub, or moving from a shared single user server image,
you might need to create a new image for users. We use 
`repo2docker <https://github.com/jupyterhub/repo2docker>`_ to do this.

There are two approaches to creating a repo2docker image:
1. Use a repo2docker-style image `template <https://github.com/berkeley-dsep-infra/datahub/tree/staging/deployments/data100/image>`_ (environment.yaml, etc)
2. Use a `Dockerfile <https://github.com/berkeley-dsep-infra/datahub/tree/staging/deployments/datahub/images/default>`_ (useful for larger/more complex images)

Generally, we prefer to use the former approach, unless we need to install
specific packages or utilities outside of python/apt as ``root``.  If that is 
the case, only a :file:`Dockerfile` format will work.

Of course, as always create a feature branch for your changes, and submit a
PR when done.

Find a hub to use as a template
===============================

Browse through our :file:`deployments/` directory to find a hub that is similar to
the one you are trying to create. This will give you a good starting point.

Create the :file:`image/` directory for your new hub
====================================================

Create a new directory under :file:`deployments/` with the name of your hub. This
directory will contain the files that will be used to create the image.

Then, copy the contents (and any subdirectories) of the source :file:`image/`
directory in to the new directory.

Modify :file:`hubploy.yaml` for the hub
=======================================

In the deployment's :file:`hubploy.yaml` file, add or modify the ``name``, ``path`` and
``base_image`` fields to configure the image build and where it's stored in the
Google Artifcat Registry.

``name`` should contain the path to the image in the Google Artifact Registry and the name of the image.
``path`` points to the directory containing the image configuration (typically :file::`image/`).
``base_image`` is the base Docker image to use for the image build.

For example, :file:`hubploy.yaml` for the data100 image looks like this:

.. code:: yaml

      images:
         images:
            - name: us-central1-docker.pkg.dev/ucb-datahub-2018/user-images/data100-user-image
               path: image/
               repo2docker:
                  base_image: docker.io/library/buildpack-deps:jammy
         registry:
            provider: gcloud
            gcloud:
               project: ucb-datahub-2018
               service_key: gcr-key.json

      cluster:
      provider: gcloud
      gcloud:
         project: ucb-datahub-2018
         service_key: gke-key.json
         cluster: spring-2024
         zone: us-central1

Modify the image configuration as necessary
===========================================

This step is straightforward: edit/modify/delete/add any files in the :file:`image/`
directory to configure the image as needed.

Update CI/CD configuration
==========================

Next, ensure that this image will be built and deployed by updating the
:file:`.circleci/config.yml` file in the root of the repository. Add new steps
under the ``jobs/deploy:``, ``workflows/test-build-images:`` and ``workflows/deploy:``
stanzas.

Submitting a pull request
=========================

Familiarize yourself with `pull requests <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests>`_ and `repo2docker <https://github.com/jupyter/repo2docker>`_ , and create a fork of the `datahub staging branch <https://github.com/berkeley-dsep-infra/datahub>`_.

#. Set up your git/dev environment by `following the instructions here <https://github.com/berkeley-dsep-infra/datahub/#setting-up-your-fork-and-clones>`_.
#. Create a new branch for this PR.
#. Test the changes locally using ``repo2docker``, then submit a PR to ``staging``.
	* To use ``repo2docker``, you have to point it at the correct image directory. For example, to build the data100 image, you would run ``repo2docker deployments/data100/image`` from the base datahub directory.
#. Commit and push your changes to your fork of the datahub repo, and create a new pull request at `<https://github.com/berkeley-dsep-infra/datahub/>`__.
#. Once the PR is merged to staging and the new image is built and pushed to Artifact Registry, you can test it out on :code:`<hub>-staging.datahub.berkeley.edu`.
#. Changes are only deployed to prod once the relevant CI job is completed. See `<https://circleci.com/gh/berkeley-dsep-infra/datahub>`__ to view CircleCI job statuses. 

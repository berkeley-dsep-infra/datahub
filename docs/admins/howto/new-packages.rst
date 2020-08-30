.. _howto/new-packages:

==================================
Testing and Upgrading New Packages
==================================

It is helpful to test package additions and upgrades for yourself before they
are installed for all users. You can make sure the change behaves as you think
it should, and does not break anything else. Once tested, request that the
change by installed for all users by by `creating a new issue in github
<https://github.com/berkeley-dsep-infra/datahub/issues>`_,contacting
cirriculum support staff, or creating a new pull request. Ultimately,
thouroughly testing changes locally and submitting a pull request will
result in the software being rolled out to everyone much faster.

Install a package in your notebook
==================================

When testing a notebook with new version of the package, add the following line
to a cell at the beginning of your notebook.

   .. code:: bash

      !pip install --upgrade packagename==version

You can then execute this cell every time you run the notebook. This will
ensure you have the version you think you have when running your code.

To avoid complicated errors, make sure you always specify a version. You
can find the latest version by searching on `pypi.org <https://pypi.org>`_.

Find current version of package
===============================

To find the current version of a particular installed package, you can
run the following in a notebook.

   .. code:: bash

      !pip list | grep <name-of-package>

This should show you the particular package you are interested in and its
current version.


Submitting a pull request
=========================

Familiarize yourself with `pull requests <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests>`_ and `repo2docker <https://github.com/jupyter/repo2docker>`_ , and create a fork of the `datahub staging branch <https://github.com/berkeley-dsep-infra/datahub>`_.

#. Find the correct :file:`environment.yml` file for your class. This should be under ``\deployments\class\image\``
#. In :file:`environment.yml`, packages listed under :code:`dependencies` are installed using :code:`conda`, while packages under :code:`pip` are installed using :code:`pip`. Any packages that need to be installed via :code:`apt` must be added to ``\deployments\class\image\Dockerfile``.
#. Add any packages necessary. :code:`Pip` will almost always have the latest version of a package, but :code:`conda` may only contain older versions.
	* Note that package versions for :code:`conda` are specified using :code:`=`, while in :code:`pip` they are specified using :code:`==`
#. Test the changes locally using :code:`repo2docker`, then submit a PR to ``staging``.
	* To use ``repo2docker``, you have to point it at the right Dockerfile for your class. For example, to test the data100 datahub, you would run ``repo2docker deployments/data100/image`` from the base datahub directory. 
#. Once the PR is pulled, test it out on :code:`class-staging.datahub.berkeley.edu`.
#. Finally, submit a pull request to merge from :code:`staging` into :code:`master`.
    * Double check what commits are pulled in. Creating this pull request will pull in all new commits to master.
    * If other commits are pulled into your pull request, ask the authors of those commits if they are okay with this.
    * The pull request title should be "Merge [List of commits] to prod". For example, the pr title might be "Merge #1136, #1278, #1277, #1280 to prod".
#. Changes are only deployed to datahub once the relevant Travis CI job is completed. See `<https://circleci.com/gh/berkeley-dsep-infra/datahub>`__ to view Travis CI job statuses. 

Tips for Upgrading Package
==========================
* Conda can take an extremely long time to resolve version dependency conflicts, if they are resolvable at all. When upgrading Python versions or a core package that is used by many other packages, such as `requests`, clean out or upgrade old packages to minimize the number of dependency conflicts.
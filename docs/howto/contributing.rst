.. _contributing:

========
Contributing
========

This repository has two important branches, ``staging`` and ``prod``. The branch ``prod`` is protected.

The branch ``staging`` corresponds to the staging hubs, e.g. ``staging.datahub.berkeley.edu``, while the branch corresponds to the production hubs, e.g. ``datahub.berkeley.edu``. 

**VERY IMPORTANT:** the only branch that should ever be merged into ``bekeley-dsep-infra/datahub:prod`` is ``berkeley-dsep-infra/datahub:staging``. No other branches from ``berkeley-dsep-infra/datahub``, not any branches (not even ``staging`` nor ``prod``) from any other repository should ever be merged into ``berkeley-dsep-infra/datahub:prod``. Only ``berkeley-dsep-infra/datahub:staging`` should ever be merged into ``berkeley-dsep-infra/datahub:prod``.

After a new commit is pushed to ``staging``, CircleCI tests run on it. If those tests pass, then the new hub images are deployed, and thus e.g. the backend for ``staging.datahub.berkeley.edu`` will change.

Very similarly, after a new commit is pushed to ``prod``, CircleCI tests run on it, and if those tests pass, then the new hub images are deployed, and thus e.g. the backend for ``datahub.berkeley.edu`` will change.

Contributing How-to
============

However, you will not push directly to this repository. Instead, you will do the following:

#. Create a fork of this repository, e.g. at ``https://github.com/new-contributor/datahub``.

#. Clone your fork locally so you can work on it.

   .. code-block:: bash
   
      git clone https://github.com/new-contributor/datahub.git
   
#. For ease of use, add the original ``berkeley-dsep-infra`` repository as an extra remote. (Again, you won't be able to push to this, but it will be helpful for pulling.)
   
   .. code-block:: bash
   
     git remote add origin berkeley https://github.com/berkeley-dsep-infra/datahub.git

#. Now, in the ``staging`` branch of the local version of your fork, add the changes you want to make.

   After doing that, commit those changes, and then push them to your fork on GitHub:

   .. code-block:: bash
   
     git push -u origin master

#. If you are confident those are the changes you want, next create a Pull Request to merge ``new-contributor/datahub:staging`` into ``berkeley-dsep-infra/datahub:staging``. 

#. After creating the pull request, wait for the CircleCI tests to run to completion.

#. If those CircleCI tests pass, then your changes might be good to go. However, first you will need to contact one of the maintainers to make sure everything is OK.

#. If the maintainer looks at the PR and says it is OK, then the PR of ``new-contributor/datahub:staging`` into ``berkeley-dsep-infra/datahub:staging`` may later be merged.

#. After the CircleCI tests run again and pass, you should be able to view the changes at the corresponding staging datahub. Log into that staging datahub to make sure that everything is behaving as you expect.

#. If the result of merging your changes into ``berkeley-dsep-infra/datahub:staging`` led to the desired behavior on the staging DataHub, great!

   If not, go back to the local version of your fork and keep iterating, repeating steps 4-9 as many times as necessary.

#. If everything seems to be working, then next create a PR of ``berkeley-dsep-infra/datahub:staging`` into ``berkeley-dsep-infra/datahub:prod``. Wait for the CircleCI tests to run.

#. If the CircleCI tests for the PR of ``berkeley-dsep-infra/datahub:staging`` into ``berkeley-dsep-infra/datahub:prod`` run and pass, then contact one of the maintainers to request that the PR be merged.

#. If the maintainer says that everything is OK, then the PR of ``berkeley-dsep-infra/datahub:staging`` into ``berkeley-dsep-infra/datahub:prod`` will be merged. If not, close the PR and repeat steps 4-12 as many times as necessary.

#. After the PR of ``berkeley-dsep-infra/datahub:staging`` into ``berkeley-dsep-infra/datahub:prod`` is merged, you can log in to the "real" datahub that students will use and see the new changes in work. Congratulations! 

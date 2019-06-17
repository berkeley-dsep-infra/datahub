.. _howto/new-packages:

==================================
Testing and Upgrading New Packages
==================================

It is helpful to test package additions and upgrades for yourself before they
are installed for all users. You can make sure the change behaves as you think
it should, and does not break anything else. Once tested, request that the
change by installed for all users by by `creating a new issue in github
<https://github.com/berkeley-dsep-infra/datahub/issues>`_ or by contacting
cirriculum support staff. Ultimately the software will be rolled out to
everyone much faster.

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

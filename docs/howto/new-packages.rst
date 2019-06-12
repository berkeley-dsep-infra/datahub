.. _howto/new-packages:

==========================
Test new package additions
==========================

Before adding or upgrading a new library for all users, it is helpful to test it
just for yourself. You can make sure it behaves as you think it should and does
not break anything else. This speeds up the process of rolling it out to
everyone much faster.

Install a package in your notebook
==================================

When testing a notebook with new version of the package, add the following line
to a cell at the beginning of your notebook.

```
!pip install --upgrade packagename==version
```

You can then execute this cell every time you run the notebook. This will
ensure you have the version you think you have when running your code. 

To avoid complicated errors, make sure you always specify a version. You
can find the latest version by searching on `pypi.org <https://pypi.org>`_.

Find current version of package
===============================

To find the current version of a particular installed package, you can
run the following in a notebook.

```
!pip list | grep <name-of-package>
```

This should show you the particular package you are interested in and its
current version.
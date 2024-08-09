---
title: Testing and Upgrading New Packages
---

It is helpful to test package additions and upgrades for yourself before
they are installed for all users. You can make sure the change behaves
as you think it should, and does not break anything else. Once tested,
request that the change by installed for all users by by [creating a new
issue in
github](https://github.com/berkeley-dsep-infra/datahub/issues),contacting
cirriculum support staff, or creating a new pull request. Ultimately,
thouroughly testing changes locally and submitting a pull request will
result in the software being rolled out to everyone much faster.

Install a python package in your notebook
==================================

When testing a notebook with new version of the package, add the
following line to a cell at the beginning of your notebook.

``` bash
!pip install --upgrade packagename==version
```

You can then execute this cell every time you run the notebook. This
will ensure you have the version you think you have when running your
code.

To avoid complicated errors, make sure you always specify a version. You
can find the latest version by searching on
[pypi.org](https://pypi.org).

Find current version of a python package ===============================

To find the current version of a particular installed package, you can
run the following in a notebook.

``` bash
!pip list | grep <name-of-package>
```

This should show you the particular package you are interested in and
its current version.

Install/Update a R package in your RStudio
==================================

When the required version of package is missing in the R Studio, Try the
following command to check whether the default installation repo
contains the package (and the version) required.

``` R
install.packages("packagename")
```

This should install the particular package you are interested in and its
latest version. You can find the latest version of a R package by
searching on [CRAN](https://cran.r-project.org/).

Find current version of a R package ===============================

To find the current version of a particular installed package, you can
run the following in RStudio.

``` R
packageVersion("<name-of-package>") 
```

This should show you the particular package you are interested in and
its current version.

## Submitting a pull request

Familiarize yourself with [pull
requests](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)
and [repo2docker](https://github.com/jupyter/repo2docker) , and create a
fork of the [datahub staging
branch](https://github.com/berkeley-dsep-infra/datahub).

1.  Set up your git/dev environment by [following the instructions
    here](https://github.com/berkeley-dsep-infra/datahub/#setting-up-your-fork-and-clones).

2.  Create a new branch for this PR.

3.  Find the correct `environment.yml`{.interpreted-text role="file"}
    file for your class. This should be under
    `datahub/deployments/<class or hub name>/image`

4.  In `environment.yml`{.interpreted-text role="file"}, packages listed
    under `dependencies` are installed using `conda`, while packages
    under `pip` are installed using `pip`. Any packages that need to be
    installed via `apt` must be added to either
    `datahub/deployments/<class or hub name>/image/apt.txt` or
    `datahub/deployments/<class or hub name>/image/Dockerfile`.

5.  Add any packages necessary. We typically prefer using `conda` packages, and `pip` only if necessary. Please pin to a specific version (no wildards, etc).

    - Note that package versions for `conda` are specified using
      `=`, while in `pip` they are specified using `==`

6.  Test the changes locally using `repo2docker`, then submit a PR to `staging`.

    -   To use `repo2docker`, you have to point it at the right
        Dockerfile for your class. For example, to test the data100
        datahub, you would run `repo2docker deployments/data100/image` from the
        base datahub directory.

7.  Commit and push your changes to your fork of the datahub repo, and
    create a new pull request at
    <https://github.com/berkeley-dsep-infra/datahub/>.

8.  Once the PR is merged to staging, you can test it out on
    `class-staging.datahub.berkeley.edu`.

9.  Changes are only deployed to datahub once the relevant Travis CI job
    is completed. See
    <https://circleci.com/gh/berkeley-dsep-infra/datahub> to view Travis
    CI job statuses.

## Tips for Upgrading Package

-   Conda can take an extremely long time to resolve version dependency
    conflicts, if they are resolvable at all. When upgrading Python
    versions or a core package that is used by many other packages, such
    as [requests]{.title-ref}, clean out or upgrade old packages to
    minimize the number of dependency conflicts.

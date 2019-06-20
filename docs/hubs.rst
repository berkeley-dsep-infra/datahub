.. _hubs:

==============================
JupyterHubs in this repository
==============================

.. _hubs/datahub:

DataHub
=======

`datahub.berkeley.edu <https://datahub.berkeley.edu>`_ is the 'main' JupyterHub
for use on UC Berkeley campus. It's the largest and most active hub. It has many
Python & R packages installed.

It runs on `Google Cloud Platform <https://cloud.google.com>`_ in the ``ucb-datahub-2018``
project. You can see :ref:`all config <structure>` for it under ``deployments/datahub``.

Classes
-------

* The big `data8 <http://data8.org/>`_ class.
* Active `connector courses <https://data.berkeley.edu/education/connectors>`_
* `Data Science Modules <https://data.berkeley.edu/education/modules>`_
* `Astro 128/256 <https://astro.berkeley.edu/course-information/3958209-astronomy-data-science-laboratory>`_

This hub is also the 'default' when folks wanna use a hub for a short period of time for
any reason without super specific requirements.

Prob140 Hub
===========

A hub specifically for `prob140 <http://prob140.org/>`_. Some of the admin users
on :ref:`hubs/datahub` are students in prob140 - this would allow them to see
the work of other prob140 students. Hence, this hub is separate until JupyterHub
gains features around restricting admin use.

It runs on `Google Cloud Platform <https://cloud.google.com>`_ in the ``ucb-datahub-2018``
project. You can see :ref:`all config <structure>` for it under ``deployments/prob140``.

bcourses Hub
============

A hub for use with UC Berkeley's `Canvas <https://www.canvaslms.com/>`_ system
(called `bcourses <http://bcourses.berkeley.edu>`_). Not explicitly used by any
class yet.

It runs on `Google Cloud Platform <https://cloud.google.com>`_ in the ``ucb-datahub-2018``
project. You can see :ref:`all config <structure>` for it under ``deployments/bcourses``.

Data8X Hub
==========

A hub for the `data8x course on EdX <https://www.edx.org/professional-certificate/berkeleyx-foundations-of-data-science>`_.
This hub is open to use by anyone in the world, using `LTI Authentication <https://github.com/jupyterhub/ltiauthenticator>`_
to provide login capability from inside EdX.

It runs on `Google Cloud Platform <https://cloud.google.com>`_ in the ``data8x-scratch``
project. You can see :ref:`all config <structure>` for it under ``deployments/data8x``.

External Hub
============

Hub used temporarily by other institutions that are experimenting with the UCB way of
doing data science. They receive support only on a best-effort basis.

Currently, SRM Amravati is the only institution on the hub, sponsored by Yuvi Panda &
Prof. Janaki Bakhle. IT runs in the ``data8x-scratch`` project too, since it is
technically external pedagogy.

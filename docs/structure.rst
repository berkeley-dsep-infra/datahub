.. _structure:

====================
Repository Structure
====================

Hub Configuration
=================

Each hub has a directory under ``deployments/`` where all configuration
for that particular hub is stored in a standard format. For example, all
the configuration for the primary hub used on campus (*datahub*) is stored
under ``deployments/datahub/``. 

User Image (``image/``)
-----------------------

The contents of the ``image/`` directory determine the environment provided
to the user. For example, it controls:

#. Versions of Python / R / Julia available
#. Libraries installed, and which versions of those are installed
#. Specific config for Jupyter Notebook or IPython

`repo2docker <https://repo2docker.readthedocs.io/en/latest/>`_ is used to
build the actual user image, so you can use any of the `supported config files
<https://repo2docker.readthedocs.io/en/latest/config_files.html>`_ to customize
the image as you wish.

Hub Config (``config/`` and ``secrets/``)
-----------------------------------------

All our JupyterHubs are based on `Zero to JupyterHub (z2jh) <http://z2jh.jupyter.org/>`_.
z2jh uses configuration files in `YAML <https://en.wikipedia.org/wiki/YAML>`_ format
to specify exactly how the hub is configured. For example, it controls:

#. RAM available per user
#. Admin user lists
#. User storage information
#. Per-class & Per-user RAM overrides (when classes or individuals need more RAM)
#. Authentication secret keys

These files are split between files that are visible to everyone (``config/``) and
files that are visible only to a select few illuminati (``secrets/``). To get access
to the secret files, please consult the illuminati.

Files are further split into:

#. ``common.yaml`` - Configuration common to staging and production instances of this
   hub. Most config should be here.
#. ``staging.yaml`` - Configuration specific to the staging instance of the hub.
#. ``prod.yaml`` - Configuration specific to the production instance of the hub.

``hubploy.yaml``
----------------

We use `hubploy <https://github.com/yuvipanda/hubploy>`_ to deploy our hubs in a
repeatable fashion. ``hubploy.yaml`` contains information required for hubploy to
work - such as cluster name, region, provider, etc.

Various secret keys used to authenticate to cloud providers are kept under ``secrets/``
and referred to from ``hubploy.yaml``.

Documentation
=============

Documentation is under the ``docs/`` folder, and is generated with the `sphinx
<http://www.sphinx-doc.org/>`_ project. It is written with the `reStructuredText (rst)
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
format. Documentation is automatically published to https://ucb-jupyterhubs.readthedocs.io/.
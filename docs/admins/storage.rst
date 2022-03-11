.. _topic/storage:

===========================
User home directory storage
===========================

All users on all the hubs get a home directory with persistent storage.

Why NFS?
========

NFS isn't a particularly cloud-native technology. It isn't highly available
nor fault tolerant by default, and is a single point of failure. However,
it is currently the best of the alternatives available for user home directories,
and so we use it.

#. Home directories need to be fully POSIX compliant file systems that work
   with minimal edge cases, since this is what most instructional code assumes.
   This rules out object-store backed filesystems such as `s3fs <https://github.com/s3fs-fuse/s3fs-fuse>`_.

#. Users don't usually need guaranteed space or IOPS, so providing them each
   a `persistent cloud disk <https://cloud.google.com/persistent-disk/>`_ gets
   unnecessarily expensive - since we are paying for it wether it is used or
   not.

   When we did use one persistent disk per user, the storage cost
   dwarfed everything else by an order of magnitude for no apparent benefit.

   Attaching cloud disks to user pods also takes on average about 30s on
   Google Cloud, and much longer on Azure. NFS mounts pretty quickly, getting
   this down to a second or less.

We'll probably be on some form of NFS for the foreseeable future.

NFS Server
==========

We currently have two approaches to running NFS Servers.

#. Run a hand-maintained NFS Server with `ZFS <https://en.wikipedia.org/wiki/ZFS>`_
   SSD disks.

   This gives us control over performance, size and most importantly, server options.
   We use ``anonuid=1000``, so all reads / writes from the cluster are treated as if
   they have uid ``1000``, which is the uid all user processes run as. This prevents
   us from having to muck about permissions & chowns - particularly since Kubernetes
   creates new directories on volumes as root with strict permissions (see
   `issue <https://github.com/kubernetes/kubernetes/issues/2630>`_).

#. Use a hosted NFS service like `Google Cloud Filestore <https://cloud.google.com/filestore/>`_.

   We do not have to perform any maintenance if we use this - but we have no control
   over the host machine either. This necessitates some extra work to deal with the
   permission issues - see ``jupyterhub.singleuser.initContainers`` in the ``common.yaml``
   of a hub that uses this method.

Right now, every hub except ``data8x`` is using the first approach - primarily because
Google Cloud Filestore was not available when they were first set up. ``data8x`` is
using the second approach, and if proven reliable we will switch everything to it
the next semester.

Home directory paths
====================

Each user on each hub gets their own directory on the server that gets treated
as their home directory. The staging & prod servers share home directory paths, so
users get the same home directories on both.

For most hubs, the user's home directory path relative to the exported NFS directory
is ``<hub-name>/home/<user-name>``. Prefixing the path with the name of the hub
allows us to use the same NFS share for many number of hubs.

NFS Client
==========

We use the `Kubernetes NFS Volume <https://kubernetes.io/docs/concepts/storage/volumes/#nfs>`_
provider to mount user home directories.

We also try to mount everything as ``soft``, since we would rather have a write
fail than have processes go into uninterruptible sleep mode (D) where they
can not usually be killed when NFS server runs into issues.
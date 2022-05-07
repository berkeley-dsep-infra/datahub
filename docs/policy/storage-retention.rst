.. _topic/storage-retention:

========================
Storage Retention Policy
========================

Policy
======

Criteria
--------

No non-hidden files in the user's home directory that have been modified in the last 6 months.
The archival process will not happen for users who store more than 100 GB worth of data in any of our hubs. 

Archival
--------

1. Zip the whole home directory
2. Upload it to Google drive of a
   `SPA <https://calnetweb.berkeley.edu/calnet-departments/special-purpose-accounts-spa>`_
   created for this purpose
3. Share the ZIP file in the Google Drive with the user.

Rationale
=========
Most of our users in per course hubs who used datahub in previous semesters, have not logged in
for a long time, and will probably never log in again. This costs us
a lot of money in disk space - we will have to forever expand disk space.

By cleaning it up after 6 months of non-usage, we will not affect any
current users - just folks who haven't logged in for a long time. Archiving
the contents would make sure people still have access to their old work,
without leaving the burden of maintaining it forever on us.

Yesterday (5 May 2022) - We found many scenarios where users stored more than 100 GB worth of data (approximated to be around ~2 TB) 
which includes datasets in the home directories of their hubs. Most of these users did not log into their instances of the hub for the past 6 - 12 months. 
It seems reasonable to not archive their storage data considering that their a) storage amount is large in comparision with their peers
 and b) they have not been actively using this storage during the past 6 months.
By following this practice, we will ensure that we are not spending unnecessarily on cloud storage costs. 
Once identified, Users should get informed to back up their data in the next 30 days.
Post which either the data gets deleted from their home directories or is not archived for future retrieval.

Why Google Drive?
=================

We can also perform access control easily with Google Drive.

Alternatives
============

#. Email it to our users. This will most likely be rejected by most
   mail servers as the home directory will be too big an attachment

#. Put it in `Google Cloud Nearline storage <https://cloud.google.com/storage/archival/>`_,
   build a token based access control mechanism on top, and email this
   link to the users. We will need to probably clean this up every 18 months
   or so for cost reasons. This is the viable alternative, if we decide to
   not use Google Drive
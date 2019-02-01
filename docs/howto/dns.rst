.. _howto/dns:

==========
Update DNS
=================

Some staff have access to make and update DNS entries in the .datahub.berkeley.edu and .data8x.berkeley.edu subdomains.


Authorization
=============

Request access to make changes by creating an issue in this repository.

Authorization is given through membership in the edu:berkeley:org:nos:DDI:datahub CalGroup. @yuvipanda and @ryanlovett are group admins and can update membership.

Making Changes
==============

#. Log into https://infoblox.berkeley.edu from a campus network or through the `campus VPN <https://software.berkeley.edu/cisco-vpn>`. Use your CalNet credentials.
#. Navigate to Data Management > DNS > Zones and click ``berkeley.edu``.
#. Navigate to Subzones and choose data8x or datahub, then click ``Records``.

.. tip:: For quicker access, click the star next to the zone name to make a bookmark in the ``Finder`` pane on the left side.

Create a new record
-------------------
#. Click the down arrow next to ``+ Add`` in the right-side Toolbar. Then choose Record > A Record.
#. Enter the name and IP of the A record, and uncheck ``Create associated PTR record``.
#. Consider adding a comment with a timestamp, your ID, and the nature of the change.
#. Click ``Save & Close``.

Edit an existing record
-----------------------
#. Click the gear icon to the left of the record's name and choose ``Edit``.
#. Make a change.
#. Consider adding a comment with a timestamp, your ID, and the nature of the change.
#. Click ``Save & Close``.

Delete a record
----------------
#. Click the gear icon to the left of the record's name and choose ``Delete``.

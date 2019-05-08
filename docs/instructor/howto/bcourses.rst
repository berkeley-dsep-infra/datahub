.. _instructor/howto/bcourses:

===========================
Using bcourses with DataHub
===========================

There's a trial hub running at ``bcourses.datahub.berkeley.edu`` that can
integrates with `bcourses <https://bcourses.berkeley.edu>`_. Currently,
the only primary feature available is the ability to launch into a
student's copy of a template notebook (or file, or terminal) from inside
an assignment in bcourses.

Setting up your course
======================

As an instructor or staff, you need to do a little one-time set up in
your course to be able to use the hub.

#. Open the *Setting* pane on the left.

   .. image:: images/bcourses/settings.png

#. In the top right, click the button that lets you *View App Configurations*

   .. image:: images/bcourses/app-configurations-button.png

#. Click the *Add App* button

   .. image:: images/bcourses/add-app-button.png

#. The *Add Application* dialog will open. Fill in the following information:

   #. **Name**: 'bCourses DataHub' (or any other descriptive name)
   #. **Consumer Key** and **Consumer Secret**: Unfortunately, you need to
      contact the system administrators to get these keys right now. Open
      an issue in `the github repo <https://github.com/berkeley-dsep-infra/datahub>`_
      to get these.
   #. **Launch URL**: ``https://bcourses.datahub.berkeley.edu/hub/lti/launch``
   #. **Privacy**: 'Public'. This lets the username on the hub match the
      username on canvas, which makes a bunch of things easier.
   #. **Description**: Any description that makes sense to you.

   Once filled in, press *Submit*.

   .. image:: images/bcourses/add-app-dialog.png

You can now use the bcourses hub in your course!

Creating an assignment
======================

The typical student workflow when using JupyterHub is:

#. Student clicks a link in an assignment in bcourses
#. It automatically takes them to a copy of a live interactive
   Jupyter Notebook (or RStudio session) set up with your
   content.

First, we'll create an *nbgitpuller link* that points to
the content you want them to get when they click the link.

Create an nbgitpuller link
--------------------------

This section assumes you have a repository on `Github.com
<https://github.com>`_ with your notebooks.

#. Visit the `nbgitpuller link generator <https://jupyterhub.github.io/nbgitpuller/link>`_

#. Enter ``https://bcourses.datahub.berkeley.edu`` as *JupyterHub URL*.

#. The URL of your GitHub repository goes into *Git Repository URL*. You can
   use any other git provider URL here too (GitLab, BitBucket, etc)
   if you wish, but we recommend GitHub.com for most users.

#. If you have a specific notebook, directory or file you want your
   students to land in, specify that under *File to open*.

#. Select *Launch from Canvas* tab in the top right, and copy the URL
   produced by it. This is the URL we'll use from inside bcourses.


Creating the assignment
-----------------------

#. Go to the *Assignments* tab in your course

   .. image:: images/bcourses/assignments-tab.png

#. Click the *Add Assignment* button if you want to add
   a new assignment. Alternatively, you can also edit an
   existing assignment you already have.

   .. image:: images/bcourses/add-assignment-button.png

#. Add a title and description that explains what is expected
   of your students.

#. Under *Submission Type*, select *External Tool*.

   .. image:: images/bcourses/submission-type.png

#. Paste the *nbgitpuller URL* we made in the previous step
   under *Enter or find an External Tool URL*.

   .. image:: images/bcourses/submission-url.png

   Tick the *Load This Tool in a New Tab* checkbox too.

#. Now hit *Save* button. This will save the assignment so
   you can test it out, without making it visible to your
   students. 

   .. image:: images/bcourses/assignment-save-button.png

#. This will open a page where you can test your assignment.

   .. image:: images/bcourses/launch-notebook.png

   Press the button and make sure the link launches into the
   notebook you expect it to.

#. If everything is ok, you can go back to the previous page
   by clicking the *Edit Assignment Settings* button. 
   
   .. image:: images/bcourses/edit-assignment-settings.png

#. You can now press *Save and Publish* to make this assignment
   visible to your students immediately!
   
   .. image:: images/bcourses/save-and-publish.png
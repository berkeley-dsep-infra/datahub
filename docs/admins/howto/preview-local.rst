.. _howto/preview-local:

======================================
Preview documentation changes locally
======================================


Strategy 1: convert to html
======================================

#. Create a virtual environment (Recommendation is to create conda environment)
#. Navigate to `datahub/` directory and run 
 
   .. code:: bash

      pip install -r docs/requirements.txt 
   
#. Navigate to `docs/` directory. Run the following command,

   .. code:: bash

      make html
	 
#. Navigate to `docs/_build/html` directory and open index.html file in the browser.

#. Have fun making changes to the documentation based on the HTML preview.

Strategy 2: free online previewer
======================================

Use a free, online, in-line converter such as: https://www.tutorialspoint.com/online_restructure_editor.php

Strategy 3: Visual Studio code extension
========================================

The VSCode extension `RSTPreview
<https://marketplace.visualstudio.com/items?itemName=tht13.rst-vscode>`_ provides a live preview of
your reStructuredText file as you edit it within VSCode. You may have to check the extension’s settings
to set a non-conflicting keystroke sequence for opening the preview pane.
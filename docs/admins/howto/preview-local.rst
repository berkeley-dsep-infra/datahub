.. _howto/preview-local:

================
Preview documentation changes locally
================


Steps to preview locally as HTML files
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
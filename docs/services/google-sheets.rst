.. _services/google-sheets:

==================================
Reading Google Sheets from DataHub
==================================

Available in: DataHub

We provision and make available credentials for a
`service account <https://cloud.google.com/iam/docs/understanding-service-accounts>`_
that can be used to provide readonly access to Google Sheets. This is useful in
pedagogical situations where data is read from Google Sheets, particularly with
the `gspread <https://gspread.readthedocs.io/>`_ library.

The entire contents of the JSON formatted service account key is available as an
environment variable ``GOOGLE_SHEETS_READONLY_KEY``. You can use this to read
publicly available Google Sheet documents.

The service account has no implicit permissions, and can be found under 
``singleuser.extraEnv.GOOGLE_SHEETS_READONLY_KEY`` in ``datahub/secrets/staging.yaml`` and
``datahub/secrets/prod.yaml``.

``gspread`` sample code
=======================

The following sample code reads a sheet from a URL given to it, and prints
the contents.

.. code:: python

    import gspread
    import os
    import json
    from oauth2client.service_account import ServiceAccountCredentials

    # Authenticate to Google
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['GOOGLE_SHEETS_READONLY_KEY']), scope)
    gc = gspread.authorize(creds)

    # Pick URL of Google Sheet to open
    url = 'https://docs.google.com/spreadsheets/d/1SVRsQZWlzw9lV0MT3pWlha_VCVxWovqvu-7cb3feb4k/edit#gid=0'

    # Open the Google Sheet, and print contents of sheet 1
    sheet = gc.open_by_url(url)
    print(sheet.sheet1.get_all_records())


``gspread-pandas`` sample code
==============================

The `gspread-pandas <https://gspread-pandas.readthedocs.io/>`_ library helps get data from
Google Sheets into a `pandas <https://pandas.pydata.org/>`_ dataframe. 


.. code:: python

    from gspread_pandas.client import Spread
    import os
    import json
    from oauth2client.service_account import ServiceAccountCredentials

    # Authenticate to Google
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['GOOGLE_SHEETS_READONLY_KEY']), scope)

    # Pick URL of Google Sheet to open
    url = 'https://docs.google.com/spreadsheets/d/1SVRsQZWlzw9lV0MT3pWlha_VCVxWovqvu-7cb3feb4k/edit#gid=0'

    # Open the Google Sheet, and print contents of sheet 1 as a dataframe
    spread = Spread(creds, url)
    sheet_df = spread.sheet_to_df(sheet='sheet1')
    print(sheet_df)
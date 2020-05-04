:code:`whois_record` (API)
--------------------------

Give us the WHOIS record.

.. warning::
    You may get :code:`DATE EXTRACTED FROM WHOIS DATABASE` as response when it's
    coming from the JSON database.

    The reason behind this is that we don't want to grow the size of the JSON file.
:code:`links`
^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Set the list of links which can be used/called by the system when needed.

    .. note::
        The objective of this index is to avoid hardcoded links when the configuration file is readable.


:code:`links[api_date_format]`
""""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://pyfunceble.funilrys.com/api/date-format`

    **Description:** Set the link to use when we share logs.


:code:`links[api_no_referer]`
""""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://pyfunceble.funilrys.com/api/no-referer`

    **Description:** Set the link to use when we share logs.

:code:`links[config]`
"""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://raw.githubusercontent.com/funilrys/PyFunceble/master/.PyFunceble_production.yaml`

    **Description:** Set the upstream link to the configuration file.

:code:`links[dir_structure]`
""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://raw.githubusercontent.com/funilrys/PyFunceble/master/dir_structure_production.json`

    **Description:** Set the upstream link to the directory structure dump file.

:code:`links[iana]`
"""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json`

    **Description:** Set the upstream link to the IANA zone file configuration file.

:code:`links[psl]`
""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://raw.githubusercontent.com/funilrys/PyFunceble/master/public-suffix.json`

    **Description:** Set the upstream link to the public suffix database file.


:code:`links[repo]`
"""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://github.com/funilrys/PyFunceble`

    **Description:** Set the upstream link to the repository.

:code:`links[requirements]`
"""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`https://raw.githubusercontent.com/funilrys/PyFunceble/master/requirements.txt`

    **Description:** Set the upstream link to the :code:`requirements.txt` file.

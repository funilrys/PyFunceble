SPECIAL
^^^^^^^

As PyFunceble grows, I thought that a bit of filtering for special
cases would be great.

So I introduced the SPECIAL source.

For any new suggestion of domains where a special rule can enhance PyFunceble
please either open an new `issue`_ or make you
`contribution <../contributing/index.html#contribute>`_ directly into the git.

.. note::
    Please consider all 3 digits number that are listed in this section as
    the HTTP status code catches by
    :func:`PyFunceble.lookup.http_code.HTTPCode.get`.

.. note::
    If you do not want to use these rules? You can disable these flags to
    disable the feature.

    * `--special-lookup <../usage/index.html#special-lookup>`_ arguments from the
      CLI.
    * :code:`special: True` into your local configuration file.

.. note::
    **contribution to special rules**

    To add directly into the special rules please modify both the source code
    `extra_rules.py <https://github.com/funilrys/PyFunceble/blob/dev/PyFunceble/checker/availability/extra_rules.py>`_
    and the documentation
    `source.rst <https://github.com/funilrys/PyFunceble/blob/dev/docs/responses/source.rst>`_

:code:`*.000webhostapp.com`
"""""""""""""""""""""""""""

- All :code:`410` are returned as :code:`INACTIVE`.

::code:`angelfire.com`
""""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`.

:code:`*.blogspot.*`
""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`
- All :code:`301` which are blocked by Google or does not exist are returned
  as :code:`INACTIVE`
- All :code:`302` which are blocked by Google are returned as :code:`INACTIVE`

:code:`*.canalblog.com`
"""""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.github.io`
"""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.hpg.com.br`
""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.liveadvert.com`
""""""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.skyrock.com`
"""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.tumblr.com`
""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.wix.com`
"""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.wordpress.com`
"""""""""""""""""""""""

- All :code:`301` which match :code:`doesn’t exist` are returned as
  :code:`INACTIVE`

SPECIAL rules
-------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As PyFunceble grew up, I thought that a bit of filtering for special cases
would be great to introduce. That where the idea came from.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    For any new suggestion of domains where a special rule can enhance
    PyFunceble please either open a new issue or make your
    `contribution <../contributing/index.html#contribute>`_ directly into the
    project.

.. note::
    **Contribution to the SPECIAL rules**

    To add directly to the special rules please modify both the source code
    `extra_rules.py <https://github.com/funilrys/PyFunceble/blob/dev/PyFunceble/checker/availability/extra_rules.py>`_
    and the documentation (here).

Below is the list of all special rules that are implemented into PyFunceble.
Please keep in mind that you can disable the usage those rules at any time.

------

:code:`*.000webhostapp.com`
"""""""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`410` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.24.eu`
"""""""""""""""

Any subjects matching the given pattern and the :code:`503` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.altervista.org`
""""""""""""""""""""""""

.. versionadded:: 4.1.0b13

Any subjects matching the given pattern and the :code:`403` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.angelfire.com`
"""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.blogspot.*`
""""""""""""""""""""

Any subjects matching the given pattern and:

- the :code:`404` status code
- the :code:`301` status code that does not exists or are blocked by Google
- the :code:`303` status code that are blocked by Google

are supplied as :code:`INACTIVE`.

------

:code:`*.canalblog.com`
"""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code
are supplied as :code:`INACTIVE`.

------

:code:`*.dr.ag`
"""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`503` status code
are supplied as :code:`INACTIVE`.

------

:code:`*.fc2.com`
"""""""""""""""""

Any subjects matching the given pattern and the :code:`error.fc2.com`
subdomain is into the `Location` headers are supplied as :code:`INACTIVE`.

------

:code:`*.github.io`
"""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.godaddysites.com`
""""""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status codes are
supplied as :code:`INACTIVE`.

------

:code:`*.hpg.com.br`
""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.liveadvert.com`
""""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.skyrock.com`
"""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.tumblr.com`
""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.weebly.com`
""""""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.wix.com`
"""""""""""""""""

Any subjects matching the given pattern and the :code:`404` status code are
supplied as :code:`INACTIVE`.

------

:code:`*.wordpress.com`
"""""""""""""""""""""""

Any subjects matching the given pattern and the :code:`301` and :code:`410` status code along
with the pattern :code:`doesn’t exist` are supplied as :code:`INACTIVE`.


------

IP range
""""""""

Any IPv4 and IPv6 ranges are supplied as :code:`ACTIVE`.

------

How to use it?
^^^^^^^^^^^^^^

Special rules are activated by default, but you can switch its usage through:

- the (Python) API,
- the CLI argument,
- or, your configuration file.

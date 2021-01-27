EOL of any version 3.x
----------------------

Development of Pyfunceble version 3.x have reached the End Of Life.
This means any errors recurring in any version below Pyfunceble version
4.0.0 will no longer be fixed, but we will still be here to help you with a
number of workarounds that might be required to have these releases working
for you, until the final stable release of Pyfunceble version 4.0.0.

-------

If you are new to Pyfunceble, the team will recommend you to start by using and
installing the pre-release of Pyfunceble 4.0.0

You can read more about how this is done in the docs at:
`<https://pyfunceble.readthedocs.io/en/dev/installation/index.html#development-version>`_

.. NOTE::

You should know that if you are going to install version 4.0.0
through `pip`, you should use one of the following lines. Note the `--pre`
flag

.. code-block:: console

    pip3 install --user --pre pyfunceble-dev
    python3.9 -m pip install --user --pre pyfunceble-dev


In case you would like to install PyFunceble system-wide, you have to omit
the `--user` flag from the lines above, and you should probably be using
your sudo account to do this, In that case don't forget the :code:`-H` flag...

Install PyFunceble-dev 4.x systemwide with sudo.

.. code-block:: console

    sudo -H pip3 install --user --pre pyfunceble-dev
    sudo -H python3.9 -m pip install --user --pre pyfunceble-dev


------

We will also like to point you attention to the requirement section of:
`<https://pyfunceble.readthedocs.io/en/dev/installation/index.html#requirements>`_,
where there is a pending PR
`(#196) <https://github.com/funilrys/PyFunceble/pull/196>`_,
which will correct the required python version to python version `3.7`

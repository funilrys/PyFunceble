From a GitLab CI/CD environment
-------------------------------

As we offer an argument named :code:`--ci` which will
autosave in a GitLab CI/CI environment, this document try to
describe hot it works!

Configuration
^^^^^^^^^^^^^

Personal Access Token
"""""""""""""""""""""

A personal access token is needed in order for PyFunceble to
automatically push the results.

You should get `a personal GitLab access token`_ with 
the :code:`read_repository` and :code:`write_repository` scopes.

Once created and copied in a safe place, create **a new masked variable**
named :code:`GL_TOKEN` inside the CI/CD settings of your project.
The value of the variable should be the newly generated personal
access token.

.. _a personal GitLab access token: https://gitlab.com/profile/personal_access_tokens

:code:`.gitlab-ci.yml`
""""""""""""""""""""""

.. note::
    This part only present a commented :code:`.gitlab-ci.yml`.
    This is just an example do not take the following as 
    necessarly true. 

    You're invited to submit changes if something stated in 
    this document is wrong.


::

    # Python needed, so we use the python image.
    image: python:latest

    variables:
        # This is the Git name we have to set. (git config user.name)
        GIT_EMAIL: "dead-hosts@funilrys.com"
        # This is the Git Email we have to set. (git config user.email)
        GIT_NAME: "GitLab CI/CD"

    before_script:
        # We install the development version of PyFunceble.
        # If you prefer the stable version replace `pyfunceble-dev`
        # with `pyfunceble`.
        - pip3 install PyFunceble-dev

    run:
        script:
            # Let's say we want our results and our PyFunceble 
            # infrastructure to be saved in a directory called `PyFunceble-tests`

            # We move inside it.
            - cd PyFunceble-tests
            # We test the file `my_awesome_list` which is located inside the current directory.
            # Note: we precise the `--ci` argument here,
            #     but you work without it if you set `ci: true` inside your `.PyFunceble.yaml`
            - PyFunceble --ci -f my_awesome_list --plain

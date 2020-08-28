From a Travis CI container
--------------------------

As we offer an argument named :code:`--ci` to activate 
the usage of PyFunceble in a Travis CI instance,
we document here what you need to know!

Configuration
^^^^^^^^^^^^^

.. note::
   This part only present a commented :code:`.travis.yml` so that you can understand where to start.

   If you need more practical examples, feel free to report to one of `Dead-Hosts`_ repositories which use PyFunceble with Travis CI.

.. _Dead-Hosts: https://github.com/dead-hosts


::

    env:
        global:
            # The following is your encrypted GitHub API key.
            # Indeed as we are going to push to the repository, this is needed.
            #- GH_TOKEN: # This can be set in the travis-ci https://travis-ci.com/repo/settings as 'Environment Variables'
            # or as below: secure: encrypted code
            - secure: QQdKFquFFojFT9XJ1XZp4EMoDTVoXFgqZq8XU+sCVf+pJQR6d/oKBp8rnSTCnZizWOQXUjGXUUxUpSG/dYGyBLjo3rH3rsn9ciZHVfubxbwK860w4sqibl4DvhCv2rdsFtvzXnhm4P9OL3i+krKdewh9fxpNyUU58qOgfnS7mK9FcFhb8z5ak2sxU2XRZedwm6Ro0oyVKs8kFkL4YaADfNyAHlGTfr9rVmE52WXQXQENktb9gFgR2A8ZnmLy0BCMZGkPDShJnjRDWD4DErtasLmLQvWpzOBwdbVJTY6U9KDRXVNdC9lp5E5Ba/dc0y36q6vjfgJR+QchetOtHgNbKYbLB8c26Di90OZCFJsxMNcl1Wct4qFPXkFGvjXrISW6pbdPL5Plto0Ig3iLiulhYOPVArysMIk9ymtSXP+WE7VWX01LQ1fEkIoSfeVZ2caTnCmTsoHVGRRe978CojKaT7yU45kb15hcyDrzptQ8EP2hfxeh5F7KtueQ6Rsb9LFDZMkMDKflZn6a+bRhESlmWWmYB9stzGzTurQA1E1bcSACJ8A8hG5nHBzZYJ2S+OY0PE7UdyOJ0JK0qe/67d+F9ocQdIoFpDDTdgIjHerQnD2wRg1aKPzLDb4jJTpqgr5ssPrqUAKl3st7gyaAZzCEADPDnIBDjOJS+mFWbx9DKgc=
            # This is the Git name we have to set. (git config user.name)
            - GIT_NAME: Travis CI
            # This is the Git Email we have to set. (git config user.email)
            - GIT_EMAIL: dead-hosts@funilrys.com

    # This is the language we use.
    language: python

    # This is the python version we are going to use for the tests.
    # Note: you can add any 3.x version to the list.
    python:
    - "3.8"

    # The following will tell Travis CI to ends as fast as possible.
    matrix:
        fast_finish: true

    # Here we are setting what Travis CI have to cache.
    cache:
        # We are caching pip3 as we use it to install PyFunceble
        - pip3

    install:
        # We install the development version of PyFunceble. If you prefer the stable version replace 
        # `pyfunceble-dev` with `pyfunceble`.
        - pip3 install pyfunceble-dev

    # Our tests start here.
    script:
        # Let's say we want our results and our PyFunceble infrastructure to be saved in a directory 
        # called `PyFunceble-tests`

        # We move inside it.
        - cd PyFunceble-tests
        # We test the file `my_awesome_list` which is located inside the current directory.
        # Note: we precise the `--ci` argument here,
        #     but you work without it if you set `travis: true` inside your `.PyFunceble.yaml`
        - PyFunceble --ci -f my_awesome_list --plain

    # The following initiate email notification logic.
    notifications:
        # As we want to get a mail on failure and on status change, we set the following.
        on_success:   change
        on_failure:   always

Getting a GitHub token
^^^^^^^^^^^^^^^^^^^^^^

For the :code:`secure` index of the :code:`.travis.yml` file, you have to generate a `new GitHub token`_.

After you got your token, please write it or save it in a safe place as you're going to need it 
every time you're going to interact with Travis CI.

.. note::
    The scope to set is :code:`public_repo` but you can also set others depending on your needs.

.. _new GitHub token: https://github.com/settings/tokens/new

Encrypting the token for future usage under the Travis CIs' containers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To encrypt the token simply replace and execute the following according to your personal case.

::

    $ travis encrypt 'GH_TOKEN=theGeneratedToken' -r 'The content of TRAVIS_REPO_SLUG' --add

.. warning::
    Please do not execute the following explicitly without replacing :code:`theGeneratedToken` 
    with your previously generated GitHub token and :code:`The content of TRAVIS_REPO_SLUG` with 
    your repository slug.

.. note::
    The usage of :code:`--add` ensure that the :code:`travis` program automatically add the :code:`secure` 
    index to the :code:`.travis.yml` file.

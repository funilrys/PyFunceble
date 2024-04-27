Github Actions CI/CD
--------------------

Example of how you can run PyFunceble inside Github Actions.

.. code-block:: yaml
    :caption: main.yml
    :name: main.yml

    name: PyFunceble CI tests
    on:
    push:
        branches:
        - "master"
    pull_request:
        branches:
        - "master"
    schedule:
        - cron: "0 * * * *"

    env:
    PYFUNCEBLE_AUTO_CONFIGURATION: "YES"
    GIT_NAME: "${{ secrets.GIT_BOT_NAME }}"
    GIT_EMAIL: "${{ secrets.GIT_BOT_EMAIL }}"
    PYFUNCEBLE_CONFIG_DIR: "${{ github.workspace }}/.pyfunceble"
    GITHUB_TOKEN: "${{ secrets.BOT_REPO_PAT }}"

    jobs:
    single:
        name: Run PyFunceble with a single domain
        runs-on: "${{ matrix.os }}"

        strategy:
        fail-fast: false
        matrix:
            python_version:
            - "3.11"
            os:
            - ubuntu-latest

        steps:
        - uses: actions/checkout@v4
            name: Clone repository
            with:
            token: "${{ secrets.BOT_REPO_PAT }}"

        - name: Set up Python ${{ matrix.python_version }}
            uses: actions/setup-python@v2
            with:
            python-version: ${{ matrix.python_version }}

        - name: Install dependencies
            run: |
            pip install --pre PyFunceble-dev

        - name: Get PyFunceble version
            run: |
            PyFunceble --version

        - name: Run PyFunceble
            run: |
            PyFunceble -a --logging-level critical -d github.com

    file_and_push:
        name: Run PyFunceble against a file and push result to repository
        runs-on: "${{ matrix.os }}"

        strategy:
        fail-fast: false
        matrix:
            python_version:
            - "3.11"
            os:
            - ubuntu-latest

        steps:
        - uses: actions/checkout@v4
            name: Clone repository
            with:
            token: "${{ secrets.BOT_REPO_PAT }}"

        - name: Set up Python ${{ matrix.python_version }}
            uses: actions/setup-python@v2
            with:
            python-version: ${{ matrix.python_version }}

        - name: Install dependencies
            run: |
            pip install --pre PyFunceble-dev

        - name: Get PyFunceble version
            run: |
            PyFunceble --version

        - name: Run PyFunceble
            run: |
            PyFunceble -a --ci --logging-level critical -f test.list

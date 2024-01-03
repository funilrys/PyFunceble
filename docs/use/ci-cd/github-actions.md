# Github Action

PyFunceble can be used within a GitHub Action container.
The idea is to run PyFunceble within a GitHub Action container and let PyFunceble push the result into a Git Repository.

## Environment Variables

| Environment Variable          | Description                                                                                                                                                                                                    |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GITHUB_ACTIONS                | The variable PyFunceble will look for to decide which CI "engine" to use. **BEWARE:** If you use this variable to test locally, your configurations may get messy. Please test within an isolated environment. |
| PYFUNCEBLE_AUTO_CONFIGURATION | Let PyFunceble manage the configuration files.                                                                                                                                                                 |
| PYFUNCEBLE_CONFIG_DIR         | Let PyFunceble know where it should store its configuration files.                                                                                                                                             |
| GITHUB_TOKEN                  | The token PyFunceble has to use to push changes to the repository.                                                                                                                                             |
| GIT_NAME                      | The `git.name` to setup and use.                                                                                                                                                                               |
| GIT_EMAIL                     | The `git.email` to setup and use.                                                                                                                                                                              |
| GIT_BRANCH                    | The Git branch to use to store testing results between serveral sessions.                                                                                                                                      |
| GIT_DISTRIBUTION_BRANCH       | The Git branch to use to store and distribute the final results.                                                                                                                                               |

## Example

Here is an example that demonstrate how to use PyFunceble within a GitHub Workflow.

```yaml title=".github/workflows/main.yml"
name: PyFunceble CI tests
on:
  push:
    branches:
      - "my-awesome-branch"
  pull_request:
    branches:
      - "my-awesome-branch"

env:
  # Let PyFunceble know that it has to manage the configuration by itself.
  PYFUNCEBLE_AUTO_CONFIGURATION: "YES"
  # We want PyFunceble to push result to the branch, therefore, we need to
  # declare our git settings.
  GIT_NAME: "${{ secrets.GIT_BOT_NAME }}"
  GIT_EMAIL: "${{ secrets.GIT_BOT_EMAIL }}"
  # Define the branch PyFunceble has to use while working.
  GIT_BRANCH: my-awesome-branch
  # Define the branch PyFunceble will push the final result into.
  GIT_DISTRIBUTION_BRANCH: my-awesome-branch
  # Define the path of the configuration directory.
  PYFUNCEBLE_CONFIG_DIR: "${{ github.workspace }}/.pyfunceble"
  # By settings this variable, PyFunceble will use its GitHub Action feature
  # to setup and push to the current repository.
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
      - uses: actions/checkout@v3
        name: Clone repository
        with:
          token: "${{ secrets.BOT_REPO_PAT }}"

      - name: Set up Python ${{ matrix.python_version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python_version }}

      - name: Install dependencies
        run: |
          pip install pyfunceble-dev

      - name: Get PyFunceble version
        run: |
          pyfunceble --version

      - name: Run PyFunceble
        run: |
          pyfunceble -a --logging-level critical -d github.com

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
      - uses: actions/checkout@v3
        name: Clone repository
        with:
          token: "${{ secrets.BOT_REPO_PAT }}"

      - name: Set up Python ${{ matrix.python_version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python_version }}

      - name: Install dependencies
        run: |
          pip install pyfunceble-dev

      - name: Get PyFunceble version
        run: |
          pyfunceble --version

      - name: Run PyFunceble
        # Warning: this assume that the test.list file is at the root of the
        # repository.
        run: |
          pyfunceble -a --ci --logging-level critical -f test.list
```

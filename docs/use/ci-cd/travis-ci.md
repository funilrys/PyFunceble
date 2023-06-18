# Travis CI

PyFunceble can be used within a Travis CI instance.
The idea is to run PyFunceble within an instance and let PyFunceble push the result into a Git Repository.

## Environment Variables

| Environment Variable          | Description                                                                                                                                                                                                     |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TRAVIS_BUILD_DIR              | The variables PyFunceble will look for to decide which CI "engine" to use. **BEWARE:** If you use this variable to test locally, your configurations may get messy. Please test within an isolated environment. |
| PYFUNCEBLE_AUTO_CONFIGURATION | Let PyFunceble manage the configuration files.                                                                                                                                                                  |
| PYFUNCEBLE_CONFIG_DIR         | Let PyFunceble know where it should store its configuration files.                                                                                                                                              |
| GH_TOKEN                      | The token PyFunceble has to use to push changes to the repository.                                                                                                                                              |
| GIT_NAME                      | The `git.name` to setup and use.                                                                                                                                                                                |
| GIT_EMAIL                     | The `git.email` to setup and use.                                                                                                                                                                               |
| GIT_BRANCH                    | The Git branch to use to store testing results between serveral sessions.                                                                                                                                       |
| GIT_DISTRIBUTION_BRANCH       | The Git branch to use to store and distribute the final results.                                                                                                                                                |

## Configuration: GitHub Personal Access Token

A personal access token is needed in order for PyFunceble to automatically push the results. If your repository is hosted on GitHub, you have to [generate a new GitHub PAT](https://github.com/settings/tokens/new) with _(at least)_ the `public_repo` scope.

Once created and copied in a safe place, you can use the Travis CI CLI to embed your
variable into your job description through the following command:

```sh
travis encrypt 'GH_TOKEN=MyAwes0meToken' -r 'myowner/myrepo' --add
```

## Example

Here is an example that demonstrate how to use PyFunceble within a Travis CI instance.

!!! warning

    This example won't push result until you define the `GH_TOKEN` secret environment variable.

```yaml title=".gitlab-ci.yml"
env:
  global:
    # The following is your encrypted GitHub API key.
    # Indeed as we are going to push to the repository, this is needed.
    #- GH_TOKEN: # This can be set in the travis-ci https://travis-ci.com/repo/settings as 'Environment Variables'
    # or as below: secure: encrypted code
    - secure: QQdKFquFFojFT9XJ1XZp4EMoDTVoXFgqZq8XU+sCVf+pJQR6d/oKBp8rnSTCnZizWOQXUjGXUUxUpSG/dYGyBLjo3rH3rsn9ciZHVfubxbwK860w4sqibl4DvhCv2rdsFtvzXnhm4P9OL3i+krKdewh9fxpNyUU58qOgfnS7mK9FcFhb8z5ak2sxU2XRZedwm6Ro0oyVKs8kFkL4YaADfNyAHlGTfr9rVmE52WXQXQENktb9gFgR2A8ZnmLy0BCMZGkPDShJnjRDWD4DErtasLmLQvWpzOBwdbVJTY6U9KDRXVNdC9lp5E5Ba/dc0y36q6vjfgJR+QchetOtHgNbKYbLB8c26Di90OZCFJsxMNcl1Wct4qFPXkFGvjXrISW6pbdPL5Plto0Ig3iLiulhYOPVArysMIk9ymtSXP+WE7VWX01LQ1fEkIoSfeVZ2caTnCmTsoHVGRRe978CojKaT7yU45kb15hcyDrzptQ8EP2hfxeh5F7KtueQ6Rsb9LFDZMkMDKflZn6a+bRhESlmWWmYB9stzGzTurQA1E1bcSACJ8A8hG5nHBzZYJ2S+OY0PE7UdyOJ0JK0qe/67d+F9ocQdIoFpDDTdgIjHerQnD2wRg1aKPzLDb4jJTpqgr5ssPrqUAKl3st7gyaAZzCEADPDnIBDjOJS+mFWbx9DKgc=
    # Let PyFunceble know that it has to manage the configuration by itself.
    PYFUNCEBLE_AUTO_CONFIGURATION: "YES"
    # This is the Git name we have to set. (git config user.name)
    - GIT_NAME: "PyFunceble @ Travis CI"
    # This is the Git Email we have to set. (git config user.email)
    - GIT_EMAIL: foobar@example.com
    # Define the branch PyFunceble has to use while working.
    - GIT_BRANCH: my-awesome-branch
    # Define the branch PyFunceble will push the final result into.
    - GIT_DISTRIBUTION_BRANCH: my-awesome-branch
    # Define the path of the configuration directory.
    - PYFUNCEBLE_CONFIG_DIR: "${TRAVIS_BUILD_DIR}/.pyfunceble"

# This is the language we use.
language: python

# This is the python version we are going to use for the tests.
# Note: you can add any 3.x version to the list.
python:
  - "3.11"

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
  - pyfunceble --version
  # Warning: this assume that the test.list file is at the root of the
  # repository.
  - pyfunceble -a --ci --logging-level critical -f test.list

# The following initiate email notification logic.
notifications:
  # As we want to get a mail on failure and on status change, we set the following.
  on_success: change
  on_failure: always
```

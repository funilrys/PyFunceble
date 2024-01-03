# GitLab CI/CD

PyFunceble can be used within a GitLab CI/CD runner.
The idea is to run PyFunceble within a runner and let PyFunceble push the result into a Git Repository.

## Environment Variables

| Environment Variable          | Description                                                                                                                                                                                                     |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GITLAB_CI / GITLAB_USER_ID    | The variables PyFunceble will look for to decide which CI "engine" to use. **BEWARE:** If you use this variable to test locally, your configurations may get messy. Please test within an isolated environment. |
| PYFUNCEBLE_AUTO_CONFIGURATION | Let PyFunceble manage the configuration files.                                                                                                                                                                  |
| PYFUNCEBLE_CONFIG_DIR         | Let PyFunceble know where it should store its configuration files.                                                                                                                                              |
| GL_TOKEN                      | The token PyFunceble has to use to push changes to the repository.                                                                                                                                              |
| GIT_NAME                      | The `git.name` to setup and use.                                                                                                                                                                                |
| GIT_EMAIL                     | The `git.email` to setup and use.                                                                                                                                                                               |
| GIT_BRANCH                    | The Git branch to use to store testing results between serveral sessions.                                                                                                                                       |
| GIT_DISTRIBUTION_BRANCH       | The Git branch to use to store and distribute the final results.                                                                                                                                                |

## Configuration: Personal Access Token

A personal access token is needed in order for PyFunceble to automatically push the results.

You should get [a personal GitLab access token](https://gitlab.com/profile/personal_access_tokens) with the `read_repository` and `write_repository` scopes.

Once created and copied in a safe place, create a new masked variable called `GL_TOKEN` inside the CI/CD settings of your project. The value of the variable should be the newly generated personal access token.

## Example

Here is an example that demonstrate how to use PyFunceble within a GitLab CI/CD Runner.

!!! warning

    This example won't push result until you define the `GL_TOKEN` secret environment variable.

```yaml title=".travis.yml"
# Python needed, so we use the python image.
image: python:latest

variables:
  # Let PyFunceble know that it has to manage the configuration by itself.
  PYFUNCEBLE_AUTO_CONFIGURATION: "YES"
  # This is the Git name we have to set. (git config user.name)
  GIT_EMAIL: "foobar@example.org"
  # This is the Git Email we have to set. (git config user.email)
  GIT_NAME: "PyFunceble @ GitLab CI/CD"
  # Define the branch PyFunceble has to use while working.
  GIT_BRANCH: my-awesome-branch
  # Define the branch PyFunceble will push the final result into.
  GIT_DISTRIBUTION_BRANCH: my-awesome-branch
  # Define the path of the configuration directory.
  PYFUNCEBLE_CONFIG_DIR: "${CI_PROJECT_DIR}/.pyfunceble"

before_script:
  - pip3 install pyfunceble-dev

run:
  script:
    - pyfunceble --version
    # Warning: this assume that the test.list file is at the root of the
    # repository.
    - pyfunceble -a --ci --logging-level critical -f test.list
```

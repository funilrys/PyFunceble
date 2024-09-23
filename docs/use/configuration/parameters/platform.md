# `platform`

PyFunceble alone is a great tool. What if we could just test the subject that
were not already tested by others ?

!!! danger "Beware!!!!"

    The parameters listed below are not production ready. You should use or
    activate them only if you have good reasons to.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
platform:
  # Provides everything related to the platform.
  # PyFunceble alone is a great tool. What if we could just test the subject that
  # were not already tested by others ?

  # Enable or disable the push of datasets (cf: test results) into the platform
  # (API).
  #
  # NOTE:
  #     This parameter is useless, unless you have a valid API Token defined
  #     into the PYFUNCEBLE_PLATFORM_API_TOKEN environment variable.
  #
  # CLI Argument: --push-platform
  push: no

  # Set the preferred pull "method".
  #
  # The platform (API) does not only provides datasets but it also offer an
  # aggregation endpoint that let PyFunceble pull datasets.
  # When pulling information about a subject that is already known by the platform,
  # it returns 3 group of results:
  #
  #   - `frequent`, which provides the status that was mostly been pushed.
  #   - `latest`, which provides the status based on the latest submitted datasets.
  #   - `recommended`, which provides the recommended status.
  #
  # CLI Argument: --platform-preferred-origin
  preferred_status_origin: recommended

  # Defines the checker type to prioritize when trying to fullfil platform
  # contracts.
  #
  # Notes:
  #   1. This is a list. The order matters.
  #   2. One can overwrite this value, by settings a comma separated list of
  #      checker type to prioritize through the PYFUNCEBLE_PLATFORM_CHECKER_PRIORITY
  #      environment variable.
  #   3. When set to `none`, the platform will throw a random contract at us.
  #
  # Example:
  #   Prioritize availability checker until no contract is available, then
  #   prioritize syntax checker until no contract is available, then prioritize
  #   reputation checker until no contract is available.
  #
  #   - availability
  #   - syntax
  #   - reputation
  #
  # Available Values: none | availability | reputation | syntax
  #
  # CLI Argument: none
  checker_priority:
    - none

  # Defines the checker type to exclude when trying to fullfil platform
  # contracts.
  #
  # Notes:
  #   1. This is a list.
  #   2. One can overwrite this value, by settings a comma separated list of
  #      checker type to exclude through the PYFUNCEBLE_PLATFORM_CHECKER_EXCLUDE
  #      environment variable.
  #   3. When set to `none`, no checker type will be excluded.
  #
  # Example:
  #   Exclude the reputation checker from the list of checker to use to fullfil.
  #
  #   - reputation
  #
  # Available Values: none | availability | reputation | syntax
  #
  # CLI Argument: none
  checker_exclude:
    - none
```

## `push`

Enable or disable the push of datasets (cf: test results) into the platform
(API).

!!! danger "Beware!!!!"

    The parameters listed below are not production ready. You should use or
    activate them only if you have good reasons to.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--push-platform`

## `preferred_status_origin`

Set the preferred pull "method".

The platform (API) does not only provides datasets but it also offer an
aggregation endpoint that let PyFunceble pull datasets.
When pulling information about a subject that is already known by the platform,
it returns 3 group of results:

- `frequent`, which provides the status that was mostly been pushed.
- `latest`, which provides the status based on the latest submitted datasets.
- `recommended`, which provides the recommended status.

!!! danger "Beware!!!!"

    The parameters listed below are not production ready. You should use or
    activate them only if you have good reasons to.

**Type:** string

**Default Value:** `recommended`

**Available Values:** `frequent`, `latest`, `recommended`

**CLI Argument:** `--platform-preferred-origin`

## `checker_priority`

Defines the checker type to prioritize when trying to fullfil platform contracts.

!!! note "Notes:"

    1. This is a list. The order matters.
    2. One can overwrite this value, by settings a comma separated list of
       checker type to prioritize through the PYFUNCEBLE_PLATFORM_CHECKER_PRIORITY
       environment variable.
    3. When set to `none`, the platform will throw a random contract at us.

**Example:**
  Prioritize availability checker until no contract is available, then
  prioritize syntax checker until no contract is available, then prioritize
  reputation checker until no contract is available.

  ```yaml
  checker_priority:
    - availability
    - syntax
    - reputation
  ```

!!! danger "Beware!!!!"

    The parameters listed below are not production ready. You should use or
    activate them only if you have good reasons to.

**Type:** list[string]

**Default Value:** `["none"]`

**Available Values:** `none`, `availability`, `reputation`, `syntax`

**CLI Argument:** none

## `checker_exclude`

Defines the checker type to exclude when trying to fullfil platform contracts.

!!! note "Notes:"

    1. This is a list.
    2. One can overwrite this value, by settings a comma separated list of
       checker type to exclude through the PYFUNCEBLE_PLATFORM_CHECKER_EXCLUDE
       environment variable.
    3. When set to `none`, no checker type will be excluded.

**Example:**

  Exclude the reputation checker from the list of checker to use to fullfil.

  ```yaml
  checker_exclude:
    - reputation
  ```

!!! danger "Beware!!!!"

    The parameters listed below are not production ready. You should use or
    activate them only if you have good reasons to.

**Type:** list[string]

**Default Value:** `["none"]`

**Available Values:** `none`, `availability`, `reputation`, `syntax`

**CLI Argument:** none


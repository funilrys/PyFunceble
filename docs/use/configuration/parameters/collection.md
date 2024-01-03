# `collection`

PyFunceble alone is a great tool. What if we could just test the subject that
were not already tested by others ?

!!! danger "Beware!!!!"

    The parameters listed below are not production ready. You should use or
    activate them only if you have good reasons to.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
collection:
  # Provides everything related to the collection.
  # PyFunceble alone is a great tool. What if we could just test the subject that
  # were not already tested by others ?

  # Set the base URL to access to the collection (API).
  url_base: https://collection.dead-hosts.funilrys.com

  # Enable or disable the push of datasets (cf: test results) into the collection
  # (API).
  #
  # NOTE:
  #     This parameter is useless, unless you have a valid API Token defined
  #     into the COLLECTION_API_TOKEN environment variable.
  #
  # CLI Argument: --push-collection
  push: no

  # Set the prefered pull "method".
  #
  # The collection (API) is not only a collection of datasets but it also offer
  # an aggregeation endpoints that let PyFunceble pull datasets.
  # When pulling information about a subject that is already known by the collection,
  # it returns 3 group of results:
  #
  #   - `frequent`, which provides the status that was mostly been pushed.
  #   - `latest`, which provides the status based on the lastest submitted datasets.
  #   - `recommended`, which provides the recommended status.
  #
  # CLI Argument: --collection-preferred-origin
  preferred_status_origin: recommended
```

## `url_base`

Set the base URL to access to the collection (API).

**Type:** HTTP URL

**Default Value:** `https://collection.dead-hosts.funilrys.com`

**Available Values:** -

**CLI Argument:** None

## `push`

Enable or disable the push of datasets (cf: test results) into the collection
(API).

!!! danger Beware!!!

    This parameter is useless, unless you have a valid API token defined into
    the COLLECTION_API_TOKEN environment variable.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--push-collection`

## `preferred_status_origin`

Set the prefered pull "method".

The collection (API) is not only a collection of datasets but it also offer
an aggregeation endpoints that let PyFunceble pull datasets.
When pulling information about a subject that is already known by the collection,
it returns 3 group of results:

- `frequent`, which provides the status that was mostly been pushed.
- `latest`, which provides the status based on the lastest submitted datasets.
- `recommended`, which provides the recomended status.

**Type:** string

**Default Value:** `recommended`

**Available Values:** `frequent`, `latest`, `recommended`

**CLI Argument:** `--collection-preferred-origin`

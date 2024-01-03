# `max_http_retries`

To retry or not to retry, that is the question!

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
# Set the maximum number of retries to perform before giving up a request.
#
# WARNING:
#   This should be an integer >= 0.
#
# CLI Argument: --max-http-retries
max_http_retries: 3
```

**Type:** integer

**Default Value:** `3`

**Available Values:** Any value greater than `0`.

**CLI Argument:** `--max-http-retries`

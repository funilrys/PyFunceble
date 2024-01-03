# `debug`

PyFunceble provides a debug mode which outputs everything that is being done.
While this is helpful for troubleshooting, this is not adviced for everyone.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
debug:
  # Provides everything related to the debug mode.

  # Enable/Disable the debug mode.
  #
  # NOTE:
  #   When enabled, the output will be found inside the logs output directory.
  #   If you prefer to have the output to STDOUT, you should declare the
  #   following environment variable.
  #
  #     PYFUNCEBLE_DEBUG_ON_SCREEN=yes

  # Environment Variable: PYFUNCEBLE_DEBUG
  # CLI Switch: `--debug`
  active: no

  # Set the logging level.
  #
  # Available: info, error, debug, critical
  #
  # Environment Variables: PYFUNCEBLE_DEBUG_LVL | PYFUNCEBLE_LOGGING_LVL
  # CLI Switch: --logging-level
  level: info
```

## `active`

Enable or disable the debug mode.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--debug`

**Environment Variable:** `PYFUNCEBLE_DEBUG=yes`

## `level`

Set the minimal logging level.

**Type:** string

**Default Value:** `info`

**Available Values:** `info`, `error`, `debug`, `critical`

**CLI Argument:** `--logging-level`

**Environment Variable:** `PYFUNCEBLE_DEBUG_LVL=info` | `PYFUNCEBLE_LOGGING_LVL`
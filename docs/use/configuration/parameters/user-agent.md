# `user_agent`

PyFunceble can choose a random user-agent to send when making HTTP requests. This
is how to parametrize.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
user_agent:
  # Provides everything related to choice of user agent.

  # Set the browser to pickup.
  #
  # WARNING:
  #     This parameter will be deprecated (soon?).
  #
  # Available Values: chrome, edge, firefox, ie, opera, safari
  browser: chrome

  # Set the platform to pickup.
  #
  # Available Values: linux, macosx, win10
  platform: linux

  # Set the User-Agent to use.
  #
  # WARNING:
  #     If you choose to set this argument, the browser or platform arguments
  #     won't be taken into consideration.
  #
  # CLI Argument: -ua | --user-agent
  custom: null
```

## `browser`

Set the browser to pickup.

**Type:** string

**Default Value:** `chrome`

**Available Values:** `chrome`, `edge`, `firefox`, `ie`, `opera`, `safari`

**CLI Argument:** None

## `platform`

Set the platform to pickup.

**Type:** string

**Default Value:** `chrome`

**Available Values:** `linux`, `macosx`, `win10`

**CLI Argument:** None

## `custom`

Set the User-Agent to use.


**Type:** string

**Default Value:** `null`

**Available Values:** User-Defined values

**CLI Argument:** `-ua`, `--user-agent`
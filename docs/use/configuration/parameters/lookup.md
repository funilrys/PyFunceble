# `lookup`

To lookup or not lookup, that is the question!

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
lookup:
  # Provides everything related to the lookups.

  # Enable/Disable the usage of DNS records to lookup the status.
  #
  # CLI Argument: --dns-lookup
  # Exclusive CLI Argument: --dns-lookup-only
  dns: yes

  # Enable/Disable the usage of HTTP status codes to lookup the status.
  #
  # CLI Argument: --http | --http-status-code-lookup
  # Exclusive CLI Argument: --http-only | --http-status-code-lookup
  http_status_code: yes

  # Enable/Disable the usage of network (information) socket to lookup the status.
  #
  # CLI Argument: --netinfo-lookup
  # Exclusive CLI Argument: --netinfo-lookup-only
  netinfo: yes

  # Enable/Disable the usage of special rules to lookup or switch the status.
  #
  # CLI Argument: --special-lookup
  # Exclusive CLI Argument: --special-lookup-only
  special: yes

  # Enable/Disable the usage of WHOIS records to lookup the status.
  #
  # CLI Argument: --whois-lookup
  # Exclusive CLI Argument: --whois-lookup-only
  whois: yes

  # Enable/Disable the usage of the reputation data to lookup the status.
  #
  # NOTE:
  #     The reputation lookup is actualy a lookup against the AlienVault IPv4
  #     reputation file.s
  #
  # CLI Argument: --reputation-lookup
  # Exclusive CLI Argument: --reputation-lookup
  reputation: no

  # Enable/Disable the usage of the collection (API) to lookup the status.
  #
  # CLI Argument: --collection-lookup
  # Exclusive CLI Argument: --collection-lookup-only
  collection: no

  # Set the timeout to apply to each of our lookup methods - when possible.
  #
  # WARNING:
  #     This should be a value >= 0.
  #
  # CLI Argument: -t | --timeout
  timeout: 5
```

## `dns`

Enable or disable the usage of DNS recors to lookup the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--dns-lookup`

**Exclusive CLI Argument:** `--dns-lookup-only`

## `http_status_code`

Enable or disable the usage of HTTP status codes to lookup the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--http-only`, `--http-status-code-lookup`

**Exclusive CLI Argument:** `--http-only`, `--http-status-code-lookup-only`

## `netinfo`

Enable or disable the usage of network (information) socket to lookup the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--netinfo-lookup`

**Exclusive CLI Argument:** `--netinfo-lookup-only`

## `special`

Enable or disable the usage of special rules to lookup or switch the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--special-lookup`

**Exclusive CLI Argument:** `--special-lookup-only`

## `whois`

Enable or disable the usage of WHOIS records to lookup the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--whois-lookup`

**Exclusive CLI Argument:** `--whois-lookup-only`

## `reputation`

Enable or disable the usage of reputation data to lookup the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--reputation-lookup`

**Exclusive CLI Argument:** `--reputation-lookup-only`

## `collection`

Enable or disable the usage of the collection (API) to lookup the status.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--collection-lookup`

**Exclusive CLI Argument:** `--collection-lookup-only`

## `timeout`

Set the timeout to apply to each of our lookup methods - when possible.

**Type:** integer

**Default Value:** `5`

**Available Values:** Any value greater that `0`.

**CLI Argument:** `-t`, `--timeout`

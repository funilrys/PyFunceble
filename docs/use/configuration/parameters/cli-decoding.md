# `cli_decoding`

When using the CLI, you can use some of the parameters listed below to control
the way inputed files are being decoded or interpreted.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
cli_decoding:
  # Provides everything related to the decoding of input files from the CLI.

  # Enable/Disable the aggressive decoding.
  #
  # The aggressive mode is a mode that tries to decode as much as possible without
  # trying to follow any technical conventions.
  #
  # When decoding AdBlock filter lists, it will try to decode almost every
  # domains it finds.
  #
  # When decoding hosts file or plain text files, it will try to convert URLS
  # (e.g https://example.org/hello/world) into domains to test (e.g example.org).
  #
  # CLI Argument: --aggressive
  aggressive: no

  # Enable/Disable the (exclusive) decoding using the adblock decoder.
  #
  # WARNING:
  #     Activating this parameter in your configuration file, will make
  #     PyFunceble assume that it has to decode adblock files - exclusively.
  #
  # CLI Argument: --adblock
  adblock: no

  # Enable/Disable the (exclusive) decoding using the RPZ decoder.
  #
  # WARNING:
  #     Activating this parameter in your configuration file, will make
  #     PyFunceble assume that it has to decode RPZ files - exclusively.
  #
  # CLI Argument: --rpz
  rpz: no

  # Enable or disable the reduction of wildcards.
  #
  # Meaning that any caught wildcards (e.g. *.example.org) will be reduced so
  # that we have a "valid" domain to test (e.g. example.org).
  #
  # WARNING:
  #     Activating this parameter will reduce wildcards (e.g *.example.org) to
  #     match domains (e.g ecample.org)
  #
  # CLI Argument: --wildcard
  wildcard: no
```

## `aggressive`

Enable or disable the aggressive mode. The aggressive mode is a mode that tries
to decode as much as possible without trying to follow any technical conventions.

When using this parameter while decoding AdBlock filter lists, it will try to
decode almost every domains it finds.

However, when using this parameter while decoding hosts or plain lists, it will
also convert URLs (e.g `https://example.com/hello/world`) into domains to test
(e.g `example.com`).

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--aggressive`

## `adblock`

Enable or disable the (exclusive) decoding of AdBlock filter lists.

!!! danger "Beware!!!!"

    If you choose to activate this parameter in your configuration file,
    PyFunceble will assume that any inputed files are AdBlock filter lists to
    decode.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--adblock`

## `rpz`

Enable or disable the (exclusive) decoding of RPZ files.

!!! danger "Beware!!!!"

    If you choose to active this parameter in your configuration file,
    PyFunceble will assume that any inputed files are RPZ files to decode.

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--rpz`

## `wildcard`

Enable or disable the reduction of wildcards. Meaning that any caught wildcards
(e.g. \*.example.org) will be reduced so that we have a "valid" domain to test
(e.g. example.org).

**Type:** boolean

**Default Value:** `no`

**Available Values:** `yes`, `no`

**CLI Argument:** `--wildcard`

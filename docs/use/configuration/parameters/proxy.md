# `proxy`

PyFunceble can let you proxy requests to another server or service.
This parameter let you defines rules and global proxies to use.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
proxy:
  # Provides everything related to the proxy usage and configuration.
  #
  # The idea:
  #   We have two main keys, "global" and "rules".
  #   The system will always follow the global keys unless you define an explit
  #   TLD.
  #
  # Example:
  #
  #   Let's say we want all HTTP requests to go through example.org but we want
  #   all HTTP request for domains ending with `.com`, `.org` and `.dev` to go
  #   through example.com. And, we want all domains ending with `.onion` to go
  #   through example.dev.
  #
  #   This is how it will look like.
  #
  #       global:
  #         http: http://example.org:8080
  #         https: http://example.org:8080
  #
  #       rules:
  #         - http: http://example.com:8080
  #           https: http://example.org:8080
  #           tld:
  #             - com
  #             - org
  #             - dev
  #         - http: socks5h://example.dev:8080
  #           https: socks5h://example.dev:8080
  #           tld:
  #             - onion
  #

  global:
    # Global HTTP proxy to use when no rule is given or matched.
    #
    # CLI Argument: --http-proxy
    http: null

    # Global HTTPS proxy to use when no rule is given or matched.
    #
    # CLI Argument: --https-proxy
    https: null

  # The rules to apply.
  # See example.
  rules: []
```

## Example

PyFunceble - like many other python programs - follow any `HTTP_PROXY` or
`HTTPS_PROXY` environment variable. However, end-users that want to define
a proxy per Top Level Domain are advised to use the configuration parameters as
it offers of way to define proxy rules.

Through the `proxy.global.http` and `proxy.global.https` parameters, one can set
the proxy to reach when no rules is given or matched.

However, if you want something more granular, you may use the `proxy.rules`
parameter.

Let's say we want:

- any domains ending with `.com`, `.org`, and `.dev` to be tested through the
  `http://spec-proxy.example.com` proxy for any HTTP traffic and
  `http://spec-proxy.example.com:8443` for any HTTPS traffic.

- any domains ending with `.ionion` to be tested through the
  `http://onion-proxy.example.com` proxy.

- any other domains to be tested through `http://proxy.example.com` for any HTTP
  traffic and `http://proxy.example.com:8443` for any HTTP traffic.

How would you do that ? It's simple, simply define the following rules:

```yaml title=".PyFunceble.overwrite.yaml"
proxy:
  rules:
    # Any domains ending with `.com`, `.org` and `.dev`
    - http: http://spec-proxy.example.com
      https: http://spec-proxy.example.com:8443
      tld:
        - com
        - org
        - dev

    # Any domains ending with `.onion`
    - http: http://onion-proxy.example.com
      https: http://onion-proxy.example.com
      tld:
        - onion

  global:
    # Any other domains
    http: http://proxy.example.com
    https: http://proxy.example.com:8443
```

## `global`

Set the global HTTP and HTTPS proxies.

### Overview

```yaml title=".PyFunceble.overwrite.yaml"
proxy:
  global:
    # Global HTTP proxy to use when no rule is given or matched.
    #
    # CLI Argument: --http-proxy
    http: null

    # Global HTTPS proxy to use when no rule is given or matched.
    #
    # CLI Argument: --https-proxy
    https: null
```

### `http`

Set the proxy to reach for any HTTP traffic when no rule is given or matched.

**Type:** string

**Default Value:** `null`

**Available Values:** User-Defined Values

**CLI Argument:** `--http-proxy`

### `https`

Set the proxy to reach for any HTTPS traffic when no rule is given or matched.

**Type:** string

**Default Value:** `null`

**Available Values:** User-Defined Values

**CLI Argument:** `--https-proxy`

## `rules`

Set the proxy rules PyFunceble has to match. (See also: [Example](#example)).

**Type:** list[dict]

**Default Value:** `[]`

**Available Values:** User-Defined Values

**CLI Argument:** `--https-proxy`

**Boilerplate:**

```yaml
- http: {HTTP_PROXY}
  https: {HTTP_PROXY}
  tld:
    - {TLD}
    - {TLD2}
    - {TLD3}
```

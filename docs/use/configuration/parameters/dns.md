# `dns`

PyFunceble has its own DNS resolver which is extensively used to lookup statuses.
In this section, you will find all available parameters.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
dns:
  # Provides everything related to the DNS resolver & lookup.

  # Enable/Disable the follow-up of the order of DNS server.
  #
  # NOTE:
  #     When disabled, the order of the DNS servers is randomized.
  #
  # CLI Argument: --follow-server-order
  follow_server_order: yes

  # Enable/Disable the trust mode.
  #
  # When this parameter is enabled, we will trust the result of the first DNS
  # server and only switch to the next server in the list ONLY when it is
  # unreachable.
  #
  # However, when this parameter is disabled, we will ask the other server when
  # the previous DNS give us a negative response - until a positive on is given.
  #
  # CLI Argument: --trust-dns-server
  trust_server: no

  # Set the list of DNS server to communicate with.
  #
  # WARNING:
  #   IPv6 should be given in this format if a port is explicitly given:
  #
  #     [ip]:port
  #
  #   If you omit the braket, the port will be set to the default one (53).
  #
  # Example:
  #   - first.dns
  #   - second.dns
  #
  # CLI Argument: --dns
  server: null

  # Set the protocol to use.
  #
  # Available Values: UDP | TCP | HTTPS | TLS
  #
  # CLI Argument: --dns-protocol
  protocol: UDP

  # Set the delay (in second) to apply between each queries.
  #
  # WARNING:
  #     This should be a value >= 0.0.
  #
  # CLI Argument: --dns-delay
  delay: 0.0
```

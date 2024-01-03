# Parameters

As you now know, PyFunceble can be configured through the CLI, or its configuration
file.

## CLI Arguments: Behavior while switching boolean parameters

When switching boolean parameters through the CLI arguments, you have to keep
in mind that the CLI will act like a light switch.
Meaning that if you define `yes` in any boolean parameter and you use
the CLI argument to quickly switch its value, PyFunceble will be started with
the parameter set to `no`.

The same thing happens the other way around. if you define `no` in any boolean
parameter and you use the CLI argument to quickly switch its value, PyFunceble
will be started with the paramet set to `yes`.

Let say we set the `verify_ssl_certificates` parameter to `yes`:`

```yaml title=".PyFunceble.overwrite.yaml"
verify-ssl-certificates: yes
```

If we now use the `--verify-ssl-certificate` parameter through the CLI

```shell
pyfunceble  --verify-ssl-certificate -d example.org
```

PyFunceble will starts with the `verify_ssl_certificates` set to `no` - and
vice-versa.


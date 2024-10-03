# Configuration

PyFunceble provides a set of functionalities that you can influence through configuration.
There are multiple way to configure PyFunceble so let's get started :smile:

PyFunceble primarily load it's configuration from a file called `.PyFunceble.yaml`.
That's the file PyFunceble generate with its default settings. However, you can
overwrite any of the configuration value through a `.PyFunceble.overwrite.yaml` file
or the corresponding CLI parameter.

## TLTR; Location

Here a table that show the configuration file location - at best efforts.
If your installation is not writing at any of the location listed below,
please refer to the [location documentation](location.md) page.

If you want to skip and define your own configuration folder, you can define
the storage location of the configuration files through
the `PYFUNCEBLE_CONFIG_DIR` environment variable.

| OS / Engine    | Location               |
| -------------- | ---------------------- |
| Linux          | `~/.config/PyFunceble` |
| MacOS          | `~/.config/PyFunceble` |
| Windows        | `%APPDATA%\PyFunceble` |
| GitHub Actions | Workspace              |
| GitLab CI/CD   | Workspace              |
| Travis CI      | Workspace              |
| Jenkins CI     | Workspace              |

At any time, you can provide your own configuration file through the `--config-file` CLI argument. If the given argument is a URL, PyFunceble will download it and use it as the configuration file.

## Filename-s

At you configuration folder, PyFunceble will automatically create 2 files for you.

1. `.PyFunceble.yaml`, this file is the default configuration file for your current version. Overtime, it will be overwritten and updated as features comes and goes from a version to another. This file is provided to ensure PyFunceble run at all time with a fully compatible configuration file.
2. `.PyFunceble.overwrite.yaml`, this is generated empty. One generated, PyFunceble will never write into it. That's the file where you put your own configuration choices overwrites.

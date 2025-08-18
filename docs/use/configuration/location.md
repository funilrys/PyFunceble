# Location

Depending on how and where PyFunceble is operated, it will try to load the
configuration from dedicated locations.

## Custom Folder

If you want to skip and define your own configuration folder, you can define
the storage location of the configuration files through
the `PYFUNCEBLE_CONFIG_DIR` environment variable.

## Custom File

If you want to provide your own configuration file, you can provide it through
the `--config-file` CLI argument. If the given argument is a URL, PyFunceble
will download it and use it as the configuration file.


!!! note

    The given configuration file will be loaded **after** the default
    configuration file _(`.PyFunceble.yaml`)_ and **before** the overwrite _(`.PyFunceble.overwrite.yaml`)_ configuration file.

## Operating Systems

### Linux & MacOS

Under Linux or MacOS, PyFunceble will look for the following folders respectively.

1. `~/.config/PyFunceble`
2. `~/.PyFunceble`
3. `$PWD` _(current folder)_

The first matching and found folder will be used to install the initial configuration
or system files.

!!! note

    If the parent folder does not exist, it will try to look for the next possible
    location.

    However, if none is found, it will try to create the `~/.config/PyFunceble`
    folder. If the `~/.config` folder doesn't exists, it will try the next one
    until a viable folder is found.

!!! danger "Beware!!"

    Under some circumstances _(cf: under a CI/CD engine)_, the behavior may be different.

### Windows

Under Windows, PyFunceble will look for the following folders respectively.

1. `%APPDATA%\PyFunceble`
2. `%CD%`

The first matching and found folder will be used to initall the initial configuration
or system files.

!!! note

    If the parent folder does not exist, it will try to look for the next possible
    location.

    However, if none is found, it will try to create the `%APPDATA%\PyFunceble`
    folder. If the `%APPDATA%` folder doesn't exists, it will try the next one
    until a viable folder is found.

## CI / CD Engines

When runing under a CI/CD engine, PyFunceble mostly use the workspace folder a the current folder.

That means, that if you don't set the `PYFUNCEBLE_CONFIG_DIR` environment variable, the root folder of your repository will be used as the configuration folder.


## Edge Cases


### Cloned Repository

If you cloned the [PyFunceble](https://github.com/funilrys/PyFunceble) repository,
and you are trying to run a test from the root folder, PyFunceble will consider
the repository's root folder as its configuration directory.

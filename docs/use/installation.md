# Installation

PyFunceble is distributed through 2 packages that reflects our 2 main development and
deployment branches. Both packages are stable but with 2 different phylosophies.
Therefore, the choice is up to you.


The 2 packages are `pyfunceble` and `pyfunceble-dev`.

If you want a **stable** but **mature**, and **slowly** updating package, you
should install the `pyfunceble` package.
It reflects the `master` branch which only get updated once the new features and
bugfixes of `pyfunceble-dev` are tested long enough to be considered mature.

On the other hand, if you want a **stable** but **fast** updating package, you
should install the `pyfunceble-dev` package.
It reflects the `dev` branch which get updated frequently to allow the community to
provide feedbacks as soon as possible.

**Recommendation:**
For most people the `pyfunceble` package should be sufficient. But if you want to help
the community or always want to have the latest features and bugfix as soon as possible,
you should prefer the `pyfunceble-dev` package.

## Overview: Installation Method

| OS        | Technology                  | Tools        | Link                               |
| --------- | --------------------------- | ------------ | ---------------------------------- |
| Any       | PyPi - Python Package Index | `pip3`       | [Link](#pypi-python-package-index) |
| Any       | Container Image Registry    | `docker`     | [Link](#container-image-registry)  |
| Any       | Git                         | `pip3`       | [Link](#git-repository)            |
| Any       | Zip File                    | `pip3`       | [Link](#from-source)               |
| ArchLinux | AUR Helper                  | `aur-helper` | [Link](#arch-linux)                |

## PyPi - Python Package Index

Installing from the Python Package Index is for most people the prefered one - after
the OS specific packages _(see below)_.

Here is an overview of the packages and where they are hosted.

| Package        | PyPi Link                                                                       |
| -------------- | ------------------------------------------------------------------------------- |
| pyfunceble     | [https://pypi.org/project/PyFunceble](https://pypi.org/project/PyFunceble)      |
| pyfunceble-dev | [https://pypi.org/project/PyFunceblee-dev](https://pypi.org/project/PyFunceble) |

!!! danger "Beware!!"

    We recommend the usage of the `--user` flag as it installs the required
    dependencies at the user level. The main reason behind that is to avoid
    crashes or clashes between you OS package manager and `pip3`.

    However, if you:

    - are aware of the possible consequences
    - are running PyFunceble within a CI engine or in an automated environment

    you shouldn't use it.


### Optional Dependencies

The following dependencies are optional and can be installed if you need them.

| Dependency                         | Description                                                                                                                                                            |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `all`                              | Install all functional dependencies. Basically all but `dev`, `test` and `docs`. _When a binary and non binary version is available, the binary version is installed._ |
| `full`                             | Install all dependencies listed below. _When a binary and non binary version is available, the binary version is installed._                                           |
| `psql`, `postgresql`               | **Build** and install the dependencies required to interact with PostgreSQL.                                                                                           |
| `psql-binary`, `postgresql-binary` | **Install** the dependencies required to interact with PostgreSQL - from binary.                                                                                       |
| `docs`                             | Install the dependencies required to build the documentation.                                                                                                          |
| `test`                             | Install the dependencies required to run the tests.                                                                                                                    |
| `dev`                              | Install the dependencies required to develop PyFunceble.                                                                                                               |

They are intended to be installed through the following syntax:

```shell
pip3 install --user {pkg}[{dependency}]
```

As an example if you want to install the `docs` and `test` dependencies, you should run:

```shell
pip3 install --user pyfunceble[docs,test]
```

### pyfunceble

You can install the **pyfunceble** through `pip3`:

```shell
pip3 install --user pyfunceble
```

### pyfunceble-dev

You can install the  **pyfunceble-dev** package through `pip3`:

```shell
pip3 install --user pyfunceble-dev
```

If you want to help and use the unstable pre-releases, you should install with
the `--pre` argument.

```shell
pip3 install --user --pre pyfunceble-dev
```

## Container Image Registry

Installing from a Container Image Registry is the way to go if you are in a
hurry or always want the best from the beat without having to look if an update
is available. :smile:

Here is an overview of the packages and where they are hosted.

| Host       | Package        | Link                                                                                                     |
| ---------- | -------------- | -------------------------------------------------------------------------------------------------------- |
| Docker Hub | pyfunceble     | [https://hub.docker.com/r/pyfunceble/pyfunceble](https://hub.docker.com/r/pyfunceble/pyfunceble)         |
| Docker Hub | pyfunceble-dev | [https://hub.docker.com/r/pyfunceble/pyfunceble-dev](https://hub.docker.com/r/pyfunceble/pyfunceble-dev) |

### pyfunceble

#### Docker Hub

You can install the **pyfunceble** image from Docker Hub through `docker`:

```shell
docker pull pyfunceble/pyfunceble
```

### pyfunceble-dev

#### Docker Hub

You can install the **pyfunceble-dev** image from Docker Hub through `docker`:

```shell
docker pull pyfunceble/pyfunceble-dev
```

## Arch Linux

Installing from the ArchLinux User Repository is the way to go if you are using
ArchLinux.

Here is an overview of the packages and where they are hosted.

| Package        | AUR Link                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| pyfunceble     | [https://aur.archlinux.org/packages/pyfunceble](https://aur.archlinux.org/packages/pyfunceble)         |
| pyfunceble-dev | [https://aur.archlinux.org/packages/pyfunceble-dev](https://aur.archlinux.org/packages/pyfunceble-dev) |

### pyfunceble

#### AUR Helper

You can install the **pyfunceble** package through your favorite AUR helper:

```shell
aur-helper -S pyfunceble
```

#### Manually

You can install the **pyfunceble** package manually through the following:

```shell
git clone https://aur.archlinux.org/pyfunceble.git pyfunceble
cd pyfunceble
makepkg -fsri
```

### pyfunceble-dev

#### AUR Helper

You can install the **pyfunceble-dev** package through your favorite AUR helper:

```shell
aur-helper -S pyfunceble-dev
```

#### Manually

You can install the **pyfunceble** package manually through the following:

```shell
git clone https://aur.archlinux.org/pyfunceble-dev.git pyfunceble-dev
cd pyfunceble-dev
makepkg -fsri
```

## Git Repository

Installing from a Git Repository with `pip3` is not recommended for general user as
you will easily get the latest development patches even before they get published. But if you
are one of those who always want to be in sync with the latest development patches,
this is probably for you.

Here is an overview of the packages and where they are hosted.

| Host   | Package        | Repository                                                              |
| ------ | -------------- | ----------------------------------------------------------------------- |
| GitHub | pyfunceble     | `git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble`  |
| GitHub | pyfunceble-dev | `git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble-dev` |
| GitLab | pyfunceble     | `git+https://gitlab.com/funilrys/PyFunceble.git@master#egg=PyFunceble`  |
| GitLab | pyfunceble-dev | `git+https://gitlab.com/funilrys/PyFunceble.git@dev#egg=PyFunceble-dev` |

!!! danger "Beware!!"

    We recommend the usage of the `--user` flag as it installs the required
    dependencies at the user level. The main reason behind that is to avoid
    crashes or clashes between you OS package manager and `pip3`.

    However, if you:

    - are aware of the possible consequences
    - are running PyFunceble within a CI engine or in an automated environment

    you shouldn't use it.

### pyfunceble

#### GitHub

You can install the **pyfunceble** package from GitHub through `pip3`:

```shell
pip3 install --user git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble
```

#### GitLab

You can install the **pyfunceble** package from GitLab through `pip3`:

```shell
pip3 install --user git+https://gitlab.com/funilrys/PyFunceble.git@master#egg=PyFunceble
```

### pyfunceble-dev

#### GitHub

You can install the **pyfunceble-dev** package from GitHub through `pip3`:

```shell
pip3 install --user git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble-dev
```

#### GitLab

You can install the **pyfunceble-dev** package from GitLab through `pip3`:

```shell
pip3 install --user git+https://gitlab.com/funilrys/PyFunceble.git@dev#egg=PyFunceble-dev
```

## From Source

Installing from source is not recommended at all as you may need to keep the repository
up-to-date by yourself.

Here is an overview of the packages and where they are hosted.

| Host   | Package        | Branch   | Repository                                                                                               |
| ------ | -------------- | -------- | -------------------------------------------------------------------------------------------------------- |
| GitHub | pyfunceble     | `master` | [https://github.com/funilrys/PyFunceble/tree/master](https://github.com/funilrys/PyFunceble/tree/master) |
| GitHub | pyfunceble-dev | `dev`    | [https://github.com/funilrys/PyFunceble/tree/dev](https://github.com/funilrys/PyFunceble/tree/dev)       |
| GitLab | pyfunceble     | `master` | [https://gitlab.com/funilrys/PyFunceble/tree/master](https://gitlab.com/funilrys/PyFunceble/tree/master) |
| GitLab | pyfunceble-dev | `dev`    | [https://gitlab.com/funilrys/PyFunceble/tree/master](https://gitlab.com/funilrys/PyFunceble/tree/master) |

You can install the package from source through `pip3`:

```shell
# From Github
pip3 install --upgrade --user https://github.com/funilrys/PyFunceble/archive/{{branch}}.zip

# From GitLab
pip3 install --upgrade --user https://gitlab.com/funilrys/PyFunceble/-/archive/{{branch}}/PyFunceble-{{branch}}.zip
```
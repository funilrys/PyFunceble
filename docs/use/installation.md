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


## PyPi - Python Package Index

Installing from the Python Package Index is for most people the prefered one - after
the OS specific packages _(see below)_.

Here is an overview of the packages and where they are hosted.

| Package        | PyPi Link                                                                       |
|----------------|---------------------------------------------------------------------------------|
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
|------------|----------------|----------------------------------------------------------------------------------------------------------|
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
|----------------|--------------------------------------------------------------------------------------------------------|
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
curl https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=pyfunceble -o PKGBUILD
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
curl https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=pyfunceble-dev -o PKGBUILD
makepkg -fsri
```

## Git Repository

Installing from a Git Repository with `pip3` is not recommended for general user as
you will get the latest development patches even before they get published. But if you
are one of those who always want to be in sync with the latest development patches,
this is probably for you.

Here is an overview of the packages and where they are hosted.

| Host   | Package        | Repository                                                              |
|--------|----------------|-------------------------------------------------------------------------|
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

| Host   | Package        | Repository                                                              |
|--------|----------------|------------------------------------------------------------------------------------------------------------|
| GitHub | pyfunceble     | [https://github.com/funilrys/PyFunceble/tree/master](https://github.com/funilrys/PyFunceble/tree/master)  |
| GitHub | pyfunceble-dev | [https://github.com/funilrys/PyFunceble/tree/dev](https://github.com/funilrys/PyFunceble/tree/dev)        |
| GitLab | pyfunceble     | [https://gitlab.com/funilrys/PyFunceble/tree/master](https://gitlab.com/funilrys/PyFunceble/tree/master)  |
| GitLab | pyfunceble-dev | [https://gitlab.com/funilrys/PyFunceble/tree/master](https://gitlab.com/funilrys/PyFunceble/tree/master) |

You can install the package from source through `pip3`:

```shell
cd /path/to/source
git checkout dev|master # switch to desired branch - if source is a git repo
pip3 install --user .
```

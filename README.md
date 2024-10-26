![image](https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png)

# The tool to check the availability or syntax of domain, IP or URL

[![image](https://img.shields.io/badge/code%20style-black-000000.png)](https://github.com/ambv/black)
[![image](https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev)](https://coveralls.io/github/funilrys/PyFunceble?branch=dev)
[![image](https://img.shields.io/github/license/funilrys/PyFunceble.png)](https://github.com/funilrys/PyFunceble/blob/dev/LICENSE)
[![image](https://img.shields.io/pypi/v/pyfunceble-dev.png)](https://pypi.org/project/pyfunceble-dev)
[![image](https://img.shields.io/github/issues/funilrys/PyFunceble.png)](https://github.com/funilrys/PyFunceble/issues)

[![image](https://static.pepy.tech/badge/pyfunceble-dev)](https://pepy.tech/project/pyfunceble-dev)
[![image](https://static.pepy.tech/badge/pyfunceble-dev/month)](https://pepy.tech/project/pyfunceble-dev)
[![image](https://static.pepy.tech/badge/pyfunceble-dev/week)](https://pepy.tech/project/pyfunceble-dev)

**PyFunceble** aims to provide an accurate availability check through
the usage of multiple sources which are for example - to only list a
few:

- the WHOIS record(s).
- the DNS record(s).
- the HTTP status code.

PyFunceble can be included in your existing project through:

- its standard built-in CLI implementation.
- its [Python
  API](https://docs.pyfunceble.com/develop/getting-started.html).
- the [PyFunceble
  web-worker](https://github.com/pyfunceble/web-worker) project that
  provides the core functionalities of PyFunceble behind a web API.

The PyFunceble CLI can test from a hosts file, a plain list of subjects,
an AdBlock filter list or even an RPZ record.

As of today, PyFunceble is running actively - if not daily - within
several servers, laptops, PCs, and Raspberry Pis. It is even used -
thanks to our auto continue mechanism - with CI engines like GitHub
Action, Travis CI, or GitLab CI.

Happy testing with PyFunceble!

[![image](https://github.com/PyFunceble/gifs/raw/master/repo-showcase.gif)](https://github.com/PyFunceble/gifs/raw/master/repo-showcase.gif)

# Table of Content

- [Installation](#installation)
  - [Packages \& Versioning](#packages--versioning)
  - [PyPi - Python Package Index](#pypi---python-package-index)
    - [Optional Dependencies](#optional-dependencies)
    - [pyfunceble](#pyfunceble)
    - [pyfunceble-dev](#pyfunceble-dev)
  - [Container Image Registry](#container-image-registry)
    - [pyfunceble](#pyfunceble-1)
      - [Docker Hub](#docker-hub)
    - [pyfunceble-dev](#pyfunceble-dev-1)
      - [Docker Hub](#docker-hub-1)
  - [ArchLinux](#archlinux)
  - [Git Repository](#git-repository)
    - [pyfunceble](#pyfunceble-2)
      - [GitHub](#github)
      - [GitLab](#gitlab)
    - [pyfunceble-dev](#pyfunceble-dev-2)
      - [GitHub](#github-1)
      - [GitLab](#gitlab-1)
  - [From Source](#from-source)
- [Usage](#usage)
  - [Common Setups](#common-setups)
  - [Container Image Setups](#container-image-setups)
    - [Data Persitence](#data-persitence)
  - [Common Examples](#common-examples)
- [Documentation as the place to be!](#documentation-as-the-place-to-be)
- [Supporting the project](#supporting-the-project)
- [Contributors](#contributors)
- [Special Thanks](#special-thanks)
- [License](#license)


# Installation

## Packages & Versioning

This project follows the semver standard.

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

| Package        | PyPi Link                                |
| -------------- | ---------------------------------------- |
| pyfunceble     | https://pypi.org/project/PyFunceble      |
| pyfunceble-dev | https://pypi.org/project/PyFunceblee-dev |

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

## ArchLinux

For the **`pyfunceble`** package:

```shell
aur-helper -S pyfunceble
pyfunceble --version
```

For the **`pyfunceble-dev`** package:

```shell
aur-helper -S pyfunceble-dev
pyfunceble --version
```

## Git Repository

Installing from a Git Repository with `pip3` is not recommended for general user as
you will get the latest development patches even before they get published. But if you
are one of those who always want to be in sync with the latest development patches,
this is probably for you.

Here is an overview of the packages and where they are hosted.

| Host   | Package        | Repository                                                              |
| ------ | -------------- | ----------------------------------------------------------------------- |
| GitHub | pyfunceble     | `git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble`  |
| GitHub | pyfunceble-dev | `git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble-dev` |
| GitLab | pyfunceble     | `git+https://gitlab.com/funilrys/PyFunceble.git@master#egg=PyFunceble`  |
| GitLab | pyfunceble-dev | `git+https://gitlab.com/funilrys/PyFunceble.git@dev#egg=PyFunceble-dev` |

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
pip3 install --user https://github.com/funilrys/PyFunceble/archive/{{branch}}.zip # From Github
pip3 install --user https://gitlab.com/funilrys/PyFunceble/-/archive/{{branch}}/PyFunceble-{{branch}}.zip # From GitLab
```

# Usage

## Common Setups

If you installed PyFunceble through any other method that doesn't involve a container image, you can use PyFunceble "normally" through the `pyfunceble` executable.

```sh
pyfunceble --help
```


## Container Image Setups


If you installed PyFunceble through the container image registry method, you can run pyfunceble through:

```sh
docker run -it pyfunceble/pyfunceble[-dev] --help
```

**Beware:** if the first parameter starts with a slash (`/`), the entrypoint will assume that you want to run a command within the container.

### Data Persitence

If you wish to persist your data, you simply have to mount a volume to the `/home/pyfunceble` directory.

Example:

```sh
mkdir -p pyf-data
echo "example.com" > pyf-data/test.list

docker run -v pyf-data:/home/pyfunceble -it pyfunceble/pyfunceble[-dev] -f /home/pyf-data/test.list
```


## Common Examples

Here are some examples to get started.

Check the availability of 'example.com'.

    $ pyfunceble -d example.com

Check the availability of 'example.com' with a simple (stdout) output.

    $ pyfunceble -s -d example.com

Check the availability of 'example.com' with extended (stdout) output.

    $ pyfunceble -a -d example.com

Check the availability of 'example.com' and 'example.org'.

    $ pyfunceble -d example.com example.org

Check the availability of 'https://example.com'.

    $ pyfunceble -u https://example.com

Check the availability of 'https://example.com' and 'https://example.org'.

    $ pyfunceble -u https://example.com https://example.com

Check the syntax of 'example.com'.

    $ pyfunceble --syntax -d example.com

Check the reputation of 'example.com'.

    $ pyfunceble --reputation -d example.com

Check the availability of all subjects in the 'myhosts' file.

    $ pyfunceble -f myhosts

Check the availability of all subjects in the 'myhosts' and 'yourhosts' files.

    $ pyfunceble -f myhosts yourhosts

Check the availability of all (decoded) subject of the adblock filter list 'myadblock'.

    $ pyfunceble --adblock -f myadblock

# Documentation as the place to be!

Want to know more about details **PyFunceble**? I invite you to read the
documentation at [docs.pyfunceble.com](https://docs.pyfunceble.com)!

Want a local copy? I get you covered!

If you want to run the documentation locally, you can do so by following the
instructions below.

Through Docker:

```shell
docker run -it -p 8080:80 pyfunceble/docs
# Open Documentation with browser: http://localhost:8080
palemoon http://127.0.0.1:8000
```

From source:

```shell
# Install dependencies.
pip install --user .[docs]
# Serve documentation locally.
mkdocs serve
# Open Documentation with browser.
palemoon http://127.0.0.1:8000
```

**NOTE:** You are also invited to submit changes and improvement to the
documentation through a new Pull Request.

# Supporting the project

[PyFunceble](https://github.com/funilrys/PyFunceble),
[Dead-Hosts](https://github.com/dead-hosts), [adblock-decoder](https://github.com/pyunceble/adblock-decoder)
and all other analog projects are powered by free time and a lot of coffee!

This project helps you and you have to possibility to help back financially?
Sponsor [@funilrys](https://github.com/funilrys) through the GitHub Sponsor
program by clicking the image below!

[![image](https://github.blog/de/wp-content/uploads/sites/3/2019/05/mona-heart-featured.png?w=200)](https://github.com/sponsors/funilrys)

# Contributors

Thanks to those awesome peoples for their awesome and crazy idea(s),
contribution(s) and or issue report which made or make
[PyFunceble](https://github.com/funilrys/PyFunceble) a better tool.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://github.com/AvinashReddy3108"><img src="https://avatars.githubusercontent.com/u/27774996?v=4?s=100" width="100px;" alt="Avinash Reddy"/><br /><sub><b>Avinash Reddy</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AAvinashReddy3108" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/bigdargon"><img src="https://avatars.githubusercontent.com/u/10969626?v=4?s=100" width="100px;" alt="BigDargon"/><br /><sub><b>BigDargon</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Abigdargon" title="Bug reports">🐛</a> <a href="#ideas-bigdargon" title="Ideas, Planning, & Feedback">🤔</a> <a href="#question-bigdargon" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/pulls?q=is%3Apr+reviewed-by%3Abigdargon" title="Reviewed Pull Requests">👀</a> <a href="#data-bigdargon" title="Data">🔣</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=bigdargon" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="http://www.fanboy.co.nz/"><img src="https://avatars.githubusercontent.com/u/1659004?v=4?s=100" width="100px;" alt="Fanboynz"/><br /><sub><b>Fanboynz</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Aryanbr" title="Bug reports">🐛</a> <a href="#ideas-ryanbr" title="Ideas, Planning, & Feedback">🤔</a> <a href="#financial-ryanbr" title="Financial">💵</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=ryanbr" title="Tests">⚠️</a> <a href="#userTesting-ryanbr" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/veracioux"><img src="https://avatars.githubusercontent.com/u/29044423?v=4?s=100" width="100px;" alt="Haris Gušić"/><br /><sub><b>Haris Gušić</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/commits?author=veracioux" title="Documentation">📖</a> <a href="#a11y-veracioux" title="Accessibility">️️️️♿️</a> <a href="#tool-veracioux" title="Tools">🔧</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=veracioux" title="Tests">⚠️</a> <a href="#video-veracioux" title="Videos">📹</a> <a href="#tutorial-veracioux" title="Tutorials">✅</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=veracioux" title="Code">💻</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/DandelionSprout"><img src="https://avatars.githubusercontent.com/u/22780683?v=4?s=100" width="100px;" alt="Imre Eilertsen"/><br /><sub><b>Imre Eilertsen</b></sub></a><br /><a href="#a11y-DandelionSprout" title="Accessibility">️️️️♿️</a> <a href="https://github.com/funilrys/PyFunceble/issues?q=author%3ADandelionSprout" title="Bug reports">🐛</a> <a href="#data-DandelionSprout" title="Data">🔣</a> <a href="#example-DandelionSprout" title="Examples">💡</a> <a href="#financial-DandelionSprout" title="Financial">💵</a> <a href="#ideas-DandelionSprout" title="Ideas, Planning, & Feedback">🤔</a> <a href="#promotion-DandelionSprout" title="Promotion">📣</a> <a href="#question-DandelionSprout" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/pulls?q=is%3Apr+reviewed-by%3ADandelionSprout" title="Reviewed Pull Requests">👀</a> <a href="#tool-DandelionSprout" title="Tools">🔧</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=DandelionSprout" title="Tests">⚠️</a> <a href="#userTesting-DandelionSprout" title="User Testing">📓</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://github.com/kowith337"><img src="https://avatars.githubusercontent.com/u/16535467?v=4?s=100" width="100px;" alt="Kowith Singkornkeeree"/><br /><sub><b>Kowith Singkornkeeree</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Akowith337" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="20%"><a href="https://ubuntu101.co.za/"><img src="https://avatars.githubusercontent.com/u/9961541?v=4?s=100" width="100px;" alt="Mitchell Krog"/><br /><sub><b>Mitchell Krog</b></sub></a><br /><a href="#a11y-mitchellkrogza" title="Accessibility">️️️️♿️</a> <a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Amitchellkrogza" title="Bug reports">🐛</a> <a href="#blog-mitchellkrogza" title="Blogposts">📝</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=mitchellkrogza" title="Code">💻</a> <a href="#content-mitchellkrogza" title="Content">🖋</a> <a href="#data-mitchellkrogza" title="Data">🔣</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=mitchellkrogza" title="Documentation">📖</a> <a href="#design-mitchellkrogza" title="Design">🎨</a> <a href="#example-mitchellkrogza" title="Examples">💡</a> <a href="#fundingFinding-mitchellkrogza" title="Funding Finding">🔍</a> <a href="#ideas-mitchellkrogza" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-mitchellkrogza" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#mentoring-mitchellkrogza" title="Mentoring">🧑‍🏫</a> <a href="#platform-mitchellkrogza" title="Packaging/porting to new platform">📦</a> <a href="#plugin-mitchellkrogza" title="Plugin/utility libraries">🔌</a> <a href="#promotion-mitchellkrogza" title="Promotion">📣</a> <a href="#question-mitchellkrogza" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/pulls?q=is%3Apr+reviewed-by%3Amitchellkrogza" title="Reviewed Pull Requests">👀</a> <a href="#tool-mitchellkrogza" title="Tools">🔧</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=mitchellkrogza" title="Tests">⚠️</a> <a href="#tutorial-mitchellkrogza" title="Tutorials">✅</a> <a href="#talk-mitchellkrogza" title="Talks">📢</a> <a href="#userTesting-mitchellkrogza" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/Nilsonfsilva"><img src="https://avatars.githubusercontent.com/u/91392383?v=4?s=100" width="100px;" alt="Nilsonfsilva"/><br /><sub><b>Nilsonfsilva</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3ANilsonfsilva" title="Bug reports">🐛</a> <a href="#infra-Nilsonfsilva" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#platform-Nilsonfsilva" title="Packaging/porting to new platform">📦</a> <a href="#tool-Nilsonfsilva" title="Tools">🔧</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=Nilsonfsilva" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/Odyseus"><img src="https://avatars.githubusercontent.com/u/3822556?v=4?s=100" width="100px;" alt="Odyseus"/><br /><sub><b>Odyseus</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AOdyseus" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=Odyseus" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/ybreza"><img src="https://avatars.githubusercontent.com/u/35470865?v=4?s=100" width="100px;" alt="Reza Rizqullah"/><br /><sub><b>Reza Rizqullah</b></sub></a><br /><a href="#design-ybreza" title="Design">🎨</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=ybreza" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://github.com/techdragon"><img src="https://avatars.githubusercontent.com/u/2115079?v=4?s=100" width="100px;" alt="Samuel Bishop"/><br /><sub><b>Samuel Bishop</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Atechdragon" title="Bug reports">🐛</a> <a href="#ideas-techdragon" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="20%"><a href="https://scripttiger.github.io/"><img src="https://avatars.githubusercontent.com/u/29940916?v=4?s=100" width="100px;" alt="ScriptTiger"/><br /><sub><b>ScriptTiger</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AScriptTiger" title="Bug reports">🐛</a> <a href="#ideas-ScriptTiger" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=ScriptTiger" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/sjhgvr"><img src="https://avatars.githubusercontent.com/u/51121527?v=4?s=100" width="100px;" alt="Stephan van Ruth"/><br /><sub><b>Stephan van Ruth</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Asjhgvr" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=sjhgvr" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="http://stevenblack.com/"><img src="https://avatars.githubusercontent.com/u/80144?v=4?s=100" width="100px;" alt="Steven Black"/><br /><sub><b>Steven Black</b></sub></a><br /><a href="#ideas-StevenBlack" title="Ideas, Planning, & Feedback">🤔</a> <a href="#financial-StevenBlack" title="Financial">💵</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/T145"><img src="https://avatars.githubusercontent.com/u/1214129?v=4?s=100" width="100px;" alt="T145"/><br /><sub><b>T145</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AT145" title="Bug reports">🐛</a> <a href="#ideas-T145" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://infosec.exchange/@wally3k"><img src="https://avatars.githubusercontent.com/u/3049142?v=4?s=100" width="100px;" alt="WaLLy3K"/><br /><sub><b>WaLLy3K</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AWaLLy3K" title="Bug reports">🐛</a> <a href="#ideas-WaLLy3K" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/Yuki2718"><img src="https://avatars.githubusercontent.com/u/58900598?v=4?s=100" width="100px;" alt="Yuki2718"/><br /><sub><b>Yuki2718</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AYuki2718" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=Yuki2718" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/Zachinquarantine"><img src="https://avatars.githubusercontent.com/u/69423184?v=4?s=100" width="100px;" alt="Zachinquarantine"/><br /><sub><b>Zachinquarantine</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/commits?author=Zachinquarantine" title="Code">💻</a></td>
      <td align="center" valign="top" width="20%"><a href="http://bit.ly/cBWeb"><img src="https://avatars.githubusercontent.com/u/28985171?v=4?s=100" width="100px;" alt="ZeroDot1"/><br /><sub><b>ZeroDot1</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AZeroDot1" title="Bug reports">🐛</a> <a href="#ideas-ZeroDot1" title="Ideas, Planning, & Feedback">🤔</a> <a href="#question-ZeroDot1" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=ZeroDot1" title="Tests">⚠️</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=ZeroDot1" title="Code">💻</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/avatartw"><img src="https://avatars.githubusercontent.com/u/69660730?v=4?s=100" width="100px;" alt="avatartw"/><br /><sub><b>avatartw</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Aavatartw" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://github.com/dnmTX"><img src="https://avatars.githubusercontent.com/u/34774426?v=4?s=100" width="100px;" alt="dnmTX"/><br /><sub><b>dnmTX</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3AdnmTX" title="Bug reports">🐛</a> <a href="#ideas-dnmTX" title="Ideas, Planning, & Feedback">🤔</a> <a href="#question-dnmTX" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/pulls?q=is%3Apr+reviewed-by%3AdnmTX" title="Reviewed Pull Requests">👀</a> <a href="#data-dnmTX" title="Data">🔣</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=dnmTX" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/gwarser"><img src="https://avatars.githubusercontent.com/u/886325?v=4?s=100" width="100px;" alt="gwarser"/><br /><sub><b>gwarser</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Agwarser" title="Bug reports">🐛</a> <a href="#data-gwarser" title="Data">🔣</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=gwarser" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/hawkeye116477"><img src="https://avatars.githubusercontent.com/u/19818572?v=4?s=100" width="100px;" alt="hawkeye116477"/><br /><sub><b>hawkeye116477</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Ahawkeye116477" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/jawz101"><img src="https://avatars.githubusercontent.com/u/14151703?v=4?s=100" width="100px;" alt="jawz101"/><br /><sub><b>jawz101</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Ajawz101" title="Bug reports">🐛</a> <a href="#ideas-jawz101" title="Ideas, Planning, & Feedback">🤔</a> <a href="#question-jawz101" title="Answering Questions">💬</a> <a href="#data-jawz101" title="Data">🔣</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/keczuppp"><img src="https://avatars.githubusercontent.com/u/74409207?v=4?s=100" width="100px;" alt="keczuppp"/><br /><sub><b>keczuppp</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Akeczuppp" title="Bug reports">🐛</a> <a href="#ideas-keczuppp" title="Ideas, Planning, & Feedback">🤔</a> <a href="#question-keczuppp" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=keczuppp" title="Tests">⚠️</a> <a href="#data-keczuppp" title="Data">🔣</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://github.com/opav"><img src="https://avatars.githubusercontent.com/u/6770347?v=4?s=100" width="100px;" alt="opav"/><br /><sub><b>opav</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Aopav" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=opav" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/rusty-snake"><img src="https://avatars.githubusercontent.com/u/41237666?v=4?s=100" width="100px;" alt="rusty-snake"/><br /><sub><b>rusty-snake</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Arusty-snake" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=rusty-snake" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/smed79"><img src="https://avatars.githubusercontent.com/u/1873139?v=4?s=100" width="100px;" alt="smed79"/><br /><sub><b>smed79</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Asmed79" title="Bug reports">🐛</a> <a href="#ideas-smed79" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=smed79" title="Code">💻</a> <a href="#question-smed79" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=smed79" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://speedmann.de/"><img src="https://avatars.githubusercontent.com/u/424659?v=4?s=100" width="100px;" alt="speedmann"/><br /><sub><b>speedmann</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Aspeedmann" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=speedmann" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="20%"><a href="https://www.mypdns.org/"><img src="https://avatars.githubusercontent.com/u/44526987?v=4?s=100" width="100px;" alt="spirillen"/><br /><sub><b>spirillen</b></sub></a><br /><a href="#a11y-spirillen" title="Accessibility">️️️️♿️</a> <a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Aspirillen" title="Bug reports">🐛</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=spirillen" title="Code">💻</a> <a href="#content-spirillen" title="Content">🖋</a> <a href="#data-spirillen" title="Data">🔣</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=spirillen" title="Documentation">📖</a> <a href="#example-spirillen" title="Examples">💡</a> <a href="#ideas-spirillen" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-spirillen" title="Maintenance">🚧</a> <a href="#mentoring-spirillen" title="Mentoring">🧑‍🏫</a> <a href="#promotion-spirillen" title="Promotion">📣</a> <a href="#question-spirillen" title="Answering Questions">💬</a> <a href="https://github.com/funilrys/PyFunceble/pulls?q=is%3Apr+reviewed-by%3Aspirillen" title="Reviewed Pull Requests">👀</a> <a href="#tool-spirillen" title="Tools">🔧</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=spirillen" title="Tests">⚠️</a> <a href="#tutorial-spirillen" title="Tutorials">✅</a> <a href="#talk-spirillen" title="Talks">📢</a> <a href="#userTesting-spirillen" title="User Testing">📓</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="20%"><a href="https://github.com/NeolithEra"><img src="https://avatars.githubusercontent.com/u/52778917?v=4?s=100" width="100px;" alt="watchman-pypi"/><br /><sub><b>watchman-pypi</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3ANeolithEra" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="20%"><a href="https://github.com/xxcriticxx"><img src="https://avatars.githubusercontent.com/u/15007183?v=4?s=100" width="100px;" alt="xxcriticxx"/><br /><sub><b>xxcriticxx</b></sub></a><br /><a href="https://github.com/funilrys/PyFunceble/issues?q=author%3Axxcriticxx" title="Bug reports">🐛</a> <a href="#ideas-xxcriticxx" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/funilrys/PyFunceble/commits?author=xxcriticxx" title="Tests">⚠️</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->


# Special Thanks

Thanks to those awesome organization(s), tool(s) and or people(s) for

- Their awesome documentation
- Their awesome repository
- Their awesome tool/software/source code
- Their breaking reports
- Their contributions
- Their current work/purpose
- Their promotion of Py-Funceble
- Their support
- Their testings reports

which helped and/or still help me build, test and or make
[PyFunceble](https://github.com/funilrys/PyFunceble) a better tool.

- Adam Warner - [@PromoFaux](https://github.com/PromoFaux)
- Adblock Plus - [@adblockplus](https://github.com/adblockplus)
- asciinema - [@asciinema](https://github.com/asciinema)
- Bob Halley - [@rthalley](https://github.com/rthalley)
  ([DNSPython](https://github.com/rthalley/dnspython))
- Chris Griffith - [@cdgriffith](https://github.com/cdgriffith)
  ([Box](https://github.com/cdgriffith/Box))
- Daniel - [@dnmTX](https://github.com/dnmTX)
- Jonathan Hartley - [@tartley](https://github.com/tartley)
  ([colorama](https://github.com/tartley/colorama))
- [IANA](https://www.iana.org/) - [ICANN](https://www.icann.org/)
  ([Root Zone Database](https://www.iana.org/domains/root/db))
- [Iterative](https://github.com/iterative)
  ([shtab](https://github.com/iterative/shtab))
- Kenneth Reitz - [@kennethreitz](https://github.com/kennethreitz)
  ([requests](https://github.com/kennethreitz/requests))
- Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
- Mohammad Fares - [@faressoft](https://github.com/faressoft)
  ([Terminalizer](https://github.com/faressoft/terminalizer))
- Pi-Hole - [@pi-hole](https://github.com/pi-hole/pi-hole)
- Public Suffix List -
  [@publicsuffix](https://github.com/publicsuffix)
- Reza Rizqullah - [@ybreza](https://github.com/ybreza)
- Saurabh Kumar - [@theskumar](https://github.com/theskumar)
  ([python-dotenv](https://github.com/theskumar/python-dotenv))
- ScriptTiger - [@ScriptTiger](https://github.com/ScriptTiger)
- SMed79 - [@SMed79](https://github.com/SMed79)
- spirillen - [@spirillen](https://www.mypdns.org/p/Spirillen/)
- The YAML Project - [@yaml](https://github.com/yaml)
  ([pyyaml](https://github.com/yaml/pyyaml))
- [yWorks](https://www.yworks.com) - ([yEd Graph
  Editor](https://www.yworks.com/products/yed))

# License

    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

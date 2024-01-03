# Getting started

If you feel that something is missing, feel free to submit an issue or edit this
page on GitHub.

## The basics

Before starting to play with PyFunceble, the first recommended action is to
read the version to be sure that everything is expected to work as it should.

To do that simple execute:

```shell
pyfunceble --version
```

<script async id="asciicast-SNpIyoVueCt9IIHO8xbXbmfzT" src="https://asciinema.org/a/SNpIyoVueCt9IIHO8xbXbmfzT.js"></script>

### Testing modes

PyFunceble provides 3 testing modes, that you can't use in parallel. You must
choose one of the provided testing modes in order for PyFunceble to produce outputs.

| Test Mode    | Description                                                                                                                                | Argument       | Configuration Parameter                 |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------- | --------------------------------------- |
| Availability | This is the default mode.<br>It exists to help us find the availability / reachability of subjects.                                        | None, Default  | `cli_testing.testing_mode.availability` |
| Syntax       | This is the mode that exclusively check whether the inputed subjects are VALID or INVALID.                                                 | `--syntax`     | `cli_testing.testing_mode.syntax`       |
| Reputation   | This is the mode that exclusively check whether the inputed subjects have a bad reputation by checking against the OTX IP reputation list. | `--reputation` | `cli_testing.testing_mode.reputation`   |

### Input Sources

PyFunceble expects you to provide the information needed for launching tests.
Therefore, it is important that you understand the different way to input
tests subjects into PyFunceble.

PyFunceble has 2 _(direct)_ ways to directly get inputs from operators:

1. Inline: You manually type what you want to be tested.
2. Files: You give PyFunceble a path to the file that you want to be decoded and tested.

#### Inline: The Quick Way!

The "inline" input, describes the process of manually listing the subjects PyFunceble
has to test. This can be done through the following arguments:

| Argument         | Multiple Possible | Example                                                       | Description                              |
| ---------------- | ----------------- | ------------------------------------------------------------- | ---------------------------------------- |
| `-d`, `--domain` | ✔️                | `-d example.com 192.0.43.7 github.com`                        | Inputs a list of domains or IPs to test. |
| `-u`, `--url`    | ✔️                | `-u https://example.com http://192.0.43.7 https://github.com` | Inputs a list of URLs to test.           |

#### File: The Managable Way!

The "files" input, describes the process of input a local or remote path to a file that
PyFunceble has to read _(or download)_, decode and test. This can be done through the following arguments:

| Argument             | Multiple Possible | Expected Input Format   | Example                                              | Description                                                                 |
| -------------------- | ----------------- | ----------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| `-f`, `--file`       | ✔️                | Hosts File / Plain Text | `-f ./domains.list https://example.org/my/blocklist` | Input a hosts file or plain text file that PyFunceble has to read and test. |
| `-uf`, `--url-files` | ✔️                | Plain Text              | `-uf ./urls.list https://example.org/my/urls.txt`    | Input a plain text file that PyFunceble has to read and test.               |

PyFunceble can decode multiple formats. You can influence the decoding mechanism by using ONE of the following arguments:

!!! warning

    Only one decoding method at a time is supported.

| Argument | Configuration Parameter | Description |
| ----------- | ----------------------- | ---------------------------------------------------------------------------- |
| `--adblock` | `cli_decoding.adblock` | Forces PyFunceble to assume that the inputed file is an AdBlock filter list. |
| `--rpz` | `cli_decoding.rpz` | Forces PyFunceble to assume that the inputed file is an RPZ formatted file. |

You can force PyFunceble to to some extra steps while decoding files - in order to test what you really want. This
can be done through the following arguments.

| Argument       | Configuration Parameter   | Description                                                                                           |
| -------------- | ------------------------- | ----------------------------------------------------------------------------------------------------- |
| `--aggressive` | `cli_decoding.aggressive` | Forces PyFunceble to try to decodes as much as possible - even if doesn't necessarly makes sense.      |
| `--wildcard`   | `cli_decoding.wildcard`   | Forces PyFunceble to remove the wildcards parts of subjects. Example: `*.example.org -> example.org`. |

You can also force PyFunceble to filter or generate new subjects to test.
This can be controlled through the following argument:

| Argument       | Configuration Parameter   | Description                                                                                                                                                        |
| -------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--complement` | `cli_testing.complements` | Forces PyFunceble to generate complements. <br>A complement of a domain is for example `www.example.org` when `example.org` is supplied - and vice-versa.          |
| `--filter`     | `cli_testing.file_filter` | Forces PyFunceble to only tests the matching subjects. Example `--filter "example.org$"` will force PyFunceble to only test subjects that ends with `example.org`. |

### Output Format

The PyFunceble CLI has 3 ways of displaying information to you.

The (default) output:

```sh
pyfunceble -d github.com
[...]
Subject                                                                                              Status      Source
---------------------------------------------------------------------------------------------------- ----------- ----------
github.com                                                                                           ACTIVE      WHOIS
```

<script async id="asciicast-jAmoOxJqhcTXfVatz98EDStnz" src="https://asciinema.org/a/jAmoOxJqhcTXfVatz98EDStnz.js"></script>

The complete output, that you can get through the `-a` or `--all` arguments:

```sh
pyfunceble -a -d github.com
[...]
Subject                                                                                              Status      Source     Expiration Date   Registrar                      HTTP Code  Checker
---------------------------------------------------------------------------------------------------- ----------- ---------- ----------------- ------------------------------ ---------- -------------
github.com                                                                                           ACTIVE      WHOIS      09-oct-2024       MarkMonitor Inc.               301        AVAILABILITY
```

<script async id="asciicast-bzAR5whEIsen7XkKSR1A6SqGL" src="https://asciinema.org/a/bzAR5whEIsen7XkKSR1A6SqGL.js"></script>

The simple output, that you can get through the `-s`or `--simple` arguments:

```sh
pyfunceble -s -d github.com
github.com ACTIVE
```

<script async id="asciicast-3GHKvuYVMN8RF1vmItWFZtphz" src="https://asciinema.org/a/3GHKvuYVMN8RF1vmItWFZtphz.js"></script>


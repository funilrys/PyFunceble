# Syntax Check

## Domains / IPs Syntax

PyFunceble can check the syntax of domains and IPs.

### Input Source: Inline

You can check the syntax of a domain or IP, by running PyFunceble with
the `-d` argument along with `--syntax` argument.

```sh
pyfunceble -d github.com --syntax
```

The `-d` argument can also take multiple domains to test.

```sh
pyfunceble -d github.com gitlab.com gitea.com 93.184.216.34 --syntax
```

<script async id="asciicast-OpqvsHdWBmD3jjLl0gVNVj7rK" src="https://asciinema.org/a/OpqvsHdWBmD3jjLl0gVNVj7rK.js"></script>

### Input Source: File

You can check the syntax of the domains or IPs located inside a file, by
giving the file path-s to PyFunceble through the `-f` argument.

```sh
pyfunceble -f ./source.list --syntax
pyfunceble -f https://example.org/my/awesome/file --syntax
```

When using the `-f` argument, the inputted source can be:

- any file-s on your filesystem accessible by the user running PyFunceble.
- an HTTP (raw) URLs of the file you want PyFunceble to download and check.

When testing for the syntax of domains or IPs, PyFunceble supports the
following file formats:

- hosts file
- plain text file
- AdBlock filter list (please use with the `--adblock` argument)
- RPZ (formatted) file (please use with the `--rpz` argument)

<script async id="asciicast-zoKLgHzy2Fpeud7KatlUQuGSf" src="https://asciinema.org/a/zoKLgHzy2Fpeud7KatlUQuGSf.js"></script>

## URLs Syntax

PyFunceble can check the syntax of URLs.

### Input Source: Inline

You can check the syntax of a URL through the `-u` argument of PyFunceble.

```sh
pyfunceble -u https://github.com/pyfunceble
```

That `-u` argument can also take multiple URLs to test.

```sh
pyfunceble -u https://github.com/pyfunceble https://gitlab.com/funilrys https://gitea.com
```

<script async id="asciicast-s7Vvf821ax2aJ8QlPkMqKHd2v" src="https://asciinema.org/a/s7Vvf821ax2aJ8QlPkMqKHd2v.js"></script>

### Input Source: File

You can check the snytax of the URLs located inside a file, by
giving the file path-s to PyFunceble through the `-uf` argument.

```sh
pyfunceble -uf ./source.url.list
pyfunceble -uf https://example.org/my/awesome/file
```

Just like the `-f` argument, when using the `-uf` argument, the inputted source can be:

- any file-s on your filesystem accessible by the user running PyFunceble.
- an HTTP (raw) URL-s of the file you want PyFunceble to download and check.

When testing the syntax of URLs, PyFunceble following the following formats:

- plain text file

<script async id="asciicast-rOKnzpYgss7tKwd8s3t7tv22v" src="https://asciinema.org/a/rOKnzpYgss7tKwd8s3t7tv22v.js"></script>

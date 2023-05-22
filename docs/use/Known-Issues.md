# Known Issues

On this page, you will find any issues that are known and not fixed - yet.

## Language Support

Any Python version lower than `3.7` are not compatible with PyFunble.

This means you actually are unable to run any version below Python 3.7 as a
number of used builtin features are missing and were first introduced in Python 3.7.

Here are some of the message you might experience:

```python
Fatal Error: type object 'datetime.datetime' has no attribute 'fromisoformat'
```

```python
ModuleNotFoundError: No module named 'dataclasses'
```

## PyFunceble CLI

### Combination of `-f`, `-uf` and `--adblock`

You can't use the following arguments simultaneously:

- `-f` | `--file`
- `-uf` | `--url-file`
- `--adblock`

### SQL Error: Missing default value

If you are trying to move or restore your SQL database from a dump, you may
see an error message that looks like this:

```sql
SQL Error [1364][HY000]: (conn=12345678) Field 'created_at' doesn't have a default value
    (conn=12345678) Field 'created_at' doesn't have a default value
    (conn=12345678) Field 'created_at' doesn't have a default value
        Field 'created_at' doesn't have a default value
```

The issue arises from the way PyFunceble configures [SQLAlchemy](https://www.sqlalchemy.org/) as PyFunceble is assuming the full control of the datasets by setting the default on the software side and not in the database.

To solve the issue, you will have to manually set the default for `created_at`
to for example `2020-12-22 09:09:50` in `pyfunceble_whois_record` table.
You can use [dBeaver](https://dbeaver.io/) or manually run the following SQL statement inside your database.

```sql
ALTER TABLE pyfunceble_whois_record
    MODIFY COLUMN created_at datetime
    DEFAULT '2020-12-22 09:09:50'
    NOT NULL;
```

## Operating Systems

### Ubuntu

#### Ubuntu 20.04.1 LTS - Focal

In Ubuntu 20.04, the dynamicly linked library named `libffi.so.6` has been replaced
with `libffi.so.7`.

This means that PyFunceble will throw such errors:

```
ImportError: libffi.so.6: cannot open shared object file: No such file or directory
```

The problem can be solved through the creation of a softlink between the version
with the following:

```shell
sudo ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libffi.so.6
```

!!! warning ""

    Please locate `libffi.so.7` first through:

    ```shell
    find /usr/lib/ -type f -iname 'libffi.so.*'
    ```

### Windows

#### Windows Powershell with Python or Cygwin


There are a number of well Known limitation by running or even
installing Python on Windows.

If you intend to run PyFunceble through Powershell, you have to ensure that
Python is installed into the system's `PATH` environment variable. Otherwise,
your Powershell won't be able to locate the PyFunceble executable.

If however you intend to run PyFunceble through Cygwin, you have to manually
define the `PATH` (as Cygwin won't follow the system-wide settings) or use
the absolute path of the PyFunceble executable.

!!! note ""

    Since this issue is not directly related to PyFunceble, you may document
    yourself throught the [issue #127](https://github.com/funilrys/PyFunceble/issues/127).


## CI / CD Engines

### Travis CI

While using PyFunceble under the Travis CI engine, no coloration will be displayed.

### GitLab CI/CD

While using PyFunceble under the GitLab CI/CD engine, no coloration will be displayed.

### GitHub Workflows

While using PyFunceble under the GitHub Workflows/Actions engine, no coloration will be displayed.


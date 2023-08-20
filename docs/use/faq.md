# FAQ

## How to speed up the test process

!!! danger "Beware!!!!"

    When talking about speed, a lot of things have to be taken into consideration.
    Here is a non-exhaustive list of things that can fluctuate the testing speed.

    - Bandwidth
    - DNS Server response time
    - CPU
    - ISP filter _(cf: blocking connection to huge amount of IPs)_
    - Our very own databases management _(cf: this does not apply to PostgreSQL, MySQL or MariaDB)_
    - Size of the dataset to test
    - Disk I/O in particular as PyFunceble is heavy on the I/O _(cf: RAM Drives and NVMe disks are very suitable for PyFunceble's CSV storage)_
    - ...

### With dedicated Server, VM or machine

If you have a dedicated server, VM or machine for PyFunceble, you can simply increase
the number of maximal workers PyFunceble is allowed to use through the `--max-workers`
argument or its `cli_testing.max_workers` setting.

By default, the number of worker is equal to the number of CPU Cores minus 2 (`CPU Cores - 2`).
Meaning that if you have `8` CPU threads, the value will be automatically set to `6`.

If that is still not sufficient for you, and you feel chancy, you my try to use the
dangerous `--chancy` argument.

!!! info

    Keep in mind that the max workers setting mostly - if not only - affects the tester
    subprocesses and not the one in charge of generating outputs. Therefore, you may
    have the feeling that it takes time because you feel that the output
    is slow but that's actually not the case. (cf: this doesn't apply if you
    choose to use the `--chancy` argument - or its setting switch).

    Indeed, because we want to safely write the files _(Disk I/O)_, we still need
    a single process that reads the submitted results and generates the outputs.

    This has been a design decision because having safely formatted files is more
    important that having the feeling that the output is pretty quick.

!!! danger "Beware!!!!"

    No contributor or maintainer of PyFunceble shall be responsible for your
    decisions. If you felt chancy enough to use the `--chancy` argument, you
    shouldn't not yield when something inexpected happens.

    You are still welcome to propose some changes though :smile:.
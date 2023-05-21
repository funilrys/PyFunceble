Frequently Asked Questions
==========================

How to speed up the test process?
---------------------------------

.. warning::
    Beware, when talking about speed a lot of things have to be taken into consideration.
    Indeed here is a non-exhaustive list of things that fluctuate the testing speed.

    * Bandwidth.
    * DNS Server response time.
    * CPU.
    * ISP's who blocks a big amount of connection to the outside world.
    * Our databases management (do not apply for PostgreSQL, MySQL and MariaDB format).
    * Amount of data to test.
    * Disk I/O in particular as PyFunceble is heavy on the I/O
      * RamDrives and NVME disks are very suitable for PyFunceble CSV db.
    * ...

I have a dedicated server or machine just for PyFunceble
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply increase the number of maximal workers PyFunceble is allowed to use
through the `--max-workers <../usage/index.html#w-max-workers>`_ argument.

By default, the number of workers is equal to:

::

    CPU CORES - 2

meaning that if you have :code:`8` CPU threads, the value will be
automatically set to :code:`6`.

If that's not sufficient for you, you may try the dangerous
`--chancy <../usage/index.html#chancy>`_  argument.


.. warning::
    Keep in mind that the :code:`--max-workers` (:code:`-w`) mostly - if
    not only - affects the tester processes. Because we want to safely
    write the files(Disk I/O), we still need a single process that reads the
    submitted results and generates the outputs.

    The reason we added this to PyFunceble :code:`4.0.0` is we don't want
    to have a wrongly formatted file output.


Setup and use ramfs
-------------------
What is a ramfs and why not use tmpfs?

:code:`ramfs` is better than :code:`tmpfs` when data needs to be secret,
since :code:`ramfs` data never gets swapped (saved to a physical storage
drive), while tmpfs may get swapped.
Third parties who later gain root or physical access to the machine then
can inspect the swap space and extract sensitive data.

The HOWTO solution
^^^^^^^^^^^^^^^^^^
You can prepare :code:`ramfs` mount so any non-privileged user can
mount/unmount it on-demand.

To do this, you will need root privilege, once. Ask the administrator of
your system to set this up for you, if you lack root privileges.

At first, you need to add a line to the :code:`/etc/fstab`. The line in
fstab may look like this:


.. :code-block:: console
    none    /mnt/ramfs    ramfs    noauto,user,size=1024M,mode=0777    0    0

* :code:`/mnt/ramfs` is a mount point, where the ramfs filesystem will be
  mounted. Directory **most** exist.
* :code:`noauto` option prevents this from being mounted automatically
  (e.g. at system's boot-up).
* :code:`user` makes this mountable by regular users.
* :code:`size` sets this "ramdisk's" size (you can use :code:`M` and
  :code:`G` here)
* :code:`mode` is very important, with the octal :code 0770 only root and
  user, who mounted this filesystem, will be able to read and write to
  it, not the others (you may use different :code of your choice as well,
  but be very sure about it!).

.. note::

    We recommend you to set the file mode to :code:`0777` in case you
    are using this in relation to any kind of scripting, to ensure
    subprocesses have access to the file(s). In all other cases, you should set the folder
    permision to :code:`0770`.

**Mount**

  .. code-block:: console

      $ mount /mnt/ramfs/


**Unmount**

  .. code-block:: console

      $ umount /mnt/ramfs/


This chapter has practically been copied from
`<https://unix.stackexchange.com/a/325421>`_ creditted to Neurotransmitter
as it is well written and cover our purpose for describing how to setup a
ramFS to be used for testing with PyFunceble.

Next, we need to configure PyFunceble to use the newly created and mounted
ramFS. This is done with the
`PYFUNCEBLE_OUTPUT_LOCATION <../usage/index.html#global-variables>`_ ; now
all outputs are stored in the ramFS, so remember to copy the results to a
stationary file path when you are done.

Next time you are going to run a test with PyFunceble are will do:
  1. Mount the ramFS
  2. Copy the last test results to the ramFS
  3. Run your test
  4. Copy your results from ramFS to a stationary file path.

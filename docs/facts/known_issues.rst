Known issues
============

This is the list of issues which are not or will not be fixed (yet...).

* Under Travis CI the coloration may not be shown.
* Under GitLab CI/CD the coloration may not be shown.


Ubuntu 20.04.1 LTS Focal
^^^^^^^^^^^^^^^^^^^^^^^^


In Ubunto release 20.04 they have removed a package name
:code:`libffi.so.6` and upgraded it with version :code:`libffi.so.7`

This means PyFunceble will trow an error like:

:code:`ImportError: libffi.so.6: cannot open shared object file: No such file or directory`

The fix for this issue is then rather simple, add a softlink between the
versions with :code:`ln -s`

The complete line in my case was:

:code:`sudo ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libffi.so.6`

However, the right way to do this is by first locate where your's
:code:`libffi.so.7` is by

:code:`find /usr/lib/ -type f -iname 'libffi.so.*'` and then apply the
softlink to :code:`libffi.so.7`

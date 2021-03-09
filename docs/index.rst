.. image:: https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png
    :alt: PyFunceble logo

The tool to check the availability or syntax of domain, IP or URL.
==================================================================

.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=dev
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/blob/dev/LICENSE
.. image:: https://img.shields.io/pypi/v/pyfunceble-dev.png
    :target: https://pypi.org/project/pyfunceble-dev
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://pepy.tech/badge/pyfunceble-dev
    :target: https://pepy.tech/project/pyfunceble-dev
.. image:: https://pepy.tech/badge/pyfunceble-dev/month
    :target: https://pepy.tech/project/pyfunceble-dev
.. image:: https://pepy.tech/badge/pyfunceble-dev/week
    :target: https://pepy.tech/project/pyfunceble-dev


Welcome to PyFunceble!

PyFunceble  is the little sister of `Funceble`_ which was archived on 13th March
2018. In March 2018, because Funceble was starting to become a huge unmanageable
script, I - Nissar Chababy aka `@funilrys`_ - decided to make it a Python tool
for the purpose of extending my Python knowledge. It was meant for my own use case.

Back then, my problem was that I didn't want to download a huge hosts file
knowing that most of the entries do not exist anymore. That's how Py-Funceble
started.

My objective - now - through this tool is to provide a tool and a Python API
which helps the world test the availability of domains, IPs and URL through
the gathering and interpretation of information from existing tools or
protocols like WHOIS records, DNS lookup, or even HTTP status codes.

The base of this tool was my idea.
But as with many Open Source (related) projects, communities or
individuals, we evolve with the people we meet, exchange with or just discuss
with privately. PyFunceble was and is still not an exception to that.

My main idea was to check the availability of domains in hosts files.
But 3 years later, PyFunceble is now capable of a lot including:

- The testing of domains, IPs, and URLs.
- The checking of the syntax or reputation of a domain, IPs, and URLs.
- The decoding of AdBlock filters, RPZ records, or plain files before a test
  from the CLI.

PyFunceble evolved and will probably continue to evolve with the time
and the people using it.

In June 2020, The PyFunceble-dev PyPI package - which gets everything as
soon as possible compared to the PyFunceble (stable) package - reached 1 million
total downloads. I never noticed it until I was reached by someone informing me
of it. But, I was shocked.

I never thought that something I built from A to Z in my free time will ever
reach that point.
I was thankful to that nice person for informing me of it. But at the same time
concerned about PyFunceble and how it will evolve. That's why I started the
development of PyFunceble 4.0.0. My idea as I was refactoring it was to provide
a better Python API and implementation of my core ideas along with a better
incorporation and extension capability.
Indeed, in the last few years, I was so much obsessed with the CLI that I
really never wrote each component individually. They were all dependent - if
not part of - the CLI. With 4.0.0, you can now import one of the components
of PyFunceble and start straight away. No real need to play with the
configuration unless you want something very specific.
That's how I see the future of PyFunceble.

As of today, PyFunceble is running actively - if not daily - within several
servers, laptops, PCs, and Raspberry Pis. It is even used - thanks to our
auto continue dataset and component - with CI engines like GitHub Action,
Travis CI, and GitLab CI.

PyFunceble is my tool. But it is indirectly also become yours.
Therefore, I invite you to let me know how you use PyFunceble or simply open a
discussion - or join an existing one - about anything you do with PyFunceble.
But also anything that you - would - like - or dislike - in PyFunceble.

Happy testing with PyFunceble!

.. _Funceble: https://github.com/funilrys/funceble
.. _@funilrys: https://github.com/funilrys

.. toctree::
   :maxdepth: 3

   what-can-we-do
   contributors
   special-thanks
   supporting-the-project

.. toctree::
   :maxdepth: 3

   respect/license
   respect/code-of-conduct

.. toctree::
   :maxdepth: 3

   dead-hosts/index

.. toctree::
   :maxdepth: 3

   installation/index

.. toctree::
   :maxdepth: 3

   update/index

.. toctree::
   :maxdepth: 5

   configuration/index

.. toctree::
   :maxdepth: 3

   usage/index

.. toctree::
   :maxdepth: 3

   responses/index

.. toctree::
   :maxdepth: 3

   api/index

.. toctree::
   :maxdepth: 3

   components/index

.. toctree::
   :maxdepth: 3

   contributing/index

.. toctree::
   :maxdepth: 5

   code/modules

.. toctree::
   :maxdepth: 3

   facts/they-use-d-it
   facts/faq
   facts/known_issues
   facts/contact

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

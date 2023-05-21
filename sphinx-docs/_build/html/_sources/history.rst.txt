History of the project
======================

PyFunceble  is the little sister of `Funceble`_ which was archived on 13th March
2018. In March 2018, because Funceble was starting to become a huge unmanageable
script, I - Nissar Chababy aka `@funilrys`_ - decided to make it a Python tool
while extending my Python knowledge. It was meant for my own use
case.

Back then, my problem was that I didn't want to download a huge hosts file
knowing that most of the entries do not exist or are not reachable - anymore.
That's how Py-Funceble started.

My objective - now - through this tool is to provide a tool and a Python API
which helps the world test the availability of domains, IPs and URL through
the gathering and interpretation of information from existing tools or
protocols like WHOIS records, DNS lookup, or even HTTP status codes.

The base of this tool was my idea.
But as with many Open Source projects, communities, or individuals, we evolve
with the people we meet, exchange with or just discuss
with privately. PyFunceble was and is still not an exception to that.

My main idea was to check the availability of domains in a hosts files.
But 3 years later, PyFunceble is now capable of a lot including:

- The testing of domains, IPs, and URLs.
- The checking of the syntax or reputation of a domain, IP, and URL.
- The decoding of AdBlock filters, RPZ records, hosts or plain files before a
  test from the CLI.

PyFunceble evolved and will probably continue to evolve with the time
and the people using it.

In June 2020, the PyFunceble-dev PyPI package - which gets everything as
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

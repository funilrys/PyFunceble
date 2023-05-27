# Getting Started

PyFunceble has an internal API that can be used for you own logic. Before PyFunceble
`v4.0.0`, the internal API was extremely tight to the CLI. Therefore it has
been hard for developers to reuse PyFunceble as part of their program because
there was a lot to activate or deactivate to get things started.

Since PyFunceble `v4.0.0`, it is possible to use the internel checkers without
any initial configuration or initialization of any sort.

In other words: Simply choose your checker, interact with it and get what you are looking for!

## The Basics

Before starting to play with any [checkers](./api-reference/checker/index.md),
let me explain some basics.

To get started, you mostly need to understand the following classes:

1. [`CheckerBase`](./api-reference/checker/base.md)
2. [`CheckerStatusBase`](./api-reference/checker/status_base.md)

The first one is the base class of all checkers, and the second one is the base of
all status you get from any checker when you call the `.get_status()` method.

### Interacting with checkers

!!! note

    The method described below is the same for all available checkers.

Let's say we want to test the availability of the **domain** `github.com`.

We first have to select and prepare the checker.

```python linenums="1"
from PyFunceble import from PyFunceble import Domain

checker = DomainAvailabilityChecker()
```

We then declare the subject that we want to test:

```python linenums="1" hl_lines="4 5 6"
from PyFunceble import from PyFunceble import Domain

checker = DomainAvailabilityChecker()
checker.set_subject("github.com")
# This is the same.
checker.subject = "github.com"
```

Now, we trigger the query of the status:

```python linenums="1" hl_lines="8"
from PyFunceble import from PyFunceble import Domain

checker = DomainAvailabilityChecker()
checker.set_subject("github.com")
# This is the same.
checker.subject = "github.com"

status = checker.get_status()
```

Once we have the status, we can print the `#!python dict()` or JSON representation.

```python linenums="1" hl_lines="10 11 12 14 15 16"
from PyFunceble import from PyFunceble import Domain

checker = DomainAvailabilityChecker()
checker.set_subject("github.com")
# This is the same.
checker.subject = "github.com"

status = checker.get_status()

print("DICT REPRESENTATION")
print(status.to_dict())
print("-" * 80)

print("JSON REPRESENTATION")
print(status.to_json())
print("-" * 80)
```

We can also interact with any of the attributes of the status object:

```python linenums="1" hl_lines="18"
from PyFunceble import from PyFunceble import Domain

checker = DomainAvailabilityChecker()
checker.set_subject("github.com")
# This is the same.
checker.subject = "github.com"

status = checker.get_status()

print("DICT REPRESENTATION")
print(status.to_dict())
print("-" * 80)

print("JSON REPRESENTATION")
print(status.to_json())
print("-" * 80)

print(f"{status.idna_subject} is {status.status}")
```

Finally, and probably most importantly, we can ask questions.

!!! note

    Each checker has its own set of method. Be sure the read them or follow the
    autocomplete of your favorite editor.

```python linenums="1" hl_lines="20 21 22 23 24 25"
from PyFunceble import from PyFunceble import Domain

checker = DomainAvailabilityChecker()
checker.set_subject("github.com")
# This is the same.
checker.subject = "github.com"

status = checker.get_status()

print("DICT REPRESENTATION")
print(status.to_dict())
print("-" * 80)

print("JSON REPRESENTATION")
print(status.to_json())
print("-" * 80)

print(f"{status.idna_subject} is {status.status}")

# Is it active ?
print("Is GitHub active ?", "yes" if status.is_active() else "no")
# Is it inactive ?
print("Is GitHub inactive ?", "yes" if status.is_inactive() else "no")
# Is it invalid ?
print("Is github.com invalid ?", "yes" if status.is_invalid() else "no")
```

That's it, you went through the basic. Feel free to discover other checkers or
ask questions if something is not clear.


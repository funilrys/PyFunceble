:code:`ipv6_syntax_validation` (API)
------------------------------------

The :code:`ipv6_syntax_validation` provides the response we got while trying to validate (with :func:`PyFunceble.check.Check.is_ipv6`) the given subject.

The response will be :code:`True` for the case of a successful validation, :code:`False` otherwise, and :code:`None` for the case that the validation was not executed.
CLI Responses
-------------

From the CLI, there is a lot less information available to the end-user.
This patch intend to shortly preset each column of the CLI stdout outputs.

Subject
^^^^^^^

The subject. It describes the given or decoded subject after conversion to IDNA.

Status
^^^^^^

The status. It describes the official status of the tested subject.

Source
^^^^^^

The status source. It describes the method that let to the given status.

Expiration Date
^^^^^^^^^^^^^^^

The expiration date. It describes the expiration date extracted from the WHOIS
record - if found. Otherwise, :code:`Unknown` is supplied.

HTTP Code
^^^^^^^^^

The HTTP status code. It describes the HTTP status code - if found. Otherwise,
:code:`Unknown` is supplied.

Checker
^^^^^^^

The checker. It describes the checker used to gather the status.

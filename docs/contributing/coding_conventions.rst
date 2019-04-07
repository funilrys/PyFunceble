Coding conventions
==================

- We make sure that a method, a function, and a class **have doctrings**.

- One line should not exceed 79 characters for docstring and 100 characters for long declaration/assignment.

  - Exception granted for regular expressions or long string assignment.

- We use `Black`_, *The uncompromising Python code formatter*, to format our code.

- Our code should pass :code:`pylint PyFunceble && pylint tests/*.py` with at least a score of 10.00/10.00

- We do not forget to follow the steps before any commits.

.. _Black: https://github.com/ambv/black
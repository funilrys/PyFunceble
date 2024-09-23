# URL Syntax

```python linenums="1" title="Syntax of a URL using the API"
from PyFunceble import URLSyntaxChecker

checker = URLSyntaxChecker()
to_test = "https://github.com/pyfunceble"

# You can do it this way.
status = checker.set_subject(to_test).get_status()

# Or this way.
checker.set_subject(to_test)
status = checker.get_status()

# We can convert the status to json.
status_json = status.to_json()

# We can convert the status to dict.
status_dict = status.to_dict()

# We can ask "questions".
print(f"Is {to_test} VALID ?", "yes" if status.is_valid() else "no")
print(f"Is {to_test} INVALID ?", "yes" if status.is_invalid() else "no")
```
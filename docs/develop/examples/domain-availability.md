# Domain Availability

```python linenums="1" title="Availability of a domain using the API"
from PyFunceble import DomainAvailabilityChecker

checker = DomainAvailabilityChecker()
to_test = "github.com"

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
print(f"Is {to_test} ACTIVE ?", "yes" if status.is_active() else "no")
print(f"Is {to_test} INACTIVE ?", "yes" if status.is_inactive() else "no")
print(f"Is {to_test} INVALID ?", "yes" if status.is_invalid() else "no")
```
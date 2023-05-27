# Domain or IP Availability

```python linenums="1" title="Availability of a domain or IP using the API"
from PyFunceble import DomainAndIPAvailabilityChecker

checker = DomainAndIPAvailabilityChecker()
to_test = ["github.com", "192.0.2.1"]


for subject in to_test:
    # You can do it this way.
    status = checker.set_subject(subject).get_status()

    # Or this way.
    checker.set_subject(subject)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {subject} ACTIVE ?", "yes" if status.is_active() else "no")
    print(f"Is {subject} INACTIVE ?", "yes" if status.is_inactive() else "no")
    print(f"Is {subject} INVALID ?", "yes" if status.is_invalid() else "no")
```
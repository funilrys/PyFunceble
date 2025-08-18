# `special_rules`

PyFunceble tries to be as flexible as possible. This is why we now allow you to define special rules that PyFunceble should follow.

The special rules are defined in the `special_rules` section of the configuration file.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
special_rules:
  # Let end-user define or integrate their own special rules.
  #
  # The idea: We want to give the end-user the possibility to define their own
  # rules. This is useful when they want to switch the status of a subject based
  # on a specific pattern, header, body, or status code.
  #
  # The structure:
  #    subject_pattern:
  #      -> The pattern to match against the subject.
  #    validation_type:
  #      -> The type of validation to perform. It can be one of the following:
  #         - all: A combination of everything (first match wins).
  #         - status_code: Only the status code.
  #         - headers: Only the headers.
  #         - body: Only the body.
  #         - headers+body: Match against the headers and the body.
  #    state_transition:
  #      -> The state to switch to when the validation is successful.
  #         When set to `down`, the status will be switched to INACTIVE. When set
  #         to `up`, the status will be switched to ACTIVE.
  #    required_status_code:
  #      -> A list of status code to match against.
  #    required_headers_patterns:
  #      -> A dictionary of headers to match against. The key is the header name
  #         and the value is a list of patterns to match against.
  #    required_body_patterns:
  #      -> A list of patterns to match against the body.
  #
  # Examples:
  #    When testing httpbin.org, we want to switch the status to down when the
  #    status code is 403 and the server header contains "gunicorn".
  #
  #    - subject_pattern: "^httpbin\\.org$"
  #      validation_type: all
  #      state_transition: down
  #      required_status_code:
  #        - 403
  #      required_headers_patterns:
  #        server:
  #          - gunicorn
  #
  #    When testing example.org, we want to switch the status to down when the
  #    status code is 404.
  #
  #    - subject_pattern: "^example\\.org$"
  #      validation_type: status_code
  #      state_transition: down
  #      required_status_code:
  #        - 404
  #
  #    When testing example.com, we want to switch The body and headers.the status to down when the
  #    header `server` contains `nginx`.
  #
  #    - subject_pattern: "^example\\.com$"
  #      validation_type: headers
  #      state_transition: down
  #      required_headers_patterns:
  #        server:
  #          - nginx
  #
  #    When testing example.net, we want to switch the status to down when the
  #    body contains "Hello, World!".
  #
  #    - subject_pattern: "^example\\.net$"
  #      validation_type: body
  #      state_transition: down
  #      required_body_patterns:
  #        - Hello, World!
  #
  #    When testing example.dev, we want to switch the status to down when the
  #    headers server contains `nginx` or the body contains "Hello, World!".
  #
  #    - subject_pattern: "^example\\.dev$"
  #      validation_type: headers+body
  #      state_transition: down
  #      required_headers_patterns:
  #        server:
  #          - nginx
  #      required_body_patterns:
  #        - Hello, World!
  []
```

## Examples

### `validation_type`: `all`

When testing httpbin.org, we want to switch the status to down when the status
code is 403 and the server header contains "gunicorn".

```yaml title=".PyFunceble.overwrite.yaml"
special_rules:
  - subject_pattern: "^httpbin\\.org$"
    validation_type: all
    state_transition: down
    required_status_code:
      - 403
    required_headers_patterns:
      server:
        - gunicorn
```

### `validation_type`: `status_code`

When testing example.org, we want to switch the status to down when the status
code is 404.

```yaml title=".PyFunceble.overwrite.yaml"
special_rules:
  - subject_pattern: "^example\\.org$"
    validation_type: status_code
    state_transition: down
    required_status_code:
      - 404
```

### `validation_type`: `headers`

When testing example.com, we want to switch the status to down when the header
`server` contains `nginx`.

```yaml title=".PyFunceble.overwrite.yaml"
special_rules:
  - subject_pattern: "^example\\.com$"
    validation_type: headers
    state_transition: down
    required_headers_patterns:
      server:
        - nginx
```

### `validation_type`: `body`

When testing example.net, we want to switch the status to down when the body
contains `Hello, World!`.

```yaml title=".PyFunceble.overwrite.yaml"
special_rules:
  - subject_pattern: "^example\\.net$"
    validation_type: body
    state_transition: down
    required_body_patterns:
      - Hello, World!
```

### `validation_type`: `headers+body`

When testing example.dev, we want to switch the status to down when the header
`server` contains `nginx` or the body contains `Hello, World!`.

```yaml title=".PyFunceble.overwrite.yaml"
special_rules:
  - subject_pattern: "^example\\.dev$"
    validation_type: headers+body
    state_transition: down
    required_headers_patterns:
      server:
        - nginx
    required_body_patterns:
      - Hello, World!
```





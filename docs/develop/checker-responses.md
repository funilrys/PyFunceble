# Checker Responses

This page tries to document the response that you may expect from the different
checker types.

## Syntax Checker

```json
{
  "checker_type": "SYNTAX",
  "idna_subject": "example.com",
  "params": null,
  "status": "VALID",
  "status_source": "SYNTAX",
  "subject": "example.com",
  "tested_at": "2021-03-09T17:43:24.477977"
}
```

### checker_type

The checker type describes the kind of the checker that was used to provide the given response.

It should be set to `SYNTAX`, `AVAILABILITY` or `REPUTATION`

### idna_subject

The IDNA encoded subject that has been used to perform the tests.

### params

The parameters describes the parameter that has been applied to the checker.
Most of the time, if you are using the Python API, you should be able to control most of them through the class constructor or their property setters.

For the syntax checker, this parameter is set to `null`.

### status

The status describes the (final) status that has been gathered by the checker.

For the syntax checker, it should be set to `VALID` or `INVALID`.

### status_source

The status source describes the last test method that led to the decision of the given status.

For the syntax checker, it should always be set to `SYNTAX`.


### subject

The subject describes the subject that you supplied to PyFunceble.

## Availability Checker

```json
{
    "checker_type": "AVAILABILITY",
    "dns_lookup": {
        "NS": [
            "a.iana-servers.net.",
            "b.iana-servers.net."
        ]
    },
    "dns_lookup_record": {
        "dns_name": "example.com.",
        "follow_nameserver_order": true,
        "nameserver": "9.9.9.9",
        "port": 53,
        "preferred_protocol": "UDP",
        "query_record_type": "NS",
        "query_timeout": 5.0,
        "response": [
            "a.iana-servers.net.",
            "b.iana-servers.net."
        ],
        "subject": "example.com",
        "used_protocol": "UDP"
    },
    "domain_syntax": true,
    "expiration_date": null,
    "http_status_code": null,
    "idna_subject": "example.com",
    "ip_syntax": false,
    "ipv4_range_syntax": false,
    "ipv4_syntax": false,
    "ipv6_range_syntax": false,
    "ipv6_syntax": false,
    "netinfo": null,
    "netloc": "example.com",
    "params": {
        "do_syntax_check_first": false,
        "use_dns_lookup": true,
        "use_extra_rules": true,
        "use_http_code_lookup": true,
        "use_netinfo_lookup": true,
        "use_reputation_lookup": false,
        "use_whois_db": true,
        "use_whois_lookup": false,
        "use_collection": false
    },
    "registrar": null,
    "second_level_domain_syntax": true,
    "status": "ACTIVE",
    "status_after_extra_rules": null,
    "status_before_extra_rules": null,
    "status_source": "DNSLOOKUP",
    "status_source_after_extra_rules": null,
    "status_source_before_extra_rules": null,
    "subdomain_syntax": false,
    "subject": "example.com",
    "tested_at": "2021-03-09T17:42:15.771647",
    "url_syntax": false,
    "whois_lookup_record": {
        "expiration_date": null,
        "port": 43,
        "query_timeout": 5.0,
        "record": null,
        "server": null,
        "subject": "example.com",
        "registrar": null
    },
    "whois_record": null
}
```

## Reputation Checker

```json
{
    "checker_type": "REPUTATION",
    "dns_lookup": [
        "93.184.216.34"
    ],
    "dns_lookup_record": {
        "dns_name": "example.com.",
        "follow_nameserver_order": true,
        "nameserver": "9.9.9.9",
        "port": 53,
        "preferred_protocol": "UDP",
        "query_record_type": "A",
        "query_timeout": 5.0,
        "response": [
            "93.184.216.34"
        ],
        "subject": "example.com",
        "used_protocol": "UDP"
    },
    "domain_syntax": true,
    "idna_subject": "example.com",
    "ip_syntax": false,
    "ipv4_range_syntax": false,
    "ipv4_syntax": false,
    "ipv6_range_syntax": false,
    "ipv6_syntax": false,
    "params": {
        "do_syntax_check_first": false,
        "use_collection": false
    },
    "second_level_domain_syntax": true,
    "status": "SANE",
    "status_source": "REPUTATION",
    "subdomain_syntax": false,
    "subject": "example.com",
    "tested_at": "2021-03-09T17:44:02.908452",
    "url_syntax": false
}
```
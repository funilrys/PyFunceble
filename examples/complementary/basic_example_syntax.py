"""
This is a basic example which checks syntax.
"""

from PyFunceble import (
    is_domain,
    is_ipv4,
    is_ipv4_range,
    is_subdomain,
    is_url,
    load_config,
)

load_config(custom={"db_type": "json"})

print("Start of basic example for syntax check.")
print("google.com", is_domain("google.com"))
print("https://google.com", is_url("https://google.com"))
print("216.58.207.46", is_ipv4("216.58.207.46"))

print("forest-jump", is_domain("forest-jump"))
print("https://forest-jump", is_url("https://forest-jump"))
print("257.58.207.46", is_ipv4("257.58.207.46"))
print("End of basic example for syntax check.")

print("\nStart of the subdomain check.")
print("hello.google.com", is_subdomain(subject="hello.google.com"))
print("google.com", is_subdomain(subject="google.com"))
print("End of the subdomain check.")

print("\nStart of the IPv4 range check.")
print("192.168.0.0/24", is_ipv4_range(subject="192.168.0.0/24"))
print("192.168.0.0", is_ipv4_range(subject="192.168.0.0"))
print("End of the IPv4 range check.")

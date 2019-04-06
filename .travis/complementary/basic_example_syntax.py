"""
This is a basic example which checks syntax.
"""

from PyFunceble import ipv4_syntax_check as PyFuncebleIPv4Syntax
from PyFunceble import is_ipv4_range, is_subdomain
from PyFunceble import syntax_check as PyFuncebleDomainSyntax
from PyFunceble import url_syntax_check as PyFuncebleURLSyntax

print("Start of basic example for syntax check.")
print("google.com", PyFuncebleDomainSyntax(domain="google.com"))
print("https://google.com", PyFuncebleURLSyntax(url="https://google.com"))
print("216.58.207.46", PyFuncebleIPv4Syntax(ip="216.58.207.46"))

print("forest-jump", PyFuncebleDomainSyntax(domain="forest-jump"))
print("https://forest-jump", PyFuncebleURLSyntax(url="https://forest-jump"))
print("257.58.207.46", PyFuncebleIPv4Syntax(ip="257.58.207.46"))
print("End of basic example for syntax check.")

print("\nStart of the subdomain check.")
print("hello.google.com", is_subdomain(subject="hello.google.com"))
print("google.com", is_subdomain(subject="google.com"))
print("End of the subdomain check.")

print("\nStart of the IPv4 range check.")
print("192.168.0.0/24", is_ipv4_range(subject="192.168.0.0/24"))
print("192.168.0.0", is_ipv4_range(subject="192.168.0.0"))
print("End of the IPv4 range check.")

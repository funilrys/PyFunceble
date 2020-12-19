"""
This is a basic example which checks syntax.
"""

from PyFunceble import (
    DomainSyntaxChecker,
    IPv4SyntaxChecker,
    SubDomainSyntaxChecker,
    URLSyntaxChecker,
)

print(f"Starting syntax check using {DomainSyntaxChecker}")
checker = DomainSyntaxChecker()

for domain in ["google.com", "forest-jump"]:
    print(f"{domain} VALID ? {checker.set_subject(domain).is_valid()}")
print(f"Finished syntax check using {DomainSyntaxChecker}\n")

print(f"Starting syntax check using {URLSyntaxChecker}")
checker = URLSyntaxChecker()

for domain in ["https://google.com", "https://forest-jump"]:
    print(f"{domain} VALID ? {checker.set_subject(domain).is_valid()}")
print(f"Finished syntax check using {URLSyntaxChecker}\n")

print(f"Starting syntax check using {IPv4SyntaxChecker}")
checker = IPv4SyntaxChecker()

for domain in ["216.58.207.46", "257.58.207.46"]:
    print(f"{domain} VALID ? {checker.set_subject(domain).is_valid()}")
print(f"Finished syntax check using {IPv4SyntaxChecker}\n")

print(f"Starting syntax check (range) using {IPv4SyntaxChecker}")
checker = IPv4SyntaxChecker()

for domain in ["192.168.0.0/24", "192.168.0.0"]:
    print(f"{domain} VALID range ? {checker.set_subject(domain).is_valid_range()}")
print(f"Finished syntax check (range) using {IPv4SyntaxChecker}\n")

print(f"Starting syntax check using {SubDomainSyntaxChecker}")
checker = SubDomainSyntaxChecker()

for domain in ["hello.google.com", "google.com"]:
    print(f"{domain} VALID ? {checker.set_subject(domain).is_valid()}")
print(f"Finished syntax check using {SubDomainSyntaxChecker}\n")

"""
This is an advanced example which get more information about the tested element.
"""

from PyFunceble import DomainAndIPAvailabilityChecker, URLAvailabilityChecker

SUBJECTS = ["google.com", "github.com", "example.org", "8.8.8.8", "8.8.4.4"]

domain_ip_avail_checker = DomainAndIPAvailabilityChecker(use_whois_lookup=False)
url_avail_checker = URLAvailabilityChecker()

for subject in SUBJECTS:
    domain_ip_avail_checker.subject = subject
    url_avail_checker.subject = f"https://{subject}"

    domain_ip_status = domain_ip_avail_checker.get_status()
    url_status = url_avail_checker.get_status()

    print(
        f"============== COMPLETE DATA: {domain_ip_avail_checker.subject} "
        "=============="
    )
    print(domain_ip_status.to_json(), "\n\n")

    print(f"============== COMPLETE DATA: {url_avail_checker.subject} ==============")
    print(url_status.to_json(), "\n\n")

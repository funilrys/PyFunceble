"""
This is an example which check that the file generation from the API is still
working.
"""

import sys
from os import path

import PyFunceble
import PyFunceble.cli

PyFunceble.cli.initiate_colorama(True)
PyFunceble.load_config(
    generate_directory_structure=False,
    custom={"api_file_generation": True, "plain_list_domain": True},
)
PyFunceble.output.Clean(None)

DOMAINS = ["github.com", "twitter.com"]

for domain in DOMAINS:
    print(f"{domain} is {PyFunceble.test(domain)}")

if path.isfile(
    PyFunceble.CONFIG_DIRECTORY
    + PyFunceble.OUTPUTS.parent_directory
    + "domains/ACTIVE/list"
):
    print(
        f"{PyFunceble.cli.Style.BRIGHT + PyFunceble.cli.Fore.GREEN}All right, "
        "files correctly generated!"
    )
    sys.exit(0)
else:
    print(
        f"{PyFunceble.cli.Style.BRIGHT + PyFunceble.cli.Fore.RED}Something went wrong, "
        "files not correctly generated!"
    )
    sys.exit(1)

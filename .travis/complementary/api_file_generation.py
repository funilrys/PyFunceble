"""
This is an example which check that the file generation from the API is still
working.
"""

from os import path

import PyFunceble

PyFunceble.initiate_colorama(True)
PyFunceble.load_config(
    generate_directory_structure=True,
    custom={"api_file_generation": True, "plain_list_domain": True},
)
PyFunceble.Clean(None)

DOMAINS = ["github.com", "twitter.com"]

for domain in DOMAINS:
    print(f"{domain} is {PyFunceble.test(domain)}")

if path.isfile(
    PyFunceble.CONFIG_DIRECTORY
    + PyFunceble.OUTPUTS.parent_directory
    + "domains/ACTIVE/list"
):
    print(
        f"{PyFunceble.Style.BRIGHT + PyFunceble.Fore.GREEN}All right, "
        "files correctly generated!"
    )
    PyFunceble.sys.exit(0)
else:
    print(
        f"{PyFunceble.Style.BRIGHT + PyFunceble.Fore.RED}Something went wrong, "
        "files not correctly generated!"
    )
    PyFunceble.sys.exit(1)

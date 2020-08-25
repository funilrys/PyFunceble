What can PyFunceble do?
=======================

- Test the availability of a domain.
- Test the availability of an IPv4.
- Test the availability of an IPv6.
- Test the availability of a URL.
- Test the availability of a domain/DNS name in a private or local network.
- Test the availability of an IPv4 in a private or local network.
- Test the availability of an IPv6 in a private or local network.
- Test the availability of a URL in a private or local network.
- Test the syntax of a domain.
- Test the syntax of an IPv4.
- Test the syntax of an IPv6.
- Test the syntax of a URL.
- Test the AlienVault's reputation of an IPv4.
- Test of domain or IP which are present into an Adblock formatted file.
- Test from a given raw link.
- Test using multiprocessing (from CLI only).
- Save test result(s) in file(s) (hosts file, plain text and/or JSON format).
- Save test result in a SQL database.
- Show test result(s) on screen.
- Show percentage of each status (:code:`ACTIVE`, :code:`INACTIVE`, 
  :code:`INVALID`)
- Sort outputs hierarchically.
- "Mining" of domain or IP which are related to the tested element.
- Auto-continuation of tests in case of system crash or script stop.
- Filtering of a file content.

  - This feature will let us for example test all blogspot domain of the given 
    file no matter the content of the file.

- Set the user-agent to use for the tests.
- Give some analytic depending of the HTTP status code (:code:`ACTIVE`, 
  :code:`POTENTIALLY_ACTIVE`, :code:`POTENTIALLY_INACTIVE`, :code:`SUSPICIOUS`).
- Retest overtime of :code:`INACTIVE` and :code:`INVALID` domains.
- Print the execution time on screen and file.
- Customisation of the different option via command-line arguments or 
  configuration file.
- Continuous tests under Travis CI or GitLab CI/CI

  - ... with the help of an auto saving and database system.
  - Set the branch to push the result to. For the autosaving system.
  - Set the minimal time before we autosave in order to avoid CI/CD limitation.
  - Set a command to execute at the end of the test.
  - Set the commit message for the autosaving system.

- ... and a lot more!

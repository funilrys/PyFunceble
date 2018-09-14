What can PyFunceble do?
=======================

- Test of the availability of a domain.
- Test of the availability of an IPv4.
- Test of the availability of a URL.
- Test of domain or IP which are present into an Adblock formatted file.
- Test from a given raw link.
- Save test result(s) on file(s) (in several format).
- Show test result(s) on screen.
- Show percentage of each status (:code:`ACTIVE`, :code:`INACTIVE`, :code:`INVALID`)
- Auto-continuation of tests in case of system crash or script stop.
- Filtering of a file content. This feature will let us for example test all Blogspot domain of the given file no matter the content of the file.
- Customisation of the different option via command-line arguments or configuration file.
- Set the user-agent to use for the tests.
- Give some analytic depending of the HTTP status code (:code:`ACTIVE`, :code:`POTENTIALLY_ACTIVE`, :code:`POTENTIALLY_INACTIVE`, :code:`SUSPICIOUS`).
- Continuous tests under Travis CI with the help of an autosaving and database system.
    - Set branch to push the result to for the autosaving system.
    - Set the minimal time before we autosave.
    - Set a command to execute at the end of the test.
    - Set the commit message for the autosaving system
- ... and a lot more!
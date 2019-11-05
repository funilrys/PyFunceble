class PyFuncebleException(Exception):
    pass


class PyFuncebleExternalException(PyFuncebleException):
    pass


class PyFuncebleInternalException(PyFuncebleException):
    pass


class WrongParameterType(PyFuncebleInternalException):
    pass


class WrongParameterValue(PyFuncebleInternalException):
    pass


class NoInternetConnection(PyFuncebleExternalException):
    pass


class ConfigurationFileNotFound(PyFuncebleInternalException):
    pass


class GitHubTokenNotFound(PyFuncebleExternalException):
    pass


class GitEmailNotFound(PyFuncebleExternalException):
    pass


class GitNameNotFound(PyFuncebleExternalException):
    pass


class PleaseUpdatePyFunceble(PyFuncebleInternalException):
    pass


class NoConversionMade(PyFuncebleInternalException):
    pass


class NoExtractionMade(PyFuncebleInternalException):
    pass


class UnknownSubject(PyFuncebleInternalException):
    pass

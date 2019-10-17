class PyFuncebleException(Exception):
    pass


class PyFuncebleExternalException(PyFuncebleException):
    pass


class PyFuncebleInternalException(PyFuncebleException):
    pass


class WrongParameterType(PyFuncebleInternalException):
    pass


class NoInternetConnection(PyFuncebleExternalException):
    pass


class MessageNotFound(PyFuncebleInternalException):
    pass


class ConfigurationFileNotFound(PyFuncebleInternalException):
    pass


class GitHubTokenNotFound(PyFuncebleExternalException):
    pass


class GitEmailNotFound(PyFuncebleExternalException):
    pass


class GitNameNotFound(PyFuncebleExternalException):
    pass

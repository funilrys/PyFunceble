from platform import system


class Platform:  # pragma: no cover
    """
    Provides an easy way to get the current platform.
    """

    WINDOWS = ["windows", "cygwin", "cygwin_nt-10.0"]
    """
    Provides the list of supported windows platform.
    """

    UNIX = ["linux", "darwin"]
    """
    Provides the list of supported unix platform.
    """

    MAC = ["darwin"]
    """
    Provides teh list of supported MAC platform.
    """

    @classmethod
    def get(cls):
        """
        Returns the current platform.
        """
        return system().lower()

    @classmethod
    def is_windows(cls):
        """
        Checks if the current platform is in our windows list.
        """

        return cls.get() in cls.WINDOWS

    @classmethod
    def is_unix(cls):
        """
        Checks if the current platform is in our unix list.
        """

        return cls.get() in cls.UNIX  # pragma: no cover

    @classmethod
    def is_mac_os(cls):
        """
        Checks if the current platform is in our OSX list.
        """

        return cls.get() in cls.MAC

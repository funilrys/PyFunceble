import PyFunceble.helpers as helpers


class Package:
    """
    Provides some packaging related abstractions.
    """

    NAME = "PyFunceble"
    """
    Sets the package name.
    """

    VERSION = "2.31.1.dev (Green Galago: Skitterbug)"
    """
    Sets the package version.
    """


class Version:
    """
    Provides a simple way to compare our own versions.
    """

    @classmethod
    def split_versions(cls, version, return_non_digits=False):
        """
        Convert the versions to a shorter one.

        :param str version: The version to split.

        :param bool return_non_digits:
            Activate the return of the non-digits parts of the splitted
            version.

        :return: The splitted version name/numbers.
        :rtype: list
        """

        # We split the version.
        splited_version = version.split(".")

        # We split the parsed version and keep the digits.
        digits = [x for x in splited_version if x.isdigit()]

        if not return_non_digits:
            # We do not have to return the non digits part of the version.

            # We return the digits part of the version.
            return digits

        # We have to return the non digit parts of the version.

        # We split the parsed version and keep the non digits.
        non_digits = [x for x in splited_version if not x.isdigit()]

        # We return a tuple with first the digits part and finally the non digit parts.
        return (digits, non_digits[0])

    @classmethod
    def literally_compare(cls, local, upstream):
        """
        Compare the given versions literally.

        :param str local: The local version converted by split_versions().

        :param str upstream: The upstream version converted by split_versions().

        :return:
            - True: local == upstream
            - False: local != upstream
        :rtype: bool
        """

        return local == upstream

    @classmethod
    def compare(cls, upstream):
        """
        Compare the given versions with the local one.

        :param list local: The local version converted by split_versions().

        :param list upstream: The upstream version converted by split_versions().

        :return:
            - True: local < upstream
            - None: local == upstream
            - False: local > upstream
        :rtype: bool|None
        """

        # We get the local version.
        local = cls.split_versions(Package.VERSION)
        # We get the upstream version
        upstream = cls.split_versions(upstream)

        # A version should be in format [1,2,3] which is actually the version `1.2.3`
        # So as we only have 3 elements in the versioning,
        # we initiate the following variable in order to get the status of each parts.
        status = [None, None, None]

        for index, version_number in enumerate(local):
            # We loop through the local version.

            if int(version_number) < int(upstream[index]):
                # The local version is less than the upstream version.

                # We initiate its status to True which means that we are in
                # an old version (for the current version part).
                status[index] = True
            elif int(version_number) > int(upstream[index]):
                # The local version is greater then the upstream version.

                # We initiate its status to False which means that we are in
                # a more recent version (for the current version part).
                status[index] = False
            else:
                # The local version is eqal to the upstream version.

                # We initiate its status to None which means that we are in
                # the same version (for the current version part).
                status[index] = None

            # Otherwise the status stay None which means that there is no change
            # between both local and upstream.

        # We consider that the version is the same.
        result = None

        for data in status:
            # We loop through the list of status.
            # The purpose of this loop is only to
            # get the first not None value.

            if result is None:
                # The result is None (no changes).
                # We set the currently read one as the result.
                result = data

        # We return the result.
        return result

    @classmethod
    def is_local_dev(cls):
        """
        Checks if the local version is the development version.
        """

        return "dev" in Package.VERSION

    @classmethod
    def is_local_cloned(cls):  # pragma: no cover
        """
        Let us know if we are currently in the cloned version of
        PyFunceble which implicitly mean that we are in developement mode.
        """

        if not helpers.Directory(".git").exists():
            # The git directory does not exist.

            # We return False, the current version is not the cloned version.
            return False

        # We list the list of file which can be found only in a cloned version.
        list_of_file = [
            ".coveragerc",
            ".coveralls.yml",
            ".gitignore",
            ".PyFunceble_production.yaml",
            ".travis.yml",
            "CODE_OF_CONDUCT.rst",
            "CONTRIBUTING.rst",
            "dir_structure_production.json",
            "MANIFEST.in",
            "README.rst",
            "requirements.txt",
            "setup.py",
            "version.yaml",
        ]

        # We list the list of directory which can be found only in a cloned
        # version.
        list_of_dir = ["docs", "PyFunceble", "tests"]

        if not all([helpers.File(x).exists() for x in list_of_file]):
            return False

        # All required files exist in the current directory.

        if not all([helpers.Directory(x).exists() for x in list_of_dir]):
            return False

        # All required directories exist in the current directory.

        # We return True, the current version is a cloned version.
        return True

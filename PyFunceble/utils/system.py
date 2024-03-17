# pylint: disable=invalid-name
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some global utilities.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import functools
import importlib
from collections.abc import Iterable
from typing import List, Union


class DynamicImport:
    """
    Provides the ability to dynamically import a module before executing the
    decorated method or function.

    :param statements:
        The statement to import.

        Possible formats:

            - :code:`from X import Y`
            - :code:`from X import Y as Z`
            - :code:`import X.Y`
            - :code:`import X.Y as Z`
            - :code:`X.Y` means `import X.Y`
            - :code:`X.Y as Z` means `import X.Y as Z`
            - :code:`X` means `import X`
            - :code:`X as Y` means `import X as Y`
            - :code:`X<-Y` means `from X import Y`
            - :code:`X<-Y->Z` means `from X import Y as Z`

    Usage:

        ```python
        @DynamicImport("from X import Y as Z")
        def hello_name(name: str):
            print(f"{Z.hello_german}, {name}!")
        ```
    """

    def __init__(self, *statements: Union[str, List[str]]):
        self.statements = statements

    @staticmethod
    def handle_from_import(statement):
        """
        Given a function and a statement, process the import of the given
        statement.

        :param func:
            The function to work with.
        :param statement: b
            The statement to process.

            Possible formats:

                - :code:`from X import Y`
                - :code:`from X import Y as Z`

        :return:
            :code:`(target global name, the imported module)`
        """

        splitted_statement = statement.split()

        if len(splitted_statement) == 4:
            # Format: from X import Y
            module, target = splitted_statement[1], splitted_statement[3]
            save_as = target
        else:
            # Format: from X import Y as Z
            module, target, save_as = (
                splitted_statement[1],
                splitted_statement[3],
                splitted_statement[5],
            )

        return save_as, getattr(importlib.import_module(module), target)

    @staticmethod
    def handle_import(statement):
        """
        Given a function and a statement, process the import of the given
        statement.

        :param func:
            The function to work with.
        :param statement:
            The statement to process.

            Possible formats:

                - :code:`import X.Y`
                - :code:`import X.Y as Z`

        :return:
            :code:`(target global name, the imported module)`
        """

        splitted_statement = statement.split()
        save_as = ""

        if len(splitted_statement) == 2:
            # Format: import X.X
            module = splitted_statement[1]
        else:
            # Format: import X.X as Y
            module, save_as = splitted_statement[1], splitted_statement[3]

        imported_module = importlib.import_module(module)
        save_as = module if not save_as else save_as

        return save_as, imported_module

    @staticmethod
    def handle_arrow_import(statement):
        """
        Given a function and a statement, process the import of the given
        statement.

        :param func:
            The function to work with.
        :param statement:
            The statement to process.

            Possible formats:

                - :code:`X<-Y` means `from X import Y`
                - :code:`X<-Y->Z` means `from X import Y as Z`
                - :code:`X->Z` means `import X as Z`

        :return:
            :code:`(target global name, the imported module)`
        """

        target = ""

        if "<-" in statement:
            module, target = statement.split("<-", 1)

            if "->" in target:
                target, save_as = target.split("->", 1)
            else:
                save_as = target
        else:
            module, save_as = statement.split("->", 1)

        if target:
            return save_as, getattr(importlib.import_module(module), target)

        return save_as, importlib.import_module(module)

    @staticmethod
    def handle_dot_import(statement):
        """
        Given a function and a statement, process the import of the given
        statement.

        :param func:
            The function to work with.
        :param statement:
            The statement to process.

            Possible formats:

                - :code:`X.Y` means `import X.Y`

        :return:
            :code:`(target global name, the imported module)`
        """

        module, _ = statement.split(".", 1)
        save_as = module

        return save_as, importlib.import_module(module)

    @classmethod
    def proceed_import(cls, func, statement):
        """
        Given a function and a statement, process the parsing and import of the
        given statement.

        :param func:
            The function to work with.
        :param statement:
            The statement to process.

            Possible formats:

                - :code:`from X import Y`
                - :code:`from X import Y as Z`
                - :code:`import X.Y`
                - :code:`import X.Y as Z`
                - :code:`X.Y` means `import X.Y`
                - :code:`X.Y as Z` means `import X.Y as Z`
                - :code:`X` means `import X`
                - :code:`X as Y` means `import X as Y`
                - :code:`X<-Y` means `from X import Y`
                - :code:`X<-Y->Z` means `from X import Y as Z`
        """
        try:
            if statement.startswith("from "):
                save_as, imported_module = cls.handle_from_import(statement)
            elif statement.startswith("import "):
                save_as, imported_module = cls.handle_import(statement)
            elif " as " in statement:
                module, save_as = statement.split(" as ", 1)
                imported_module = importlib.import_module(module)
            elif "<-" in statement or "->" in statement:
                save_as, imported_module = cls.handle_arrow_import(statement)
            elif "." in statement:
                save_as, imported_module = cls.handle_dot_import(statement)
            else:
                save_as, imported_module = statement, importlib.import_module(statement)

            func.__globals__[save_as] = imported_module
        except ImportError as exception:
            raise ImportError(f"Could not process or find {statement!r}") from exception

        return func

    def __call__(self, func):
        """
        Process the import before the decorated method or function is executed.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(self.statements, (Iterable, list, tuple)):
                for statement in self.statements:
                    self.proceed_import(func, statement.strip())
            else:
                self.proceed_import(func, self.statements[0].strip())
            return func(*args, **kwargs)

        return wrapper


Import = DynamicImport
LateImport = DynamicImport

"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the command helpers. This helpers let us run Shell commands.

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


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import subprocess
import sys
from typing import Generator, Optional, Union


class CommandHelper:
    """
    Shell command execution.

    :param str command: The command to execute.
    :param str encoding: The encoding to use to decode the shell output.
    """

    _command: Optional[str] = None
    _encoding: str = "utf-8"

    def __init__(
        self,
        command: Optional[Union[str, list]] = None,
        *,
        encoding: Optional[str] = None,
    ) -> None:

        if command is not None:
            self.command = command

        if encoding is not None:
            self.encoding = encoding

    @property
    def command(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_command` attribute.
        """

        return self._command

    @command.setter
    def command(self, value: Union[str, list]) -> None:
        """
        Sets the command to use.

        :param value:
            The command to use/execute.

        :raise TypeError:
            When the value is not a :py:class:`list` or :py:class:`str`
        """

        if not isinstance(value, (str, list)):
            raise TypeError(
                f"<value> should be {str} or {list}, " f"{type(value)} given."
            )

        if isinstance(value, list):
            self._command = " ".join(value)
        else:
            self._command = value

    def set_command(self, value: Union[str, list]) -> "CommandHelper":
        """
        Sets the command to use.

        :param value:
            The command to use/execute.
        """

        self.command = value

        return self

    @property
    def encoding(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_encoding` attribute.
        """

        return self._encoding

    @encoding.setter
    def encoding(self, value: str) -> None:
        """
        Sets the encoding to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the value is not a :py:class:`str`
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._encoding = value

    def set_encoding(self, value: str) -> "CommandHelper":
        """
        Sets the encoding to use.

        :param value:
            The value to set.
        """

        self.encoding = value

        return self

    def _decode_output(self, to_decode: bytes) -> str:
        """
        Decode the output of a shell command in order to be readable.

        :param bytes to_decode: Output of a command to decode.

        :return: The decoded output.
        :rtype: str
        """

        if to_decode:
            return to_decode.decode(self.encoding)

        return ""

    def execute(self, *, raise_on_error: bool = False) -> str:
        """
        Execute the given command.

        :parma raise_on_error:
            Raises on error if set to :py:class:`True`.

        :return: The output of the command.

        :raise RuntimeError:
            When the exit code is not equal to 0.
        """

        # We initiate a process and parse the command to it.
        with subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            env=os.environ,
        ) as process:
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                if raise_on_error:
                    raise RuntimeError(repr(self._decode_output(stderr)))
                return self._decode_output(stderr)
            return self._decode_output(stdout)

    def run(self, rstrip: bool = True) -> Generator[str, None, None]:
        """
        Run the given command and yield each line(s) one by one.

        .. note::
            The difference between this method and
            :func:`~PyFunceble.helpers.Command.execute`
            is that :func:`~PyFunceble.helpers.Command.execute` wait for the
            process to end in order to return its output while this method
            return each line one by one
            - as they are outputed.

        :param bool rstrip:
            Deactivates the rstrip of the output.
        """

        with subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            env=os.environ,
        ) as process:
            while True:
                # Note: we use rstrip() because we are paranoid :-)
                current_line = process.stdout.readline()

                if not current_line and process.poll() is not None:
                    break

                if rstrip:
                    yield self._decode_output(current_line.rstrip())
                else:
                    yield self._decode_output(current_line)

    def run_to_stdout(self) -> None:
        """
        Run the given command and print each line(s) to stdout.
        """

        for line in self.run(rstrip=False):
            sys.stdout.write(line)

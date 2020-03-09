"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

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
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import sys
from os import environ
from subprocess import PIPE, STDOUT, Popen


class Command:
    """
    Shell command execution.

    :param str command: The command to execute.
    :param str encoding: The encoding to use to decode the shell output.
    """

    def __init__(self, command, encoding="utf-8"):  # pragma: no cover
        # We set the default decoding type.
        self.decode_type = encoding

        if isinstance(command, list):
            # The given command is a list.

            # We construct the command we are going to run.
            self.command = " ".join(command)
        elif isinstance(command, str):
            # The given command is a string.

            # We set the command we are going to run.
            self.command = command.strip()
        else:
            raise NotImplementedError(
                "Unknown command type: `{}`".format(type(command))
            )

    def _decode_output(self, to_decode):
        """
        Decode the output of a shell command in order to be readable.

        :param bytes to_decode: Output of a command to decode.

        :return: The decoded output.
        :rtype: str
        """

        if to_decode:
            return to_decode.decode(self.decode_type)

        return ""

    def execute(self):
        """
        Execute the given command.

        :return: The output of the command.
        :rtype: str
        """

        # We initiate a process and parse the command to it.
        with Popen(
            self.command, stdout=PIPE, stderr=STDOUT, shell=True, env=environ
        ) as process:
            # We communicate the command and get the output and the error.
            (stdout, stderr) = process.communicate()

            if process.returncode != 0:  # pragma: no cover
                # The return code is different to 0.

                # We return the decoded error.
                return self._decode_output(stderr)

            # The return code (or exit code if you prefer) if equal to 0.

            # We return the decoded output of the executed command.
            return self._decode_output(stdout)

    def run(self, rstrip=True):
        """
        Run the given command and yield each line(s) one by one.

        .. note::
            The difference between this method and :func:`~PyFunceble.helpers.Command.execute`
            is that :func:`~PyFunceble.helpers.Command.execute` wait for the process to end
            in order to return its output while this method return each line one by one
            - as they are outputed.

        :param bool rstrip:
            Deactivates the rstrip of the output.
        """

        with Popen(
            self.command, stdout=PIPE, stderr=STDOUT, shell=True, env=environ
        ) as process:
            # We initiate a process and parse the command to it.

            while True:
                # We loop infinitly because we want to get the output
                # until there is none.

                # We get the current line from the process stdout.
                #
                # Note: we use rstrip() because we are paranoid :-)
                current_line = process.stdout.readline()

                if not current_line and process.poll() is not None:
                    # The current line is empty or equal to None.

                    # We break the loop.
                    break

                # The line is not empty nor equal to None.

                if rstrip:
                    # We encode and yield the current line
                    yield self._decode_output(current_line.rstrip())
                else:
                    # We encode and yield the current line
                    yield self._decode_output(current_line)

    def run_to_stdout(self):
        """
        Run the given command and print each line(s) to stdout.
        """

        for line in self.run(rstrip=False):
            sys.stdout.write(line)

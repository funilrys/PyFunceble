from subprocess import PIPE, Popen


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

        return to_decode.decode(self.decode_type)

    def execute(self):
        """
        Execute the given command.

        :return: The output of the command.
        :rtype: str
        """

        # We initiate a process and parse the command to it.
        process = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=True)

        # We communicate the command and get the output and the error.
        (output, error) = process.communicate()

        if process.returncode != 0:  # pragma: no cover
            # The return code is different to 0.

            # We return the decoded error.
            return self._decode_output(error)

        # The return code (or exit code if you prefer) if equal to 0.

        # We return the decoded output of the executed command.
        return self._decode_output(output)

    def run(self):
        """
        Run the given command and yield each line(s) one by one.

        .. note::
            The difference between this method and :func:`~PyFunceble.helpers.Command.execute`
            is that :func:`~PyFunceble.helpers.Command.execute` wait for the process to end
            in order to return its output while this method return each line one by one
            - as they are outputed.
        """

        with Popen(self.command, stdout=PIPE, shell=True) as process:
            # We initiate a process and parse the command to it.

            while True:
                # We loop infinitly because we want to get the output
                # until there is none.

                # We get the current line from the process stdout.
                #
                # Note: we use rstrip() because we are paranoid :-)
                current_line = process.stdout.readline().rstrip()

                if not current_line:
                    # The current line is empty or equal to None.

                    # We break the loop.
                    break

                # The line is not empty nor equal to None.

                # We encode and yield the current line
                yield self._decode_output(current_line)

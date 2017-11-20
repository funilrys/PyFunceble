#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This tool come along with PyFunceble. Its main purpose is to help installing or
reseting PyFunceble to its default states.
"""

#  _______           _______           _        _______  _______  ______
# (  ____ )|\     /|(  ____ \|\     /|( (    /|(  ____ \(  ____ \(  ___ \ ( \      (  ____ \
# | (    )|( \   / )| (    \/| )   ( ||  \  ( || (    \/| (    \/| (   ) )| (      | (    \/
# | (____)| \ (_) / | (__    | |   | ||   \ | || |      | (__    | (__/ / | |      | (__
# |  _____)  \   /  |  __)   | |   | || (\ \) || |      |  __)   |  __ (  | |      |  __)
# | (         ) (   | (      | |   | || | \   || |      | (      | (  \ \ | |      | (
# | )         | |   | )      | (___) || )  \  || (____/\| (____/\| )___) )| (____/\| (____/\
# |/          \_/   |/       (_______)|/    )_)(_______/(_______/|/ \___/ (_______/(_______/

# Written by: @Funilrys, Nissar Chababy <contact at funilrys dot com>
# GitHub : https://github.com/funilrys/PyFunceble

################################ Contributors ################################
# - All contributors of https://github.com/funilrys/Funceble
#
# - Let's contribute to PyFunceble !
##############################################################################

import argparse


class Check(object):
    """
    Check if depenndencies are satisfied or not.
    """

    def __init__(self):
        self.done = '✔'.encode('utf-8')
        self.error = '✘'.encode('utf-8')

        self.script()
        self.dependencies()

    def dependencies(self):
        """
        Check if all needed modules are installed.
        """

        list_of_dependencies = [
            'argparse',
            'os',
            'socket',
            're',
            'time',
            'requests']

        for dependency in list_of_dependencies:
            print(dependency + ' installed ', end=" ")

            try:
                __import__(dependency)
                print(self.done.decode('utf-8'))
            except ImportError:
                print(self.error.decode('utf-8'))

    def script(self):
        """
        Check if the script is needed.
        """

        from os import path
        from os import access, R_OK, X_OK

        location = './PyFunceble.py'

        print('Script exist', end=' ')
        if path.exists(location):
            print(self.done.decode('utf-8'))
        else:
            print(self.error.decode('utf-8'))
            exit(1)

        print('Script readable', end=' ')
        if access(location, R_OK):
            print(self.done.decode('utf-8'))
        else:
            print(self.error.decode('utf-8'))
            exit(1)

        print('Script executable', end=' ')
        if access(location, X_OK):
            print(self.done.decode('utf-8'))
        else:
            print(self.error.decode('utf-8'))
            exit(1)

        print('\n')


class Install(object):
    """
    Installations scripts.
    """

    def __init__(
            self,
            file_to_install=None,
            data_to_install=None,
            production=False):
        Check()

        from os import getcwd

        path = getcwd()

        if not path.endswith('/'):
            path += '/'

        self.path = path

        if file_to_install is None:
            self.file_to_install = 'PyFunceble.py'
        else:
            self.file_to_install = file_to_install

        self.file_to_install = self.path + self.file_to_install
        self.production = production
        self.data_to_install = data_to_install

        self.execute()

    def default_values(self):
        """
        Return PyFunceble's default variables values according to the
        current installation status (installation or production).
        """

        if self.production:
            return {
                'official_status_index': '5',
                'official_down_status': 'down_status[official_status_index]',
                'official_up_status': 'up_status[official_status_index]',
                'official_invalid_status': 'invalid_status[official_status_index]',
                'auto_continue': 'True',
                'command_before_end': "''",
                'custom_ip': "'0.0.0.0'",
                'debug': 'False',
                'domain': "''",
                'generate_hosts': 'True',
                'header_printed': 'False',
                'to_filter': "''",
                'less': 'False',
                'logs': 'True',
                'plain_list_domain': 'False',
                'quiet': 'False',
                'referer': "''",
                'seconds_before_http_timeout': '1',
                'show_execution_time': 'False',
                'show_percentage': 'True',
                'split_files': 'False',
                'travis': 'False',
                'travis_autosave_minutes': '15',
                'travis_autosave_commit': '"PyFunceble - Autosave"',
                'travis_autosave_final_commit': '"PyFunceble - Results"',
                'unified_file': 'True',
                'link_to_repo': "'https://github.com/funilrys/PyFunceble'",
                'iana_server': "'whois.iana.org'",
                'current_datetime': 'strftime("%a %d %b %H:%m:%S %Z %Y")',
                'number_of_tested': '0',
                'number_of_up': '0',
                'number_of_down': '0',
                'number_of_invalid': '0',
                'http_code_status': 'True',
                'http_code': "''",
                'cleaned_done': 'False',
                'no_files': 'False',
                'current_dir': "'%%current_dir%%'"}
        return {
            'current_dir': "'" + self.path + "'"
        }

    def execute(self):
        """
        Execute the installation or production logic.
        """

        from PyFunceble import Helpers as PyFuncebleHelpers

        replacement_production = {
            'to_replace': [
                'official_status_index',
                'official_down_status',
                'official_up_status',
                'auto_continue',
                'command_before_end',
                'custom_ip',
                'debug',
                'domain',
                'generate_hosts',
                'header_printed',
                'to_filter',
                'less',
                'logs',
                'plain_list_domain',
                'quiet',
                'referer',
                'seconds_before_http_timeout',
                'show_execution_time',
                'show_percentage',
                'split_files',
                'travis',
                'travis_autosave_minutes',
                'travis_autosave_commit',
                'travis_autosave_final_commit',
                'unified_file',
                'link_to_repo',
                'iana_server',
                'current_datetime',
                'number_of_tested',
                'number_of_up',
                'number_of_down',
                'number_of_invalid',
                'http_code_status',
                'http_code',
                'cleaned_done',
                'current_dir'
            ]
        }

        replacement_installation = {
            'current_dir': r"current_dir = '%%current_dir%%'"
        }

        replacement_list = {}

        if self.production:
            replacement_list = replacement_production
        else:
            replacement_list = replacement_installation

            if self.data_to_install is not None:
                replacement_list.update(self.data_to_install)

        script = PyFuncebleHelpers.File(
            self.file_to_install).read()

        for to_replace in replacement_list:
            if to_replace == 'to_replace' or to_replace == 'to_install':
                for variable in replacement_list[to_replace]:

                    if to_replace == 'to_install':
                        replacement = variable + ' = ' + \
                            str(replacement_list[to_replace][variable])
                    else:
                        replacement = variable + ' = ' + \
                            self.default_values()[variable]

                    script = PyFuncebleHelpers.Regex(
                        script,
                        variable + ' = .*',
                        replace_with=replacement,
                        occurences=1).replace()
            else:
                replacement = to_replace + ' = ' + \
                    self.default_values()[to_replace]

                script = PyFuncebleHelpers.Regex(
                    script,
                    replacement_list[to_replace],
                    replace_with=replacement,
                    occurences=1).replace()

        PyFuncebleHelpers.File(
            self.file_to_install).write(script, True)
        print('done')


class Clean(object):
    """
    Directory cleaning logic.
    """

    def __init__(self):
        self.them_all()

    @classmethod
    def file_to_delete(cls):
        """
        Return the list of file to delete.
        """

        from os import getcwd, walk

        directory = getcwd() + '/output/'
        result = []

        for root, dirs, files in walk(  # pylint: disable=unused-variable
                directory):
            for file in files:
                if file not in ['.gitignore', '.keep']:
                    if root.endswith('/'):
                        result.append(root + file)
                    else:
                        result.append(root + '/' + file)

        return result

    def them_all(self):
        """
        Delete all discovered files.
        """

        from PyFunceble import Helpers

        to_delete = self.file_to_delete()

        for file in to_delete:
            print(file)
            Helpers.File(file).delete()


class Uninstall(object):  # pylint: disable=too-few-public-methods
    """
    Uninstallation logic.
    """

    def __init__(self):
        from os import chdir, path
        from shutil import rmtree

        self.done = '✔'
        self.error = '✘'

        confirmation = input(
            'Do you really want to uninstall PyFunceble? (yes/no)')

        print('Deletion of funceble ')

        if confirmation == 'yes':
            current_file = __file__
            real_path = path.realpath(current_file)
            directory_path = path.dirname(real_path)
            directory_path = path.basename(directory_path)

            chdir('..')
            rmtree(directory_path)
            print(self.done + '\n\n')

            to_print = 'Thank you for having used PyFunceble!!\n\n'
            to_print += "Your're not satisfied by PyFuncebl?\n Please let me know there : %s"

            print(to_print % 'Unknown link')
            exit(0)
        else:
            print(self.error + '\n\n\n Thenk you for keeping PyFunceble !!\n\n')
            exit(0)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description=None,
        epilog="Crafted with \033[1m\033[31m♥\033[0m by \033[1mNissar Chababy (Funilrys)\033[0m")

    PARSER.add_argument(
        '--autosave-minutes',
        type=int,
        help="Replace the  minimum of minutes before we start commiting \
            to upstream under Travis CI."
    )
    PARSER.add_argument(
        '-c',
        '--clean',
        action='store_true',
        help='Clean all files under output.'
    )
    PARSER.add_argument(
        '--commit-autosave-message',
        type=str,
        help='Replace the default autosave commit message.'
    )
    PARSER.add_argument(
        '--commit-results-message',
        type=str,
        help='Replace the default results (final) commit message.'
    )
    PARSER.add_argument(
        '-del',
        '--delete',
        action='store_true',
        help='Uninstall PyFunceble and all its components.'
    )
    PARSER.add_argument(
        '-i',
        '--installation',
        action='store_false',
        help="Execute the installation script."
    )
    PARSER.add_argument(
        '-p',
        '--production',
        action='store_true',
        help="Prepare the repository for production."
    )

    ARGS = PARSER.parse_args()

    DATA = {'to_install': {}}

    if ARGS.autosave_minutes:
        DATA['to_install']['travis_autosave_minutes'] = ARGS.autosave_minutes

    if ARGS.clean:
        Clean()

    if ARGS.commit_autosave_message:
        DATA['to_install']['travis_autosave_commit'] = '"' + \
            ARGS.commit_autosave_message + '"'

    if ARGS.commit_results_message:
        DATA['to_install']['travis_autosave_final_commit'] = '"' + \
            ARGS.commit_results_message + '"'

    if not ARGS.installation:
        Install(None, DATA, ARGS.installation)
    elif ARGS.production:
        Install(None, DATA, ARGS.production)

    if ARGS.delete:
        Uninstall()

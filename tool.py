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
import hashlib


class Settings(object):
    """
    Scripts settings.
    """

    # Activate/Deactivate the download of the developement version of
    # PyFunceble.
    dev = True
    # Activate/Deactivate the download of the stable version of PyFunceble.
    stable = False
    # Funilrys
    funilrys = 'funilrys'
    # Script Name.
    script = 'PyFunceble'
    # Tool name.
    tool = 'tool'
    # GitHub raw.
    github_raw = 'https://raw.githubusercontent.com/' + \
        funilrys + '/' + script + '/master/'
    # Link to the online version of the script.
    online_script = github_raw + script + '.py'
    # Link to the online version of the tool.
    online_tool = github_raw + tool + '.py'
    # Activate/Deactivate quiet mode.
    quiet = False

    @classmethod
    def switch_version(cls, dev):
        """
        Switch Settings.dev and Settings.stable according to argparse.

        :param dev: A bool, the status to set to dev
        """

        Settings.dev = dev

        if dev:
            Settings.stable = False

            Settings.online_script = Settings.online_script.replace(
                'master', 'dev')
            Settings.online_tool = Settings.online_tool.replace(
                'master', 'dev')
        else:
            Settings.stable = True

        return


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
            if not Settings.quiet:
                print(dependency + ' installed ', end=" ")

            try:
                __import__(dependency)

                if not Settings.quiet:
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

        if not Settings.quiet:
            print('Script exist', end=' ')

        if path.exists(location) and not Settings.quiet:
            print(self.done.decode('utf-8'))
        else:
            if not Settings.quiet:
                print(self.error.decode('utf-8'))
            exit(1)

        if not Settings.quiet:
            print('Script readable', end=' ')
        if access(location, R_OK) and not Settings.quiet:
            print(self.done.decode('utf-8'))
        else:
            if not Settings.quiet:
                print(self.error.decode('utf-8'))
            exit(1)

        if not Settings.quiet:
            print('Script executable', end=' ')
        if access(location, X_OK) and not Settings.quiet:
            print(self.done.decode('utf-8'))
        else:
            if not Settings.quiet:
                print(self.error.decode('utf-8'))
            exit(1)

        if not Settings.quiet:
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


class Update(object):
    """
    Update logic.download_files
    """

    def __init__(self):
        from os import getcwd, path, rename
        from PyFunceble import Helpers

        self.current_path = getcwd()

        self.destination = self.current_path + Settings.funilrys + '.'

        self.files = {
            'script': 'PyFunceble.py',
            'tool': 'tool.py',
        }

        if path.isdir(
                self.current_path +
                '/.git') and Settings.script in Helpers.Command('git remote show origin').execute():
            self.git()
        else:
            if not self.check_version(True):
                for data in self.files:
                    Helpers.File(self.destination + self.files[data]).delete()
                    rename(
                        self.destination +
                        self.files[data],
                        self.current_path +
                        self.files[data])

                Helpers.Command('python tool.py -q -i').execute()

                print('Checking version', end=' ')
                if self.check_version():
                    print('✔\n\nThe update was successfully completed!')
                else:
                    print('✘\nImpossible to update PyFunceble. Please report issue.')
            else:
                print('No need to update.\n')

                for data in self.files:
                    Helpers.File(self.destination + self.files[data]).delete()

    @classmethod
    def git(cls):
        """
        Update repository if cloned (git).
        """

        from PyFunceble import Helpers

        if Settings.stable:
            Helpers.Command('git checkout master').execute()
        else:
            Helpers.Command('git checkout dev').execute()

        print(Helpers.Command('git pull').execute())
        return

    def update_permission(self):
        """
        Update the permissions of the downloaded files in order to be
        executable.
        """

        from os import chmod, stat
        from stat import S_IEXEC

        for data in self.files:
            stats = stat(self.destination + self.files[data])
            chmod(self.destination + self.files[data], stats.st_mode | S_IEXEC)

        return

    def download_files(self):
        """
        Download the online version of PyFunceble and tool.
        """

        print('\n Download of the scripts ')

        from shutil import copyfileobj
        from requests import get

        req = get(Settings.online_script, stream=True)
        req2 = get(Settings.online_tool, stream=True)

        if req.status_code == 200:
            with open(self.destination + self.files['script']) as file:
                copyfileobj(req.raw, file)

            with open(self.destination + self.files['tool']) as file:
                copyfileobj(req2.raw, file)

            del req
            del req

            self.update_permission()

            Settings.quiet = True

            return

        print(
            '✘\nImpossible to update %s.Please report issue.' %
            Settings.script)
        exit(1)

    @classmethod
    def hash(cls, file):
        """
        Get/return the sha512sum of the current PyFunceble.py.

        :param file: A string, the file to get the hash.
        """

        return Hash(file, 'sha512', True).get()

    def check_version(self, download=False):
        """
        Compare the current version to the online version.
        """

        if download:
            self.download_files()

        for file in self.files:
            current_version = self.hash(
                self.current_path + '/' + self.files[file])
            copied_version = self.hash(self.destination + self.files[file])

            if current_version != copied_version:
                return False

        return True


class Hash(object):
    """
    Get and return the hash a file with the given algorithm.

    :param path: A string, the path to the file we have to hash.
    :param algorithm: A string, the algorithm to use.
    :param only_hash: A bool, Return only the desired algorithm if algorithm != 'all'.

    :Note: Original version : https://git.io/vFQrK
    """

    def __init__(self, path, algorithm='sha512', only_hash=False):
        self.valid_algorithms = ['all', 'md5',
                                 'sha1', 'sha224', 'sha384', 'sha512']

        self.path = path
        self.algorithm = algorithm
        self.only_hash = only_hash

    def hash_data(self, algo):
        """Get the hash of the given file

        :param algo: A string, the algorithm to use.
        """

        hash_data = getattr(hashlib, algo)()

        with open(self.path, 'rb') as file:
            content = file.read()

            hash_data.update(content)
        return hash_data.hexdigest()

    def get(self):
        """
        Return the hash of the given file
        """

        from os import path

        result = {}

        if path.isfile(self.path) and self.algorithm in self.valid_algorithms:
            if self.algorithm == 'all':
                del self.valid_algorithms[0]
                for algo in self.valid_algorithms:
                    result[algo] = None
                    result[algo] = self.hash_data(algo)
            else:
                result[self.algorithm] = None
                result[self.algorithm] = self.hash_data(self.algorithm)
        else:
            return None

        if self.algorithm != 'all' and self.only_hash:
            return result[self.algorithm]
        return result


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
        '--dev',
        action='store_true',
        help='Activate the download of the developement version of PyFunceble.'
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
    PARSER.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='Split outputed files.'
    )
    PARSER.add_argument(
        '--stable',
        action='store_false',
        help=" Activate the download of the stable version of PyFunceble."
    )
    PARSER.add_argument(
        '-t',
        '--timeout',
        type=int,
        help="Set the default timeout in seconds."
    )
    PARSER.add_argument(
        '-u',
        '--update',
        action='store_true',
        help=" Update the scripts"
    )
    PARSER.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.0.1-beta'
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

    if ARGS.timeout:
        DATA['to_install']['seconds_before_http_timeout'] = ARGS.timeout

    if ARGS.dev:
        Settings().switch_version(ARGS.dev)

    if not ARGS.stable:
        Settings().switch_version(ARGS.stable)

    if ARGS.quiet:
        Settings.quiet = False

    if ARGS.update:
        Update()

    if not ARGS.installation:
        Install(None, DATA, ARGS.installation)
    elif ARGS.production:
        Install(None, DATA, ARGS.production)

    if ARGS.delete:
        Uninstall()

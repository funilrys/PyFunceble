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
# pylint: disable=too-many-lines,cyclic-import
import argparse
import hashlib
from os import sep as directory_separator
from os import (R_OK, X_OK, access, chdir, chmod, getcwd, mkdir, path, rename,
                stat, walk)

from colorama import init as initiate
from colorama import Fore, Style

from PyFunceble import Helpers


class Settings(object):  # pylint: disable=too-few-public-methods
    """
    Scripts settings.
    """

    ################################# Version ################################
    # Activate/Deactivate the download of the developement version of
    # PyFunceble.
    dev = True
    # Activate/Deactivate the download of the stable version of PyFunceble.
    stable = False
    ################################## Names #################################
    # Funilrys
    funilrys = 'funilrys'
    # Script Name.
    script = 'PyFunceble'
    # Tool name.
    tool = 'tool'
    ################################## Links #################################
    # GitHub raw.
    github_raw = 'https://raw.githubusercontent.com/' + \
        funilrys + '/' + script + '/master/'
    # Link to the online version of the script.
    online_script = github_raw + script + '.py'
    # Link to the online version of the tool.
    online_tool = github_raw + tool + '.py'
    # Link to the online version of the iana-domains-db.json.
    online_iana = github_raw + 'iana-domains-db.json'
    # IANA whois Server
    iana_server = 'whois.iana.org'
    # IANA DB url
    iana_url = 'https://www.iana.org/domains/root/db'
    # dir_structure.json url
    online_dir_structure = github_raw + 'dir_structure_production.json'
    # requirements.txt url
    online_requirements = github_raw + 'requirements.txt'
    # config_production.json url
    online_config = github_raw + 'config_production.yaml'
    ################################# Options ################################
    # Activate/Deactivate quiet mode.
    quiet = False
    ################################## Status ################################
    # Done string
    done = Fore.GREEN + '✔'
    # Error string
    error = Fore.RED + '✘'

    @classmethod
    def switch_version(cls, dev):
        """
        Switch Settings.dev and Settings.stable according to argparse.

        :param dev: A bool, the status to set to dev
        """

        Settings.dev = dev

        if dev:
            Settings.stable = False

        to_replace = [
            'online_script',
            'online_tool',
            'online_iana',
            'online_dir_structure',
            'online_requirements',
            'online_config'
        ]

        for var in to_replace:
            if dev:
                setattr(
                    Settings,
                    var,
                    getattr(
                        Settings,
                        var).replace(
                            'master',
                            'dev'))
            else:
                setattr(
                    Settings,
                    var,
                    getattr(
                        Settings,
                        var).replace(
                            'dev',
                            'master'))

        return


class Check(object):
    """
    Check if depenndencies are satisfied or not.
    """

    def __init__(self):
        self.script()
        self.dependencies()

    @classmethod
    def dependencies(cls):
        """
        Check if all needed modules are installed.
        """

        list_of_dependencies = [
            'argparse',
            'collections',
            'colorama',
            'json',
            'os',
            're',
            'requests',
            'socket',
            'subprocess',
            'sys',
            'time']

        for dependency in list_of_dependencies:
            if not Settings.quiet:
                print(
                    Style.BRIGHT +
                    dependency +
                    Style.RESET_ALL +
                    ' installed ',
                    end=" ")

            try:
                __import__(dependency)

                if not Settings.quiet:
                    print(Settings.done)
            except ModuleNotFoundError:
                print(Settings.error)
                exit(1)

    @classmethod
    def script_exist(cls, location):
        """
        Check if the given path exist.

        :param location: A string, a path to whatever file you want.
        """

        if path.exists(location) and not Settings.quiet:
            print(Settings.done)
        else:
            if not Settings.quiet:
                print(Settings.error)
            exit(1)

    @classmethod
    def script_readable(cls, location):
        """
        Check if the given path is readable.

        :param location: A string, a path to whatever file you want.
        """

        if access(location, R_OK) and not Settings.quiet:
            print(Settings.done)
        else:
            if not Settings.quiet:
                print(Settings.error)
            exit(1)

    @classmethod
    def script_executable(cls, location):
        """
        Check if the given path is executable.

        :param location: A string, a path to whatever file you want.
        """

        if access(location, X_OK) and not Settings.quiet:
            print(Settings.done)
        else:
            if not Settings.quiet:
                print(Settings.error)
            exit(1)

    def script(self):
        """
        Check if the script is needed.
        """

        location = getcwd() + directory_separator + 'PyFunceble.py'

        if not Settings.quiet:
            print('Script exist', end=' ')

        self.script_exist(location)

        if not Settings.quiet:
            print('Script readable', end=' ')

        self.script_readable(location)

        if not Settings.quiet:
            print('Script executable', end=' ')

        self.script_executable(location)

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

        _path = getcwd()

        if not _path.endswith(directory_separator):
            _path += directory_separator

        self.path = _path

        if file_to_install is None:
            self.file_to_install = 'PyFunceble.py'
        else:
            self.file_to_install = file_to_install

        self.file_to_install = self.path + self.file_to_install
        self.production = production
        self.data_to_install = data_to_install

        if self.production and not Settings.quiet:
            print('\nDefault timeout: %s seconds' %
                  self.default_values()['seconds_before_http_timeout'])
            print('Installation of default variables for production', end=" ")
        else:
            if not Settings.quiet:
                print('\n\nInstallation of working directory', end=" ")

        self.execute()

        regex_skip = r'\[PyFunceble\sskip\]|\[ci\sskip\]'
        if Helpers.Regex(
                Helpers.Command('git log -2').execute(),
                regex_skip,
                return_data=False).match() or self.production:
            Clean()

        Directory(self.production)

        if self.production and not Settings.quiet:
            print(
                Fore.CYAN +
                Style.BRIGHT +
                '\n\nThe production logic was successfully completed!')
            print('You can now distribute this repository.\n')
        else:
            if not Settings.quiet:
                print(
                    Fore.CYAN +
                    Style.BRIGHT +
                    '\n\nThe installation was successfully completed!')
                print(
                    "You can now use the script with '%s' or learn how to use it with '%s'\n" %  # pylint: disable=line-too-long
                    (Style.BRIGHT + './' + Settings.script + '.py [-OPTIONS]' + Style.RESET_ALL,
                     Style.BRIGHT + './' + Settings.script + '.py --help' + Style.RESET_ALL))

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
                'adblock': 'False',
                'auto_continue': 'True',
                'command_before_end': "''",
                'custom_ip': "'0.0.0.0'",
                'days_between_db_retest': '1',
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
                'seconds_before_http_timeout': '3',
                'share_logs': 'False',
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
            'current_dir': "'" + repr(self.path).strip("'") + "'"
        }

    def execute(self):
        """
        Execute the installation or production logic.
        """

        replacement_production = {
            'to_replace': [
                'official_status_index',
                'official_down_status',
                'official_up_status',
                'adblock',
                'auto_continue',
                'command_before_end',
                'custom_ip',
                'days_between_db_retest',
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
                'share_logs',
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

        script = Helpers.File(
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

                    script = Helpers.Regex(
                        script,
                        variable + ' = .*',
                        replace_with=replacement,
                        occurences=1).replace()
            else:
                replacement = to_replace + ' = ' + \
                    self.default_values()[to_replace]

                script = Helpers.Regex(
                    script,
                    replacement_list[to_replace],
                    replace_with=replacement,
                    occurences=1).replace()

        Helpers.File(
            self.file_to_install).write(script, True)

        if not Settings.quiet:
            print(Settings.done)


class Clean(object):
    """
    Directory cleaning logic.

    :param quiet: A boolean, True: run in quiet mode.
    """

    def __init__(self, quiet=False):
        if quiet:
            Settings.quiet = True
        if not Settings.quiet:
            print('\n\nCleaning generated files', end=" ")
        self.them_all()
        if not Settings.quiet:
            print(Settings.done)

    @classmethod
    def file_to_delete(cls):
        """
        Return the list of file to delete.
        """

        directory = getcwd() + directory_separator + 'output' + directory_separator
        result = []

        for root, dirs, files in walk(  # pylint: disable=unused-variable
                directory):
            for file in files:
                if file not in ['.gitignore', '.keep']:
                    if root.endswith(directory_separator):
                        result.append(root + file)
                    else:
                        result.append(root + directory_separator + file)

        return result

    def them_all(self):
        """
        Delete all discovered files.
        """

        to_delete = self.file_to_delete()

        for file in to_delete:
            Helpers.File(file).delete()


class Uninstall(object):  # pylint: disable=too-few-public-methods
    """
    Uninstallation logic.
    """

    def __init__(self):
        from shutil import rmtree

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

            print(Settings.done + '\n\n')

            to_print = 'Thank you for having used PyFunceble!!\n\n'
            to_print += "Your're not satisfied by PyFuncebl?\n Please let me know there : %s"

            print(to_print % 'Unknown link')
            exit(0)
        else:
            print(
                Settings.error +
                '\n\n\n Thenk you for keeping PyFunceble !!\n\n')
            exit(0)


class Update(object):
    """
    Update logic.download_files
    """

    def __init__(self):
        self.current_path = getcwd()

        self.destination = self.current_path + \
            directory_separator + Settings.funilrys + '.'

        self.files = {
            'script': 'PyFunceble.py',
            'tool': 'tool.py',
            'iana': 'iana-domains-db.json',
            'dir_structure': 'dir_structure_production.json',
            'config': 'config_production.yaml',
            'requirements': 'requirements.txt'
        }

        if path.isdir(
                self.current_path +
                directory_separator +
                '.git') and Settings.script in Helpers.Command('git remote show origin').execute():
            self.git()
        else:
            if not self.same_version(True):
                for data in self.files:
                    Helpers.File(
                        self.current_path +
                        directory_separator +
                        self.files[data]).delete()
                    rename(
                        self.destination +
                        self.files[data],
                        self.current_path +
                        directory_separator +
                        self.files[data])

                if not Settings.quiet:
                    print('Checking version', end=' ')
                if self.same_version() and not Settings.quiet:
                    Helpers.File('tool.py').delete()
                    print(
                        Settings.done +
                        '\n\nThe update was successfully completed!')
                else:
                    if not Settings.quiet:
                        print(
                            Settings.error +
                            '\nImpossible to update PyFunceble. Please report issue.')
            else:
                if not Settings.quiet:
                    print('No need to update.\n')

                for data in self.files:
                    Helpers.File(self.destination + self.files[data]).delete()

    @classmethod
    def git(cls):
        """
        Update repository if cloned (git).
        """

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

        from stat import S_IEXEC

        for data in self.files:
            if data not in ['iana', 'dir_structure']:
                stats = stat(self.destination + self.files[data])
                chmod(
                    self.destination +
                    self.files[data],
                    stats.st_mode | S_IEXEC)

        return

    def download_files(self):
        """
        Download the online version of PyFunceble and tool.
        """

        if not Settings.quiet:
            print('\nDownload of the scripts', end=' ')

        from shutil import copyfileobj
        from requests import get

        result = []

        for data in self.files:
            req = get(getattr(Settings, 'online_' + data), stream=True)

            if req.status_code == 200:
                with open(self.destination + self.files[data], 'wb') as file:
                    req.raw.decode_content = True
                    copyfileobj(req.raw, file)

                del req
                result.append(True)
            else:
                result.append(False)

        if False not in result:
            self.update_permission()
            return

        if not Settings.quiet:
            print(Settings.error)

            print(
                '\nImpossible to update %s. Please report issue.' %
                Settings.script)
            exit(1)

    @classmethod
    def hash(cls, file):
        """
        Get/return the sha512sum of the current PyFunceble.py.

        :param file: A string, the file to get the hash.
        """

        return Hash(file, 'sha512', True).get()

    def same_version(self, download=False):
        """
        Compare the current version to the online version.
        """

        if download:
            self.download_files()

        result = []

        for file in self.files:
            current_version = self.hash(
                self.current_path + directory_separator + self.files[file])
            copied_version = self.hash(self.destination + self.files[file])

            if copied_version is not None:
                if not download and current_version == copied_version:
                    result.append(True)
                else:
                    result.append(False)
            else:
                result.append(True)

        if True in result:
            return True
        return False


class IANA(object):
    """
    Logic behind the update of iana-domains-db.json
    """

    def __init__(self):
        if not Settings.quiet:
            print('Update of iana-domains-db', end=" ")
        self.download_destination = 'iana-db-dump'
        self.destination = 'iana-domains-db.json'

        self.update()

    def download(self):
        """
        Download the database from IANA website.
        """

        from shutil import copyfileobj
        from requests import get

        req = get(Settings.iana_url, stream=True)

        if req.status_code == 200:
            with open(self.download_destination, 'wb') as file:
                req.raw.decode_content = True
                copyfileobj(req.raw, file)
            del req

            return True
        return False

    @classmethod
    def referer(cls, extension):
        """
        Return the referer for the given extension.

        :pram extension: A string, a valid domain extension.
        """

        from PyFunceble import Lookup

        manual_server = {
            'aaa': 'whois.nic.aaa',
            'abb': 'whois.nic.abb',
            'able': 'whois.nic.able',
            'accenture': 'whois.nic.accenture',
            'aetna': 'whois.nic.aetna',
            'aig': 'whois.nic.aig',
            'americanexpress': 'whois.nic.americanexpress',
            'amex': 'whois.nic.amex',
            'amica': 'whois.nic.amica',
            'amsterdam': 'whois.nic.amsterdam',
            'analytics': 'whois.nic.analytics',
            'aramco': 'whois.nic.aramco',
            'athleta': 'whois.nic.athleta',
            'audible': 'whois.nic.audible',
            'author': 'whois.nic.author',
            'aws': 'whois.nic.aws',
            'axa': 'whois.nic.axa',
            'azure': 'whois.nic.azure',
            'baby': 'whois.nic.baby',
            'banamex': 'whois.nic.banamex',
            'bananarepublic': 'whois.nic.bananarepublic',
            'baseball': 'whois.nic.baseball',
            'bharti': 'whois.nic.bharti',
            'bing': 'whois.nic.bing',
            'bloomberg': 'whois.nic.bloomberg',
            'bm': 'whois.afilias-srs.net',
            'book': 'whois.nic.book',
            'booking': 'whois.nic.booking',
            'bot': 'whois.nic.bot',
            'bz': 'whois.afilias-grs.net',
            'buzz': 'whois.nic.buzz',
            'call': 'whois.nic.call',
            'calvinklein': 'whois.nic.calvinklein',
            'caravan': 'whois.nic.caravan',
            'cartier': 'whois.nic.cartier',
            'cbn': 'whois.nic.cbn',
            'cbre': 'whois.nic.cbre',
            'cd': 'chois.nic.cd',
            'chase': 'whois.nic.chase',
            'circle': 'whois.nic.circle',
            'cisco': 'whois.nic.cisco',
            'citadel': 'whois.nic.citadel',
            'citi': 'whois.nic.citi',
            'citic': 'whois.nic.citic',
            'cm': 'whois.netcom.cm',
            'coupon': 'whois.nic.coupon',
            'crown': 'whois.nic.crown',
            'crs': 'whois.nic.crs',
            'fj': 'whois.usp.ac.fj',
            'ga': 'whois.my.ga',
            'gh': 'whois.nic.gh',
            'int': 'whois.iana.org',
            'kw': 'whois.nic.kw',
            'lc': 'whois2.afilias-grs.net',
            'lk': 'whois.nic.lk',
            'microsoft': 'whois.nic.microsoft',
            'nagoya': 'whois.nic.nagoya',
            'nyc': 'whois.nic.nyc',
            'ps': 'whois.pnina.ps',
            'ren': 'whois.nic.ren',
            'rw': 'whois.ricta.org.rw',
            'shop': 'whois.nic.shop',
            'sl': 'whois.nic.sl',
            'stream': 'whois.nic.stream',
            'tokyo': 'whois.nic.tokyo',
            'uno': 'whois.nic.uno',
            'za': 'whois.registry.net.za'
        }

        if extension in manual_server:
            return manual_server[extension]
        else:
            whois_record = Lookup().whois(Settings.iana_server, 'hello.' + extension, 10)

            if whois_record is not None:
                regex_referer = r'(refer:)\s+(.*)'

                if Helpers.Regex(
                        whois_record,
                        regex_referer,
                        return_data=False).match():
                    return Helpers.Regex(
                        whois_record,
                        regex_referer,
                        return_data=True,
                        group=2).match()
            return None

    def get_valid_extensions(self):
        """
        Get the list of valid extensions based on the result of self.download().
        """

        result = {}
        regex_valid_extension = r'(/domains/root/db/)(.*)(\.html)'

        for readed in open(self.download_destination):
            readed = readed.rstrip('\n').strip()

            matched = Helpers.Regex(
                readed,
                regex_valid_extension,
                return_data=True,
                rematch=True).match()

            if not matched:
                continue
            else:
                ext_with_referer = {matched[1]: self.referer(matched[1])}
                result.update(ext_with_referer)

        Helpers.File(self.download_destination).delete()
        Helpers.File(self.destination).delete()
        return result

    def update(self):
        """
        Update the content of the `iana-domains-db` file.
        """

        if self.download():
            Helpers.Dict(self.get_valid_extensions()).to_json(self.destination)

            if not Settings.quiet:
                print(Settings.done)
        else:
            if not Settings.quiet:
                print(Settings.error)
            exit(1)


class Directory(object):
    """
    Consider this class as a backup/reconstructor of desired directory.
    (By default, the output direcctory)
    """

    def __init__(self, production=False):
        self.base = getcwd() + directory_separator

        self.path = 'output' + directory_separator
        self.structure = self.base + 'dir_structure.json'

        if production:
            self.backup()
        else:
            if not path.isfile(self.structure):
                self.download()

            self.restore()

    def backup(self):
        """
        Backup the developer state of `output/` in order to make it restorable
            and portable for user.
        """

        result = {'output': {}}

        if not Settings.quiet:
            print('Generation of dir-structure.json', end=" ")

        for root, _, files in walk(self.path):
            directories = root.split(self.path)[1]

            local_result = result['output']

            for file in files:
                file_path = root + directory_separator + file
                file_hash = Hash(file_path, 'sha512', True).get()

                lines_in_list = [line.rstrip('\n') for line in open(file_path)]
                formated_content = ''

                for line in lines_in_list:
                    if line != lines_in_list[-1]:
                        formated_content += line + '@@@'
                    else:
                        formated_content += line
                local_result = local_result.setdefault(
                    directories, {file: {'sha512': file_hash, 'content': formated_content}})

            Helpers.Dict(result).to_json(self.structure)

        if not Settings.quiet:
            print(Settings.done)

    def download(self):
        """
        Download the `dir_structure.json` from the repository upstream.
        """

        from shutil import copyfileobj
        from requests import get

        req = get(Settings.online_dir_structure, stream=True)

        if req.status_code == 200:
            with open(self.structure, 'wb') as file:
                req.raw.decode_content = True
                copyfileobj(req.raw, file)
            del req

            return True
        return False

    def restore_replace(self):
        """
        Check if we need to replace ".gitignore" to ".keep".
        """

        if path.isdir(self.base + '.git'):
            if Settings.script not in  \
                    Helpers.Command('git remote show origin').execute():
                return True
            return False
        return True

    @classmethod
    def travis_permissions(cls):
        """
        Set permissions in order to avoid issues before commiting.
        """

        try:
            build_dir = environ['TRAVIS_BUILD_DIR']
            commands = [
                'sudo chown -R travis:travis %s' %
                (build_dir),
                'sudo chgrp -R travis %s' %
                (build_dir),
                'sudo chmod -R g+rwX %s' %
                (build_dir),
                'sudo chmod 777 -Rf %s.git' %
                (build_dir +
                 directory_separator),
                r"sudo find %s -type d -exec chmod g+x '{}' \;" %
                (build_dir)]

            for command in commands:
                Helpers.Command(command).execute()

            if Helpers.Command(
                    'git config core.sharedRepository').execute() == '':
                Helpers.Command(
                    'git config core.sharedRepository group').execute()
        except NameError:
            pass

        return

    def restore(self):
        """
        Restore the 'output/' directory structure based on the `dir_structure.json` file.
        """

        if not Settings.quiet:
            print('Creation of non existant files and directories', end=" ")

        structure = Helpers.Dict().from_json(Helpers.File(self.structure).read())

        structure = structure['output']
        replace = self.restore_replace()

        for directory in structure:
            if not path.isdir(self.base + self.path + directory):
                self.travis_permissions()
                mkdir(self.base + self.path + directory)
                self.travis_permissions()

            for file in structure[directory]:
                file_path = self.path + directory + directory_separator + file

                content_to_write = structure[directory][file]['content']
                online_sha = structure[directory][file]['sha512']
                content_to_write = Helpers.Regex(
                    content_to_write, '@@@', escape=True, replace_with='\\n').replace()

                git_to_keep = file_path.replace('gitignore', 'keep')
                keep_to_git = file_path.replace('keep', 'gitignore')

                if replace:
                    if path.isfile(file_path) and Hash(
                            file_path, 'sha512', True).get() == online_sha:
                        rename(file_path, git_to_keep)
                        write = False
                    else:
                        Helpers.File(file_path).delete()
                        file_path = git_to_keep
                        write = True
                else:
                    if path.isfile(keep_to_git) and Hash(
                            file_path, 'sha512', True).get() == online_sha:
                        rename(file_path, keep_to_git)
                        write = False
                    else:
                        Helpers.File(keep_to_git).delete()
                        file_path = keep_to_git
                        write = True

                if write:
                    Helpers.File(file_path).write(
                        content_to_write + '\n', True)

        if not Settings.quiet:
            print(Settings.done)


class Hash(object):
    """
    Get and return the hash a file with the given algorithm.

    :param path: A string, the path to the file we have to hash.
    :param algorithm: A string, the algorithm to use.
    :param only_hash: A bool, Return only the desired algorithm if algorithm != 'all'.

    :Note: Original version : https://git.io/vFQrK
    """

    def __init__(self, path, algorithm='sha512', only_hash=False):  # pylint: disable=redefined-outer-name
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
        description='This is the tool that comes with the awesome PyFunceble !!"',
        epilog="Crafted with %s by %s\033[0m " %
        (Fore.RED +
         '♥' +
         Fore.RESET,
         Style.BRIGHT +
         'Nissar Chababy (Funilrys)'))

    PARSER.add_argument(
        '-ad',
        '--adblock',
        action='store_true',
        help='Activate the systematic decoding of the adblock format.')
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
        '-dbr',
        '--days-between-db-retest',
        type=int,
        help="Set the numbers of day(s) between each retest of domains present \
        into inactive-db.json"
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
        '--directory-structure',
        action='store_false',
        help='Generate the directory and files that are needed and which does \
            not exist in the current directory.'
    )
    PARSER.add_argument(
        '-i',
        '--installation',
        action='store_false',
        help="Execute the installation script."
    )
    PARSER.add_argument(
        '--iana',
        action='store_true',
        help="Update `iana-domains-db`."
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
        '--share-logs',
        '-sl',
        action='store_true',
        help="Activate the sharing of logs to an API which helps manage logs in \
            order to make PyFunceble a better script."
    )
    PARSER.add_argument(
        '--stable',
        action='store_false',
        help="Activate the download of the stable version of PyFunceble."
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
        version='%(prog)s 0.13.0-beta'
    )

    ARGS = PARSER.parse_args()
    initiate(autoreset=True)

    DATA = {'to_install': {}}

    if ARGS.adblock:
        DATA['to_install']['adblock'] = ARGS.adblock

    if ARGS.autosave_minutes:
        DATA['to_install']['travis_autosave_minutes'] = ARGS.autosave_minutes

    if ARGS.commit_autosave_message:
        DATA['to_install']['travis_autosave_commit'] = '"' + \
            ARGS.commit_autosave_message + '"'

    if ARGS.commit_results_message:
        DATA['to_install']['travis_autosave_final_commit'] = '"' + \
            ARGS.commit_results_message + '"'

    if ARGS.days_between_db_retest:
        DATA['to_install']['days_between_db_retest'] = ARGS.days_between_db_retest

    if ARGS.timeout:
        DATA['to_install']['seconds_before_http_timeout'] = ARGS.timeout

    if ARGS.share_logs:
        DATA['to_install']['share_logs'] = ARGS.share_logs

    if ARGS.dev:
        Settings().switch_version(ARGS.dev)

    if not ARGS.stable:
        Settings().switch_version(ARGS.stable)

    if ARGS.quiet:
        Settings.quiet = True

    if ARGS.clean:
        Clean()

    if ARGS.update:
        Update()

    if ARGS.iana:
        IANA()

    if not ARGS.directory_structure:
        Directory(ARGS.directory_structure)

    if not ARGS.installation:
        Install(None, DATA, ARGS.installation)
    elif ARGS.production:
        Install(None, None, ARGS.production)

    if ARGS.delete:
        Uninstall()

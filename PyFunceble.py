#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyFunceble is the litle sister of Funceble (https://github.com/funilrys/PyFunceble).
Consider PyFunceble as a tool to check the status of a given domain name
or IP.
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
##########################################################################
# pylint: disable=too-many-lines
import argparse
import socket
from json import decoder, dump, loads
from os import environ, path, remove
from re import compile as comp
from re import sub as substrings
from re import escape
from subprocess import PIPE, Popen
from time import strftime

import requests
from colorama import init as initiate
from colorama import Back, Fore, Style


class Settings(object):  # pylint: disable=too-few-public-methods
    """
    Serve as "saver" of all needed settings or parameters.
    """

    ################################# Status #################################
    # Default index for "official" returned status.
    # Why 5 ? Simply luck I started to write the status and it's appears that the
    # fifth index is simply what we used in Funceble.
    official_status_index = 5
    # List of valid down status.
    down_status = ['down', 'Down', 'DOWN', 'inactive',
                   'Inactive', 'INACTIVE', 'error', 'Error', 'ERROR']
    # Official down status.
    official_down_status = down_status[official_status_index]
    # List of valid up status.
    up_status = [
        'up',
        'Up',
        'UP',
        'active',
        'Active',
        'ACTIVE',
        'valid',
        'Valid',
        'VALID']
    # Official up status.
    official_up_status = up_status[official_status_index]
    # List of valid invalid status.
    invalid_status = ['ouch', 'Ouch', 'OUCH', 'invalid', 'Invalid', 'INVALID']
    # Official invalid status.
    official_invalid_status = invalid_status[official_status_index]
    # Generic status.
    # Why generic ? Good question that the first word who come to discribed the
    # unified table system.
    generic_status = ['generic', 'Generic', 'GENERIC']
    # Potentionally up status
    # Why potentially ? Please note: https://git.io/vFttS
    # I consider them as potentially because for example we can't be sure that
    # a 403 HTTP status code represent an 'INACTIVE' domain.
    potentialy_up_status = ['potentially_up', 'potentially_active']
    # Potentially down status
    # As an example, We can't be sure that a 400 HTTP status code result
    # represent an 'INACTIVE' domain.
    potentially_down_status = ['potentially_down', 'potentially_inactive']
    # Active status
    # As exemple, we are sure that a 200 HTTP status code represent an
    # 'ACTIVE' domain.
    http_active_status = [
        'http_active',
        'HTTP_ACTIVE',
        'HTTP_active',
        'HTTP_Active']
    ##########################################################################
    ################################ Defaults ################################
    # Activation/Deactivation of the autocontinue system.
    auto_continue = True
    # We use are going to use this variable is order to pass some command before
    # the final commit in case auto_continue = True.
    command_before_end = ''
    # Set the custom IP in case we need to generate hosts files according to our
    # results.
    custom_ip = '0.0.0.0'
    # Generate debug file if logs are activated.
    debug = False
    # This will save the domain that is currently under test.
    domain = ''
    # Activate/Deactivate the generation of hosts file.
    generate_hosts = True
    # Used to check if the header has been already printed on screen.
    header_printed = False
    # Domain to filter. For example \.blogspot\. will test only blogspot.*
    # domains.
    to_filter = ''
    # Activate/Deactive the output of every informations.
    less = False
    # Activate/Deactivate the output of logs.
    logs = True
    # Activate/Deactivate the usage of WHOIS.
    no_whois = False
    # Activate/Deactivate the generation of plain list of domains accoding to
    # out status.
    plain_list_domain = False
    # Activate/Deactive the quiet mode.
    quiet = False
    # The following will save the referer
    referer = ''
    # HTTP Status code timeout.
    # Consider this as the minimum time in seconds that we need before.
    seconds_before_http_timeout = 3
    # Show/hide execution time
    show_execution_time = False
    # Show/hide the percentage.
    show_percentage = True
    # If set to true, we generate the files into the 'splited/' directory.
    split_files = False
    # Activation/Deactivation of Travis CI autosave system.
    travis = False
    # Minimum of minutes before we start commiting to upstream under Travis CI.
    travis_autosave_minutes = 15
    # Default travis final commit message
    travis_autosave_final_commit = "PyFunceble - Results"
    # Default travis commit message
    travis_autosave_commit = "PyFunceble - Autosave"
    # Output into unified files.
    unified_file = True
    ##########################################################################
    ############################ Links / Servers #############################
    # Link of the repository.
    link_to_repo = 'https://github.com/funilrys/PyFunceble'
    # IANA whois Servers.
    iana_server = 'whois.iana.org'
    ##########################################################################
    ################################## Time ##################################
    # Current date & Time.
    current_datetime = strftime("%a %d %b %H:%m:%S %Z %Y")
    ##########################################################################
    ################################# Counter ################################
    # Counter of the number of tested.
    number_of_tested = 0
    # Counter of the number of active/up.
    number_of_up = 0
    # Counter of the number of inactive/down.
    number_of_down = 0
    # Counter of the number of invalid.
    number_of_invalid = 0
    # Percentage of active/up.
    percentage_of_up = 0
    # Percentage of inactive/down.
    percentage_of_down = 0
    # Percentage of invalid.
    percentage_of_invalid = 0
    ##########################################################################
    ################################ HTTP Code ###############################
    # Activate/Deactivate the used of the http code.
    http_code_status = True
    # The following will get the http code
    http_code = ''
    # Active considered codes.
    # Note that if nslookup = inactive and http code is in the following list,
    # We set the domain to active.
    active_http_codes = [100, 101, 200, 201, 202, 203, 204, 205, 206]
    # Potentially active codes.
    potentially_up_codes = [
        000,
        300,
        301,
        302,
        303,
        304,
        305,
        307,
        403,
        405,
        406,
        407,
        408,
        411,
        413,
        417,
        500,
        501,
        502,
        503,
        504,
        505]
    # Potentially inactive codes.
    down_potentially_codes = [400, 402, 403, 404, 409, 410, 412, 414, 415, 416]
    ##########################################################################
    ########################### File Manipulation ############################
    # Used to check if we already cleaned the given file.
    cleaned_done = False
    # If set to True, we don't generate any files.
    # Please note: This does not apply to hosts files.
    no_files = False
    ##########################################################################
    ################################# Outputs ################################
    # Note: DO NOT FORGET `/` AT THE END.

    # Current directory.
    current_dir = '%%current_dir%%'
    # Output directory.
    # DO NOT UPDATE THIS UNLESS YOU KNOW WHAT YOU ARE DOING.
    output_dir = current_dir + 'output/'
    # Autocontinue log file.
    # Please note that this file is != from Funceble.
    autocontinue_log_file = output_dir + 'continue.json'
    # Output of unified results.
    # Please note that this the default output unless Settings.split_files is
    # activated.
    output_unified_results = output_dir + 'results.txt'

    ##########################################################################
    #                               `output/domains/`
    # This directory will keep the plain list of domain to their
    # official status.
    ##########################################################################
    # Domains directory.
    domains_dir = output_dir + 'domains/'
    # Default filename.
    domains_default_filename = 'list'
    # ACTIVE/Up domains directory.
    up_domains_dir = domains_dir + official_up_status + '/'
    # INACTIVE/Down domains directory.
    down_domains_dir = domains_dir + official_down_status + '/'
    # INVALID domains directory.
    invalid_domains_dir = domains_dir + official_invalid_status + '/'
    # Output of ACTIVE/Up domains.
    output_up_domain = up_domains_dir + domains_default_filename
    # Output of INACTIVE/Down domains.
    output_down_domain = down_domains_dir + domains_default_filename
    # Output of INVALID domains.
    output_invalid_domain = invalid_domains_dir + domains_default_filename

    ##########################################################################
    #                               `output/hosts/`
    # This directory will keep the generated hosts files according to their
    # official status.
    ##########################################################################
    # hosts directory.
    hosts_dir = output_dir + 'hosts/'
    # Default filename.
    hosts_default_filename = 'hosts'
    # ACTIVE/Up hosts directory.
    up_hosts_dir = hosts_dir + official_up_status + '/'
    # INACTIVE/Down hosts directory.
    down_hosts_dir = hosts_dir + official_down_status + '/'
    # INVALID hosts directory.
    invalid_hosts_dir = hosts_dir + official_invalid_status + '/'
    # Output of ACTIVE/Up hosts.
    output_up_host = up_hosts_dir + hosts_default_filename
    # Output of INACTIVE/Down hosts.
    output_down_host = down_hosts_dir + hosts_default_filename
    # Output of INVALID hosts.
    output_invalid_host = invalid_hosts_dir + hosts_default_filename

    ##########################################################################
    #                               `output/logs/`
    # This directory will keep all generated logs of the current session
    # if Settings.logs is activated.
    ##########################################################################
    # logs directory.
    logs_dir = output_dir + 'logs/'
    # WHOIS logs output.
    # Please note that this directory will keep the whois records according to
    # WHOIS server only if Settings.debug is activated.
    whois_logs_dir = logs_dir + 'whois/'
    # Wrong date format logs output.
    # Please note thet this directory will keep a record of all wrong formated
    # date.
    date_format_logs_dir = logs_dir + 'date_format/'
    # Percentages logs.
    # Please note that this directory will keep the percentage of the current
    # session.
    percentage_logs_dir = logs_dir + 'percentage/'
    # Output of percentae logs.
    output_percentage_log = percentage_logs_dir + 'percentage.txt'
    # Execution time logs.
    # Please note that this file is generated when Settings.show_execution_time
    # is activated.
    execution_time_logs = logs_dir + 'execution.log'
    # No referer logs.
    # Please note that this directory will keep a record of all domains
    # extensions which don't have any known referer.
    no_referer_logs_dir = logs_dir + 'no_referer/'

    ##########################################################################
    #                               `output/splited/`
    # This directory will keep all the results of execution according to
    # the different matched status.
    # Please note that this only works if Settings.split_files is activated.
    ##########################################################################
    # Splited directory.
    output_splited_results = output_dir + 'splited/'
    # Output of ACTIVE/Up results.
    output_up_result = output_splited_results + official_up_status
    # Output of INACTIVE/Down results.
    output_down_result = output_splited_results + official_down_status
    # Output of INVALID results.
    output_invalid_result = output_splited_results + official_invalid_status

    ##########################################################################
    #                               `output/HTTP_Analytic/`
    # This directory will keep all the results of the HTTP status code
    # analyze.
    # Please note that this only works if Settings.http_code_status
    # is activated.
    ##########################################################################
    # HTTP analytic directory.
    output_http_analytic = output_dir + 'HTTP_Analytic/'
    # Active HTTP codes directory.
    http_up = output_http_analytic + official_up_status + '/'
    # Output of Active codes.
    # Please note that a domain is set into the following file only if
    # the official status is not normally `ACTIVE`.
    # Please also note that the domains listed here are automatically set
    # into all ACTIVE results files.
    output_http_up = http_up + official_up_status
    # Potentially active codes directory.
    http_potentially_up = output_http_analytic + 'POTENTIALLY_ACTIVE/'
    # Output of potentially active codes.
    output_http_potentially_up = http_potentially_up + 'potentially_active'
    # Potentially inactive codes directory.
    http_potentially_down = output_http_analytic + 'POTENTIALLY_INACTIVE/'
    # Output of potentially inactive codes.
    output_http_potentially_down = http_potentially_down + 'inactive_or_potentially'

    @classmethod
    def switch(cls, variable):
        """
        Switch class variables to their opposite.
        """

        links = {
            'auto_continue': 'https://git.io/v7xma',
            'debug': 'https://git.io/v7xmD',
            'show_execution_time': 'Unknown',
            'generate_hosts': 'Unknown',
            'http_code_status': 'https://git.io/v5vHm',
            'no_files': 'Unknown',
            'logs': 'Unknown',
            'unified_file': 'Unknown',
            'no_whois': 'Unknown',
            'percentage': 'https://git.io/v7xtP',
            'plain_list_domain': 'Unknown',
            'quiet': 'Unknown',
            'split_files': 'Unknown',
            'travis': 'Unknown'
        }

        current_state = getattr(Settings, variable)

        if current_state is True:
            return False
        elif current_state is False:
            return True

        to_print = 'Your configuration is not valid.\n'
        to_print += 'Please use the auto update or post an issue to %s'

        print(to_print % links[variable])
        exit(1)


class PyFunceble(object):
    """
    Main entry to Funceble. Brain of the program. Also known as "put everything
    together to make the system works".

    :param domain: A string, a domain or IP to test.
    :param file_path: A string, a path to a file to read.
    """

    def __init__(self, domain=None, file_path=None):

        ExecutionTime('start')

        if domain is not None and domain != '':
            self.domain(domain)

        elif file_path is not None and file_path != '':
            self.file(file_path)

        ExecutionTime('stop')
        Percentage().log()

    @classmethod
    def print_header(cls):
        """
        Decide if we print or not the header.
        """

        if not Settings.quiet:
            print('\n')
            if Settings.less:
                Prints(None, 'Less').header()
            else:
                Prints(None, 'Generic').header()

    def domain(self, domain):
        """
        Manage the case that we want to test only a domain.

        :param domain: A string, a domain or IP to test.
        """

        Settings.domain = domain.lower()

        self.print_header()
        ExpirationDate()

    @classmethod
    def reset_counters(cls):
        """
        Reset the counters when needed.
        """

        for string in [
                'number_of_up',
                'number_of_down',
                'number_of_invalid',
                'number_of_tested']:
            setattr(Settings, string, 0)

        return

    def file(self, file_path):
        """
        Manage the case that need to test each domain of a given file path.
        Note: 1 domain per line.

        :param file_path: A string, a path to a file to read.
        """

        list_to_test = []

        AutoContinue().restore(file_path)
        self.print_header()

        for read in open(file_path):
            read = read.rstrip('\n').strip()

            if not read.startswith('#'):
                list_to_test.append(read)

        if Settings.number_of_tested == 0 or list_to_test[
                Settings.number_of_tested - 1] == list_to_test[-1]:
            self.reset_counters()

        i = int(Settings.number_of_tested)

        while i < len(list_to_test):
            domain = list_to_test[i]

            if Settings.to_filter != '' and not Helpers.Regex(
                    domain, Settings.to_filter, return_data=False, escape=True).match():
                continue

            regex_listing = [
                r'.*localhost.*',
                r'.*local.*',
                r'.*broadcasthost.*']
            match_result = []

            for regx in regex_listing:
                match_result.append(
                    Helpers.Regex(
                        domain,
                        regx,
                        return_data=False).match())

            domain = domain.rstrip('\n')

            regex_ip = r'127\.0\.0\.1'
            regex_ip2 = r'0\.0\.0\.0'

            space = ' '
            double_space = space * 2

            if domain == '' or True in match_result:
                i += 1
                continue
            elif Helpers.Regex(domain, regex_ip, return_data=False).match() \
                    or Helpers.Regex(domain, regex_ip2, return_data=False).match():
                if double_space in domain:
                    domain = domain.split(double_space)[1]
                elif space in domain:
                    domain = domain.split(' ')[1]
            else:
                if double_space in domain:
                    domain = domain.split(double_space)[0]
                elif space in domain:
                    domain = domain.split(' ')[0]

            Settings.domain = domain.split('#')[0]

            ExpirationDate()
            AutoContinue().backup(file_path)
            AutoSave()

            i += 1

        AutoSave(True)


class AutoContinue(object):
    """
    Autocontinue logic/subsystem.
    """

    def __init__(self):
        if Settings.auto_continue:
            if path.isfile(Settings.autocontinue_log_file):
                self.backup_content = Helpers.Dict().from_json(
                    Helpers.File(Settings.autocontinue_log_file).read())
            else:
                self.backup_content = {}
                Helpers.File(Settings.autocontinue_log_file).write(
                    str(self.backup_content))

    def backup(self, file_path):
        """
        Backup the current execution state.

        :param file_path: The path of the currently tested file.
        """

        if Settings.auto_continue:
            data_to_backup = {}
            data_to_backup[file_path] = {
                "number_of_tested": Settings.number_of_tested,
                "number_of_up": Settings.number_of_up,
                "number_of_down": Settings.number_of_down,
                "number_of_invalid": Settings.number_of_invalid
            }

            to_save = {}

            to_save.update(self.backup_content)
            to_save.update(data_to_backup)

            Helpers.Dict(to_save).to_json(Settings.autocontinue_log_file)

    def restore(self, file_to_restore):
        """
        Restore data from the given path.

        :param file_to_restore: A string, a path to file to test.
        """

        if Settings.auto_continue and self.backup_content != {}:
            if file_to_restore in self.backup_content:
                to_initiate = [
                    'number_of_up',
                    'number_of_down',
                    'number_of_invalid',
                    'number_of_tested']

                for string in to_initiate:
                    setattr(
                        Settings,
                        string,
                        self.backup_content[file_to_restore][string])


class AutoSave(object):
    """
    Logic behind autosave.
    """

    def __init__(self, last_domain=False):
        if Settings.travis:
            self.last = last_domain
            self.travis()

    @classmethod
    def travis_permissions(cls):
        """
        Set permissions in order to avoid issues before commiting.
        """

        build_dir = environ['TRAVIS_BUILD_DIR']
        commands = [
            'chown -R travis:travis ' + build_dir,
            'chgrp -R travis ' + build_dir,
            'chmod -R g+rwX ' + build_dir,
            'chmod 777 -Rf ' + build_dir + '/.git',
            'find ' + build_dir + " -type d -exec chmod g+x '{}'"
        ]

        for command in commands:
            Helpers.Command(command).execute()

        if Helpers.Command('git config core.sharedRepository').execute() == '':
            Helpers.Command('git config core.sharedRepository group').execute()

        return

    def travis(self):
        """
        Logic behind travis autosave.
        """

        current_time = int(strftime('%s'))
        time_of_start = int(Settings.start) + \
            (int(Settings.travis_autosave_minutes) * 60)

        if current_time >= time_of_start or self.last:
            Percentage().log()
            self.travis_permissions()

            command = 'git add --all && git commit -a -m "%s"'

            if self.last:
                if Settings.command_before_end != '':
                    Helpers.Command(Settings.command_before_end).execute()

                message = Settings.travis_autosave_final_commit + ' [ci skip]'

                Helpers.Command(command % message).execute()
            else:
                Helpers.Command(command %
                                Settings.travis_autosave_commit).execute()

            Helpers.Command('git push origin master').execute()
            exit(0)
        return


class ExecutionTime(object):
    """
    Set and return the exection time of the program.

    :param action: A string, 'start' or 'stop'.
    :param return_result: A boolean, if true, we return the executionn time.
    """

    def __init__(self, action='start'):
        if Settings.show_execution_time or Settings.travis:
            if action == 'start':
                self.starting_time()
            elif action == 'stop':
                self.stoping_time()

                print('\nExecution Time:')
                print(self.format_execution_time())

    @classmethod
    def starting_time(cls):
        """
        Set the starting time.
        """

        Settings.start = int(strftime('%s'))

    @classmethod
    def stoping_time(cls):
        """
        Set the ending time.
        """

        Settings.end = int(strftime('%s'))

    @classmethod
    def calculate(cls):
        """
        calculate the difference between starting and ending time.
        """

        time_difference = Settings.end - Settings.start

        return {
            'days': str((time_difference // 24) % 24).zfill(2),
            'hours': str(time_difference // 3600).zfill(2),
            'minutes': str((time_difference % 3600) // 60).zfill(2),
            'seconds': str(time_difference % 60).zfill(2)
        }

    def format_execution_time(self):
        """
        Format the calculated time into a human readable format.
        """

        result = ''
        calculated_time = self.calculate()
        times = list(calculated_time.keys())

        for time in times:
            result += calculated_time[time]

            if time != times[-1]:
                result += ':'

        return result


class Prints(object):
    """
    Print data on screen and into a file if needed.
    Template Possibilities: Percentage, Less, HTTP and any status you want.

    :param to_print: A list, the list of data to print.
    :param template: A string, the template to use.
    :param output_file: A string, the file to write.
    :param only_on_file: A boolean, if true, we don't print data on screen.
    """

    def __init__(
            self,
            to_print,
            template,
            output_file=None,
            only_on_file=False):
        self.template = template
        self.output = output_file
        self.data_to_print = to_print
        self.only_on_file = only_on_file

        self.headers = {
            'Generic': {
                'Domain': 100,
                'Status': 11,
                'Expiration Date': 17,
                'Source': 10,
                'HTTP Code': 10,
                'Analyze Date': 20
            },
            Settings.official_up_status: {
                'Domain': 100,
                'Expiration Date': 17,
                'Source': 10,
                'HTTP Code': 10,
                'Analyze Date': 20
            },
            Settings.official_down_status: {
                'Domain': 100,
                'WHOIS Server': 35,
                'Status': 11,
                'Source': 10,
                'HTTP Code': 10,
                'Analyze Date': 20
            },
            Settings.official_invalid_status: {
                'Domain': 100,
                'Source': 10,
                'HTTP Code': 10,
                'Analyze Date': 20
            },
            'Less': {
                'Domain': 100,
                'Status': 11,
                'HTTP Code': 10
            },
            'Percentage': {
                'Status': 11,
                'Percentage': 12,
                'Numbers': 12
            },
            'HTTP': {
                'Domain': 100,
                'Status': 11,
                'HTTP Code': 10,
                'Analyze Date': 20
            }
        }

        self.currently_used_header = {}

    def before_header(self):
        """
        Print informations about PyFunceble and the date of generation of a file
        into a given path, if doesn't exist.
        """

        if self.output is not None and self.output != '' and not path.isfile(
                self.output):
            link = ("# File generated with %s\n" % Settings.link_to_repo)
            date_of_generation = (
                "# Date of generation: %s \n\n" %
                Settings.current_datetime)

            Helpers().File(self.output).write(link + date_of_generation)

    @classmethod
    def header_constructor(cls, data_to_print, separator='-'):
        """
        Construct header of the table according to template.

        :param data_to_print: A list, the list of data to print into the header.
        :param separator: A string, the separator to use forr the table generation.
        """

        header_data = []
        header_size = ''
        before_size = '%-'
        after_size = 's '

        if separator:
            separator_data = []

        for data in data_to_print:
            size = data_to_print[data]
            header_data.append(data)

            header_size += before_size + str(size) + after_size

            if separator:
                separator_data.append(separator * size)

        if separator:
            return [
                header_size %
                tuple(header_data),
                header_size %
                tuple(separator_data)]
        return [header_size % tuple(header_data)]

    def header(self, do_not_print=False):  # pylint: disable=too-many-branches
        """
        Management and creation of templates of header.
        Please consider as "header" the title of each columns.
        """

        if not Settings.header_printed or self.template == 'Percentage':
            if self.template in Settings.generic_status or self.template == 'Generic_File':
                to_print = self.headers['Generic']

                if self.template in Settings.generic_status:
                    to_print = Helpers.Dict(
                        to_print).remove_key('Analyze Date')
            if self.template in Settings.up_status:
                to_print = self.headers[Settings.official_up_status]
            elif self.template in Settings.down_status:
                to_print = self.headers[Settings.official_down_status]
            elif self.template in Settings.invalid_status:
                to_print = self.headers[Settings.official_invalid_status]
            elif self.template == 'Less' or self.template == 'Percentage' \
                    or self.template == 'HTTP':
                to_print = self.headers[self.template]

                if self.template == 'Less' and not Settings.http_code_status:
                    to_print['Source'] = 10

            if not Settings.http_code_status:
                to_print = Helpers.Dict(to_print).remove_key('HTTP Code')

            self.currently_used_header = to_print

            if not do_not_print:
                self.before_header()
                for formated_template in self.header_constructor(to_print):
                    if not self.only_on_file:
                        print(formated_template)
                    if self.output is not None and self.output != '':
                        Helpers.File(
                            self.output).write(formated_template + '\n')

    def data_constructor(self, size):
        """
        Construct the table of data according to given size.

        :param size: A list, The maximal length of each string in the table.
        """

        result = {}
        if len(self.data_to_print) == len(size):
            i = 0
            while i < len(self.data_to_print):
                result[self.data_to_print[i]] = size[i]

                i += 1
        else:
            # This should never happend. If it's happens then there is something
            # wrong from the inputed data.
            raise Exception(
                'Inputed: ' +
                str(len(self.data_to_print)) +
                '; Size: ' +
                str(len(size)))

        return result

    @classmethod
    def size_from_header(cls, header):
        """
        Get the size of each columns from the header.

        :param header_type: The header we have to get.
        """

        result = []

        for data in header:
            result.append(header[data])

        return result

    def colorify(self, data):
        """
        Retun colored string.

        :param data: A string, the string to colorify.
        """

        if self.template in ['Generic', 'Less']:
            if self.data_to_print[1] in Settings.up_status:
                data = Fore.BLACK + Back.GREEN + data
            elif self.data_to_print[1] in Settings.down_status:
                data = Fore.BLACK + Back.RED + data
            else:
                data = Fore.BLACK + Back.CYAN + data
        return data

    def data(self):
        """
        Management and input of data to the table.
        Please consider as "
        """

        if isinstance(self.data_to_print, list):
            to_print = {}
            to_print_size = []

            alone_cases = ['Percentage', 'HTTP']
            without_header = ['FullHosts', 'PlainDomain']

            if self.template not in alone_cases and self.template not in without_header:
                self.header(True)
                to_print_size = self.size_from_header(
                    self.currently_used_header)
            elif self.template in without_header:
                for data in self.data_to_print:
                    to_print_size.append(str(len(data)))
            else:
                to_print_size = self.size_from_header(
                    self.headers[self.template])

            to_print = self.data_constructor(to_print_size)

            self.before_header()

            for data in self.header_constructor(to_print, False):
                if self.template in Settings.generic_status or self.template in [
                        'Less', 'Percentage']:
                    if not self.only_on_file:
                        data = self.colorify(data)
                        print(data)
                if self.output is not None and self.output != '':
                    Helpers.File(self.output).write(data + '\n')
        else:
            # This should never happend. If it's happens then there's a big issue
            # around data_to_print.
            raise Exception('Please review Prints().data()')


class HTTPCode(object):
    """
    Get and return the HTTP code status of a given domain.
    """

    @classmethod
    def access(cls):
        """
        Get the HTTP code status.
        """

        try:
            try:
                try:
                    req = requests.get(
                        'http://' + Settings.domain + ':80',
                        timeout=Settings.seconds_before_http_timeout)
                except socket.timeout:
                    return
            except requests.exceptions.Timeout:
                return

            return req.status_code
        except requests.ConnectionError:
            return

    def get(self):
        """
        Return the HTTP code status.
        """

        http_code = self.access()
        list_of_valid_http_code = []

        for codes in [
                Settings.active_http_codes,
                Settings.potentially_up_codes,
                Settings.potentially_down_status]:
            list_of_valid_http_code.extend(codes)

        if http_code not in list_of_valid_http_code or http_code is None:
            return '*' * 3
        return http_code


class Lookup(object):
    """
    This class can be used to NSLOOKUP or WHOIS lookup.
    """

    @classmethod
    def nslookup(cls):
        """
        Implementation of UNIX nslookup.
        """

        try:
            try:
                socket.gethostbyaddr(Settings.domain)
            except socket.herror:
                return False

            return True
        # except socket.gaierror or socket.herror:
        except socket.gaierror:
            return False

    @classmethod
    def whois(cls, whois_server):
        """
        Implementation of UNIX whois.

        :param whois_server: The whois server to use to get the record.
        """

        if whois_server is not None and whois_server != '':

            req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if Settings.seconds_before_http_timeout % 3 == 0:
                req.settimeout(Settings.seconds_before_http_timeout)
            else:
                req.settimeout(3)

            try:
                req.connect((whois_server, 43))
            except socket.error:
                return None

            req.send((Settings.domain + '\r\n').encode())
            response = b""

            while True:
                try:
                    try:
                        data = req.recv(4096)
                    except ConnectionResetError:
                        req.close()

                        return None
                except socket.timeout:
                    req.close()

                    return None

                response += data
                if not data:
                    break

            req.close()

            try:
                return response.decode()
            except UnicodeDecodeError:
                return response.decode('utf-8', 'replace')
        return None


class Percentage(object):
    """
    Calculation of the percentage of each status.

    :param domain_status: A string, the status to increment.
    :param init: A dict, Dictionary of data to initiate.
    """

    def __init__(self, domain_status=None, init=None):
        self.status = domain_status

        if init is not None and isinstance(init, dict):
            for data in init:
                setattr(Settings, data, init[data])

    def count(self):
        """
        Count the number of domain for each status.
        """

        if self.status is not None or self.status != '':
            Settings.number_of_tested += 1

            if self.status in Settings.up_status:
                Settings.number_of_up += 1
            elif self.status in Settings.down_status:
                Settings.number_of_down += 1
            else:
                Settings.number_of_invalid += 1

    @classmethod
    def calculate(cls):
        """
        Calculate the percentage of each status.
        """

        percentages = {
            'percentage_of_up': Settings.number_of_up,
            'percentage_of_down': Settings.number_of_down,
            'percentage_of_invalid': Settings.number_of_invalid
        }

        for percentage in percentages:
            setattr(
                Settings,
                percentage,
                percentages[percentage] *
                100 //
                Settings.number_of_tested)

    def log(self):
        """
        Print on screen and on file the percentages for each status.
        """

        if Settings.show_percentage and Settings.number_of_tested > 0:
            Helpers.File(Settings.output_percentage_log).delete()

            self.calculate()

            print('\n')
            Prints(None, 'Percentage', Settings.output_percentage_log).header()

            for to_print in [[Settings.official_up_status,
                              str(Settings.percentage_of_up) + '%',
                              Settings.number_of_up],
                             [Settings.official_down_status,
                              str(Settings.percentage_of_down) + '%',
                              Settings.number_of_down],
                             [Settings.official_invalid_status,
                              str(Settings.percentage_of_invalid) + '%',
                              Settings.number_of_invalid]]:
                Prints(
                    to_print,
                    'Percentage',
                    Settings.output_percentage_log).data()


class Generate(object):
    """
    Generate different sort of files.

    :param domain_status: A string, the domain status.
    :param source: A string, the source of the given status.
    :param expiration_date: A string, the expiration date of the domain.
    """

    def __init__(self, domain_status, source=None, expiration_date=None):
        self.domain_status = domain_status
        self.source = source
        self.expiration_date = expiration_date

        self.refer_status = ''
        self.output = ''

    def hosts_file(self):
        """
        Generate a hosts file.
        """

        if Settings.generate_hosts or Settings.plain_list_domain:
            splited_destination = ''

            if self.domain_status in Settings.up_status:
                hosts_destination = plain_destination = Settings.output_up_host
            elif self.domain_status in Settings.down_status:
                hosts_destination = plain_destination = Settings.output_down_host
            elif self.domain_status in Settings.invalid_status:
                hosts_destination = plain_destination = Settings.output_invalid_host
            elif self.domain_status in Settings.potentialy_up_status \
                or self.domain_status in Settings.potentially_down_status \
                    or self.domain_status in Settings.http_active_status:

                if self.domain_status in Settings.potentialy_up_status:
                    output_dir = Settings.output_http_potentially_up
                elif self.domain_status in Settings.potentially_down_status:
                    output_dir = Settings.output_http_potentially_down
                else:
                    output_dir = Settings.output_http_up

                hosts_destination = output_dir + Settings.hosts_default_filename
                plain_destination = output_dir + Settings.domains_default_filename

                if Settings.split_files:
                    splited_destination = output_dir + str(Settings.http_code)

            if Settings.generate_hosts:
                Prints([Settings.custom_ip, Settings.domain],
                       'FullHosts', hosts_destination).data()

            if Settings.plain_list_domain:
                Prints([Settings.domain], 'PlainDomain',
                       plain_destination).data()

            if Settings.split_files and splited_destination != '':
                Prints([Settings.domain], 'PlainDomain',
                       splited_destination).data()

    def unified_file(self):
        """
        Generate unified file. Understand by that that we use an unified table
        instead of a separate table for each status which could result into a
        misunderstanding.
        """

        if Settings.unified_file:
            if Settings.less:
                if Settings.http_code_status:
                    to_print = [
                        Settings.domain,
                        self.domain_status,
                        Settings.http_code]
                else:
                    to_print = [
                        Settings.domain,
                        self.domain_status,
                        self.source]

                Prints(
                    to_print,
                    'Less',
                    Settings.output_unified_results,
                    True).data()
            else:
                to_print = [
                    Settings.domain,
                    self.domain_status,
                    self.expiration_date,
                    self.source,
                    Settings.http_code,
                    Settings.current_datetime]

                Prints(
                    to_print,
                    'Generic_File',
                    Settings.output_unified_results,
                    True).data()

    @classmethod
    def analytic_file(cls, new_status, old_status):
        """
        Generate HTTP_Analytic/* files.

        :param new_status: A string, the new status of the domain.
        :param old_status: A strinf, the old status of the domain.
        """

        if new_status in Settings.up_status:
            output = Settings.output_http_up
            Generate('HTTP_Active').hosts_file()
        elif new_status in Settings.potentialy_up_status:
            output = Settings.output_http_potentially_up
            Generate('potentially_up').hosts_file()
        else:
            output = Settings.output_http_potentially_down

        Prints([Settings.domain, old_status, Settings.http_code,
                Settings.current_datetime], 'HTTP', output, True).data()

    def up_status_file(self):
        """
        Logic behind the up status when generating the status file.
        """

        if self.expiration_date in [None, '', False]:
            self.expiration_date = 'Unknown'

        if Settings.http_code_status and Settings.http_code in Settings.down_potentially_codes:
            self.analytic_file(
                Settings.official_down_status,
                self.domain_status)

            regex_to_match = [
                r'\.doubleclick\.net', r'\.liveadvert\.com']

            for regx in regex_to_match:
                if Helpers.Regex(
                        Settings.domain, regx, return_data=False).match():
                    self.source = 'SPECIAL'
                    self.domain_status = Settings.official_down_status
                    self.output = Settings.output_down_result

            regex_blogspot = r'\.blogspot\.'
            regex_blogger = [r'create-blog.g?', r'87065']

            if Helpers.Regex(
                    Settings.domain,
                    regex_blogspot,
                    return_data=False).match() and Settings.http_code == 302:
                blogger_content_request = requests.get(
                    'http://' + Settings.domain + ':80')
                blogger_content = blogger_content_request.text

                for regx in regex_blogger:
                    if regx in blogger_content:
                        self.source = 'SPECIAL'
                        self.domain_status = Settings.official_down_status
                        self.output = Settings.output_down_result
                        break

        if self.source != 'SPECIAL':
            self.domain_status = Settings.official_up_status
            self.output = Settings.output_up_result

    def down_status_file(self):
        """
        Logic behind the down status when generating the status file.
        """

        self.refer_status = 'Not Found'
        self.expiration_date = 'Unknown'

        if Settings.http_code_status:
            if Settings.http_code in Settings.active_http_codes:
                self.analytic_file(
                    Settings.official_up_status, self.domain_status)
                self.source = 'HTTP Code'
                self.domain_status = Settings.official_up_status
                self.output = Settings.output_up_result
            elif Settings.http_code in Settings.potentially_up_codes:
                self.analytic_file('potentially_up', self.domain_status)

        if self.source != 'HTTP Code':
            self.domain_status = Settings.official_down_status
            self.output = Settings.output_down_result

    def invalid_status_file(self):
        """
        Logic behind the invalid status when generating the status file.
        """

        self.expiration_date = 'Unknown'

        if Settings.http_code_status:
            if Settings.http_code in Settings.active_http_codes:
                self.analytic_file(
                    Settings.official_up_status, self.domain_status)
                self.source = 'HTTP Code'
                self.domain_status = Settings.official_up_status
                self.output = Settings.output_up_result
            elif Settings.http_code in Settings.potentially_up_codes:
                self.analytic_file(
                    'potentially_up', self.domain_status)
            elif Settings.http_code in Settings.down_potentially_codes:
                self.analytic_file(
                    Settings.official_down_status, self.domain_status)

            if self.source != 'HTTP Code':
                self.domain_status = Settings.official_invalid_status
                self.output = Settings.output_invalid_result

    def prints_status_file(self):
        """
        Logic behind the printing when generating status file.
        """

        if Settings.less:
            Prints([Settings.domain, self.domain_status,
                    self.source], 'Less', self.output, True).data()
        else:
            if not Settings.split_files:
                if self.domain_status in Settings.up_status:
                    Prints([Settings.domain,
                            self.expiration_date,
                            self.source,
                            Settings.http_code,
                            Settings.current_datetime],
                           Settings.official_up_status,
                           self.output,
                           True).data()
                elif self.domain_status in Settings.down_status:
                    Prints([Settings.domain,
                            Settings.referer,
                            self.domain_status,
                            self.source,
                            Settings.http_code,
                            Settings.current_datetime],
                           Settings.official_down_status,
                           self.output,
                           True).data()
                elif self.domain_status in Settings.invalid_status:
                    Prints([Settings.domain,
                            self.source,
                            Settings.http_code,
                            Settings.current_datetime],
                           Settings.official_invalid_status,
                           self.output,
                           True).data()

    def status_file(self):
        """
        Generate a file according to the domain status.
        """

        if self.domain_status in Settings.up_status:
            self.up_status_file()
        elif self.domain_status in Settings.down_status:
            self.down_status_file()
        elif self.domain_status in Settings.invalid_status:
            self.invalid_status_file()

        Generate(
            self.domain_status,
            self.source,
            self.expiration_date).hosts_file()
        Percentage(self.domain_status).count()

        if not Settings.quiet:
            if Settings.less:
                Prints([Settings.domain,
                        self.domain_status,
                        Settings.http_code],
                       'Less').data()
            else:
                Prints([Settings.domain,
                        self.domain_status,
                        self.expiration_date,
                        self.source,
                        Settings.http_code],
                       'Generic').data()

        if not Settings.no_files and Settings.split_files:
            self.prints_status_file()
        else:
            self.unified_file()


class Status(object):  # pylint: disable=too-few-public-methods
    """
    Return the domain status in case we don't use WHOIS or in case that WHOIS
    record is not readable.

    :param matched_status: A string, the previously catched status.
    """

    def __init__(self, matched_status):
        self.matched_status = matched_status

        self.handle()

    def handle(self):
        """
        Handle the lack of WHOIS. :)
        """

        source = 'NSLOOKUP'

        if self.matched_status not in Settings.invalid_status:
            if Lookup().nslookup():
                Generate(Settings.official_up_status, source).status_file()
            else:
                Generate(Settings.official_down_status, source).status_file()
        else:
            Generate(Settings.official_invalid_status, 'IANA').status_file()

        return


class Referer(object):
    """
    Get the WHOIS server (referer) of the current domain extension according to
        the IANA database.
    """

    def __init__(self):
        self.domain_extension = Settings.domain[Settings.domain.rindex(
            '.') + 1:]

        self.manual_server = {
            'bm': 'whois.afilias-srs.net',
            'bz': 'whois.afilias-grs.net',
            'cd': 'chois.nic.cd',
            'cm': 'whois.netcom.cm',
            'fj': 'whois.usp.ac.fj',
            'ga': 'whois.my.ga',
            'lc': 'whois2.afilias-grs.net',
            'lk': 'whois.nic.lk',
            'nyc': 'whois.nic.nyc',
            'ps': 'whois.pnina.ps',
            'ren': 'whois.nic.ren',
            'rw': 'whois.ricta.org.rw',
            'shop': 'whois.nic.shop',
            'sl': 'whois.nic.sl',
            'stream': 'whois.nic.stream',
            'tokyp': 'whois.nic.tokyo',
            'uno': 'whois.nic.uno',
            'za': 'whois.registry.net.za'
        }

        self.list_of_excluded_extension = [
            'ad',
            'al',
            'an',
            'ao',
            'arpa',
            'az',
            'ba',
            'bd',
            'bf',
            'bh',
            'bs',
            'comm',
            'cu',
            'dj',
            'eg',
            'fm',
            'ge',
            'gh',
            'gm',
            'gp',
            'gr',
            'gt',
            'jo',
            'kh',
            'lb',
            'mil',
            'mm',
            'mt',
            'mw',
            'ne',
            'np',
            'nr',
            'pa',
            'ph',
            'pn',
            'pk',
            'py',
            'rr',
            'sd',
            'sr',
            'sv',
            'sz',
            'tj',
            'tp',
            'tt',
            'vi',
            'vn',
            'xx',
            'z',
            'zw']

    @classmethod
    def iana_database(cls):
        """
        Convert `iana-domains-db` into a list.
        """

        file_to_read = Settings.current_dir + 'iana-domains-db'

        return [extension.rstrip('\n') for extension in open(file_to_read)]

    @classmethod
    def from_iana(cls):
        """
        Return the referer from IANA database.
        """

        whois_record = Lookup().whois(Settings.iana_server)

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

    def get(self):
        """
        Return the referer aka the WHOIS server of the current domain extension.
        """

        if not Settings.no_whois:
            regex_ipv4 = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'  # pylint: disable=line-too-long
            referer = None

            if not Helpers.Regex(
                    Settings.domain,
                    regex_ipv4,
                    return_data=False).match():
                if self.domain_extension in self.iana_database():
                    if self.domain_extension in self.list_of_excluded_extension:
                        Status(Settings.official_down_status)
                        referer = True
                    elif self.domain_extension in self.manual_server:
                        referer = self.manual_server[self.domain_extension]
                    else:
                        referer = self.from_iana()

                        if referer is None:
                            self.log()
                            Status(Settings.official_down_status)
                else:
                    Status(Settings.official_invalid_status)
                    referer = True
            else:
                Status(Settings.official_down_status)
                referer = True

            return referer
        return None

    def log(self):
        """
        Log if no referer is found for a domain extension.
        """

        if Settings.logs:
            logs = '=' * 100
            logs += '\nNo referer found for: %s domains\n' % self.domain_extension
            logs += '=' * 100
            logs += '\n'

            Helpers.File(
                Settings.no_referer_logs_dir +
                self.domain_extension).write(logs)


class ExpirationDate(object):
    """
    Get, format and return the epiration date of a domain if exist.
    """

    def __init__(self):
        Settings.http_code = HTTPCode().get()

        self.log_separator = '=' * 100 + ' \n'

        self.expiration_date = ''
        self.whois_record = ''

        if '.' in Settings.domain:
            Settings.referer = Referer().get()

            if Settings.referer in [True, False]:
                return
            elif Settings.referer is not None:
                self.extract()
            else:
                Status(Settings.official_down_status)
        else:
            Status(Settings.official_invalid_status)

    def whois_log(self):
        """
        Log the whois record into a file
        """

        if Settings.debug and Settings.logs:
            log = self.log_separator + self.whois_record + '\n' + self.log_separator

            Helpers.File(Settings.whois_logs_dir + Settings.referer).write(log)

    @classmethod
    def convert_1_to_2_digits(cls, number):
        """
        Convert 1 digit number to two digits.
        """

        return str(number).zfill(2)

    @classmethod
    def convert_or_shorten_month(cls, data):
        """
        Convert a given month into our unified format.

        :param data: A string, The month to convert or shorten.
        """

        short_month = {
            'jan': [str(1), '01', 'Jan', 'January'],
            'feb': [str(2), '02', 'Feb', 'February'],
            'mar': [str(3), '03', 'Mar', 'March'],
            'apr': [str(4), '04', 'Apr', 'April'],
            'may': [str(5), '05', 'May'],
            'jun': [str(6), '06', 'Jun', 'June'],
            'jul': [str(7), '07', 'Jul', 'July'],
            'aug': [str(8), '08', 'Aug', 'August'],
            'sep': [str(9), '09', 'Sep', 'September'],
            'oct': [str(10), 'Oct', 'October'],
            'nov': [str(11), 'Nov', 'November'],
            'dec': [str(12), 'Dec', 'December']
        }

        for month in short_month:
            if data in short_month[month]:
                return month

        return data

    def log(self):
        """
        Log the extracted expiration date and domain into a file.
        """

        if Settings.logs:
            log = self.log_separator + 'Expiration Date: %s \n' % self.expiration_date
            log += 'Tested domain: %s \n' % Settings.domain

            Helpers.File(
                Settings.date_format_logs_dir +
                Settings.referer).write(log)

    @classmethod
    def cases_management(cls, regex_number, matched_result):
        """
        A little helper of self.format. (Avoiding of nested loops)
        """

        cases = {
            'first': [[1, 2, 3, 10, 11, 26, 27, 28, 29, 32], [0, 1, 2]],
            'second': [[14, 15, 31, 33, 36], [1, 0, 2]],
            'third': [[4, 5, 6, 7, 8, 9, 12, 13,
                       16, 17, 18, 19, 20, 21, 23, 24, 25, 30, 35], [2, 1, 0]]
        }

        for case in cases:
            case_data = cases[case]

            if int(regex_number) in case_data[0]:
                return [matched_result[case_data[1][0]],
                        matched_result[case_data[1][1]],
                        matched_result[case_data[1][2]]]
            else:
                continue
        return None

    def format(self):
        """
        Format the expiration date into an unified format (01-jan-1970).
        """

        regex_dates = {
            # Date in format: 02-jan-2017
            '1': r'([0-9]{2})-([a-z]{3})-([0-9]{4})',
            # Date in format: 02.01.2017 // Month: jan
            '2': r'([0-9]{2})\.([0-9]{2})\.([0-9]{4})$',
            # Date in format: 02/01/2017 // Month: jan
            '3': r'([0-3][0-9])\/(0[1-9]|1[012])\/([0-9]{4})',
            # Date in format: 2017-01-02 // Month: jan
            '4': r'([0-9]{4})-([0-9]{2})-([0-9]{2})$',
            # Date in format: 2017.01.02 // Month: jan
            '5': r'([0-9]{4})\.([0-9]{2})\.([0-9]{2})$',
            # Date in format: 2017/01/02 // Month: jan
            '6': r'([0-9]{4})\/([0-9]{2})\/([0-9]{2})$',
            # Date in format: 2017.01.02 15:00:00
            '7': r'([0-9]{4})\.([0-9]{2})\.([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}',
            # Date in format: 20170102 15:00:00 // Month: jan
            '8': r'([0-9]{4})([0-9]{2})([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}',
            # Date in format: 2017-01-02 15:00:00 // Month: jan
            '9': r'([0-9]{4})-([0-9]{2})-([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}',
            # Date in format: 02.01.2017 15:00:00 // Month: jan
            '10': r'([0-9]{2})\.([0-9]{2})\.([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}',
            # Date in format: 02-Jan-2017 15:00:00 UTC
            '11': r'([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{1}.*',  # pylint: disable=line-too-long
            # Date in format: 2017/01/02 01:00:00 (+0900) // Month: jan
            '12': r'([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s\(.*\)',
            # Date in format: 2017/01/02 01:00:00 // Month: jan
            '13': r'([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}$',
            # Date in format: Mon Jan 02 15:00:00 GMT 2017
            '14': r'[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{3}\s([0-9]{4})',  # pylint: disable=line-too-long
            # Date in format: Mon Jan 02 2017
            '15': r'[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s([0-9]{4})',
            # Date in format: 2017-01-02T15:00:00 // Month: jan
            '16': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}$',
            # Date in format: 2017-01-02T15:00:00Z // Month: jan${'7}
            '17': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Z].*',
            # Date in format: 2017-01-02T15:00:00+0200 // Month: jan
            '18': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{4}',
            # Date in format: 2017-01-02T15:00:00+0200.622265+03:00 //
            # Month: jan
            '19': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[+-][0-9]{2}:[0-9]{2}',  # pylint: disable=line-too-long
            # Date in format: 2017-01-02T15:00:00+0200.622265 // Month: jan
            '20': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}$',
            # Date in format: 2017-01-02T23:59:59.0Z // Month: jan
            '21': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[A-Z]',
            # Date in format: 02-01-2017 // Month: jan
            '22': r'([0-9]{2})-([0-9]{2})-([0-9]{4})',
            # Date in format: 2017. 01. 02. // Month: jan
            '23': r'([0-9]{4})\.\s([0-9]{2})\.\s([0-9]{2})\.',
            # Date in format: 2017-01-02T00:00:00+13:00 // Month: jan
            '24': r'([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}',  # pylint: disable=line-too-long
            # Date in format: 20170102 // Month: jan
            '25': r'(?=[0-9]{8})(?=([0-9]{4})([0-9]{2})([0-9]{2}))',
            # Date in format: 02-Jan-2017
            '26': r'([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})$',
            # Date in format: 02.1.2017 // Month: jan
            '27': r'([0-9]{2})\.([0-9]{1})\.([0-9]{4})',
            # Date in format: 02 Jan 2017
            '28': r'([0-9]{1,2})\s([A-Z]{1}[a-z]{2})\s([0-9]{4})',
            # Date in format: 02-January-2017
            '29': r'([0-9]{2})-([A-Z]{1}[a-z]*)-([0-9]{4})',
            # Date in format: 2017-Jan-02.
            '30': r'([0-9]{4})-([A-Z]{1}[a-z]{2})-([0-9]{2})\.',
            # Date in format: Mon Jan 02 15:00:00 2017
            '31': r'[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{1,2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s([0-9]{4})',  # pylint: disable=line-too-long
            # Date in format: Mon Jan 2017 15:00:00
            '32': r'()[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}',
            # Date in format: January 02 2017-Jan-02
            '33': r'([A-Z]{1}[a-z]*)\s([0-9]{1,2})\s([0-9]{4})',
            # Date in format: 2.1.2017 // Month: jan
            '34': r'([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})',
            # Date in format: 20170102000000 // Month: jan
            '35': r'([0-9]{4})([0-9]{2})([0-9]{2})[0-9]+',
            # Date in format: 01/02/2017 // Month: jan
            '36': r'(0[1-9]|1[012])\/([0-3][0-9])\/([0-9]{4})'
        }

        for regx in regex_dates:
            matched_result = Helpers.Regex(
                self.expiration_date,
                regex_dates[regx],
                return_data=True,
                rematch=True).match()

            if matched_result:
                date = self.cases_management(regx, matched_result)

                if date is not None:
                    day = self.convert_1_to_2_digits(date[0])
                    month = self.convert_or_shorten_month(date[1])
                    year = str(date[2])

                    self.expiration_date = day + '-' + month + '-' + year
                break

        if self.expiration_date != '' and Helpers.Regex(
                self.expiration_date,
                r'[0-9]{2}\-[a-z]{3}\-2[0-9]{3}',
                return_data=False).match() != True:
            self.log()

    def extract(self):
        """
        Extract the expiration date from the whois record.
        """

        self.whois_record = Lookup().whois(Settings.referer)

        to_match = [
            r'expire:(.*)',
            r'expire on:(.*)',
            r'Expiry Date:(.*)',
            r'free-date(.*)',
            r'expires:(.*)',
            r'Expiration date:(.*)',
            r'Expiry date:(.*)',
            r'Expire Date:(.*)',
            r'renewal date:(.*)',
            r'Expires:(.*)',
            r'validity:(.*)',
            r'Expiration Date             :(.*)',
            r'Expiry :(.*)',
            r'expires at:(.*)',
            r'domain_datebilleduntil:(.*)',
            r'Data de expiração \/ Expiration Date \(dd\/mm\/yyyy\):(.*)',
            r'Fecha de expiración \(Expiration date\):(.*)',
            r'\[Expires on\](.*)',
            r'Record expires on(.*)(\(YYYY-MM-DD\))',
            r'status:      OK-UNTIL(.*)',
            r'renewal:(.*)',
            r'expires............:(.*)',
            r'expire-date:(.*)',
            r'Exp date:(.*)',
            r'Valid-date(.*)',
            r'Expires On:(.*)',
            r'Fecha de vencimiento:(.*)',
            r'Expiration:.........(.*)',
            r'Fecha de Vencimiento:(.*)',
            r'Registry Expiry Date:(.*)',
            r'Expires on..............:(.*)',
            r'Expiration Time:(.*)',
            r'Expiration Date:(.*)',
            r'Expired:(.*)',
            r'Date d\'expiration:(.*)']

        if self.whois_record is not None:
            for string in to_match:
                expiration_date = Helpers.Regex(
                    self.whois_record,
                    string,
                    return_data=True,
                    rematch=True,
                    group=0).match()

                if expiration_date != []:
                    self.expiration_date = expiration_date[0].strip()

                    regex_rumbers = r'[0-9]'
                    if Helpers.Regex(
                            self.expiration_date,
                            regex_rumbers,
                            return_data=False).match():

                        self.format()
                        Generate(Settings.official_up_status, 'WHOIS',
                                 self.expiration_date).status_file()
                        return

                    self.whois_log()
                    Status(Settings.official_down_status)

                    return

        self.whois_log()
        Status(Settings.official_down_status)
        return


class Helpers(object):  # pylint: disable=too-few-public-methods
    """
    PyFunceble's helpers.
    """

    class Command(object):
        """Shell command execution."""

        def __init__(self, command):
            self.decode_type = 'utf-8'
            self.command = command

        def decode_output(self, to_decode):
            """Decode the output of a shell command in order to be readable.

            :param to_decode: byte(s), Output of a command to decode.
            """

            return to_decode.decode(self.decode_type)

        def execute(self):
            """Execute the given command."""

            process = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=True)
            (output, error) = process.communicate()

            if process.returncode != 0:
                return self.decode_output(error)
            return self.decode_output(output)

    class Dict(object):
        """
        Dictionary manipulations.
        """

        def __init__(self, main_dictionnary=None):

            if main_dictionnary is None:
                self.main_dictionnary = {}
            else:
                self.main_dictionnary = main_dictionnary

        def remove_key(self, key_to_remove):
            """
            Remove a given key from a given dictionary.

            :param key_to_remove: A string or a list, the key(s) to delete.
            """

            if isinstance(self.main_dictionnary, dict):
                if isinstance(key_to_remove, list):
                    for k in key_to_remove:
                        del self.main_dictionnary[k]
                else:
                    del self.main_dictionnary[key_to_remove]
                return self.main_dictionnary
            return None

        def to_json(self, destination):
            """
            Save a dictionnary into a JSON file.

            :param destination: A string, A path to a file where we're going to
            write the converted dict into a JSON format.
            """

            with open(destination, 'w') as file:
                dump(
                    self.main_dictionnary,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True)

        @classmethod
        def from_json(cls, data):
            """
            Convert a JSON formated string into a dictionary.

            :param data: A string, a JSON formeted string to convert to dict format.
            """

            try:
                return loads(data)
            except decoder.JSONDecodeError:
                return {}

    class File(object):
        """
        File treatment/manipulations.

        :param file: A string, a path to the file to manipulate.
        """

        def __init__(self, file):
            self.file = file

        def write(self, data_to_write, overwrite=False):
            """
            Write or append data into the given file path.

            :param data_to_write: A string, the data to write.
            """

            if data_to_write is not None and isinstance(
                    data_to_write, str):
                if overwrite or not path.isfile(self.file):
                    with open(self.file, 'w', encoding="utf-8") as file:
                        file.write(data_to_write)
                else:
                    with open(self.file, 'a', encoding="utf-8") as file:
                        file.write(data_to_write)

        def read(self):
            """
            Read a given file path and return its content.
            """

            with open(self.file, 'r', encoding="utf-8") as file:
                funilrys = file.read()

            return funilrys

        def delete(self):
            """
            Delete a given file path.
            """

            try:
                remove(self.file)
            except OSError:
                pass

    class Regex(object):  # pylint: disable=too-few-public-methods

        """A simple implementation ot the python.re package


        :param data: A string, the data to regex check
        :param regex: A string, the regex to match
        :param return_data: A boolean, if True, return the matched string
        :param group: A integer, the group to return
        :param rematch: A boolean, if True, return the matched groups into a
            formated list. (implementation of Bash ${BASH_REMATCH})
        :param replace_with: A string, the value to replace the matched regex with.
        :param occurences: A int, the number of occurence to replace.
        """

        def __init__(self, data, regex, **args):
            # We initiate the needed variable in order to be usable all over
            # class
            self.data = data

            # We assign the default value of our optional arguments
            optional_arguments = {
                "escape": False,
                "group": 0,
                "occurences": 0,
                "rematch": False,
                "replace_with": None,
                "return_data": True
            }

            # We initiate our optional_arguments in order to be usable all over the
            # class
            for (arg, default) in optional_arguments.items():
                setattr(self, arg, args.get(arg, default))

            if self.escape:  # pylint: disable=no-member
                self.regex = escape(regex)
            else:
                self.regex = regex

        def match(self):
            """Used to get exploitable result of re.search"""

            # We initate this variable which gonna contain the returned data
            result = []

            # We compile the regex string
            to_match = comp(self.regex)

            # In case we have to use the implementation of ${BASH_REMATCH} we use
            # re.findall otherwise, we use re.search
            if self.rematch:  # pylint: disable=no-member
                pre_result = to_match.findall(self.data)
            else:
                pre_result = to_match.search(self.data)

            if self.return_data and pre_result is not None:  # pylint: disable=no-member
                if self.rematch:  # pylint: disable=no-member
                    for data in pre_result:
                        if isinstance(data, tuple):
                            result.extend(list(data))
                        else:
                            result.append(data)

                    if self.group != 0:  # pylint: disable=no-member
                        return result[self.group]  # pylint: disable=no-member
                else:
                    result = pre_result.group(
                        self.group).strip()  # pylint: disable=no-member

                return result
            elif not self.return_data and pre_result is not None:  # pylint: disable=no-member
                return True
            return False

        def replace(self):
            """Used to replace a matched string with another."""

            if self.replace_with is not None:  # pylint: disable=no-member
                return substrings(
                    self.regex,
                    self.replace_with,  # pylint: disable=no-member
                    self.data,
                    self.occurences)  # pylint: disable=no-member
            return self.data


if __name__ == '__main__':
    if Settings.current_dir == '%%current_dir%%':
        print(
            'Please run the installation script first.\n You can run it with : %s \n' %
            './tool -i\n')
        exit(1)
    else:
        PARSER = argparse.ArgumentParser(
            description='Python version of Funceble, an awesome script to check \
                domains or IP accessibility. Also described as "[an] excellent script \
                for checking ACTIVE, INACTIVE and EXPIRED Domain Names."',
            epilog="Crafted with %s by %s\033[0m " %
            (Fore.RED +
             '♥' +
             Fore.RESET,
             Style.BRIGHT +
             'Nissar Chababy (Funilrys)'),
            add_help=False)

        PARSER.add_argument(
            '-a',
            '--all',
            action='store_false',
            help='Output all available informations on screen.')
        PARSER.add_argument(
            '--cmd-before-end',
            type=str,
            help='Pass a command before the results (final) commit of travis mode.')
        PARSER.add_argument(
            '-c',
            '--auto-continue',
            '--continue',
            action='store_true',
            help='Switch the default value of the auto continue mode to its opposite.')
        PARSER.add_argument(
            '-d',
            '--domain',
            type=str,
            help='Analyze the given domain.')
        PARSER.add_argument(
            '--debug',
            action='store_true',
            help='Switch the default value of the debug mode to its opposite.'
        )
        PARSER.add_argument(
            "-f",
            "--file",
            type=str,
            help="Test a file with a list of domains."
        )
        PARSER.add_argument(
            '--filter',
            type=str,
            help='Domain to filter.'
        )
        PARSER.add_argument(
            '-ex',
            '--execution',
            action='store_true',
            help='Show the execution time.'
        )
        PARSER.add_argument(
            '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show this help message and exit.'
        )
        PARSER.add_argument(
            '-h',
            '--host',
            action='store_true',
            help='Activate the generation of hosts file.'
        )
        PARSER.add_argument(
            '--http',
            action='store_true',
            help='Switch the default value of the usage of HTTP code.'
        )
        PARSER.add_argument(
            '-ip',
            type=str,
            help='Change the ip to print in host file.'
        )
        PARSER.add_argument(
            '--less',
            action='store_true',
            help='Output less informations on screen.'
        )
        PARSER.add_argument(
            '-n',
            '--no-files',
            action='store_true',
            help='Deactivate the production of output files.'
        )
        PARSER.add_argument(
            '-nl',
            '--no-logs',
            action='store_true',
            help='Deactivate the production of logs files in case we encounter some errors.'
        )
        PARSER.add_argument(
            '-nu',
            '--no-unified',
            action='store_true',
            help='Deactivate the production of result.txt as unified result \
                under the output directory.'
        )
        PARSER.add_argument(
            '-nw',
            '--no-whois',
            action='store_true',
            help="Deactivate the usage of whois to test domain's status."
        )
        PARSER.add_argument(
            '-p',
            '--percentage',
            action='store_true',
            help='Switch the default value of the percentage output mode to its opposite.'
        )
        PARSER.add_argument(
            '--plain',
            action='store_true',
            help='Switch the default value of the generation \
                of the plain list of domain to its opposite.'
        )
        PARSER.add_argument(
            '-q',
            '--quiet',
            action='store_true',
            help='Split outputed files.'
        )
        PARSER.add_argument(
            '--split',
            action='store_true',
            help='Split output files.'
        )
        PARSER.add_argument(
            '-t',
            '--timeout',
            type=int,
            default=3,
            help='Seconds before timeout.'
        )
        PARSER.add_argument(
            '--travis',
            action='store_true',
            help='Activate the travis mode.'
        )
        PARSER.add_argument(
            '-v',
            '--version',
            action='version',
            version='%(prog)s 0.7.0-beta'
        )

        ARGS = PARSER.parse_args()
        initiate(autoreset=True)

        if ARGS.less:
            Settings.less = ARGS.less
        else:
            Settings.less = ARGS.all

        if ARGS.cmd_before_end:
            Settings.command_before_end = ARGS.cmd_before_end

        if ARGS.auto_continue:
            Settings.auto_continue = Settings().switch('auto_continue')

        if ARGS.debug:
            Settings.debug = Settings().switch('debug')

        if ARGS.execution:
            Settings.show_execution_time = Settings().switch('show_execution_time')

        if ARGS.filter:
            Settings.to_filter = ARGS.filter

        if ARGS.host:
            Settings.generate_hosts = Settings().switch('generate_hosts')

        if ARGS.http:
            Settings.http_code_status = Settings().switch('http')

        if ARGS.ip:
            Settings.custom_ip = ARGS.ip

        if ARGS.no_files:
            Settings.no_files = Settings().switch('no_files')

        if ARGS.no_logs:
            Settings.logs = Settings().switch('logs')

        if ARGS.no_unified:
            Settings.unified_file = Settings().switch('unified_file')

        if ARGS.no_whois:
            Settings.no_whois = Settings().switch('no_whois')

        if ARGS.percentage:
            Settings.show_percentage = Settings().switch('show_percentage')

        if ARGS.plain:
            Settings.plain_list_domain = Settings().switch('plain_list_domain')

        if ARGS.quiet:
            Settings.quiet = Settings().switch('quiet')

        if ARGS.split:
            Settings.split_files = Settings().switch('split_files')

        if ARGS.timeout:
            if ARGS.timeout % 3 == 0:
                Settings.seconds_before_http_timeout = ARGS.timeout

        if ARGS.travis:
            Settings.travis = Settings().switch('travis')

        PyFunceble(ARGS.domain, ARGS.file)

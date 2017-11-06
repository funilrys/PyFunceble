#!/bin/env python3

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

from os import path, remove
from time import strftime


class Settings(object):
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
    # a 403 HTTP code status represent an 'INACTIVE' domain.
    potentialy_up_status = ['potentially_up', 'potentially_active']
    # Potentially down status
    # As an example, We can't be sure that a 400 HTTP code status result
    # represent an 'INACTIVE' domain.
    potentially_down_status = ['potentially_down', 'potentially_inactive']
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
    # Activate/Deactivate the generation of plain list of domains accoding to
    # out status.
    plain_list_domain = False
    # Activate/Deactive the quiet mode.
    quiet = False
    # HTTP Status code timeout.
    # Consider this as the minimum time in seconds that we need before.
    seconds_before_http_timeout = 1
    # Show/hide the percentage.
    show_percentage = True
    # If set to true, we generate the files into the 'splited/' directory.
    split_files = False
    # Activation/Deactivation of Travis CI autosave system.
    travis = False
    # Minimum of minutes before we start commiting to upstream under Travis CI.
    travis_autosave_minutes = 15
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

    # Output directory.
    # DO NOT UPDATE THIS UNLESS YOU KNOW WHAT YOU ARE DOING.
    output_dir = '/home/funilrys/Projects/PyFunceble/output/'
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


class PyFunceble(object):
    """
    Main entry to Funceble. Brain of the program. Also known as "put everything
    together to make the system works".

    :param domain: A string, a domain or IP to test.
    :param file_path: A string, a path to a file to read.
    """

    def __init__(self, domain=None, file_path=None):

        if domain is not None and domain != '':
            self.domain(domain)

        elif file_path is not None and file_path != '':
            self.file(file_path)

    def domain(self, domain):
        """
        Manage the case that we want to test only a domain.

        :param domain: A string, a domain or IP to test.
        """

        Settings.domain = domain.lower()

    def file(self, file_path):
        """
        Manage the case that need to test each domain of a given file path.
        Note: 1 domain per line.

        :param file_path: A string, a path to a file to read.
        """
        list_to_test = []

        for read in open(file_path):
            read = read.rstrip('\n').strip()

            if not read.startswith('#'):
                list_to_test.append(read)


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

    def header_constructor(self, data_to_print, separator='-'):
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

    def header(self):
        """
        Management and creation of templates of header.
        Please consider as "header" the title of each columns.
        """

        if not Settings.header_printed or self.template == 'Percentage':
            headers = {
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

            if self.template in Settings.up_status or \
                    self.template in Settings.generic_status or self.template == 'Generic_File':
                to_print = headers[Settings.official_up_status]

                if self.template in Settings.generic_status:
                    to_print = Helpers.Dict(
                        to_print).remove_key('Analyze Date')
            elif self.template in Settings.down_status:
                to_print = headers[Settings.official_down_status]
            elif self.template in Settings.invalid_status:
                to_print = headers[Settings.official_invalid_status]
            elif self.template == 'Less' or self.template == 'Percentage' \
                    or self.template == 'HTTP':
                to_print = headers[self.template]

                if self.template == 'Less' and not Settings.http_code_status:
                    to_print['Source'] = 10

            if not Settings.http_code_status:
                to_print = Helpers.Dict(to_print).remove_key('HTTP Code')

            self.before_header()

            for formated_template in self.header_constructor(to_print):
                if not self.only_on_file:
                    print(formated_template)
                if self.output is not None and self.output != '':
                    Helpers.File(self.output).write(formated_template + '\n')


class Helpers(object):
    """
    PyFunceble's helpers.
    """

    class Dict(object):
        """
        Dictionary manipulations.
        """

        def __init__(self, main_dictionnary):
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

    class File(object):
        """
        File treatment/manipulations.

        :param file: A string, a path to the file to manipulate.
        """

        def __init__(self, file):
            self.file = file

        def write(self, data_to_write):
            """
            Write or append data into the given file path.

            :param data_to_write: A string, the data to write.
            """

            if data_to_write is not None and isinstance(data_to_write, str):
                if path.isfile(self.file):
                    with open(self.file, 'a') as file:
                        file.write(data_to_write)
                else:
                    with open(self.file, 'w') as f:
                        f.write(data_to_write)

        def read(self):
            """
            Read a given file path and return its content.
            """

            with open(self.file, 'r') as f:
                funilrys = f.read()

            return funilrys

        def delete(self):
            """
            Delete a given file path.
            """

            try:
                remove(self.file)
            except OSError:
                pass

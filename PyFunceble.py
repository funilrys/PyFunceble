#!/bin/env python3

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

from time import strftime


class Settings(object):
    """
    Serve as "saver" of all needed settings or parameters.
    """

    ################################# Status #################################
    # Default index for "official" returned status
    # Why 5 ? Simply luck I started to write the status and it's appears that the
    # fifth index is simply what we used in Funceble.
    official_status_index = 5
    # List of valid down status
    down_status = ['down', 'Down', 'DOWN', 'inactive',
                   'Inactive', 'INACTIVE', 'error', 'Error', 'ERROR']
    # Official down status
    official_down_status = down_status[official_status_index]
    # List of valid up status
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
    # Official up status
    official_up_status = up_status[official_status_index]
    # List of valid invalid status
    invalid_status = ['ouch', 'Ouch', 'OUCH', 'invalid', 'Invalid', 'INVALID']
    # Official invalid status
    official_invalid_status = invalid_status[official_status_index]
    # Generic status
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
    # Activate/Deactivate the generation of hosts file
    generate_hosts = True
    # Used to check if the header has been already printed on screen.
    header_printed = False
    # Domain to filter. For example \.blogspot\. will test only blogspot.*
    # domains.
    to_filter = ''
    # Activate/Deactive the output of every informations.
    less = False
    # Activate/Deactivate the output of logs
    logs = True
    # Activate/Deactivate the generation of plain list of domains accoding to
    # out status.
    plain_list_domain = False
    # Activate/Deactive the quiet mode
    quiet = False
    # HTTP Status code timeout
    # Consider this as the minimum time in seconds that we need before
    seconds_before_http_timeout = 1
    # Show/hide the percentage
    show_percentage = True
    # If set to true, we generate the files into the 'splited/' directory
    split_files = False
    # Activation/Deactivation of Travis CI autosave system
    travis = False
    # Minimum of minutes before we start commiting to upstream under Travis CI
    travis_autosave_minutes = 15
    # Output into unified files
    unified_file = True
    ##########################################################################
    ############################ Links / Servers #############################
    # Link of the repository
    link_to_repo = 'https://github.com/funilrys/PyFunceble'
    # IANA whois Servers
    iana_server = 'whois.iana.org'
    ##########################################################################
    ################################## Time ##################################
    # Current date & Time
    current_datetime = strftime("%a %d %b %H:%m:%S %Z %Y")
    ##########################################################################
    ################################# Counter ################################
    # Counter of the number of tested
    number_of_tested = 0
    # Counter of the number of active/up
    number_of_up = 0
    # Counter of the number of inactive/down
    number_of_down = 0
    # Counter of the number of invalid
    number_of_invalid = 0
    # Percentage of active/up
    percentage_of_up = 0
    # Percentage of inactive/down
    percentage_of_down = 0
    # Percentage of invalid
    percentage_of_invalid = 0
    ##########################################################################
    ################################ HTTP Code ###############################
    # Activate/Deactivate the used of the http code
    http_code_status = True
    # Active considered codes.
    # Note that if nslookup = inactive and http code is in the following list,
    # We set the domain to active.
    active_http_codes = [100, 101, 200, 201, 202, 203, 204, 205, 206]
    # Potentially active codes
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
    # Potentially inactive codes
    down_potentially_codes = [400, 402, 403, 404, 409, 410, 412, 414, 415, 416]
    ##########################################################################
    ########################### File Manipulation ############################
    # Used to check if we already cleaned the given file
    cleaned_done = False
    # Default hosts file filename
    hosts_default_filename = 'hosts'
    # Default plain list domain filename
    plain_list_domain_default_filename = 'list'
    # If set to True, we don't generate any files.
    # Please note: This does not apply to hosts files
    no_files = False
    ##########################################################################
    ################################# Outputs ################################
    # Note: DO NOT FORGET `/` AT THE END.

    # Output directory.
    # DO NOT UPDATE THIS UNLESS YOU KNOW WHAT YOU ARE DOING.
    output_dir = '/home/funilrys/Projects/PyFunceble/output/'
    # Autocontinue log file.
    # Please not that this file is != from Funceble.
    autocontinue_log_file = output_dir + 'continue.json'

    ##########################################################################
    #                               `output/domains/`
    # This directory will keep the plain list of domain to their
    # official status.
    ##########################################################################
    # Domains directory.
    domains_dir = output_dir + 'domains/'
    # ACTIVE/Up domains directory.
    up_domains_dir = domains_dir + official_up_status + '/'
    # INACTIVE/Down domains directory.
    down_domains_dir = domains_dir + official_down_status + '/'
    # INVALID domains directory.
    invalid_domains_dir = domains_dir + official_invalid_status + '/'

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

################################ Contributors ############################
# - All contributors of https://github.com/funilrys/Funceble
#
# - Let's contribute to PyFunceble !
##########################################################################


class Settings(object):
    """
    Serve as "saver" of all needed settings or parameters.
    """

    ################################### Status #################################
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
    up_status =  ['up', 'Up', 'UP', 'active','Active', 'ACTIVE', 'valid', 'Valid', 'VALID']
    # Official up status
    official_up_status = up_status[official_status_index]
    # List of valid invalid status
    invalid_status = ['ouch', 'Ouch', 'OUCH', 'invalid', 'Invalid', 'INVALID']
    # Official invalid status
    official_invalid_status = invalid_status[official_status_index]
    # Generic status
    # Why generic ? Good question that the first word who come to discribed the
    # unified table system.
    generic_status = ['generic','Generic','GENERIC']
    # Potentionally up status
    # Why potentially ? Please note: https://git.io/vFttS
    # I consider them as potentially because for example we can't be sure that
    # a 403 HTTP code status represent an 'INACTIVE' domain
    potentialy_up_status = ['potentially_up', 'potentially_active']
    # Potentially down status
    # As an example, We can't be sure that a 400 HTTP code status result
    # represent an 'INACTIVE' domain
    potentially_down_status = ['potentially_down', 'potentially_inactive']
    ############################################################################

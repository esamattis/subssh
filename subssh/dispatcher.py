# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Esa-Matti Suuronen <esa-matti@suuronen.org>

This file is part of subssh.

Subssh is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Subssh is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public 
License along with Subssh.  If not, see 
<http://www.gnu.org/licenses/>.
"""


import os
import sys

import config

from optparse import OptionParser

import customlogger
logger = customlogger.get_logger(__name__)

access_logger = customlogger.get_logger("access", filepath=config.LOG_ACCESS)


import apprunner
import shell
import tools
import appimporter
appimporter.import_all_apps_from_config()


parser = OptionParser()


parser.add_option("-t", "--ssh-tunnel", dest="ssh_username",
                  help="Run subssh as user. Command is read from "
                  "SSH_ORIGINAL_COMMAND enviroment variable.", 
                  metavar="<username>")



def from_ssh(username):
    
    if os.environ.has_key('SSH_CONNECTION'):
        from_ip = os.environ.get('SSH_CONNECTION', '').split()[0]
    else:
        from_ip = "localhost"
    
    
    
    try:
        ssh_original_command = os.environ['SSH_ORIGINAL_COMMAND']
    except KeyError:
        ssh_original_command = None

    
    access_logger.info("%s from %s cmd: %s" % 
                       (username, from_ip, ssh_original_command))
    
    
    if not ssh_original_command:
        return "", []

    # Clean up the original command
    parts = [part.strip("'\" ") for part in ssh_original_command.split()]
    
    cmd = parts[0]
    args = parts[1:]
    return cmd, args
    


class UserRequest(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
    
def dispatch():

    options, args = parser.parse_args()
    
    
    if options.ssh_username:
        username = options.ssh_username
        if username == config.ADMIN:
            tools.errln("Cannot login as admin '%s' over SSH!" % username)
            return 1
        cmd, args = from_ssh(username)
    else:
        username = tools.hostusername()
        cmd, args = tools.to_cmd_args(sys.argv[1:])
        
    user = UserRequest(username=username, 
                       cmd=cmd, 
                       from_ssh=bool(options.ssh_username),
                       logger=customlogger.get_user_logger(username))
    
    if cmd:
        user.interactive = False
        return apprunner.run(user, args)
    else:
        user.interactive = True
        return shell.prompt(user)
        
    



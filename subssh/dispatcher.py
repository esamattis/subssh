# -*- coding: utf-8 -*-
'''
Created on Mar 5, 2010

@author: epeli
'''
import os
import sys

import config

from optparse import OptionParser

import customlogger
logger = customlogger.get_logger(__name__)

access_logger = customlogger.get_logger("access", filepath=config.LOG_ACCESS)


import apploader
import shell
import tools
import admintools


parser = OptionParser()


parser.add_option("-t", "--ssh-tunnel", dest="ssh_username",
                  help="Run subssh as user. Command is read from "
                  "SSH_ORIGINAL_COMMAND enviroment variable.", 
                  metavar="<username>")


parser.add_option("--add-key", dest="add_key_username",
                  metavar="<username> <input>",
                  help="Add public key to user. Input may be an url, - for " 
                       "stdin or the key itself")


parser.add_option("-u", "--update-keys", action="store_true",
                  help="Rewrite authorized_keys file")

parser.add_option("--restore-default-config", action="store_true",
                  help="Restore default config")


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
    
     
    
def dispatch():

    options, args = parser.parse_args()
    
    if options.update_keys:
        return admintools.rewrite_authorized_keys() 
    
    if options.restore_default_config:
        return admintools.restore_config()
    
    if options.add_key_username:
        return admintools.add_key(options.add_key_username, args)
    
    
    
    
    if options.ssh_username:
        username = options.ssh_username
        if username == config.ADMIN:
            tools.errln("Cannot login as admin '%s' over SSH!" % username)
            return 1
        cmd, args = from_ssh(username)
    else:
        username = os.getlogin()
        cmd, args = tools.to_cmd_args(sys.argv[1:])
        
    if cmd:
        return apploader.run(username, cmd, args)
    else:
        return shell.prompt(username)
        
def main():
    
    exit_status = dispatch()
    if exit_status == None:
        return 0
    return exit_status
        

if __name__ == "__main__":
    main()

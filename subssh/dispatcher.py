# -*- coding: utf-8 -*-
'''
Created on Mar 5, 2010

@author: epeli
'''
import os
import sys

import config

from optparse import OptionParser
import logging
logging.basicConfig(filename=config.LOG ,level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("main")

import apploader
import shell
import tools
import admintools


parser = OptionParser()


parser.add_option("-t", "--ssh-tunnel", dest="ssh_username",
                  help="run subssh as user", metavar="ssh_username")



parser.add_option("-u", "--update-keys", action="store_true",
                  help="Rewrite authorized_keys -file")

parser.add_option("--restore-default-config", action="store_true",
                  help="Restore default config")


def from_ssh():
    
    if os.environ.has_key('SSH_CONNECTION'):
        from_ip = os.environ.get('SSH_CONNECTION', '').split()[0]
    else:
        from_ip = "localhost"
    
    # TODO: log ip
    
    try:
        ssh_original_command = os.environ['SSH_ORIGINAL_COMMAND']
    except KeyError:
        return "", []

    # Clean up the original command
    parts = [part.strip("'\" ") for part in ssh_original_command.split()]
    
    cmd = parts[0]
    args = parts[1:]
    return cmd, args
    


     
        


def main():
    options, args = parser.parse_args()
    
    if options.update_keys:
        return admintools.rewrite_authorized_keys() 
    
    if options.restore_default_config:
        return admintools.restore_config()
    
    
    if options.ssh_username:
        username = options.ssh_username
        cmd, args = from_ssh()
    else:
        username = os.getlogin()
        cmd, args = tools.to_cmd_args(sys.argv[1:])
        
    if cmd:
        return apploader.run(username, cmd, args)
    else:
        return shell.prompt(username)
        
        

if __name__ == "__main__":
    main()
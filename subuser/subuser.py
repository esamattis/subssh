# -*- coding: utf-8 -*-
'''
Created on Mar 5, 2010

@author: epeli
'''
import os
import sys

import config


import logging
logging.basicConfig(filename=config.log ,level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("main")


import apps





def main():
    username = sys.argv[1]
    msg = ("User:%s IP:%s" %(
              username, os.environ.get('SSH_CONNECTION', '').split()[0]))
    try:
        ssh_original_command = os.environ['SSH_ORIGINAL_COMMAND']
        msg += " cmd: " +  ssh_original_command
    except KeyError:
        logger.info("Connection without cmd " + msg)
        sys.stderr.write( "cmds: %s\n" % ", ".join(apps.cmds.keys()).strip(",") )
        return 0
        
    cmd = ssh_original_command.split()[0]
    
    try:
        f = apps.cmds[cmd]
    except KeyError:
        logger.warning("Unknown cmd. " + msg)
        sys.stderr.write("Unknown command %s\n" % cmd)
        return 1
    else:
        logger.info("Running " + msg)
        return f(username, ssh_original_command)
        
        

if __name__ == "__main__":
    main()
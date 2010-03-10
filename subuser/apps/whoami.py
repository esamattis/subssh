# -*- coding: utf-8 -*-
'''
Created on Mar 9, 2010

@author: epeli
'''

from subuser import tools
from subuser import config


def whoami(username, ssh_original_command):
    tools.writeln(username)

cmds = {
        "whoami": whoami,
        }


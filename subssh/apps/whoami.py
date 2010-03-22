# -*- coding: utf-8 -*-
'''
Created on Mar 9, 2010

@author: epeli
'''

from subssh import tools



def whoami(username, cmd, args):
    """Tells who you are
    """
    tools.writeln(username)

cmds = {
        "whoami": whoami,
        }


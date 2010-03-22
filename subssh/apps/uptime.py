# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

import subprocess

from subssh import tools

class config:
    HELLO = "default hello"



@tools.require_args(at_most=4, at_least=2)
def uptime(username, cmd, args):
    """Example application for integrating uptime of the host system"""
    tools.writeln(config.HELLO)
    return subprocess.call(["uptime"])
    
    

cmds = {"uptime": uptime}
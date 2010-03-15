# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

import subprocess

from subssh import tools

class config:
    hello = "default hello"



def uptime(username, ssh_original_command):
    tools.writeln(config.hello)
    return subprocess.call(["uptime"])
    
    

cmds = {"uptime": uptime}
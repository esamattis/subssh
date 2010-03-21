# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

import subprocess

from subssh import tools

class config:
    hello = "default hello"



def uptime(username, cmd, args):
    """Example application for integrating uptime of the host system"""
    return subprocess.call(["uptime"])
    
    

cmds = {"uptime": uptime}
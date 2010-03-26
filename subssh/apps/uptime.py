# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

import subprocess

from subssh import tools

class config:
    HELLO = "default hello"



@tools.expose_as("expose", "alt")
def foo(username, cmd, args):
    """foo doc"""
    print "works!"

@tools.expose_as("uptime")
def uptime(username, cmd, args):
    """Example application for integrating uptime of the host system"""
    tools.writeln(config.HELLO)
    return subprocess.call(("uptime"))

    



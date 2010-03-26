# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

import subprocess

import subssh

class config:
    HELLO = "default hello"



@subssh.expose_as("expose", "alt")
def foo(username, cmd, args):
    """foo doc"""
    print "works!"

@subssh.expose_as("uptime")
def uptime(username, cmd, args):
    """Example application for integrating uptime of the host system"""
    subssh.writeln(config.HELLO)
    return subprocess.call(("uptime"))

    



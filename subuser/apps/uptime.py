'''
Created on Mar 5, 2010

@author: epeli
'''

import subprocess

import tools


def uptime(username, ssh_original_command):
    return subprocess.call(["uptime"])
    
    

cmds = {"uptime": uptime}
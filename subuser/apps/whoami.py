'''
Created on Mar 9, 2010

@author: epeli
'''

import tools

def whoami(username, ssh_original_command):
    tools.writeln(username)

cmds = {
        "whoami": whoami,
        }


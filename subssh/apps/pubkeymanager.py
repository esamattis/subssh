# -*- coding: utf-8 -*-
'''
Created on Mar 21, 2010

@author: epeli
'''



import subssh
from subssh import admintools
from subssh import tools



@subssh.expose_as("addkey")
def add_key(username, cmd, args):
    """
    Add new public key.
    
    usage:
    
    from web:
        $cmd http://example.com/mykey.pub
    
    from args:
        $cmd ssh-rsa AAAthekeyitself... 
        
    from stdin:
        you@home:~$$ cat mykey.pub | ssh $hostusername@$hostname $cmd -
    
    """
    
    return admintools.add_key(username, args)

    
def list_keys(username, cmd, args):    
    """List keys you've uploaded"""
    return admintools.list_keys(username)
    
    
cmds = {
        "addkey": add_key,
        "listkeys": list_keys,
        }
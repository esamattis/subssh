# -*- coding: utf-8 -*-
'''
Created on Mar 21, 2010

@author: epeli
'''

import urllib2

from subssh.authorizedkeys import AuthorizedKeysDB
from subssh import tools

@tools.default_to_doc
def add_key(username, cmd, args):
    """
    Add new public key.
    
    usage: addkey <HTTP-URL to key or key itself>
    
    """
    
    
    db = AuthorizedKeysDB()
    
    if args[0].startswith("http"):
        try:
            key = urllib2.urlopen(args[0]).read(4096)
        except urllib2.HTTPError, e:
            tools.errln(e.args)
            return 1
    else:
        key = " ".join(args)
            
            
    db.add_key_from_str(username, key)
    
    
    db.commit()
    db.close()
    
    
cmds = {"addkey": add_key}
'''
Created on Mar 21, 2010

@author: epeli
'''

import sys
import shutil
import urllib2


import tools
import config
from authorizedkeys import AuthorizedKeysDB
from subssh.keyparsers import PubKeyException

def rewrite_authorized_keys():
    db = AuthorizedKeysDB()
    db.commit()
    db.close()
    return 0

def restore_config():
    shutil.copy(config.DEFAULT_CONFIG_PATH, config.CONFIG_PATH)
    return 0


def add_key(username, args):
    
    max_key_size = 4096
    
    if args[0].startswith("http"):
        try:
            key = urllib2.urlopen(args[0]).read(max_key_size)
        except urllib2.HTTPError, e:
            tools.errln(e.args[0])
            return 1
    elif args[0] == "-":
        key = sys.stdin.read(max_key_size)
    else:
        key = " ".join(args)
            
            
    db = AuthorizedKeysDB()
    
    exit_status = 0
    
    try:
        db.add_key_from_str(username, key)
    except PubKeyException, e:
        tools.errln(e.args[0])
        exit_status = 1
    else:
        db.commit()
        
    db.close()
    
    return exit_status

def list_keys(username):
    db = AuthorizedKeysDB(disable_lock=True)
    try:
        subuser = db.subusers[username]
    except KeyError:
        tools.writeln("%s has no keys" % username)
    else:
        for i, (key, (type, comment)) in enumerate(subuser.pubkeys.items()):
            tools.writeln("%s. %s %s key: %s..." % (i+1, type, comment, key[:20]))
    
    db.close()
    
    
    
    
    
    

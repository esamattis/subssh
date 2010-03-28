# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Esa-Matti Suuronen <esa-matti@suuronen.org>

This file is part of subssh.

Subssh is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Subssh is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public 
License along with Subssh.  If not, see 
<http://www.gnu.org/licenses/>.
"""

import sys
import shutil
import urllib2
from optparse import OptionParser


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
    hopefully_a_pubkey = " ".join(args)
    # 4096 is enough for everybody? :)
    max_key_size = 4096
    
    if hopefully_a_pubkey.startswith("http"):
        try:
            key = urllib2.urlopen(hopefully_a_pubkey).read(max_key_size)
        except urllib2.HTTPError, e:
            tools.errln(e.args[0])
            return 1
    elif hopefully_a_pubkey == "-":
        key = sys.stdin.read(max_key_size)
            
            
    
    exit_status = 0
    
    db = AuthorizedKeysDB()
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
            tools.writeln("%s. %s\n   %s %s" % 
                          (i+1, comment, type , key))
    
    db.close()
    
    

def list_users():
    db = AuthorizedKeysDB(disable_lock=True)
    for user in db.subusers.values():
        print "%s with %s keys" % (user.username, len(user.pubkeys))
    db.close()


def remove_user(username):
    db = AuthorizedKeysDB()
    try:
        db.remove_user(username)
    except KeyError:
        tools.errln("No such user '%s'" % username)   
    else:
        db.commit()
    db.close()
    





def build_parser(args=sys.argv[1:]):

    parser = OptionParser(description=handle_cmdline.__doc__)
    
    parser.add_option("-a", "--add-key", dest="add_key_username",
                      metavar="<username> <input>",
                      help="Add public key to user. Input may be an url, - for " 
                           "stdin or the key itself")
    
    
    parser.add_option("-u", "--update-keys", action="store_true",
                      help="Rewrite authorized_keys file")
    
    parser.add_option("--restore-default-config", action="store_true",
                      help="Restores default config")
        
    parser.add_option("--ls-users", action="store_true",
                      help="List users")        
        
    parser.add_option("--rm-user", dest="rm_user",
                      metavar="<username>",
                      help="Remove user and his/her keys from authorized_keys")        
        
    parser.add_option("--ls-keys",
                      metavar="<username>",
                      help="List users keys")
    
    return parser




def handle_cmdline():
    """
    Add keys (create users) and delete users.
    """
    
    parser = build_parser()
    parser.option_list
    options, args = parser.parse_args()

    if options.update_keys:
        return rewrite_authorized_keys() 
    
    elif options.restore_default_config:
        return restore_config()
    
    elif options.add_key_username:
        return add_key(options.add_key_username, args)

    elif options.ls_users:
        return list_users()

    elif options.ls_keys:
        return list_keys(options.ls_keys)
    
    elif options.rm_user:
        return remove_user(options.rm_user)

    else:
        parser.print_help()
        return 1









    

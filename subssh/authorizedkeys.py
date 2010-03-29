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



import os
import sys
import time

import tools
from keyparsers import parse_subssh_key
from keyparsers import parse_public_key
from keyparsers import PubKeyException


import config
    
class Subuser(object):
    
    ssh_options = (
#                  "no-pty,"
                  "no-port-forwarding,"
                  "no-agent-forwarding,"
                  "no-X11-forwarding"
                  )
    
    
    _extra = (config.SUBSSH_PYTHONPATH and "SUBSSHPYTHONPATH=%s " 
                                    % config.SUBSSH_PYTHONPATH)
    subssh_cmd = "%s%s" % (_extra,  config.SUBSSH_BIN)
    
    
    def __init__(self, username):
        self.username = username
        self.pubkeys = {}
    
    def __hash__(self):
        return self.username.__hash__()
    
    def __repr__(self):
        return "<%s %s with %s keys>" % (self.__class__.__name__,
                                    self.username,
                                    len(self.pubkeys))
    
    def add_key(self, type, key, comment):
        try:
            orig_type, orig_comment = self.pubkeys[key]
            # Key Already exists. Update comment
            self.pubkeys[key] = orig_type, comment
        except KeyError:
            self.pubkeys[key] = type, comment
    


    def has_key_str(self, key):
        type, key, comment = parse_public_key(key)
        return self.pubkeys.has_key(key)

    def has_key(self, key):
        return self.pubkeys.has_key(key)

    def iter_in_authorized_keys_format(self):
        for key in self.pubkeys.keys():
            yield self.in_authorized_keys_format(key)
    
    def __iter__(self):
        for key, meta in self.pubkeys.items():
            type, comment = meta
            yield type, key, comment
            
    def in_authorized_keys_format(self, key):
        type, comment = self.pubkeys[key]
        return ("command=\"%(subssh_cmd)s -t %(username)s\","
                "%(ssh_options)s "
                "%(type)s %(key)s "
                "%(comment)s" 
                % {
                'subssh_cmd': self.subssh_cmd,
                'ssh_options':  self.ssh_options,
                'type': type,
                'key': key,
                'comment': comment, 
                'username': self.username})
    
    
    

class AuthorizedKeysException(Exception):
    pass
    
class AuthorizedKeysDB(object):
    _lock_timeout = 500
    
    def __init__(self, ssh_home=os.path.join( os.environ["HOME"], ".ssh" ),
                 disable_lock=False):
        
        # Lock can be disabled for read only sessions
        self.disable_lock = disable_lock
        
        self.keypath = os.path.join( ssh_home, "authorized_keys" )
            
        self.lockpath = os.path.join(ssh_home, "subssh_lock")
        
        self._acquire_lock()
        
            
        self.custom_key_lines = []
        self.subusers = {}
        
        self.load_keys()


    def remove_user(self, username):
        del self.subusers[username]

        

    def load_keys(self):
        """
        (re)load keys from authorized_keys -file
        """
        self.custom_key_lines = []
        self.subusers = {}
        
        if os.path.exists(self.keypath):
            keyfile = open(self.keypath, "r")
    
            for line in keyfile:
                line = line.strip()
                try:
                    username, type, key, comment = parse_subssh_key(line)
                except PubKeyException:
                    self.custom_key_lines.append(line)
                else:
                    self.add_key(username, type, key, comment)
            
            keyfile.close()
                


    def _acquire_lock(self):
        if self.disable_lock:
            return
        
        timeout = self._lock_timeout
        if os.path.exists(self.lockpath):
            tools.writeln("authorized_keys is locked!")
        while os.path.exists(self.lockpath):
            time.sleep(0.01)
            timeout -= 1
            if timeout <= 0:
                tools.writeln("Force removing authorized_keys lock")
                os.remove(self.lockpath)
            
            
        open(self.lockpath, "w").close()        
        
    
    
    def iter_all_keys(self):
        for user in self.subusers.values():
            for line in user.iter_in_authorized_keys_format():
                yield line
        for custom_line in self.custom_key_lines:
            yield custom_line
        
        
    
    def add_key(self, username, type, key, comment):
        
        try:
            user = self.subusers[username]
        except KeyError:
            user = Subuser(username)
            self.subusers[username] = user
            
        user.add_key(type, key, comment)


    def add_key_from_str(self, username, key, comment=""):
        type, key, key_comment = parse_public_key(key)
        
        if not comment:
            comment = key_comment
        
        self.add_key(username, type, key, comment)


    def commit(self):
        if self.disable_lock:
            raise AuthorizedKeysException("Cannot commit read only session")
        f = open(self.keypath, "w")
        for line in self.iter_all_keys():
            f.write(line + "\n")
        f.close()
        
        
        
    def _unlock(self):
        if self.disable_lock:
            return
        if os.path.exists(self.lockpath):
            os.remove(self.lockpath)
        
        
    def close(self):
        self._unlock()    
    
    

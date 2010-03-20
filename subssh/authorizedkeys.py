# -*- coding: utf-8 -*-

'''
Created on Mar 9, 2010

@author: epeli
'''



import os
import time

from keyparsers import parse_subssh_key
from keyparsers import parse_public_key
from keyparsers import PubKeyException

    
    
class Subuser(object):
    
    ssh_options = (
                  "no-port-forwarding,"
                  "no-pty,"
                  "no-agent-forwarding,"
                  "no-X11-forwarding"
                  )
    
    # sys.executable
    subssh_cmd = "PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subssh"
    
    
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
            yield self.as_authorized_keys_format(key)
    
    def __iter__(self):
        for key, meta in self.pubkeys.items():
            type, comment = meta
            yield type, key, comment
            
    def as_authorized_keys_format(self, key):
        type, comment = self.pubkeys[key]
        return ("command=\"%(subssh_cmd)s --ssh %(username)s\","
                "%(ssh_options)s "
                "%(type)s %(key)s "
                "%(comment)s" % {
                                                      
                'subssh_cmd': self.subssh_cmd,
                'ssh_options':  self.ssh_options,
                'type': type,
                'key': key,
                'comment': comment, 
                'username': self.username,
                 })
    
    
    

class AuthorizedKeysException(Exception):
    pass
    
class AuthorizedKeysDB(object):
    _lock_timeout = 500
    
    def __init__(self, ssh_home=os.path.join( os.environ["HOME"], ".ssh" )):
        
        
        self.keypath = os.path.join( ssh_home, "authorized_keys" )
            
        self.lockpath = os.path.join(ssh_home, "subssh_lock")
        
        self._acquire_lock()
        
            
        self.custom_key_lines = []
        self.subusers = {}
        
        self.load_keys()


        

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
        timeout = self._lock_timeout
        while os.path.exists(self.lockpath):
            time.sleep(0.01)
            timeout -= 1
            if timeout <= 0:
                raise AuthorizedKeysException("authorized_keys lock file timeout")
            
            
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


    def add_key_from_str(self, username, key):
        type, key, comment = parse_public_key(key)
        self.add_key(username, type, key, comment)


    def commit(self):
        f = open(self.keypath, "w")
        for line in self.iter_all_keys():
            f.write(line + "\n")
        f.close()
        
        
        
    def _unlock(self):
        if os.path.exists(self.lockpath):
            os.remove(self.lockpath)
        
        
    def close(self):
        self._unlock()    
    
    

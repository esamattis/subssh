'''
Created on Mar 9, 2010

@author: epeli
'''

"""

re.sub(r"command=\".+\",", "", key)
re.sub(r"\s{1}\w+@subuser$", "", key)

"""


import os
import re



    
subuser_pattern = re.compile(r"\s{1}([a-z]+)@subuser$")    
options_pattern = re.compile(r"command=\"([^\"]+)\"[^ ]* ")      

def parse_subuser_key(line):
    """
    
    
    
    """
    match = subuser_pattern.search(line)
    username = match.groups(1)[0]
    
    # Remove username/subuser identifier from end
    line = subuser_pattern.sub("", line)
    # Remove options from start
    line = options_pattern.sub("", line)
    
    type, key = line.split(None, 2)
    
    return username, type, key, comment

    
    
    
    
class Subuser(object):
    
    ssh_options = (
                  "no-port-forwarding,"
                  "no-pty,"
                  "no-agent-forwarding,"
                  "no-X11-forwarding"
                  )
    
    subuser_cmd = "PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subuser"
    
    
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
        

    def iter_in_authorized_keys_format(self):
        for key in self.pubkeys.keys():
            yield self.as_authorized_keys_format(key)
    
    def __iter__(self):
        for key, meta in self.pubkeys.items():
            type, comment = meta
            yield type, key, comment
            
    def as_authorized_keys_format(self, key):
        type, comment = self.pubkeys[key]
        return ("command=\"%(subuser_cmd)s %(username)s\","
                "%(ssh_options)s "
                "%(type)s %(key)s "
                "%(comment)s %(username)s@subuser" % {
                                                      
                'subuser_cmd': self.subuser_cmd,
                'ssh_options':  self.ssh_options,
                'type': type,
                'key': key,
                'comment': comment, 
                'username': self.username,
                 })
    
    
    
    
    
class AuthorizedKeysDB(object):
    
    
    
    
    def __init__(self, keypath=None):
        
        if not keypath:
            keypath = os.path.join( os.environ["HOME"], 
                                     ".ssh", "authorized_keys" )
            
        
        keyfile = open(keypath, "r")
            
        self.custom_key_lines = []
        self.subusers = {}


        for line in keyfile:
            line = line.strip()
            if line.strip().endswith("subuser"):
                self.add_key_from_str(line)
            else:
                self.custom_key_lines.append(line)
        
    
    
    def iter_in_authorized_keys_format(self):
        for custom_line in self.custom_key_lines:
            yield custom_line
        for user in self.subusers.values():
            for line in user.iter_in_authorized_keys_format():
                yield line
        
        
    
    def add_key_from_str(self, line):
        username, type, key, comment = parse_subuser_key(line)
        try:
            user = self.subusers[username]
        except KeyError:
            user = Subuser(username)
            self.subusers[username] = user
            
        user.add_key(type, key, comment)
        
        
        
    
    

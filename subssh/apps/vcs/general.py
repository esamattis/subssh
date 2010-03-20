# -*- coding: utf-8 -*-

'''
Created on Mar 10, 2010

@author: epeli
'''

import os
from ConfigParser import SafeConfigParser, NoOptionError



class InvalidRepository(IOError):
    pass


class InvalidPermissions(Exception):
    pass


def set_default_permissions(path, owner, vcs_class):
    
    f = open(os.path.join(path, vcs_class.owner_filename), "w")
    f.write(owner)
    f.close()        
    
    
    repo = vcs_class(path, owner)
    repo.set_permissions("*", "r")
    repo.set_permissions(owner, "rw")
    repo.save()






class VCS(object):
    """
    Abstract class for creating VCS support
    """
    
    
    # Add some files/directories here which are required by the vcs
    required_by_valid_repo = None
    
    _permissions_section = "permissions"
    
    permdb_name="subssh_permissions"
    
    owner_filename="subssh_owners"
    
    known_permissions = "rw"
    
    
    def __init__(self, repo_path, requester):
        self.requester = requester
        self.repo_path = repo_path
        self.repo_name = self.repo_path.split("/")[-1]
        
        for path in self.required_by_valid_repo:
            if not os.path.exists(os.path.join(repo_path, path)):
                raise InvalidRepository("%s does not seem to be "
                                        "valid %s repository" % 
                                    (path, self.__class__.__name__))
                                
        
        self.permdb_filepath = os.path.join(repo_path, self.permdb_name)
        self.owner_filepath = os.path.join(repo_path, self.owner_filename)
        
        self._owners = set()
        
        if os.path.exists(self.owner_filepath):
            f = open(self.owner_filepath, "r")
            for owner in f:
                self._owners.add(owner.strip())
            f.close()

        
        if self.requester != os.getlogin() and not self.is_owner(self.requester):
            raise InvalidPermissions("%s has no permissions to %s" %
                                     (self.requester, self))

        
        self.permdb = SafeConfigParser()
        self.permdb.read(self.permdb_filepath)
        
        if not self.permdb.has_section(self._permissions_section):
            self.permdb.add_section(self._permissions_section)
    
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.repo_name)
    
    def assert_permissions(self, permissions):
        for p in permissions:
            if p not in self.known_permissions:
                raise InvalidPermissions("Unknown permission %s" % p)
    
    def add_owner(self, username):
        self._owners.add(username)

    def is_owner(self, username):
        return username in self._owners

    def remove_owner(self, username):
        if len(self._owners) == 1 and self.is_owner(username):
            raise InvalidPermissions("Cannot remove last owner %s" % username)
        self._owners.remove(username)


    def set_permissions(self, username, permissions):
        """Overrides previous permissions"""
        self.assert_permissions(permissions)
        if not permissions:
            self.remove_all_permissions(username)
            return
        
        perm_set = set(permissions)
        self.permdb.set(self._permissions_section, username, "".join(perm_set))
    
    
    def has_permissions(self, username, permissions):
        self.assert_permissions(permissions)
        permissions_got = set()
        
        try: # First get general permissions
            for p in self.permdb.get(self._permissions_section, "*"):
                permissions_got.add(p)
        except NoOptionError:
            pass
        
        try: # and user specific permissions
            for p in self.permdb.get(self._permissions_section, username):
                permissions_got.add(p)            
        except NoOptionError:
            pass
        
        # Iterate through required permissions
        for perm in permissions:
            # If even one is missing bail out!
            if perm not in permissions_got:
                return False
            
        # Everything was found
        return True
        
    def get_permissions(self, username):
        return self.permdb.get(self._permissions_section, 
                               username)
    
    def remove_all_permissions(self, username):
        try:
            self.permdb.remove_option(self._permissions_section, username)
        except NoOptionError:
            pass
    
    def save(self):
        f = open(self.permdb_filepath, "w")
        self.permdb.write(f)
        f.close()
        
        f = open(self.owner_filepath, "w")
        for owner in self._owners:
            f.write(owner + "\n")
        f.close()        
        
        
        
        
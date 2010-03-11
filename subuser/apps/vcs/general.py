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
    
    
    repo = vcs_class(path)
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
    
    permdb_name="subuser_permissions"
    
    owner_filename="subuser_owner"
    
    _owner_changed = False
    
    def __init__(self, repo_path):
        
        self.repo_path = repo_path
        self.repo_name = self.repo_path.split("/")[-1]
        
        for path in self.required_by_valid_repo:
            if not os.path.exists(os.path.join(repo_path, path)):
                raise InvalidRepository("%s does not seem to be "
                                        "valid %s repository" % (
                                    path, self.__class__.__name__))
                                
        
        self.permdb_filepath = os.path.join(repo_path, self.permdb_name)
        self.owner_filepath = os.path.join(repo_path, self.owner_filename)
        
        if os.path.exists(self.owner_filepath):
            f = open(self.owner_filepath, "r")
            self.owner = f.read(50).strip()
            f.close()
        else:
            self.owner = None
        
        self.permdb = SafeConfigParser()
        self.permdb.read(self.permdb_filepath)
        
        if not self.permdb.has_section(self._permissions_section):
            self.permdb.add_section(self._permissions_section)
    
    def set_owner(self, username):
        self.owner = username
        self._owner_changed = True


    def set_permissions(self, username, permissions):
        self.permdb.set(self._permissions_section, username, permissions)
    
    def has_permissions(self, username, permissions):

        permissions_got = ""
        
        try: # First get general permissions
            permissions_got += self.permdb.get(self._permissions_section, "*")
        except NoOptionError:
            pass
        
        try: # and user specific permissions
            permissions_got += self.permdb.get(self._permissions_section, 
                                               username)
        except NoOptionError:
            pass
        
        # Iterate through required permissions
        for perm in permissions:
            # If even one is missing bail out!
            if perm not in permissions_got:
                return False
            
        # If everything was found, authorize the user
        return True
        
    def get_permissions(self, username):
        return self.permdb.get(self._permissions_section, 
                               username)
    
    def remove_all_permissions(self, username):
        self.permdb.remove_option(self._permissions_section, username)
    
    def save(self):
        f = open(self.permdb_filepath, "w")
        self.permdb.write(f)
        f.close()
        
        if self._owner_changed:
            f = open(self.owner_filepath, "w")
            f.write(self.owner)
            f.close()        
        
        
        
        
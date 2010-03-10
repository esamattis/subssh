# -*- coding: utf-8 -*-

'''
Created on Mar 10, 2010

@author: epeli
'''

import os
from ConfigParser import SafeConfigParser, NoOptionError


class InvalidRepository(IOError):
    pass


class VCSPermissions(object):
    """
    Abstract class for creating VCS support
    """
    
    
    # Add some files/directories here which are required by the vcs
    required_by_valid_repo = None
    
    _permissions_section = "permissions"
    
    
    def __init__(self, repo_path):
        self.repo_path = repo_path
        
        for path in self.required_by_valid_repo:
            if not os.path.exists(os.path.join(repo_path, path)):
                raise InvalidRepository("%s does not seem to be "
                                        "valid %s repository" % (
                                    path, self.__class__.__name__))
                                
        
        self.authzconfig_filepath = os.path.join(repo_path, self.authzfilename)
        self.authzconfig = SafeConfigParser()
        self.authzconfig.read(self.authzconfig_filepath)
        if not self.authzconfig.has_section(self._permissions_section):
            self.authzconfig.add_section(self._permissions_section)
        


    def set_permission(self, username, permissions):
        self.authzconfig.set(self._permissions_section, username, permissions)
    
    def has_permissions(self, username, permissions):
        try:
            permissions_got = self.authzconfig.get(self._permissions_section, 
                                               username)
        except NoOptionError:
            return False
        
        for perm in permissions:
            if perm not in permissions_got:
                return False
        
        return True
        
    
    def remove_all_permissions(self, username):
        self.authzconfig.remove_option(self._permissions_section, username)
    
    def save(self):
        f = open(os.path.join(self.repo_path, self.authzfilename), "w")
        self.authzconfig.write(f)
        f.close()
        
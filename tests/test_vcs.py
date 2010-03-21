'''
Created on Mar 11, 2010

@author: epeli
'''


import unittest
import tempfile
import os
import shutil

from subssh.apps.vcs import git, svn
from subssh.apps.vcs.general import InvalidPermissions

class VCSTestBase(object):
    username = "tester"
    vcs = None
    vcs_class = None


    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="subuser_test_tmp_")
        self.vcs.init_repository(self.dir, self.username)
    
    def test_test(self):
        self.assert_(os.path.exists(self.dir))
    
    
    def test_unknown_users_has_read_only_permissions(self):
        repo = self.vcs_class(self.dir, self.username)
        self.assert_(repo.has_permissions("nonexistent", "r"))
        self.assertFalse(repo.has_permissions("nonexistent", "rw"))
        self.assertFalse(repo.has_permissions("nonexistent", "w"))
    
    def test_default_permissions(self):
        repo = self.vcs_class(self.dir, self.username)
        self.assertEquals(repo.get_permissions(self.username),
                          "rw")
        self.assertEquals(repo.get_permissions("*"),
                          "r")    
        
        self.assert_(repo.has_permissions("*", "r"))
        self.assertFalse( repo.has_permissions("*", "w"))
        
        self.assert_(repo.has_permissions(self.username, "rw"))
        self.assert_(repo.has_permissions(self.username, "wr"))
        self.assert_(repo.has_permissions(self.username, "w"))
        self.assert_(repo.has_permissions(self.username, "r"))
    
    
    def test_add_permissions(self):
        repo = self.vcs_class(self.dir, self.username)
        repo.set_permissions("new", "rw")
        repo.save()
        
        repo = self.vcs_class(self.dir, self.username)
        self.assert_(repo.has_permissions("new", "rw"))
        self.assert_(repo.has_permissions("new", "w"))
        self.assert_(repo.has_permissions("new", "r"))    
    
    def test_remove_permissions(self):
        repo = self.vcs_class(self.dir, self.username)
        repo.set_permissions("new", "rw")
        repo.save()
        
        repo = self.vcs_class(self.dir, self.username)     
        repo.remove_all_permissions("new")
        repo.save()
        
        repo = self.vcs_class(self.dir, self.username)
        self.assertFalse(repo.has_permissions("new", "w"))
        self.assertFalse(repo.has_permissions("new", "rw"))        
        

    def test_add_owner(self):
        repo = self.vcs_class(self.dir, self.username)
        repo.add_owner("new")
        repo.save()
        
        repo = self.vcs_class(self.dir, self.username)
        self.assert_(repo.is_owner("new"))
        
        
    def test_remove_owner(self):
        self.test_add_owner()
        repo = self.vcs_class(self.dir, self.username)
        repo.remove_owner("new")
        repo.save()
                
        repo = self.vcs_class(self.dir, self.username)
        self.assertFalse(repo.is_owner("new"))
        

    def test_cannot_remove_last_owner(self):
        repo = self.vcs_class(self.dir, self.username)
        exception = False
        try:
            repo.remove_owner(self.username)
        except InvalidPermissions:
            exception = True
        
        self.assert_(exception)
        
        
    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        
        
        


class TestSvn(VCSTestBase, unittest.TestCase):
    vcs = svn
    vcs_class = svn.Subversion 
    
        
        
class TestGit(VCSTestBase, unittest.TestCase):
    vcs = git
    vcs_class = git.Git         
        
        
        
        
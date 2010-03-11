'''
Created on Mar 11, 2010

@author: epeli
'''


import unittest
import tempfile
import os
import shutil

from subuser.apps.vcs import git, svn


class TestVCS(object):
    username = "tester"
    vcs = None
    vcs_class = None


    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="subuser_test_tmp_")
        self.vcs.init_repository(self.dir, self.username)
    
    def test_test(self):
        self.assert_(os.path.exists(self.dir))
    
    
    def test_unknown_users_has_read_only_permissions(self):
        repo = self.vcs_class(self.dir)
        self.assert_(repo.has_permissions("nonexistent", "r"))
        self.assertFalse(repo.has_permissions("nonexistent", "rw"))
        self.assertFalse(repo.has_permissions("nonexistent", "w"))
    
    def test_default_permissions(self):
        repo = self.vcs_class(self.dir)
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
        repo = self.vcs_class(self.dir)
        repo.set_permissions("new", "rw")
        repo.save()
        
        repo = self.vcs_class(self.dir)
        self.assert_(repo.has_permissions("new", "rw"))
        self.assert_(repo.has_permissions("new", "w"))
        self.assert_(repo.has_permissions("new", "r"))    
    
    def test_remove_permissions(self):
        repo = self.vcs_class(self.dir)
        repo.set_permissions("new", "rw")
        repo.save()
        
        repo = self.vcs_class(self.dir)     
        repo.remove_all_permissions("new")
        repo.save()
        
        repo = self.vcs_class(self.dir)
        self.assertFalse(repo.has_permissions("new", "w"))
        self.assertFalse(repo.has_permissions("new", "rw"))        
        
        
    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        
        
        


class TestSvn(TestVCS, unittest.TestCase):
    vcs = svn
    vcs_class = svn.Subversion 
    
        
        
class TestGit(TestVCS, unittest.TestCase):
    vcs = git
    vcs_class = git.Git         
        
        
        
        
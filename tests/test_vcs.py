'''
Created on Mar 11, 2010

@author: epeli
'''


import unittest
import tempfile
import os
import shutil

from subssh.app.vcs import git, svn
from subssh.app.vcs.abstractrepo import InvalidPermissions
class UserRequest(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class VCSMixIn(object):
    username = "tester"
    vcs_class = None
    manager_class = None
    repo_name = "testingrepo"


    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix="subuser_test_tmp_")
        self.repomanager = self.manager_class(self.tempdir)
        
        user = UserRequest(username=self.username)
        
        self.repomanager.init(user, self.repo_name)
        
        self.dir = self.repomanager.real(self.repo_name)
    
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
        repo.remove_permissions("new")
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
        shutil.rmtree(self.tempdir, ignore_errors=True)
        
        
        


class TestSvn(VCSMixIn, unittest.TestCase):
    manager_class = svn.SubversionManager
    vcs_class = svn.Subversion 
    
        
        
class TestGit(VCSMixIn, unittest.TestCase):
    manager_class = git.GitManager
    vcs_class = git.Git
    

class RepoManagertMixIn(object):
    username = "tester"
    vcs_class = None
    manager_class = None
    repo_name = "testingrepo"


    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix="subuser_test_tmp_")
        self.repomanager = self.manager_class(self.tempdir)
        
        self.user = UserRequest(username=self.username)
        
        self.repomanager.init(self.user, self.repo_name)
        
        
    def test_get_repo_object(self):
        self.repomanager.get_repo_object(self.username, self.repo_name)


    def test_fork(self):
        forker = "forker"
        original_owner = self.username
        randomdude = "randomdude"
        
        repo = self.repomanager.get_repo_object(original_owner, self.repo_name)
        repo.set_permissions(randomdude, "rw")
        repo.add_owner(randomdude)
        repo.save()
        
        
        user = UserRequest(username=forker)
        self.repomanager.fork(user, self.repo_name, "newfork")
        
        newrepo = self.repomanager.get_repo_object(forker, "newfork")
        self.assert_(newrepo.has_permissions(forker, "rw"))
        self.assert_(newrepo.is_owner(forker))

        # Original owner is not owner in the fork
        self.assertFalse(newrepo.has_permissions(original_owner, "w"))
        self.assertFalse(newrepo.is_owner(original_owner))
        
        # Random dude has no permissions either        
        self.assertFalse(newrepo.has_permissions(randomdude, "w"))
        self.assertFalse(newrepo.is_owner(randomdude))
                

class TestGitManager(RepoManagertMixIn, unittest.TestCase):
    manager_class = git.GitManager
    
            
class TestSubversionManager(RepoManagertMixIn, unittest.TestCase):
    manager_class = svn.SubversionManager
        
        
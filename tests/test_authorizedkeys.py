# -*- coding: utf-8 -*-

'''
Created on Mar 9, 2010

@author: epeli
'''

import unittest
import tempfile
import sys
import os
import shutil


from subssh.authorizedkeys import AuthorizedKeysDB

from subssh.authorizedkeys import AuthorizedKeysException

THIS_DIR = os.path.dirname(__file__) 

class TestAuthorizedKeysDB(unittest.TestCase):
    
    def setUp(self):
        self.dir = tempfile.mkdtemp(suffix="subssh_tmp")
        shutil.copy(os.path.join(THIS_DIR, "authorized_keys"), self.dir)
        
        
    
    def test_lock(self):
        # Lock the file
        AuthorizedKeysDB._lock_timeout = 10
        db = AuthorizedKeysDB(self.dir)
        
        # Try opening another
        self.assertRaises(AuthorizedKeysException, 
                          AuthorizedKeysDB, self.dir)
    
    def test_test(self):
        pass
    
    def test_add_key(self):
        db = AuthorizedKeysDB(self.dir)
        
        self.assertRaises(KeyError, lambda: db.subusers["tester"])
        
        key_str = "tester ssh-rsa dummykey comment foobar"
        db.add_key_from_str("tester", key_str)
        db.commit()
        db.close()
        
        db = AuthorizedKeysDB(self.dir)
        db.subusers["tester"]
        self.assert_(db.subusers["tester"].has_key_str(key_str))
        
    
    def test_preserve_manually_created_keys(self):
        db = AuthorizedKeysDB(self.dir)
        
        manual_keys_before_adding = len(db.custom_key_lines) 
        
        
        db.add_key_from_str("tester", "tester ssh-rsa dummykey comment foobar")
        db.commit()
        db.close()
        
        
        db = AuthorizedKeysDB(self.dir)
        self.assertEquals(len(db.custom_key_lines), manual_keys_before_adding)
        
    
    def test_users_have_only_unique_keys(self):
        db = AuthorizedKeysDB(self.dir)
        db.add_key_from_str("tester", "tester ssh-rsa duplicatekey comment foobar")
        db.add_key_from_str("tester", "tester ssh-rsa duplicatekey different comment")
        db.commit()
        db.close()
        
        
        db = AuthorizedKeysDB(self.dir)
        tester = db.subusers["tester"]
        self.assertEqual(len(tester.pubkeys), 1)
        
        
        
    def test_different_users_can_have_same_keys(self):
        """
        This is stupid thing to do on clients part...
        """

        db = AuthorizedKeysDB(self.dir)
        db.add_key_from_str("user1", "tester ssh-rsa duplicatekey comment foobar")
        db.add_key_from_str("user2", "tester ssh-rsa duplicatekey comment foobar")
        db.commit()
        db.close() 
        
        
        db = AuthorizedKeysDB(self.dir)
        
        user1 = db.subusers["user1"]
        self.assert_(user1.has_key("duplicatekey"))
        
        user2 = db.subusers["user2"]
        self.assert_(user2.has_key("duplicatekey"))        
       
    

    def test_read_usernames(self):
        db = AuthorizedKeysDB(self.dir)
        db.subusers["essuuron"]
        db.subusers["foobar"]
    
    def test_foobar_has_two_keys(self):
        db = AuthorizedKeysDB(self.dir)
        count = len(db.subusers["foobar"].pubkeys.keys())
        self.assertEquals(count, 2)
    
            
    def tearDown(self):
        shutil.rmtree(self.dir)

if __name__ == "__main__":
    print "hello"
    
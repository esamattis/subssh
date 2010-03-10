# -*- coding: utf-8 -*-

'''
Created on Mar 9, 2010

@author: epeli
'''

import unittest

import sys
import os


from subuser.authorizedkeys import AuthorizedKeysDB
from subuser.authorizedkeys import parse_subuser_key
from subuser.authorizedkeys import AuthorizedKeysException

THIS_DIR = os.path.dirname(__file__) 

class TestParseSubuserKey(unittest.TestCase):
    
    def test_parse(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subuser foobar" ssh-rsa avain== kommentti'
        username, type, key, comment = parse_subuser_key(line)
        self.assertEquals(username, "foobar")
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "kommentti")
        
    def test_parse_multiple_comment_words(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subuser foobar" ssh-rsa avain== monisanainen kommentti'
        username, type, key, comment = parse_subuser_key(line)
        self.assertEquals(comment, "monisanainen kommentti")        
        
    
    def test_no_comment(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subuser foobar" ssh-rsa avain=='
        username, type, key, comment = parse_subuser_key(line)
        self.assertEquals(comment, "")        

    def test_simple_cmd(self):
        line = 'command="subuser foobar" ssh-rsa avain== kommentti'
        username, type, key, comment = parse_subuser_key(line)
        self.assertEquals(username, "foobar")
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "kommentti")
        
class TestAuthorizedKeysDB(unittest.TestCase):
    
    def setUp(self):
        self.db = AuthorizedKeysDB(THIS_DIR)
    
    def test_lock(self):
        exception = False
        try:
            AuthorizedKeysDB(THIS_DIR)
        except AuthorizedKeysException:
            exception = True
        self.assert_(exception)
    
    def test_test(self):
        pass

    def test_read_usernames(self):
        self.db.subusers["essuuron"]
        self.db.subusers["foobar"]
    
    def test_foobar_has_two_keys(self):
        count = len(self.db.subusers["foobar"].pubkeys.keys())
        self.assertEquals(count, 2)
    
            
    def tearDown(self):
#        self.db.commit()
        self.db.close()

if __name__ == "__main__":
    print "hello"
    
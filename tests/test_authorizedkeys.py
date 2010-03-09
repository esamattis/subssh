'''
Created on Mar 9, 2010

@author: epeli
'''

import unittest

import sys
import os


from subuser.authorizedkeys import AuthorizedKeysDB, parse_subuser_key

KEYPATH = os.path.join( os.path.dirname(__file__), "authorized_keys") 

class TestParseSubuserKey(unittest.TestCase):
    
    def test_parse(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subuser foobar" ssh-rsa avain== joku kommentti foobar@subuser'
        username, type, key, comment = parse_subuser_key(line)
        self.assertEquals(username, "foobar")
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "joku kommentti")
    
    def test_no_comment(self):
        line = 'command="PYTHONPATH=/home/epeli/SubUser/ SubUser/bin/subuser foobar" ssh-rsa avain== foobar@subuser'
        username, type, key, comment = parse_subuser_key(line)
        self.assertEquals(username, "foobar")
        self.assertEquals(type, "ssh-rsa")
        self.assertEquals(key, "avain==")
        self.assertEquals(comment, "")        


class TestAuthorizedKeysDB(unittest.TestCase):
    
    def setUp(self):
        self.db = AuthorizedKeysDB(KEYPATH)
    
    def test_test(self):
        pass

    def test_read_usernames(self):
        self.db.subusers["essuuron"]
        self.db.subusers["foobar"]
    
    def test_foobar_has_two_keys(self):
        count = len(self.db.subusers["foobar"].pubkeys.keys())
        self.assertEquals(count, 2)
    
    def test_dummy(self):
        for line in self.db.iter_in_authorized_keys_format():
            print line
    

if __name__ == "__main__":
    print "hello"
    
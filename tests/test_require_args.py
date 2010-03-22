'''
Created on Mar 22, 2010

@author: epeli
'''

import unittest

from subssh.tools import require_args, InvalidArguments 


class TestRequireArgumens(unittest.TestCase):
    

    def test_require_zero(self):
        @require_args(exactly=0)
        def f(username, cmd, args):
            pass
        f("user", "cmd", [])
        
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1])
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1,2])    
    
    
    def test_require_exactly_one(self):
        @require_args(exactly=1)
        def f(username, cmd, args):
            pass
        f("user", "cmd", [1])
        
        self.assertRaises(InvalidArguments, f, "user", "cmd", [])
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1,2])
        

    def test_require_at_least_two(self):
        @require_args(at_least=2)
        def f(username, cmd, args):
            pass
        f("user", "cmd", [1,2])
        f("user", "cmd", [1,2,3])
        
        self.assertRaises(InvalidArguments, f, "user", "cmd", [])
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1])
        
                    
    def test_require_at_most_two(self):
        @require_args(at_most=2)
        def f(username, cmd, args):
            pass
        
        f("user", "cmd", [])
        f("user", "cmd", [1,2])
        
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1,2,3])
        
        
    def test_require_2_to__4(self):
        @require_args(at_least=2, at_most=4)
        def f(username, cmd, args):
            pass
        
        self.assertRaises(InvalidArguments, f, "user", "cmd", [])
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1])        
        
        f("user", "cmd", [1,2])
        f("user", "cmd", [1,2,3])
        f("user", "cmd", [1,2,3,4])
        
        self.assertRaises(InvalidArguments, f, "user", "cmd", [1,2,3,4,5])        
        
        
                            
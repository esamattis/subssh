'''
Created on Mar 26, 2010

@author: epeli
'''

import unittest

from subssh.tools import assert_args
from subssh import  InvalidArguments






class TestRequireArgumensWithFunctions(unittest.TestCase):


    def test_require_zero(self):
        def f():
            pass

        assert_args(f, [])


        args = [1]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

        args = [1,2]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

    def test_localvar(self):
        def f():
            foo = 1

        assert_args(f, [])


        args = [1]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

        args = [1,2]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)




    def test_require_one(self):
        def f(user):
            pass

        assert_args(f, [1])

        args = [1,2]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)


    def test_require_two(self):
        def f(user, second):
            pass

        assert_args(f, [1, 2])

        args = [1]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

        args = [1,2,3]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)



    def test_require_1_to_n(self):
        def f(user, *args):
            pass

        assert_args(f, [1])
        assert_args(f, [1, 2])
        assert_args(f, [1, 2 ,3])


        args = []
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)


    def test_require_2_to_n(self):
        def f(user, second, *args):
            pass

        assert_args(f, [1, 2])
        assert_args(f, [1, 2 ,3])
        assert_args(f, range(100))


        args = []
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

        args = [1]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)




    def test_default_value(self):
        def f(user, value="default"):
            pass

        assert_args(f, [1])
        assert_args(f, [1, 2])


        args = []
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

        args = [1,2,3]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)



    def test_multi_default_values(self):
        def f(user, value="default", value2="default2"):
            pass

        assert_args(f, [1])
        assert_args(f, [1, 2])
        assert_args(f, [1, 2, 3])


        args = []
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)

        args = [1,2,3,4]
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)


    def test_default_with_n(self):
        def f(user, value="default", *args):
            pass

        assert_args(f, [1])
        assert_args(f, [1, 2])
        assert_args(f, [1, 2, 3])
        assert_args(f, [1, 2, 3, 4])


        args = []
        self.assertRaises(InvalidArguments, assert_args, f, args)
        self.assertRaises(TypeError, f, *args)


class TestRequireArgumensWithMethods(unittest.TestCase):


    def test_require_zero(self):
        class C(object):
            def m(self):
                pass
        o = C()

        assert_args(o.m, [])


        args = [1]
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)

        args = [1,2]
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)


    def test_require_one(self):
        class C(object):
            def m(self, user):
                pass
        o = C()

        assert_args(o.m, [1])

        args = [1,2]
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)


    def test_require_two(self):
        class C(object):
            def m(self, user, second):
                pass
        o = C()

        assert_args(o.m, [1, 2])

        args = [1]
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)

        args = [1,2,3]
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)



    def test_require_1_to_n(self):
        class C(object):
            def m(self, user, *args):
                pass
        o = C()

        assert_args(o.m, [1])
        assert_args(o.m, [1, 2])
        assert_args(o.m, [1, 2 ,3])


        args = []
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)


    def test_require_2_to_n(self):
        class C(object):
            def m(self, user, second, *args):
                pass
        o = C()

        assert_args(o.m, [1, 2])
        assert_args(o.m, [1, 2 ,3])
        assert_args(o.m, range(100))


        args = []
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)

        args = [1]
        self.assertRaises(InvalidArguments, assert_args, o.m, args)
        self.assertRaises(TypeError, o.m, *args)



class TestInvalidArgumentsArg(unittest.TestCase):

    def test_zero(self):
        def f():
            pass

        raised = False
        try:
            assert_args(f, [1])
        except InvalidArguments, e:
            raised = True
            self.assertEquals(e.args[0], 'Invalid argument count 1. Required 0 arguments.')

        self.assert_(raised)


    def test_1_to_n(self):
        class C(object):
            def m(self, user, second, *args):
                pass
        o = C()

        raised = False
        try:
            assert_args(o.m, [])
        except InvalidArguments, e:
            raised = True
            self.assertEquals(e.args[0], 'Invalid argument count 0. Required 2-n arguments.')

        self.assert_(raised)




# -*- coding: utf-8 -*-
'''
Created on Mar 9, 2010

@author: epeli
'''

from subssh import tools


@tools.expose_as()
def whoami(user):
    """Tells who you are
    """
    tools.writeln(user.username)



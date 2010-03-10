# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

import os.path

SVN_REPOS = os.path.join( os.environ["HOME"], "repos", "svn" )

GIT_REPOS = os.path.join( os.environ["HOME"], "repos", "git" )

CMD_LOG = os.path.join( os.environ["HOME"], ".subuser", "log", "cmds.log" )


SSH_HOME = os.path.join( os.environ["HOME"], ".ssh" )
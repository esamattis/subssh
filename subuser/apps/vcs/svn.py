# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''

"""
svnadmin create testi
svn -m "created project base" mkdir file:///$(pwd)/testi/trunk file:///$(pwd)/testi/tags



epeli@debian:~/repos/svn/testi$ tail conf/authz  -n 4
[/]
essuuron = rw
* = r


epeli@debian:~/repos/svn/testi$ cat conf/svnserve.conf
...
[general]
authz-db = authz
...

"""


import os
import subprocess


from subuser import tools

from permissions import VCSPermissions

class config:
    """Default config"""
    repositories = os.path.join( os.environ["HOME"], "repos", "svn" )
    webview = os.path.join( os.environ["HOME"], "repos", "webgit" )



def _create_svn_repository(path, owner):
    
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.abspath(path)
    
    tools.check_call(("svnadmin", "create", path))
    tools.check_call((
                      "svn", "-m", "created automatically project base", 
                      "mkdir", "file://%s" % os.path.join(path, "trunk"),
                               "file://%s" % os.path.join(path, "tags"),
                      ))

    
    confpath = os.path.join(path, "conf/svnserve.conf")
    conf = SafeConfigParser()
    conf.read(confpath)
    conf.set("general", "authz-db", "authz")
    f = open(confpath, "w")
    conf.write(f)
    f.close()
    
    subversion = Subversion(path)
    subversion.add_permission(owner, "rw")
    subversion.add_permission("*", "r")
    subversion.save()




class Subversion(VCSPermissions):
    
    
    required_by_valid_repo = (authzfilename, 
                              conffilename) = ("conf/authz", 
                                               "conf/svnserve.conf")
    _permissions_section = "/"
    
    

@tools.parse_cmd
def create_svn_repository(username, cmd, args):
    
    repo_name = tools.to_safe_chars(args[0])
     
    _create_svn_repository(os.path.join(config.repositories, repo_name), username)


@tools.parse_cmd
def handle_svn(username, cmd, args):
    
    return subprocess.call(['/usr/bin/svnserve', 
                            '--tunnel-user=' + username,
                            '-t', '-r',  
                            config.repositories])
    
    


cmds = {
        "svnserve": handle_svn,
        "svn-create-repo": create_svn_repository,
        }




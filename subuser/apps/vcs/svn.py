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
from ConfigParser import SafeConfigParser

from subuser import tools

from general import VCS, set_default_permissions

class config:
    repositories = os.path.join( os.environ["HOME"], "repos", "svn" )
    
    webview = os.path.join( os.environ["HOME"], "repos", "webgit" )
    
    rwurl = "svn+ssh://vcs.linkkijkl.fi/"

class Subversion(VCS):

    required_by_valid_repo = ("conf/svnserve.conf",)
    permdb_name= "conf/" + VCS.permdb_name
    _permissions_section = "/"
    

        
    
    
def enable_svn_permissions(path, dbfile="authz"):
    confpath = os.path.join(path, "conf/svnserve.conf")
    conf = SafeConfigParser()
    conf.read(confpath)
    conf.set("general", "authz-db", dbfile)
    f = open(confpath, "w")
    conf.write(f)
    f.close()

def init_repository(path, owner):
    
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.abspath(path)
    
    tools.check_call(("svnadmin", "create", path))
    tools.check_call((
                      "svn", "-m", "created automatically project base", 
                      "mkdir", "file://%s" % os.path.join(path, "trunk"),
                               "file://%s" % os.path.join(path, "tags"),
                      ))

    
    enable_svn_permissions(path, os.path.basename(Subversion.permdb_name))
    
    set_default_permissions(path, owner, Subversion)




    

@tools.parse_cmd
def handle_init_repo(username, cmd, args):
    
    repo_name = " ".join(args).strip()
     
    if not tools.safe_chars_only_pat.match(repo_name):
        tools.errln("Bad repository name. Allowed characters: %s (regexp)" % tools.safe_chars)
        return 1
     

    repo_path = os.path.join(config.repositories, repo_name)
    if os.path.exists(repo_path):
        tools.errln("Repository '%s' already exists." % repo_name)
        return 1
    
    
    init_repository(repo_path, username)

    tools.writeln("\nCreated Subversion repository to " +
                  config.rwurl + repo_name)




@tools.no_user
@tools.parse_cmd
def handle_svn(username, cmd, args):
    # Subversion can handle itself permissions and virtual root
    
    return subprocess.call(['/usr/bin/svnserve', 
                            '--tunnel-user=' + username,
                            '-t', '-r',  
                            config.repositories])
    
    
    


cmds = {
        "svnserve": handle_svn,
        "svn-init": handle_init_repo,
        }




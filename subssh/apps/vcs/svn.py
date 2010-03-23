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

from subssh import tools
from abstractrepo import VCS
from repomanager import RepoManager
from repomanager import parse_url_configs
from subssh.config import DISPLAY_HOSTNAME
import subssh.customlogger
logger = subssh.customlogger.get_logger(__name__)


class config:
    SVNSERVE_BIN = "svnserve"
    
    SVN_BIN = "svn"
    
    SVNADMIN_BIN = "svnadmin"
    
    REPOSITORIES = os.path.join( os.environ["HOME"], "repos", "svn" )

    WEBVIEW = os.path.join( os.environ["HOME"], "repos", "websvn" )
    
    URLS = """Read/Write|svn+ssh://$hostname/$name_on_fs
Webview|http://$hostname/websvn/$name_on_fs"""


    MANAGER_TOOLS = "true"

class Subversion(VCS):
    required_by_valid_repo = ("conf/svnserve.conf",)
    permdb_name= "conf/" + VCS.permdb_name
    # For svnserve, "/" stands for whole repository
    _permissions_section = "/"
    


class SubversionManager(RepoManager):
    
    klass = Subversion
    cmd_prefix = "svn-"
    
    def _enable_svn_perm(self, path, dbfile="authz"):
        """
        Set Subversion repository to use our permission config file
        """
        confpath = os.path.join(path, "conf/svnserve.conf")
        conf = SafeConfigParser()
        conf.read(confpath)
        conf.set("general", "authz-db", dbfile)
        f = open(confpath, "w")
        conf.write(f)
        f.close()


    def create_repository(self, path, owner):
        
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.abspath(path)
        
        tools.check_call((config.SVNADMIN_BIN, "create", path))
        tools.check_call((
                          config.SVN_BIN, "-m", "created automatically project base", 
                          "mkdir", "file://%s" % os.path.join(path, "trunk"),
                                   "file://%s" % os.path.join(path, "tags"),
                                   "file://%s" % os.path.join(path, "branches"),
                          ))
    
        
        self._enable_svn_perm(path, os.path.basename(Subversion.permdb_name))
        
        return 0


    




@tools.no_user
def handle_svn(username, cmd, args):
    # Subversion can handle itself permissions and virtual root.
    # So there's no need to manually check permissions here or
    # transform the virtual root.
    return subprocess.call((config.SVNSERVE_BIN, 
                            '--tunnel-user=' + username,
                            '-t', '-r',  
                            config.REPOSITORIES))
    
    
    
    


cmds = {
        "svnserve": handle_svn,
        }

def __appinit__():
    if tools.to_bool(config.MANAGER_TOOLS):
        manager = SubversionManager(config.REPOSITORIES, 
                                    urls=parse_url_configs(config.URLS) )
        cmds.update(manager.cmds)
        logger.info(config.URLS)


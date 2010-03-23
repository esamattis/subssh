# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli



git config --global user.name "Oma Nimi" && git config --global user.email oma.nimi@oma.domain
'''

import os
import subprocess
import re

from subssh import tools
from abstractrepo import VCS
from abstractrepo import InvalidPermissions
from repomanager import RepoManager
from repomanager import parse_url_configs
import subssh.customlogger

logger = subssh.customlogger.get_logger(__name__)

from subssh.config import DISPLAY_HOSTNAME



class config:
    GIT_BIN = "git"
    
    REPOSITORIES = os.path.join( os.environ["HOME"], "repos", "git" )
    
    WEBVIEW = os.path.join( os.environ["HOME"], "repos", "webgit" )

    MANAGER_TOOLS = "true"
    
    URLS = """Read/Write|ssh://$hostname/$name_on_fs
Read only clone|http://$hostname/repo/$name_on_fs
Webview|http://$hostname/gitphp/$name_on_fs"""



class Git(VCS):
    
    required_by_valid_repo  = ("config", 
                               "objects",
                               "hooks")

    permissions_required = { "git-upload-pack":    "r",
                             "git-upload-archive": "r",
                             "git-receive-pack":   "rw" }    
    
    
    @property
    def name(self):
        name = os.path.basename(self.repo_path)    
        if self.repo_path.endswith(".git"):
            return name[:-4]
        return name
    
    def execute(self, username, cmd, git_bin="git"):
        
        if not self.has_permissions(username, self.permissions_required[cmd]):
            raise InvalidPermissions("%s has no permissions to run %s on %s" %
                                     (username, cmd, self.repo_name))                                 
        
        shell_cmd = cmd + " '%s'" %  self.repo_path

        return subprocess.call((git_bin, "shell", "-c", shell_cmd))


class GitManager(RepoManager):
    cmd_prefix = "git-"
    suffix = ".git"
    klass = Git


    def create_repository(self, path, owner):
        
        os.chdir(path)
        
        tools.check_call((config.GIT_BIN, "init", "--bare"))
        
        f = open("hooks/post-update", "w")
        f.write("""#!/bin/sh
#
# Prepare a packed repository for use over
# dumb transports.
#

exec git-update-server-info

""")
        f.close()
        
        os.chmod("hooks/post-update", 0700)
    
            




            

            
    
valid_repo = re.compile(r"^/[%s]+\.git$" % tools.safe_chars)
@tools.no_user
def handle_git(username,  cmd, args):
    
    request_repo = args[0]
    
    if not valid_repo.match(request_repo):
        tools.errln("Illegal repository path '%s'" % request_repo)
        return 1    
    
    repo_name = request_repo.lstrip("/")
    
    # Transform virtual root
    real_repository_path = os.path.join(config.REPOSITORIES, repo_name)
    
    repo = Git(real_repository_path)
    
    try: # run requested command on the repository
        return repo.execute(username, cmd, git_bin=config.GIT_BIN)
    except InvalidPermissions, e:
        tools.errln(e.args[0], log=logger.warning)
        return 1
    


cmds = {
        "git-upload-pack": handle_git,
        "git-receive-pack": handle_git,
        "git-upload-archive": handle_git,
        }


def __appinit__():
    if tools.to_bool(config.MANAGER_TOOLS):
        manager = GitManager(config.REPOSITORIES, 
                             urls=parse_url_configs(config.URLS) )
        cmds.update(manager.cmds)


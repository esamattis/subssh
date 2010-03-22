# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli



git config --global user.name "Oma Nimi" && git config --global user.email oma.nimi@oma.domain
'''

import os
import subprocess
import subssh.customlogger
import re

from subssh import tools

from abstractrepo import VCS
from abstractrepo import InvalidPermissions
from repomanager import RepoManager

logger = subssh.customlogger.get_logger(__name__)

from subssh.config import DISPLAY_HOSTNAME



class config:
    GIT_BIN = "git"
    
    REPOSITORIES = os.path.join( os.environ["HOME"], "repos", "git" )
    
    WEBVIEW = os.path.join( os.environ["HOME"], "repos", "webgit" )
    
    RWURL = "ssh://%s@%s/" % (tools.admin_name(), DISPLAY_HOSTNAME )

    MANAGER_TOOLS = "true"


class Git(VCS):
    
    required_by_valid_repo  = ("config", 
                               "objects",
                               "hooks")

    permissions_required = { "git-upload-pack":    "r",
                             "git-upload-archive": "r",
                             "git-receive-pack":   "rw" }    
    
    
    def execute(self, username, cmd, git_bin="git"):
        
        if not self.has_permissions(username, self.permissions_required[cmd]):
            raise InvalidPermissions("%s has no permissions to run %s on %s" %
                                     (username, cmd, self.repo_name))                                 
        
        shell_cmd = cmd + " '%s'" %  self.repo_path

        return subprocess.call((git_bin, "shell", "-c", shell_cmd))


class GitManager(RepoManager):

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
    

def print_config(*args):
    print cmds
    

cmds = {
        "git-upload-pack": handle_git,
        "git-receive-pack": handle_git,
        "git-upload-archive": handle_git,
        "config": print_config
        }


if tools.to_bool(config.MANAGER_TOOLS):
    manager = GitManager(config.REPOSITORIES, Git, suffix=".git",
                         cmd_prefix="git-")
    cmds.update(manager.cmds)


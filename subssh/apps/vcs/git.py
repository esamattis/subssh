# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli



git config --global user.name "Oma Nimi" && git config --global user.email oma.nimi@oma.domain
'''

import os
import sys
import subprocess
import logging
import re

from subssh import tools

from general import VCS, set_default_permissions, InvalidPermissions

logger = logging.getLogger(__name__)






class config:
    GIT_BIN = "git"
    
    REPOSITORIES = os.path.join( os.environ["HOME"], "repos", "git" )
    
    WEBVIEW = os.path.join( os.environ["HOME"], "repos", "webgit" )
    
    RWURL = "ssh://vcs.linkkijkl.fi/"

    


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




def init_repository(path, owner):
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.abspath(path)
    
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


    set_default_permissions(path, owner, Git)

    







def handle_init_repo(username, cmd, args):
    """
    usage: git-init <repository name without .git extensions>
    """

    
    repo_name = " ".join(args).strip()
     
    if not tools.safe_chars_only_pat.match(repo_name):
        tools.errln("Bad repository name. Allowed characters: %s (regexp)" 
                    % tools.safe_chars)
        return 1
     
    repo_name += ".git" 
    
    repo_path = os.path.join(config.REPOSITORIES, repo_name)
    if os.path.exists(repo_path):
        tools.errln("Repository '%s' already exists." % repo_name)
        return 1
    
    
    init_repository(repo_path, username)

    tools.writeln("\nCreated Git repository to " +
                  config.RWURL + repo_name)

    return 0



            
def hanle_set_permissions(username,  cmd, args):
    """
    usage: git-set-permissions <username> <permissions> <repo_name>
    
    eg. git-set-permissions essuuron rw myrepository
    """
    
    target_username = args[0]
    new_permissions = args[1]
    repo_name = args[2] + ".git"
    
    repo = Git(os.path.join(config.REPOSITORIES, repo_name), username)
    
    repo.set_permissions(target_username, new_permissions)
    repo.save()
            
            
    
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
        tools.errln(e.args[0], log=logger.error)
        return 1
    


cmds = {
        "git-upload-pack": handle_git,
        "git-receive-pack": handle_git,
        "git-upload-archive": handle_git,
        "git-init": handle_init_repo,
        "git-set-permissions": hanle_set_permissions,
        }

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

from subuser import tools

from general import VCS, set_default_permissions

logger = logging.getLogger(__name__)

valid_repo = re.compile(r"^/[a-z_-]+\.git$")

gitshell = [ "git", "shell", "-c"]

permissions = {
        "git-upload-pack": "r",
        "git-upload-archive": "r",
        "git-receive-pack": "rw",
        }




class config:
    """Default config"""
    repositories = os.path.join( os.environ["HOME"], "repos", "git" )
    webview = os.path.join( os.environ["HOME"], "repos", "webgit" )
    rwurl = "ssh://vcs.linkkijkl.fi/"



class Git(VCS):
    
    
    required_by_valid_repo  = ("config", 
                               "objects",
                               "hooks")






def init_repository(path, owner):
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.abspath(path)
    
    os.chdir(path)
    
    tools.check_call(("git", "init", "--bare"))
    
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

    



def unquote(string):
    return string.strip().strip("'").strip('"').strip()





@tools.parse_cmd
def handle_init_repo(username, cmd, args):
    
    repo_name = " ".join(args).strip()
     
    if not tools.safe_chars_only_pat.match(repo_name):
        tools.errln("Bad repository name. Must match [%s]+" % tools.safe_chars)
        return 1
     
    repo_name += ".git"
    
    repo_path = os.path.join(config.repositories, repo_name)
    if os.path.exists(repo_path):
        tools.errln("Repository %s already exists." % repo_name)
        return 1
    
    
    init_repository(repo_path, username)

    tools.writeln("\nCreated Git repository to " +
                  config.rwurl + repo_name)




def check_permissions(username, cmd, repo_path):
    repo = Git(repo_path)
    if username == repo.owner:
        return True
    
    required = permissions[cmd.strip()]
    return repo.has_permissions(username, required)
            
        
    

@tools.no_user
@tools.parse_cmd
def handle_git(username,  cmd, args):
    
    request_repo = unquote(args[0])
    
    if not valid_repo.match(request_repo):
        msg = "illegal repository path '%s'" % request_repo
        logger.fatal("%s tried to access %s" % (username, msg))
        sys.stderr.write(msg.capitalize() + "\n")
        return 1    
    
    real_repository = os.path.join(config.repositories, 
                                   request_repo.lstrip("/"))
    
    
    if not check_permissions(username, cmd, real_repository):
        tools.errln("Subuser unauthorized")
        return 1
    
    
    git_cmd = cmd + " '%s'" %  real_repository
    gitshell.append(git_cmd)
    return subprocess.call(gitshell)
    


cmds = {
        "git-upload-pack": handle_git,
        "git-receive-pack": handle_git,
        "git-upload-archive": handle_git,
        "git-init": handle_init_repo,
        }

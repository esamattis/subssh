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


class config:
    """Default config"""
    repositories = os.path.join( os.environ["HOME"], "repos", "git" )
    webview = os.path.join( os.environ["HOME"], "repos", "webgit" )



class Git(VCS):
    
    
    required_by_valid_repo  = ("config", 
                               "objects",
                               "hooks")






def _create_repository(path, owner):
    
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


exec git-update-server-info""")
    f.close()
    
    os.chmod("hooks/post-update", 0700)


    set_default_permissions(path, owner, Git)

    



def unquote(string):
    return string.strip().strip("'").strip('"').strip()


    
@tools.parse_cmd
def handle_git(username,  cmd, args):
    
    
    gitshell = [ "git", "shell", "-c"]

    request_repo = unquote(args[0])
    
    if not valid_repo.match(request_repo):
        msg = "illegal repository '%s'" % request_repo
        logger.fatal("%s tried to access %s" % (username, msg))
        sys.stderr.write(msg.capitalize() + "\n")
        return 1    
    
    repo_to_be_served = os.path.join(config.repositories, request_repo.lstrip("/"))
    
    git_cmd = cmd + " '%s'" %  repo_to_be_served
    
    gitshell.append(git_cmd)
    
    return subprocess.call(gitshell)
    


cmds = {
        "git-upload-pack": handle_git,
        "git-receive-pack": handle_git,
        "git-upload-archive": handle_git,
        }

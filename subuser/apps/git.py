'''
Created on Mar 5, 2010

@author: epeli
'''

import os
import sys
import subprocess
import logging
import re

import config
import tools

logger = logging.getLogger(__name__)

valid_repo = re.compile(r"^/[a-z_-]+\.git$")


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
    
    repo_to_be_served = os.path.join(config.GIT_REPOS, request_repo.lstrip("/"))
    
    git_cmd = cmd + " '%s'" %  repo_to_be_served
    
    gitshell.append(git_cmd)
    
#    sys.stderr.write(str(gitshell))
    return subprocess.call(gitshell)
    


cmds = {
        "git-upload-pack": handle_git,
        "git-receive-pack": handle_git,
        "git-upload-archive": handle_git,
        }

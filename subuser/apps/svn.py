'''
Created on Mar 5, 2010

@author: epeli
'''


import subprocess

import config



def handle_svn(username, cmd, args):
    
    return subprocess.call(['/usr/bin/svnserve', 
                            '--tunnel-user=' + username,
                            '-t', '-r',  
                            config.SVN_REPOS])
    
    


cmds = {"svnserve": handle_svn}
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


import subprocess

import tools
import config


@tools.parse_cmd
def handle_svn(username, cmd, args):
    
    return subprocess.call(['/usr/bin/svnserve', 
                            '--tunnel-user=' + username,
                            '-t', '-r',  
                            config.SVN_REPOS])
    
    


cmds = {"svnserve": handle_svn}
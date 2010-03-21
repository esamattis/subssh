# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''


import os
import socket
import shutil
from ConfigParser import SafeConfigParser

_THIS_DIR = os.path.abspath(os.path.dirname(__file__))

LOG_ACCESS = os.path.join( os.environ["HOME"], ".subssh", "access.log" )

LOG_ERROR = os.path.join( os.environ["HOME"], ".subssh", "error.log" )

LOG_USERS = os.path.join( os.environ["HOME"], ".subssh", "users" )

TRACEBACKS = os.path.join( os.environ["HOME"], ".subssh", "tracebacks" )

DISPLAY_HOSTNAME = socket.gethostname() 

# HAX
PYTHON_PATH = "/".join(_THIS_DIR.split("/")[-1:])

SUBSSH_BIN = os.path.join(PYTHON_PATH, "bin", "subssh")

DEFAULT_CONFIG_PATH = os.path.join(_THIS_DIR, "dist", "config")

SUBSSH_HOME = os.path.join(os.environ['HOME'], ".subssh")

CONFIG_PATH = os.path.join(SUBSSH_HOME, "config")


for dir in (SUBSSH_HOME, LOG_USERS, TRACEBACKS):
    if not os.path.exists(dir):
        os.mkdir(dir)
        
# Copy default config
if not os.path.exists(CONFIG_PATH):
    shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)


_config = SafeConfigParser()
_config.read(CONFIG_PATH)

for option, value in _config.items("general"):
    globals()[option.upper()] = value

def yield_enabled_apps():
    for sec in _config.sections():
        if sec.startswith("app:"):
            yield (sec.replace("app:", "").strip(),
                   _config.items(sec) )
            
        

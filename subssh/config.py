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

LOG = os.path.join( os.environ["HOME"], ".subuser", "log", "cmds.log" )

PROMPT_HOST = socket.gethostname() 

# HAX
PYTHON_PATH = "/".join(_THIS_DIR.split("/")[-1:])

SUBSSH_BIN = os.path.join(PYTHON_PATH, "bin", "subssh")

DEFAULT_CONFIG_PATH = os.path.join(_THIS_DIR, "dist", "config")

CONFIG_DIR = os.path.join(os.environ['HOME'], ".subssh")




if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)

CONFIG_PATH = os.path.join(CONFIG_DIR, "config")

if not os.path.exists(CONFIG_PATH):
    shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)


_config = SafeConfigParser()
_config.read(CONFIG_PATH)


for option, value in _config.items("general"):
    globals()[option] = value

def yield_enabled_apps():
    for sec in _config.sections():
        if sec.startswith("app:"):
            yield (sec.replace("app:", "").strip(),
                   _config.items(sec) )
            
        
        
        

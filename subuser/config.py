# -*- coding: utf-8 -*-

'''
Created on Mar 5, 2010

@author: epeli
'''


import os.path
from ConfigParser import SafeConfigParser


# Defaults
log = os.path.join( os.environ["HOME"], ".subuser", "log", "cmds.log" )



this = os.path.abspath(os.path.dirname(__file__))
# TODO: Move to home
config_path = os.path.join(this, "dist", "config")

_config = SafeConfigParser()
_config.read(config_path)


for option, value in _config.items("general"):
    globals()[option] = value

def yield_enabled_apps():
    for sec in _config.sections():
        if sec.startswith("app:"):
            yield (sec.replace("app:", "").strip(),
                   _config.items(sec) )
            
        
        
        

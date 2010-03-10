# -*- coding: utf-8 -*-

import sys

from subuser import config
import uptime

cmds = {}



for module_path, options in config.yield_enabled_apps():
    last = module_path.split(".")[-1]
    imported = __import__(module_path, fromlist=[last])
    
    if hasattr(imported, "cmds"):
        cmds.update(imported.cmds)
        if hasattr(imported, "config"):
            for option, value in options:
                setattr(imported.config, option, value)
    else:
        raise ImportError("%s is not valid Supuser app" % module_path)
    
    
    



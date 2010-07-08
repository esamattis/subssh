# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Esa-Matti Suuronen <esa-matti@suuronen.org>

This file is part of subssh.

Subssh is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Subssh is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public 
License along with Subssh.  If not, see 
<http://www.gnu.org/licenses/>.
"""


import config
import tools
import customlogger
logger = customlogger.get_logger(__name__)

def import_subssh_app(module_path, options):
    """
    Import Subssh app 
    """
    last = module_path.split(".")[-1]
    
    imported =  __import__(module_path, globals(), locals(), [last])
    
    # Override default config with the user config
    if hasattr(imported, "config"):
        for option, value in options:
            setattr(imported.config, option, value)
    
    # Run init if app has one
    if hasattr(imported, "__appinit"):
        imported.__appinit()        

    return imported    
    
    



def import_all_apps_from_config():
    """Imports all the apps user has enabled in config file"""
    
    
    for module_path, options in config.yield_enabled_apps():
        
        try:
            import_subssh_app(module_path, options)
        except ImportError, e:
            # TODO: Should log the traceback
            tools.errln("Warning: Could not import app %s" % module_path)
            logger.error("Could not import app %s reason: %s" 
                         % (module_path, e) )

                
                
    








'''
Created on Mar 26, 2010

@author: epeli
'''

import config

def import_subssh_app(module_path):
    """
    Import Subssh app 
    
    
    """
    last = module_path.split(".")[-1]
    imported = __import__(module_path, fromlist=[last])

    return imported    
    
    



def import_all_apps_from_config():
    """Imports all the apps user has enabled in config file"""
    
    
    for module_path, options in config.yield_enabled_apps():
        
        imported = import_subssh_app(module_path)
        
        # Override default config with the user config
        if hasattr(imported, "config"):
            for option, value in options:
                setattr(imported.config, option, value)
        
        # Run init if app has one
        if hasattr(imported, "__appinit__"):
            imported.__appinit__()
            
            
    








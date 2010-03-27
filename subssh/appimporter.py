'''
Created on Mar 26, 2010

@author: epeli
'''

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
    if hasattr(imported, "__appinit__"):
        imported.__appinit__()        

    return imported    
    
    



def import_all_apps_from_config():
    """Imports all the apps user has enabled in config file"""
    
    
    for module_path, options in config.yield_enabled_apps():
        
        try:
            import_subssh_app(module_path, options)
        except ImportError, e:
            tools.errln("Warning: Could not import app %s" % module_path)
            logger.error("Could not import app %s reason: %s" 
                         % (module_path, e) )

                
                
    








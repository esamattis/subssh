# -*- coding: utf-8 -*-

from subssh import config

cmds = {}

class UnknownCmd(Exception):
    pass

def import_subuser_app(module_path, options):
    """
    Import Subuser apps and overrides their default config. 
    
    Raises ImportError if module is not valid Subuser app.
    
    """
    last = module_path.split(".")[-1]
    imported = __import__(module_path, fromlist=[last])

    
    # Subuser apps must have cmds-attribute
    if hasattr(imported, "cmds"):
        # config attribute is optional
        if hasattr(imported, "config"):
            # Override default config with the user config
            for option, value in options:
                setattr(imported.config, option, value)
    
    else:
        raise ImportError("%s is not valid Subuser app" % module_path)
    
    return imported    
    
    

def get_all_apps():
    for module_path, options in config.yield_enabled_apps():
        imported = import_subuser_app(module_path, options)
        
        cmds.update(imported.cmds)

    return cmds.items()
    
    
    
def load(cmd):
    """
    Load requested app.
    """
    
    try:
        return cmds[cmd]
    except KeyError:
        pass
    
    for module_path, options in config.yield_enabled_apps():
        imported = import_subuser_app(module_path, options)
        cmds.update(imported.cmds)            
        try:
            return imported.cmds[cmd]
        except KeyError:
            continue
        
    raise UnknownCmd(cmd)
        




from subuser import config
import uptime

cmds = {}

#modules = map(__import__, config.ENABLED_APPS, level=0)
#
#
#print config.ENABLED_APPS
#print [dir(m) for m in  modules]
#
#for module in modules:
#    if hasattr(module, "cmds"):
#        cmds.update(module.cmds)



def import_last(module_path):
    """
    import last part of subuser app path.
    Eg. subuser.apps.vcs.git is translated to
    from subuser.apps.vcs import git
    """
    __import__(module_path)
    parts = module_path.split(".")
    parent = parts[-2]
    last = parts[-1]
    if parent != "apps":
        imported = getattr(globals()[parent], last)
        globals()[last] = imported
        return imported 
    else:
        return globals()[last]
    


for module_path, options in config.yield_enabled_apps():
    imported = import_last(module_path)
    if hasattr(imported, "cmds"):
        cmds.update(imported.cmds)
        if hasattr(imported, "config"):
            for option, value in options:
                setattr(imported.config, option, value)
    else:
        raise ImportError("%s is not valid Supuser app" % module_path)
    
    
    



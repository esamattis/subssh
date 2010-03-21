# -*- coding: utf-8 -*-

import sys

from subssh import config

import tools


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
    

def user_apps():
    return [ app_name for app_name, app in get_all_apps()
             if not getattr(app, "no_user", False) ]

    
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
        


def run(username, cmd, args):
    
    try:
        app = load(cmd)
    except UnknownCmd:
        sys.stderr.write("Unknown command \"%s\"\n" % cmd)
        return 1
    
    return app(username, cmd, args)


# Buildins


def commands(username, cmd, args):
    """list all commands"""
    for name in user_apps():
        tools.writeln(name)
        
cmds["commands"] = commands
cmds["help"] = lambda *args: tools.writeln("type 'commands' to list all available "
                                     "commands. 'man <app>' will display "
                                     "the command's doc string")    
    
def exit(username, cmd, args):
    """
    usage: exit [exit status]
    """
    try:
        return int(args[0])
    except (ValueError, IndexError):
        return 0
cmds["exit"] = exit
cmds["logout"] = exit

def show_doc(username, cmd, args):
    """
    usage: man <another command>
    """
    try:
        
        doc = cmds[args[0]].__doc__
    except IndexError:
        doc = man.__doc__
    
    if doc:
        tools.writeln(doc)
    else:
        tools.writeln("'%s' has no doc string" % args[0])
    
cmds["man"] = show_doc    

    


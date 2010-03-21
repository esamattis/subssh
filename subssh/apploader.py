# -*- coding: utf-8 -*-

import os
import sys
import traceback
import time

from subssh import config
import customlogger
import tools

logger = customlogger.get_logger(__name__)

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
    # Log all commands that are ran
    # TODO: preserve history for prompt
    user_logger = customlogger.get_user_logger(username)
    user_logger.info("%s %s" % (cmd, args)) 
    
    try:
        app = load(cmd)
    except UnknownCmd:
        sys.stderr.write("Unknown command \"%s\"\n" % cmd)
        return 1
    
    try:
        return app(username, cmd, args)
    except Exception, e:
        # Show traceback if user is admin
        if username == tools.admin_name():
            traceback.print_exc()
        else:
            # Log traceback
            timestamp = str(time.time())
            logger.error("%s's traceback logged to %s" % (username, timestamp))
            f = open(os.path.join(config.TRACEBACKS, timestamp), "w")
            traceback.print_exc(file=f)
            f.close()
            tools.errln("System error (%s): %s" % (timestamp, e.args[0]))
            
        return 1
    

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
        doc = show_doc.__doc__
    
    if doc:
        tools.writeln(doc)
    else:
        tools.writeln("'%s' has no doc string" % args[0])
    
cmds["man"] = show_doc    

    


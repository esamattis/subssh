# -*- coding: utf-8 -*-

import os
import sys
import traceback

from subssh import config
import customlogger
import tools

logger = customlogger.get_logger(__name__)


# All known applications are set to this dictionary
cmds = {}



def import_subuser_app(module_path, options):
    """
    Import Subuser apps and overrides their default config. 
    
    Raises ImportError if module is not valid Subuser app.
    
    """
    last = module_path.split(".")[-1]
    imported = __import__(module_path, fromlist=[last])

    
    # Subuser apps must have cmds-attribute
    if hasattr(imported, "cmds"):
        
        # Override default config with the user config
        if hasattr(imported, "config"):
            for option, value in options:
                setattr(imported.config, option, value)

        # Run init if app has one
        if hasattr(imported, "__appinit__"):
            imported.__appinit__()
            
    
    else:
        raise ImportError("%s is not valid Subuser app" % module_path)
    
    return imported    
    
    

def load_all_apps():
    # TODO: Ability to reload
    if cmds:
        return cmds.items()
    
    for module_path, options in config.yield_enabled_apps():
        imported = import_subuser_app(module_path, options)
        
        cmds.update(imported.cmds)

    return cmds.items()
    

def user_apps():
    return [ app_name for app_name, app in load_all_apps()
             if not getattr(app, "no_user", False) ]

    

def run(username, cmd, args):
    # Log all commands that are ran
    # TODO: preserve history for prompt
    
    user_logger = customlogger.get_user_logger(username)
    user_logger.info("%s %s" % (cmd, args)) 
    
    try:
        app = cmds[cmd]
    except KeyError:
        sys.stderr.write("Unknown command '%s'\n" % cmd)
        return 1
    
        
    
    try:
        return app(username, cmd, args)
    except tools.InvalidArguments, e:
        tools.errln("Invalid arguments. %s" % e.args[0])
        show_doc(username, "man", [cmd])
        return 1
    except tools.SoftException, e:
        # Expected exception. Print error to user.
        tools.errln("%s: %s" % (e.__class__.__name__, e.args[0]))
        return 1
    except Exception, e:
        # Unexpected exception! Log it!
        
        # Show traceback if user is admin
        if username == tools.admin_name():
            traceback.print_exc()
        else:
            # Log traceback
            import time
            timestamp = time.time()
            
            f = open(os.path.join(config.TRACEBACKS, 
                                  "%s-%s" % (timestamp, username)), 
                    "w")
            
            f.write("%s %s\n" %(cmd, args))
            traceback.print_exc(file=f)
            f.close()
            tools.errln("System error (%s): %s: %s" % (timestamp, 
                                                   e.__class__.__name__,
                                                   e.args[0]))
            
        return 1
    

load_all_apps()


# Buildins


def commands(username, cmd, args):
    """list all commands"""
    for name in sorted(user_apps()):
        tools.writeln(name)
        
cmds["commands"] = commands
cmds["help"] = lambda *args: tools.writeln(
"""
    type commands to list all available commands.
     
        man <app> 
    
    will display the command's doc string
""")    
    
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
    except KeyError:
        tools.errln("Unkown command '%s'" % args[0])
        return 1
    
    
    
    if doc:
        # Set document variables
        doc = doc % {'name': args[0]}
        tools.writeln(doc)
    else:
        tools.writeln("'%s' has no doc string" % args[0])
    
cmds["man"] = show_doc    

    


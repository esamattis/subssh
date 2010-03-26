# -*- coding: utf-8 -*-

import os
import sys
import traceback
from string import Template

import active
import customlogger
import tools
import config
import buildins

logger = customlogger.get_logger(__name__)




def import_subuser_app(module_path, options):
    """
    Import Subuser apps and overrides their default config. 
    
    Raises ImportError if module is not valid Subuser app.
    
    """
    last = module_path.split(".")[-1]
    imported = __import__(module_path, fromlist=[last])

    
        
    # Override default config with the user config
    if hasattr(imported, "config"):
        for option, value in options:
            setattr(imported.config, option, value)

    # Run init if app has one
    if hasattr(imported, "__appinit__"):
        imported.__appinit__()
        
    if hasattr(imported, "cmds"):
        active.cmds.update(imported.cmds)
    
    
    return imported    
    
    

def load_all_apps():
    
    for module_path, options in config.yield_enabled_apps():
        imported = import_subuser_app(module_path, options)
        

    return active.cmds.items()
    



    

def run(user, args):
    # Log all commands that are ran
    # TODO: preserve history for prompt
    
    user_logger = customlogger.get_user_logger(user.username)
    user_logger.info("%s %s" % (user.cmd, args)) 
    
    try:
        app = active.cmds[user.cmd]
    except KeyError:
        sys.stderr.write("Unknown command '%s'\n" % user.cmd)
        return 1
    
    
    
    try:
        # Ignore "user" which is always supplied.
        tools.assert_args(app, args, ignore=1)
        # Execute the app
        return app(user, *args)
    except tools.InvalidArguments, e:
        tools.errln("Invalid arguments. %s" % e.args[0])
        buildins.show_doc(user, user.cmd)
        return 1
    except tools.SoftException, e:
        # Expected exception. Print error to user.
        tools.errln("%s: %s" % (e.__class__.__name__, e.args[0]))
        return 1
    except Exception, e:
        # Unexpected exception! Log it!
        
        #  We can just print the traceback if user is admin
        if user.username == config.ADMIN:
            traceback.print_exc()
        else:
            # Log traceback
            import time
            timestamp = time.time()
            
            f = open(os.path.join(config.TRACEBACKS, 
                                  "%s-%s" % (timestamp, user.username)), 
                    "w")
            
            f.write("%s %s\n" %(user.cmd, args))
            traceback.print_exc(file=f)
            f.close()
            tools.errln("System error (%s): %s: %s" % (timestamp, 
                                                   e.__class__.__name__,
                                                   e.args[0]))
            tools.errln("Please report to admin.")
            
        return 1
    



load_all_apps()



    


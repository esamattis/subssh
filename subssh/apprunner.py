'''
Created on Mar 26, 2010

@author: epeli
'''

import sys
import os
import traceback

import config
import buildins
import tools
import active

    

def run(user, args):
    # Log all commands that are ran
    # TODO: preserve history for prompt
    
    
    user.logger.info("%s %s" % (user.cmd, args)) 
    
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
    except tools.UserException, e:
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
            
            f.write("%s %s\n" % (user.cmd, args))
            traceback.print_exc(file=f)
            f.close()
            tools.errln("System error (%s): %s: %s" % (timestamp, 
                                                   e.__class__.__name__,
                                                   e.args[0]))
            tools.errln("Please report to admin.")
            
        return 1
    


'''
Created on Mar 23, 2010

@author: epeli


This an example subssh application.


'''

import sys

from subssh import tools


class config:
    """
    Optional configuration object. This can be any object of which attributes 
    can be rewritten. Use only upper case attributes. 
    """
    MESSAGE = "Hello"
    ENABLE_ANOTHER = "disabled"


@tools.require_args(exactly=1)
def hello_cmd(username, cmd, args):
    """
    This is doc string. It will be used as man page of this command.
    '%(name)s' will be replaced by the name of calling cmd.  
    """
    tools.writeln("%s %s! You said %s" 
                  % (config.MESSAGE, username, args[0]))
    
    
    # Return value will be the exit status of the command. Zero means success.
    # None will be converted to 0 (return statement omitted).
    return 0 



def another_hello(username, cmd, args):
    """
    This app only greets you
    """
    sys.stdout.write("Another hello here!\n")
    return 0


# cmds is the only required variable in subssh apps.
# Add default app to it
cmds = {"hello": hello_cmd}




def __appinit__():
    """
    Optional __appinit__ is run at import time after the default config is 
    overridden by user's config.
    """
    
    # Enable other cmds depending on configuration
    if config.ENABLE_ANOTHER == "enabled":
        cmds['another-hello'] = another_hello
        
        
        
        
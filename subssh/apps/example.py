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


def hello_cmd(username, cmd, args):
    """
    This is doc string. It will be used as man page of this command.
    '$cmd' will be replaced by the name of calling cmd.  
    """
    tools.writeln("%s %s! You said %s" 
                  % (config.MESSAGE, username, " ".join(args)))
    
    
    # Return value will be the exit status of the command. Zero means success.
    # None will be converted to 0 (return statement omitted).
    return 0 



def another_hello(username, cmd, args):
    """
    This app only greets you
    """
    sys.stdout.write("Another hello here!\n")
    return 0


class MyError(tools.SoftException): pass
# @tools.require_args can be used to restrict arguments passed to cmd.
# If requirement is not met an InvalidArguments(SoftException) is raised and
# doc string of the cmd is printed
@tools.require_args(exactly=1)
def soft_exception_example(username, cmd, args):
    """
    This application demonstrates SoftExceptions.
    
    usage: $cmd writethis
    
    """
    
    
    if args[0] == "writethis":
        tools.writeln("ok")
    else:
        raise MyError("First argument must be 'writethis'")
    
    
@tools.no_user
def no_prompt(username, cmd, args):
    """
    This cmd won't show up on commads listing
    """
    tools.writeln("Used directly")

# cmds is the only required variable in subssh apps.
# Add default apps to it
cmds = {
        "hello": hello_cmd,
        "do_what_i_say": soft_exception_example,
        "doesnt_show_on_promt": no_prompt,
        }




def __appinit__():
    """
    Optional __appinit__ is run at import time after the default config is 
    overridden by user's config.
    """
    
    # Enable other cmds depending on configuration
    if config.ENABLE_ANOTHER == "enabled":
        cmds['another-hello'] = another_hello
        
        
        
        
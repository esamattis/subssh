# -*- coding: utf-8 -*-
'''
Created on Mar 8, 2010

@author: epeli
'''

import sys
import os
import subprocess
import re
import traceback
import inspect

import active
import customlogger
logger = customlogger.get_logger(__name__)

safe_chars = r"a-zA-Z_\-\."

safe_chars_only_pat = re.compile(r"^[%s]+$" % safe_chars )


not_safe_char = re.compile(r"[^%s]{1}" % safe_chars)
def to_safe_chars(string):
    string = string.replace("ä", "a")
    string = string.replace("Ä", "A")
    string = string.replace("ö", "o")
    string = string.replace("Ö", "O")
    string = string.replace(" ", "_")
    return not_safe_char.sub("", string)
            

class SoftException(Exception):
    """Exception class that will not get logged as system error when uncaught
    """

def to_bool(value):
        return str(value).lower() in ("true", "1",  "enabled")


def to_cmd_args(input):
    if isinstance(input, str):
        parts = input.split()
    else:
        parts = input
    
    try:
        cmd = parts[0]
    except IndexError:
        cmd = ""
    
    try:
        args = parts[1:]
    except IndexError:
        args = []        
        
    return cmd, args
    
    
def no_user(f):
    f.no_user = True
    return f
    


def writeln(msg="", out=sys.stdout, log=None):
    if log and msg:
        log(msg)
        
    out.write("%s\n"  % msg)

def errln(msg, log=None):
    writeln(msg, out=sys.stderr, log=log)
    


class CalledProcessError(Exception):
    """This exception is raised when a process run by check_call() returns
    a non-zero exit status.  The exit status will be stored in the
    returncode attribute."""
    def __init__(self, returncode, cmd):
        self.returncode = returncode
        self.cmd = cmd
    def __str__(self):
        return ("Command '%s' returned non-zero exit status %d" 
                % (self.cmd, self.returncode))


def check_call(cmd, *args, **kw):
    """
    subprocess.check_call is new in Python 2.5. This is copied from 2.6 for
    2.4.
    
    Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    check_call(["ls", "-l"])
    """    
    if subprocess.call(cmd, *args, **kw) != 0:
        raise CalledProcessError("Command '%s' returned non-zero exit status 1" 
                                 % str(cmd))    
# For  convenience   
def call(*args, **kw):
    """Run command with arguments.  Wait for command to complete, then
    return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])
    """
    return subprocess.call(*args, **kw)


def hostusername():
    try:
        return os.getlogin()
    except OSError:
        return os.environ['LOGNAME']

class InvalidArguments(SoftException): pass




def assert_args(f, function_args, ignore=0):
    
    (args,
     varargs,
     keywords,
     defaults) = inspect.getargspec(f)
    
    
    supplied_arg_count = len(function_args)
    
    # Methods of objects automatically get +1 arg for the object itself
    # We can ignore that.
    if hasattr(f, 'im_self'):
        ignore += 1
    
    # How many  arguments with default values we have
    if defaults:
        default_count = len(defaults)
    else:
        default_count = 0
    
    
    # Compute how many arguments we really need
    required_args_count = len(args) - default_count - ignore
    
    
    max_str = ""
    if varargs:
        max_str = "-n"
    if default_count > 0:
        max_str = "-%s" % (required_args_count + default_count)
     
    required = "Required %s%s arguments" % (required_args_count,
                                            max_str) 
        
    if supplied_arg_count == required_args_count:
        return
    
    # More than required is ok, if function has *args arg
    if varargs and supplied_arg_count > required_args_count:
        return
    
    if default_count:
        redundant_arg_count = supplied_arg_count - required_args_count
        
        # Negative redundant_arg_count means that we have to few
        # arguments.
        if redundant_arg_count > 0 and redundant_arg_count <= default_count:
            return
        
    
    
    raise InvalidArguments("Invalid argument count %s. %s." 
                           % (supplied_arg_count, required))
    
        

def _default_name(f):
    return f.__name__.replace("_", "-")


def expose(f, *cmd_names):
    if not cmd_names:
        # Use name of the function if no name is supplied
        active.cmds[_default_name(f)] = f
    else:
        for name in cmd_names:
            active.cmds[name] = f    
    

def expose_as(*cmd_names):
    """Decorator for exposing functions as subssh commands"""
    
    def expose_function(f):
        expose(f, *cmd_names)
        return f
        
    return expose_function




def exposable_as(*cmd_names):
    """
    Methods decorated with this will marked as exposable.
    Methods can be exposed with expose_instance.
    """
    def set_exposed_name(f):
        if cmd_names:
            f.exposed_names = cmd_names
        else:
            f.exposed_names = _default_name(f),
        return f
    
    return set_exposed_name



def expose_instance(obj):
    for key, method in inspect.getmembers(obj):
        if hasattr(method, "exposed_names"):
            
            prefix = getattr(obj, "cmd_prefix", "")
            suffix = getattr(obj, "cmd_suffix", "")
            
            wrapped_names = [prefix + name + suffix
                              for name in method.exposed_names]
            
            expose(method, *wrapped_names)
            




is_inactive = lambda req: not req and req != 0
def require_args_deprecated(exactly=None, at_least=None, at_most=None):
    """
    Decorator for setting constraints for arguments of a command.
    
    Raises  InvalidArguments exception if command 
    is not supplied with required amount of arguments
    """
     
    requirements = (lambda count: is_inactive(exactly) or count == exactly,
                    lambda count: is_inactive(at_least) or count >= at_least, 
                    lambda count: is_inactive(at_most) or count <= at_most)

    
    def wrapper(f):
        def args_wrapper(*function_args):
            # Funtion decorator
            if len(function_args) == 3:
                username, cmd, args = function_args
            # Method decorator
            elif len(function_args) == 4:
                obj, username, cmd, args = function_args
            else:
                raise TypeError("require_args-decorator takes 3-4 arguments")
            
            for require in requirements:
                if not require(len(args)):
                    msg = "Required arguments "
                    if exactly:
                        msg += "exactly %s. " % exactly 
                    if at_least:
                        msg += "at least %s. " % at_least 
                    if at_most:
                        msg += "at most %s. " % at_most                                                 
                        
                    raise InvalidArguments(msg)
                
            return f(*function_args)
        args_wrapper.__name__ = f.__name__
        args_wrapper.__doc__ = f.__doc__
        args_wrapper.__dict__ = f.__dict__
        return args_wrapper
    
        
    return wrapper



if __name__ == "__main__":
    def bar(eka, toka):
        pass
    
    def foo(valu):
        bar(1,2)
        
        
    try:
        foo()
    except TypeError, e:
        print traceback.extract_stack()
        t =  sys.exc_info()
        print t




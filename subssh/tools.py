# -*- coding: utf-8 -*-
'''
Created on Mar 8, 2010

@author: epeli
'''

import sys
import os
import subprocess
import re



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


is_inactive = lambda req: not req and req != 0
def require_args(exactly=None, at_least=None, at_most=None):
    """Raise  InvalidArguments exception with doc string of the command if it 
    is not supplied with required amount of arguments
    """
     
    requirements = (
                  lambda count: is_inactive(exactly) or count == exactly,
                  lambda count: is_inactive(at_least) or count >= at_least, 
                  lambda count: is_inactive(at_most) or count <= at_most,
                  )
    
    def decorator(f):
        def args_wrapper(*function_args):
            # Funtion decorator
            if len(function_args) == 3:
                username, cmd, args = function_args
            # Method decorator
            elif len(function_args) == 4:
                obj, username, cmd, args = function_args
            else:
                raise TypeError("require_args-decorator takes 3-4 arguments")
            
            for requirement in requirements:
                if not requirement(len(args)):
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
        
    return decorator

if __name__ == "__main__":
    
    @require_args(3)
    def app(username, cmd, args):
        """%(name)s lol"""
        print "hello"
        
    print app
    app("esa", "testingapp", [1, 2])
        




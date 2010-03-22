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
    






def writeln(msg, out=sys.stdout, log=None):
    if log:
        log(msg)
    out.write("%s\n"  % msg)

def errln(msg, log=None):
    writeln(msg, out=sys.stderr, log=log)
    


class CalledProcessError(OSError):
    pass

def check_call(cmd, *args, **kw):
    """
    subprocess.check_call is new in Python 2.5.
    """
    if subprocess.call(cmd, *args, **kw) != 0:
        raise CalledProcessError("Command '%s' returned non-zero exit status 1" 
                                 % str(cmd))    

def admin_name():
    try:
        return os.getlogin()
    except OSError:
        return os.environ['LOGNAME']

class InvalidArguments(SoftException): pass

def require_args(exactly=None, at_least=None, at_most=None):
    """Raise  InvalidArguments exception with doc string of the command if it 
    is not supplied with required amount of arguments
    """
    
    requirements = (
                  # Return Falsy when ok 
                  lambda count: exactly and count != exactly,
                  lambda count: at_least and count < at_least, 
                  lambda count: at_most and count > at_most,
                  )
    
    
    def decorator(f):
        def args_wrapper(*function_args):
            # Funtion decorator
            if len(function_args) == 3:
                username, cmd, args = function_args
            # Method decorator
            elif len(function_args) == 4:
                obj, username, cmd, args = function_args
            
            for requirement in requirements:
                if requirement(len(args)):
                    # Raise SoftException with doc string
                    raise InvalidArguments("\n\n" + f.__doc__ % dict(name=cmd))
                
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
        




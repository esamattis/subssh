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
    



def default_to_doc(f):
    """Print documentation when app is run without any arguments"""
    def args_checker(username, cmd, args):
        if not args:
            errln(f.__doc__)
            return 1
        else:
            return f(username, cmd, args)
    args_checker.__dict__ = f.__dict__
    args_checker.__doc__ = f.__doc__
    args_checker.__name__ = f.__name__
    return args_checker    


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
        




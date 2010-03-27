# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Esa-Matti Suuronen <esa-matti@suuronen.org>

This file is part of subssh.

Subssh is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Subssh is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public 
License along with Subssh.  If not, see 
<http://www.gnu.org/licenses/>.
"""

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
            

class UserException(Exception):
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
    exitstatus = subprocess.call(cmd, *args, **kw)
    if exitstatus != 0:
        raise CalledProcessError(exitstatus, 
                                 "Command '%s' returned non-zero exit status 1" 
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



class InvalidArguments(UserException): pass




def assert_args(f, function_args, ignore=0):
    
    (args,
     varargs,
     keywords,
     defaults) = inspect.getargspec(f)
    
    
    supplied_arg_count = len(function_args)
    
    # Methods of objects automatically get +1 arg for the object itself
    # We can ignore that.
    if inspect.ismethod(f):
        ignore += 1
    
    # How many  arguments with default values we have
    if defaults:
        default_count = len(defaults)
    else:
        default_count = 0
    
    
    # Compute how many arguments we really need
    required_args_count = len(args) - default_count - ignore
    
    
    # Build error message
    if varargs:
        max_str = "-n"
    elif default_count > 0:
        max_str = "-%s" % (required_args_count + default_count)
    else:
        max_str = ""
     
    required = "Required %s%s arguments" % (required_args_count,
                                            max_str) 
        
    if supplied_arg_count == required_args_count:
        return
    
    # More than required is ok, if function has *args arg
    if varargs and supplied_arg_count > required_args_count:
        return
    
    if default_count:
        redundant_arg_count = supplied_arg_count - required_args_count
        
        # Negative redundant_arg_count means that we have too few
        # arguments.
        if redundant_arg_count > 0 and redundant_arg_count <= default_count:
            return
        
    
    
    raise InvalidArguments("Invalid argument count %s. %s." 
                           % (supplied_arg_count, required))
    
        










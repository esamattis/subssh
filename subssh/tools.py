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
import inspect
import getpass
from string import Template
from optparse import OptionParser

import config
import customlogger
logger = customlogger.get_logger(__name__)

username_chars = r"a-zA-Z_-"

safe_chars = r"a-zA-Z0-9_\-\."

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

_LOWER_BOOL_STRS_TRUE = ("true", "1", "enabled", "yes")
_LOWER_BOOL_STRS_FALSE = ("false", "0", "disabled", "no")

def to_bool(value):
    """Return a boolean value represented by `value` string.

    Valid values for True: "true", "1", "enabled" or "yes"
    Valid values for False: "false", "0", "disabled" or "no"

    Case of the `value` is ignored. Raise ValueError if `value` is invalid.
    """

    val = value.lower()
    if val in _LOWER_BOOL_STRS_TRUE:
        return True
    elif val in _LOWER_BOOL_STRS_FALSE:
        return False
    raise ValueError("%s is not a valid boolean value" % value)


def writeln(msg="", out=sys.stdout, log=None, indent=None):
    if log and msg:
        log(msg)

    if indent != None:
        for line in msg.split("\n"):
            out.write("%s%s\n"  %  (" "*indent, line.strip() ))

    else:
        out.write("%s\n"  % msg)

def errln(msg, log=None, indent=None):
    writeln(msg, out=sys.stderr, log=log, indent=indent)



class CalledProcessError(Exception):
    """This exception is raised when a process run by check_call() returns
    a non-zero exit status.  The exit status will be stored in the
    returncode attribute."""
    def __init__(self, returncode, cmd):
        self.returncode = returncode
        self.cmd = cmd
        self.args[returncode, cmd]
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





def expand_subssh_vars(template, **extra):
        tmpl_o = Template(template)
        return tmpl_o.substitute(
                                hostname=config.DISPLAY_HOSTNAME,
                                hostusername=hostusername(),
                                **extra)



class InvalidArguments(UserException): pass

def assert_args(f, function_args, ignore=0):
    """
    Assert that given function_args-list is valid input for function f.
    If this function does not raise InvalidArguments it should be safe to call:

        f(*function_args)

    """

    # We could use just try-except for detecting invalid arguments given by the
    # Subssh user, but that's not really wise, since the same exception could
    # be risen by a bug in subsequent function calls in Subssh. Nobody likes
    # eating bugs.


    ## Start by collecting required data from the given function

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





    ## Assert arguments

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




    ## Build error message and throw it

    if varargs:
        max_str = "-n"
    elif default_count > 0:
        max_str = "-%s" % (required_args_count + default_count)
    else:
        max_str = ""

    required = "Required %s%s arguments" % (required_args_count,
                                            max_str)

    raise InvalidArguments("Invalid argument count %s. %s."
                           % (supplied_arg_count, required))








def get_user_ip():

    try:
        return os.environ['SSH_CONNECTION'].split()[0]
    except KeyError:
        # User invoked locally the subssh shell, not over SSH
        return  "direct"



def get_local_cmd():
    """
    Get command given by local user
    """

    cmd_pos = 1

    # This is bit cheap. 
    if len(sys.argv) > 1 and sys.argv[1] in ('-t', '--ssh-tunnel'):
        cmd_pos += 2

    try:
        cmd = sys.argv[cmd_pos]
    except IndexError:
        # No command given
        return "", []

    return cmd, sys.argv[cmd_pos+1:]



def get_ssh_cmd():
    """
    Get command given by ssh user
    """

    try:
        ssh_original_command = os.environ['SSH_ORIGINAL_COMMAND']
    except KeyError:
        # No command given
        return "", []

    # Clean up the original command
    parts = [part.strip("'\" ") for part in ssh_original_command.split()]

    cmd = parts[0]
    args = parts[1:]
    return cmd, args


# Just a convience object
class UserRequest(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

def hostusername():
    return getpass.getuser()





parser = OptionParser()
parser.add_option("-t", "--ssh-tunnel", dest="ssh_username",
                  help="Run subssh as user. Command is read from "
                  "SSH_ORIGINAL_COMMAND enviroment variable.",
                  metavar="<username>")


def get_user():

    options, args = parser.parse_args()

    if options.ssh_username:
        username = options.ssh_username
    else:
        username = hostusername()

    if get_user_ip() == "direct":
        cmd, args = get_local_cmd()
    else:
        cmd, args = get_ssh_cmd()

    return UserRequest(username=username,
                       cmd=cmd,
                       args=args,
                       from_ssh=bool(options.ssh_username),
                       logger=customlogger.get_user_logger(username))




def create_required_directories_or_die(directories):
    """
    Try to create directories in given order. Raises SystemExit if creation fails
    """
    for dir in directories:
        if not os.path.exists(dir):
            try:
                os.mkdir(dir)
            except OSError, e:
                sys.stderr.write("Cannot create dir '%s' Reason: %s \n"
                                 % (dir, " ".join(e.args()) ))
                sys.exit(1)

# http://hacktux.com/bash/colors
colors = {
    "black":        "0;30",
    "dark gray":    "1;30",
    "light gray":   "0;37",
    "blue":         "0;34",
    "light blue":   "1;34",
    "green":        "0;32",
    "light green":  "1;32",
    "cyan":         "0;36",
    "light cyan":   "1;36",
    "red":          "0;31",
    "light red":    "1;31",
    "purple":       "0;35",
    "light purple": "1;35",
    "brown":        "0;33",
    "yellow":       "1;33",
    "white":        "1;37",
}

def set_text_color(color):
    """
    Change terminal text color.
    """
    sys.stderr.write( "\033[%sm" % colors[color])

def reset_text_color():
    sys.stderr.write("\033[00m")


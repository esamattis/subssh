# -*- coding: utf-8 -*-
'''
Created on Mar 8, 2010

@author: epeli
'''

import sys
import subprocess
import re



safe_chars = r"a-z_A-Z\-\."

safe_chars_only_pat = re.compile(r"^[%s]+$" % safe_chars )


not_safe_char = re.compile(r"[^%s]{1}" % safe_chars)
def to_safe_chars(string):
    string = string.replace("ä", "a")
    string = string.replace("Ä", "A")
    string = string.replace("ö", "o")
    string = string.replace("Ö", "O")
    string = string.replace(" ", "_")
    return not_safe_char.sub("", string)
            

def no_user(f):
    f.no_user = False
    return f
    
    

def parse_cmd(f):
    def parse(username, ssh_original_command): 
        parts = ssh_original_command.split()
        cmd = parts[0]
        args = [arg.strip('"').strip("'") for arg in parts[1:]]
        return f(username, cmd, args)
    parse.__dict__ = f.__dict__
    parse.__doc__ = f.__doc__
    parse.__name__ = f.__name__
    
    
    
    return parse


def writeln(msg, out=sys.stdout):
    out.write("%s\n"  % msg)

def errln(msg):
    writeln(msg, out=sys.stderr)
    


class CalledProcessError(OSError):
    pass

def check_call(cmd, *args, **kw):
    """
    subprocess.check_call is new in Python 2.5.
    """
    if subprocess.call(cmd, *args, **kw) != 0:
        raise CalledProcessError("Command '%s' returned non-zero exit status 1" 
                                 % str(cmd))    


if __name__ == "__main__":
    
    @parse_cmd
    def test(cmd, args):
        print cmd, args
        
        
    test("customcmd arg1 arg2")

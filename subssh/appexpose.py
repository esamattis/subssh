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

import inspect

import active



def gen_default_name(f):
    return f.__name__.replace("_", "-")


def expose(f, *cmd_names):
    names = list(cmd_names)
    if not names:
        # Use name of the function if no name is supplied
        names.append( gen_default_name(f) )
    
    for name in names:
        active.cmds[name] = f
        


def expose_instance(obj, prefix="", suffix=""):
    for key, method in inspect.getmembers(obj):
        if hasattr(method, "exposed_names"):
            
            
            wrapped_names = [prefix + name + suffix
                              for name in method.exposed_names]
            
            expose(method, *wrapped_names)
            




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
            f.exposed_names = gen_default_name(f),
        return f
    
    return set_exposed_name


def no_interactive(f):
    """Cannot be user interactively"""
    f.disable_interactive = True
    return f

def no_direct_access(f):
    """Cannot be user directly. Interactive usage only"""
    f.disable_direct = True
    return f

    


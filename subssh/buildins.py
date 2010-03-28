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

import os
from string import Template


import subssh
import active
import config
import tools


@subssh.expose_as()
def commands(user):
    """List all commands."""
    
    
    for name, app in sorted(active.user_apps()):
        if app.__doc__:
            doc = [line.strip() # Get first line with content 
                   for line  in app.__doc__.split("\n") 
                   if line.strip()][0]
        else:
            doc = "%s has no doc string" % name
            
        tools.writeln("%s - %s" % ( name, doc ))
        



@subssh.expose_as()
def help(user):
    """Show help."""
    tools.writeln(
"""
    type commands to list all available commands.
     
        man <command> 
    
    will display the command's doc string
""")    
    
    
    
    
    
    
    
@subssh.expose_as("exit", "logout")    
def exit(user, exitstatus=0):
    """
    Logout from subssh.
    
    usage: exit [exit status]
    
    Pro tip: Hit Ctrl+d to logout.
    """
    try:
        return int(exitstatus)
    except ValueError:
        raise subssh.UserException("Bad exits status %s" % exitstatus)

@subssh.expose_as("version")
def version(user):
    """
    Displays the version number of subssh
    """
    this_dir = os.path.dirname(__file__)
    f = open(os.path.join(this_dir,'version.txt'), 'r')
    version = f.read()
    f.close()
    print version



@subssh.expose_as("man")
def show_doc(user, command):
    """
    Show man page of a command.
    
    usage: man <command>
    """
    try:
        doc_tmpl = active.cmds[command].__doc__
    except KeyError:
        subssh.errln("Unkown command '%s'" % command)
        return 1
    
    if doc_tmpl:
        # Set document variables
        doc = Template(doc_tmpl).substitute(cmd=command,
                                            hostname=config.DISPLAY_HOSTNAME,
                                            hostusername=subssh.hostusername())
        subssh.writeln(doc)
    else:
        subssh.writeln("'%s' has no doc string" % command)
    

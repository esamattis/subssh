'''
Created on Mar 25, 2010

@author: epeli
'''
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
    

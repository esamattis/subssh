'''
Created on Mar 25, 2010

@author: epeli
'''
from string import Template


import tools
import active
import config





@tools.expose_as()
def commands(user):
    """List all commands."""
    
    for name, app in sorted(active.user_apps()):
        first_line = [line.strip() 
                 for line  in app.__doc__.split("\n") 
                 if line.strip()][0]
        tools.writeln("%s - %s" % ( name, first_line ))
        



@tools.expose_as()
def help(user):
    """Show help."""
    tools.writeln(
"""
    type commands to list all available commands.
     
        man <app> 
    
    will display the command's doc string
""")    
    
    
    
    
    
    
    
    
@tools.expose_as("exit", "logout")    
def exit(user, exitstatus=0):
    """
    Logout from subssh.
    
    usage: exit [exit status]
    
    Pro tip: Hit Ctrl+d to logout.
    """
    try:
        return int(exitstatus)
    except ValueError:
        raise tools.SoftException("Bad exits status %s" % exitstatus)
    




@tools.expose_as("man")
def show_doc(user, command="man"):
    """
    Show man page of a command.
    
    usage: man <another command>
    """
    try:
        doc_tmpl = active.cmds[command].__doc__
    except KeyError:
        tools.errln("Unkown command '%s'" % command)
        return 1
    
    if doc_tmpl:
        # Set document variables
        doc = Template(doc_tmpl).substitute(cmd=command,
                                            hostname=config.DISPLAY_HOSTNAME,
                                            hostusername=tools.hostusername())
        tools.writeln(doc)
    else:
        tools.writeln("'%s' has no doc string" % command)
    
active.cmds["man"] = show_doc    

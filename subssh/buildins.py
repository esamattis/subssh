'''
Created on Mar 25, 2010

@author: epeli
'''
from string import Template


import tools
import active
import config






def commands(username, cmd, args):
    """List all commands."""
    
    for name, app in sorted(active.user_apps()):
        first_line = [line.strip() 
                 for line  in app.__doc__.split("\n") 
                 if line.strip()][0]
        tools.writeln("%s - %s" % ( name, first_line ))
        
active.cmds["commands"] = commands




def help(username, cmd, args):
    """Show help."""
    tools.writeln(
"""
    type commands to list all available commands.
     
        man <app> 
    
    will display the command's doc string
""")    
    
active.cmds["help"] = help
    
    
    
    
    
    
    
    
def exit(username, cmd, args):
    """
    Logout from subssh.
    
    usage: exit [exit status]
    
    Pro tip: Hit Ctrl+d to logout.
    """
    try:
        return int(args[0])
    except (ValueError, IndexError):
        return 0
    
active.cmds["exit"] = exit
active.cmds["logout"] = exit





@tools.require_args(exactly=1)
def show_doc(username, cmd, args):
    """
    Show man page of a command.
    
    usage: man <another command>
    """
    try:
        doc_tmpl = active.cmds[args[0]].__doc__
    except IndexError:
        doc_tmpl = show_doc.__doc__
    except KeyError:
        tools.errln("Unkown command '%s'" % args[0])
        return 1
    
    if doc_tmpl:
        # Set document variables
        doc = Template(doc_tmpl).substitute(cmd=args[0],
                                            hostname=config.DISPLAY_HOSTNAME,
                                            hostusername=tools.hostusername())
        tools.writeln(doc)
    else:
        tools.writeln("'%s' has no doc string" % args[0])
    
active.cmds["man"] = show_doc    

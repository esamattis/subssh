'''
Created on Mar 20, 2010

@author: epeli
'''


import readline


import apploader
import tools
import config
import active




def complete(text, state):
    for cmd, app in active.user_apps():
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


readline.set_completer_delims(' `~!@#$%^&*()=+[{]}\|;:\'",<>/?')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def prompt(user):
    

    
    exit_status = 0
    cmd = ""
    args = []
    promt_str = "%s@%s> " % (user.username, config.DISPLAY_HOSTNAME)
    
    while cmd not in ("exit", "logout"):
        try:
            input = raw_input(promt_str)
        except KeyboardInterrupt:
            print
            continue
        except EOFError:
            print "exit",
            return 0
        
        cmd, args = tools.to_cmd_args(input)
        
        if not cmd:
            continue
        
        user.cmd = cmd
        exit_status = apploader.run(user, args)
        
    return exit_status

    
